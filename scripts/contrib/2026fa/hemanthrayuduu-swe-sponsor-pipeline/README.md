---
owner: hemanthrayuduu
term: 2026fa
component: swe-sponsor-pipeline
status: DRAFT  # mirrors the recipe; becomes RUNNABLE-SAMPLE when the named human clears the sample-run gate
promoted_to: null
---

# swe-sponsor-pipeline

## Executive summary

**What this is:** a small program for a master's student in computer science who graduates in December, hasn't started post-graduation work authorization, and needs a visa-sponsoring employer. It starts from public records of which companies sponsored visas for software and machine-learning titles and which of them raised money recently. It then checks those companies' live job boards for entry-level US software and AI engineering openings.

**Why use it:** doing this research by hand takes hours per company. This produces a sourced, labeled list in minutes.

**What it decides:** nothing final. It sorts the results into four lists:
- **apply** (tailor an application);
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
- **Output:** `course/2026fa/submissions/hemanthrayuduu/runs/<today>-live/`. Change it with `--out-dir`.
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
| Persona and résumé (fictional) | `search/examples/kiran-rao/` | your-input |
| Thresholds, patterns, tier p-values | `rules.json` (this folder) | your-input |

**Reused code (not copied):**
- `normalize_company_name` from `scripts/ats/scrapers/common/normalize.py`;
- `board_url`, `fetch_board`, `normalize_jobs`, `resume_features` and `judge` from `.claude/skills/greenhouse-watch/scripts/greenhouse_watch.py`;
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
