# Run log — 2026fa-hemanthrayuduu-1

## Executive summary

This is the run record for a new job-search recipe that lists open entry-level software and AI jobs at companies with a public record of visa sponsorship and recent funding. One full live run on 2026-10-02 completed and was checked against its sources. Two bugs found along the way were fixed. The student then checked the results by hand and signed off on 2026-10-02, which promoted the recipe from draft to runnable-on-sample-data. That review found that both AI Engineer roles the tool suggested were ones this student cannot apply to.

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
