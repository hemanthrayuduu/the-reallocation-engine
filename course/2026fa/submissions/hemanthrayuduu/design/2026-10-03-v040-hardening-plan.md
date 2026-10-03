# v0.4.0 Hardening Implementation Plan

## Executive summary

**What this is:** the step-by-step build plan for the last round of improvements to the job-list tool.

**Why read it:** it lists, in order, every change to the code, tests and documents, and how each change is checked before the next begins.

**What it decides:**
1. **Years rule.** Read years of experience from job descriptions more accurately.
2. **Fit scale.** Stop the résumé-fit score from saturating.
3. **Audit.** Write a full audit of every relevant posting with every run.
4. **Verification loop.** Check a fixed sample by hand until it shows zero misclassifications.
5. **Corrections.** Fix a wrong claim about the Austin role in every document.
6. **Submit.**

> **For agentic workers:** REQUIRED SUB-SKILL: use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** make the pipeline's output *verified accurate*. That means: the years read correctly; fit on an honest scale; every posting decision auditable; and a hand-verified sample with zero misclassifications. Then ship v0.4.0.

**Architecture:**
- **Code.** Three changes inside the existing single-file prototype `pipeline.py`:
  - a pure `years_requirement()` that replaces the flat-text years regex;
  - a pure `scheme_max()` for the fit scale;
  - audit rows collected in the existing per-posting loop, plus `verification_sample()` and `render_audit()`.
- **Interfaces kept:**
  - the scorer is still called as a subprocess, unchanged;
  - the output folder rules (gitignored default; refuse foreign or tracked folders) are unchanged;
  - the JSON log gains fields; it loses none.

**Tech stack:** Python 3.9 standard library, `unittest`, Node 20+ (for `scripts/score/role-scorer.mjs` only).

**Spec:** `course/2026fa/submissions/hemanthrayuduu/design/2026-10-03-v040-hardening-design.md`

## Global constraints

- Status may not exceed `RUNNABLE-SAMPLE`; `attestation: null`.
- Every value is labeled `record` or `your-input`; `model-judgment` never appears.
- No weakening a rule so that a role passes. Rule changes need a principled reason and a `rules.json` changelog line.
- Network calls only to `boards-api.greenhouse.io` and `api.ashbyhq.com` (plus `npm run ats:liveness` at gate G1).
- `scripts/score/role-scorer.mjs` is not modified or copied.
- Files are written only in:
  - `scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/`
  - `recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.{md,card.md}`
  - `logs/runs/2026fa-hemanthrayuduu-1.md`
  - `course/2026fa/submissions/hemanthrayuduu/`
  - `search/examples/kiran-rao/`
- The real résumé is used only in `private/` (gitignored). Nothing from it goes into a tracked file.
- Offline tests (`python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py'`) must pass with no network.
- Before submitting: `node scripts/conformance.mjs`, `npm run verify`, `npm run doctor`, and `node scripts/pii-scan.mjs --diff main` must all pass.
- Every human-facing Markdown file opens with `## Executive summary` (P9).

## Review focus

The five inputs most likely to bite, each pinned by a test in the task that owns it:
1. **A heading and its text on the same line.** For example `<p><strong>Preferred:</strong> 5+ years of … experience</p>`. Expected: that line counts as *preferred*. → Task 1, `test_inline_heading_prefix_sets_section`
2. **Plain-text descriptions** (Ashby `descriptionPlain`) with newline-separated headings. Expected: the same section handling as HTML. → Task 1, `test_plain_text_lines_and_headings`
3. **Years written in words** ("five years of experience"). Expected: not parsed, so `required` is `None`. The posting is kept and the limit is documented. → Task 1, `test_years_in_words_are_not_parsed`
4. **A missing description** (`content` is `None`). Expected: no crash; years `None`; posting kept. → Task 1, `test_missing_content_is_safe`
5. **A big board with many other-family postings.** Expected: the audit Markdown counts them and does not list them. → Task 3, `test_audit_markdown_counts_other_family_without_listing`

---

### Task 1: Years rule v2

**Files:**
- Modify: `scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py`
  - add `description_lines`, `heading_section` and `years_requirement` after `no_sponsorship_phrase`;
  - rewrite the years part of `description_check`;
  - update `role_meta` years fields in `run()`;
  - update the "Years asked" cell in `render_report`.
- Modify: `scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/test_pipeline.py` (new class `YearsRuleV2`).

**Interfaces:**
- Produces:
  - `description_lines(content: str | None) -> list[tuple[str, bool]]`, giving `(text, is_list_item)`.
  - `heading_section(text: str, is_li: bool) -> "required" | "preferred" | None`.
  - `years_requirement(content: str | None) -> {"required": int | None, "preferred": int | None, "lines": [{"section", "text", "value", "rule"}]}`.
  - `description_check(job, rules, persona)` still returns `(reason | None, info)`, and `info` gains `years_preferred`, `years_lines`, `phrase_context`. `years_required` and `years_mentions` are kept.

- [ ] **Step 1: Write the failing tests.** Add to `test_pipeline.py`, before `class LocationRule`:

```python
class YearsRuleV2(unittest.TestCase):
    """Patterns taken from the live descriptions read on 2026-10-03 (rewritten as fictional text)."""

    def y(self, html):
        return P.years_requirement(html)

    def test_largest_required_line_wins_over_a_secondary_skill_line(self):
        r = self.y("<p><strong>What You Bring</strong></p><ul><li>4+ years of industry software engineering experience</li>"
                   "<li>1+ years of work or research experience with neural net frameworks</li></ul>")
        self.assertEqual((r["required"], r["preferred"]), (4, None))

    def test_or_alternatives_count_their_smallest(self):
        r = self.y("<ul><li>5+ years of professional software engineering experience in ML platforms, OR 3+ years of direct, "
                   "hands-on experience owning data and evaluation infrastructure</li></ul>")
        self.assertEqual(r["required"], 3)
        self.assertEqual(r["lines"][0]["rule"], "min (or-alternatives)")

    def test_preferred_section_never_decides(self):
        r = self.y("<h3>Preferred Skills</h3><ul><li>4+ years of machine learning engineering experience</li></ul>")
        self.assertEqual((r["required"], r["preferred"]), (None, 4))

    def test_list_item_is_never_a_heading(self):
        r = self.y("<h3>Nice to have</h3><ul><li>Experience with Kubernetes</li><li>6+ years of platform experience</li></ul>")
        self.assertEqual((r["required"], r["preferred"]), (None, 6))

    def test_inline_heading_prefix_sets_section(self):
        r = self.y("<p><strong>Preferred qualifications:</strong> 5+ years of distributed systems experience</p>")
        self.assertEqual((r["required"], r["preferred"]), (None, 5))

    def test_a_plus_on_the_line_marks_it_preferred(self):
        r = self.y("<ul><li>3+ years of Python experience</li><li>2+ years of Spark experience is a plus</li></ul>")
        self.assertEqual((r["required"], r["preferred"]), (3, 2))

    def test_no_headings_means_required(self):
        self.assertEqual(self.y("3+ years of experience with Azure OpenAI")["required"], 3)

    def test_plain_text_lines_and_headings(self):
        r = self.y("About the role\nRequirements\n3+ years of experience shipping ML\nBonus points\n7+ years of experience leading teams")
        self.assertEqual((r["required"], r["preferred"]), (3, 7))

    def test_years_without_experience_are_ignored(self):
        self.assertIsNone(self.y("Founded 10+ years ago; we value curiosity.")["required"])

    def test_years_in_words_are_not_parsed(self):
        self.assertIsNone(self.y("Five years of experience with LLMs")["required"])

    def test_missing_content_is_safe(self):
        self.assertEqual(self.y(None), {"required": None, "preferred": None, "lines": []})

    def test_description_check_uses_v2_and_keeps_evidence(self):
        persona = {"experience_years": 3.5}
        rules = json.loads((HERE / "rules.json").read_text())
        job = {"title": "AI Engineer", "content": "&lt;h3&gt;Requirements&lt;/h3&gt;&lt;ul&gt;&lt;li&gt;6+ years of industry experience&lt;/li&gt;&lt;/ul&gt;"}
        reason, info = P.description_check(job, rules, persona)
        self.assertTrue(reason.startswith("experience:"), reason)
        self.assertEqual(info["years_required"], 6)
        self.assertEqual(info["years_lines"][0]["section"], "required")
```

- [ ] **Step 2: Run them and confirm they fail.**

Run: `python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' 2>&1 | tail -3`
Expected: `FAILED (errors=…)` with `AttributeError: module 'ssp_pipeline' has no attribute 'years_requirement'`.

- [ ] **Step 3: Implement.** In `pipeline.py`, add `import html` to the imports and add after `no_sponsorship_phrase`:

```python
_BLOCK_TAGS = re.compile(r"</?(?:p|li|br|div|h[1-6]|tr|ul|ol|table|section)\b[^>]*>", re.I)
_YEARS = re.compile(r"(\d{1,2})\s*\+?\s*(?:(?:-|–|to)\s*(\d{1,2})\s*\+?\s*)?years?\b(?=[^.;]{0,60}?experience)", re.I)
_PREFERRED_HEAD = re.compile(r"prefer|nice[- ]to[- ]have|bonus|\bplus\b|ideal|desired", re.I)
_HEADING_WORDS = re.compile(r"qualif|require|what you|you have|you bring|you'?ll need|must|basic|minimum|experience|"
                            r"about you|skills|prefer|nice[- ]to[- ]have|bonus|\bplus\b|ideal|desired", re.I)
_PREFERRED_INLINE = re.compile(r"\ba plus\b|nice[- ]to[- ]have|\bbonus\b", re.I)


def description_lines(content):
    """[(text, is_list_item)] from a description in HTML (escaped or not) or plain text."""
    raw = html.unescape(content or "")
    raw = re.sub(r"<li\b[^>]*>", "\n\x00LI", raw, flags=re.I)
    raw = _BLOCK_TAGS.sub("\n", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    out = []
    for part in raw.split("\n"):
        is_li = part.startswith("\x00LI")
        text = re.sub(r"\s+", " ", part.replace("\x00LI", "")).strip()
        if text:
            out.append((text, is_li))
    return out


def heading_section(text, is_li):
    """'preferred' | 'required' for a section heading line, else None. List items are never headings."""
    if is_li or len(text) > 60 or re.search(r"\d", text) or text.endswith(".") or not _HEADING_WORDS.search(text):
        return None
    return "preferred" if _PREFERRED_HEAD.search(text) else "required"


def years_requirement(content):
    """Years rule v2 (rules 0.4.0): largest value among required lines; within a line, mentions joined by 'or'
    are alternatives (smallest counts), otherwise all apply (largest counts); preferred lines never decide."""
    section, req, pref, lines = "required", [], [], []
    for text, is_li in description_lines(content):
        h = heading_section(text, is_li)
        if h:
            section = h
            continue
        m = re.match(r"^([^:]{3,60}):\s*\S", text)
        if m and not is_li:
            h2 = heading_section(m.group(1), False)
            if h2:
                section = h2
        mentions = list(_YEARS.finditer(text))
        if not mentions:
            continue
        values = [int(x.group(1)) for x in mentions]
        alt = any(re.search(r"\bor\b", text[mentions[i].end():mentions[i + 1].start()], re.I)
                  for i in range(len(mentions) - 1))
        value = min(values) if alt else max(values)
        line_section = "preferred" if (section == "preferred" or _PREFERRED_INLINE.search(text)) else "required"
        lines.append({"section": line_section, "text": text[:240], "value": value,
                      "rule": "min (or-alternatives)" if alt else "max"})
        (pref if line_section == "preferred" else req).append(value)
    return {"required": max(req) if req else None, "preferred": max(pref) if pref else None, "lines": lines}
```

Replace the body of `description_check` with:

```python
def description_check(job, rules, persona):
    """Rules applied to the posting text (record). Returns (ruled_out_reason or None, info)."""
    d = rules.get("description_rules") or {}
    text = (GW.strip_html(job.get("content") or "") + " " + (job.get("title") or "")).lower()
    yr = years_requirement(job.get("content"))
    info = {"years_required": yr["required"], "years_preferred": yr["preferred"], "years_lines": yr["lines"],
            "years_mentions": [l["text"] for l in yr["lines"]], "matched_phrase": None, "phrase_context": None,
            "stack_terms": [s for s in rules.get("microsoft_ai_stack_terms", []) if GW.phrase_in(s, text)]}
    for key, label in (("eligibility_exclude_phrases", "eligibility"), ("no_sponsorship_phrases", "no-sponsorship")):
        for ph in d.get(key, []):
            if GW.phrase_in(ph, text):
                i = text.find(ph.lower())
                info["matched_phrase"] = ph
                info["phrase_context"] = text[max(0, i - 60): i + len(ph) + 60] if i >= 0 else None
                return f"{label}: description says «{ph}»", info
    y = d.get("years_of_experience")
    if y is not None and persona.get("experience_years") is not None and yr["required"] is not None:
        limit = persona["experience_years"] + y.get("tolerance_years", 0)
        if yr["required"] > limit:
            return (f"experience: description requires {yr['required']}+ years (largest required line; 'or' alternatives "
                    f"count their smallest), above persona {persona['experience_years']} + tolerance "
                    f"{y.get('tolerance_years', 0)}"), info
    return None, info
```

In `run()`, replace the `"years_required": lab(...)` entry of `role_meta[rid]` with:

```python
                              "years_required": lab(dinfo["years_required"], REC,
                                                    note=("description text (record) read by years rule v2 (your-input): largest required "
                                                          "line; 'or' alternatives count their smallest") if dinfo["years_lines"]
                                                         else "not stated in the description"),
                              "years_preferred": lab(dinfo["years_preferred"], REC, note="preferred-only lines; never decide"),
                              "years_lines": dinfo["years_lines"],
```

In `render_report`, `role_rows`, replace the `yrs` cell expression `{(str(yrs) + '+') if yrs is not None else 'not stated'}` with `{years_cell(m)}`, and add before `render_report`:

```python
def years_cell(m):
    req, pref = m["years_required"]["value"], (m.get("years_preferred") or {}).get("value")
    cell = f"{req}+" if req is not None else "not stated"
    return cell + (f" (pref {pref}+)" if pref is not None else "")
```

- [ ] **Step 4: Run all the tests and confirm they pass.**

Run: `python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' 2>&1 | tail -3`
Expected: `OK` (26 earlier + 12 new = 38 tests; 1 may be skipped outside git).

- [ ] **Step 5: Commit.**

```bash
git add scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/test_pipeline.py
git commit -m "2026fa hemanthrayuduu: years rule v2 (required vs preferred, or-alternatives, largest required line)"
```

### Task 2: Fit on the scheme's own scale

**Files:**
- Modify: `pipeline.py` (add `scheme_max`; change the `fit_p` line and its basis string in `run()`).
- Modify: `rules.json` (`fit.full_score` becomes `"scheme_max"`; `fit._note`; `rules_version` 0.4.0; changelog).
- Test: `test_pipeline.py` (class `FitScale`).

**Interfaces:**
- Produces: `scheme_max(scheme: dict) -> float` (12.0 for `scheme.json`); `fit.basis` text contains `/ scheme max 12.0`.

- [ ] **Step 1: Write the failing tests.** Add before `class LocationRule`:

```python
class FitScale(unittest.TestCase):
    def test_scheme_max_is_computed_from_the_scheme(self):
        scheme = json.loads((HERE / "scheme.json").read_text())
        self.assertEqual(P.scheme_max(scheme), 12.0)

    def test_fit_is_score_over_scheme_max(self):
        tmp = tempfile.TemporaryDirectory(); out = Path(tmp.name)
        rc, _, err = run(BASE + ["--out-dir", str(out)])
        self.assertEqual(rc, 0, err)
        role = next(r for r in json.loads((out / "roles.json").read_text())["roles"] if r["role_id"] == "greenhouse:lumenbyte:101")
        self.assertIn("/ scheme max 12.0", role["fit"]["basis"])
        score = float(role["fit"]["basis"].split("score ")[1].split(" ")[0])
        self.assertAlmostEqual(role["fit"]["p"], round(min(1.0, score / 12.0), 3))
        tmp.cleanup()
```

- [ ] **Step 2: Run and confirm failure.** Same command as before. Expected: `AttributeError: … 'scheme_max'`.

- [ ] **Step 3: Implement.** Add after `tier_for` in `pipeline.py`:

```python
def scheme_max(scheme):
    """Highest score the fit scheme can give: title + capped skills + any-skill bonus + degree + positive location."""
    w = scheme["weights"]
    return float(w.get("title", 0) + scheme.get("max_skill_hits", 8) * w.get("skill", 0)
                 + w.get("skill_any", 0) + w.get("degree", 0) + max(w.get("location", 0), 0))
```

In `run()`, after `scheme = GW.load_scheme(...)`, add:

```python
    full = scheme_max(scheme) if rules["fit"]["full_score"] == "scheme_max" else float(rules["fit"]["full_score"])
```

Then replace the `fit_p` line and the fit basis with:

```python
            fit_p = round(max(0.0, min(1.0, fscore / full)), 3)
```
```python
                "fit": {"p": fit_p, "source": INP,
                        "basis": f"scheme {scheme.get('scheme_version')} score {fscore:.2f} / scheme max {full} — deterministic phrase match, no model"},
```

In `rules.json`:
- set `"rules_version": "0.4.0"`;
- set `"fit": {"scheme": …, "full_score": "scheme_max", "_note": "fit p = min(1, scheme score / scheme max). The max is computed from scheme.json (title 3 + 8 skills × 1 + any-skill 0.5 + degree 0.5 = 12), so 1.0 means a complete match rather than '8 points or more' (0.3.x divided by 8 and saturated for skill-rich résumés)."}`;
- append to `_changelog`: `"0.4.0 (2026-10-03): years rule v2 (largest required line; or-alternatives; preferred lines never decide; list items never headings) and fit divided by the scheme maximum (12) instead of 8. Evidence: 16 live descriptions read on 2026-10-03 (verify-iteration files)."`;
- in `description_rules.years_of_experience._note`, describe rule v2 in one sentence.

- [ ] **Step 4: Run the tests.** Expected: `OK`. If `test_soft_sponsorship_tier_is_demoted_to_consider` fails because a fixture role's composite fell below 0.20, **do not change a threshold**. Read the new composite in the failure, and update that test's expectation to the scorer's real output, with a comment `# 0.4.0 fit scale: composite X → <bucket>`. That is a consequence of the approved scale, not a rule change.

- [ ] **Step 5: Commit.**

```bash
git add scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/{pipeline.py,test_pipeline.py,rules.json}
git commit -m "2026fa hemanthrayuduu: fit on the scheme's own scale (score / 12), rules 0.4.0"
```

### Task 3: Per-posting audit and verification sample

**Files:**
- Modify: `pipeline.py`:
  - add `audit_row`, `verification_sample`, `evidence_text`, `render_audit`;
  - in `run()`, collect audit rows and other-family postings, finalize the kept decisions after bucketing, add `postings_audit` and `verification_sample` to the log, and write `pipeline-audit.md`.
- Test: `test_pipeline.py` (methods added to `HappyPathOffline`).

**Interfaces:**
- Consumes: `description_check` info from Task 1 (`years_lines`, `matched_phrase`, `phrase_context`).
- Produces:
  - log keys `postings_audit` (a list of rows: `company`, `board`, `id`, `title`, `url`, `location`, `decision`, `reason`, `evidence`) and `verification_sample` (rows with `why`);
  - `comp["other_family_postings"]`, a list of `{"title", "url"}`;
  - the file `pipeline-audit.md`.
- Decision values: `kept:apply|kept:consider|kept:skip`, `non-us`, `wrong-level`, `ruled-out:eligibility`, `ruled-out:no-sponsorship`, `ruled-out:experience`.

- [ ] **Step 1: Write the failing tests.** Add to `HappyPathOffline`:

```python
    def test_audit_has_every_target_family_posting_once_with_its_decision(self):
        got = {r["id"]: r["decision"]["value"] for r in self.log["postings_audit"]}
        self.assertEqual(got, {"101": "kept:apply", "102": "kept:apply", "103": "kept:consider", "105": "ruled-out:eligibility",
                               "106": "ruled-out:experience", "107": "kept:skip", "qh-1": "wrong-level", "qh-2": "non-us",
                               "401": "kept:consider", "402": "ruled-out:no-sponsorship", "501": "non-us"})
        self.assertEqual(len(self.log["postings_audit"]), len(got))

    def test_verification_sample_has_every_kept_row_and_is_deterministic(self):
        sample = self.log["verification_sample"]
        kept = {r["id"] for r in self.log["postings_audit"] if r["decision"]["value"].startswith("kept")}
        self.assertTrue(kept <= {r.get("id") for r in sample})
        tmp = tempfile.TemporaryDirectory()
        rc, _, _ = run(BASE + ["--out-dir", tmp.name])
        again = json.loads((Path(tmp.name) / "pipeline-log.json").read_text())["verification_sample"]
        key = lambda s: [(r["why"], r["company"], r["title"]["value"]) for r in s]
        self.assertEqual(key(sample), key(again))
        tmp.cleanup()

    def test_audit_markdown_counts_other_family_without_listing(self):
        md = (self.out / "pipeline-audit.md").read_text()
        self.assertTrue(md.splitlines()[2].startswith("## Executive summary"))
        self.assertIn("Verification sample", md)
        self.assertNotIn("Account Executive", md)   # an other-family title: counted, never listed
        self.assertIn("other-family", md)
```

- [ ] **Step 2: Run and confirm failure.** Expected: `KeyError: 'postings_audit'`.

- [ ] **Step 3: Implement.** Add before `CANNOT_VERIFY` in `pipeline.py`:

```python
_BOUNDARY_TITLE = re.compile(r"engineer|scientist|data|\bai\b|\bml\b|machine learning|analytics", re.I)


def audit_row(company, disc, job, title, loc, lclass, decision, reason, evidence):
    return {"company": company, "board": f"{disc['ats']}:{disc['slug']}", "id": str(job.get("id")),
            "title": lab(title, REC), "url": lab(job.get("absolute_url"), REC),
            "location": lab(loc, REC, location_class=lclass),
            "decision": lab(decision, INP, note="rules.json applied to the posting (record)"),
            "reason": lab(reason, INP), "evidence": evidence}


def verification_sample(audit, companies):
    """Deterministic: every kept row; first 3 (by company, title) of every other decision; first 5 other-family
    postings whose title looks like engineering/data/AI work (the family rule's boundary)."""
    key = lambda r: (r["company"], r["title"]["value"] or "")
    rows = sorted(audit, key=key)
    sample = [{"why": "kept", **r} for r in rows if r["decision"]["value"].startswith("kept")]
    others = {}
    for r in rows:
        if not r["decision"]["value"].startswith("kept"):
            others.setdefault(r["decision"]["value"], []).append(r)
    for d in sorted(others):
        sample += [{"why": f"first 3 of {d}", **r} for r in others[d][:3]]
    boundary = sorted((c["company"]["value"], p["title"] or "", p["url"]) for c in companies
                      for p in c.get("other_family_postings", []) if _BOUNDARY_TITLE.search(p["title"] or ""))
    sample += [{"why": "boundary other-family title", "company": co, "id": None, "title": lab(t, REC), "url": lab(u, REC),
                "decision": lab("other-family", INP), "reason": lab("title not in a targeted family", INP), "evidence": {}}
               for co, t, u in boundary[:5]]
    return sample


def evidence_text(r):
    e = r.get("evidence") or {}
    parts = []
    if e.get("location_class"):
        parts.append(f"location «{r['location']['value']}» → {e['location_class']}")
    if e.get("seniority_pattern"):
        parts.append(f"title matches /{e['seniority_pattern']}/")
    if e.get("phrase"):
        parts.append(f"«{e['phrase']}» in «…{(e.get('context') or '').strip()}…»")
    for l in e.get("years_lines") or []:
        parts.append(f"[{l['section']}] {l['value']}+ ({l['rule']}): «{l['text'][:110]}»")
    return "; ".join(parts) or "—"


def render_audit(log):
    a, s = log["postings_audit"], log["verification_sample"]
    counts = {}
    for r in a:
        counts[r["decision"]["value"]] = counts.get(r["decision"]["value"], 0) + 1
    other = sum(c["postings"]["value"]["other_family"] for c in log["companies"] if c.get("postings"))
    L = ["# Posting audit — every decision and its evidence", "", "## Executive summary", "",
         f"This file lists every posting the tool judged relevant ({len(a)} postings in a targeted job family on the boards it "
         f"found), what it decided for each, and the exact text that decided it. It exists so a person can check the tool by "
         f"hand instead of trusting it. {other} other-family postings were counted, not listed. The verification sample below "
         f"({len(s)} rows, chosen by a fixed rule) is what gets checked against the live descriptions in each iteration.", "",
         "## Decisions", "", "| Decision | Postings |", "|---|---:|"]
    L += [f"| {d} | {n} |" for d, n in sorted(counts.items())] + [f"| other-family (counted, not listed) | {other} |", ""]
    L += ["## Verification sample", "", "| # | Why sampled | Company | Posting | Decision | Evidence | Checked |",
          "|---:|---|---|---|---|---|---|"]
    for i, r in enumerate(s, 1):
        L.append(f"| {i} | {r['why']} | {r['company']} | [{(r['title']['value'] or '').strip()}]({r['url']['value']}) | "
                 f"{r['decision']['value']} | {evidence_text(r)} |  |")
    L += ["", "## Every target-family posting", "", "| Company | Posting | Location | Decision | Evidence |", "|---|---|---|---|---|"]
    for r in sorted(a, key=lambda r: (r["company"], r["title"]["value"] or "")):
        L.append(f"| {r['company']} | [{(r['title']['value'] or '').strip()}]({r['url']['value']}) | {r['location']['value'] or '—'} | "
                 f"{r['decision']['value']} | {evidence_text(r)} |")
    return "\n".join(L) + "\n"
```

In `run()`:
- Before the company loop, add `audit = []`.
- Inside the posting loop, after `fam = family_of(...)`, replace the other-family branch with:

```python
            if fam not in targets:
                pc["other_family"] += 1
                other_family.append({"title": title, "url": job.get("absolute_url")})
                continue
```

- At the top of each company's posting loop (next to `excluded_examples, ruled_out, no_sponsor = [], [], []`), add `other_family = []`.
- At each exclusion, append a row before `continue`:
  - non-US: `audit.append(audit_row(c["name"], disc, job, title, loc, lclass, "non-us", "location not in the US", {"location_class": lclass}))`
  - seniority: `audit.append(audit_row(c["name"], disc, job, title, loc, lclass, "wrong-level", f"title matches /{sh}/", {"seniority_pattern": sh}))`
  - description: `audit.append(audit_row(c["name"], disc, job, title, loc, lclass, "ruled-out:" + dreason.split(":")[0], dreason, {"phrase": dinfo["matched_phrase"], "context": dinfo["phrase_context"], "years_lines": dinfo["years_lines"]}))`
- For kept postings, after `rid = …`, append `audit.append(audit_row(c["name"], disc, job, title, loc, lclass, "kept", "passed family, US, level and description rules", {"years_lines": dinfo["years_lines"], "rid": rid}))`.
- After the loop, set `comp["other_family_postings"] = other_family`.
- After the buckets loop:

```python
    for r in audit:
        if r["decision"]["value"] == "kept":
            r["decision"]["value"] = "kept:" + role_meta[r["evidence"]["rid"]]["bucket"]
    sample = verification_sample(audit, companies)
```

- Add `"postings_audit": audit, "verification_sample": sample,` to `log`.
- After writing `pipeline-report.md`, add `(out_dir / "pipeline-audit.md").write_text(render_audit(log), encoding="utf-8")`.

- [ ] **Step 4: Run the tests.** Expected: `OK`.

- [ ] **Step 5: Run conformance.**

Run: `node scripts/conformance.mjs scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline`
Expected: `✓ all conform`.

- [ ] **Step 6: Commit.**

```bash
git add scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/{pipeline.py,test_pipeline.py}
git commit -m "2026fa hemanthrayuduu: per-posting audit (pipeline-audit.md) + deterministic verification sample"
```

### Task 4: Verification loop (iterate until correct)

**Files:**
- Create: `course/2026fa/submissions/hemanthrayuduu/evidence/verify-iteration-<N>.md` (one per iteration, P9 executive summary).
- Create: `course/2026fa/submissions/hemanthrayuduu/runs/2026-10-03-live-v4/` (the run that passes).

- [ ] **Step 1: Run live.**

Run: `python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --out-dir course/2026fa/submissions/hemanthrayuduu/runs/2026-10-03-live-v4 2>&1 | tail -5 | tee course/2026fa/submissions/hemanthrayuduu/evidence/42-iteration4-live-run.txt`
Expected: a summary line and `exit` 0. It may take 2–12 minutes, depending on API latency.

- [ ] **Step 2: Check every sampled row against its live description.** Fetch with the Greenhouse/Ashby job API (named hosts only). For each row, decide `correct` or `misclassified`, using the decision's own definition:
  - **family:** is the title AI/ML/data work?
  - **US:** is the location in the US?
  - **level:** is the title's seniority right?
  - **years:** what is the largest *required* number, with or-alternatives counting their smallest?
  - **eligibility / no-sponsorship:** is the phrase really a requirement for this role?
  - **boundary titles:** is the role really outside every targeted family?

  Write `evidence/verify-iteration-<N>.md`: an executive summary; a table `# | company | posting | tool decision | what the description says | correct?`; and the misclassification count. Label it *checked by Claude Code*.

- [ ] **Step 3: If the count is above zero,** change only the responsible rule, on a principled ground; never to admit or reject a specific role. Add a `rules.json` changelog line naming the evidence file, add a test with a fictional fixture for the pattern, run the tests, commit, delete the run folder (it is regenerated), and repeat from Step 1 with N+1.

- [ ] **Step 4: Stop when an iteration records 0 misclassifications.** Commit that iteration's run folder and evidence.

```bash
git add course/2026fa/submissions/hemanthrayuduu/runs/2026-10-03-live-v4 course/2026fa/submissions/hemanthrayuduu/evidence/
git commit -m "2026fa hemanthrayuduu: iteration 4 live run + verification (0 misclassifications in the sample)"
```

### Task 5: Corrections and documents for 0.4.0

**Files:** `recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md`, `.card.md`, `scripts/contrib/…/README.md`, and in `course/2026fa/submissions/hemanthrayuduu/`: `worked-run.md`, `TEST-REPORT.md`, `CHANGE-BRIEF.md`, `FRICTIONAL.md`, `SOURCES.md`, `SUBMISSION.md`, `domain-justification.md`; plus `logs/runs/2026fa-hemanthrayuduu-1.md`.

- [ ] **Step 1: Austin correction.** `grep -rn "5+ years of software engineering\|reach\|and 3+\|\*and\* 3+" <files>`. Rewrite each hit to state that the description says "5+ years … **OR** 3+ years …", that the 3+ path is a real alternative, and (in the run log and FRICTIONAL) that the earlier "reach" wording came from Claude's misreading. The author's G3 decision (apply) stands.
- [ ] **Step 2: CHANGE-BRIEF.** Append "Revision 5". Copy P6–P8 from the spec verbatim, marked *written before implementation (spec commit 4918f08)*, with an outcome table filled from Task 4.
- [ ] **Step 3: Recipe 0.4.0.**
  - frontmatter: `recipe_version: 0.4.0`; `status: DRAFT` until Task 6 Step 4; `todos_open: 7`;
  - close open decision 9: strike it and write the rule from spec §1 with one sentence of reasoning, citing "decided by the author 2026-10-03, design approval";
  - output contract: add `pipeline-audit.md`, `postings_audit[]`, `verification_sample[]`;
  - add a "Verification loop" section (spec §4, including its stated limit);
  - can't verify: add "years written in words or without the word 'experience' are not read".
- [ ] **Step 4: Card.** Update failure mode 4 (years) to rule v2, add the audit file to "What it produces", and change the expected test count to the real number.
- [ ] **Step 5: TEST-REPORT, worked run, run log, FRICTIONAL, SOURCES, SUBMISSION, README.**
  - Add an "Iteration 4 (v0.4.0)" section to each, with real pasted output from Task 4 and the verify-iteration table.
  - FRICTIONAL Part A rows: the brainstorming design (chosen approach C), each verify iteration, the Austin correction.
  - SOURCES: what Claude did in iteration 4.
- [ ] **Step 6: Checks and commit.**

Run: `node scripts/conformance.mjs recipes/cases/2026fa scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline && node scripts/pii-scan.mjs --diff main`
Expected: `✓ all conform` and `pii-scan: clean ✓`.

```bash
git add -A recipes/cases/2026fa scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline course/2026fa/submissions/hemanthrayuduu logs/runs/2026fa-hemanthrayuduu-1.md
git commit -m "2026fa hemanthrayuduu: 0.4.0 documents; Austin 'OR' correction; open decision 9 closed"
```

### Task 6: Sign-off and submission

- [ ] **Step 1: Author re-run.** The author types `! bash .build/rerun.sh` and `! bash .build/fresh-clone.sh`.
  - Expected: the real test count passes; the live summary matches iteration 4 up to posting churn; git status is empty.
  - Save both outputs verbatim as `evidence/43-v040-author-rerun.txt` and `evidence/44-v040-author-fresh-clone.txt`.
  - If the author directs Claude to run them instead, Claude runs them and labels both files *run by Claude Code at the author's direction*. The attestation must then say so; it never claims the author ran them.
- [ ] **Step 2: Attestation.** Add "Re-signed for v0.4.0" to `worked-run.md`, using the exact numbers from Step 1, and the author's name only on the author's word.
- [ ] **Step 3: Gate G1, machine half.** Write the kept URLs and run the liveness check:

```bash
python3 -c "import json; l=json.load(open('course/2026fa/submissions/hemanthrayuduu/runs/2026-10-03-live-v4/pipeline-log.json')); print('\n'.join(r['url']['value'] for r in l['postings_audit'] if r['decision']['value'] in ('kept:apply','kept:consider')))" > .build/kept-urls-v4.txt
npm run ats:liveness -- --file .build/kept-urls-v4.txt | tee course/2026fa/submissions/hemanthrayuduu/evidence/45-v040-G1-liveness.txt
```
- [ ] **Step 4: Gates G1 (human), G2, G3 and the sample-run gate.**
  - Ask the author for the G1 human check, G2, the G3 rows to act on, and the sample-run gate.
  - Record the answers in the run log, then set the recipe and README `status: RUNNABLE-SAMPLE` with `last_gate` naming v0.4.0.
  - Rows identical to iteration 3 may carry the author's earlier G3 decision **only if the author says so**.
- [ ] **Step 5: Final checks.**
  - Run `npm run verify`, `npm run doctor`, `node scripts/pii-scan.mjs --diff main`, and the tests in the repo.
  - Run `node scripts/pii-scan.mjs` inside `.build/fresh-clone` (what CI sees).
  - Every result must be clean.
- [ ] **Step 6: Push and PR.**
  - `git push origin contrib/2026fa-hemanthrayuduu-swe-sponsor-pipeline`.
  - Open the PR (authorized by the author, "submit the assignment"):
    - target `nikbearbrown/the-reallocation-engine`;
    - title `AI/Data Engineer sponsor pipeline (Microsoft stack, OPT) — RUNNABLE-SAMPLE`;
    - body: `.github/PULL_REQUEST_TEMPLATE.md` filled in, with the doctor, verify, pii-scan and test outputs pasted; persona-folder note; CI harness note (repo scripts missing); package-lock note.
- [ ] **Step 7: SUBMISSION.md and ZIP.**
  - Put the PR URL in `SUBMISSION.md`, then commit and push.
  - `bash .build/make-zip.sh`; unzip into `.build/zip-check` and run the tests with `GIT_CEILING_DIRECTORIES` set (git blind). Expected: `OK`.
  - Tell the author where the ZIP is and what to upload: the ZIP, plus the top-level `SUBMISSION.md` from inside it.
- [ ] **Step 8 (optional, private).** `python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --persona private/persona.json --out-dir private/runs/2026-10-03-v040`, then show the author their list in chat. Never commit it.
