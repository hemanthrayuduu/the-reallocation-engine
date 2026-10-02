# TEST-REPORT — swe-sponsor-pipeline

## Executive summary

**What this is:** the record of every check run on the job-list tool before submission: the toolchain before and after, a run from a fresh copy of the branch, a run on real data, each predicted failure, and two deliberate attempts to break it.

**Why read it:** to see what was actually run and observed, as opposed to what was intended.

**What it found:**
- The tool runs from a fresh copy with no installation.
- All 16 offline tests pass.
- Every named failure stops cleanly without inventing a value.
- The changes stay inside the assigned folders.

Testing also found two real defects, both fixed and now covered by tests:
1. A location bug that put a company with a matching job on the wrong list.
2. A silent failure: given the wrong input file, the tool reported a "successful" run with nothing in it.

It also exposed a design weakness, recorded rather than tuned away: a strong sponsorship record alone is enough for an "apply" recommendation.

## Run record

| Field | Value |
|---|---|
| Branch | `contrib/2026fa-hemanthrayuduu-swe-sponsor-pipeline` |
| Code commit tested from a clean clone | `e26febd` (later commits change documentation only) |
| Node / Python / OS | v23.11.0 / 3.9.10 / Darwin 27.0.0 |
| Run date | 2026-10-02 |
| Who ran it | Claude Code, the agent, in the student's session. The student re-runs the clean-checkout and test commands before signing the attestation in `worked-run.md`. |
| Raw evidence | `evidence/` (numbered files are verbatim terminal output) |

## Checks

| # | Check | Command / action | Observed | Evidence |
|---|---|---|---|---|
| 1 | Toolchain before | `npm run doctor`; `npm run verify` | both exit 0; verify passes with 3 pre-existing manifest warnings | `evidence/00-doctor-before.txt`, `01-verify-before.txt` |
| 2 | Engine run once | `npm run ats:scan -- --dry-run` | **failed on a fresh clone**: `portals.yml not found`. Worked after `cp data/ats/portals.example.yml data/ats/portals.yml` (gitignored target) | `02-…`, `02b-…` |
| 3 | Engine run once | `npm run ats:liveness -- <Databricks job URL>` | **failed**: Playwright browser missing. Worked after `npx playwright install chromium` → `✅ active` | `03a-…`, `03b-…` |
| 4 | Engine run once | `npm run score -- data/examples/ch11-roles.json --out-dir course/2026fa/submissions/hemanthrayuduu/runs` | `scored 5 roles → Apply 2 · Consider 1 · Skip 2`; tracked example output untouched | `04-score-ch11.txt` |
| 5 | Offline tests | `python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v` | `Ran 16 tests … OK`. Network is patched to raise; `hosts_contacted == []` | `12-offline-tests.txt` |
| 6 | Clean checkout | `git clone --branch … /tmp/ssp-clean`, then the tests and `pipeline.py --limit 3` | 16 OK; live run exit 0; `git status --short` empty afterwards | `14-clean-checkout-run.txt` |
| 7 | Real sample run (live) | `python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py` | 30,369 rows → 37 candidates → 9 boards found → 253 SWE/ML postings → **apply 9 · consider 2 · network 4 · check-by-hand 28 · skip 2**; overall skip share 96%; hosts: `api.ashbyhq.com`, `boards-api.greenhouse.io` (108 calls) | `09-final-live-run.txt`, `runs/2026-10-02-live/` |
| 8 | F1: company not in CSV / no H-1B record | `--company "Imaginary Rocket Co" --company "10000 INC" --company "VERKADA INC"` | `✗ Imaginary Rocket Co: not in the 80 Days CSV — no sponsorship record, not scored`; `✗ 10000 INC: no H-1B approvals on record (Total Approvals = blank)`; Verkada scored | `10-F1-named-companies.txt` |
| 9 | F2: board 404 / fetch failure / wrong board | live: 28 `not-found`; fixtures: 404, simulated HTTP 503, board-name mismatch | all in `check-by-hand`; **none in `roles.json`** (test asserts it) | `09-…`; tests `test_F2_…` |
| 10 | F3: OPT window closed | `--persona fixtures/persona.past-opt.fixture.json --today 2026-10-01` | `ERROR: OPT window already closed … No timeline factor computed.`, exit 1, output folder not created | `11-F3-opt-window-closed.txt` |
| 11 | F4: SOC with no BLS row | fixture BLS without `15-1221.00`; ML posting | `wage_context.status = "unmapped"`, no wage number | test `test_F4_…` (not observed on real data: the real BLS file has both SOCs used) |
| 12 | F5: no Form D sample match | live run | 36 of 37 labeled `no Form D sample match — funding from 80 Days CSV only`; Databricks matched | `runs/2026-10-02-live/pipeline-log.json` |
| 13 | F6: senior-only / non-US board | live run | Apptronik, Twin Health, PsiQuantum, VidMob → `network` (e.g. Apptronik: 80 postings, 73 other roles, 7 senior) | `09-…`, report "Network" table |
| 14 | **Break 1:** wrong input file | `--csv data/bls/compact/soc_occupation_compact.csv` | **before fix:** `✓ … 0 candidates`, exit 0, a silent failure. **After:** `ERROR: … missing columns […]`, exit 1 | `08a-…`, `08b-…`; test `test_wrong_schema_csv_…` |
| 15 | **Break 2:** does the regression test catch the location bug? | `git stash` the fix, run tests | `FAIL: test_location_classes … 'non-us' != 'us'`; passes with the fix | `07-regression-test-catches-us-bug.txt` |
| 16 | Hand cross-check | CSV row, BLS row and live API compared with the report | Cohere Health: 104.0 approvals, funding 2025-05-07 ✓; 15-1252.00 median 133080.0, zone 4 ✓; posting 7930480003 "Software Engineer II", United States ✓ | `13-hand-cross-check.txt` |
| 17 | Conformance | `node scripts/conformance.mjs scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/ recipes/cases/2026fa/` | `✓ all conform` | (re-run in PR body) |
| 18 | Toolchain after | `npm run doctor`; `npm run verify` | both exit 0, same output as before | `15-doctor-after.txt`, `16-verify-after.txt` |
| 19 | Privacy | `node scripts/pii-scan.mjs`; `--diff main` | tree: 1 finding, an email inside `package-lock.json` that is **already on `main`** (an npm package author's address, not from this work; not reproduced here so this file stays scan-clean). Branch diff: `clean ✓` | `17-pii-scan.txt` |
| 20 | Scope | `git diff --stat main` | 54 files at the time of the snapshot, before the documentation commit added the rest; all under `course/2026fa/submissions/hemanthrayuduu/`, `recipes/cases/2026fa/`, `scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/`, `search/examples/kiran-rao/` | `18-diff-stat.txt` |
| 21 | Gate G1 (human + machine) | `npm run ats:liveness -- --file /tmp/apply-urls.txt`; Hemanth opened all 11 links | `11 active 0 expired 0 uncertain`; every page showed its description and an Apply button | `19-G1-liveness-11-links.txt`, run log |
| 22 | Gate G3 (human, agent-assisted) | the two AI Engineer job descriptions pulled from the Greenhouse job API and searched for eligibility terms | #10 "not intended for … new graduate"; #11 "U.S. citizenship and … secret clearance are required". **Both rejected** at G3 | `20-G3-ai-engineer-requirements.txt`; recipe TODO 7 |

## Defects found and fixed during testing

1. **PhD roles on an MS student's Apply list** (first live pass, `evidence/05-first-live-smoke/`). Two "Systems PhD - Software Engineer" postings were recommended. Fix: `rules.json` 0.1.1 adds `\bph\.?d\b` to the seniority exclusions, with a changelog line. This is a rule change, so it is labeled your-input.
2. **"Anywhere in the US" classed non-US** (first full live run, `evidence/06-full-live-run-before-us-fix/`). Diligent Robotics went to the networking list although it had a matching US posting. Fix: `location_class` recognizes `US` / `U.S.` / `USA` case-sensitively. Regression test `LocationRule`.
3. **Wrong-schema CSV gave a successful empty run** (break 1). Fix: `require_columns` halts on missing columns, for both CSVs.
4. **pii-scan flagged company addresses in raw board responses** (in gitignored `.build/`, never committed). Fix: each raw response's sha256 is recorded in the log, and `.build/` is cleared before scanning.

## Found and NOT fixed (by design or out of scope)

- **Sponsorship alone clears Apply.** Proven p 0.9 × weight 0.35 = 0.315 ≥ 0.30. Logged as `[TODO: DEFINE]` in the recipe. Changing it is a human decision, not a tuning step.
- **The timeline gate doesn't bind for this persona yet.** 191 days available against a 60-day lag gives factor 1.0 everywhere. It starts to matter once OPT starts.
- **Board discovery coverage is 24% (9/37).** Prediction P1 was confirmed.
- **Fit penalizes "United States"-wide postings as a location miss** (−1.0 for not Boston and not "remote"). That rule comes from the shared greenhouse-watch scheme, which is not edited here.

## What the gates require a human to judge

- **G1:** each of the 11 Apply/Consider links is live. All 11 come from Greenhouse boards whose name matched the CSV company (Verkada 6, Databricks 4, Cohere Health 1). The only Ashby board found, VidMob, is on the networking list with identity unverified.
- **G2:** `opt_start_date` 2027-01-11 and the 60-day hiring lag are the student's own.
- **G3:** for each row, the sponsored titles fit the posting. Example: Verkada's "Embedded Software Engineer" against its sponsored software titles. The role should also be genuinely entry level.
