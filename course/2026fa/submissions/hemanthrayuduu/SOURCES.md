# SOURCES — swe-sponsor-pipeline

## Executive summary

This page credits everything the submission was built from: the repository, its rules, its data, the tools, and the AI assistant. It also states plainly who did what. Most of the code and the first drafts of the documents were written by an AI coding assistant under the student's direction. The student chose the problem, redirected the design, and owns every sign-off. The "What the author did" section is the student's to complete in their own words.

## Repository and governing documents

- *The Reallocation Engine*, Nik Bear Brown. Fork of `nikbearbrown/the-reallocation-engine` at commit `015843d`.
- `SNICKERDOODLE.md` (constitution: labels, gates, lifecycle, attestation format), `DOMAIN.md`, `CONTRIBUTING.md`, `DATA_CONTRACT.md` §Zero-Conditions, `AGENTS.md`, `recipes/_shared.md` (run-log template).
- Style models: `recipes/local-wage-adjustment.md`, `recipes/local-wage-adjustment.card.md`, `recipes/scan.md`.
- Assignment: *The Reallocation Engine — Recipe Design Assignment*, INFO 7375, Fall 2026.

## Data (all shipped in the repository; nothing new was downloaded into it)

| Data | Path | Used for |
|---|---|---|
| 80 Days to Stay mapped CSV | `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` | H-1B approvals, sponsored titles, funding |
| SEC Form D **samples** | `data/sec/form-d/processed/sample/companies-sec-{2025q2,2025q3,2025q4,2026q1}-d.sample.json` | funding cross-check |
| BLS OEWS + O*NET compact | `data/bls/compact/soc_occupation_compact.csv` | wage / job-zone context |
| Live job boards | `boards-api.greenhouse.io`, `api.ashbyhq.com` (public APIs, fetched 2026-10-02) | postings, liveness |

## Code reused (called, not copied)

- `scripts/score/role-scorer.mjs`: the decision. Run as a subprocess.
- `.claude/skills/greenhouse-watch/scripts/greenhouse_watch.py`: `board_url`, `fetch_board` (host allow-list, no redirects), `normalize_jobs`, `resume_features`, `judge`, `load_resume`, `load_scheme`. Also `.claude/skills/greenhouse-watch/scheme.default.json`.
- `scripts/ats/scrapers/common/normalize.py`: `normalize_company_name`.
- `scripts/ats/check-liveness.mjs` (`npm run ats:liveness`): human spot-check at gate G1.

## Tools

- Claude Code (model: Claude Opus 5.5), the AI coding assistant, used in the student's terminal session on 2026-10-02.
- Python 3.9.10 standard library; Node v23.11.0; Playwright Chromium (for `ats:liveness` only); git.

## What the AI contributed

Claude Code, in this session:
- **Wrote:** the Markdown reformatting of the assignment instructions (kept local, not committed); the plan; `pipeline.py`; `test_pipeline.py`; `rules.json`; all fixtures; the fictional persona `search/examples/kiran-rao/`; the recipe and card; and first drafts of CHANGE-BRIEF, TEST-REPORT, worked-run, domain-justification and the run log.
- **Ran:** every command whose output is in `evidence/`.
- **Proposed** the first design, a "network, don't apply" list only.
- **Found and fixed** the PhD, US-location and wrong-CSV defects.
- **Caught its own errors in drafts:**
  - an unverified claim about which ATS Intel and ServiceNow use, which was removed;
  - a wrong count of identity-confirmed rows in TEST-REPORT, which was corrected after checking the log.
- **Drafted** predictions P1–P3. These are labeled as Claude's in CHANGE-BRIEF.

## What the author decided, checked, changed, or rejected

*(Author: complete in your own words. The decisions below are recorded from the session, to start from.)*

- **Chose** the career situation (MS CS, December graduation, OPT not started), the target roles (software / AI engineer), the GitHub handle, and the starting recipe idea.
- **Rejected** the first design. You asked why the output was "network, don't apply" and whether it would give you jobs to apply to. That made an Apply list the primary output, with networking kept as a secondary bucket.
- **Rejected** a hard-coded prototype. You asked for one that is "not a hard coded one". That replaced the hand-typed board list, constant fit and fixed SOC with automatic board discovery, per-posting fit and BLS lookup.
- **Asked** whether the plan followed the assignment instructions. That produced the requirement trace in the plan.
- *(Add: what you personally re-ran, read, checked against a source, and what you accepted or changed in each drafted document.)*
