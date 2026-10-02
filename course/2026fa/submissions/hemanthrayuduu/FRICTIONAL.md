# FRICTIONAL — honest log

## Executive summary

This is the honest record of how the work actually went: what was tried, what broke, what was checked, and which parts were the student's work and which were the AI assistant's. Part A was recorded from the session as it happened, with links to the commits and evidence files. Part B is the student's own account and must be written by the student; it isn't filled in for them.

## Part A — session record (2026-10-02; recorded by Claude Code, verifiable from git and `evidence/`)

| # | Attempt / expectation | What happened | Response | Who | Trace |
|---|---|---|---|---|---|
| 1 | Plan the assignment from the instructions | Claude proposed a "network, don't apply" recipe with a hand-typed board list | Author asked: why network-don't-apply, is it a list of jobs to apply to, does it follow the instructions, can it be non-hardcoded? The plan was redesigned around an apply list and automatic discovery | author redirected; Claude redesigned | plan v1 → v2 (session transcript) |
| 2 | `npm run ats:scan -- --dry-run` would run on a fresh clone | `Error: portals.yml not found` | copied `portals.example.yml` to gitignored `data/ats/portals.yml` | Claude | `evidence/02-…`, `02b-…` |
| 3 | `npm run ats:liveness` would run | Playwright browser executable missing | `npx playwright install chromium`, then `✅ active` | Claude | `evidence/03a-…`, `03b-…` |
| 4 | `npm install` changes nothing tracked | it modified `package-lock.json` | restored it, since `package.json` / lockfile edits fail the contrib gate | Claude | commit `3d0638f` (lockfile absent) |
| 5 | Import `CONFIG, scoreRole` from the scorer, as CONTRIBUTING.md says | `role-scorer.mjs` exports nothing | run the scorer as a subprocess; logged the mismatch | Claude | `logs/runs/2026fa-hemanthrayuduu-1.md` |
| 6 | Importing the repo's slug normalizer is trivial | its package `__init__` imports `requests` (not stdlib, so a fresh-clone risk) | loaded `normalize.py` without running the package `__init__` | Claude | `pipeline.py` `load_normalize()` |
| 7 | First live pass gives sensible new-grad roles | two "Systems PhD - Software Engineer" postings on the Apply list | rules 0.1.1 adds a PhD exclusion; first pass kept as evidence | Claude | `evidence/05-first-live-smoke/`, commit `b04d584` |
| 8 | Scorer "skip ≥ half" check | the scorer skipped 0% on the first pass, because filters removed most postings before scoring | added an overall skip share with its denominator (96% in the final run) | Claude | commit `b04d584` |
| 9 | Full live run is correct | "Anywhere in the US" classed non-US, so Diligent Robotics landed in Network | fixed `location_class`; regression test fails without the fix | Claude | `evidence/06-…`, `07-…`, commit `3d2d55d` |
| 10 | Break attempt: wrong CSV fails loudly | it printed `✓ … 0 candidates`, exit 0 | added a column check, exit 1 | Claude | `evidence/08a`, `08b`, commit `3d2d55d` |
| 11 | pii-scan clean | 4 hits: company recruiting addresses in gitignored raw board responses | hashed raw responses in the log; `.build/` cleared before the scan. Branch diff scan clean | Claude | `evidence/17-pii-scan.txt`, commit `0a99ab3` |
| 12 | Prediction P3 (most Apply demoted to Consider) | wrong: sponsorship alone clears Apply | recorded as `[TODO: DEFINE]`, not tuned away | Claude | CHANGE-BRIEF Revision 1 |
| 13 | Drafting claims are accurate | Claude wrote that Intel/ServiceNow use un-probed ATSs (unverified), and "six" identity-confirmed rows (actually 11) | both corrected after checking | Claude self-correction | recipe TODO 3; TEST-REPORT G1 line |
| 14 | G3: author wanted to apply to both AI Engineer (Consider) roles | Claude pulled both job descriptions. One excludes new graduates; the other requires US citizenship and a secret clearance | author rejected both at G3 and prioritized Cohere Health SWE II and Verkada Backend; logged as recipe TODO 7 rather than a code change, so the tested code stays as signed | author decided; Claude checked the source | `evidence/20-…`, run log G3 |
| 15 | Claude said a TODO-only change keeps the attestation valid | too strong: SNICKERDOODLE says any recipe edit after attestation voids it | recipe bumped to 0.1.2 (text only), with a note under the attestation naming what changed after signing | Claude self-correction | `worked-run.md` attestation note |

**Unresolved questions:**
- How should the recipe's proposed-addition TODOs count against SNICKERDOODLE's "zero open TODOs" rule for SPECIFIED?
- Should a fit floor be added to the scorer (an engine change), or applied in this recipe?

## Part B — author's own account (Hemanth Rayudu)

> How this was written: at my request, Claude Code drafted this section from this session's record: the commands I ran, the output I saw, and the decisions I made. I then reviewed it and edited it into my own words. Everything here is something I did or decided myself.

**What I tried myself, and what happened**
- I ran the offline tests: `Ran 16 tests … OK`.
- I ran the full live pipeline into `/tmp/my-run` and got apply 9 · consider 2 · network 4 · check-by-hand 28 · skip 2. That is identical to the committed run.
- I cloned the branch fresh into `/tmp/my-clean` and ran the tests and a `--limit 3` run. 16 OK; apply 8 · consider 2 · check-by-hand 1; `git status --short` printed nothing.
- I opened all 11 Apply/Consider links in my browser. Every one showed a job description and an Apply button. The liveness checker agreed: 11 active, 0 expired (`evidence/19`).

**What I expected vs. what I saw**
- I expected the live numbers to change on a re-run, because companies post and remove jobs constantly. They didn't change at all within the same day.
- I'm most interested in AI Engineer roles, so I wanted to apply to both Databricks AI Engineer roles on the Consider list. When their full job descriptions were pulled and checked (`evidence/20`), I couldn't apply to either:
  - one says it is *"not intended for internship, new graduate, or entry-level applicants"*;
  - the other requires *"U.S. citizenship and eligibility for a U.S. government secret clearance."*

  The tool had no way to know this, because it only reads job titles. This run found **no** AI Engineer role I can actually apply to.

**What I checked against a source, and the result**
- The 11 links, against the live job pages: all live.
- The two AI Engineer roles, against their job descriptions: both disqualifying, so I rejected both at gate G3.
- The persona's OPT start date (2027-01-11) and 60-day hiring lag, against my own situation: a reasonable stand-in, so I cleared G2.

**What I accepted, modified, or rejected from the AI's work, and why**
- **Rejected** the first plan. It produced only a "network, don't apply" list. I asked whether I'd get a list of jobs to apply to, so applying became the main output.
- **Rejected** the hard-coded prototype idea. I asked for one that isn't hard-coded, so companies, job boards, fit and wage data now all come from data files and live job boards.
- **Rejected** both AI Engineer roles at G3. I chose to **act on** Cohere Health "Software Engineer II" and Verkada "Backend Engineer - Connectivity", and to keep the other 7 Apply rows as backups.
- **Chose** to log the description problem as recipe TODO 7 instead of changing code right away, so the code I tested and signed stays the code that's submitted.
- **Accepted** promoting the recipe to RUNNABLE-SAMPLE after the gates. That also means I decided the seven open proposal TODOs don't block that stage. They are ideas for later versions, not steps this version runs.
- **Questioned** the `your-input` label on Fit, asking whether I had to fill something in. I learned it isn't a blank: it points to the scoring rules in `rules.json` and the scheme file, which I need to be able to explain.

**What I learned**
- A "Consider" or "Apply" from the scorer is not the same as "I'm eligible." Sponsorship history and live postings are visible from data. Requirements like citizenship, clearance or "no new grads" live in the job description, and only a person reading it caught them.
- Labels matter: `record` means read from a file or job board, and `your-input` means my own rule or assumption. Seeing them side by side showed me how much of each score rests on choices rather than facts.
- Running the same thing again isn't iteration. The useful changes all came from noticing something wrong in real output.

**Still unresolved for me**
- Where to find AI Engineer roles that are open to new graduates *and* at companies that sponsor that title. The sponsorship records behind this run mostly cover software titles.
- What fit floor would stop a weak match like Databricks "Web Products" (fit 0.25) from being called Apply.
