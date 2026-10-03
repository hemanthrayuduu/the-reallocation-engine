# Verification — iteration 1 (rules 0.4.0, run runs/2026-10-03-live-v4)

## Executive summary

This is the first hand-check of the tool's decisions after the v0.4.0 changes. Every row of the fixed verification sample (23 postings) was compared with its live job description. 22 were right and 1 was wrong: a Senior AI Engineer role that really requires 5+ years was kept, because the word "a plus" in the next sentence made the whole line look optional. A wider scan of job titles the tool treated as outside the target families found real AI and data roles it misses (reinforcement learning, model serving, data platform, distributed data systems, business intelligence engineering). Both problems are fixed in iteration 2 and checked again there.

## Run record

- Checked by Claude Code on 2026-10-03, by fetching each posting from the named board API (`boards-api.greenhouse.io`, `api.ashbyhq.com`) and reading the deciding lines (scratch helper `.build/verify_fetch.py`, gitignored).
- Run: `runs/2026-10-03-live-v4/` — 49 candidates, 11 boards, 67 target-family postings, sample of 23.

## Verification sample

| # | Why sampled | Company | Posting | Tool decision | What the live description says | Verdict |
|---:|---|---|---|---|---|---|
| 1 | kept | APPTRONIK INC | Senior Software Engineer, ML Infrastructure | kept:consider | Description: “5+ years … OR 3+ years …” → or-alternatives → 3+ ≤ 4.5; US (Austin, TX); Senior allowed | **correct** |
| 2 | kept | DATABRICKS INC | AI Engineer – Forward Deployed Engineering (AI FDE) | kept:consider | No numeric years (“extensive years”); US; no eligibility or can't-sponsor phrase | **correct** |
| 3 | kept | DATABRICKS INC | Senior Applied ML Engineer - ML4Sys | kept:consider | “4+ years …” sits under <p>Preferred Skills</p> → preferred only; no required years | **correct** |
| 4 | kept | DATABRICKS INC | Senior Data Scientist | kept:consider | No years stated; US; data-science family | **correct** |
| 5 | kept | DILIGENT ROBOTICS INC | ML Engineer, Manipulation | kept:consider | “3+ years …” under Basic Qualifications → 3+ ≤ 4.5; Anywhere in the US | **correct** |
| 6 | kept | TWIN HEALTH INC | Senior AI Engineer | kept:consider | “5+ years of industry experience … in production. Experience building consumer facing features a plus.” — “a plus” belongs to the SECOND sentence; the 5+ requirement is required → 5 > 4.5 → should be ruled-out:experience | **MISCLASSIFIED** |
| 7 | kept | VERKADA INC | Senior Software Engineer - Computer Vision | kept:consider | “4+ years industry SWE” + “1+ years neural nets” → max 4 ≤ 4.5; also says “We do sponsor … for this role” | **correct** |
| 8 | kept | VERKADA INC | Software Engineer - Computer Vision | kept:consider | “1-3 years” + “1+ years …” → 1+; also says “We do sponsor … for this role” | **correct** |
| 9 | first 3 of non-us | COHERE HEALTH INC | Data Science Manager | non-us | Hyderabad, Telangana, India | **correct** |
| 10 | first 3 of non-us | COHERE HEALTH INC | Data Scientist | non-us | Hyderabad, Telangana, India | **correct** |
| 11 | first 3 of non-us | COHERE HEALTH INC | Lead Applied Scientist | non-us | Hyderabad, Telangana, India | **correct** |
| 12 | first 3 of ruled-out:eligibility | DATABRICKS INC | AI Engineer – Forward Deployed Engineering (AI FDE), U.S. Public Sector (Federal Focus) | ruled-out:eligibility | “U.S. citizenship and eligibility for a U.S. government secret clearance are required” | **correct** |
| 13 | first 3 of ruled-out:experience | DATABRICKS INC | Senior Software Engineer (Backend) - AI/ML Environments | ruled-out:experience | “5+ years of experience in backend or infrastructure engineering” (required) | **correct** |
| 14 | first 3 of ruled-out:experience | DATABRICKS INC | Senior Software Engineer, AI Native Web Platform | ruled-out:experience | “8+ years of software engineering experience” (required) | **correct** |
| 15 | first 3 of ruled-out:experience | DATABRICKS INC | Senior Software Engineer, AI Runtime | ruled-out:experience | “5+ years of experience building and operating large-scale distributed systems” (required) | **correct** |
| 16 | first 3 of wrong-level | APPTRONIK INC | Principal Robotics Machine Learning Engineer | wrong-level | Title says Principal | **correct** |
| 17 | first 3 of wrong-level | APPTRONIK INC | Staff MLOps Engineer | wrong-level | Title says Staff | **correct** |
| 18 | first 3 of wrong-level | CODAMETRIX INC | Principal Data Engineer | wrong-level | Title says Principal | **correct** |
| 19 | boundary other-family title | APPTRONIK INC | Controls Engineer - Actuation | other-family | Controls engineering, not AI/data | **correct** |
| 20 | boundary other-family title | APPTRONIK INC | Electrical Engineer | other-family | Electrical engineering | **correct** |
| 21 | boundary other-family title | APPTRONIK INC | Firmware Engineer - Actuation | other-family | Embedded firmware | **correct** |
| 22 | boundary other-family title | APPTRONIK INC | Firmware Engineer – Hands | other-family | Embedded firmware | **correct** |
| 23 | boundary other-family title | APPTRONIK INC | Hardware Integration Engineer - Dexterity | other-family | Hardware integration | **correct** |

**Sample result: 1 misclassified of 23.**

## Extended boundary scan (beyond the sample)

The sample's 5 boundary rows all came from one company (the rule takes the first five by company), so every other-family title containing an AI or data word was also read. These are real AI or data roles the title rule missed (false negatives):

| Company | Title the tool counted as other-family | Why it belongs |
|---|---|---|
| APPTRONIK INC | [Senior Reinforcement Learning Engineer](https://boards.greenhouse.io/apptronik/jobs/5813673004?gh_jid=5813673004) | reinforcement learning is machine learning |
| APPTRONIK INC | [Senior Reinforcement Learning Engineer](https://boards.greenhouse.io/apptronik/jobs/6142286004?gh_jid=6142286004) | reinforcement learning is machine learning |
| COHERE HEALTH INC | [Business Intelligence Engineer](https://job-boards.greenhouse.io/coherehealth/jobs/7693133003) | business-intelligence engineering is data/analytics engineering |
| COHERE HEALTH INC | [Sr Business Intelligence Engineer](https://job-boards.greenhouse.io/coherehealth/jobs/7663856003) | business-intelligence engineering is data/analytics engineering |
| COHERE HEALTH INC | [Sr. Software Engineer, Data Platform](https://job-boards.greenhouse.io/coherehealth/jobs/7978386003) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Senior Software Engineer (Data Platform)](https://databricks.com/company/careers/open-positions/job?gh_jid=7647369002) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Senior Software Engineer - Data Platform](https://databricks.com/company/careers/open-positions/job?gh_jid=7601580002) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Senior Software Engineer - Distributed Data Systems](https://databricks.com/company/careers/open-positions/job?gh_jid=4513122002) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Senior Software Engineer - Distributed Data Systems](https://databricks.com/company/careers/open-positions/job?gh_jid=6544325002) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Senior Software Engineer - Distributed Data Systems](https://databricks.com/company/careers/open-positions/job?gh_jid=6936994002) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Senior Software Engineer - Distributed Data Systems](https://databricks.com/company/careers/open-positions/job?gh_jid=8012800002) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Senior Software Engineer, Model Serving](https://databricks.com/company/careers/open-positions/job?gh_jid=8211648002) | model serving is ML infrastructure |
| DATABRICKS INC | [Software Engineer - Distributed Data Systems](https://databricks.com/company/careers/open-positions/job?gh_jid=8012691002) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Staff Software Engineer (Data Platform)](https://databricks.com/company/careers/open-positions/job?gh_jid=7652016002) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Staff Software Engineer - Data Platform](https://databricks.com/company/careers/open-positions/job?gh_jid=7601572002) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Staff Software Engineer - Distributed Data Systems](https://databricks.com/company/careers/open-positions/job?gh_jid=5646855002) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Staff Software Engineer - Distributed Data Systems](https://databricks.com/company/careers/open-positions/job?gh_jid=6544364002) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Staff Software Engineer - Distributed Data Systems](https://databricks.com/company/careers/open-positions/job?gh_jid=6937001002) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Staff Software Engineer - Distributed Data Systems](https://databricks.com/company/careers/open-positions/job?gh_jid=8012831002) | data-platform / distributed-data engineering is data engineering |
| DATABRICKS INC | [Staff Software Engineer, Foundational Model Serving](https://databricks.com/company/careers/open-positions/job?gh_jid=8224683002) | model serving is ML infrastructure |
| DATABRICKS INC | [Staff Software Engineer, Model Serving](https://databricks.com/company/careers/open-positions/job?gh_jid=8211647002) | model serving is ML infrastructure |
| VERKADA INC | [Senior Software Engineer, Data Platform](https://job-boards.greenhouse.io/verkada/jobs/5215882007) | data-platform / distributed-data engineering is data engineering |
| VERKADA INC | [Software Engineer - Data Platform](https://job-boards.greenhouse.io/verkada/jobs/4129304007) | data-platform / distributed-data engineering is data engineering |

**Extended scan: 23 false negatives** (titles listed above; seniority and description rules still apply once they are recognised).

## Fixes for iteration 2 (principled, logged in the `rules.json` changelog)

1. **"A plus" is read per sentence, not per line.** A years mention is preferred only if its own sentence says "a plus", "nice to have" or "bonus".
2. **Family words added:** AI: reinforcement learning, model serving, model inference, foundation model. Data engineering: a role word plus data platform, data infrastructure, distributed data, data pipeline(s), data systems, big data, data warehouse, lakehouse, ETL; and the title "business intelligence engineer" / "BI engineer". Not applied when the title names security, support, sales, solutions, partner, customer, marketing, QA or test work.
3. **Sample rule:** boundary titles are taken round-robin across companies (still deterministic), so one board cannot fill all five rows.

Iteration 2 re-runs live and repeats this check.
