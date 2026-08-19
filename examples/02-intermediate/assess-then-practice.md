# Assess, Then Practice

**Goal:** Figure out your actual level with a Skill IQ, then get hands-on practice matched to it.

## Prompt

```text
I think I'm intermediate at SQL but I'm not sure. Find me a Pluralsight
Skill IQ assessment for SQL, and based on my recent activity, suggest
hands-on labs at the level you think I'm actually at.
```

## Tools used

1. `search_pluralsight_library` with `content_type: "skilliq"` — find the assessment.
2. `get_user_content_activity` — check for existing Skill IQ scores or recent SQL content that indicates level.
3. `search_pluralsight_library` with `content_type: "lab"` and a `levels` filter — find matching hands-on labs.

## What to expect

A link to the Skill IQ assessment plus lab suggestions. If your activity already includes a SQL Skill IQ score, the assistant should use it instead of guessing. This measure-then-practice loop is the foundation of the validation steps in the advanced learning-plan workflows.
