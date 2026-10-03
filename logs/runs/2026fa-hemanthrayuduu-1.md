# Run log — 2026fa-hemanthrayuduu-1

## Executive summary

This is the run record for a job-search recipe that finds open jobs at companies with a public record of visa sponsorship and recent funding. It went through two iterations on 2026-10-02.
- **Iteration 1:** entry-level software and AI roles. It ran, was checked against its sources, and was signed off by the student. That sign-off revealed that both AI roles it suggested were closed to them.
- **Iteration 2:** after the student corrected their situation (pre-completion OPT, about 3.5 years of experience, mid-level AI Engineer roles on the Microsoft AI stack, Texas and remote first), the tool was changed to read job descriptions. It was run again.

- **Iteration 3:** the student widened the target to include Senior titles and Data Scientist / Data Engineer roles. That was a rules-only change, and the tool was run once more.

The iteration-3 sign-off lines at the bottom are still open.

## 2026-10-02 — swe-sponsor-pipeline live sample run

- **Recipe:** manual (`recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md` v0.1.1, rules 0.1.1, code commit e26febd)
- **Inputs:**
  - Command: `python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py` (no flags; today = system date 2026-10-02).
  - Persona `search/examples/kiran-rao/persona.json`, fictional.
  - `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` (full shipped file).
  - `data/bls/compact/soc_occupation_compact.csv`.
  - `data/sec/form-d/processed/sample/*.sample.json` (**samples only**).
  - Live Greenhouse and Ashby board APIs, 108 calls. sha256 of every input and raw response is in `pipeline-log.json`.
- **Outputs:**
  - `course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live/`: `pipeline-report.md`, `pipeline-log.json`, `roles.json`, `role-scores.json`, `role-scores.md`.
  - Terminal output in `course/2026fa/submissions/hemanthrayuduu/evidence/09-final-live-run.txt`.
- **Result:**
  - Funnel: 30,369 rows → 1,552 with H-1B approvals → 557 that sponsored a software/ML title → 37 funded since 2024-10-02.
  - Boards found for 9 of 37. 253 SWE/ML postings evaluated.
  - Buckets: **apply 9 · consider 2 · network 4 · check-by-hand 28 · skip 2**.
  - Overall skip share 96% (1 − 11/253). The scorer itself: Apply 9 · Consider 2 · Skip 6.
  - Offline tests 16/16. Conformance ✓; doctor and verify exit 0 before and after; `pii-scan --diff main` clean.
- **Open issues:**
  - Board discovery coverage is 24%.
  - Sponsorship alone clears Apply (0.35 × 0.9 = 0.315 ≥ 0.30; recipe `[TODO: DEFINE]` 5).
  - The scorer has no funding vote (`[TODO: DEV]` 4), and a missing gate defaults to open. This recipe works around it by never scoring unfetched boards.
  - Fresh-clone friction: `ats:scan` needs `data/ats/portals.yml` copied from the example, and `ats:liveness` needs `npx playwright install chromium`.
  - **Conflict to report:** SNICKERDOODLE's DRAFT → SPECIFIED rule requires zero open `[TODO]`s, but the assignment asks the recipe to list proposed additions as `[TODO: DEV]` / `[TODO: DATA SOURCE]`. The recipe keeps its proposal TODOs open and counted (`todos_open` 6, then 7 after G3). **Decision, Hemanth Rayudu, 2026-10-02:** these TODOs are proposals for later versions and for the engine; none sits on the path this version executes, so they are not treated as blocking the sample-run promotion. The conflict stays reported here for the maintainer.
  - Also found: CONTRIBUTING.md says to import `CONFIG, SRC, applyProfile, scoreRole` from `role-scorer.mjs`, but the file exports nothing.

## 2026-10-02 — defects found and fixed during the run

- **Recipe:** manual (same)
- **Inputs:** first live pass `--limit 3` (`evidence/05-first-live-smoke/`); first full live pass (`evidence/06-full-live-run-before-us-fix/`); break attempt with a wrong CSV (`evidence/08a`)
- **Outputs:** `rules.json` 0.1.1; `pipeline.py` (`location_class`, `require_columns`, raw-response hashes); regression tests `LocationRule` and `test_wrong_schema_csv_…`
- **Result:** the PhD-only roles are now excluded; "Anywhere in the US" is classed US; a wrong-schema CSV halts with exit 1 instead of reporting an empty success. The regression test fails without its fix (`evidence/07`).
- **Open issues:** none from these fixes.

## Gate decisions (to be completed by the named human)

- **Sample-run gate (lifecycle):** ☑ cleared. I read `pipeline-report.md` and the `evidence/` folder · by: Hemanth Rayudu · date: 2026-10-02 · note: full sample run complete; conformance, tests and gates G1–G3 cleared; recipe promoted to RUNNABLE-SAMPLE (v0.1.2).
- **G1 liveness:** ☑ cleared. All 11 Apply/Consider links are live. Machine check: `npm run ats:liveness -- --file /tmp/apply-urls.txt` returned `11 active 0 expired 0 uncertain` (`course/2026fa/submissions/hemanthrayuduu/evidence/19-G1-liveness-11-links.txt`). Human check: I opened all 11 in a browser, and each showed its job description and an Apply button (Cohere Health 1, Verkada 6, Databricks 4; for all three, the pipeline's record shows the board name matching the company). Removed: none · by/date: Hemanth Rayudu, 2026-10-02
- **G2 timeline:** ☑ cleared. The persona's OPT start date (2027-01-11) and 60-day hiring-lag assumption are confirmed as a realistic stand-in for my situation; timeline factor 1.0 (margin 131 days) accepted · by/date: Hemanth Rayudu, 2026-10-02
- **G3 release:** ☑ cleared.
  - **Acting on (tailor an application):** Cohere Health "Software Engineer II" and Verkada "Backend Engineer - Connectivity", the two highest-scoring Apply rows.
  - **Kept on the list, no action this pass:** the other 7 Apply rows (Verkada ×5, Databricks Web Products ×2).
  - **Rejected:** both Consider rows. My priority is AI Engineer roles, but the job descriptions disqualify me from both (`course/2026fa/submissions/hemanthrayuduu/evidence/20-G3-ai-engineer-requirements.txt`):
    - Databricks "AI Engineer – Forward Deployed Engineering" says *"not intended for internship, new graduate, or entry-level applicants"*.
    - Databricks "AI FDE, U.S. Public Sector (Federal Focus)" says *"U.S. citizenship and eligibility for a U.S. government secret clearance are required"*.
  - **Finding:** the pipeline reads seniority and eligibility from titles only, so it cannot see these description-level disqualifiers. Logged as recipe `[TODO: DEV]` 7. This run found no AI Engineer role this persona can actually apply to.
  - by/date: Hemanth Rayudu, 2026-10-02

*When the sample-run gate is cleared:* set `status: RUNNABLE-SAMPLE` and `last_gate: "sample-run, <date>, <name>, logs/runs/2026fa-hemanthrayuduu-1.md"` in the recipe frontmatter, and `status: RUNNABLE-SAMPLE` in the prototype README.

## 2026-10-02 — iteration 2: author re-scope, description rules (rules 0.2.1, code 75f3c41)

- **Recipe:** manual (`recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md` v0.2.1, rules 0.2.1, code `75f3c41`)
- **Trigger (author):** the real situation is pre-completion OPT from mid-October, about 3.5 years of experience, AI Engineer roles on the Microsoft AI stack, all US with Texas and remote first.
  - Checked against DHS *Study in the States* (F-1 OPT page, 2026-10-02): the 90-day unemployment limit is stated for post-completion OPT, and the student, not an employer, applies for OPT. So the timeline gate stays on post-completion OPT, and "who sponsors OPT" means "who hires on OPT and sponsors H-1B later".
- **Inputs:**
  - Command: `python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --out-dir course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live-v2`.
  - Persona v2, résumé v2, `rules.json` 0.2.1, `scheme.json`. Same CSV/BLS/Form D files as iteration 1 (sha256 in `pipeline-log.json`).
- **Outputs:** `course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live-v2/`; terminal output `evidence/25-iteration2-final-live-run.txt`.
- **Result:**
  - Funnel: 40 candidates → 10 boards found → 55 AI/ML postings → 40 in the US → 4 at the right level → **1 ruled out by its description** (Databricks Federal Focus: «u.s. citizenship») → 3 kept.
  - Buckets: **apply 0 · consider 3 · network 6 · check-by-hand 30 · skip 1**; skip share 94.5%. Tests 21/21; pii-scan `--diff main` clean.
- **Intermediate passes (kept as evidence):**
  - `23a`: AI-only sponsorship evidence gave 10 candidates and 0 US AI roles. Widened to software-or-AI evidence, with mismatches soft-tiered.
  - `23b`: "Partner Engineer … AI & Apps" and "AI Automation QA Engineer" counted as AI roles. Excluded by rule.
  - `24a`: draft rule dropped any company with one "can't sponsor" posting from networking. **Withdrawn**: `24b` shows the statements are role-specific (Verkada 156/307, Twin Health 23/39, absent on their engineering roles).
- **Open issues:**
  - Nothing reaches Apply, because every AI posting is tier Possible (the CSV's top-few sponsored titles rarely name AI roles; TODO 1).
  - Board coverage is 10 of 40.
  - Senior titles are excluded by default.
  - No Texas AI posting appeared in this run.
  - E-Verify data is absent (TODO 8).
  - **Gates G1–G3 and the sample-run gate for v0.2.1 are not yet cleared.** Recipe status is DRAFT.

## Gate decisions — iteration 2 (v0.2.1) — superseded by iteration 3 before sign-off; not cleared

- **Sample-run gate (lifecycle):** ☐ cleared / ☐ not cleared · by: ______ · date: ______ · note: ______
- **G1 liveness:** links checked for the 3 Consider rows (`npm run ats:liveness -- <url>` or a browser): ___ of 3 live · by/date: ______
- **G2 timeline:** post-completion OPT start (2027-01-11, fictional stand-in) and 60-day hiring lag confirmed · by/date: ______
- **G3 release:** rows I would act on: ______; rows rejected and why: ______; networking targets I would contact: ______ · by/date: ______

## 2026-10-02 — iteration 3: Senior titles + Data Scientist / Data Engineer (rules 0.3.0, code 75f3c41 unchanged)

- **Recipe:** manual (`recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md` v0.3.0, rules 0.3.0, code `75f3c41`)
- **Trigger (author):** "include Senior titles and re-run, include Data Engineer, Data Scientist roles also".
- **Changes:**
  - `rules.json` 0.3.0: Senior patterns removed; `data_science` and `data_engineering` families added, with SOC lookups backed by O*NET (alternate titles: "Data Engineer" under 15-1242.00, "Big Data Engineer" under 15-1243.00); Microsoft data-stack terms added.
  - Persona v3: target and evidence families.
  - Test file: 23 tests.
  - `pipeline.py` unchanged (`git diff 75f3c41 -- pipeline.py` is empty).
- **Inputs:** `python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --out-dir course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live-v3`; same CSV/BLS/Form D files.
- **Outputs:** `course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live-v3/`; `evidence/29-iteration3-live-run.txt`.
- **Result:**
  - Funnel: 49 candidates → 11 boards → 67 AI/data postings → 48 US → 16 right level by title → **9 ruled out by description** (1 citizenship, 8 asking 5+ or 8+ years) → 7 kept.
  - Buckets: **apply 0 · consider 7 · network 6 · check-by-hand 38 · skip 1**; skip share 89.6%.
  - First ★ Texas match: Apptronik "Senior Software Engineer, ML Infrastructure", Austin, TX. Tests 23/23.
- **Hand check (`evidence/30`):**
  - The Austin role states "5+ years of professional software engineering experience" *and* "3+ years …". The lowest-bound rule kept it at 3+ (recipe TODO 9, a human decision; not tuned).
  - Twin Health "Senior AI Engineer" (Remote, USA) asks 5+ years, so it was correctly ruled out. It carries no "can't sponsor" statement.
- **Open issues:**
  - Nothing reaches Apply: all 7 kept postings are tier Possible.
  - No Data Engineer posting appeared on the 11 boards found.
  - "Sr. Developer Advocate, AI and Machine Learning" matched the AI family (ruled out anyway on years). Developer-advocate titles are another title-rule gap.
  - Board coverage 11 of 49.
  - **Gates for v0.3.0 are not yet cleared.**

## Gate decisions — iteration 3 (v0.3.0)

- **Sample-run gate (lifecycle):** ☑ cleared · by: Hemanth Rayudu · date: 2026-10-02 · note: full sample run of v0.3.0 (`runs/2026-10-02-live-v3/`) with conformance, tests (23) and G1–G3 cleared; recipe promoted to RUNNABLE-SAMPLE. The seven open proposal TODOs are treated as non-blocking, as decided for iteration 1. The iteration-3 attestation is signed separately after my own re-run.
- **Author re-runs:**
  - working copy (`evidence/34b`);
  - fresh clone of the branch at `99bc2c9` (`evidence/35`): 23 tests OK, identical live result, clone `git status` empty.
- **G1 liveness:** ☑ cleared. All 7 Consider links are live. Machine check: `npm run ats:liveness -- --file /tmp/consider-urls-v3.txt` returned `7 active 0 expired 0 uncertain` (`course/2026fa/submissions/hemanthrayuduu/evidence/33-iteration3-G1-liveness-7-links.txt`). Human check: I opened all 7 in a browser, and each showed its job description and an Apply button. Removed: none · by/date: Hemanth Rayudu, 2026-10-02
- **G2 timeline:** ☑ cleared. The post-completion OPT start (2027-01-11, fictional stand-in; pre-completion OPT from mid-October) and the 60-day hiring lag are confirmed; timeline factor 1.0 (margin 131 days) · by/date: Hemanth Rayudu, 2026-10-02
- **G3 release:** ☑ cleared.
  - **Acting on (tailor an application) — all 7 Consider rows:**
    - Apptronik "Senior Software Engineer, ML Infrastructure" (★ Austin, TX). Applying knowing its description asks 5+ years of software engineering (TODO 9), so it's a reach.
    - Diligent Robotics "ML Engineer, Manipulation" (★ anywhere in the US).
    - Databricks "AI Engineer – Forward Deployed Engineering".
    - Databricks "Senior Applied ML Engineer - ML4Sys".
    - Databricks "Senior Data Scientist".
    - Verkada "Senior Software Engineer - Computer Vision".
    - Verkada "Software Engineer - Computer Vision" (neither Verkada posting carries Verkada's "can't sponsor this role" statement).
  - **Rejected:** none.
  - **Networking targets:** not decided in this pass.
  - by/date: Hemanth Rayudu, 2026-10-02

## 2026-10-02 — v0.3.1: outputs never overwrite a tracked file (requirements audit, fixes A–D)

- **Recipe:** manual (`recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md` v0.3.1, rules 0.3.0)
- **Trigger:** the author asked whether the work follows the assignment's §1–§4. The audit found:
  - (A) the documented command's default output, `course/…/runs/<today>-live`, collided with the committed iteration-1 folder when run on 2026-10-02;
  - (B) two `[TODO: DEFINE]` items sat in the "Proposed additions" list, which the assignment types as DEV or DATA SOURCE;
  - (C) no `git diff --stat` after iteration 1;
  - (D) no iteration-3 "what the human must judge" note.
- **Changes:**
  - (A) `pipeline.py`: default output `<prototype>/.build/runs/<today>-<mode>/` (gitignored), plus `refuse_tracked_out_dir`; two tests.
  - (B) recipe: the DEFINE items moved to "Open decisions".
  - (C) final `git diff --stat main` added to the evidence (`37`).
  - (D) TEST-REPORT section added. Matching, rules and scoring are unchanged.
- **Result:** 25 tests OK. A break attempt writing into the committed run folder was refused (exit 1), with nothing overwritten (`evidence/36`).
- **Author re-runs (v0.3.1):** working copy (`evidence/38`) and a fresh clone at `0e46158` (`evidence/39`). Both: 25 tests OK; apply 0 · consider 7 · network 6 · check-by-hand 38 · skip 1, identical to v0.3.0; git status empty.
- **Gate decision:** the sample-run gate is re-confirmed for v0.3.1 by these re-runs, and the recipe is back at **RUNNABLE-SAMPLE**. The author's iteration-3 G1–G3 decisions stand for the same 7 rows, since matching and scoring are unchanged · Hemanth Rayudu, 2026-10-02.
- **Open issues:** none from this fix.

## 2026-10-02 — v0.3.2: Canvas ZIP built and tested; output guard made git-independent

- **Recipe:** manual (`recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md` v0.3.2, rules 0.3.0)
- **Inputs:** `bash .build/make-zip.sh` (`git archive` of the branch commit minus `private/`, plus `SUBMISSION.md` at the top level with the SHA filled in). The ZIP was then unzipped and its offline tests run.
- **Outputs:** `../reallocation-hemanthrayuduu-recipe.zip`, outside the repo and rebuilt per commit; `evidence/40`, `41`.
- **Result:**
  - The v0.3.1 ZIP failed one test: the output guard relied on git, and an unzipped submission isn't a checkout.
  - v0.3.2 adds a git-independent check (refuse a non-empty folder this tool didn't write) and skips the gitignore test outside a checkout.
  - The ZIP's tests then pass with git unable to see any repository (`evidence/41`).
- **Open issues:** status is DRAFT until the author re-runs the tests and a fresh clone on v0.3.2. The ZIP must be rebuilt after the final commit. The PR is not opened yet (author's decision).

## 2026-10-03 — iteration 4: years rule v2, fit scale, per-posting audit (rules 0.4.0–0.4.2, recipe 0.4.2)

- **Recipe:** manual (`recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md` v0.4.2)
- **Inputs:** same data and persona as iteration 3; `pipeline.py --out-dir course/2026fa/submissions/hemanthrayuduu/runs/2026-10-03-live-v4` (live, run by Claude Code).
- **Outputs:** `runs/2026-10-03-live-v4/` (report, log, audit, scorer files); `evidence/42`–`44`; `evidence/verify-iteration-1`–`3.md`.
- **Result:**
  - Three live runs, each followed by a hand check of a fixed 23-row sample against the live descriptions: 1 wrong + boundary misses → 2 wrong → **0 wrong**. All 16 years rule-outs of the final run were also checked: 16 of 16 correct.
  - Final: apply 0 · consider 8 · network 6 · check-by-hand 38 · skip 1. 92 target-family postings, 17 ruled out by description, skip share 91.3%. Tests 49/49.
  - TODO 9 closed by the years rule v2 (author's decision in the approved design). `todos_open` 7.
- **Correction:** the iteration-3 entry above says the Austin role states 5+ years *and* 3+ years. The description says 5+ **or** 3+. The entry is left as written; this line corrects it.
- **Author re-run and fresh clone (2026-10-03, at `b81f526`):** 49 tests OK; apply 0 · consider 8 · network 6 · check-by-hand 38 · skip 1, identical to the committed run; clean status in the clone (`evidence/46`, `47`).

## Gate decisions — iteration 4 (v0.4.2)

- **Sample-run gate (lifecycle):** ☑ cleared · by: Hemanth Rayudu · date: 2026-10-03 · note: full sample run of v0.4.2 (`runs/2026-10-03-live-v4/`), my own re-run and fresh clone (`evidence/46`, `47`), conformance, 49 tests and G1–G3 cleared; recipe promoted to RUNNABLE-SAMPLE. The seven open proposal TODOs stay non-blocking, as decided for iteration 1.
- **G1 liveness:** ☑ cleared. All 8 Consider links are live. Machine check: `npm run ats:liveness -- --file .build/kept-urls-v4.txt` returned `8 active 0 expired 0 uncertain` (`course/2026fa/submissions/hemanthrayuduu/evidence/45-iteration4-G1-liveness-8-links.txt`). Human check: I opened all 8, and each showed its job description and an Apply button. Removed: none · by/date: Hemanth Rayudu, 2026-10-03
- **G2 timeline:** ☑ cleared. The post-completion OPT start stand-in (2027-01-11) and the 60-day hiring lag are confirmed; timeline factor 1.0 · by/date: Hemanth Rayudu, 2026-10-03
- **G3 release:** ☑ cleared. Rows I will act on: all 8 Consider rows, Austin (Apptronik) and US-remote (Diligent Robotics) first. Rows rejected: none. (Context added by Claude Code, not the author's words: each row passed the years and eligibility checks, and Verkada's three rows say "We do sponsor … for this role".) · by/date: Hemanth Rayudu, 2026-10-03
