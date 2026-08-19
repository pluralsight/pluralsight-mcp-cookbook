# What Should I Learn Next?

**Goal:** Get recommendations grounded in what you've actually been learning, not generic suggestions.

## Prompt

```text
Look at my recent Pluralsight activity and recommend what I should learn next
to build on it. Suggest 2-3 options and explain why each fits.
```

## Tools used

1. `get_user_content_activity` — to see your recent courses, assessments, and Skill IQ scores.
2. `search_pluralsight_library` — one or more searches for content that extends your recent topics, filtered to appropriate levels.

## What to expect

Recommendations that reference your actual history ("since you finished X, a natural next step is Y") rather than a generic top-10 list. If your recent activity spans several topics, the assistant should ask which direction you want to go or offer one option per topic.

## Why this matters

This is the core pattern of personalized workflows: **read state, then search**. The advanced examples build on it — see the [learning-plan skill](../03-advanced/use-learning-plan-skill.md).
