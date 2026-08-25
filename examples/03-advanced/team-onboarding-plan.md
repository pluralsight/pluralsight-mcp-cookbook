# Team Onboarding Plan

**Goal:** Build a reusable onboarding curriculum for new team members on your team's stack.

## Prompt

```text
Create an onboarding learning plan for new engineers joining a team that
uses TypeScript, React, PostgreSQL, and AWS. Structure it as:

- Week 1: fundamentals they must have (with a Skill IQ per topic to let
  experienced hires skip ahead)
- Weeks 2-3: core stack courses
- Week 4: hands-on labs

For each item, search Pluralsight and pick specific content. Output the
plan as a markdown document I can commit to our repo.
```

## Tools used

- `search_pluralsight_library` — many calls: `content_type: "skilliq"` for week 1 assessments, `content_type: "video-course"` with `levels` filters for weeks 2–3, `content_type: "lab"` for week 4.

## What to expect

A markdown document with named Pluralsight content per week. Review it, adjust for your team, and commit it — new hires' assistants can then execute it ("start me on week 1 of ONBOARDING.md").

## Adapt it

- Swap the stack for your own.
- Turn this prompt into a project skill so anyone can run `/onboarding-plan <stack>` — see [adding skills](../../docs/adding-skills.md).
