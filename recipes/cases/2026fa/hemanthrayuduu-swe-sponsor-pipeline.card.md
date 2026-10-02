# Sponsor-ready AI Engineer jobs — human card

**Audience:** an international MS CS student on pre-completion OPT with about 3.5 years of AI engineering experience, deciding which mid-level AI Engineer roles (Microsoft AI stack; anywhere in the US, Texas and remote first) deserve a tailored application this week.  
**Agent twin:** `recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md`  
**Engine layers:** 80 Days to Stay (sponsorship and funding) · Job-Ops (live boards and job descriptions) · Cognitive Pivot (wage context only).

## Executive summary

This one-page card explains what the job-list tool tells you and where it can mislead you. The tool lists open AI Engineer jobs at companies that have sponsored work visas and raised money recently. It drops jobs whose description rules you out: US citizenship, a clearance, "can't sponsor this role", or too many years. Texas and remote jobs are listed first. It also names strong sponsors to network into and companies it couldn't check. Read this card before you trust a row.

## Purpose

Answer: *which open AI Engineer roles are worth my research-and-apply hours today, given that I'll need H-1B sponsorship?* And, for strong sponsors with nothing open right now: *who should I reach out to instead?*

## What it can verify

- The company has N H-1B approvals and these top sponsored titles (record).
- Its latest funding is inside your window (record).
- The posting was live on the company's Greenhouse or Ashby board when fetched; for Greenhouse, the board's name matches the company (record).
- What the description says: the years asked, and phrases like "U.S. citizenship" or "unable to sponsor … for this role" (record).
- Which Microsoft AI stack terms appear in the posting (record).
- The national median wage for the occupation, and the scorer's exact arithmetic.

## What it cannot verify

- That the company will sponsor **this** job. History isn't a promise, and live postings at sponsoring companies sometimes say "unable to sponsor … for this role". The tool counts those statements and shows them; it doesn't decide for you.
- That a "check by hand" company has no jobs. 30 of 40 boards weren't found in the live run.
- Eligibility clauses worded differently from the tool's phrase list.
- The real level of a role whose description gives no years.
- Whether a job really uses the Microsoft stack. "Azure" alone may just be the company's cloud.
- Pay at this employer. Your hiring-lag assumption.

## Dependencies

- Python 3.9+ (standard library only) and Node 20+. Nothing to install.
- Network: only `boards-api.greenhouse.io` and `api.ashbyhq.com`.
- Your situation file: `search/examples/kiran-rao/persona.json` (fictional). Edit `experience_years`, `preferred_locations` and the OPT dates for yourself, in a copy kept under `private/`.

## Annotated commands

Offline test. Expect 21 tests and `OK`, with no network used:

```bash
python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v
```

Live run. Expect about 2 minutes. In the 2026-10-02 run: `apply 0 · consider 3 · network 6 · check-by-hand 30`.

```bash
python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --out-dir /tmp/my-run
```

Check one company. A name not in the CSV prints `not in the 80 Days CSV — no sponsorship record, not scored`:

```bash
python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --company "DATABRICKS INC" --out-dir /tmp/one
```

Spot-check a link before tailoring (gate G1). Expect `✅ active`:

```bash
npm run ats:liveness -- <url from the Consider table>
```

## What it produces

- `pipeline-report.md`: your lists, ★ for Texas/remote, every value tagged `record` or `your-input`, plus a table of what the job descriptions ruled out and why.
- `pipeline-log.json`: the same run for an agent, with input hashes.
- `role-scores.json` / `.md`: the engine scorer's own output.

## Named failure modes

1. **"Can't sponsor" read as all-or-nothing.** The statements are per role. Verkada says it on 156 of 307 postings (mostly sales), but not on its backend roles. Twin Health says it on 23 of 39, but not on "Senior AI Engineer". *Hardest to catch for:* anyone who skims one posting and writes off the company. *Mitigation:* the posting is ruled out; the company stays, with its count shown.
2. **The sponsorship record covers software titles, not AI titles.** The CSV keeps only a company's top few sponsored titles. So an AI posting at a big software sponsor is graded "Possible": a Consider at best. *Hardest to catch for:* a student who sees no "Apply" rows and concludes nobody sponsors AI engineers. *Mitigation:* read the Consider list, and see `[TODO: DATA SOURCE]` 1.
3. **Title words mislead.** "AI" plus "engineer" also matches partner, sales and QA roles. Those are now excluded by rule, but new variants will appear. *Mitigation:* gate G3.
4. **Senior roles hidden by default.** With 3.5 years you may qualify for some "Senior" roles, but they're excluded by default. *Mitigation:* delete the two Senior patterns in `rules.json` if you want them, and re-run.
