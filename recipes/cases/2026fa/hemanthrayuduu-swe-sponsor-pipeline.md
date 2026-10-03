---
status: RUNNABLE-SAMPLE  # DRAFT | SPECIFIED | RUNNABLE-SAMPLE | RUNNABLE-LIVE. v0.3.0 sample-run gate cleared by a named human (run log, iteration 3). See "Lifecycle note".
todos_open: 8
last_gate: "sample-run, 2026-10-02, Hemanth Rayudu, logs/runs/2026fa-hemanthrayuduu-1.md (iteration 3, v0.3.0; G1–G3 cleared)"
attestation: null  # set only at VERIFIED; sample-run attestations are in course/2026fa/submissions/hemanthrayuduu/worked-run.md
recipe_version: 0.3.0  # 0.2.x: author re-scoped to AI Engineer (Microsoft AI stack), description rules, location preference; 0.3.0: Senior titles + Data Scientist / Data Engineer roles
---

# swe-sponsor-pipeline — AI Engineer, Data Scientist and Data Engineer postings at sponsoring, recently funded companies

## Executive summary

**What it does:** it is built for an international MS Computer Science student on **pre-completion OPT** (from mid-October 2026) with about **3.5 years** of AI engineering experience. The student is looking for **mid-level and senior AI Engineer, Data Scientist and Data Engineer roles**, ideally on the Microsoft AI and data stack: anywhere in the US, with **Texas and remote first**. The recipe finds open postings at companies that, by public record, have sponsored H-1B visas for software or AI titles and raised money recently. It also reads each job description for things that would rule the student out: US citizenship, a security clearance, "can't sponsor this role", or too many years asked. It labels every piece of evidence, then stops, and the student decides.

**Who it's for:** that student, deciding where to spend the two research-and-apply hours of the day before post-completion OPT starts the 90-day unemployment clock.

**What it decides:** each result gets a next action:
- **apply:** tailor an application;
- **consider:** apply if time allows;
- **network:** a strong, recently funded sponsor with no matching opening today, so ask for an informational conversation;
- **check by hand:** the job board wasn't found automatically, which is not the same as having no jobs;
- **skip.**

It never applies, never emails, and never treats a guess as a record.

**Handoff condition (done when):**
- `pipeline.py` exits 0 and writes both `pipeline-log.json` and `pipeline-report.md`.
- Every value carries `record` or `your-input`, and `model-judgment` never appears.
- Every company with no fetched board is in `check-by-hand` and absent from `roles.json`.
- Every posting ruled out by its description is listed with the phrase or years found, and absent from `roles.json`.
- The scorer's own `role-scores.json` exists, with its `_scorer` field.
- The overall skip share is shown with its denominator.

## Required reads

1. `SNICKERDOODLE.md`: gates, provenance, labels.
2. `DOMAIN.md`: layout, known gaps.
3. `data/80-days-to-stay/README.md`: the mapped CSV.
4. `scripts/score/role-scorer.mjs`: the CONFIG block (votes, gates, thresholds).
5. `.claude/skills/greenhouse-watch/SKILL.md`: the allow-listed fetcher and fit scheme reused here.
6. This recipe and its card, `recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.card.md`.

## Purpose and source inventory

| Evidence | Engine layer | Source (exact path or host) | Label | Role in decision |
|---|---|---|---|---|
| H-1B approvals, denials, rate, top sponsored titles | 80 Days to Stay | `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` (30,369 rows; 1,552 with approvals) | record | candidate filter + sponsorship **vote** |
| Latest funding date / amount / stage | 80 Days to Stay | same CSV | record | candidate filter (the scorer has no funding vote; TODO 4) |
| Form D cross-check | 80 Days to Stay | `data/sec/form-d/processed/sample/companies-sec-*-d.sample.json` (4 files × 50) | record | reported only |
| Live postings and their descriptions | Job-Ops | `boards-api.greenhouse.io`, `api.ashbyhq.com` via `.claude/skills/greenhouse-watch/scripts/greenhouse_watch.py` (`board_url`, `fetch_board`, `normalize_jobs`) | record | liveness **gate**; description rules |
| Company → slug | Job-Ops | `scripts/ats/scrapers/common/normalize.py` (`normalize_company_name`) | rule | discovery |
| Fit | (résumé) | `judge()` in `greenhouse_watch.py` with `scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/scheme.json` (the greenhouse-watch default with location weights 0), against `search/examples/kiran-rao/resume.example.json` | your-input (deterministic) | fit **vote** |
| Microsoft AI stack terms, years asked, can't-sponsor statements | Job-Ops | posting text, matched by `rules.json` `microsoft_ai_stack_terms` / `description_rules` | record (rule: your-input) | context; rule-outs |
| Wage, job zone, cognitive pivot score | Cognitive Pivot | `data/bls/compact/soc_occupation_compact.csv` | record (SOC mapping: record or your-input) | context only (Fact 1) |
| Situation: OPT dates, years, target and evidence families, preferred locations, hiring lag, funding window | — | `search/examples/kiran-rao/persona.json` | your-input | timeline **gate**, filters, sort |
| Thresholds, patterns, tier p-values | — | `scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/rules.json` (v0.3.0) | your-input | all rules |
| Decision | engine | `scripts/score/role-scorer.mjs`, as a subprocess with `--out-dir`, never copied | record of arithmetic | Apply / Consider / Skip |

**Prototype command** (repo root; Python 3.9+ stdlib, Node 20+):

```bash
python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py
```

**Test** (offline, fixtures only; any network call fails it):

```bash
python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v
```

**Visa timing, from the record and not from memory:** DHS *Study in the States*, F-1 OPT page, checked 2026-10-02.
- *"A student on post-completion OPT can be unemployed for a total of 90 days."* The page does not apply that limit to pre-completion OPT.
- *"It is the student who must apply for the work permit with USCIS"*. No employer sponsors OPT itself.
- So the timeline gate counts from the persona's **post-completion** OPT start. The question "who sponsors OPT" becomes "who hires on OPT and will sponsor H-1B later", which is exactly what the H-1B record measures. Pre-completion OPT time reduces the 12 months left after graduation, so the student should confirm with their DSO.

**How the engine's known gaps are handled:**

| Fact | Handling here |
|---|---|
| 1. `role_quality` weight is 0.0 `[VERIFY]` | Wage, job zone and `cognitive_pivot_score` are shown beside each posting, **not** sent to the scorer. No weight is proposed: all target postings map to 15-1221.00 or 15-1252.00, and a weight with no calibration set would invent a number. |
| 2. `bls:local-wage` feeds nothing | Not used. The wage is the national OEWS median, labeled as such. |
| 3. Only Form D samples ship | 196 sample companies. In the live runs only Databricks matched. Every miss is labeled "no Form D sample match". |
| 4. Planned directories don't exist | Gates write to `course/2026fa/submissions/hemanthrayuduu/` and `logs/runs/` only. |
| 5. `snickerdoodle` CLI is roadmap | Not used. |
| 7 and 8. local-wage `.venv`; H-1B join validator | Not used. Only the shipped CSV and samples are read. |
| Found: **a missing gate defaults to open (1.0)** | Unfetched boards are never written to `roles.json`; they go to `check-by-hand` (tested). |
| Found: **no funding vote, no exports** in the scorer | Funding is a pre-filter (TODO 4). The scorer is run as a subprocess. |
| Found: **the CSV keeps only a company's top few sponsored titles** | Only 100 of 1,552 sponsors list an AI/ML title. So software **or** AI sponsorship counts as evidence (persona `sponsorship_evidence_families`). An AI posting at a software-only sponsor gets the soft tier **Possible**, which can reach Consider but never Apply. |

## Proposed additions

| # | Type | Addition | Why it belongs |
|---|---|---|---|
| 1 | `[TODO: DATA SOURCE]` | SOC code per sponsored petition (DOL LCA disclosure `SOC_CODE`) joined to the 80 Days CSV | "Sponsored this kind of role" rests on a top-few title list. In iteration 2, every Consider row was tier Possible for that reason alone. |
| 2 | `[TODO: DATA SOURCE]` | Verified company → ATS `careers_url` map | Slug guessing found 10 of 40 boards; 30 are `check-by-hand`. |
| 3 | `[TODO: DEV]` | Lever, SmartRecruiters, Workday probes (`scripts/ats/providers/lever.mjs` exists; greenhouse-watch supports SmartRecruiters) | The largest sponsors (Intel, ServiceNow) were not found on Greenhouse/Ashby by slug. Their ATS was not established. |
| 4 | `[TODO: DEV]` | A funding vote in `role-scorer.mjs` (engine change, outside this namespace) | The assignment calls funding a vote; the scorer has none. |
| 5 | `[TODO: DEFINE]` | A fit floor, or a lower Proven p | Proven p 0.9 × 0.35 = 0.315 ≥ 0.30, so a Proven posting is Apply at any fit (iteration 1: fit 0.25 → Apply). |
| 6 | `[TODO: DATA SOURCE]` | Hiring-lag record (application → offer) | The timeline gate rests on the persona's 60-day assumption. |
| 7 | ~~`[TODO: DEV]`~~ **closed 2026-10-02** | Description rules: eligibility phrases, can't-sponsor phrases, years of experience | Closed by code (`description_check`, `no_sponsorship_phrase` in `pipeline.py`) + tests (`test_TODO7_…`, `test_years_parse_…`, break check `evidence/22-…`) + handoff met: in the iteration-2 live run the Federal Focus role was ruled out automatically (`evidence/25-…`). |
| 8 | `[TODO: DATA SOURCE]` | E-Verify participation per employer | For a later STEM OPT extension the employer must use E-Verify (to be confirmed with the DSO; not confirmed on the DHS page read here). No repo data has it. |
| 9 | `[TODO: DEFINE]` | Which number counts when a description gives several year requirements | The rule takes the **lowest** (lenient). The iteration-3 hand check found Apptronik's Austin role asks "5+ years of professional software engineering experience" *and* "3+ years … owning data and evaluation infrastructure", so it was kept at 3+ although its main requirement is 5+ (`evidence/30-…`). Lowest, highest, or first-stated is a human choice; it isn't changed here after seeing one result. |

## Phase gates

Liveness and timeline are **gates** (multipliers in the scorer), not votes.

| Gate | Test | Pass | Fail |
|---|---|---|---|
| G0 inputs (machine) | CSV/BLS present with required columns; persona dates parse; target and evidence families exist in `rules.json`; `today ≤ opt_start_date + unemployment_days_allowed` | run continues | `ERROR:` line, exit 1, no output (tests: wrong-schema CSV, closed OPT window) |
| G1 liveness (machine, then **human**) | Machine: posting present in today's board response → `liveness.factor 1.0` (record). Board with no qualifying posting → `0.0`. Board not fetched → no role. Human: open each Apply/Consider URL or run `npm run ats:liveness -- <url>`. | row stays | human moves it to skip; reason in the run log |
| G2 timeline (machine, then **human**) | `timeline.arithmetic` uses the student's post-completion OPT start and a hiring lag they stand behind | factor used | student edits `persona.json` and reruns; the old run is kept |
| G3 release (**human**) | For each Apply / Consider / Network row, read the description. Does the sponsored-title evidence fit? Do the level and years fit? Is there an eligibility clause the phrase list missed? Check the "can't sponsor" counts per company. | student acts | skip; reason in the run log |
| Sample-run gate (lifecycle) | Named human read `pipeline-report.md` and the evidence of a full sample run of **this version**, and signed `logs/runs/2026fa-hemanthrayuduu-1.md` | `RUNNABLE-SAMPLE` | stays `DRAFT` |

## What it can and can't verify

**Can verify, as records:**
- N H-1B approvals and these top sponsored titles for the company.
- Latest recorded funding date and amount.
- The posting was on the live board at fetch time; the Greenhouse board name matches the company.
- The phrases and years found in the description.
- The Microsoft AI stack terms found in the posting text.
- National OEWS median and job zone.
- The scorer's arithmetic.

**Applies stated rules (your-input), reproducibly:**
- title family (including the role-word + AI-word rule and its exclusions);
- sponsorship tier and p;
- US location;
- seniority (Staff / Principal / Lead and above, interns and PhD titles excluded; Senior included since 0.3.0);
- description rule-outs;
- fit p (phrase-match score ÷ 8, location weight 0);
- timeline factor;
- Texas / remote preference (sort and ★ only);
- SOC fallback.

The log records hashes of `rules.json`, `persona.json`, the résumé and the scheme.

**Cannot verify:**
- That the company will sponsor **this** posting or next year's cycle. Iteration 2 showed live postings saying *"unable to sponsor … for this role, at this time"* at companies with H-1B history (Verkada: 156 of 307 postings; Twin Health: 23 of 39). The statements are role-specific, so they rule out the posting that carries them, never the whole company.
- That a `check-by-hand` company has no openings.
- That an Ashby board belongs to the company.
- That the student is eligible when a requirement is worded differently from the phrase list.
- The real level of a role whose description states no years, or states several (the lowest is used; TODO 9).
- That a posting genuinely uses the Microsoft AI stack. The column is a word match; "Azure" alone may just mean the company's cloud.
- That the hiring lag is realistic. What the employer pays.

## Workflow

1. Confirm inputs and toolchain:

   ```bash
   test -f data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv && test -f data/bls/compact/soc_occupation_compact.csv && node --version && python3 --version
   ```

2. Offline test (must print `OK`):

   ```bash
   python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v
   ```

3. Live sample run. Use `--out-dir` to keep earlier runs, `--limit 5` for a demo, or `--company "NAME"` to check one company:

   ```bash
   python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py --out-dir course/2026fa/submissions/hemanthrayuduu/runs/<date>-live-v2
   ```

4. Read `pipeline-report.md`, then run the G1 spot-check:

   ```bash
   npm run ats:liveness -- <apply-or-consider-url>
   ```

5. Clear G2 and G3 in the run log. Before any `pii-scan`, run `rm -rf course/2026fa/submissions/hemanthrayuduu/runs/*/.build`. The raw responses carry company recruiting addresses, and their sha256 hashes stay in the log.

## Output contract

**Agent: `pipeline-log.json`.** Every leaf is `{value, source[, note]}`.

```
_tool, rules_version, generated, today, mode, command,
inputs{csv,bls,persona,resume,rules: {path, sha256}; scheme; form_d_samples[]},
hosts_contacted[], http_calls, raw_responses{<ats>-<slug>: {path, sha256}},
persona{summary, target_families, experience_years, preferred_locations, visa, …}, funding_window_start,
timeline{factor, arithmetic, …},
funnel{csv_rows, with_approvals, target_family_sponsored, funded_in_window, candidates, probed, board_*,
       postings_seen, postings_target_family, postings_us, postings_level_ok,
       postings_ruled_out_by_description, postings_kept, roles_scored, advanced_to_apply_or_consider},
companies[]{company, h1b_*, sponsored_titles, sponsored_families, latest_funding_*, form_d_sample, company_tier,
            board{status, ats, slug, identity, attempts[]}, postings{seen, other_family, non_us, seniority, description, kept},
            ruled_out_by_description[]{title, url, reason, years_mentions}, no_sponsorship_statements[]{title, url, phrase}, bucket},
roles[]{role_id, company, title, sponsorship, fit, liveness, timeline,
        result{url, location, preferred_location, family, years_required, microsoft_ai_stack_terms,
               wage_context, fit_lines[], recommendation, composite, reason, bucket}},
buckets{apply, consider, network, check-by-hand, skip}, scorer{…}, pipeline_skip_share, cannot_verify[]
```

**Human: `pipeline-report.md`.** Sections in this order:
1. Executive summary (from the persona's own `summary`).
2. Apply table: ★ preferred-location rows first; columns for score, sponsorship, fit, years asked, stack terms, wage.
3. Consider table.
4. Network table, with each company's count of postings saying "can't sponsor this role".
5. Check by hand.
6. "Can't sponsor this role" statements on live boards.
7. Ruled out by the job description.
8. Skipped, with skip share and denominator.
9. Label legend.
10. Could not verify.
11. Gates.
12. Run record.

**Scorer output:** `roles.json` in; `role-scores.json` and `role-scores.md` written by `role-scorer.mjs`.

## Stop conditions, and the next action per result

**Stop and invent nothing when:**
- an input is missing or has the wrong columns;
- a persona family isn't in `rules.json`;
- the OPT window has closed;
- `node` is missing or the scorer fails.

**Refuse to:**
- score an unfetched board;
- relabel a `your-input` value as `record`;
- raise a tier or drop a rule so one role passes;
- call a host other than the two named;
- treat a role-specific "can't sponsor" statement as the company's policy.

| Result | Next action (3-3-2 day) |
|---|---|
| **apply** | Tailor today (the 2 research-and-apply hours). Start from `fit_lines` and the stack terms found. |
| **consider** | Tailor if Apply is empty, which it was in iteration 2. Read the description first: why is sponsorship only "Possible"? |
| **network** | Informational conversation with an engineer there (the 3 networking hours). Check that company's "can't sponsor" count first. Rerun weekly. |
| **check by hand** | Find the careers page once (about 2 minutes). Note the slug for TODO 2. |
| **skip** | Nothing. Skipping is a success. |

## Lifecycle note

- **v0.1.2** reached RUNNABLE-SAMPLE on 2026-10-02. Hemanth Rayudu cleared G1–G3 and the sample-run gate (run log, iteration 1).
- **v0.2.1** changed code (`75f3c41`), `rules.json` and the persona after the author re-scoped the situation.
- **v0.3.0** changed only `rules.json` (Senior titles in; data_science and data_engineering families; Microsoft data-stack terms) and the persona's target families. The code is still `75f3c41`.
- A gate cleared for one version does not carry over (P4), so v0.3.0 had its own gates. Hemanth Rayudu cleared G1–G3 and the sample-run gate for v0.3.0 on 2026-10-02, so this version claims **RUNNABLE-SAMPLE** and no more: no gated live run beyond the sample, and no VERIFIED attestation.
- The seven open TODOs are proposals outside the executed path. SNICKERDOODLE's zero-open-TODO rule for SPECIFIED conflicts with the assignment's request to list proposals as TODOs. The author's decision on that conflict is recorded in the run log.

## Run-log template (`logs/runs/`)

```markdown
## YYYY-MM-DD — swe-sponsor-pipeline <live|offline> run (iteration N)

- **Recipe:** manual (recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md v<version>, rules <rules_version>, code <commit>)
- **Inputs:** command; persona path + sha256; CSV/BLS sha256 (from pipeline-log.json); --today; --limit
- **Outputs:** <run folder>/pipeline-report.md, pipeline-log.json, roles.json, role-scores.{json,md}
- **Result:** candidates N · boards N/N · postings evaluated N · ruled out by description N · apply N · consider N · network N · check-by-hand N · skip share N%
- **Gate decisions:** G1 <who, date, rows checked/removed> · G2 <who, date> · G3 <who, date, rows acted on / rejected + why>
- **Open issues:** …
```
