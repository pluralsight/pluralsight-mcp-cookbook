---
name: learning-plan
description: Build a personalized Pluralsight learning plan based on the user's recent activity and goals. Use when the user asks what to learn next, wants a study plan or curriculum, or wants to level up in a technology.
license: MIT
compatibility: Requires the Pluralsight MCP server. The optional schedule script requires Python 3.10+ (uv recommended).
metadata:
  author: Pluralsight
  version: "1.0"
---

# Build a Learning Plan

Create a personalized, ordered learning plan for the user. Their goal is: "$ARGUMENTS" (if empty, ask what skill or role they are working toward and their timeframe).

## Step 1: Understand where they are

Call `get_user_content_activity` to see the user's last 3 interactions across Pluralsight content (courses, assessments, Skill IQ scores, paths, labs). This is a snapshot, not full history — use it to:

- Infer their current level and recent focus areas.
- Avoid recommending content that appears in those recent interactions.
- Connect the plan to what they were last working on when relevant.

If the activity is empty or unrelated to the goal, ask one clarifying question about their experience level instead of guessing.

## Step 2: Find candidate content

Call `search_pluralsight_library` one or more times: `sort: "relevance"` with the goal as the query, `content_type: "path"` first, then supplement with courses, labs, and Skill IQ searches at the user's level and one level up. Full parameter values and search strategy: [references/search-parameters.md](references/search-parameters.md).

## Step 3: Assemble the plan

Present an ordered plan of 3–7 items following the arc *baseline → core learning → hands-on practice → validation*, formatted like [assets/plan-template.md](assets/plan-template.md). Detailed design rules (level progression, sequencing, right-sizing to timeframe): [references/plan-design.md](references/plan-design.md).

Only include content that appeared in tool results — never invent titles.

## Step 4 (optional): Turn the plan into a dated schedule

If the user gives a start date and weekly time budget (or asks "when will I finish?"), use the bundled script to compute the week-by-week schedule instead of doing date math yourself.

### Available scripts

- **`scripts/build_schedule.py`** — distributes plan items across calendar weeks by estimated hours. No third-party dependencies; run `--help` for the input format.

```bash
uv run scripts/build_schedule.py --input plan.json --start-date 2026-09-01 --hours-per-week 5
```

(Or `python3 scripts/build_schedule.py ...` if uv is unavailable.) Write the plan items to a JSON file — or pipe them on stdin — with each item's `title`, `type`, `level`, and estimated `hours`, then include the script's markdown output in your response.
