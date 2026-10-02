# Domain justification — swe-sponsor-pipeline

## Executive summary

This page explains who the job-list tool is for, what hidden information it surfaces, and where it saves time in a job-search day. It is built for an international computer-science master's student who graduates in December and needs a visa-sponsoring employer. The core problem: the student can't easily see which open jobs are at companies with a real record of sponsoring this kind of role. Here is the case that the tool turns hours of manual checking into a short review, and the two mistakes it is most likely to make.

## Who, in exactly what situation

An international MS Computer Science student in Boston, graduating **December 2026**, on F-1 status with post-completion OPT **not yet started** (EAD expected around January 2027). They are targeting entry-level **software and AI/ML engineering** roles (SOC 15-1252 Software Developers; 15-1221 for AI Engineer and Applied Scientist titles), and they need an employer that will file an H-1B.

Timing is what makes this the right moment. Applying in October–December burns **zero** of the 90 unemployment days, because the clock only starts with OPT. But only applications to real postings at real sponsors count. Every week spent on non-sponsors is a week the clock will later take back.

## The information asymmetry

From the outside, the student cannot easily see three things together:
1. Whether a company has **sponsored H-1Bs for software titles**, rather than for any title.
2. Whether it **raised money recently** and is likely hiring.
3. Whether it has an **open entry-level US posting today**, or only senior roles and ghost listings.

Job boards show postings without sponsorship history. H-1B lookup sites show history without postings. Neither shows funding. A chatbot answers "does X sponsor?" fluently whether or not a record exists. The tool joins the three, and it labels which parts are records and which are the student's own rules.

## Engine layers it connects

- **80 Days to Stay:** H-1B approvals, sponsored titles and funding from the mapped CSV, cross-checked against the Form D samples.
- **Job-Ops:** board discovery and liveness, through the repo's allow-listed Greenhouse/Ashby fetcher.
- **Cognitive Pivot:** national wage and job zone shown beside each posting as context only, because the scorer gives role quality zero weight.

Decisions come from the engine's own scorer, run unchanged.

## Where it fits the 3-3-2 day

It takes over the **research half of the 2 research-and-apply hours**: deciding *which* postings deserve tailoring, before any tailoring starts.

- **By hand** *(estimate, not measured)*: about 20–25 minutes per company to look up sponsorship history, check funding, find the careers page and filter to entry-level US roles. For the 37 candidate companies that is roughly 12–15 hours.
- **With the tool** *(observed for the run; the review time is an estimate)*: the run itself takes about 2 minutes. Clearing gates G1–G3 takes roughly 45 minutes.
- **Saving** *(estimate)*: about **10+ hours the first week**, then 2–3 hours per weekly re-run. The saving is mostly in the companies it lets the student skip: 96% of evaluated postings in this run.

It also **feeds the 3 networking hours**. The "network, don't apply" list names strong, recently funded sponsors with no matching opening today; in this run, Apptronik, Twin Health, PsiQuantum and VidMob. Those are targets for an informational conversation before a role opens. The prototype itself, with its tests and an honest account of what it can't verify, is a **credibility-hours** artifact for a software-engineering candidate.

## Domain-specific failure modes

1. **"Software Engineer" means different jobs.** The sponsorship match is by title family. So a robotics or quantum-hardware company's past "Software Engineer III" petitions count toward an embedded-firmware posting, and a med-tech company's toward a cloud backend role. *Hardest to catch for:* a new graduate who hasn't yet seen how differently industries use the title. A long-time engineer would spot it from the job description in seconds.
2. **A strong sponsor is mistaken for a good match.** A company with hundreds of approvals clears "Apply" on sponsorship alone, even when the résumé barely matches (live run: fit 0.25, still Apply). *Hardest to catch for:* a student anxious about the clock, who reads "Apply" as "you'll get this job". The fit column is the only warning, and the report's ordering doesn't force anyone to read it.
