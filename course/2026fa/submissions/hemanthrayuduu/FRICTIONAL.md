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

## Part B — author's own account (write this yourself)

*Fill in each item from your own experience. Credit comes from honest, specific entries, not length.*

- **What I tried myself, and what happened:** (e.g. re-running the tests and the live run; opening Apply links for gate G1)
- **What I expected vs. what I saw:**
- **What I checked against a source, and the result:**
- **What I accepted, modified, or rejected from the AI's drafts, and why:**
- **What I learned:**
- **Still unresolved for me:**
