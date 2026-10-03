# SUBMISSION

## Executive summary

This is the cover sheet for the Canvas upload. It identifies the student, the exact commit submitted, how to run the work, the lifecycle stage claimed, and its known limits. The submission is a job-search recipe and working tool that lists open mid-level AI Engineer jobs at companies with a public record of visa sponsorship and recent funding. It reads each job description for anything that rules the student out, for an international master's student on pre-completion OPT.

## Submission record

```text
Assignment: The Reallocation Engine — Recipe Design Assignment
Student: Hemanth Rayudu
GitHub handle: hemanthrayuduu
Domain / situation: International MS Computer Science student on F-1 pre-completion OPT (from mid-October 2026) with about 3.5 years of AI engineering experience, targeting mid-level and senior AI Engineer, Data Scientist and Data Engineer roles (Microsoft AI and data stack preferred; anywhere in the US, Texas and remote first) at H-1B-sponsoring, recently funded companies
Recipe path: recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md (+ .card.md)
Prototype command: python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py
Test command: python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v
GitHub repository / branch / PR URL: https://github.com/hemanthrayuduu/the-reallocation-engine / contrib/2026fa-hemanthrayuduu-swe-sponsor-pipeline (https://github.com/hemanthrayuduu/the-reallocation-engine/tree/contrib/2026fa-hemanthrayuduu-swe-sponsor-pipeline) / PR: not opened yet. It will be opened from this branch to nikbearbrown/the-reallocation-engine after further iteration.
Submitted commit SHA: the commit that contains this file. A file cannot hold its own commit's SHA, so the exact SHA is filled in on the copy of this file at the top level of the Canvas ZIP (written by the ZIP build script).
Lifecycle stage claimed: RUNNABLE-SAMPLE (v0.3.1): G1–G3 and the sample-run gate cleared by Hemanth Rayudu on 2026-10-02 for v0.3.0, re-confirmed for v0.3.1 by his own re-run and fresh-clone check (logs/runs/2026fa-hemanthrayuduu-1.md). attestation: null (not VERIFIED).
Summary of my changes: A Python (stdlib) pipeline: filters the 80 Days CSV to companies with H-1B approvals for software/AI titles and funding in the last 24 months; finds their Greenhouse/Ashby boards by slug through the repo's allow-listed greenhouse-watch fetcher; keeps US AI Engineer postings at the persona's level; reads each description for citizenship/clearance, 'can't sponsor this role' and years-of-experience rule-outs; flags Microsoft AI stack terms and puts Texas/remote first; scores roles with the unmodified role-scorer.mjs; writes an agent JSON log and a human Markdown report (apply / consider / network / check-by-hand / skip). Three iterations on 2026-10-02: iteration 1 (entry-level SWE/AI): apply 9, consider 2, network 4; iteration 2 (author re-scope, mid-level AI): apply 0, consider 3, network 6, 1 ruled out by description; iteration 3 (+ Senior titles, Data Scientist / Data Engineer): apply 0, consider 7 (first Texas match), network 6, 9 ruled out by description. Includes a recipe and card, a fictional persona, 23 offline tests, and evidence for every run and break attempt.
Known limitations: Board discovery found 11/49 (Lever, Workday, iCIMS, SmartRecruiters not probed); sponsorship history is a top-few title list, so every AI posting is the soft tier 'Possible' and nothing reaches Apply (per-petition SOC data is TODO 1); description rules match listed phrases only; 'can't sponsor' statements are role-specific and are counted, not generalised; several year requirements in one description: the lowest is used (TODO 9); one Texas match and no Data Engineer posting in the live run; funding is a pre-filter (the scorer has no funding vote); Form D samples only; wage is national OEWS context with zero scorer weight; hiring lag is an assumption; no E-Verify data; Ashby board identity unconfirmed.
```

## The ZIP

`reallocation-hemanthrayuduu-recipe.zip` is a `git archive` of one commit of this branch. It contains every tracked file except `private/`, so it has no `node_modules`, caches, credentials, `search/resume.json` or `private/`. A copy of this `SUBMISSION.md` sits at the ZIP's top level, with the commit SHA filled in; the source is in `the-reallocation-engine/`.

## How to reproduce (from a fresh clone of the branch)

```bash
python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v   # offline, no installs
python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --limit 5                         # quick live demo
python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --out-dir /tmp/run                 # full live run (~2 min)
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
| `runs/2026-10-02-live-v3/` | iteration 3 (current) live run outputs |
| `runs/2026-10-02-live-v2/` | iteration 2 live run outputs |
| `runs/2026-10-02-live/` | iteration 1 live run outputs |
| `runs/role-scores.*` | the warm-up `npm run score` on `data/examples/ch11-roles.json` |
