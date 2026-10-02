# Sponsor-ready SWE jobs — human card

**Audience:** an international MS CS student who graduates in December, hasn't started OPT, and must decide which software or AI engineering jobs deserve a tailored application this week.  
**Agent twin:** `recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md`  
**Engine layers:** 80 Days to Stay (sponsorship and funding) · Job-Ops (live boards) · Cognitive Pivot (wage context only).

## Executive summary

This card explains, in one page, what the job-list tool tells you and where it can mislead you. The tool lists open entry-level US software and AI jobs at companies that sponsored H-1B visas for similar titles and raised money recently. It also lists strong sponsors to **network into** and companies it **couldn't check**. Read this card before you trust a row.

## Purpose

Answer: *which open roles are worth my two research-and-apply hours today, given that I need a sponsor?* And, for strong sponsors with nothing open right now: *who should I reach out to instead?*

## What it can verify

- The company has N H-1B approvals and these top sponsored titles in the 80 Days CSV (record).
- Its latest recorded funding falls inside your window (record). One company in the live run also matched a Form D sample.
- The posting was on the company's live Greenhouse or Ashby board when fetched (record). For Greenhouse, the board's name matches the company.
- The national median wage and job zone for the posting's occupation code (record).
- The exact arithmetic the engine's scorer used (`role-scores.json`).

## What it cannot verify

- That the company will sponsor **this** job, or sponsor next year.
- That a "check by hand" company has no jobs. Its board just wasn't found: 28 of 37 in the live run.
- That an Ashby board (marked ⚠) belongs to the company.
- That the role is truly entry level. Only the title is read.
- That your 60-day hiring-lag assumption is realistic.
- What this employer pays. The wage is a national median for the occupation.

## Dependencies

- Python 3.9+ (standard library only) and Node 20+. Nothing to install.
- Network: only `boards-api.greenhouse.io` and `api.ashbyhq.com`.
- Your situation file: `search/examples/kiran-rao/persona.json` (fictional). Copy it and edit the OPT date and hiring lag for yourself, but **keep your copy in `private/`**.

## Annotated commands

Offline test. Expect 16 tests passing and `OK`, with no network used:

```bash
python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v
```

Full live run. Expect about 2 minutes and a summary like `apply 9 · consider 2 · network 4 · check-by-hand 28`:

```bash
python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py
```

Check one company. A name that isn't in the CSV prints `not in the 80 Days CSV — no sponsorship record, not scored`:

```bash
python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --company "VERKADA INC"
```

Spot-check an Apply link before tailoring (gate G1). Expect `✅ active`:

```bash
npm run ats:liveness -- <url from the Apply table>
```

## What it produces

- `pipeline-report.md`: your lists, each value tagged `record` or `your-input`.
- `pipeline-log.json`: the same run for an agent, with input file hashes.
- `role-scores.json` / `.md`: the engine scorer's own output.

## Named failure modes

1. **Title-family false match.** A company's "Software Engineer" sponsorships at a robotics or medical-device firm count toward a cloud-backend posting, and an embedded-firmware role reads as "software". *Hardest to catch for:* a new graduate who doesn't yet know how differently "software engineer" is used across industries. *Mitigation:* gate G3 asks you to read the sponsored titles beside each row. A `[TODO: DATA SOURCE]` asks for SOC codes per petition.
2. **Sponsorship drowns out fit.** With a Proven sponsor, the score clears Apply even when your résumé barely matches (live run: fit 0.25, still Apply). *Hardest to catch for:* anyone who reads "Apply" as "good match". *Mitigation:* sort by the Fit column too. `[TODO: DEFINE]` a fit floor.
3. **"Not found" read as "not hiring."** Slug guessing misses most boards. *Mitigation:* those companies are never scored; they are listed for a 2-minute manual check.
4. **Stale sponsorship.** The CSV is history. A company that sponsored in past years may have stopped. *Mitigation:* none in this tool. Ask about sponsorship in the first recruiter call.
