# Worked run — swe-sponsor-pipeline

## Executive summary

**What this is:** one complete, real run of the job-list tool for a fictional student, with every command and its actual output pasted in.

**Why read it:** to see which parts of each result are public records and which are the student's own rules or assumptions, and how the output was checked against its sources.

**What it found:**
- On 2026-10-02 the tool narrowed 30,369 company records to 37 companies that sponsored visas for software or machine-learning titles and raised money in the past two years.
- It found job boards for 9 of them.
- It recommended 9 postings to apply to and 2 to consider, and named 4 strong sponsors to network into because they had no matching opening.
- It listed 28 companies to check by hand.

Checking the output against the source files found it accurate. Building and testing it surfaced two real bugs (fixed) and one design weakness (a strong sponsor alone is enough for "apply"), which is reported below rather than hidden.

## Inputs

| Input | Value | Label |
|---|---|---|
| Persona | `search/examples/kiran-rao/persona.json`: fictional MS CS student, Boston, graduating 2026-12-18, OPT start 2027-01-11, 90 unemployment days, hiring-lag assumption 60 days, funding window 24 months, ≥ 1 H-1B approval | your-input |
| Résumé | `search/examples/kiran-rao/resume.example.json` (fictional; `@example.com`, 555 phone) | your-input |
| Rules | `scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/rules.json` v0.1.1 | your-input |
| Sponsorship + funding | `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` (shipped, full file) | record |
| Form D | `data/sec/form-d/processed/sample/*.sample.json`: **samples only** (4 × 50 companies) | record |
| Wages | `data/bls/compact/soc_occupation_compact.csv` | record |
| Live boards | `boards-api.greenhouse.io`, `api.ashbyhq.com`, fetched 2026-10-02 | record |

## Commands and real output

### 1. Offline test

```text
# offline test suite
$ python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v
test_F1_and_window_filters_drop_companies_without_a_record (test_pipeline.HappyPathOffline) ... ok
test_F2_missing_or_failed_board_is_check_by_hand_and_never_scored (test_pipeline.HappyPathOffline) ... ok
test_F4_soc_without_bls_row_shows_no_wage (test_pipeline.HappyPathOffline) ... ok
test_F5_form_d_match_and_miss_are_both_labelled (test_pipeline.HappyPathOffline) ... ok
test_F6_senior_only_or_non_us_board_becomes_network_target (test_pipeline.HappyPathOffline) ... ok
test_completes_and_writes_both_outputs (test_pipeline.HappyPathOffline) ... ok
test_every_value_carries_one_of_the_three_labels (test_pipeline.HappyPathOffline) ... ok
test_live_new_grad_posting_at_proven_sponsor_is_apply (test_pipeline.HappyPathOffline) ... ok
test_no_network_host_was_contacted (test_pipeline.HappyPathOffline) ... ok
test_real_scorer_produced_the_decisions (test_pipeline.HappyPathOffline) ... ok
test_soft_sponsorship_tier_is_demoted_to_consider (test_pipeline.HappyPathOffline) ... ok
test_location_classes (test_pipeline.LocationRule) ... ok
test_F1_named_company_not_in_csv_is_reported_not_scored (test_pipeline.NamedFailures) ... ok
test_F3_closed_opt_window_fails_without_a_timeline_value (test_pipeline.NamedFailures) ... ok
test_missing_csv_fails_clearly (test_pipeline.NamedFailures) ... ok
test_wrong_schema_csv_halts_instead_of_reporting_zero_candidates (test_pipeline.NamedFailures) ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.062s

OK
exit=0
```

### 2. The live sample run

```text
$ python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py
  [1/37] INTEL CORP: not-found
  [2/37] DATABRICKS INC: found greenhouse:databricks (886 postings)
  [3/37] VERKADA INC: found greenhouse:verkada (307 postings)
  [4/37] CCC INTELLIGENT SOLUTIONS HOLDINGS INC: not-found
  [5/37] GRAMMARLY INC: not-found
  [6/37] WHATNOT INC: not-found
  [7/37] COHERE HEALTH INC: found greenhouse:coherehealth (76 postings)
  [8/37] APEX TECHNOLOGY INC: not-found
  [9/37] APPTRONIK INC: found greenhouse:apptronik (80 postings)
  [10/37] CELESTIAL AI INC: not-found
  [11/37] FOURSQUARE LABS INC: not-found
  [12/37] SPANIO INC: not-found
  [13/37] HIGHNOTE PLATFORM INC: not-found
  [14/37] MERCURY TECHNOLOGIES INC: not-found
  [15/37] TWIN HEALTH INC: found greenhouse:twinhealth (37 postings)
  [16/37] CYNGN INC: not-found
  [17/37] PSIQUANTUM CORP: found greenhouse:psiquantum (74 postings)
  [18/37] CENTIFIC GLOBAL SOLUTIONS INC: not-found
  [19/37] VIDMOB INC: found ashby:vidmob (3 postings)
  [20/37] AEYE INC: not-found
  [21/37] BLUECORE INC: not-found
  [22/37] DILIGENT ROBOTICS INC: found greenhouse:diligentrobotics (9 postings)
  [23/37] OBSERVE INC: not-found
  [24/37] BUTLR TECHNOLOGIES INC: not-found
  [25/37] VOUCH INC: not-found
  [26/37] AIM INTELLIGENT MACHINES INC: not-found
  [27/37] MEMBRION INC: not-found
  [28/37] IFOODDECISIONSCIENCES INC: not-found
  [29/37] SWING THERAPEUTICS INC: not-found
  [30/37] UNDERDOG SPORTS HOLDINGS INC: not-found
  [31/37] BELFRY SOFTWARE INC: not-found
  [32/37] HALCYON TECH INC: not-found
  [33/37] LUMEN ENERGY INC: not-found
  [34/37] MISO ROBOTICS INC: not-found
  [35/37] PLEXIUM INC: found greenhouse:plexium (0 postings)
  [36/37] RAISE ROBOTICS INC: not-found
  [37/37] SERVICENOW INC: not-found
✓ swe-sponsor-pipeline (live): 37 candidates, 37 probed, 9 boards found, 17 roles scored
  apply 9 · consider 2 · network 4 · check-by-hand 28 · skip 2
  scorer: ✓ scored 17 roles → Apply 9 · Consider 2 · Skip 6 (skip 35%)
  course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live/pipeline-report.md  +  course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live/pipeline-log.json
exit=0
```

The resulting report is `runs/2026-10-02-live/pipeline-report.md`. Its Apply table, verbatim (first three rows):

```text
| # | Company | Posting | Score | Sponsorship evidence | Fit | Wage context (SOC) |
|---:|---|---|---:|---|---:|---|
| 1 | COHERE HEALTH INC | [Software Engineer II](https://job-boards.greenhouse.io/coherehealth/jobs/7930480003) — United States `record` | 0.568 | 104 approvals `record`; tier **Proven** (p 0.9) `your-input` | 0.84 `your-input` | $133,080 median, job zone 4 `record` · SOC 15-1252.00 via family rule `your-input` |
| 2 | VERKADA INC | [Backend Engineer - Connectivity](https://job-boards.greenhouse.io/verkada/jobs/5194598007) — San Mateo, CA United States `record` | 0.559 | 272 approvals `record`; tier **Proven** (p 0.9) `your-input` | 0.81 `your-input` | $133,080 median, job zone 4 `record` · SOC 15-1252.00 via family rule `your-input` |
| 3 | VERKADA INC | [Embedded Software Engineer - Access Control](https://job-boards.greenhouse.io/verkada/jobs/5233102007) — San Mateo, CA United States `record` | 0.540 | 272 approvals `record`; tier **Proven** (p 0.9) `your-input` | 0.75 `your-input` | $133,080 median, job zone 4 `record` · SOC 15-1252.00 via family rule `your-input` |
```

### 3. Named failure F1 on real data: company not in the CSV, and a CSV company with no H-1B record

```text
# F1 on real data: a company not in the CSV, a CSV company with no H-1B record, and a real candidate
$ python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --company "Imaginary Rocket Co" --company "10000 INC" --company "VERKADA INC" --out-dir /tmp/ssp-f1
  [1/1] VERKADA INC: found greenhouse:verkada (307 postings)
✓ swe-sponsor-pipeline (live): 1 candidates, 1 probed, 1 boards found, 6 roles scored
  apply 6 · consider 0 · network 0 · check-by-hand 0 · skip 0
  scorer: ✓ scored 6 roles → Apply 6 · Consider 0 · Skip 0 (skip 0%)
  ✗ Imaginary Rocket Co: not in the 80 Days CSV — no sponsorship record, not scored
  ✗ 10000 INC: no H-1B approvals on record (Total Approvals = blank)
  /tmp/ssp-f1/pipeline-report.md  +  /tmp/ssp-f1/pipeline-log.json
exit=0
```

### 4. Named failure F3: OPT window already closed

```text
# F3 on real data: persona whose OPT window closed before --today
$ python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --persona scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/fixtures/persona.past-opt.fixture.json --today 2026-10-01 --out-dir /tmp/ssp-f3
ERROR: OPT window already closed: opt_start_date 2026-01-05 + 90 unemployment days = 2026-04-05, which is before today 2026-10-01. No timeline factor computed.
exit=1
$ ls /tmp/ssp-f3
ls: /tmp/ssp-f3: No such file or directory
```

## Verified vs. inferred, line by line

**Row 1 of the Apply list: Cohere Health, "Software Engineer II", score 0.568**

| Line in the result | Value | Label | Why that label |
|---|---|---|---|
| Company has H-1B approvals | 104 (2 denials, 98.1% rate) | **record** | read from the 80 Days CSV row |
| Sponsored titles include a software title | "Software Engineer II", "Senior Software Engineer, Platform", … | **record** | same row, `top_job_titles_sponsored` |
| Posting family = software | `software` | your-input | `title_families` pattern match (rule) |
| Sponsorship tier and p | Proven, p 0.9 | your-input | rule: ≥ 10 approvals and same family → 0.9 |
| Latest funding inside window | 2025-05-07, $89,999,876 | **record** | CSV row; window start 2024-10-02 is your-input |
| Form D sample | no match | **record** (absence) | samples hold 196 companies |
| Posting is live | factor 1.0 | **record** | present in the Greenhouse board response fetched 2026-10-02. Board name «Cohere Health» matches |
| Location | "United States" | **record** | posting field; "US" class is a rule |
| Not senior | passes | your-input | title has no excluded word (rule) |
| Fit | p 0.844 (scheme score 6.75 / 8) | your-input | deterministic phrase match; the matched phrases are listed in `fit_lines`. **No model judgment** |
| Timeline | factor 1.0 (191 − 60 = 131 days margin) | your-input | the persona's OPT date and lag assumption |
| Wage context | $133,080 median, job zone 4 | **record** | BLS row 15-1252.00 (OEWS 2024) |
| SOC 15-1252.00 for this title | via family rule | your-input | no O*NET title in the shipped sample matched "Software Engineer II" |
| Score and decision | (0.9·0.35 + 0.844·0.30) × 1 × 1 = 0.568 → Apply | **record of arithmetic** | written by `role-scorer.mjs`, not by this tool |

**A networking row: Apptronik.** These are records: 56 approvals; sponsored titles including "Software Engineer III"; funding 2025-01-31, $415,000,000; Greenhouse board fetched, 80 postings. These are your-input rules: "73 are other roles, 7 are senior, so 0 qualify" applies the family and seniority rules to those postings. The liveness factor 0.0 is a record that no posting *passed the rules*, not a record that the company isn't hiring. The decision to treat it as a networking target is the rules' (`eligible_tiers`), and the student's at gate G3.

**What is never in the output:** a `model-judgment` value. The test walks the whole log and fails if one appears.

## Verification: how the output was confirmed real

1. **Hand cross-check against the sources.** The CSV row, the BLS row and the live posting were re-read without the pipeline:

```text
# Hand cross-check 1: report row "COHERE HEALTH INC — 104 approvals" vs the raw 80 Days CSV row
$ grep "^COHERE HEALTH INC," data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv | cut -d, -f1,15-
  company_name: COHERE HEALTH INC
  latest_funding_date: 2025-05-07
  latest_funding_amount: 89999876.0
  Total Approvals: 104.0
  Total Denials: 2.0
  Approval_Rate: 98.1132075471698
  top_job_titles_sponsored: ['Engineering Manager ', 'Senior Software Engineer, Platform', 'Senior Machine Learning DevOps Engineer', 'Software Engineer II', 'Machine Learning Engineer']
$ grep -o "COHERE HEALTH INC.*" pipeline-report.md (Apply row, first 260 chars)
COHERE HEALTH INC | [Software Engineer II](https://job-boards.greenhouse.io/coherehealth/jobs/7930480003) — United States `record` | 0.568 | 104 approvals `record`; tier **Proven** (p 0.9) `your-input` | 0.84 `your-input` | $133,080 median, job zone 4 `record`

# Hand cross-check 2: wage context "$133,080 median, job zone 4 · SOC 15-1252.00" vs the BLS compact CSV
$ python3 -c (print onet_soc_code, title, annual_median_wage, job_zone, oews_year for 15-1252.00)
   15-1252.00 | Software Developers | median 133080.0 | zone 4 | oews_year 2024

# Hand cross-check 3: posting is really on the live board (independent of the pipeline, via curl)
$ curl -s https://boards-api.greenhouse.io/v1/boards/coherehealth/jobs/7930480003 | python3 -c "print title, location"
   Software Engineer II | United States | updated 2026-08-21T16:30:45-04:00
```

All three match the report.

2. **Deliberate break: give it the wrong file.** Before the fix, the BLS file passed as the 80 Days CSV produced a "successful" empty run:

```text
# break attempt: wrong CSV (BLS file passed as the 80 Days CSV) — BEFORE schema check
$ python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --csv data/bls/compact/soc_occupation_compact.csv --out-dir /tmp/ssp-break
✓ swe-sponsor-pipeline (live): 0 candidates, 0 probed, 0 boards found, 0 roles scored
  apply 0 · consider 0 · network 0 · check-by-hand 0 · skip 0
  /tmp/ssp-break/pipeline-report.md  +  /tmp/ssp-break/pipeline-log.json
exit=0
```

After adding a column check:

```text
# break attempt: wrong CSV — AFTER schema check
$ python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --csv data/bls/compact/soc_occupation_compact.csv --out-dir /tmp/ssp-break2
ERROR: 80 Days CSV data/bls/compact/soc_occupation_compact.csv is missing columns ['company_name', 'website', 'Total Approvals', 'Total Denials', 'Approval_Rate', 'top_job_titles_sponsored', 'latest_funding_date', 'latest_funding_amount', 'latest_funding_stage', 'total_funding'] — wrong file or schema change; nothing scored
exit=1
```

3. **Deliberate break: does the test catch the bug it was written for?** The location fix was stashed and the tests re-run:

```text
# break check: pipeline.py WITHOUT the US-location fix (git stash), test_pipeline.py WITH the regression test
$ python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py'
FAIL: test_location_classes (test_pipeline.LocationRule)
AssertionError: 'non-us' != 'us'
Ran 15 tests in 0.067s
FAILED (failures=1)
```

## Reflection

**What worked:**
- Reusing the repo's own pieces made a real end-to-end path with little new code: the slug normalizer, the greenhouse-watch fetcher and fit scheme, and the engine scorer run as a subprocess.
- Refusing to score companies whose board wasn't fetched mattered. The scorer would otherwise treat their missing liveness evidence as "live".
- The skip share across everything evaluated was 96%, so most of the student's time is protected from roles that don't fit.

**What it got wrong or missed:**
1. **The first live pass recommended two PhD-only roles** to an MS student (`evidence/05-first-live-smoke/`). Rules 0.1.1 excludes them.
2. **"Anywhere in the US" was read as non-US.** That put Diligent Robotics on the networking list while it had a matching posting (`evidence/06-…`). It was fixed, and a regression test now fails without the fix.
3. **A wrong input file produced a quiet empty success.** That is the most dangerous kind of failure for someone short on time, because it reads as "no jobs today".
4. **Sponsorship alone clears Apply.** Databricks "Software Engineer, Web Products" is Apply at fit 0.25, because 0.35 × 0.9 = 0.315 ≥ 0.30. Prediction P3 expected the opposite (most results demoted to Consider), and P3 was wrong.
5. **Coverage is thin.** Only 9 of 37 boards were found by guessing slugs (prediction P1 was confirmed), and the four ATSs not probed hide large sponsors.
6. **Title-family matching is coarse.** Verkada's "Embedded Software Engineer" counts as software, and Twin Health's family match comes from a sponsored "Senior Backend Engineer". Prediction P2 was confirmed. Only gate G3 catches this today.
7. **Both AI Engineer suggestions were roles this student cannot apply to.** This was caught at gate G3, after the run. Databricks "AI Engineer – Forward Deployed Engineering" is *"not intended for internship, new graduate, or entry-level applicants"*. The Federal Focus variant requires *"U.S. citizenship and eligibility for a U.S. government secret clearance"* (`evidence/20-G3-ai-engineer-requirements.txt`). The tool reads seniority from titles only, so description-level disqualifiers pass straight through. For a student who wants AI Engineer roles most, this run found **none** they can apply to. That is the most important limitation for this persona (recipe TODO 7).

**One concrete next improvement:** close `[TODO: DEFINE]` #5 with a fit floor. For example, only Apply when fit p ≥ 0.4, otherwise Consider. Pass it to the scorer as an explicit human-chosen rule, and add a test row with Proven sponsorship and fit 0.25 that must land in Consider. It is one rule plus one test, and it addresses the failure most likely to waste an application.

## Attestation

- Recipe: swe-sponsor-pipeline v0.1.1 (rules 0.1.1, code commit e26febd)
- By: Hemanth Rayudu · 2026-10-02. I re-ran rows 1, 2 and 6 myself on 2026-10-02: 16 tests OK; live run gave apply 9 · consider 2 · network 4 · check-by-hand 28 · skip 2 (scorer: Apply 9 · Consider 2 · Skip 6), identical to the committed run; fresh clone of the branch: 16 tests OK, `--limit 3` run apply 8 · consider 2 · check-by-hand 1, `git status --short` empty. The other rows were run by Claude Code in my session on 2026-10-02.
- Note added after signing (2026-10-02): the recipe text moved to v0.1.2 (TODO 7 from gate G3, one "cannot verify" line, the lifecycle note, and the frontmatter promotion). Code `e26febd` and `rules.json` 0.1.1, which the rows below tested, are unchanged.

### Tested

| Ran | Saw | Expected |
|---|---|---|
| `python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v` | `Ran 16 tests … OK`; no host contacted | all pass offline |
| `python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py` | exit 0; apply 9 · consider 2 · network 4 · check-by-hand 28 · skip 2; hosts: the two named APIs | completes; both outputs written; only named hosts |
| `--company "Imaginary Rocket Co" --company "10000 INC" --company "VERKADA INC"` | not-in-CSV and no-H-1B messages; Verkada scored | F1 reported, nothing invented |
| `--persona fixtures/persona.past-opt.fixture.json --today 2026-10-01` | `ERROR: OPT window already closed …`, exit 1, no output folder | F3 fails without a timeline value |
| **Break:** `--csv data/bls/compact/soc_occupation_compact.csv` | before fix: `✓ … 0 candidates` exit 0 (**wrong**); after fix: `ERROR … missing columns`, exit 1 | a halt, not a polite empty report |
| **Break:** stash the location fix, re-run the tests | `FAIL: test_location_classes 'non-us' != 'us'` | the regression test catches the bug |
| Hand cross-check: Cohere Health CSV row, BLS 15-1252.00 row, live posting via curl | 104.0 approvals; 133080.0 median, zone 4; "Software Engineer II", United States | the report matches its sources |
| `git clone` the branch to `/tmp`, then tests + `--limit 3` | 16 OK; exit 0; `git status` clean | runs on a fresh clone, writes nothing tracked |

### Did not test

- Lever, Workday, iCIMS and SmartRecruiters boards (not probed at all).
- Whether any Apply posting would actually sponsor this candidate. No recruiter was contacted.
- Ashby board identity on a real Apply row (none occurred in this run).
- F4 on real data. The real BLS file has both SOCs the run used, so "unmapped" was exercised only with a fixture.
- Python versions other than 3.9.10, and Node other than 23.11.0. Windows was not tested.
- Rate limits or throttling from Greenhouse/Ashby under repeated runs.
- The timeline gate closing on real data. The persona's margin is 131 days; a closed gate was tested only through F3's halt.
- *(Since tested at gate G1, after signing: `npm run ats:liveness` on all 11 Apply/Consider links gave `11 active 0 expired 0 uncertain`, and Hemanth opened each one in a browser. See `evidence/19-G1-liveness-11-links.txt` and the run log.)*

### Broke during testing, fixed

- PhD-only roles on the Apply list → `rules.json` 0.1.1 adds `\bph\.?d\b` (`evidence/05-first-live-smoke/`).
- "Anywhere in the US" classed non-US → `location_class` in `pipeline.py` and regression test `LocationRule` (`evidence/06-…`, `07-…`).
- Wrong-schema CSV gave exit 0 with an empty result → `require_columns` in `pipeline.py` and `test_wrong_schema_csv_…` (`evidence/08a`, `08b`).
- pii-scan hits in raw board responses (gitignored, never committed) → sha256 per response in the log; `.build/` cleared before scanning.
