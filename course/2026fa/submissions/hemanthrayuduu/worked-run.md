# Worked run — swe-sponsor-pipeline

## Executive summary

**What this is:** the real runs of the job-list tool for a fictional student who mirrors the author's situation, with every command and its actual output pasted in.

**Why read it:** to see which parts of each result are public records and which are the student's own rules, how the output was checked against its sources, and how the tool changed over three iterations.

**What it found:**
- **Iteration 1** targeted entry-level software roles. A hand check showed both AI roles it suggested were closed to the student.
- **Iteration 2** re-scoped to mid-level AI Engineer roles on the Microsoft AI stack, Texas and remote first. It reads job descriptions for disqualifiers.
- **Iteration 3** added Senior titles and Data Scientist / Data Engineer roles, as the author asked. On 2026-10-02 it found **7 roles worth considering**, including the first Texas match, in Austin. It ruled out 9 postings by their descriptions (one citizenship requirement, eight asking 5+ years).
- **Nothing reached "apply".** That's an honest limit of the sponsorship data, explained below.

---

# Iteration 3 (current): + Senior titles, Data Scientist and Data Engineer

Code `75f3c41` (unchanged since iteration 2) · rules 0.3.0 · recipe 0.3.0 · run folder `runs/2026-10-02-live-v3/`

## What changed from iteration 2 (all your-input)

- **`rules.json` 0.3.0:**
  - the two Senior title patterns are removed, while Staff, Principal, Lead and above are still excluded;
  - new `data_science` and `data_engineering` families, with SOC lookups backed by O*NET ("Data Engineer" is an O*NET alternate title of 15-1242.00);
  - Microsoft data-stack terms added (Data Factory, Synapse, Fabric, Power BI, …).
- **Persona v3:** targets `ml_ai`, `data_science`, `data_engineering`; sponsorship history in any of those or software counts as evidence.
- **Unchanged:** the years-of-experience rule (persona 3.5 + tolerance 1). It now decides which Senior roles fit.

## Commands and real output

### 1. Offline tests

```text
# offline test suite, iteration 3 (code 75f3c41 + rules 0.3.0 / persona v3; test file updated)
$ python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v
test_F1_and_window_filters_drop_companies_without_a_record (test_pipeline.HappyPathOffline) ... ok
test_F2_missing_or_failed_board_is_check_by_hand_and_never_scored (test_pipeline.HappyPathOffline) ... ok
test_F4_soc_without_bls_row_shows_no_wage (test_pipeline.HappyPathOffline) ... ok
test_F5_form_d_match_and_miss_are_both_labelled (test_pipeline.HappyPathOffline) ... ok
test_F6_senior_only_or_non_us_board_becomes_network_target (test_pipeline.HappyPathOffline) ... ok
test_TODO7_description_rules_rule_out_without_scoring (test_pipeline.HappyPathOffline) ... ok
test_cant_sponsor_statements_are_counted_per_company_not_used_to_drop_it (test_pipeline.HappyPathOffline) ... ok
test_completes_and_writes_both_outputs (test_pipeline.HappyPathOffline) ... ok
test_every_value_carries_one_of_the_three_labels (test_pipeline.HappyPathOffline) ... ok
test_live_posting_at_proven_sponsor_is_apply (test_pipeline.HappyPathOffline) ... ok
test_no_network_host_was_contacted (test_pipeline.HappyPathOffline) ... ok
test_real_scorer_produced_the_decisions (test_pipeline.HappyPathOffline) ... ok
test_rules_030_senior_titles_are_scored (test_pipeline.HappyPathOffline) ... ok
test_soft_sponsorship_tier_is_demoted_to_consider (test_pipeline.HappyPathOffline) ... ok
test_stack_terms_years_and_preferred_location_are_labelled_records (test_pipeline.HappyPathOffline) ... ok
test_location_classes (test_pipeline.LocationRule) ... ok
test_F1_named_company_not_in_csv_is_reported_not_scored (test_pipeline.NamedFailures) ... ok
test_F3_closed_opt_window_fails_without_a_timeline_value (test_pipeline.NamedFailures) ... ok
test_missing_csv_fails_clearly (test_pipeline.NamedFailures) ... ok
test_wrong_schema_csv_halts_instead_of_reporting_zero_candidates (test_pipeline.NamedFailures) ... ok
test_family_of (test_pipeline.TitleAndDescriptionRules) ... ok
test_seniority_rules_030 (test_pipeline.TitleAndDescriptionRules) ... ok
test_years_parse_reads_only_experience_requirements (test_pipeline.TitleAndDescriptionRules) ... ok

----------------------------------------------------------------------
Ran 23 tests in 0.231s

OK
exit=0
```

### 2. The live run

```text
$ python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --out-dir course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live-v3
  [1/49] INTEL CORP: not-found
  [2/49] ICON TECHNOLOGY INC: not-found
  [3/49] DATABRICKS INC: found greenhouse:databricks (885 postings)
  [4/49] VERKADA INC: found greenhouse:verkada (307 postings)
  [5/49] CCC INTELLIGENT SOLUTIONS HOLDINGS INC: not-found
  [6/49] GRAMMARLY INC: not-found
  [7/49] WHATNOT INC: not-found
  [8/49] COHERE HEALTH INC: found greenhouse:coherehealth (76 postings)
  [9/49] AIERA INC: not-found
  [10/49] APEX TECHNOLOGY INC: not-found
  [11/49] APPTRONIK INC: found greenhouse:apptronik (80 postings)
  [12/49] CELESTIAL AI INC: not-found
  [13/49] FOURSQUARE LABS INC: not-found
  [14/49] SPANIO INC: not-found
  [15/49] HIGHNOTE PLATFORM INC: not-found
  [16/49] OUTSET MEDICAL INC: found greenhouse:outsetmedical (30 postings)
  [17/49] MERCURY TECHNOLOGIES INC: not-found
  [18/49] TWIN HEALTH INC: found greenhouse:twinhealth (39 postings)
  [19/49] ICERTIS INC: not-found
  [20/49] CYNGN INC: not-found
  [21/49] PSIQUANTUM CORP: found greenhouse:psiquantum (74 postings)
  [22/49] CENTIFIC GLOBAL SOLUTIONS INC: not-found
  [23/49] VIDMOB INC: found ashby:vidmob (3 postings)
  [24/49] AEYE INC: not-found
  [25/49] BLUECORE INC: not-found
  [26/49] DILIGENT ROBOTICS INC: found greenhouse:diligentrobotics (9 postings)
  [27/49] OBSERVE INC: not-found
  [28/49] CODAMETRIX INC: found ashby:codametrix (2 postings)
  [29/49] BUTLR TECHNOLOGIES INC: not-found
  [30/49] VOUCH INC: not-found
  [31/49] AIM INTELLIGENT MACHINES INC: not-found
  [32/49] FARMER'S BUSINESS NETWORK INC: not-found
  [33/49] FEMTOSENSE INC: not-found
  [34/49] LILT INC: not-found
  [35/49] MEMBRION INC: not-found
  [36/49] WORKFUSION INC: not-found
  [37/49] IFOODDECISIONSCIENCES INC: not-found
  [38/49] SWING THERAPEUTICS INC: not-found
  [39/49] UNDERDOG SPORTS HOLDINGS INC: not-found
  [40/49] WAFFLE LABS INC: not-found
  [41/49] BELFRY SOFTWARE INC: not-found
  [42/49] HALCYON TECH INC: not-found
  [43/49] LUMEN ENERGY INC: not-found
  [44/49] MISO ROBOTICS INC: not-found
  [45/49] PLEXIUM INC: found greenhouse:plexium (0 postings)
  [46/49] POLYOPS INC: not-found
  [47/49] PRIME ARTIFICIAL INTELLIGENCE INC: not-found
  [48/49] RAISE ROBOTICS INC: not-found
  [49/49] SERVICENOW INC: not-found
✓ swe-sponsor-pipeline (live): 49 candidates, 49 probed, 11 boards found, 14 roles scored
  apply 0 · consider 7 · network 6 · check-by-hand 38 · skip 1
  scorer: ✓ scored 14 roles → Apply 0 · Consider 7 · Skip 7 (skip 50%)
  course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live-v3/pipeline-report.md  +  course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live-v3/pipeline-log.json
exit=0
```

The Consider table from `runs/2026-10-02-live-v3/pipeline-report.md`, verbatim:

```text
| # | ★ | Company | Posting | Score | Sponsorship evidence | Fit | Years asked | Microsoft AI stack terms | Wage context (SOC) |
|---:|---|---|---|---:|---|---:|---|---|---|
| 1 | ★ austin | APPTRONIK INC | [Senior Software Engineer, ML Infrastructure](https://boards.greenhouse.io/apptronik/jobs/6176116004?gh_jid=6176116004) — Austin, TX `record` | 0.403 | 56 approvals `record`; tier **Possible** (p 0.4) `your-input` | 0.88 `your-input` | 3+ `record` | none found `record` | $140,910 median, job zone 5 `record` · SOC 15-1221.00 via family rule `your-input` |
| 2 | ★ anywhere in the us | DILIGENT ROBOTICS INC | [ML Engineer, Manipulation](https://job-boards.greenhouse.io/diligentrobotics/jobs/7651459003) — Anywhere in the US `record` | 0.290 | 20 approvals `record`; tier **Possible** (p 0.4) `your-input` | 0.50 `your-input` | 3+ `record` | none found `record` | $140,910 median, job zone 5 `record` · SOC 15-1221.00 via family rule `your-input` |
| 3 |  | DATABRICKS INC | [AI Engineer – Forward Deployed Engineering (AI FDE)](https://databricks.com/company/careers/open-positions/job?gh_jid=8546367002) — United States `record` | 0.440 | 1640 approvals `record`; tier **Possible** (p 0.4) `your-input` | 1.00 `your-input` | not stated `record` | azure `record` | $140,910 median, job zone 5 `record` · SOC 15-1221.00 via O*NET title match `record` |
| 4 |  | DATABRICKS INC | [Senior Applied ML Engineer - ML4Sys ](https://databricks.com/company/careers/open-positions/job?gh_jid=8656900002) — San Francisco, California `record` | 0.290 | 1640 approvals `record`; tier **Possible** (p 0.4) `your-input` | 0.50 `your-input` | 4+ `record` | none found `record` | $140,910 median, job zone 5 `record` · SOC 15-1221.00 via family rule `your-input` |
| 5 |  | DATABRICKS INC | [Senior Data Scientist ](https://databricks.com/company/careers/open-positions/job?gh_jid=5634684002) — Mountain View, California; San Francisco, California `record` | 0.290 | 1640 approvals `record`; tier **Possible** (p 0.4) `your-input` | 0.50 `your-input` | not stated `record` | none found `record` | $112,590 median, job zone 4 `record` · SOC 15-2051.00 via O*NET title match `record` |
| 6 |  | VERKADA INC ⚠ 156 of 307 postings here say they can't sponsor that role | [Senior Software Engineer - Computer Vision](https://job-boards.greenhouse.io/verkada/jobs/4128624007) — San Mateo, CA United States `record` | 0.290 | 272 approvals `record`; tier **Possible** (p 0.4) `your-input` | 0.50 `your-input` | 1+ `record` | none found `record` | $140,910 median, job zone 5 `record` · SOC 15-1221.00 via family rule `your-input` |
| 7 |  | VERKADA INC ⚠ 156 of 307 postings here say they can't sponsor that role | [Software Engineer - Computer Vision](https://job-boards.greenhouse.io/verkada/jobs/5195995007) — San Mateo, CA United States `record` | 0.290 | 272 approvals `record`; tier **Possible** (p 0.4) `your-input` | 0.50 `your-input` | 1+ `record` | none found `record` | $140,910 median, job zone 5 `record` · SOC 15-1221.00 via family rule `your-input` |
```

## Verified vs. inferred: the Austin row

| Line | Value | Label | Why |
|---|---|---|---|
| Company H-1B approvals | 56 | **record** | 80 Days CSV |
| Sponsored titles | Senior Electrical Engineer, Software Engineer III | **record** | CSV `top_job_titles_sponsored` |
| Posting | "Senior Software Engineer, ML Infrastructure", Austin, TX | **record** | Greenhouse API, fetched 2026-10-02 |
| Family | `ml_ai` | your-input | role word "engineer" + AI word "ML" (composite rule) |
| Tier and p | Possible, p 0.4 | your-input | ML posting, software-only sponsored titles, so a soft tier |
| ★ preferred | yes, "austin" | your-input | persona `preferred_locations` |
| Years asked | 3+ shown | **record** text, your-input rule | lowest stated bound; the description also says **5+ years** of software engineering (see the cross-check) |
| Fit | 0.875 | your-input | deterministic phrase match against the résumé |
| Score | 0.403 → Consider | **record of arithmetic** | `role-scorer.mjs`; the soft tier caps it at Consider |

## Verification

**Hand cross-check against the live job API**, independent of the pipeline:

```text
# Hand cross-check (iteration 3): the Austin, TX Consider row and a Senior role ruled out on years, read independently from the public Greenhouse job API
$ curl -s https://boards-api.greenhouse.io/v1/boards/apptronik/jobs/6176116004  (title, location, years sentences, sponsorship sentence)
   Senior Software Engineer, ML Infrastructure | Austin, TX
   years: 5+ years of professional software engineering experience in ML platforms, data infrastructure, or 
   years: 3+ years of direct, hands-on experience owning the data and evaluation infrastructure behind model
   sponsor sentence: none found
$ curl -s https://boards-api.greenhouse.io/v1/boards/twinhealth/jobs/5655780004  (title, location, years sentences, sponsorship sentence)
   Senior AI Engineer | Remote, USA
   years: 5+ years of industry experience developing AI and Machine Learning systems in production
   sponsor sentence: 100% Employer sponsored healthcare, dental, and vision for you, and 80% coverage for your family; Hea
```

What it showed:
- **Twin Health "Senior AI Engineer":** correctly ruled out (5+ years), and it really has no "can't sponsor" line; the only "sponsor" text is about healthcare.
- **The Austin role exposes a rule choice.** Its main requirement is 5+ years, but the rule shows 3+. Recorded as `[TODO: DEFINE]` 9 and left for the author to decide, rather than tuned after seeing the result.

## Reflection (iteration 3)

**What worked:** with Senior titles allowed, the years-asked rule did the real filtering. 8 Senior roles were ruled out on 5+ or 8+ years, and the ones left state 3–4 years or nothing.

**What it missed:**
1. **The Austin role's 5+ years main requirement** (TODO 9).
2. **No Data Engineer posting appeared on the 11 boards found.** The family is in place, but this sample has none.
3. **"Sr. Developer Advocate, AI and Machine Learning" matched the AI family**, a new title-rule gap. It was ruled out anyway on years.

**Next improvement:** the same as iteration 2. Per-petition SOC data (TODO 1), so AI and data postings at big software sponsors can reach Apply on evidence.

## Attestation (iteration 3)

- Recipe: swe-sponsor-pipeline v0.3.0 (rules 0.3.0, code commit 75f3c41)
- By: **[Hemanth Rayudu signs after re-running the tests and the live run himself] · [date]**. The rows below were run by Claude Code in the author's session on 2026-10-02.

### Tested

| Ran | Saw | Expected |
|---|---|---|
| `python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v` | `Ran 23 tests … OK` | all pass offline |
| `pipeline.py --out-dir course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live-v3` | apply 0 · consider 7 · network 6 · check-by-hand 38 · skip 1; 9 ruled out by description | completes; only the two named hosts |
| **Break, by rule change:** with the Senior patterns removed, does the fixture Senior posting get scored? | `test_rules_030_senior_titles_are_scored` passes; Staff still excluded (`test_seniority_rules_030`) | Senior in, Staff out |
| Hand cross-check: Apptronik 6176116004, Twin Health 5655780004 via the API | "5+ years … and 3+ years …"; "5+ years …", no can't-sponsor line | matches the report, and exposes TODO 9 |

### Did not test

- Data Engineer postings live (none on the boards found); the family is tested with titles only (`test_family_of`).
- Lever, Workday, iCIMS, SmartRecruiters; E-Verify; clauses worded outside the phrase lists.
- A fresh clone for iteration 3 *(to be run by the author)*.

### Broke during testing, fixed

- `test_F6_…` failed after the Senior change, because fixture 102 "Senior Software Engineer" was now scored. That's the intended effect, so the test was updated and a dedicated test added.

---

# Iteration 2: mid-level AI Engineer, Microsoft AI stack

Code `75f3c41` · rules 0.2.1 · recipe 0.2.1 · run folder `runs/2026-10-02-live-v2/`

## Inputs

| Input | Value | Label |
|---|---|---|
| Persona | `search/examples/kiran-rao/persona.json` v2: fictional MS CS student. Pre-completion OPT from mid-October 2026; post-completion OPT start 2027-01-11, the date the timeline gate uses (DHS: the 90-day limit is a post-completion rule). About 3.5 years of experience. Targets `ml_ai` postings; software or AI sponsorship history counts as evidence. Preferred: Texas, remote, "anywhere in the US". 60-day hiring lag; 24-month funding window | your-input |
| Résumé | `search/examples/kiran-rao/resume.example.json` v2: AI Engineer and ML Engineer co-op; Azure OpenAI, AI Foundry, Azure ML, AI Search, Semantic Kernel, AutoGen, C#/.NET | your-input |
| Rules | `rules.json` 0.2.1 + `scheme.json` (greenhouse-watch default, location weights 0) | your-input |
| Records | 80 Days CSV (full shipped file), BLS compact CSV, Form D **samples**, live Greenhouse/Ashby boards fetched 2026-10-02 | record |

## Commands and real output

### 1. Offline tests

```text
# offline test suite, iteration 2 (code 75f3c41)
$ python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v
test_F1_and_window_filters_drop_companies_without_a_record (test_pipeline.HappyPathOffline) ... ok
test_F2_missing_or_failed_board_is_check_by_hand_and_never_scored (test_pipeline.HappyPathOffline) ... ok
test_F4_soc_without_bls_row_shows_no_wage (test_pipeline.HappyPathOffline) ... ok
test_F5_form_d_match_and_miss_are_both_labelled (test_pipeline.HappyPathOffline) ... ok
test_F6_senior_only_or_non_us_board_becomes_network_target (test_pipeline.HappyPathOffline) ... ok
test_TODO7_description_rules_rule_out_without_scoring (test_pipeline.HappyPathOffline) ... ok
test_cant_sponsor_statements_are_counted_per_company_not_used_to_drop_it (test_pipeline.HappyPathOffline) ... ok
test_completes_and_writes_both_outputs (test_pipeline.HappyPathOffline) ... ok
test_every_value_carries_one_of_the_three_labels (test_pipeline.HappyPathOffline) ... ok
test_live_posting_at_proven_sponsor_is_apply (test_pipeline.HappyPathOffline) ... ok
test_no_network_host_was_contacted (test_pipeline.HappyPathOffline) ... ok
test_real_scorer_produced_the_decisions (test_pipeline.HappyPathOffline) ... ok
test_soft_sponsorship_tier_is_demoted_to_consider (test_pipeline.HappyPathOffline) ... ok
test_stack_terms_years_and_preferred_location_are_labelled_records (test_pipeline.HappyPathOffline) ... ok
test_location_classes (test_pipeline.LocationRule) ... ok
test_F1_named_company_not_in_csv_is_reported_not_scored (test_pipeline.NamedFailures) ... ok
test_F3_closed_opt_window_fails_without_a_timeline_value (test_pipeline.NamedFailures) ... ok
test_missing_csv_fails_clearly (test_pipeline.NamedFailures) ... ok
test_wrong_schema_csv_halts_instead_of_reporting_zero_candidates (test_pipeline.NamedFailures) ... ok
test_family_of (test_pipeline.TitleAndDescriptionRules) ... ok
test_years_parse_reads_only_experience_requirements (test_pipeline.TitleAndDescriptionRules) ... ok

----------------------------------------------------------------------
Ran 21 tests in 0.490s

OK
exit=0
```

### 2. The live run

```text
$ python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --out-dir course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live-v2
  [1/40] INTEL CORP: not-found
  [2/40] DATABRICKS INC: found greenhouse:databricks (885 postings)
  [3/40] VERKADA INC: found greenhouse:verkada (307 postings)
  [4/40] CCC INTELLIGENT SOLUTIONS HOLDINGS INC: not-found
  [5/40] GRAMMARLY INC: not-found
  [6/40] WHATNOT INC: not-found
  [7/40] COHERE HEALTH INC: found greenhouse:coherehealth (76 postings)
  [8/40] AIERA INC: not-found
  [9/40] APEX TECHNOLOGY INC: not-found
  [10/40] APPTRONIK INC: found greenhouse:apptronik (80 postings)
  [11/40] CELESTIAL AI INC: not-found
  [12/40] FOURSQUARE LABS INC: not-found
  [13/40] SPANIO INC: not-found
  [14/40] HIGHNOTE PLATFORM INC: not-found
  [15/40] MERCURY TECHNOLOGIES INC: not-found
  [16/40] TWIN HEALTH INC: found greenhouse:twinhealth (39 postings)
  [17/40] CYNGN INC: not-found
  [18/40] PSIQUANTUM CORP: found greenhouse:psiquantum (74 postings)
  [19/40] CENTIFIC GLOBAL SOLUTIONS INC: not-found
  [20/40] VIDMOB INC: found ashby:vidmob (3 postings)
  [21/40] AEYE INC: not-found
  [22/40] BLUECORE INC: not-found
  [23/40] DILIGENT ROBOTICS INC: found greenhouse:diligentrobotics (9 postings)
  [24/40] OBSERVE INC: not-found
  [25/40] CODAMETRIX INC: found ashby:codametrix (2 postings)
  [26/40] BUTLR TECHNOLOGIES INC: not-found
  [27/40] VOUCH INC: not-found
  [28/40] AIM INTELLIGENT MACHINES INC: not-found
  [29/40] FEMTOSENSE INC: not-found
  [30/40] MEMBRION INC: not-found
  [31/40] IFOODDECISIONSCIENCES INC: not-found
  [32/40] SWING THERAPEUTICS INC: not-found
  [33/40] UNDERDOG SPORTS HOLDINGS INC: not-found
  [34/40] BELFRY SOFTWARE INC: not-found
  [35/40] HALCYON TECH INC: not-found
  [36/40] LUMEN ENERGY INC: not-found
  [37/40] MISO ROBOTICS INC: not-found
  [38/40] PLEXIUM INC: found greenhouse:plexium (0 postings)
  [39/40] RAISE ROBOTICS INC: not-found
  [40/40] SERVICENOW INC: not-found
✓ swe-sponsor-pipeline (live): 40 candidates, 40 probed, 10 boards found, 10 roles scored
  apply 0 · consider 3 · network 6 · check-by-hand 30 · skip 1
  scorer: ✓ scored 10 roles → Apply 0 · Consider 3 · Skip 7 (skip 70%)
  course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live-v2/pipeline-report.md  +  course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live-v2/pipeline-log.json
exit=0
```

The Consider table from `runs/2026-10-02-live-v2/pipeline-report.md`, verbatim:

```text
| # | ★ | Company | Posting | Score | Sponsorship evidence | Fit | Years asked | Microsoft AI stack terms | Wage context (SOC) |
|---:|---|---|---|---:|---|---:|---|---|---|
| 1 | ★ anywhere in the us | DILIGENT ROBOTICS INC | [ML Engineer, Manipulation](https://job-boards.greenhouse.io/diligentrobotics/jobs/7651459003) — Anywhere in the US `record` | 0.290 | 20 approvals `record`; tier **Possible** (p 0.4) `your-input` | 0.50 `your-input` | 3+ `record` | none found `record` | $140,910 median, job zone 5 `record` · SOC 15-1221.00 via family rule `your-input` |
| 2 |  | DATABRICKS INC | [AI Engineer – Forward Deployed Engineering (AI FDE)](https://databricks.com/company/careers/open-positions/job?gh_jid=8546367002) — United States `record` | 0.440 | 1640 approvals `record`; tier **Possible** (p 0.4) `your-input` | 1.00 `your-input` | not stated `record` | azure `record` | $140,910 median, job zone 5 `record` · SOC 15-1221.00 via O*NET title match `record` |
| 3 |  | VERKADA INC ⚠ 156 of 307 postings here say they can't sponsor that role | [Software Engineer - Computer Vision](https://job-boards.greenhouse.io/verkada/jobs/5195995007) — San Mateo, CA United States `record` | 0.290 | 272 approvals `record`; tier **Possible** (p 0.4) `your-input` | 0.50 `your-input` | 1+ `record` | none found `record` | $140,910 median, job zone 5 `record` · SOC 15-1221.00 via family rule `your-input` |
```

## Verified vs. inferred, line by line

**Consider row: Databricks "AI Engineer – Forward Deployed Engineering", score 0.440**

| Line | Value | Label | Why |
|---|---|---|---|
| H-1B approvals | 1,640 | **record** | 80 Days CSV row |
| Top sponsored titles | Software Engineer, Senior Software Engineer, Solutions Architect, … | **record** | `top_job_titles_sponsored` |
| Sponsored families | `software` only | your-input | title-family rule applied to the record |
| Posting family | `ml_ai` | your-input | title contains "ai engineer" |
| Tier and p | **Possible**, p 0.4 | your-input | rule: posting family not among sponsored families, so a soft tier |
| Funding | 2025-09-08, $1,074,999,900; Form D sample match | **record** | CSV row; Form D sample |
| Live | factor 1.0 | **record** | in the Greenhouse response fetched 2026-10-02; board name «Databricks» matches |
| Location | "United States", no ★ | **record** / your-input | posting field / preference rule |
| Years asked | not stated | **record** (absence) | the description says "extensive years", with no number |
| Eligibility / sponsorship phrases | none found | **record** (absence) | phrase lists in `rules.json` |
| Stack terms | `azure` | **record** | word match on the posting text |
| Fit | 1.0 (scheme score 9.75, capped at 8) | your-input | matched: résumé title «AI Engineer», PyTorch, LangChain, RAG, LLM, machine learning, Azure. **No model** |
| Timeline | 1.0 (margin 131 days) | your-input | persona dates |
| Wage | $140,910 median, job zone 5, SOC 15-1221.00 | **record** | BLS row; SOC via O*NET title «AI Engineer» (record) |
| Score and decision | (0.4·0.35 + 1·0.30) × 1 × 1 = 0.440 → Consider | **record of arithmetic** | `role-scorer.mjs` (soft tier demotes Apply to Consider) |

**Ruled out: Databricks "AI FDE, U.S. Public Sector (Federal Focus)".** The phrase «u.s. citizenship» in its description is a **record**. The rule that the phrase rules the student out is **your-input**. In iteration 1 this took a human at gate G3; now it is automatic.

**Network row: Twin Health.** These are records: 40 H-1B approvals; funding 2025-05-07, $55,000,000; Greenhouse board with 39 postings; and **23 of 39** postings saying *"we are unable to sponsor … at this time"*. "No qualifying AI posting" applies the rules to those postings: its AI postings are "Senior" or "Staff", which the mid-level rule excludes. So it stays a networking target, with the count shown beside it for the student to judge.

## Verification: how the output was confirmed real

1. **Hand cross-check against the sources:**

```text
# Hand cross-check (iteration 2), independent of the pipeline
$ grep CSV rows for CODAMETRIX INC and DILIGENT ROBOTICS INC (approvals, sponsored titles, funding)
   CODAMETRIX INC | approvals 18.0 | titles ['NLP Scientist'] | funding 2025-04-16 15000000.0
   DILIGENT ROBOTICS INC | approvals 20.0 | titles ['Staff Software Engineer'] | funding 2025-02-13 20000000.0
$ curl Diligent Robotics posting 7651459003: title, location, and the years sentence
   ML Engineer, Manipulation | Anywhere in the US
   years: 3+ years of experience applying ML to robotics manipulation, visuomotor control, or sequ
$ BLS row 15-1221.00 (wage shown for AI/ML postings)
   15-1221.00 | Computer and Information Research Scientists | median 140910.0 | zone 5
```

2. **Checking the tool's own rule against the data.** This is how a draft rule was withdrawn. A draft of 0.2.1 dropped any company from networking if *one* posting said "unable to sponsor". The raw descriptions showed the statements are role-specific:

```text
# Why the company-wide rule was withdrawn: context of "unable to sponsor" on the two boards (raw responses from runs/2026-10-02-live-v2/.build/raw, rules draft 0.2.1)
== verkada: 156 of 307 postings contain 'unable to sponsor'
  most common wording (117x): …aily Commuter benefits Additional Information You must be independently authorized to work in the U.S. We are unable to sponsor or take over sponsorship of an employment visa for this role, at this…
  engineering titles WITHOUT the statement (first 8): ['AI Marketing Engineer', 'AV Engineer - East Coast (NYC)', 'AV Engineer - London & United States East Coast', 'Backend Engineer - Connectivity', 'Backend Software Engineering Intern 2027', 'Business Systems Support Engineer', 'Director of Firmware Engineering, Cameras', 'Embedded Automated Test & Test System Engineer']
== twinhealth: 23 of 39 postings contain 'unable to sponsor'
  most common wording (16x): …e opportunity based out of the U.S. Applicants must be authorized to work for any employer in the U.S. We are unable to sponsor or take over sponsorship of an employment Visa at this time. Compensa…
  engineering titles WITHOUT the statement (first 8): ['Lead Software Engineer', 'Senior AI Engineer', 'Senior AI Platform Engineer']
```

3. **Deliberate break: switch off the description rules.** The test must fail:

```text
# break check (iteration 2): description_check patched to never rule anything out; the TODO 7 test must FAIL
$ python3 - <<EOF   (patch P.description_check -> (None, info), run HappyPathOffline)
======================================================================
FAIL: test_TODO7_description_rules_rule_out_without_scoring (test_pipeline.HappyPathOffline)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/HemanthRayudu/Profession/Assignments/Prompt Engineering/the-reallocation-engine/scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/test_pipeline.py", line 140, in test_TODO7_description_rules_rule_out_without_scoring
    self.assertEqual(set(ruled), {"105", "106", "402"}, "description rules did not rule out the expected postings")
AssertionError: Items in the second set but not the first:
'106'
'402'
'105' : description rules did not rule out the expected postings

----------------------------------------------------------------------
Ran 13 tests in 0.057s

FAILED (failures=1)
failed tests: ['test_TODO7_description_rules_rule_out_without_scoring']
```

## Iteration 1 → iteration 2: what changed and why

| | Iteration 1 (rules 0.1.1) | Iteration 2 (rules 0.2.1) | Why it changed |
|---|---|---|---|
| Who | MS student, December graduation, entry-level software/AI | pre-completion OPT, about 3.5 years, mid-level AI Engineer, Microsoft stack | the author corrected the situation |
| Reads job descriptions | no (titles only) | yes: citizenship/clearance, can't-sponsor, years | G3 in iteration 1 found both AI roles disqualified only in their descriptions |
| Location | US only, no preference; fit −1 if not Boston | US only; Texas/remote/anywhere-US first (★); location removed from fit | author's preference |
| Sponsorship evidence | posting family must match sponsored titles | software **or** AI sponsorship counts; a mismatch gets the soft tier | only 100 of 1,552 sponsors list an AI title in the top-few list (evidence/23a: 10 candidates → 40) |
| Result | apply 9 · consider 2 · network 4 · check 28 | apply 0 · consider 3 · network 6 · check 30 · 1 ruled out by description | different target, stricter evidence |

## Reflection (iteration 2)

**What worked:**
- Reading descriptions caught, automatically, the citizenship requirement a human had to find in iteration 1.
- Testing the tool's own rule against raw data stopped a wrong company-wide "doesn't sponsor" rule from shipping.
- The ★ preference and the stack column show the student's priorities without changing a single score.

**What it got wrong or missed:**
1. **The first iteration-2 pass found only 10 candidates and no US AI roles.** The sponsorship filter demanded AI titles in a top-few list (`evidence/23a`). Widening the evidence to software titles, while keeping AI postings soft-tiered, fixed the scope without inflating any score.
2. **"AI" plus "engineer" matched a partner role and a QA role.** They're now excluded by rule (0.2.1).
3. **I (Claude) first told the author that Twin Health "won't sponsor".** That was based on one posting. The data showed it was role-specific; the claim and the rule were withdrawn (`evidence/24a`, `24b`).
4. **Nothing reaches Apply.** Every AI posting is tier Possible, because the CSV's sponsored-title list rarely names AI titles. That reflects the data, not the market. Per-petition SOC data (TODO 1) is the real fix.
5. **Senior roles are excluded by default** for a 3.5-year engineer. Twin Health's "Senior AI Engineer", with no "can't sponsor" line, is hidden by that choice.

**One concrete next improvement:** join DOL LCA disclosure data (SOC code per petition) to the 80 Days CSV, so "has this company sponsored an AI Engineer?" becomes a record match rather than a top-few title list. Then re-run and compare the Consider list.

## Attestation (iteration 2): superseded by iteration 3 before signing, not signed

- Recipe: swe-sponsor-pipeline v0.2.1 (rules 0.2.1, code commit 75f3c41)
- By: **[Hemanth Rayudu signs after re-running rows 1, 2 and 6 himself] · [date]**. The rows below were run by Claude Code in the author's session on 2026-10-02.

### Tested

| Ran | Saw | Expected |
|---|---|---|
| `python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v` | `Ran 21 tests … OK` | all pass offline |
| `pipeline.py --out-dir course/2026fa/submissions/hemanthrayuduu/runs/2026-10-02-live-v2` | apply 0 · consider 3 · network 6 · check-by-hand 30 · skip 1; 1 ruled out by description; hosts: the two named APIs | completes; both outputs; only named hosts |
| **Break:** `description_check` patched to never rule out | `FAIL: test_TODO7_description_rules_rule_out_without_scoring` | the test catches it |
| **Break (on real data):** draft rule "one 'can't sponsor' posting drops the company" | Twin Health dropped from networking although its Senior AI postings carry no such statement | rule withdrawn; statements now counted per company (`24a`, `24b`) |
| Hand cross-check: CodaMetrix / Diligent CSV rows, Diligent posting via curl, BLS 15-1221.00 | 18 approvals, NLP Scientist; 20 approvals; "3+ years of experience …"; median 140910, zone 5 | report matches sources |
| Fresh clone of the branch, tests + `--limit 3` | *(to be run by the author)* | 21 OK; exit 0; `git status` clean |

### Did not test

- Lever, Workday, iCIMS, SmartRecruiters boards (not probed).
- Eligibility or no-sponsorship clauses worded outside the phrase lists.
- Whether any company would actually sponsor this candidate; no recruiter contacted.
- Texas-specific results: no ★ Texas posting appeared in the AI lists of this run, so the Texas match was exercised only with a fixture (Austin, TX).
- E-Verify status of any employer (no data; TODO 8).
- Python other than 3.9.10, Node other than 23.11.0; Windows.

### Broke during testing, fixed

- Candidate filter too strict (10 candidates, 0 US AI roles) → `sponsorship_evidence_families` in the persona (`23a` → `25`).
- Partner and QA roles counted as AI roles → `not_if_title_has` in `rules.json` 0.2.1; tests in `test_family_of`.
- Company-wide "doesn't sponsor" draft rule → withdrawn before commit; statements counted per company; test `test_cant_sponsor_statements_are_counted_per_company_not_used_to_drop_it`.
- The test caught the disabled description rules only as a crash (`KeyError`) → explicit assertion added (`evidence/22`).

---

# Iteration 1 (record): entry-level SWE/AI, code e26febd, rules 0.1.1

*Kept unchanged below as the record of the first iteration, including its signed attestation. Its findings motivated iteration 2.*

### Inputs

| Input | Value | Label |
|---|---|---|
| Persona | `search/examples/kiran-rao/persona.json`: fictional MS CS student, Boston, graduating 2026-12-18, OPT start 2027-01-11, 90 unemployment days, hiring-lag assumption 60 days, funding window 24 months, ≥ 1 H-1B approval | your-input |
| Résumé | `search/examples/kiran-rao/resume.example.json` (fictional; `@example.com`, 555 phone) | your-input |
| Rules | `scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/rules.json` v0.1.1 | your-input |
| Sponsorship + funding | `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` (shipped, full file) | record |
| Form D | `data/sec/form-d/processed/sample/*.sample.json`: **samples only** (4 × 50 companies) | record |
| Wages | `data/bls/compact/soc_occupation_compact.csv` | record |
| Live boards | `boards-api.greenhouse.io`, `api.ashbyhq.com`, fetched 2026-10-02 | record |

### Commands and real output

#### 1. Offline test

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

#### 2. The live sample run

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

#### 3. Named failure F1 on real data: company not in the CSV, and a CSV company with no H-1B record

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

#### 4. Named failure F3: OPT window already closed

```text
# F3 on real data: persona whose OPT window closed before --today
$ python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --persona scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/fixtures/persona.past-opt.fixture.json --today 2026-10-01 --out-dir /tmp/ssp-f3
ERROR: OPT window already closed: opt_start_date 2026-01-05 + 90 unemployment days = 2026-04-05, which is before today 2026-10-01. No timeline factor computed.
exit=1
$ ls /tmp/ssp-f3
ls: /tmp/ssp-f3: No such file or directory
```

### Verified vs. inferred, line by line

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

### Verification: how the output was confirmed real

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

### Reflection

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

### Attestation

- Recipe: swe-sponsor-pipeline v0.1.1 (rules 0.1.1, code commit e26febd)
- By: Hemanth Rayudu · 2026-10-02. I re-ran rows 1, 2 and 6 myself on 2026-10-02: 16 tests OK; live run gave apply 9 · consider 2 · network 4 · check-by-hand 28 · skip 2 (scorer: Apply 9 · Consider 2 · Skip 6), identical to the committed run; fresh clone of the branch: 16 tests OK, `--limit 3` run apply 8 · consider 2 · check-by-hand 1, `git status --short` empty. The other rows were run by Claude Code in my session on 2026-10-02.
- Note added after signing (2026-10-02): the recipe text moved to v0.1.2 (TODO 7 from gate G3, one "cannot verify" line, the lifecycle note, and the frontmatter promotion). Code `e26febd` and `rules.json` 0.1.1, which the rows below tested, are unchanged.

#### Tested

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

#### Did not test

- Lever, Workday, iCIMS and SmartRecruiters boards (not probed at all).
- Whether any Apply posting would actually sponsor this candidate. No recruiter was contacted.
- Ashby board identity on a real Apply row (none occurred in this run).
- F4 on real data. The real BLS file has both SOCs the run used, so "unmapped" was exercised only with a fixture.
- Python versions other than 3.9.10, and Node other than 23.11.0. Windows was not tested.
- Rate limits or throttling from Greenhouse/Ashby under repeated runs.
- The timeline gate closing on real data. The persona's margin is 131 days; a closed gate was tested only through F3's halt.
- *(Since tested at gate G1, after signing: `npm run ats:liveness` on all 11 Apply/Consider links gave `11 active 0 expired 0 uncertain`, and Hemanth opened each one in a browser. See `evidence/19-G1-liveness-11-links.txt` and the run log.)*

#### Broke during testing, fixed

- PhD-only roles on the Apply list → `rules.json` 0.1.1 adds `\bph\.?d\b` (`evidence/05-first-live-smoke/`).
- "Anywhere in the US" classed non-US → `location_class` in `pipeline.py` and regression test `LocationRule` (`evidence/06-…`, `07-…`).
- Wrong-schema CSV gave exit 0 with an empty result → `require_columns` in `pipeline.py` and `test_wrong_schema_csv_…` (`evidence/08a`, `08b`).
- pii-scan hits in raw board responses (gitignored, never committed) → sha256 per response in the log; `.build/` cleared before scanning.
