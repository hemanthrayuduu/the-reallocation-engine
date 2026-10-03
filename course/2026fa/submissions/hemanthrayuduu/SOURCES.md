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
- **Drafted** FRICTIONAL Part B at the author's request, from the session record of his commands, output and decisions, for him to review and edit. Also wrote the gate-decision lines in the run log and the attestation line, from his stated results.
- **Pulled** the two AI Engineer job descriptions at gate G3 (`evidence/20`). Ran the 11-link liveness check at the author's request (`evidence/19`).
- **Iteration 2 (after the author's re-scope):**
  - **Checked** the DHS Study in the States OPT page for the 90-day rule and for who applies for OPT.
  - **Rewrote** the persona, résumé and rules (0.2.0 → 0.2.1); `scheme.json`; and the description rules, stack terms and location preference in `pipeline.py`. Also the fixture persona and tests (21).
  - **Ran** every iteration-2 command in `evidence/22`–`27`.
  - **Made and withdrew** a wrong company-wide "doesn't sponsor" rule, after checking the raw descriptions (`24a`, `24b`).
  - **Told the author** Twin Health "won't sponsor" from one posting; corrected it.
  - **Wrongly labeled** two drafted predictions as written before the run; corrected before commit.
- **Iteration 3:** rules 0.3.0 (Senior titles; data_science and data_engineering families with O*NET-backed SOC lookups; Microsoft data-stack terms), persona v3, two new tests; ran `evidence/29`–`32`; found the two-requirement years case (TODO 9).
- **Iteration 4 (2026-10-03):** wrote the design and plan (`design/`); years rule v2, fit on the scheme's own scale, `pipeline-audit.md` and the verification sample, with tests (49); rules 0.4.0–0.4.2; ran `evidence/42`–`44`; checked each verification sample against the live descriptions (`verify-iteration-1`–`3`). **Misread** the Austin role as "5+ and 3+" in iteration 3 (it is "or"); corrected in every document with a dated note.
- **DHS source used:** *Study in the States*, "F-1 Optional Practical Training (OPT)", studyinthestates.dhs.gov, read 2026-10-02.

## What the author decided, checked, changed, or rejected

- **Chose** the starting career situation (MS CS, December graduation, OPT not started; later corrected, see *Re-scoped*), the target roles (software / AI engineer), the GitHub handle, and the starting recipe idea.
- **Rejected** the first design. I asked why the output was "network, don't apply" and whether it would give me jobs to apply to. That made an Apply list the primary output, with networking kept as a secondary bucket.
- **Rejected** a hard-coded prototype. I asked for one that is "not a hard coded one". That replaced the hand-typed board list, constant fit and fixed SOC with automatic board discovery, per-posting fit and BLS lookup.
- **Asked** whether the plan followed the assignment instructions. That produced the requirement trace in the plan.
- **Re-ran myself:**
  - the offline tests (16 OK);
  - the full live run (identical to the committed run);
  - a fresh clone of the branch (tests OK, live run OK, no tracked files changed).
- **Checked myself:** I opened all 11 Apply/Consider links (all live, with descriptions and Apply buttons). I confirmed the persona's OPT date and hiring lag as a stand-in for my situation (gate G2).
- **Decided at gate G3:**
  - rejected both Databricks AI Engineer roles once their descriptions showed a new-grad exclusion and a US citizenship and clearance requirement;
  - chose Cohere Health SWE II and Verkada Backend to apply to;
  - kept 7 rows as backups.
- **Decided** to log the description problem as TODO 7 rather than change the tested code. Promoted the recipe to RUNNABLE-SAMPLE.
- **Signed** the attestation after my own re-runs. Reviewed and edited FRICTIONAL Part B.
- **Re-scoped** the work after iteration 1. I corrected my situation (pre-completion OPT, about 3.5 years, mid-level AI Engineer, Microsoft AI stack) and my location priority (all US, Texas and remote first), and asked which employers hire on OPT.
- **Widened** the target again: Senior titles in, plus Data Engineer and Data Scientist roles (iteration 3).
- **Iteration 3, checked and decided myself:**
  - opened all 7 Consider links (all live, with descriptions and Apply buttons);
  - confirmed the timeline stand-in (G2);
  - chose to apply to all 7 Consider rows (G3), treating the Austin role as a reach because its description asks 5+ years; *(the "5+ years" reading was Claude's mistake: the description says 5+ **or** 3+; corrected 2026-10-03)*
  - promoted the recipe to RUNNABLE-SAMPLE for v0.3.0.
- **Re-ran myself for iteration 3:** I stopped Claude Code's re-run so I could run the checks myself. I ran `! bash .build/rerun.sh` (`evidence/34b`) and `! bash .build/fresh-clone.sh` on a fresh clone at `99bc2c9` (`evidence/35`). Both gave 23 tests OK and an identical live result.
- **Asked Claude Code to write** the iterations 2–3 part of FRICTIONAL Part B and this iteration-3 entry from the session record; I read them before submitting.
