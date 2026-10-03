# Verification — iteration 3 (rules 0.4.2, run runs/2026-10-03-live-v4) — PASS

## Executive summary

This is the third hand-check, after the fixes from iterations 1 and 2. All 23 sampled postings matched their live job descriptions: zero misclassifications, which is the stopping rule agreed in the design. As extra assurance, every one of the 16 postings ruled out for asking too many years was also checked from its evidence line, and all 16 state a required 5+ or 8+ years. One harmless family mistake is noted: a developer-advocate role counts as AI work, but it is ruled out on years anyway. Zero errors in a sample is not proof of zero errors overall; the full audit file lets anyone extend the check.

## Run record

- Checked by Claude Code on 2026-10-03 against the live descriptions (named board APIs only).
- Run: 49 candidates, 11 boards, 92 target-family postings, 8 kept (consider), sample of 23.

## Verification sample

| # | Why sampled | Company | Posting | Location | Tool decision | What the live description says | Verdict |
|---:|---|---|---|---|---|---|---|
| 1 | kept | APPTRONIK INC | Senior Software Engineer, ML Infrastructure | Austin, TX | kept:consider | “5+ … OR 3+ …” → 3+ ≤ 4.5; Austin, TX | **correct** |
| 2 | kept | DATABRICKS INC | AI Engineer – Forward Deployed Engineering (AI FDE) | United States | kept:consider | no numeric years; United States | **correct** |
| 3 | kept | DATABRICKS INC | Senior Applied ML Engineer - ML4Sys | San Francisco, California | kept:consider | 4+ under <p>Preferred Skills</p> → preferred only | **correct** |
| 4 | kept | DATABRICKS INC | Senior Data Scientist | Mountain View, California; San Francisco, California | kept:consider | no years stated | **correct** |
| 5 | kept | DILIGENT ROBOTICS INC | ML Engineer, Manipulation | Anywhere in the US | kept:consider | 3+ under Basic Qualifications; Anywhere in the US | **correct** |
| 6 | kept | VERKADA INC | Senior Software Engineer - Computer Vision | San Mateo, CA United States | kept:consider | 4+ and 1+ → 4+ ≤ 4.5; “We do sponsor … for this role” | **correct** |
| 7 | kept | VERKADA INC | Software Engineer - Computer Vision | San Mateo, CA United States | kept:consider | 1-3 and 1+ → 1+; “We do sponsor … for this role” | **correct** |
| 8 | kept | VERKADA INC | Software Engineer - Data Platform | San Mateo, CA United States | kept:consider | “1-3 years of software engineering experience”; data-platform engineering; “We do sponsor … for this role” | **correct** |
| 9 | first 3 of non-us | COHERE HEALTH INC | Business Intelligence Engineer | Hyderabad, Telangana, India | non-us | Hyderabad, India | **correct** |
| 10 | first 3 of non-us | COHERE HEALTH INC | Data Science Manager | Hyderabad, Telangana, India | non-us | Hyderabad, India | **correct** |
| 11 | first 3 of non-us | COHERE HEALTH INC | Data Scientist | Hyderabad, Telangana, India | non-us | Hyderabad, India | **correct** |
| 12 | first 3 of ruled-out:eligibility | DATABRICKS INC | AI Engineer – Forward Deployed Engineering (AI FDE), U.S. Public Sector (Federal Focus) | Maryland; Virginia; Washington, D.C. | ruled-out:eligibility | “U.S. citizenship … required” | **correct** |
| 13 | first 3 of ruled-out:experience | APPTRONIK INC | Senior Reinforcement Learning Engineer | Sunnyvale, CA | ruled-out:experience | required “expertise (5+ years)”; the 2+ is “strongly preferred” → 5 > 4.5 | **correct** |
| 14 | first 3 of ruled-out:experience | APPTRONIK INC | Senior Reinforcement Learning Engineer | Austin, TX | ruled-out:experience | same as #13 (Austin listing) | **correct** |
| 15 | first 3 of ruled-out:experience | COHERE HEALTH INC | Sr. Software Engineer, Data Platform | United States | ruled-out:experience | “5+ years of experience in data engineering …” (required) | **correct** |
| 16 | first 3 of wrong-level | APPTRONIK INC | Principal Robotics Machine Learning Engineer | Austin, TX | wrong-level | Principal | **correct** |
| 17 | first 3 of wrong-level | APPTRONIK INC | Staff MLOps Engineer | Onsite - Austin, TX | wrong-level | Staff | **correct** |
| 18 | first 3 of wrong-level | CODAMETRIX INC | Principal Data Engineer | Boston Hybrid • Remote | wrong-level | Principal | **correct** |
| 19 | boundary other-family title | APPTRONIK INC | Controls Engineer - Actuation | — | other-family | controls engineering | **correct** |
| 20 | boundary other-family title | COHERE HEALTH INC | Associate SDET Engineer | — | other-family | QA / SDET | **correct** |
| 21 | boundary other-family title | DATABRICKS INC | Sales Dev AI Program Manager | — | other-family | sales program management | **correct** |
| 22 | boundary other-family title | DILIGENT ROBOTICS INC | Lead Engineer, Issue Management & Triage | — | other-family | issue-management lead, not AI/data | **correct** |
| 23 | boundary other-family title | OUTSET MEDICAL INC | Field Service Engineer II (Dubuque, IA) | — | other-family | field service | **correct** |

**Sample result: 0 misclassified of 23. Stopping rule met.**

## Extra check: every experience rule-out (16)

| Company | Posting | Location | Required years (deciding sentence) | Verdict |
|---|---|---|---|---|
| APPTRONIK INC | Senior Reinforcement Learning Engineer | Sunnyvale, CA | 5+: “Deep, hands-on expertise (5+ years) with common RL frameworks (e.g., PyTorch, JAX) and high-fidelity physics s” | **correct** |
| APPTRONIK INC | Senior Reinforcement Learning Engineer | Austin, TX | 5+: “Deep, hands-on expertise (5+ years) with common RL frameworks (e.g., PyTorch, JAX) and high-fidelity physics s” | **correct** |
| COHERE HEALTH INC | Sr. Software Engineer, Data Platform | United States | 5+: “5+ years of experience in data engineering or software development with a strong focus on data infrastructure” | **correct** |
| DATABRICKS INC | Senior Software Engineer (Backend) - AI/ML Environments | Mountain View, California | 5+: “5+ years of experience in backend or infrastructure engineering with a focus on building systems” | **correct** |
| DATABRICKS INC | Senior Software Engineer - Distributed Data Systems | Bellevue, Washington | 5+: “5+ years of production level experience in either Java, Scala or C++.” | **correct** |
| DATABRICKS INC | Senior Software Engineer - Distributed Data Systems | San Francisco, California | 5+: “5+ years of production level experience in either Java, Scala or C++.” | **correct** |
| DATABRICKS INC | Senior Software Engineer - Distributed Data Systems | Mountain View, California | 5+: “5+ years of production level experience in either Java, Scala or C++.” | **correct** |
| DATABRICKS INC | Senior Software Engineer, AI Native Web Platform | Mountain View, California | 8+: “8+ years of software engineering experience with a track record of shipping and operating production web infra” | **correct** |
| DATABRICKS INC | Senior Software Engineer, AI Runtime | Mountain View, California; San Francisco, California | 5+: “5+ years of experience building and operating large-scale distributed systems, with experience in GPU training” | **correct** |
| DATABRICKS INC | Senior Software Engineer, Model Serving | San Francisco, California | 5+: “5+ years of experience building and operating large-scale distributed systems.” | **correct** |
| DATABRICKS INC | Sr Software Engineer, Agentic Applications | Mountain View, California | 5+: “5+ years of experience with HTML, CSS, and JavaScript” | **correct** |
| DATABRICKS INC | Sr. Developer Advocate, AI and Machine Learning | San Francisco, California | 5+: “5+ years of combined experience as a developer advocate and in a hands-on technical role — software engineer, ” | **correct** |
| DATABRICKS INC | Sr. Developer Advocate, AI and Machine Learning | Seattle, Washington | 5+: “5+ years of combined experience as a developer advocate and in a hands-on technical role — software engineer, ” | **correct** |
| TWIN HEALTH INC | Senior AI Engineer | Remote, USA | 5+: “5+ years of industry experience developing AI and Machine Learning systems in production.” | **correct** |
| TWIN HEALTH INC | Senior AI Platform Engineer | Remote, USA | 5+: “Bachelor's or Master's degree in Computer Science, Engineering, or a related field with 5+ years of industry e” | **correct** |
| VERKADA INC | Senior Software Engineer, Data Platform | San Mateo, CA United States | 5+: “5+ years of data engineering related development experience” | **correct** |

**16 of 16 correct.** Note: Databricks “Sr. Developer Advocate, AI and Machine Learning” is counted in the AI family ("developer" + "AI"). It is developer relations, not AI engineering, but it is ruled out on years (5+), so the outcome does not change. Logged as a next step: add “advocate” to the AI family's not-if words.

## Extended boundary scan

The family rules did not change in 0.4.2, so the iteration-2 scan stands: no clear AI-engineering, data-engineering or data-science role at an eligible level is missed; three borderline titles are left for the human gate (see verify-iteration-2.md).
