# Domain justification — swe-sponsor-pipeline

## Executive summary

This page explains who the job-list tool is for, what hidden information it surfaces, and where it saves time in a job-search day. It is built for an international computer-science master's student on pre-completion OPT who has a few years of AI engineering experience and needs an employer that will eventually sponsor a work visa. The core problem: the student can't easily see which open AI Engineer jobs are at companies with a real sponsorship record, and which job descriptions quietly rule them out. Here is the case that the tool turns many hours of manual checking into a short review, and the two mistakes it is most likely to make.

## Who, in exactly what situation

The student is an international MS Computer Science student on F-1 status, working under **pre-completion OPT** from mid-October 2026. They have about **3.5 years** of prior AI engineering experience (Azure OpenAI, Semantic Kernel, Azure ML, C#/.NET). They want **mid-level and senior AI Engineer, Data Scientist and Data Engineer roles**, ideally on the Microsoft AI and data stack, anywhere in the US but **Texas and remote first**, at an employer that will file an H-1B.

Two facts from DHS (*Study in the States*, F-1 OPT page, checked 2026-10-02) shape the timing:
- The 90-day unemployment limit applies to **post-completion** OPT.
- OPT is applied for by the **student**; no employer "sponsors OPT". So the question "who sponsors OPT?" really means "who hires people on OPT and will sponsor an H-1B later?". That is what this recipe answers from the H-1B record.

## The information asymmetry

From the outside, this student cannot easily see four things together:
1. Whether a company has a real **H-1B record** for engineering titles.
2. Whether it **raised money recently**.
3. Whether it has an **open AI Engineer posting at their level** today.
4. Whether that posting's **description rules them out**.

The fourth was invisible until the author checked by hand at gate G3 in iteration 1. Both AI Engineer roles the tool suggested then were disqualifying: one was closed to new graduates, the other required US citizenship and a secret clearance. Iteration 2 reads descriptions. It found live postings at companies *with* H-1B history saying *"unable to sponsor … for this role"*: Verkada on 156 of 307 postings, Twin Health on 23 of 39. Job boards don't show sponsorship history; H-1B lookup sites don't show live descriptions; a chatbot answers "does X sponsor?" fluently either way. The tool joins them and labels which parts are records.

## Engine layers it connects

- **80 Days to Stay:** H-1B approvals, sponsored titles, funding; Form D samples as a cross-check.
- **Job-Ops:** board discovery, liveness, and now the job descriptions, through the repo's allow-listed Greenhouse/Ashby fetcher.
- **Cognitive Pivot:** national wage and job zone as context only (the scorer gives role quality zero weight).

Decisions come from the engine's own scorer, unchanged.

## Where it fits the 3-3-2 day

It takes over the **research half of the 2 research-and-apply hours**: finding which postings are even worth tailoring.

- **By hand** *(estimate, not measured)*: about 25–30 minutes per company to check sponsorship history, funding, the careers page, the level, and the fine print. For the 49 candidate companies in iteration 3 that is roughly 20–25 hours.
- **With the tool** *(run time observed; review time estimated)*: about 2 minutes for the run, then roughly 45 minutes to clear gates G1–G3.
- **Saving** *(estimate)*: **15+ hours the first week**, then 2–3 hours per weekly re-run. Most of it comes from what it lets the student skip: 89.6% of the 67 AI and data postings evaluated in iteration 3, including 8 Senior roles whose descriptions ask 5+ years.

It also **feeds the 3 networking hours**. In iteration 3 the network list (Cohere Health, Outset Medical, Twin Health, PsiQuantum, VidMob, CodaMetrix) names recently funded sponsors with no qualifying AI opening today, each shown with its count of "can't sponsor this role" postings. The prototype itself is a **credibility-hours** artifact for an AI engineer.

## Domain-specific failure modes

1. **A role-specific "can't sponsor" read as company policy, or the reverse.** Verkada's statement appears on most sales roles but not its backend roles. A student who sees it once may write off a 272-approval sponsor. A student who never reads it may apply to a role explicitly closed to them. *Hardest to catch for:* someone short on time who reads one posting per company. The tool counts the statements per company and rules out only the posting that carries them.
2. **A top-few title list mistaken for the whole sponsorship record.** The CSV keeps only a company's top sponsored titles, and only 100 of 1,552 sponsors list an AI/ML title. So every AI and data posting in iterations 2 and 3 was graded "Possible" and none reached Apply, even at Databricks (1,640 approvals). *Hardest to catch for:* a student who sees an empty Apply list and concludes nobody sponsors AI engineers. Per-petition SOC data (recipe TODO 1) is the fix.
