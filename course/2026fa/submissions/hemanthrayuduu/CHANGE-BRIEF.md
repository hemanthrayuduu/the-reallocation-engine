# CHANGE-BRIEF — swe-sponsor-pipeline

## Executive summary

**What this is:** the prediction record, written before any code, for a small tool that helps one kind of student: an international master's student in computer science who graduates in December and hasn't started post-graduation work authorization yet. The tool answers three questions about software and AI engineering jobs:
- Which open jobs are at companies that have sponsored work visas for this kind of title before?
- Which of those companies raised money recently?
- Does the hiring timeline fit before the student's 90-day unemployment clock runs out?

**Why read it:** it says what the tool will reuse, where a person has to sign off, and what we expect to go wrong. It is written before the build so the predictions can be checked against what actually happens.

**What it decides:** each open posting gets one of three outcomes:
- **apply**, meaning tailor an application;
- **network**, meaning the company is a strong sponsor and recently funded but has no matching opening, so reach out instead;
- **skip**.

Companies whose job board can't be found are marked **check by hand**. They are never guessed.

> Authorship note: Claude Code (the drafting agent) drafted this brief from the author's chosen situation. Predictions P1–P3 are Claude's. The author reviews them and adds their own under *Revisions*. Nothing above the Revisions line is rewritten after the build.

---

## Situation (who this is for)

| Field | Value | Label |
|---|---|---|
| Persona | Fictional MS Computer Science student at a Boston university, graduating 2026-12-18 | your-input (fictional, `@example.com`) |
| Visa | F-1. Post-completion OPT not started; assumed EAD start 2027-01-11, so the 90-day unemployment clock begins then | your-input |
| Target roles | Software Engineer, Software Developer, ML/AI Engineer, Backend/Full-stack Engineer, entry level and new-grad level only | your-input |
| Target SOC | 15-1252 Software Developers; postings that map to 15-1221 (AI Engineer, Applied Scientist) are reported with their own SOC | record lookup |
| Constraint | Needs an employer that will sponsor H-1B, for *this kind of title* rather than for any title | your-input |

Why this is specific: a December graduate who hasn't started OPT can apply *now* while no days are burning. But only to postings that are real, at companies whose sponsorship record covers software titles. A data-science or biotech filter would describe someone else.

## Engine layers used

1. **80 Days to Stay.** Sponsorship history and funding from the mapped CSV, with a cross-check against the Form D samples.
2. **Job-Ops.** ATS board discovery and posting liveness.
3. **Cognitive Pivot.** BLS wage, job zone and `cognitive_pivot_score` per SOC, reported as context only (see Fact 1).

## What gets reused (exact paths)

| What | Path |
|---|---|
| Sponsorship and funding records | `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` |
| Form D cross-check (samples only, Fact 3) | `data/sec/form-d/processed/sample/companies-sec-*-d.sample.json` |
| Wage / O*NET context | `data/bls/compact/soc_occupation_compact.csv` |
| Company name → ATS slug | `scripts/ats/scrapers/common/normalize.py` (`normalize_company_name`) |
| Allow-listed board fetch and job normalisation | `.claude/skills/greenhouse-watch/scripts/greenhouse_watch.py` (`board_url`, `fetch_board`, `normalize_jobs`) |
| Deterministic résumé↔posting fit | same file (`resume_features`, `judge`) with `.claude/skills/greenhouse-watch/scheme.default.json` |
| Scoring (not copied) | `scripts/score/role-scorer.mjs`, called as a subprocess with `--out-dir` |
| Human spot-check of liveness | `npm run ats:liveness -- <url>` (`scripts/ats/check-liveness.mjs`) |

**New, inside my namespace only:**
- `scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/` holds the pipeline, the fixtures and an offline test.
- A fictional persona under `search/examples/`.

**Proposed for the repo, typed TODOs in the recipe:**
- `[TODO: DATA SOURCE]` an SOC column in the 80 Days CSV. Without it, "sponsored this kind of role" rests on title text.
- `[TODO: DATA SOURCE]` a verified company→ATS board map. Without it, boards are found by guessing slugs.
- `[TODO: DEV]` a funding vote in the scorer. The assignment calls funding a vote, but `role-scorer.mjs` has no funding term.

## Gates (hard stops a human clears)

| Gate | What the human must see to clear it |
|---|---|
| G1 Liveness | For every posting on the Apply list, the URL opens as a live posting. Spot-check with `npm run ats:liveness`. "Board not found" companies are reviewed by hand and never cleared automatically. |
| G2 Timeline | The OPT start date and hiring-lag assumption in the persona file are the student's own. The computed timeline factor is shown with its arithmetic. |
| G3 Release | Before acting, the student reads the Apply and Network lists. For each one: does the sponsored-title evidence actually match the posting, and is the role really entry level? |

## Predicted failure cases, and how each is checked

| # | Failure | Expected behaviour | Check |
|---|---|---|---|
| F1 | Company not in the CSV, or has no H-1B rows | Excluded with the reason; no sponsorship value invented | Fixture company with approvals = 0 |
| F2 | Slug guess returns 404, or fetch fails | "Check by hand" bucket; never sent to the scorer. The scorer treats a missing gate as open | 404 fixture; assert the company is absent from `roles.json` |
| F3 | OPT date has passed or can't be parsed | Exit non-zero with a message; no timeline value | Fixture persona with a past date |
| F4 | Posting title has no SOC match in BLS | Wage context reads "unmapped", with no number | Fixture posting with an unusual title |
| F5 | No Form D sample match | Labelled "no Form D sample match — funding from 80 Days CSV only" | Expected for almost all companies (only 1 H-1B company overlaps the samples) |
| F6 | Only senior or staff postings exist | Excluded by the persona's seniority rule and counted, so the company may land in Network | Fixture board with only "Senior" titles |

## Predictions about what the first pass gets wrong (kept as written)

- **P1 (Claude).** Slug guessing from legal names will find a board for **fewer than a third** of candidate companies. Many companies use a slug that differs from their legal name, or use an ATS we don't probe (Workday, Lever, iCIMS). So "check by hand" will be the biggest bucket.
- **P2 (Claude).** Title-text matching will both miss and wrongly include roles. For example, "Software Engineer" sponsorships at a hardware or medical-device company will count toward a cloud SWE posting. "Member of Technical Staff" postings will be missed by the title patterns.
- **P3 (Claude).** The scorer will downgrade most Apply results to Consider. The new-grad seniority filter leaves few postings, and companies whose sponsored titles don't match the posting's title family land in a weak tier.

## Revisions

*(Append only. Each revision dated and attributed.)*

### Revision 1 — 2026-10-02, Claude Code (after the build and the live run; predictions above unchanged)

| Prediction | Outcome | Evidence |
|---|---|---|
| P1: boards found for fewer than a third | **Confirmed.** 9 of 37 (24%); 28 in check-by-hand | `evidence/09-final-live-run.txt` |
| P2: title-family matching misfires both ways | **Confirmed.** "Embedded Software Engineer" counts as software; Twin Health's family match rests on one sponsored "Senior Backend Engineer". Not yet seen: a "Member of Technical Staff" miss | `runs/2026-10-02-live/pipeline-report.md` |
| P3: most Apply results demoted to Consider | **Wrong.** 9 Apply vs 2 Consider. With Proven p 0.9, sponsorship alone (0.315) clears the 0.30 Apply threshold, so fit barely matters for strong sponsors | `role-scores.json` traces; recipe `[TODO: DEFINE]` 5 |

Failures that were **not** predicted:
- PhD-only roles reached the Apply list (`evidence/05-first-live-smoke/`).
- "Anywhere in the US" was classed non-US (`evidence/06-…`).
- A wrong-schema CSV produced a successful-looking empty run (`evidence/08a-…`).

All three are fixed and tested. F4 (SOC with no BLS row) happened only in a fixture: the real BLS file has every SOC the run used. Slug changed from the plan's `swe-network-targets` to `swe-sponsor-pipeline` after the author asked for an apply list as the main output.

### Revision 2 — 2026-10-02, author (Hemanth Rayudu), recorded by Claude Code at his direction

**Situation corrected.** The original situation above (December graduate, OPT not started, entry-level) was Claude's framing of an early answer, not the author's real case. The real case:
- pre-completion OPT from mid-October 2026;
- about 3.5 years of experience;
- **mid-level AI Engineer** roles on the **Microsoft AI stack**;
- anywhere in the US, **Texas and remote first**.

Checked against DHS *Study in the States*: the 90-day unemployment limit is stated for post-completion OPT, and OPT is applied for by the student, not sponsored by an employer.

**No new predictions were written down before the iteration-2 runs.** That is an honest gap in this record, not an omission in the summary. The original predictions P1–P3 are scored against iteration 2 below instead.

### Revision 3 — 2026-10-02, Claude Code (after the iteration-2 runs)

| Original prediction | Iteration 2 outcome | Evidence |
|---|---|---|
| P1: boards found for fewer than a third | **Confirmed again:** 10 of 40 (25%) | `evidence/25-…` |
| P2: title-family matching misfires | **Confirmed again:** "Partner Engineer … AI & Apps" and "AI Automation QA Engineer" matched the AI family until excluded by rule | `evidence/23b-…` |
| P3: most Apply results demoted to Consider | Wrong in iteration 1. **In iteration 2 it is true, and more:** nothing reached Apply, and every AI posting was tier Possible | `runs/2026-10-02-live-v2/` |

Not predicted:
- **The first pass found almost nothing.** Only 100 of 1,552 sponsors list an AI title (`23a`).
- **"Can't sponsor" statements are role-specific**, so a company-wide rule drafted on that basis was wrong and was withdrawn (`24a`, `24b`).

### Revision 4 — 2026-10-02, author (Hemanth Rayudu) via Claude Code, with outcome

**Target widened by the author:** "include Senior titles and re-run, include Data Engineer, Data Scientist roles also." No predictions were written down before this run.

**Outcome (iteration 3):**
- consider 7 (was 3), including the first Texas match (Austin).
- 8 Senior postings ruled out by years asked (5+ / 8+).
- 1 Senior Data Scientist reached Consider.
- No Data Engineer postings on the boards found.
- A hand check showed the lowest-bound years rule keeps a role whose main requirement is 5+ years (TODO 9).
