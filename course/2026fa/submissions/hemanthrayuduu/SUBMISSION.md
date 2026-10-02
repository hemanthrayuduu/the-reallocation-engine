# SUBMISSION

## Executive summary

This is the cover sheet for the Canvas upload. It identifies the student, the exact commit submitted, how to run the work, the lifecycle stage claimed, and its known limits. The submission is a job-search recipe and working tool that lists open entry-level software and AI jobs at companies with a public record of visa sponsorship and recent funding, for an international master's student about to start post-graduation work authorization.

## Submission record

```text
Assignment: The Reallocation Engine — Recipe Design Assignment
Student: Hemanth Rayudu
GitHub handle: hemanthrayuduu
Domain / situation: International MS Computer Science student graduating December 2026, F-1 with post-completion OPT not yet started, targeting entry-level US software / AI engineering roles (SOC 15-1252, 15-1221) at H-1B-sponsoring, recently funded companies
Recipe path: recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md (+ .card.md)
Prototype command: python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py
Test command: python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v
GitHub repository / branch / PR URL: https://github.com/hemanthrayuduu/the-reallocation-engine / contrib/2026fa-hemanthrayuduu-swe-sponsor-pipeline / [PR URL after opening]
Submitted commit SHA: [git rev-parse HEAD of the PR head, filled in at submission]
Lifecycle stage claimed: RUNNABLE-SAMPLE (sample-run gate and G1–G3 cleared by Hemanth Rayudu, 2026-10-02, logs/runs/2026fa-hemanthrayuduu-1.md); attestation: null (not VERIFIED)
Summary of my changes: A Python (stdlib) pipeline that filters the 80 Days CSV to companies with H-1B approvals for software/ML titles and funding in the last 24 months; finds their Greenhouse/Ashby boards by slug, through the repo's allow-listed greenhouse-watch fetcher; turns every US new-grad SWE/ML posting into a role with labelled evidence; scores the roles with the unmodified role-scorer.mjs; and writes an agent JSON log and a human Markdown report bucketing apply / consider / network / check-by-hand / skip. Includes a recipe and card, a fictional persona, 16 offline tests, and a live run on 2026-10-02 (37 candidates, 9 boards, 253 postings evaluated, apply 9, consider 2, network 4).
Known limitations: Board discovery found 9/37 (Lever, Workday, iCIMS, SmartRecruiters not probed); sponsorship is matched by title family, not SOC; sponsorship alone clears the Apply threshold (fit floor is an open DEFINE); funding is a pre-filter because the scorer has no funding vote; Form D covers samples only (1 match); wage is national OEWS context with zero scorer weight; hiring lag is an assumption; Ashby board identity cannot be confirmed; eligibility requirements stated only in job descriptions (US citizenship, clearance, 'not for new graduates') are not read. Both AI Engineer suggestions in the live run were disqualifying this way, and gate G3 caught them.
```

## How to reproduce (from a fresh clone of the branch)

```bash
python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v   # offline, no installs
python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --limit 5                         # quick live demo
python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py                                   # full live run (~2 min)
```

Requires Python 3.9+ and Node 20+. No `npm install` or `pip install` is needed for the prototype.

## What's in this folder

| File | What |
|---|---|
| `CHANGE-BRIEF.md` | predictions written before the build, plus append-only revisions |
| `TEST-REPORT.md` | every check run, with evidence links |
| `worked-run.md` | the real run with pasted output, the verified/inferred split, reflection, attestation |
| `domain-justification.md` | who, asymmetry, layers, 3-3-2 fit, failure modes (one page) |
| `FRICTIONAL.md` | session record (Part A) and author account (Part B) |
| `SOURCES.md` | credits; AI vs author contributions |
| `evidence/` | verbatim terminal output, numbered in run order |
| `runs/2026-10-02-live/` | the final live run's outputs |
| `runs/role-scores.*` | the warm-up `npm run score` on `data/examples/ch11-roles.json` |
