# Verification — iteration 2 (rules 0.4.1, run runs/2026-10-03-live-v4)

## Executive summary

This is the second hand-check, after fixing what iteration 1 found. Of the 25 sampled postings, 23 were right and 2 were wrong — the same reinforcement-learning role listed in two cities. It requires 5+ years (written as "expertise (5+ years)") and only prefers 2+ years of industry experience, but the tool read the preferred 2+ as the requirement. The iteration-1 problems are gone: the Senior AI Engineer that needs 5+ years is now ruled out, and the data-platform and reinforcement-learning titles are now recognised. A rescan of the remaining other-family titles found no further AI or data engineering roles being missed. Both new problems are fixed in iteration 3.

## Run record

- Checked by Claude Code on 2026-10-03 against the live descriptions (named board APIs only).
- Run: 49 candidates, 11 boards, 92 target-family postings, sample of 25.

## Verification sample

| # | Why sampled | Company | Posting | Location | Tool decision | What the live description says | Verdict |
|---:|---|---|---|---|---|---|---|
| 1 | kept | APPTRONIK INC | Senior Reinforcement Learning Engineer | Sunnyvale, CA | kept:consider | Required section: “Deep, hands-on expertise (5+ years) with common RL frameworks …”; education line: “… 2+ years industry experience strongly preferred.” → the 2+ is PREFERRED and the 5+ (written as “expertise (5+ years)”) is REQUIRED → 5 > 4.5 → should be ruled-out:experience | **MISCLASSIFIED** |
| 2 | kept | APPTRONIK INC | Senior Reinforcement Learning Engineer | Austin, TX | kept:consider | Same description as #1 (Austin listing) | **MISCLASSIFIED** |
| 3 | kept | APPTRONIK INC | Senior Software Engineer, ML Infrastructure | Austin, TX | kept:consider | “5+ … OR 3+ …” → 3+ | **correct** |
| 4 | kept | DATABRICKS INC | AI Engineer – Forward Deployed Engineering (AI FDE) | United States | kept:consider | no numeric years | **correct** |
| 5 | kept | DATABRICKS INC | Senior Applied ML Engineer - ML4Sys | San Francisco, California | kept:consider | 4+ under <p>Preferred Skills</p> | **correct** |
| 6 | kept | DATABRICKS INC | Senior Data Scientist | Mountain View, California; San Francisco, California | kept:consider | no years stated | **correct** |
| 7 | kept | DILIGENT ROBOTICS INC | ML Engineer, Manipulation | Anywhere in the US | kept:consider | 3+ under Basic Qualifications | **correct** |
| 8 | kept | VERKADA INC | Senior Software Engineer - Computer Vision | San Mateo, CA United States | kept:consider | 4+ and 1+ → 4+; “We do sponsor … for this role” | **correct** |
| 9 | kept | VERKADA INC | Software Engineer - Computer Vision | San Mateo, CA United States | kept:consider | 1-3 and 1+ → 1+; “We do sponsor … for this role” | **correct** |
| 10 | kept | VERKADA INC | Software Engineer - Data Platform | San Mateo, CA United States | kept:consider | “1-3 years of software engineering experience” → 1+; data-platform engineering is data engineering; “We do sponsor … for this role” | **correct** |
| 11 | first 3 of non-us | COHERE HEALTH INC | Business Intelligence Engineer | Hyderabad, Telangana, India | non-us | Hyderabad, India | **correct** |
| 12 | first 3 of non-us | COHERE HEALTH INC | Data Science Manager | Hyderabad, Telangana, India | non-us | Hyderabad, India | **correct** |
| 13 | first 3 of non-us | COHERE HEALTH INC | Data Scientist | Hyderabad, Telangana, India | non-us | Hyderabad, India | **correct** |
| 14 | first 3 of ruled-out:eligibility | DATABRICKS INC | AI Engineer – Forward Deployed Engineering (AI FDE), U.S. Public Sector (Federal Focus) | Maryland; Virginia; Washington, D.C. | ruled-out:eligibility | “U.S. citizenship … required” | **correct** |
| 15 | first 3 of ruled-out:experience | COHERE HEALTH INC | Sr. Software Engineer, Data Platform | United States | ruled-out:experience | “5+ years of experience in data engineering …” (required) | **correct** |
| 16 | first 3 of ruled-out:experience | DATABRICKS INC | Senior Software Engineer (Backend) - AI/ML Environments | Mountain View, California | ruled-out:experience | “5+ years of experience in backend …” (required) | **correct** |
| 17 | first 3 of ruled-out:experience | DATABRICKS INC | Senior Software Engineer - Distributed Data Systems | Bellevue, Washington | ruled-out:experience | “5+ years of production level experience …” (required) | **correct** |
| 18 | first 3 of wrong-level | APPTRONIK INC | Principal Robotics Machine Learning Engineer | Austin, TX | wrong-level | Principal | **correct** |
| 19 | first 3 of wrong-level | APPTRONIK INC | Staff MLOps Engineer | Onsite - Austin, TX | wrong-level | Staff | **correct** |
| 20 | first 3 of wrong-level | CODAMETRIX INC | Principal Data Engineer | Boston Hybrid • Remote | wrong-level | Principal | **correct** |
| 21 | boundary other-family title | APPTRONIK INC | Controls Engineer - Actuation | — | other-family | controls engineering | **correct** |
| 22 | boundary other-family title | COHERE HEALTH INC | Associate SDET Engineer | — | other-family | QA / SDET test engineering | **correct** |
| 23 | boundary other-family title | DATABRICKS INC | Sales Dev AI Program Manager | — | other-family | sales program management | **correct** |
| 24 | boundary other-family title | DILIGENT ROBOTICS INC | Lead Engineer, Issue Management & Triage | — | other-family | issue-management / program lead, not AI/data | **correct** |
| 25 | boundary other-family title | OUTSET MEDICAL INC | Field Service Engineer II (Dubuque, IA) | — | other-family | field service | **correct** |

**Sample result: 2 misclassified of 25.**

## Extended boundary scan

Every other-family title containing an AI or data word, read by hand. Most are product, marketing, sales, management, solutions/support, security, database-engine or analyst roles, which are correctly outside the target families.

- APPTRONIK INC — Director, Product Learning & Development
- APPTRONIK INC — IROS 2026 - Robotics & AI Talent
- APPTRONIK INC — Principal People Analytics Specialist
- APPTRONIK INC — Senior Security Engineer - Data Platform
- APPTRONIK INC — Staff Product Manager, Applied AI
- COHERE HEALTH INC — Healthcare Analytics
- COHERE HEALTH INC — Lead Data Analyst
- COHERE HEALTH INC — Manager, Data Analytics
- COHERE HEALTH INC — Senior Manager, Applied Science
- COHERE HEALTH INC — Senior Manager, Data Platform Engineering
- COHERE HEALTH INC — Staff Data Architect
- DATABRICKS INC — AI Transformation Leader
- DATABRICKS INC — Customer Enablement Architect (Capability Engineering & AI Adoption)
- DATABRICKS INC — Delivery Solutions Architect - Healthcare & Life Sciences
- DATABRICKS INC — Delivery Solutions Architect - Public Sector (DOW, DHS, Intelligence Community)
- DATABRICKS INC — Director of Engineering (Data Infrastructure)
- DATABRICKS INC — Director, Agent & AI Search
- DATABRICKS INC — Director, Americas Field Marketing at Databricks
- DATABRICKS INC — Director, Marketing Strategy and AI Transformation
- DATABRICKS INC — Director, Product Marketing, AI
- DATABRICKS INC — Engineering Manager - Data Visualization Platform
- DATABRICKS INC — Engineering Manager - Databricks SQL Control Plane
- DATABRICKS INC — Finance Data and AI Lead
- DATABRICKS INC — Lakebase Associate Director, Healthcare & Life Sciences
- DATABRICKS INC — Lead Engagement Manager, FDE - Healthcare & Life Sciences
- DATABRICKS INC — Lead Learning Product Manager
- DATABRICKS INC — Lead Solutions Architect - Generative AI (EMEA Emerging DNB)
- DATABRICKS INC — Manager, Engineering - AI/BI
- DATABRICKS INC — P2P Data & Automation Lead
- DATABRICKS INC — Partner Engineer: Partner Intelligence, AI & Apps
- DATABRICKS INC — Sales Dev AI Program Manager
- DATABRICKS INC — Senior Customer Enablement AI Programs Manager
- DATABRICKS INC — Senior Engineering Manager for Self-Serve (Learning)
- DATABRICKS INC — Senior Finance Specialist (Data & AI)
- DATABRICKS INC — Senior Forward Deployed Engineer (Technical Data Architect)
- DATABRICKS INC — Senior ML & AI Technical Solutions Engineer
- DATABRICKS INC — Senior Manager - Technical Solutions (Big Data / AI)
- DATABRICKS INC — Senior Manager, AI Forward Deployed Engineering - London
- DATABRICKS INC — Senior Manager, Finance Data and AI
- DATABRICKS INC — Senior Software Engineer - Database Engine Internals
- DATABRICKS INC — Senior Solutions Architect (Data & AI) - Leeds based
- DATABRICKS INC — Senior Solutions Architect (EDW Enterprise Data Warehouse Migrations)
- DATABRICKS INC — Senior Solutions Engineer (Presales, Technical, Data and AI)
- DATABRICKS INC — Senior Solutions Engineer (Technical, Presales, Data & AI, DNB)
- DATABRICKS INC — Senior Specialist Solutions Architect (AI/ML)
- DATABRICKS INC — Senior Staff Software Engineer - Lakeflow Pipelines Datasets
- DATABRICKS INC — Software Engineer - Database Engine Internals
- DATABRICKS INC — Solutions Architect - Healthcare/Life Sciences Team (HLS)
- DATABRICKS INC — Specialist Solutions Architect - AI/ML
- DATABRICKS INC — Specialist Solutions Architect - Data Engineering & Warehousing (Financial Services)
- DATABRICKS INC — Specialist Solutions Architect - Data Warehousing
- DATABRICKS INC — Sr Software Engineer- Customer Experience Intelligence (CXI)
- DATABRICKS INC — Sr. Deployment Strategist, FDE - Healthcare & Life Sciences
- DATABRICKS INC — Sr. Engineering Manager - Customer Experience Intelligence (CXI)
- DATABRICKS INC — Sr. Engineering Manager - Notebook Dataplane
- DATABRICKS INC — Sr. Engineering Manager, AI Runtime
- DATABRICKS INC — Sr. Forward Deployed Engineer (FDE) - Healthcare & Life Sciences
- DATABRICKS INC — Sr. Learning Platform Specialist
- DATABRICKS INC — Sr. Manager – Data & AI Support Engineering
- DATABRICKS INC — Sr. Manager, AI Forward Deployed Engineering
- DATABRICKS INC — Sr. Manager, AI Forward Deployed Engineering (AI FDE)
- DATABRICKS INC — Sr. Manager, Compensation Analytics & Intelligence
- DATABRICKS INC — Sr. Manager, Engineering - AI/BI
- DATABRICKS INC — Sr. Manager, Field Engineering - Healthcare and Life Sciences (Healthcare Providers)
- DATABRICKS INC — Sr. Product Designer, AI/BI
- DATABRICKS INC — Sr. Product Manager, Data Engineering
- DATABRICKS INC — Sr. Product Manager, Data Governance
- DATABRICKS INC — Sr. Product Manager, Databricks AI
- DATABRICKS INC — Sr. Product Manager, Databricks Free Edition
- DATABRICKS INC — Sr. Product Manager, Databricks Repos
- DATABRICKS INC — Sr. Staff Software Engineer - Unity Catalog Data Governance
- DATABRICKS INC — Sr. Technology Partner Director - AI Code-Gen & Apps
- DATABRICKS INC — Staff Partner Engineer, AI Partnerships
- DATABRICKS INC — Staff Product Designer, AI Products
- DATABRICKS INC — Staff Product Manager, Agentic AI Applications
- DATABRICKS INC — Staff Software Engineer - Database Engine Internals
- DATABRICKS INC — Staff Software Engineer - Databases
- DATABRICKS INC — Staff Software Engineer – Customer Experience Intelligence (CXI)
- DATABRICKS INC — Staff Software Engineer, Data Collection (Tags & SDKs)
- DATABRICKS INC — Staff Software Engineer, Sales Data & Agents
- DATABRICKS INC — Strategic Account Executive, Life Science
- DATABRICKS INC — Strategic Enterprise Account Executive, Life Sciences
- DATABRICKS INC — Tax Data & Technology Manager
- PSIQUANTUM CORP — Director, Datacenter System Architecture
- PSIQUANTUM CORP — Technical Product Management Lead, Datacenter Networking & Optical Interconnect
- TWIN HEALTH INC — AI Automation QA Engineer
- TWIN HEALTH INC — Principal Product Manager, AI Experiences
- TWIN HEALTH INC — Product Analytics Associate Engineer
- TWIN HEALTH INC — Senior Marketing Data Analyst
- VERKADA INC — AI Marketing Engineer
- VERKADA INC — Growth Strategy & Analytics Manager
- VERKADA INC — Product Marketing Manager, Privacy and Data Security
- VERKADA INC — Project Manager, Data Trust
- VERKADA INC — Sales Strategy and Operations Division Lead
- VERKADA INC — Senior Software Engineer, Business Systems - Data Trust
- VERKADA INC — Software Engineering Manager, Data Protection Platform
- VERKADA INC — Staff Software Engineer - Data Protection
- VERKADA INC — Supply Chain Manager, Data Operations
- VIDMOB INC — Director, Data Partnerships

**Extended scan (99 titles): no clear AI-engineering, data-engineering or data-science role at an eligible level is missed.**

- **Borderline (left for the human gate, because the title does not say what the work is):** Databricks "Senior Forward Deployed Engineer (Technical Data Architect)" (customer-facing data architecture), Twin Health "Product Analytics Associate Engineer" (analytics, below the target level), Databricks "Sr Software Engineer – Customer Experience Intelligence (CXI)".
- **Data or AI work, but excluded on level anyway:** Databricks "Senior Staff Software Engineer – Lakeflow Pipelines Datasets", "Sr. Staff Software Engineer – Unity Catalog Data Governance", "Staff Software Engineer, Sales Data & Agents"; Cohere Health "Staff Data Architect". Recognising their family would not change the outcome.

## Fixes for iteration 3 (logged in the `rules.json` changelog)

1. **"Preferred" after the number marks the mention preferred** ("2+ years industry experience strongly preferred"), unless "required" comes first ("5+ years required; 7+ preferred").
2. **Years written as "expertise (N+ years)" or "N+ years of expertise" count**, like "N+ years of experience".

Iteration 3 re-runs live and repeats this check.
