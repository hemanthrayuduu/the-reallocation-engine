#!/usr/bin/env python3
"""swe-sponsor-pipeline — live SWE/AI postings at companies with a sponsorship record.

For one persona (an MS CS student graduating in December, OPT not yet started) this:

  1. filters the 80 Days CSV to companies that sponsored H-1B for software / ML titles
     and raised money inside the persona's funding window            (record)
  2. cross-checks each against the shipped Form D samples              (record)
  3. guesses each company's Greenhouse / Ashby board from its name and website,
     fetches it through greenhouse-watch's allow-listed fetcher        (record)
  4. turns every US, right-level, target-family posting whose DESCRIPTION does not rule the
     persona out (citizenship / clearance / no-sponsorship / too many years) into one role, and labels its
     evidence: sponsorship tier, fit, liveness, timeline               (record / your-input)
  5. scores the roles with the REAL scripts/score/role-scorer.mjs (subprocess, --out-dir)
  6. buckets the scorer's output: apply · consider · network · check-by-hand · skip
  7. writes pipeline-log.json (agent) and pipeline-report.md (human)

Every threshold lives in rules.json or the persona file — none in this code.

    python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py
    python3 .../pipeline.py --offline .../fixtures/boards --csv .../fixtures/80days.fixture.csv ...

Exit 0 on a completed run; exit 1 with an ERROR line (and no invented value) on a named
failure: unreadable input, OPT window already closed, scorer failure.
"""
from __future__ import annotations

import argparse
import ast
import calendar
import csv
import datetime as dt
import glob
import hashlib
import importlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
import types
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

DEFAULTS = {
    "persona": "search/examples/kiran-rao/persona.json",
    "rules": str(HERE.relative_to(REPO) / "rules.json"),
    "csv": "data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv",
    "bls": "data/bls/compact/soc_occupation_compact.csv",
    "formd": "data/sec/form-d/processed/sample/*.sample.json",
}
SCORER = REPO / "scripts/score/role-scorer.mjs"
REC, INP = "record", "your-input"  # model-judgment is never produced by this pipeline


class InputError(Exception):
    """A named failure: report it, write nothing invented, exit 1."""


# ───────────────────────────────────────────────────────────── reused repo code
def load_greenhouse_watch():
    """The greenhouse-watch skill's allow-listed fetcher, job normaliser and fit scheme."""
    path = REPO / ".claude/skills/greenhouse-watch/scripts/greenhouse_watch.py"
    spec = importlib.util.spec_from_file_location("greenhouse_watch", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_normalize():
    """scripts/ats/scrapers/common/normalize.py, imported WITHOUT running the package
    __init__ (which pulls in `requests` via retry.py — not stdlib, absent on a fresh clone)."""
    base = REPO / "scripts/ats/scrapers"
    for name, path in (("scrapers", base), ("scrapers.common", base / "common")):
        if name not in sys.modules:
            pkg = types.ModuleType(name)
            pkg.__path__ = [str(path)]
            sys.modules[name] = pkg
    return importlib.import_module("scrapers.common.normalize")


GW = load_greenhouse_watch()
NORM = load_normalize()


# ───────────────────────────────────────────────────────────── small helpers
def rel(p) -> str:
    try:
        return str(Path(p).resolve().relative_to(REPO))
    except ValueError:
        return str(p)


def sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path, what):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise InputError(f"{what} not found: {path}")
    except json.JSONDecodeError as e:
        raise InputError(f"{what} is not valid JSON ({path}): {e}")


def parse_date(value, field) -> dt.date:
    try:
        return dt.date.fromisoformat(str(value).strip()[:10])
    except (ValueError, TypeError):
        raise InputError(f"{field} is not a YYYY-MM-DD date: {value!r}")


def months_before(d: dt.date, months: int) -> dt.date:
    y, m = divmod(d.year * 12 + (d.month - 1) - months, 12)
    return dt.date(y, m + 1, min(d.day, calendar.monthrange(y, m + 1)[1]))


def to_num(x):
    try:
        v = float(str(x).replace(",", "").strip())
        return v if v == v else None  # NaN guard
    except (ValueError, TypeError):
        return None


CSV_COLUMNS = ("company_name", "website", "Total Approvals", "Total Denials", "Approval_Rate",
               "top_job_titles_sponsored", "latest_funding_date", "latest_funding_amount", "latest_funding_stage", "total_funding")
BLS_COLUMNS = ("onet_soc_code", "title", "alternate_titles_sample", "annual_median_wage", "job_zone", "cognitive_pivot_score", "oews_year")


def refuse_tracked_out_dir(out_dir):
    """Never write over a file this tool didn't write, and never over a tracked repo file.
    1. Works without git (e.g. an unzipped submission): an existing, non-empty folder is refused unless it holds this
       tool's own earlier pipeline-log.json.
    2. Inside a git checkout, additionally: a folder holding any git-tracked file is refused."""
    if out_dir.exists() and any(out_dir.iterdir()):
        own = False
        try:
            own = json.loads((out_dir / "pipeline-log.json").read_text(encoding="utf-8")).get("_tool") == "swe-sponsor-pipeline"
        except (OSError, ValueError, AttributeError):
            own = False
        if not own:
            raise InputError(f"refusing to write into {rel(out_dir)}: it already holds files this tool did not write. "
                             f"Choose an empty or new --out-dir, or omit it to use the gitignored default.")
    try:
        proc = subprocess.run(["git", "-C", str(REPO), "ls-files", "--", str(out_dir)],
                              capture_output=True, text=True, timeout=30)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return  # no git: no tracked files exist to overwrite; check 1 above still applied
    if proc.returncode == 0 and proc.stdout.strip():
        n = len(proc.stdout.strip().splitlines())
        raise InputError(f"refusing to write into {rel(out_dir)}: it holds {n} git-tracked file(s), and this tool never "
                         f"writes over a tracked repo file. Choose another --out-dir, or omit it to use the gitignored default.")


def require_columns(found, needed, path, what):
    """A conformance check, not an audit: a wrong-schema file halts the run instead of yielding '0 candidates'."""
    missing = [c for c in needed if c not in (found or [])]
    if missing:
        raise InputError(f"{what} {rel(path)} is missing columns {missing} — wrong file or schema change; nothing scored")


def lab(value, source, **extra):
    """Every value in the log is {value, source[, note…]}."""
    return {"value": value, "source": source, **extra}


def money(v):
    return "—" if v is None else f"${v:,.0f}"


# ───────────────────────────────────────────────────────────── rules applied to records
def family_of(title, rules):
    """First family (in rules.json order) whose phrase, or role-word + AI-word pair, is in the title."""
    t = (title or "").lower()
    for fam, spec in rules["title_families"].items():
        if any(GW.phrase_in(p, t) for p in spec["patterns"]):
            return fam
        combo = spec.get("also_if_title_has_role_word_and_ai_word")
        if (combo and any(GW.phrase_in(w, t) for w in combo["role_words"]) and any(GW.phrase_in(w, t) for w in combo["ai_words"])
                and not any(GW.phrase_in(w, t) for w in combo.get("not_if_title_has", []))):
            return fam
    return None


def target_families(persona, rules):
    fams = persona.get("target_families") or list(rules["title_families"])
    unknown = [f for f in fams if f not in rules["title_families"]]
    if unknown:
        raise InputError(f"persona target_families {unknown} are not families in rules.json {list(rules['title_families'])}")
    return fams


def no_sponsorship_phrase(job, rules):
    text = (GW.strip_html(job.get("content") or "") + " " + (job.get("title") or "")).lower()
    for ph in (rules.get("description_rules") or {}).get("no_sponsorship_phrases", []):
        if GW.phrase_in(ph, text):
            return ph
    return None


def description_check(job, rules, persona):
    """Rules applied to the posting text (record). Returns (ruled_out_reason or None, info)."""
    d = rules.get("description_rules") or {}
    text = (GW.strip_html(job.get("content") or "") + " " + (job.get("title") or "")).lower()
    info = {"years_required": None, "years_mentions": [], "matched_phrase": None,
            "stack_terms": [s for s in rules.get("microsoft_ai_stack_terms", []) if GW.phrase_in(s, text)]}
    for key, label in (("eligibility_exclude_phrases", "eligibility"), ("no_sponsorship_phrases", "no-sponsorship")):
        for ph in d.get(key, []):
            if GW.phrase_in(ph, text):
                info["matched_phrase"] = ph
                return f"{label}: description says «{ph}»", info
    y = d.get("years_of_experience")
    if y is not None and persona.get("experience_years") is not None:
        lows = []
        for m in re.finditer(r"(\d{1,2})\s*\+?\s*(?:(?:-|–|to)\s*(\d{1,2})\s*\+?\s*)?years?\b(?=[^.;]{0,60}?experience)", text):
            lows.append(int(m.group(1)))
            info["years_mentions"].append(m.group(0).strip())
        if lows:
            info["years_required"] = min(lows)
            limit = persona["experience_years"] + y.get("tolerance_years", 0)
            if min(lows) > limit:
                return (f"experience: description asks for {min(lows)}+ years (lowest stated), "
                        f"above persona {persona['experience_years']} + tolerance {y.get('tolerance_years', 0)}"), info
    return None, info


def sponsored_titles(raw):
    raw = (raw or "").strip()
    if not raw:
        return []
    try:
        v = ast.literal_eval(raw)
        return [str(x) for x in v] if isinstance(v, (list, tuple)) else [str(v)]
    except (ValueError, SyntaxError):
        return [raw]


def location_class(loc, rules):
    """us · remote-unstated · unstated · non-us"""
    u = rules["us_location"]
    s = (loc or "").strip()
    if not s:
        return "unstated"
    lc = s.lower()
    if any(t in lc for t in u["country_terms"]):
        return "us"
    if re.search(r"\bU\.?S\.?(A\.?)?(?![A-Za-z])", s):  # "Anywhere in the US", "U.S.", "USA" (case-sensitive: not "us")
        return "us"
    if any(GW.phrase_in(n, lc) for n in u["state_names"] + u["city_names"]):
        return "us"
    abbr = "|".join(u["state_abbreviations"])
    if re.search(rf"(?:,|\s-|\()\s*(?:{abbr})\b(?!\.?\s*[a-z])", s):
        return "us"
    residual = re.sub(r"remote|anywhere|worldwide|global|hybrid|[^a-z]", "", lc)
    if "remote" in lc and not residual:
        return "remote-unstated"
    return "non-us"


def seniority_hit(title, rules):
    for pat in rules["seniority_exclude_patterns"]:
        if re.search(pat, title or "", re.I):
            return pat
    return None


def preferred_location(loc, persona):
    """your-input preference (persona.preferred_locations) applied to the posting location (record)."""
    pref = persona.get("preferred_locations") or {}
    s = loc or ""
    for term in pref.get("terms", []):
        if GW.phrase_in(term, s.lower()):
            return term
    abbr = "|".join(pref.get("state_abbreviations", []))
    if abbr and re.search(rf"(?:,|\s-|\()\s*(?:{abbr})\b", s):
        return abbr
    return None


def tier_for(approvals, same_family, rules):
    for t in rules["sponsorship_tiers"]:
        if approvals >= t["min_approvals"] and (same_family or not t["requires_same_family"]):
            return t["tier"], t["p"]
    return None, None


def timeline_gate(persona, today, rules):
    v = persona.get("visa") or {}
    opt = parse_date(v.get("opt_start_date"), "persona visa.opt_start_date")
    days = v.get("unemployment_days_allowed")
    lag = persona.get("hiring_lag_days")
    if not isinstance(days, (int, float)) or not isinstance(lag, (int, float)):
        raise InputError("persona needs numeric visa.unemployment_days_allowed and hiring_lag_days")
    window_end = opt + dt.timedelta(days=days)
    if today > window_end:
        raise InputError(f"OPT window already closed: opt_start_date {opt} + {days} unemployment days "
                         f"= {window_end}, which is before today {today}. No timeline factor computed.")
    available = (opt - today).days + days
    margin = available - lag
    full = rules["timeline"]["full_margin_days"]
    factor = 1.0 if margin >= full else (round(margin / full, 3) if margin > 0 else 0.0)
    return {
        "factor": factor,
        "opt_start_date": str(opt), "window_end": str(window_end),
        "available_days": available, "hiring_lag_days": lag, "margin_days": margin,
        "arithmetic": f"available = ({opt} − {today}) + {days} = {available} d; margin = {available} − {lag} = {margin} d; "
                      f"factor = {'1.0 (margin ≥ ' + str(full) + ')' if margin >= full else ('margin/' + str(full) if margin > 0 else '0 (closed)')} = {factor}",
    }


# ───────────────────────────────────────────────────────────── BLS / Form D lookups
def load_bls(path):
    rows, phrases = {}, []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        require_columns(reader.fieldnames, BLS_COLUMNS, path, "BLS compact CSV")
        for r in reader:
            code = r.get("onet_soc_code", "")
            rows[code] = r
            names = [re.sub(r"s$", "", (r.get("title") or "").strip())]
            names += [re.sub(r"\s*\(.*?\)", "", x).strip() for x in (r.get("alternate_titles_sample") or "").split(";")]
            for n in names:
                if len(n.split()) >= 2:
                    phrases.append((n.lower(), code, n))
    phrases.sort(key=lambda x: -len(x[0]))  # longest (most specific) match wins
    return rows, phrases


def soc_for(title, family, bls, rules):
    rows, phrases = bls
    t = (title or "").lower()
    for p, code, shown in phrases:
        if GW.phrase_in(p, t):
            return {"code": code, "via": f"posting title contains O*NET title «{shown}»", "source": REC, "row": rows.get(code)}
    hint = rules["title_families"].get(family, {}).get("soc_hint")
    if hint:
        return {"code": hint, "via": f"no O*NET title matched; family '{family}' soc_hint from rules.json",
                "source": INP, "row": rows.get(hint)}
    return {"code": None, "via": "no O*NET title matched and no soc_hint", "source": INP, "row": None}


def wage_context(soc):
    row = soc["row"]
    if row is None:
        return {"status": "unmapped", "soc": lab(soc["code"], soc["source"], via=soc["via"]),
                "note": f"SOC {soc['code']} has no row in the BLS file — no wage shown (none invented)"}
    out = {"status": "mapped", "soc": lab(soc["code"], soc["source"], via=soc["via"]),
           "soc_title": lab(row.get("title"), REC)}
    for k in ("annual_median_wage", "job_zone", "cognitive_pivot_score", "oews_year"):
        v = to_num(row.get(k))
        out[k] = lab(v, REC) if v is not None else lab(None, REC, note="blank in BLS file")
    return out


def load_formd(pattern):
    idx, files = {}, sorted(glob.glob(str(REPO / pattern) if not os.path.isabs(pattern) else pattern))
    for fp in files:
        data = load_json(fp, "Form D sample")
        for c in data.get("companies", []):
            name = (c.get("company") or {}).get("name") or ""
            fund, fil = c.get("funding") or {}, c.get("filing") or {}
            idx.setdefault(NORM.normalize_company_name(name), []).append({
                "file": rel(fp), "name": name, "date_filed": fil.get("date_filed"),
                "total_offering_amount": fund.get("total_offering_amount"),
                "total_amount_sold": fund.get("total_amount_sold"), "stage_estimate": fund.get("stage_estimate")})
    return idx, [rel(f) for f in files]


# ───────────────────────────────────────────────────────────── board discovery
class Fetcher:
    """Live: greenhouse-watch's allow-listed, no-redirect fetch_board. Offline: fixture files
    <dir>/<ats>-<slug>.json (absent → 404). Every response is saved raw for provenance."""

    def __init__(self, offline_dir, raw_dir, delay):
        self.offline_dir, self.raw_dir, self.delay = offline_dir, raw_dir, delay
        self.hosts, self.calls, self.raw_index = set(), 0, {}

    def get(self, url, key):
        if self.offline_dir:
            fp = Path(self.offline_dir) / f"{key}.json"
            if not fp.exists():
                return "not-found", None
            data = load_json(fp, "board fixture")
            if isinstance(data, dict) and "_simulate_error" in data:
                return f"fetch-failed: {data['_simulate_error']}", None
        else:
            GW.assert_allowed(url)
            self.hosts.add(url.split("/")[2])
            self.calls += 1
            time.sleep(self.delay)
            try:
                data = GW.fetch_board(url)
            except urllib.error.HTTPError as e:
                return ("not-found", None) if e.code == 404 else (f"fetch-failed: HTTP {e.code}", None)
            except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
                return f"fetch-failed: {type(e).__name__}: {e}", None
        # raw responses go to a gitignored .build/ (they carry company contact addresses);
        # the hash in the log keeps the provenance after .build/ is cleared
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        blob = json.dumps(data).encode("utf-8")
        (self.raw_dir / f"{key}.json").write_bytes(blob)
        self.raw_index[key] = {"path": rel(self.raw_dir / f"{key}.json"), "sha256": hashlib.sha256(blob).hexdigest()}
        return "ok", data


def slug_candidates(name, website):
    base = NORM.normalize_company_name(name)
    words = re.sub(r"[^a-z0-9 ]", " ", re.sub(r",?\s+(inc|llc|corp|corporation|co|ltd|limited|pbc)\.?$", "", name.strip(), flags=re.I).lower()).split()
    out = [base, "-".join(words)]
    w = (website or "").lower().strip()
    w = re.sub(r"^https?://", "", w)
    w = re.sub(r"^www\.", "", w).split("/")[0]
    if w and "." in w:
        out.append(w.split(".")[0])
    seen, uniq = set(), []
    for s in out:
        if s and s not in seen and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", s):
            seen.add(s)
            uniq.append(s)
    return uniq


def same_company(csv_name, board_name):
    a, b = NORM.normalize_company_name(csv_name), NORM.normalize_company_name(board_name or "")
    return bool(a and b) and (a == b or a.startswith(b) or b.startswith(a))


def discover(company, fetcher, rules):
    attempts, mismatch = [], None
    for ats in rules["discovery"]["ats_order"]:
        for slug in slug_candidates(company["name"], company["website"]):
            try:
                url = GW.board_url(slug, content=True, ats=ats)
            except GW.InputError as e:
                attempts.append({"ats": ats, "slug": slug, "status": f"invalid-slug: {e}"})
                continue
            status, data = fetcher.get(url, f"{ats}-{slug}")
            attempts.append({"ats": ats, "slug": slug, "url": url, "status": status})
            if status != "ok":
                continue
            identity = lab("unverified", INP, note="Ashby's board API returns no company name; a human confirms at gate G1")
            if ats == "greenhouse":
                mstatus, meta = fetcher.get(f"https://boards-api.greenhouse.io/v1/boards/{slug}", f"{ats}-{slug}.meta")
                bname = (meta or {}).get("name") if mstatus == "ok" else None
                if bname and not same_company(company["name"], bname):
                    mismatch = {"ats": ats, "slug": slug, "board_name": bname}
                    attempts[-1]["status"] = f"identity-mismatch: board name «{bname}»"
                    continue
                identity = (lab("confirmed", REC, note=f"board name «{bname}» matches CSV name") if bname
                            else lab("unverified", INP, note=f"board meta fetch: {mstatus}"))
            jobs = data.get("jobs") if isinstance(data, dict) else None
            if not isinstance(jobs, list):
                attempts[-1]["status"] = "fetch-failed: response has no jobs list"
                continue
            if ats == "ashby":
                jobs = [j for j in jobs if j.get("isListed", True)]
            return {"status": "found", "ats": ats, "slug": slug, "url": url, "identity": identity,
                    "jobs": GW.normalize_jobs(jobs, ats), "attempts": attempts}
    failed = [a for a in attempts if a["status"].startswith("fetch-failed")]
    status = "identity-mismatch" if mismatch else ("fetch-failed" if failed else "not-found")
    return {"status": status, "attempts": attempts, "mismatch": mismatch}


# ───────────────────────────────────────────────────────────── candidates from the CSV
def load_candidates(csv_path, persona, rules, today, only):
    window_start = months_before(today, int(persona["funding_window_months"]))
    targets = target_families(persona, rules)
    # which sponsored-title families count as sponsorship EVIDENCE (persona); postings must still be in `targets`
    evidence = persona.get("sponsorship_evidence_families") or targets
    unknown = [f for f in evidence if f not in rules["title_families"]]
    if unknown:
        raise InputError(f"persona sponsorship_evidence_families {unknown} are not families in rules.json")
    funnel = {"csv_rows": 0, "with_approvals": 0, "target_family_sponsored": 0, "funded_in_window": 0}
    cands, named = [], {}
    wanted = {NORM.normalize_company_name(n): n for n in (only or [])}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        require_columns(reader.fieldnames, CSV_COLUMNS, csv_path, "80 Days CSV")
        for r in reader:
            funnel["csv_rows"] += 1
            name = (r.get("company_name") or "").strip()
            key = NORM.normalize_company_name(name)
            if wanted and key not in wanted:
                continue
            approvals = to_num(r.get("Total Approvals")) or 0
            titles = sponsored_titles(r.get("top_job_titles_sponsored"))
            fams = sorted({fam for t in titles if (fam := family_of(t, rules)) and fam in evidence})
            fdate = (r.get("latest_funding_date") or "").strip()
            reason = None
            if approvals < persona["min_h1b_approvals"] or approvals <= 0:
                reason = f"no H-1B approvals on record (Total Approvals = {r.get('Total Approvals') or 'blank'})"
            else:
                funnel["with_approvals"] += 1
                if not fams:
                    reason = f"sponsored titles on record are not in the sponsorship-evidence families {evidence}"
                else:
                    funnel["target_family_sponsored"] += 1
                    try:
                        in_window = bool(fdate) and parse_date(fdate, "latest_funding_date") >= window_start
                    except InputError:
                        in_window = False
                    if not in_window:
                        reason = f"latest funding {fdate or 'blank'} is before the window start {window_start}"
                    else:
                        funnel["funded_in_window"] += 1
            if wanted:
                named[key] = reason or "candidate"
            if reason:
                continue
            cands.append({
                "name": name, "website": (r.get("website") or "").strip(),
                "approvals": approvals, "denials": to_num(r.get("Total Denials")),
                "approval_rate": to_num(r.get("Approval_Rate")), "titles": titles, "families": fams,
                "latest_funding_date": fdate, "latest_funding_amount": to_num(r.get("latest_funding_amount")),
                "latest_funding_stage": (r.get("latest_funding_stage") or "").strip() or None,
                "total_funding": to_num(r.get("total_funding")),
                "median_salary_offered": to_num(r.get("median_salary_offered")),
                "city": (r.get("city") or "").strip(), "state": (r.get("state") or "").strip(),
            })
    not_in_csv = [n for k, n in wanted.items() if k not in named]
    excluded_named = {wanted[k]: v for k, v in named.items() if v != "candidate"}
    cands.sort(key=lambda c: (-c["approvals"], c["name"]))
    return cands, funnel, window_start, not_in_csv, excluded_named


# ───────────────────────────────────────────────────────────── the run
def run(args):
    today = parse_date(args.today, "--today") if args.today else dt.date.today()
    persona_path = REPO / args.persona if not os.path.isabs(args.persona) else Path(args.persona)
    rules_path = REPO / args.rules if not os.path.isabs(args.rules) else Path(args.rules)
    csv_path = REPO / args.csv if not os.path.isabs(args.csv) else Path(args.csv)
    bls_path = REPO / args.bls if not os.path.isabs(args.bls) else Path(args.bls)
    for p, what in ((csv_path, "80 Days CSV"), (bls_path, "BLS compact CSV")):
        if not p.exists():
            raise InputError(f"{what} not found: {p}")

    persona = load_json(persona_path, "persona")
    rules = load_json(rules_path, "rules")
    for k in ("funding_window_months", "min_h1b_approvals", "resume"):
        if k not in persona:
            raise InputError(f"persona is missing {k!r}")
    resume_path = REPO / persona["resume"]
    resume = GW.load_resume(str(resume_path))
    scheme_path = REPO / rules["fit"]["scheme"]
    scheme = GW.load_scheme(str(scheme_path))
    feats = GW.resume_features(resume)
    timeline = timeline_gate(persona, today, rules)  # F3 raises here, before any fetch
    targets = target_families(persona, rules)

    mode = "offline" if args.offline else "live"
    # default: a gitignored folder inside this prototype's own folder, so the documented command never writes
    # over a tracked file (an earlier default, course/…/runs/<today>-live, collided with a committed run folder)
    out_dir = Path(args.out_dir) if args.out_dir else HERE / ".build" / "runs" / f"{today}-{mode}"
    if not out_dir.is_absolute():
        out_dir = REPO / out_dir
    refuse_tracked_out_dir(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fetcher = Fetcher(args.offline, out_dir / ".build" / "raw", 0 if args.offline else rules["discovery"]["probe_delay_seconds"])

    cands, funnel, window_start, not_in_csv, excluded_named = load_candidates(csv_path, persona, rules, today, args.company)
    funnel["candidates"] = len(cands)
    if args.limit:
        cands = cands[: args.limit]
    funnel["probed"] = len(cands)
    bls = load_bls(bls_path)
    formd, formd_files = load_formd(args.formd)

    tl_term = {"factor": timeline["factor"], "source": INP,
               "basis": "persona opt_start_date + unemployment_days_allowed − hiring_lag_days (rules.json timeline)"}
    companies, roles, role_meta = [], [], {}
    counts = {k: 0 for k in ("board_found", "board_not_found", "fetch_failed", "identity_mismatch",
                             "postings_seen", "postings_target_family", "postings_us", "postings_level_ok",
                             "postings_ruled_out_by_description", "postings_kept")}

    for i, c in enumerate(cands, 1):
        disc = discover(c, fetcher, rules)
        print(f"  [{i}/{len(cands)}] {c['name']}: {disc['status']}"
              + (f" {disc['ats']}:{disc['slug']} ({len(disc['jobs'])} postings)" if disc["status"] == "found" else ""),
              file=sys.stderr)
        fd = formd.get(NORM.normalize_company_name(c["name"]))
        ctier, cp = tier_for(c["approvals"], True, rules)
        comp = {
            "company": lab(c["name"], REC), "website": lab(c["website"] or None, REC),
            "h1b_total_approvals": lab(c["approvals"], REC), "h1b_total_denials": lab(c["denials"], REC),
            "h1b_approval_rate": lab(c["approval_rate"], REC),
            "sponsored_titles": lab(c["titles"], REC), "sponsored_families": lab(c["families"], INP, note="title_families rule applied to the record"),
            "latest_funding_date": lab(c["latest_funding_date"], REC), "latest_funding_amount": lab(c["latest_funding_amount"], REC),
            "latest_funding_stage": lab(c["latest_funding_stage"], REC), "total_funding": lab(c["total_funding"], REC),
            "form_d_sample": lab(fd, REC) if fd else lab(None, REC, note="no Form D sample match — funding from 80 Days CSV only"),
            "company_tier": lab(ctier, INP, note="sponsorship_tiers rule applied to approvals (record)"),
            "board": {"status": disc["status"], "attempts": disc["attempts"]},
        }
        if disc["status"] != "found":
            counts[{"not-found": "board_not_found", "fetch-failed": "fetch_failed",
                    "identity-mismatch": "identity_mismatch"}[disc["status"]]] += 1
            comp["bucket"] = "check-by-hand"
            comp["board"]["mismatch"] = disc.get("mismatch")
            companies.append(comp)
            continue
        counts["board_found"] += 1
        comp["board"].update({"ats": disc["ats"], "slug": disc["slug"], "url": disc["url"], "identity": disc["identity"]})
        pc = {"seen": 0, "other_family": 0, "non_us": 0, "seniority": 0, "description": 0, "kept": 0}
        excluded_examples, ruled_out, no_sponsor = [], [], []
        for job in disc["jobs"]:
            pc["seen"] += 1
            nsp = no_sponsorship_phrase(job, rules)  # company-wide: any posting, any family
            if nsp:
                no_sponsor.append({"title": lab(job.get("title"), REC), "url": lab(job.get("absolute_url"), REC),
                                   "phrase": lab(nsp, REC, note="no_sponsorship_phrases rule (your-input) matched in the posting text")})
            title = job.get("title") or ""
            fam = family_of(title, rules)
            if fam not in targets:
                pc["other_family"] += 1
                continue
            loc = (job.get("location") or {}).get("name") or ""
            lclass = location_class(loc, rules)
            if lclass == "non-us":
                pc["non_us"] += 1
                excluded_examples.append(f"{title} — {loc} (non-US)")
                continue
            sh = seniority_hit(title, rules)
            if sh:
                pc["seniority"] += 1
                excluded_examples.append(f"{title} (seniority /{sh}/)")
                continue
            dreason, dinfo = description_check(job, rules, persona)
            if dreason:
                pc["description"] += 1
                excluded_examples.append(f"{title} ({dreason})")
                ruled_out.append({"title": lab(title, REC), "url": lab(job.get("absolute_url"), REC),
                                  "reason": lab(dreason, INP, note="description_rules phrase/years rule applied to the posting text (record)"),
                                  "years_mentions": lab(dinfo["years_mentions"], REC)})
                continue
            pc["kept"] += 1
            same = fam in c["families"]
            tier, p = tier_for(c["approvals"], same, rules)
            if tier is None:
                continue
            _, fscore, why, freason = GW.judge(job, feats, scheme)
            fit_p = round(max(0.0, min(1.0, fscore / rules["fit"]["full_score"])), 3)
            rid = f"{disc['ats']}:{disc['slug']}:{job.get('id')}"
            roles.append({
                "role_id": rid, "company": c["name"], "title": title,
                "sponsorship": {"p": p, "tier": tier, "source": INP,
                                "basis": f"{c['approvals']:.0f} H-1B approvals (record); posting family '{fam}' "
                                         f"{'IS' if same else 'is NOT'} among sponsored families {c['families']} (record); tier rule rules.json"},
                "fit": {"p": fit_p, "source": INP,
                        "basis": f"scheme {scheme.get('scheme_version')} score {fscore:.2f} / full_score {rules['fit']['full_score']} — deterministic phrase match, no model"},
                "liveness": {"factor": 1.0, "source": REC, "basis": f"posting present in {disc['ats']} board API response fetched {today}"},
                "timeline": tl_term,
            })
            soc = soc_for(title, fam, bls, rules)
            pref_hit = preferred_location(loc, persona)
            role_meta[rid] = {"url": job.get("absolute_url"), "location": lab(loc, REC, location_class=lclass),
                              "preferred_location": lab(bool(pref_hit), INP, matched=pref_hit,
                                                        note="persona preferred_locations applied to the posting location"),
                              "posted": lab(job.get("first_published") or job.get("updated_at") or None, REC),
                              "family": lab(fam, INP), "fit_lines": why, "fit_note": freason,
                              "years_required": lab(dinfo["years_required"], REC,
                                                    note="lowest 'N+ years … experience' in the description" if dinfo["years_mentions"] else "not stated in the description"),
                              "microsoft_ai_stack_terms": lab(dinfo["stack_terms"], REC, note="microsoft_ai_stack_terms found in the posting text"),
                              "wage_context": wage_context(soc), "company_key": c["name"]}
        counts["postings_seen"] += pc["seen"]
        counts["postings_target_family"] += pc["seen"] - pc["other_family"]
        counts["postings_us"] += pc["seen"] - pc["other_family"] - pc["non_us"]
        counts["postings_level_ok"] += pc["kept"] + pc["description"]
        counts["postings_ruled_out_by_description"] += pc["description"]
        counts["postings_kept"] += pc["kept"]
        comp["postings"] = lab(pc, REC, note="counts of board postings; filters are rules.json (your-input)")
        comp["excluded_examples"] = excluded_examples[:5]
        comp["ruled_out_by_description"] = ruled_out
        comp["no_sponsorship_statements"] = no_sponsor
        if pc["kept"] == 0:
            # the engine's reject: board live, nothing for this persona → liveness gate closed for the company
            rid = f"company:{disc['ats']}:{disc['slug']}"
            roles.append({
                "role_id": rid, "company": c["name"], "title": f"(no qualifying US {'/'.join(targets)} posting on board)",
                "sponsorship": {"p": cp, "tier": ctier, "source": INP,
                                "basis": f"{c['approvals']:.0f} H-1B approvals for {c['families']} titles (record); tier rule rules.json"},
                "liveness": {"factor": 0.0, "source": REC,
                             "basis": f"board fetched {today}: {pc['seen']} postings, 0 passed family+US+seniority+description rules"},
                "timeline": tl_term,
            })
            role_meta[rid] = {"company_key": c["name"], "company_level": True}
        comp["bucket"] = "pending-scorer"
        companies.append(comp)

    funnel.update(counts)
    funnel["roles_scored"] = len(roles)
    roles_path = out_dir / "roles.json"
    roles_path.write_text(json.dumps({"roles": roles}, indent=2, ensure_ascii=False), encoding="utf-8")

    # ── score with the real engine scorer (never a copy)
    scorer = {"command": None, "exit_code": None, "stdout": None}
    scored = {}
    if roles:
        cmd = ["node", str(SCORER), str(roles_path), "--out-dir", str(out_dir)]
        scorer["command"] = "node scripts/score/role-scorer.mjs " + rel(roles_path) + " --out-dir " + rel(out_dir)
        try:
            proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=120)
        except FileNotFoundError:
            raise InputError("node not found on PATH — the scorer cannot run, so no decision is made")
        scorer.update(exit_code=proc.returncode, stdout=proc.stdout.strip(), stderr=proc.stderr.strip())
        if proc.returncode != 0:
            raise InputError(f"role-scorer.mjs exited {proc.returncode}: {proc.stderr.strip()[:400]}")
        out = load_json(out_dir / "role-scores.json", "scorer output")
        scorer["scorer_id"] = out.get("_scorer")
        scored = {r["role_id"]: r for r in out.get("roles", [])}

    # ── buckets, read from the scorer's decisions
    buckets = {"apply": [], "consider": [], "network": [], "check-by-hand": [], "skip": []}
    by_company = {c["company"]["value"]: c for c in companies}
    for r in roles:
        s = scored.get(r["role_id"], {})
        rec = s.get("recommendation")
        meta = role_meta[r["role_id"]]
        if meta.get("company_level"):
            gated = rec == "Skip" and "liveness" in (s.get("reason") or "")
            b = "network" if gated and r["sponsorship"]["tier"] in rules["network"]["eligible_tiers"] else "skip"
            by_company[meta["company_key"]]["bucket"] = b
        else:
            b = {"Apply": "apply", "Consider": "consider"}.get(rec, "skip")
        buckets[b].append(r["role_id"])
        meta.update(bucket=b, recommendation=rec, composite=s.get("composite"), reason=s.get("reason"))
    for c in companies:
        if c["bucket"] == "pending-scorer":
            c["bucket"] = "has-postings"
        if c["bucket"] == "check-by-hand":
            buckets["check-by-hand"].append(c["company"]["value"])
    skip_share = (sum(1 for r in roles if role_meta[r["role_id"]]["recommendation"] == "Skip") / len(roles)) if roles else None
    # the engine's "a healthy run skips at least half" is about everything EVALUATED, not only what reached
    # the scorer: count every target-family posting seen, and how few became Apply/Consider.
    evaluated = funnel["postings_target_family"]
    advanced = len(buckets["apply"]) + len(buckets["consider"])
    funnel["advanced_to_apply_or_consider"] = advanced
    pipeline_skip_share = (1 - advanced / evaluated) if evaluated else None

    log = {
        "_tool": "swe-sponsor-pipeline", "rules_version": rules.get("rules_version"),
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "today": lab(str(today), INP if args.today else REC, note="--today" if args.today else "system clock"),
        "mode": mode,
        "command": "python3 " + rel(__file__) + (" " + " ".join(args.raw_argv) if args.raw_argv else ""),
        "inputs": {
            "csv": {"path": rel(csv_path), "sha256": sha256(csv_path)},
            "bls": {"path": rel(bls_path), "sha256": sha256(bls_path)},
            "form_d_samples": formd_files,
            "persona": {"path": rel(persona_path), "sha256": sha256(persona_path)},
            "resume": {"path": rel(resume_path), "sha256": sha256(resume_path)},
            "rules": {"path": rel(rules_path), "sha256": sha256(rules_path)},
            "scheme": {"path": rel(scheme_path), "version": scheme.get("scheme_version")},
            "offline_fixtures": rel(args.offline) if args.offline else None,
        },
        "hosts_contacted": sorted(fetcher.hosts), "http_calls": fetcher.calls,
        "raw_responses": fetcher.raw_index,
        "persona": {k: lab(persona[k], INP) for k in ("persona_id", "summary", "target_families", "experience_years", "preferred_locations",
                                        "funding_window_months", "min_h1b_approvals", "hiring_lag_days") if k in persona}
                   | {"visa": lab(persona.get("visa"), INP)},
        "funding_window_start": lab(str(window_start), INP, note="today − funding_window_months"),
        "timeline": {**timeline, "source": INP},
        "funnel": funnel,
        "named_companies": {"not_in_csv": not_in_csv, "excluded": excluded_named} if args.company else None,
        "companies": companies,
        "roles": [{**r, "result": role_meta[r["role_id"]]} for r in roles],
        "buckets": buckets,
        "scorer": {**scorer, "role_scores_json": rel(out_dir / "role-scores.json") if roles else None,
                   "skip_share": skip_share},
        "pipeline_skip_share": lab(pipeline_skip_share, REC,
                                   note="1 − (apply + consider) / target-family postings evaluated"),
        "cannot_verify": CANNOT_VERIFY,
    }
    (out_dir / "pipeline-log.json").write_text(json.dumps(log, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    (out_dir / "pipeline-report.md").write_text(render_report(log, role_meta, roles, companies), encoding="utf-8")
    return log, out_dir


CANNOT_VERIFY = [
    "That a company sponsors H-1B for THIS posting: the record is company-level approvals and its top sponsored titles, matched to the posting by title family.",
    "That a board found by slug guessing belongs to the company, for Ashby boards (no company name in the API); Greenhouse boards are name-checked.",
    "That a company with no board found has no openings: Lever, Workday, iCIMS and SmartRecruiters are not probed, and slugs are guesses.",
    "That a posting is at the right level: seniority words are read from the title, and years of experience only when the description states them in an 'N+ years … experience' form.",
    "That the student is eligible: citizenship, clearance and no-sponsorship requirements are caught only when the description uses one of the listed phrases; other wording passes through.",
    "That a posting really uses the Microsoft AI stack: the stack column is a word match on the posting text, not a reading of the job.",
    "That the hiring lag (persona) is realistic: it is the student's assumption; no record measures it.",
    "That the company will sponsor in the next H-1B cycle: history is not a promise.",
    "Funding beyond the 80 Days CSV columns: the Form D cross-check covers only the shipped samples.",
]


# ───────────────────────────────────────────────────────────── the human report
def tag(s):
    return f"`{s}`"


def render_report(log, meta, roles, companies):
    f, b = log["funnel"], log["buckets"]
    by_id = {r["role_id"]: r for r in roles}
    comp = {c["company"]["value"]: c for c in companies}
    tl = log["timeline"]

    def role_rows(ids):
        rows = ["| # | ★ | Company | Posting | Score | Sponsorship evidence | Fit | Years asked | Microsoft AI stack terms | Wage context (SOC) |",
                "|---:|---|---|---|---:|---|---:|---|---|---|"]
        order = sorted(ids, key=lambda x: (not meta[x]["preferred_location"]["value"], -(meta[x]["composite"] or 0)))
        for n, rid in enumerate(order, 1):
            r, m = by_id[rid], meta[rid]
            c = comp[r["company"]]
            w = m["wage_context"]
            zone = w["job_zone"]["value"] if w["status"] == "mapped" else None
            wage = (f"{money(w['annual_median_wage']['value'])} median, job zone {int(zone) if zone else '—'} {tag('record')} · "
                    f"SOC {w['soc']['value']} via {'O*NET title match' if w['soc']['source'] == REC else 'family rule'} "
                    f"{tag(w['soc']['source'])}" if w["status"] == "mapped"
                    else f"SOC {w['soc']['value'] or '—'} has no BLS row — no wage shown")
            lc = m["location"]["location_class"]
            flag = " ⚠ remote, country unstated" if lc == "remote-unstated" else (" ⚠ location unstated" if lc == "unstated" else "")
            ident = c["board"]["identity"]["value"]
            nn = len(c.get("no_sponsorship_statements") or [])
            nos = f" ⚠ {nn} of {c['postings']['value']['seen']} postings here say they can't sponsor that role" if nn else ""
            star = f"★ {meta[rid]['preferred_location']['matched']}" if meta[rid]["preferred_location"]["value"] else ""
            yrs = m["years_required"]["value"]
            stack = ", ".join(m["microsoft_ai_stack_terms"]["value"][:5]) or "none found"
            rows.append(
                f"| {n} | {star} | {r['company']}{' ⚠ board identity unverified' if ident != 'confirmed' else ''}{nos} | "
                f"[{r['title']}]({m['url']}) — {m['location']['value'] or 'no location'}{flag} {tag('record')} | "
                f"{m['composite']:.3f} | {c['h1b_total_approvals']['value']:.0f} approvals {tag('record')}; tier **{r['sponsorship']['tier']}** "
                f"(p {r['sponsorship']['p']}) {tag('your-input')} | {r['fit']['p']:.2f} {tag('your-input')} | "
                f"{(str(yrs) + '+') if yrs is not None else 'not stated'} {tag('record')} | {stack} {tag('record')} | {wage} |")
        return rows

    L = []
    n_apply, n_cons, n_net, n_hand = len(b["apply"]), len(b["consider"]), len(b["network"]), len(b["check-by-hand"])
    who = log["persona"].get("summary", {}).get("value") or "a student who needs a visa-sponsoring employer"
    fams = " / ".join(log["persona"].get("target_families", {}).get("value") or [])
    L += ["# Sponsor-ready jobs — run report", "",
          "## Executive summary", "",
          f"This report is for {who}. It looked at {f['candidates']} companies that, by public records, have sponsored visas "
          f"for {fams} titles and raised money recently, and checked {f['probed']} of their job boards for open US roles at the "
          f"right level. Postings whose description rules the student out (citizenship, clearance, \"no sponsorship\", or too many "
          f"years of experience) were set aside: {f.get('postings_ruled_out_by_description', 0)} of them. "
          f"Within each list, postings in the student's preferred locations come first (★).",
          "",
          f"- **Apply now — tailor an application:** {n_apply} posting(s).",
          f"- **Worth applying if time allows:** {n_cons} posting(s). These score lower, usually because the company's sponsorship record is for a different kind of title.",
          f"- **Preferred location (★):** {sum(1 for x in b['apply'] + b['consider'] if meta[x]['preferred_location']['value'])} of the apply / consider postings.",
          f"- **Reach out instead of applying:** {n_net} company(ies). Each is a strong sponsor and recently funded, but had no matching opening today. Ask for an informational chat now and check back later.",
          f"- **Check by hand:** {n_hand} company(ies). Their job board couldn't be found automatically. That does **not** mean they have no jobs.",
          "",
          "Every number is labeled as a public record, the student's own rule or assumption, or (never, in this tool) a model's guess. "
          "Nothing here is a final decision: the student reviews each list before acting on it.",
          ""]
    L += ["## Apply — tailor an application", ""]
    L += role_rows(b["apply"]) if b["apply"] else ["_No posting cleared the Apply threshold in this run._"]
    L += ["", "## Consider — apply if time allows", ""]
    L += role_rows(b["consider"]) if b["consider"] else ["_None._"]
    L += ["", "## Network — reach out, don't apply (yet)", ""]
    if b["network"]:
        L += ["| Company | H-1B approvals | Sponsored titles | Latest funding | Board checked | Why no posting qualified | Postings saying \"can't sponsor this role\" |",
              "|---|---:|---|---|---|---|---|"]
        for rid in b["network"]:
            c = comp[by_id[rid]["company"]]
            pc = c["postings"]["value"]
            why = (f"{pc['seen']} postings: {pc['other_family']} other roles, {pc['non_us']} non-US, {pc['seniority']} wrong level, "
                   f"{pc.get('description', 0)} ruled out by description"
                   + (f" (e.g. {c['excluded_examples'][0]})" if c["excluded_examples"] else ""))
            L.append(f"| {c['company']['value']} | {c['h1b_total_approvals']['value']:.0f} {tag('record')} | "
                     f"{', '.join(c['sponsored_titles']['value'][:3])} {tag('record')} | "
                     f"{c['latest_funding_date']['value']} · {money(c['latest_funding_amount']['value'])} {tag('record')} | "
                     f"{c['board']['ats']}:{c['board']['slug']} {tag('record')} | {why} | "
                     f"{len(c.get('no_sponsorship_statements') or [])} of {pc['seen']} {tag('record')} |")
    else:
        L += ["_None._"]
    L += ["", "## Check by hand — board not found automatically", ""]
    if b["check-by-hand"]:
        L += ["| Company | H-1B approvals | Latest funding | What was tried | Result |", "|---|---:|---|---|---|"]
        for name in b["check-by-hand"]:
            c = comp[name]
            tried = ", ".join(sorted({f"{a['ats']}:{a['slug']}" for a in c["board"]["attempts"]}))
            res = c["board"]["status"] + (f" (board name «{c['board']['mismatch']['board_name']}»)" if c["board"].get("mismatch") else "")
            L.append(f"| {name} | {c['h1b_total_approvals']['value']:.0f} {tag('record')} | "
                     f"{c['latest_funding_date']['value']} {tag('record')} | {tried} | {res} |")
    else:
        L += ["_None._"]
    nos = [c for c in companies if c.get("no_sponsorship_statements")]
    L += ["", "## \"Can't sponsor this role\" statements on live boards", ""]
    if nos:
        L += ["Sponsorship history is not a promise, and it is also not all-or-nothing. These companies have H-1B approvals on record, "
              "but some of their live postings say they cannot sponsor *that role*. Such a posting is ruled out; the company is not. "
              "Check whether the roles you want carry the statement.", "",
              "| Company | H-1B approvals | Postings with the statement | Examples |", "|---|---:|---:|---|"]
        for c in nos:
            xs = c["no_sponsorship_statements"]
            ex = "; ".join(x["title"]["value"].strip() for x in xs[:3])
            L.append(f"| {c['company']['value']} | {c['h1b_total_approvals']['value']:.0f} {tag('record')} | "
                     f"{len(xs)} of {c['postings']['value']['seen']} {tag('record')} | {ex} {tag('record')} |")
    else:
        L += ["_None found._"]
    ruled = [(c["company"]["value"], x) for c in companies for x in c.get("ruled_out_by_description", [])]
    L += ["", "## Ruled out by the job description", ""]
    if ruled:
        L += ["| Company | Posting | Why (phrase or years found in the description) |", "|---|---|---|"]
        for name, x in ruled[:40]:
            L.append(f"| {name} | [{x['title']['value']}]({x['url']['value']}) {tag('record')} | {x['reason']['value']} {tag('your-input')} |")
        if len(ruled) > 40:
            L.append(f"| … | {len(ruled) - 40} more | see the JSON log |")
    else:
        L += ["_None._"]
    skipped = [rid for rid in b["skip"]]
    pss = log["pipeline_skip_share"]["value"]
    L += ["", "## Skipped", "",
          f"Of {f['postings_target_family']} {fams} postings evaluated on the boards found, "
          f"{f['advanced_to_apply_or_consider']} reached Apply or Consider"
          + (f": an overall skip share of **{pss:.0%}**. The rest were dropped before scoring (non-US, wrong level, or ruled out by the description), or skipped by the scorer." if pss is not None else ".")
          + " The engine expects a healthy run to skip at least half.",
          "",
          f"The scorer itself returned Skip for {sum(1 for r in roles if meta[r['role_id']]['recommendation'] == 'Skip')} "
          f"of the {len(roles)} items it scored"
          + (f" ({log['scorer']['skip_share']:.0%})" if log["scorer"]["skip_share"] is not None else "")
          + f"; {len(b['network'])} of those are the networking targets above (closed liveness gate, strong sponsor). "
          f"The {len(skipped)} remaining skip(s):"]
    for rid in skipped[:15]:
        L.append(f"- {by_id[rid]['company']} — {by_id[rid]['title']}: {meta[rid]['reason']}")
    if len(skipped) > 15:
        L.append(f"- … and {len(skipped) - 15} more (see the JSON log)")
    L += ["", "## How to read the labels", "",
          "- `record`: read straight from a source file or a live job-board response.",
          "- `your-input`: the student's own rule or assumption (the rules file and persona file). Change it, and the result changes.",
          "- `model-judgment`: none. This tool makes no model calls; fit is a deterministic phrase match against the résumé.",
          "", "## What this run could not verify", ""]
    L += [f"- {x}" for x in log["cannot_verify"]]
    L += ["", "## Gates a person must clear", "",
          "- **G1 Liveness:** open each Apply or Consider link, or run `npm run ats:liveness -- <url>`, and confirm the posting is live and belongs to the named company (⚠ marks unverified board identity).",
          f"- **G2 Timeline:** confirm the OPT start date and hiring-lag assumption. This run used: {tl['arithmetic']}.",
          "- **G3 Release:** for each item, read the job description. Check that the sponsored-title evidence fits the posting, that the level and years match, and that nothing in it rules you out, before applying or reaching out.",
          "", "## Run record (technical)", "",
          f"- Command: `{log['command']}`",
          f"- Mode: {log['mode']} · today: {log['today']['value']} ({log['today']['note']}) · rules {log['rules_version']} · generated {log['generated']}",
          f"- Hosts contacted: {', '.join(log['hosts_contacted']) or 'none (offline)'} · HTTP calls: {log['http_calls']}",
          f"- Funding window start: {log['funding_window_start']['value']} `your-input`",
          f"- Scorer: `{log['scorer']['command']}` → {log['scorer']['stdout'] or 'not run (no roles)'}",
          "", "| Funnel step | Count |", "|---|---:|"]
    labels = [("csv_rows", "80 Days CSV rows"), ("with_approvals", "with ≥ min H-1B approvals"),
              ("target_family_sponsored", "…sponsored a software / ML title"), ("funded_in_window", "…funded inside the window"),
              ("candidates", "candidates"), ("probed", "boards probed"), ("board_found", "board found"),
              ("board_not_found", "board not found"), ("fetch_failed", "fetch failed"), ("identity_mismatch", "board name mismatch"),
              ("postings_seen", "postings seen"), ("postings_target_family", "…in a targeted family"),
              ("postings_us", "…US or unstated location"), ("postings_level_ok", "…right level by title"),
              ("postings_ruled_out_by_description", "…ruled out by the description"), ("postings_kept", "…kept"),
              ("roles_scored", "roles sent to scorer")]
    L += [f"| {lbl} | {f.get(k, '—')} |" for k, lbl in labels]
    L += ["", "| Input | Path | sha256 |", "|---|---|---|"]
    for k, v in log["inputs"].items():
        if isinstance(v, dict) and "sha256" in v:
            L.append(f"| {k} | `{v['path']}` | `{v['sha256'][:12]}…` |")
    L.append(f"| form_d_samples | {', '.join('`' + x + '`' for x in log['inputs']['form_d_samples'])} | — |")
    return "\n".join(L) + "\n"


# ───────────────────────────────────────────────────────────── CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--persona", default=DEFAULTS["persona"])
    ap.add_argument("--rules", default=DEFAULTS["rules"])
    ap.add_argument("--csv", default=DEFAULTS["csv"])
    ap.add_argument("--bls", default=DEFAULTS["bls"])
    ap.add_argument("--formd", default=DEFAULTS["formd"], help="glob of Form D sample JSON files")
    ap.add_argument("--out-dir", help="default: <this folder>/.build/runs/<today>-<mode>/ (gitignored); refused if it holds tracked files")
    ap.add_argument("--offline", help="read boards from <dir>/<ats>-<slug>.json fixtures; no network")
    ap.add_argument("--today", help="YYYY-MM-DD; default: system date (recorded in the log)")
    ap.add_argument("--limit", type=int, help="probe at most N candidates (highest approvals first)")
    ap.add_argument("--company", action="append", help="restrict to this company name (repeatable)")
    argv = sys.argv[1:] if argv is None else argv
    args = ap.parse_args(argv)
    args.raw_argv = argv
    try:
        log, out_dir = run(args)
    except (InputError, GW.InputError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    b = log["buckets"]
    print(f"✓ swe-sponsor-pipeline ({log['mode']}): {log['funnel']['candidates']} candidates, "
          f"{log['funnel']['probed']} probed, {log['funnel']['board_found']} boards found, {log['funnel']['roles_scored']} roles scored")
    print(f"  apply {len(b['apply'])} · consider {len(b['consider'])} · network {len(b['network'])} · "
          f"check-by-hand {len(b['check-by-hand'])} · skip {len(b['skip'])}")
    if log["scorer"]["stdout"]:
        print("  scorer: " + log["scorer"]["stdout"].splitlines()[0])
    if log.get("named_companies"):
        for n in log["named_companies"]["not_in_csv"]:
            print(f"  ✗ {n}: not in the 80 Days CSV — no sponsorship record, not scored")
        for n, why in log["named_companies"]["excluded"].items():
            print(f"  ✗ {n}: {why}")
    print(f"  {rel(out_dir / 'pipeline-report.md')}  +  {rel(out_dir / 'pipeline-log.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
