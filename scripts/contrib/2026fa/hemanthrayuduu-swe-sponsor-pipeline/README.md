---
owner: hemanthrayuduu
term: 2026fa
component: swe-sponsor-pipeline
status: DRAFT  # mirrors the recipe: v0.3.2 (git-independent output guard) awaits the author's re-run
promoted_to: null
---

# swe-sponsor-pipeline

## Executive summary

**What this is:** a small program for an international master's student in computer science on pre-completion OPT, with about 3.5 years of AI engineering experience, who wants **mid-level and senior AI Engineer, Data Scientist and Data Engineer roles**, ideally on the Microsoft AI and data stack: anywhere in the US, Texas and remote first. It starts from public records of which companies sponsored visas and raised money recently. It then checks those companies' live job boards, reading each job description for anything that rules the student out: US citizenship, a clearance, "can't sponsor this role", or too many years asked.

**Why use it:** doing this research by hand takes hours per company. This produces a sourced, labeled list in minutes.

**What it decides:** nothing final. It sorts the results into lists:
- **apply** / **consider** (tailor an application);
- **network** (strong sponsor, recently funded, but no matching opening, so reach out instead);
- **check by hand** (its job board couldn't be found automatically);
- **skip**.

The student reviews every list before acting.

## Run it (one command, from the repo root)

```bash
python3 scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/pipeline.py
```

- **Needs:** Python 3.9+ (standard library only) and Node 20+ (for the engine's scorer). No `pip install` is needed.
- **Network:** live mode calls only `boards-api.greenhouse.io` and `api.ashbyhq.com`, through greenhouse-watch's allow-listed fetcher, with no redirects.
- **Output:** `scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline/.build/runs/<today>-live/`. That folder is inside this one and gitignored, so a run never writes over a tracked file. `--out-dir` changes it. The run refuses any existing folder holding files it did not write, and, in a git checkout, any folder holding tracked files.
- **Test** (offline, fixtures only; any network call fails it):

```bash
python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v
```

**Useful flags:**

| Flag | Effect |
|---|---|
| `--limit N` | probe only the N candidates with the most approvals (a quick demo) |
| `--company "NAME"` | check one company. If it isn't in the CSV, the run says so and scores nothing |
| `--offline DIR` | read board fixtures `DIR/<ats>-<slug>.json` instead of the network |
| `--today YYYY-MM-DD` | fix the run date (recorded in the log) |
| `--persona`, `--rules`, `--csv`, `--bls`, `--formd` | swap inputs |

## What it reads

| Input | Path | Label |
|---|---|---|
| H-1B approvals, sponsored titles, funding | `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` | record |
| Form D cross-check (samples only) | `data/sec/form-d/processed/sample/*.sample.json` | record |
| Wage, job zone, cognitive pivot score | `data/bls/compact/soc_occupation_compact.csv` | record |
| Live postings | Greenhouse / Ashby board APIs | record |
| Persona and résumé (fictional; the tests use `fixtures/persona.fixture.json` instead) | `search/examples/kiran-rao/` | your-input |
| Thresholds, patterns, tier p-values, description rules, stack terms | `rules.json` (this folder, v0.3.0) | your-input |
| Fit scheme (greenhouse-watch default, location weights 0) | `scheme.json` (this folder) | your-input |

**Reused code (not copied):**
- `normalize_company_name` from `scripts/ats/scrapers/common/normalize.py`;
- `board_url`, `fetch_board`, `normalize_jobs`, `resume_features`, `judge` and `strip_html` from `.claude/skills/greenhouse-watch/scripts/greenhouse_watch.py`;
- the scorer `scripts/score/role-scorer.mjs`, run as a subprocess with `--out-dir`.

## What it writes (into the output folder only)

| File | For |
|---|---|
| `pipeline-log.json` | the agent: every value as `{value, source}`, input hashes, funnel, buckets |
| `pipeline-report.md` | the person: executive summary, apply / consider / network / check-by-hand tables, gates |
| `roles.json` | the scorer's input (shape of `data/examples/ch11-roles.json`) |
| `role-scores.json`, `role-scores.md` | written by `role-scorer.mjs` itself |
| `.build/raw/*.json` | raw board responses (gitignored), for provenance |

Recipe: `recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.md` · Card: `recipes/cases/2026fa/hemanthrayuduu-swe-sponsor-pipeline.card.md`.
