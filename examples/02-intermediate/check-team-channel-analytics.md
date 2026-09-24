# Check Your Team's Learning Time

> **Leader only.** Both tools in this example require a Pluralsight leader/team-management plan. If you don't manage a team, they'll error rather than return results.

**Goal:** Find out how much time your team has spent learning recently, without knowing the analytics API's query names or fields up front.

## Prompt

```text
How much time has my team spent learning in the last 30 days? Break it down
by video, labs, and practice exams.
```

Variations:

```text
What leader-analytics data can I pull? List the available queries.
```

## Tools used

1. `analytics_explore` — with no arguments, lists every available leader-analytics query and a one-line description of each. Narrow with `filter` (e.g. `"learningTimeSummary"`) and `include_details: true` to see that query's exact filters and output fields before running it.
2. `analytics_execute` — with `query_name: "learningTimeSummary"`, a `filters` object (e.g. `{"interval": "LAST_30_DAYS"}`), and `nodes` naming the output fields discovered in step 1 (e.g. `totalLearningTime`, `videoLearningTime`, `handsOnLabLearningTime`). A query with a date range needs either `interval` or both `intervalStartDate` and `intervalEndDate` — omitting both errors.

## What to expect

The assistant should call `analytics_explore` first (optionally with `filter` narrowed to a relevant query) to find the right query name and confirm which fields are available, rather than guessing `nodes` from memory. `analytics_execute` then returns the rows — for a summary query like `learningTimeSummary`, typically one row per plan, with time values in seconds. Results are capped at 200 rows, so a query returning per-learner detail may need narrower filters. This pairing generalizes to any of the other leader-analytics queries `analytics_explore` lists (course usage, Skill IQ activity, hands-on lab attempts, and more) — the same discover-then-run pattern applies to all of them.
