---
status: RUNNABLE-SAMPLE  # DRAFT | SPECIFIED | RUNNABLE-SAMPLE | RUNNABLE-LIVE. Sample-run gate cleared by a named human; see "Lifecycle note" for how the open TODOs are counted.
todos_open: 7
last_gate: "sample-run, 2026-10-02, Hemanth Rayudu, logs/runs/2026fa-hemanthrayuduu-1.md (G1–G3 cleared)"
attestation: null  # set only at VERIFIED; the sample-run attestation is in course/2026fa/submissions/hemanthrayuduu/worked-run.md
recipe_version: 0.1.2  # 0.1.2: TODO 7 + gate result added after G3 (text only; code and rules unchanged from 0.1.1)
---

# swe-sponsor-pipeline — live SWE/AI postings at sponsoring, recently funded companies

## Executive summary

**What it does:** for an international master's student in computer science who graduates in December and hasn't started post-graduation work authorization (OPT), it finds open, entry-level, US software and AI engineering jobs at companies that, by public record, have sponsored H-1B visas for that kind of title and raised money recently. It labels every piece of evidence behind each job. Then it stops, and the student decides.

**Who it's for:** that student, with the 90-day unemployment clock about to start, deciding where to spend the two research-and-apply hours of the day.

**What it decides:** each result gets a next action:
- **apply:** tailor an application;
- **consider:** apply if time allows;
- **network:** a strong, recently funded sponsor with no matching opening today, so ask for an informational conversation instead;
- **check by hand:** the company's job board couldn't be found automatically, which is not the same as having no jobs;
- **skip.**

It never applies, never emails, and never treats a guess as a record.

**Handoff condition (done when):**
- `pipeline.py` exits 0 and writes both `pipeline-log.json` and `pipeline-report.md`.
- Every value in the log carries `record` or `your-input`. `model-judgment` never appears, because this recipe makes no model calls.
- Every company with no fetched board is in `check-by-hand` and absent from `roles.json`.
- The scorer's own `role-scores.json` exists, with its `_scorer` field.
- The report's skip share across all evaluated postings is shown with its denominator.

"The list looks reasonable" is not the condition.

## Required reads

1. `SNICKERDOODLE.md`: gates, provenance, labels.
2. `DOMAIN.md`: layout, known gaps.
3. `data/80-days-to-stay/README.md`: what the mapped CSV is.
4. `scripts/score/role-scorer.mjs`: how votes and gates combine (read the CONFIG block).
5. `.claude/skills/greenhouse-watch/SKILL.md`: the fit scheme and the allow-listed fetcher this recipe reuses.
6. This recipe and its card, `recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.card.md`.

## Purpose and source inventory

| Evidence | Engine layer | Source (exact path or host) | Label | Role in decision |
|---|---|---|---|---|
| H-1B approvals, denials, approval rate, top sponsored titles | 80 Days to Stay | `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` (30,369 rows; 1,552 with approvals) | record | candidate filter + sponsorship **vote** |
| Latest funding date / amount / stage | 80 Days to Stay | same CSV | record | candidate filter (the scorer has no funding vote; see TODO 4) |
| Form D cross-check | 80 Days to Stay | `data/sec/form-d/processed/sample/companies-sec-*-d.sample.json` (4 files × 50 companies) | record | reported only |
| Live postings | Job-Ops | `boards-api.greenhouse.io`, `api.ashbyhq.com` via `.claude/skills/greenhouse-watch/scripts/greenhouse_watch.py` (`board_url`, `fetch_board`, `normalize_jobs`) | record | liveness **gate** |
| Company → slug | Job-Ops | `scripts/ats/scrapers/common/normalize.py` (`normalize_company_name`) | rule | discovery |
| Fit | (résumé) | `judge()` in `greenhouse_watch.py` + `.claude/skills/greenhouse-watch/scheme.default.json` against `search/examples/kiran-rao/resume.example.json` | your-input (deterministic) | fit **vote** |
| Wage, job zone, cognitive pivot score | Cognitive Pivot | `data/bls/compact/soc_occupation_compact.csv` | record (SOC mapping: record or your-input) | context only (Fact 1) |
| OPT start, hiring lag, funding window | — | `search/examples/kiran-rao/persona.json` | your-input | timeline **gate**, filter |
| Thresholds, patterns, tier p-values | — | `scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/rules.json` (v0.1.1) | your-input | all rules |
| Decision | engine | `scripts/score/role-scorer.mjs`, run as a subprocess with `--out-dir`, never copied | record of arithmetic | Apply / Consider / Skip |

**Prototype command** (repo root; Python 3.9+ stdlib, Node 20+):

```bash
python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py
```

**Test** (offline, fixtures only; any network call fails it):

```bash
python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v
```

**How the engine's known gaps are handled:**

| Fact | Handling here |
|---|---|
| 1. `role_quality` weight is 0.0 `[VERIFY]` | Wage, job zone and `cognitive_pivot_score` are shown **beside** each posting as context. They are **not** sent to the scorer. No weight is proposed. Every target posting maps to 15-1252.00 or 15-1221.00 (job zone 4 vs 5, pivot 3.83 vs 4.52), and choosing a weight with no calibration set would invent a number. |
| 2. `bls:local-wage` feeds nothing | Not used. The wage shown is the **national** OEWS median, labeled as such. It is not this employer's pay or the metro's pay. |
| 3. Only Form D samples ship | The cross-check covers 196 sample companies, and **1** of them (Databricks) overlaps this run's candidates. Funding comes from the 80 Days CSV columns. Every miss is labeled "no Form D sample match". |
| 4. Planned directories don't exist | Gates write to paths that exist: the run folder under `course/2026fa/submissions/hemanthrayuduu/` and `logs/runs/`. No gate uses `logs/gate-decisions/` or `data/verified/`. |
| 5. `snickerdoodle` CLI is roadmap | No such command appears in this recipe. |
| 7 and 8. local-wage `.venv`; H-1B join validator | Neither is used. Only the shipped CSV and samples are read. |
| Found while building: **a missing gate defaults to open (1.0)** in `role-scorer.mjs` | Companies whose board wasn't fetched are **never** written to `roles.json`. They go to `check-by-hand`. A test enforces this. |
| Found while building: the scorer has **no funding vote** and **no exports** | Funding is a pre-filter (TODO 4). The scorer is run as a subprocess, because CONTRIBUTING's import advice doesn't match the file. |

## Proposed additions

| # | Type | Addition | Why it belongs |
|---|---|---|---|
| 1 | `[TODO: DATA SOURCE]` | SOC code per sponsored title (DOL LCA disclosure `SOC_CODE`) joined to the 80 Days CSV | "Sponsored this kind of role" currently rests on matching title text against `top_job_titles_sponsored`. That is a short list of strings, not every petition. With SOC codes the sponsorship vote becomes a record match. |
| 2 | `[TODO: DATA SOURCE]` | A verified company → ATS `careers_url` map for the 80 Days CSV | Slug guessing found a board for 9 of 37 candidates (24%). The other 28 are `check-by-hand`, not "no jobs". |
| 3 | `[TODO: DEV]` | Lever, SmartRecruiters and Workday probes (`scripts/ats/providers/lever.mjs` exists; greenhouse-watch already supports SmartRecruiters) | The largest sponsors in this run (Intel, 13,318 approvals; ServiceNow) were not found on Greenhouse or Ashby by slug. Which ATS they use was not established by this run. |
| 4 | `[TODO: DEV]` | A funding vote in `role-scorer.mjs`, outside this namespace (an engine change for the maintainer) | The assignment's evidence table calls funding a vote, but the scorer has no such term. Here funding is a pre-filter, which is coarser: any funding inside the window counts the same. |
| 5 | `[TODO: DEFINE]` | A fit floor, or a lower Proven p | With Proven p = 0.9, sponsorship alone gives 0.35 × 0.9 = 0.315 ≥ 0.30, the Apply threshold. So a Proven-tier posting is Apply whatever its fit (live run: "Software Engineer, Web Products", fit 0.25, Apply). The human picks the value; this recipe doesn't tune it to change one result. |
| 6 | `[TODO: DATA SOURCE]` | A hiring-lag record (application → offer days) per company size or sector | The timeline gate rests entirely on the persona's 60-day assumption. No repo record measures hiring lag. |
| 7 | `[TODO: DEV]` | Exclusion rules read from the posting **description**, not only its title. For example: "not intended for … new graduate", "U.S. citizenship … required", "security clearance". These are stated phrases in `rules.json`, matched against the posting text (record) | Found at gate G3 on 2026-10-02. Both Consider rows, the Databricks AI Engineer roles, were disqualifying for this persona: one excludes new graduates, the other requires US citizenship and a secret clearance. The title-only seniority rule could not see either (`course/2026fa/submissions/hemanthrayuduu/evidence/20-G3-ai-engineer-requirements.txt`). |

## Phase gates

Each gate stops the run or the item. Liveness and timeline are **gates** (multipliers in the scorer), not votes.

| Gate | Test | Pass | Fail |
|---|---|---|---|
| G0 inputs (machine) | CSV and BLS files exist with their required columns. Persona dates parse. `today ≤ opt_start_date + unemployment_days_allowed`. | run continues | `ERROR:` line, exit 1, no output files (tests: wrong-schema CSV, closed OPT window) |
| G1 liveness (machine, then **human**) | Machine: the posting is in the board API response fetched today, so `liveness.factor = 1.0` (`record`). A board with zero qualifying postings gives `0.0`. A board not fetched gives **no role at all**. Human: open each Apply/Consider URL or run `npm run ats:liveness -- <url>`, and confirm any row marked ⚠ for board identity. | row stays on its list | human moves it to skip; the reason is written in the run log |
| G2 timeline (machine, then **human**) | `timeline.arithmetic` in `pipeline-log.json` uses the student's real OPT start date and a hiring lag they stand behind. Factor = 0 when the margin is ≤ 0. | factor used as computed | student edits `persona.json` and reruns. The old run is kept. |
| G3 release (**human**) | For each Apply / Consider / Network row: does the sponsored-title evidence fit this posting's family, and is the role really entry level? | student acts (tailor / reach out) | student skips it; the reason goes in the run log |
| Sample-run gate (lifecycle) | The named human has read `pipeline-report.md` of a full sample run and the evidence folder, and signed the gate line in `logs/runs/2026fa-hemanthrayuduu-1.md`. | `status: RUNNABLE-SAMPLE`, `last_gate` set | stays `DRAFT` |

## What it can and can't verify

**Can verify, as records:**
- The company appears in the 80 Days CSV with N H-1B approvals and these top sponsored titles.
- Its latest recorded funding date and amount fall inside the window.
- This posting was in the company's live Greenhouse/Ashby board response at fetch time.
- The board's name matches the CSV name (Greenhouse only).
- The national OEWS median and job zone for the SOC shown.
- The scorer's arithmetic for every role, from `role-scores.json`.

**Applies stated rules (your-input), reproducibly:**
- the sponsorship tier and p;
- the title family;
- the US-location, seniority and PhD exclusions;
- fit p (a deterministic phrase-match score ÷ 8);
- the timeline factor;
- the SOC fallback by family.

Changing `rules.json` or `persona.json` changes the result, and the log records the hashes of both.

**Cannot verify:**
- That the company sponsors **this** posting, or will sponsor in the next H-1B cycle. History is not a promise.
- That a company in `check-by-hand` has no openings. Slugs are guesses, and four ATSs aren't probed.
- That an Ashby board belongs to the company. The API returns no company name.
- That a posting is truly entry level. Only the title is read, so "Software Engineer" at a robotics firm may want 3+ years.
- That the student is eligible for the posting at all. Requirements stated only in the description, such as US citizenship, a security clearance, or "not for new graduates", are not read. Gate G3 caught both on 2026-10-02 (TODO 7).
- That the hiring lag is realistic.
- What this employer pays. OEWS is national and occupation-level.
- That the 80 Days CSV is complete or current for any company.

## Workflow

1. Confirm inputs and toolchain:

   ```bash
   test -f data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv && test -f data/bls/compact/soc_occupation_compact.csv && node --version && python3 --version
   ```

2. Offline test (must print `OK`):

   ```bash
   python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v
   ```

3. Live sample run. It writes to `course/2026fa/submissions/hemanthrayuduu/runs/<today>-live/`. Add `--limit 5` for a quick demo, or `--company "NAME"` to check one company:

   ```bash
   python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py
   ```

4. Read `pipeline-report.md`. Then run the G1 spot-check on Apply rows:

   ```bash
   npm run ats:liveness -- <apply-row-url>
   ```

5. Clear G2 and G3 in the run log (template below). Before any `pii-scan`, clear the generated raw cache: `rm -rf course/2026fa/submissions/hemanthrayuduu/runs/*/.build`. It holds company recruiting addresses from the board responses, and its sha256 hashes stay in the log.

## Output contract

**Agent: `pipeline-log.json`.** Every leaf value is `{value, source[, note]}`.

```
_tool, rules_version, generated, today{value,source}, mode [live|offline], command,
inputs{csv,bls,persona,resume,rules: {path, sha256}; scheme; form_d_samples[]},
hosts_contacted[], http_calls, raw_responses{<ats>-<slug>: {path, sha256}},
persona{…your-input}, funding_window_start, timeline{factor, arithmetic, …, source},
funnel{csv_rows … roles_scored, advanced_to_apply_or_consider},
companies[]{company, h1b_*, sponsored_titles, latest_funding_*, form_d_sample, company_tier,
            board{status [found|not-found|fetch-failed|identity-mismatch], ats, slug, identity, attempts[]},
            postings{seen, other_family, non_us, seniority, kept}, bucket},
roles[]{role_id, company, title, sponsorship{p,tier,source,basis}, fit{p,source,basis},
        liveness{factor,source,basis}, timeline{factor,source,basis},
        result{url, location, family, wage_context, fit_lines[], recommendation, composite, reason, bucket}},
buckets{apply[], consider[], network[], check-by-hand[], skip[]},
scorer{command, exit_code, stdout, role_scores_json, skip_share}, pipeline_skip_share, cannot_verify[]
```

**Human: `pipeline-report.md`.** Sections in this order:
1. Executive summary: counts and next actions, in plain language.
2. Apply table.
3. Consider table.
4. Network table.
5. Check-by-hand table.
6. Skipped, with the overall skip share and its denominator.
7. Label legend.
8. What this run could not verify.
9. Gates a person must clear.
10. Run record: command, hosts, funnel, input hashes.

**Scorer output:** `roles.json` (input), plus `role-scores.json` and `role-scores.md`, written by `role-scorer.mjs` itself into the same folder.

Raw board responses go to `.build/raw/`, which is gitignored and hashed in the log.

## Stop conditions, and the next action per result

**Stop and invent nothing when:**
- an input is missing or has the wrong columns;
- the OPT window has already closed;
- `node` is missing or the scorer exits non-zero.

**Also stop when asked to:**
- score a company whose board wasn't fetched;
- relabel a `your-input` value as `record`;
- raise a tier or lower a threshold so one particular role passes;
- call a host outside the two named above.

| Result | Next action (3-3-2 day) |
|---|---|
| **apply** | Tailor an application today (the 2 research-and-apply hours). Use the matched résumé phrases in `fit_lines` as the starting point. |
| **consider** | Tailor only if the Apply list is exhausted. Check first whether the sponsorship record really covers this title. |
| **network** | Ask for an informational conversation with an engineer at the company (the 3 networking hours). Rerun weekly; when a matching posting appears, the company moves to apply. |
| **check by hand** | Find the careers page once (about 2 minutes). If it's on Greenhouse or Ashby under another slug, note it for TODO 2. |
| **skip** | Nothing. Skipping is a success. |

## Lifecycle note

The sample-run gate was cleared on 2026-10-02 by Hemanth Rayudu. The record covers a full sample run, conformance passing, audits read, and G1–G3 decided (`logs/runs/2026fa-hemanthrayuduu-1.md`). So this version claims **RUNNABLE-SAMPLE** and no more: no gated live run beyond the sample, and no VERIFIED attestation.

Version 0.1.2 changed only recipe text after the student signed the sample-run attestation: TODO 7, one "cannot verify" line, this note, and the frontmatter. The code (`e26febd`) and `rules.json` 0.1.1 that were tested are unchanged.

The seven open TODOs are proposals outside the path this version executes. SNICKERDOODLE's DRAFT → SPECIFIED rule counts every open `[TODO]`, while the assignment asks for proposals written as TODOs. That conflict is recorded in the run log rather than resolved silently.

## Run-log template (`logs/runs/`)

```markdown
## YYYY-MM-DD — swe-sponsor-pipeline <live|offline> run

- **Recipe:** manual (recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md v<version>, rules <rules_version>)
- **Inputs:** command; persona path + sha256; CSV/BLS sha256 (from pipeline-log.json); --today; --limit
- **Outputs:** <run folder>/pipeline-report.md, pipeline-log.json, roles.json, role-scores.{json,md}
- **Result:** candidates N · boards found N/N · postings evaluated N · apply N · consider N · network N · check-by-hand N · skip share N%
- **Gate decisions:** G1 <who, date, rows checked, rows removed + why> · G2 <who, date, OPT date and lag confirmed> · G3 <who, date, rows acted on>
- **Open issues:** what did not work or is still missing
```
