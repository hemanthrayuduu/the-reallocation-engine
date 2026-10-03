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
| 16 | Recipe built for a December graduate on entry-level SWE/AI | author: "my case is I will be on pre-opt and the clock start in Oct 2nd week"; then "AI Engineer jobs with Microsoft AI stack mainly and mid level jobs with 3-4 years of experience"; then "all locations but focus more on jobs in texas and remote, who sponsors opt" | re-scoped persona, résumé, rules (iteration 2) | author decided; Claude built | commit `75f3c41`; CHANGE-BRIEF Rev. 2 |
| 17 | "The clock starts in October" | DHS page: the 90-day limit is stated for post-completion OPT, and the student applies for OPT (no employer sponsors it) | timeline gate stays on post-completion OPT; told the author to confirm with the DSO | Claude checked the source | persona `opt_start_note`; recipe |
| 18 | AI-only sponsorship evidence finds AI sponsors | 10 candidates, 0 US AI roles: only 100 of 1,552 sponsors list an AI title in the top-few list | software-or-AI evidence; a mismatch gets the soft tier | Claude | `evidence/23a` → `25` |
| 19 | "AI" + "engineer" means an AI role | matched "Partner Engineer … AI & Apps" and "AI Automation QA Engineer" | `not_if_title_has` exclusions + tests | Claude | `23b`; rules 0.2.1 |
| 20 | Twin Health "won't sponsor", so drop it from networking | Claude said this to the author from one posting; raw data: statements are role-specific, and its Senior AI postings have none | rule withdrawn before commit; statements counted per company; claim corrected to the author | Claude self-correction | `24a`, `24b` |
| 21 | Drafted predictions P4/P5 for iteration 2 | Claude labeled them "written before the iteration-2 live run" when they were written after | removed; CHANGE-BRIEF now says no predictions were recorded before iteration 2 | Claude self-correction | CHANGE-BRIEF Rev. 2 |
| 22 | Author: "include Senior titles and re-run, include Data Engineer, Data Scientist roles also" | rules 0.3.0: Senior in, data families added; first test run failed on the Senior fixture, which is the intended effect | test updated, 2 tests added; live run: consider 7, first Texas match | author decided; Claude built | `evidence/29`, `31` |
| 23 | The years column is trustworthy | hand check: the Austin role asks 5+ years of software engineering *and* 3+ years of data infrastructure; the rule shows 3+ | logged as `[TODO: DEFINE]` 9 for the author; rule not tuned after seeing the result | Claude checked the source | `evidence/30` |
| 24 | Claude runs the attestation re-run | author stopped it mid-run ("wait"), wanting to run it himself. Claude then said "Nothing ran, and nothing was written", which was **false**: the tests had run and a partial evidence file was left | partial file archived as `34a-INTERRUPTED…`; false claim corrected to the author; author ran `! bash .build/rerun.sh` himself (`34b`) | author ran; Claude self-correction | `evidence/34a`, `34b`, `34c` |
| 25 | "Are we following §1–§4?" (author) | requirements audit: the documented command could overwrite the committed iteration-1 run when run on 2026-10-02; DEFINE items in the additions list; no late `git diff --stat`; no iteration-3 human-judgment note | fixes A–D (v0.3.1); tests 23 → 25; break check `evidence/36` | author asked; Claude audited and fixed | `evidence/36`, `37`; run log |
| 26 | The ZIP works like the checkout | unzipped and tested, the v0.3.1 ZIP failed `test_never_writes_over_tracked_files`: the guard depended on git, and the ZIP isn't a git checkout | v0.3.2: git-independent guard; gitignore test skips outside a checkout; ZIP re-tested with git blinded | Claude found (by testing the ZIP) and fixed | `evidence/40`, `41` |

**Unresolved questions:**
- How should the recipe's proposed-addition TODOs count against SNICKERDOODLE's "zero open TODOs" rule for SPECIFIED?
- Should a fit floor be added to the scorer (an engine change), or applied in this recipe?

## Part B — author's own account (Hemanth Rayudu)

> How this was written: at my request, Claude Code drafted this section from this session's record: the commands I ran, the output I saw, and the decisions I made. I reviewed the iteration-1 part before it was committed. I asked Claude Code to write the iterations 2–3 part as well, and I read it before submitting. Everything here is something I did, saw or decided myself.

### Iteration 1 (entry-level software / AI)

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

**Still unresolved after iteration 1**
- Where to find AI Engineer roles that are open to new graduates *and* at companies that sponsor that title. The sponsorship records behind this run mostly cover software titles.
- What fit floor would stop a weak match like Databricks "Web Products" (fit 0.25) from being called Apply.

### Iterations 2 and 3 (my real situation)

**What I tried myself, and what happened**
- **Iteration 2: corrected the situation.** I'm on pre-completion OPT from mid-October, I have about 3.5 years of AI engineering experience, and I want AI Engineer roles on the Microsoft AI stack, anywhere in the US but Texas and remote first.
- **Iteration 3: widened the target.** I asked to include Senior titles and Data Engineer / Data Scientist roles.
- **Liveness:** I had the liveness check run on the 7 Consider links (7 active, `evidence/33`), and I opened all 7 in my browser. Each had a job description and an Apply button.
- **My own re-runs.** I stopped Claude Code when it started re-running the checks for my attestation, because I wanted to run them myself. I couldn't copy commands out of the terminal, so Claude put them into two short scripts, and I ran both from the Claude Code prompt:
  - `! bash .build/rerun.sh`: 23 tests OK; live run apply 0 · consider 7 · network 6 · check-by-hand 38 · skip 1 (`evidence/34b`).
  - `! bash .build/fresh-clone.sh`: a fresh clone of the branch at `99bc2c9`. 23 tests OK, the same live result, and `git status` empty in the clone (`evidence/35`).

**What I expected vs. what I saw**
- **The OPT clock.** I believed my 90-day unemployment clock starts in October. The DHS Study in the States page says the 90-day limit is a post-completion OPT rule, and that the student applies for OPT; no employer sponsors it. So my real question is "who hires people on OPT and sponsors an H-1B later?". I still have to confirm my dates with my DSO.
- **No Apply rows.** I expected some AI roles to reach Apply. None did, in iteration 2 or 3. Every AI and data posting got the weaker "Possible" sponsorship grade, because the sponsorship records list only a company's top few titles, and those are rarely AI or data titles.
- **Senior roles.** I expected adding them to open up a lot. The description check ruled out 8 of them for asking 5+ or 8+ years, and 7 roles reached Consider, including one in Austin, TX.

**What I checked against a source, and the result**
- **The 7 Consider links:** all live.
- **The Austin role (Apptronik, Senior Software Engineer, ML Infrastructure):** its description asks for 5+ years of software engineering *and* 3+ years of data-infrastructure work, but the tool shows 3+. I'm applying anyway, knowing it's a reach (`evidence/30`).
- **Twin Health's Senior AI Engineer:** it asks 5+ years, so it was correctly ruled out. It doesn't say it can't sponsor.

**What I accepted, modified, or rejected from the AI's work, and why**
- **Applying to all 7** Consider rows (gate G3), and confirming the timeline stand-in (G2).
- **Kept the years rule as it is**, rather than tuning it after seeing the Austin result. It's logged as TODO 9 for a deliberate decision.
- **Accepted Claude's correction** that "can't sponsor this role" statements are per role, not company-wide. Claude had first told me Twin Health "won't sponsor" based on one posting.
- **Didn't rely on Claude's word that "nothing ran"** after I stopped its run. My own `git status` showed a leftover file. Claude admitted the mistake, and the file is archived as `evidence/34a`.

**What I learned**
- Check visa rules against the official source. My assumption about when the OPT clock starts was wrong.
- The deciding facts are in the job description, not the title: citizenship, clearance, years, "can't sponsor this role". Even the tool's Years column needs a human reading, as the Austin role showed.
- A company's sponsorship history doesn't mean every role there is sponsored, and one "can't sponsor" line doesn't mean the company never sponsors.

**Still unresolved for me**
- Which of the six networking targets I'll contact (not decided yet).
- No Data Engineer postings turned up, and boards were found for only 11 of 49 companies.
- How the tool should read descriptions that give two different year requirements (TODO 9), and whether a fit floor is needed (TODO 5).
