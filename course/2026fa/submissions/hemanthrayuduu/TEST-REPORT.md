# TEST-REPORT — swe-sponsor-pipeline

## Executive summary

**What this is:** the record of every check run on the job-list tool before submission, across two iterations: toolchain checks, real-data runs, the named failure cases, deliberate break attempts, and hand comparisons with the sources.

**Why read it:** to see what was actually run and observed, as opposed to what was intended.

**What it found:**
- **Iteration 1 (entry-level software/AI):** the tool runs from a fresh copy with no installation, all its tests passed, and every named failure stopped cleanly. Two real defects (a location bug and a silent wrong-file success) were fixed and covered by tests.
- **Iteration 2 (the author's real situation: mid-level AI Engineer, Microsoft stack, Texas and remote first):** the tool reads job descriptions, and all 21 tests pass. A disabled rule is caught by the tests. Testing on real data also caught and withdrew a wrong rule before it shipped: one that treated "can't sponsor this role" as company-wide.
- **Iteration 3 (Senior titles + Data Scientist / Data Engineer):** a rules-only change; all 23 tests pass, and 7 roles reached Consider, including the first Texas match. A hand check exposed a rule choice: when a description states two year requirements, the lower one is used.
- **The weakness stated plainly:** with the shipped data, no AI posting reaches "apply", because the sponsorship records rarely name AI titles.

## Iteration 3 checks (code `75f3c41` unchanged, rules 0.3.0, recipe 0.3.0)

| # | Check | Command / action | Observed | Evidence |
|---|---|---|---|---|
| I3-1 | Code unchanged | `git diff --stat 75f3c41 -- scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py` | empty | (this report) |
| I3-2 | Offline tests | `python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v` | `Ran 23 tests … OK`. The first run failed `test_F6_…` because the Senior fixture was now scored, which is the intended effect, so the test was updated | `31-iteration3-offline-tests.txt` |
| I3-3 | Live run | `pipeline.py --out-dir …/runs/2026-10-02-live-v3` | 49 candidates → 11 boards → 67 AI/data postings → 48 US → 16 right level → 9 ruled out by description → 7 kept. **apply 0 · consider 7 · network 6 · check-by-hand 38 · skip 1**; skip share 89.6% | `29-iteration3-live-run.txt`, `runs/2026-10-02-live-v3/` |
| I3-4 | Hand cross-check | Apptronik 6176116004 and Twin Health 5655780004 via the Greenhouse API | Austin role: "5+ years … and 3+ years …", shown as 3+ (lowest-bound rule; TODO 9). Twin Health Senior AI Engineer: 5+ years, correctly ruled out; no can't-sponsor line | `30-iteration3-hand-cross-check.txt` |
| I3-5 | Toolchain after | doctor, verify, conformance, `pii-scan --diff main`, scope | see evidence | `32-iteration3-toolchain-after.txt` |
| I3-6 | Fresh clone + author re-run | *(to be run by the author before signing)* | — | — |

## Iteration 2 checks (code `75f3c41`, rules 0.2.1, recipe 0.2.1)

| # | Check | Command / action | Observed | Evidence |
|---|---|---|---|---|
| I2-1 | Offline tests | `python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v` | `Ran 21 tests … OK`; tests now use `fixtures/persona.fixture.json`, so editing the real persona can't break them | `27-iteration2-offline-tests.txt` |
| I2-2 | Break: description rules disabled | patch `description_check` to never rule out; run `HappyPathOffline` | `FAIL: test_TODO7_description_rules_rule_out_without_scoring` (assertion; the first version only crashed with `KeyError`, so an explicit assertion was added) | `22-break-description-rules-disabled.txt` |
| I2-3 | First live pass, AI-only sponsorship evidence | `pipeline.py --out-dir …/runs/2026-10-02-live-v2` (rules 0.2.0) | 10 candidates, 2 boards, 0 US AI roles. Only 100 of 1,552 sponsors list an AI title | `23a-iteration2-first-pass-ai-titles-only.txt` |
| I2-4 | Second pass, software-or-AI evidence | same command | consider 4 · network 6. False positives: "Partner Engineer … AI & Apps", "AI Automation QA Engineer" | `23b-iteration2-live-run.txt`, `23b-report-rules-0.2.0.md` |
| I2-5 | Break on real data: company-wide "can't sponsor" rule (draft 0.2.1) | same command | Twin Health dropped from networking on one posting's statement | `24a-…-WITHDRAWN.txt` |
| I2-6 | Checking that draft rule against raw descriptions | read "unable to sponsor" contexts on two boards | role-specific: Verkada 156/307 (sales/ops, not backend), Twin Health 23/39 (not "Senior AI Engineer") → **rule withdrawn** | `24b-cant-sponsor-statements-are-role-specific.txt` |
| I2-7 | Final live run | same command (rules 0.2.1) | 40 candidates → 10 boards → 55 AI/ML postings → 40 US → 4 right level → 1 ruled out by description → 3 kept. **apply 0 · consider 3 · network 6 · check-by-hand 30 · skip 1**; skip share 94.5%; hosts: the two named APIs | `25-iteration2-final-live-run.txt`, `runs/2026-10-02-live-v2/` |
| I2-8 | TODO 7 handoff on real data | Federal Focus role | ruled out automatically: «u.s. citizenship». A human had to catch it in iteration 1 | report "Ruled out by the job description" |
| I2-9 | Hand cross-check | CSV rows, Diligent posting via curl, BLS 15-1221.00 | CodaMetrix 18 approvals, "NLP Scientist"; Diligent 20, "3+ years of experience …"; median 140910, zone 5. All match the report | `26-iteration2-hand-cross-check.txt` |
| I2-10 | Toolchain after | doctor, verify, conformance, `pii-scan --diff main`, scope | all pass; pii `clean ✓`; 85 files, all in the five assigned namespaces | `28-iteration2-toolchain-after.txt` |
| I2-11 | Fresh clone + author re-run | *(to be run by the author before signing the iteration-2 attestation)* | — | — |

**Iteration 2 named failure cases:**
- F1 and F3 are unchanged code paths, and their tests pass.
- F2 (board not found): 30 companies in check-by-hand.
- F4 (no BLS row) and F5 (no Form D match): tests pass; F5 is seen live (all but Databricks).
- F6 (wrong level / non-US only): 6 networking targets.
- New for iteration 2: description rule-outs (eligibility, no-sponsorship, years). Exercised by fixtures 105, 106 and 402, and live by the Federal Focus role.

---

# Iteration 1 (record)

## Run record (iteration 1)

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
