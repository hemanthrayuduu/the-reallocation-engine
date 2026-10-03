# Design: v0.4.0 hardening — years rule v2, honest fit scale, per-posting audit and verification loop

## Executive summary

**What this is:** the agreed design for the last round of improvements to the job-list tool before submission, written down before any code changes.

**Why read it:** it fixes what "correct output" means for this project, what will change, what deliberately won't, and how each change gets verified.

**What it decides:** four things:
1. Read years of experience from job descriptions more carefully (required vs preferred lines, "or" alternatives).
2. Stop the résumé-fit score from saturating.
3. Write a full per-posting audit with every run, and check a fixed sample by hand each iteration until it shows zero misclassifications.
4. Correct a wrong claim about the Austin role in every document.

Bigger ideas (the book's sponsorship formula, more job boards, staleness signals) are recorded as next steps, not built tonight.

## Shared understanding (agreed 2026-10-03)

**The author said:**
- Improve the whole submission after understanding the repo, the assignment and their own situation.
- Iterate until the output is correct.
- The success criterion is **verified accuracy**: every listed role is really open, at the right level, and one the student is eligible for, with honest labels. A short list is fine.
- The deadline is **tonight, Saturday 2026-10-03, 11:59 pm**.
- Of three approaches, the author chose **C (minimal hardening)**.

**Constraints (assignment and repo):**
- Status no higher than RUNNABLE-SAMPLE; honest record / your-input labels.
- No weakening a rule so a role passes; only named hosts; the scorer unchanged; only the five assigned paths.
- The real résumé is used **only** in `private/`.
- Every code change needs the author's own re-run and re-signed attestation.

## In scope

| # | Change | Where |
|---|---|---|
| 1 | Years rule v2 | `pipeline.py` (`description_check`, new `years_requirement`), tests, fixtures |
| 2 | Fit divided by the scheme's own maximum | `pipeline.py` (fit p), `rules.json` (`fit.full_score: "scheme_max"`), tests |
| 3 | Per-posting audit + verification sample | `pipeline.py` (audit rows; `pipeline-audit.md`), tests |
| 4 | Verification loop | `evidence/verify-iteration-N.md` per iteration; fixes logged in the `rules.json` changelog |
| 5 | Austin "5+ OR 3+" correction | worked run, card, recipe, run log, TEST-REPORT, CHANGE-BRIEF, FRICTIONAL |
| 6 | Documents for 0.4.0 | recipe, card, README, SUBMISSION, TEST-REPORT, run log, worked run, FRICTIONAL, SOURCES |
| 7 | Sign-off and ZIP | author re-run and fresh clone; G1–G3; RUNNABLE-SAMPLE; ZIP rebuilt and tested outside git; push to the fork only (no PR) |
| 8 | Private run (optional) | real résumé, `private/runs/` only, never committed |

## Out of scope (recorded as next steps with evidence)

- **The Chapter 7 sponsorship composite and tiers** (Proven / Likely / Unknown / Avoid). Logged as a `[TODO: DEV]`; the off-book "Possible" tier stays, with a note.
- **More job boards** (SmartRecruiters, Lever, first-word slugs). Logged as a `[TODO: DEV]`, with the probe evidence (11 of 38 found, identity risks).
- **The Chapter 8 staleness signal and the Chapter 10 per-role timeline.** Logged as TODOs.

## 1. Years rule v2

**Input:** the posting description HTML (Greenhouse `content`, Ashby `descriptionHtml`).

**Steps:**
1. **Lines.** Split the HTML into text lines at block boundaries (`p`, `li`, `br`, `div`, `h1`–`h6`, `tr`, `ul`, `ol`), unescaping entities. Each line remembers whether it came from a list item (`<li>`).
2. **Section headings.** A line starts a section only if it is **not a list item**, is 60 characters or fewer, contains **no digits**, does not end in a period, and matches a heading keyword. (Self-review fix: a short bullet such as "Experience with Kubernetes" inside a preferred list must not be mistaken for a required heading.)
   - `preferred` section: /prefer|nice[- ]to[- ]have|bonus|\bplus\b|ideal|desired/i;
   - `required` section: /qualif|require|what you|you have|you bring|you'll need|must|basic|minimum|experience|about you/i.
   - Lines before any heading count as `required`.
3. **Year mentions per line.** Each match of the existing pattern (`N`, `N+`, `N-M`, `N to M` "years" followed within 60 characters by "experience") gives its lower bound N.
4. **Line value.**
   - If the text between any two consecutive mentions contains the word "or" (`\bor\b`, case-insensitive, so "and/or" counts), the value is the **min** (alternatives).
   - Otherwise it is the **max** (all apply).
5. **Requirement.**
   - `years_required` = max of line values over `required` lines, or `null` if there are none.
   - `years_preferred` = max over `preferred` lines, or `null`.
6. **Decision (unchanged):** rule out when `years_required > experience_years + tolerance_years`.
7. **Evidence kept:** `years_lines = [{section, text, value}]`, so every reading can be checked by hand.

**Labels:** the description text is `record`; the rule is `your-input`.

**Tests (fictional fixtures):**
- required "4+ … and 1+ …" gives 4;
- "5+ … or 3+ …" gives 3;
- preferred-only "4+" gives required null and preferred 4;
- no headings, "3+" gives 3;
- "founded 10+ years ago" gives nothing;
- required "6+" is ruled out at experience 3.5;
- the existing years tests stay green.

## 2. Fit on the scheme's own scale

- `fit p = scheme score / scheme_max`, where `scheme_max = w.title + max_skill_hits × w.skill + w.skill_any + w.degree + max(w.location, 0)`. That is computed from `scheme.json` (12.0 today), not typed in.
- `rules.json`: `fit.full_score` becomes `"scheme_max"`; a number is still accepted for older runs.
- **Test:** p equals score / 12 for a fixture posting, and is capped at 1.

## 3. Per-posting audit and verification sample

**Rows.**
- Each **target-family** posting on a found board gets one row: `company, ats:slug, id, title, location, location_class, decision, reason, evidence`.
  - Decisions: `kept:<bucket>`, `non-us`, `wrong-level`, `ruled-out:experience`, `ruled-out:eligibility`, `ruled-out:no-sponsorship`.
  - Evidence: the matched seniority pattern, the years lines, and the matched phrase with 60 characters of context.
- **Other-family** postings are counted per board. Their titles and URLs are listed in the JSON only (`other_family_postings[]` per company); the verification sample draws boundary titles from that list.

**Outputs.**
- `pipeline-log.json` gains `postings_audit[]` and `verification_sample[]`.
- `pipeline-audit.md` (P9 executive summary) gives counts per decision, then every row, then the verification sample.

**Sample rule (deterministic).**
1. Every `kept` row.
2. The first 3 rows (by company, then title) of each other decision.
3. The first 5 other-family postings (by company, then title) whose title matches /engineer|scientist|data|\bai\b|\bml\b|machine learning|analytics/i.

**Tests:**
- every target-family fixture posting appears once in the audit with the right decision;
- the sample contains every kept row;
- the sample is the same on two runs.

## 4. Verification loop (iterate until correct)

Per iteration *N*:
1. Live run with the committed persona.
2. For each sampled row, Claude Code reads the live description (named hosts only) and records `correct` or `misclassified + why` in `evidence/verify-iteration-N.md`, labeled *checked by Claude Code*.
3. If any row is misclassified, change the responsible rule only on a principled ground. Write a changelog line in `rules.json`, re-run, and take a new sample.
4. **Exit when a sample has 0 misclassifications.** The author confirms the kept rows at G3.

**Stated limit:** zero errors in the sample is not proof of zero errors overall.

## 5–7. Corrections, documents, sign-off

As in the scope table.
- Open decision 9 ("which years number counts") **closes**: the rule in §1 is the author's decision (approved 2026-10-03), so `todos_open` goes from 8 to 7.
- The Austin G3 decision (apply) stands. The "reach" wording is corrected and attributed to Claude's misreading.

## Predictions (written before implementation; kept as written)

- **P6:** years v2 flips **no** keep/exclude decision on today's live data. It changes the displayed years for Verkada "Senior Software Engineer – Computer Vision" (1+ → 4+) and Databricks "Senior Applied ML Engineer – ML4Sys" (4+ → preferred only).
- **P7:** the fit fix lowers fit values, and at least one Consider row may become Skip.
- **P8:** the first verification sample will find at least one misclassification in the *other-family* boundary titles, i.e. a real AI or data role the title rule misses.

## Done when

- Tests pass offline, including the new ones; conformance, verify, doctor and pii-scan `--diff main` pass.
- The last verification iteration records 0 misclassifications in its sample.
- Every document reflects 0.4.0, and the Austin wording is corrected everywhere.
- The author has re-run (working copy and fresh clone) and signed; G1–G3 are re-cleared; status is RUNNABLE-SAMPLE.
- The ZIP is rebuilt from the final commit and its tests pass outside git; the branch is pushed to the fork; no PR.

## Risks

- **Heading detection misses unusual headings.** Mitigation: the evidence lines are shown for every reading; fallback to `required`.
- **Time.** Mitigation: the scope is fixed to this list; anything else becomes a TODO.
