# Domain justification — swe-sponsor-pipeline

## Executive summary

This page explains who the job-list tool is for, what hidden information it surfaces, and where it saves time. The user is an international computer-science master's student who has a few years of AI experience and needs an employer that will eventually sponsor a work visa. The tool shows which open AI and data jobs are at companies with a real sponsorship record, and which job descriptions quietly rule the student out.

## Who, in exactly what situation

The student is an international MS Computer Science student on F-1 **pre-completion OPT** (from mid-October 2026), with about **3.5 years** of AI engineering experience on the Microsoft stack. They are targeting **mid-level and senior AI Engineer, Data Scientist and Data Engineer roles**, anywhere in the US but **Texas and remote first**, at an employer that will file an H-1B.

Per DHS *Study in the States*, the 90-day unemployment limit applies to post-completion OPT, and the student, not an employer, applies for OPT. So "who sponsors OPT?" really means "who hires on OPT and sponsors an H-1B later?".

## The information asymmetry

The student can't easily see four things together:
1. a company's **H-1B record** for engineering and data titles;
2. whether it **raised money recently**;
3. whether it has an **open role at their level**;
4. whether that role's **description rules them out**.

The fourth was invisible until a hand check found both suggested AI roles closed to the student (one excluded new graduates, one required US citizenship). The tool now reads descriptions. Companies *with* H-1B history post *"unable to sponsor … for this role"* on some jobs: Verkada on 156 of 307 postings, Twin Health on 23 of 39. Job boards hide sponsorship history; H-1B sites hide live descriptions.

## Engine layers

- **80 Days to Stay:** H-1B approvals, sponsored titles, funding; Form D samples as a cross-check.
- **Job-Ops:** board discovery, liveness and job descriptions.
- **Cognitive Pivot:** national wage and job zone as context only.

The engine's own scorer makes the decision.

## Where it fits the 3-3-2 day

It takes over the **research half of the 2 research-and-apply hours**: deciding which postings deserve tailoring.

- **By hand** *(estimate)*: about 25 minutes per company to check sponsorship, funding, the careers page, the level and the fine print. For 49 companies that's roughly 20 hours.
- **With the tool** *(run time observed; review time estimated)*: a 2-minute run plus about 45 minutes clearing the gates.
- **Saving** *(estimate)*: about **15+ hours the first week**, then 2–3 hours per weekly re-run. Most of it comes from what the student can skip: 89.6% of the 67 AI and data postings evaluated.

The **network** list feeds the 3 networking hours: six recently funded sponsors with no qualifying opening today. The prototype itself is a **credibility** artifact.

## Domain-specific failure modes

1. **A role-specific "can't sponsor" read as company policy, or never read at all.** One statement can make a student write off a 272-approval sponsor. Missing it means applying to a role closed to them. *Hardest to catch for:* a time-pressed student who reads one posting per company.
2. **A top-few title list mistaken for the full sponsorship record.** Only 100 of 1,552 sponsors list an AI title, so every AI and data posting is graded "Possible" and none reaches Apply, even at Databricks (1,640 approvals). *Hardest to catch for:* a student who sees an empty Apply list and concludes nobody sponsors AI engineers.
