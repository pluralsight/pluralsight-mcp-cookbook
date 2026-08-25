# Use the Learning-Plan Skill

**Goal:** Run the bundled `learning-plan` skill end-to-end to get a personalized, ordered curriculum.

## Prompt

In Claude Code, invoke the skill directly:

```text
/pluralsight:learning-plan become proficient in Go for backend services within 2 months
```

Or phrase it naturally and let the skill trigger automatically:

```text
Build me a study plan to become proficient in Go backend development.
I have about 2 months and 5 hours a week.
```

## What happens

The [learning-plan skill](../../plugins/pluralsight/skills/learning-plan/SKILL.md) walks the assistant through a fixed process:

1. `get_user_content_activity` — establish your current level and avoid recommending completed content.
2. `search_pluralsight_library` — paths first, then courses/labs/assessments at appropriate levels.
3. Assemble a 3–7 item ordered plan: optional baseline assessment → core learning → hands-on practice → validation.

## What to expect

An ordered plan sized to your timeframe, with a reason for each item. Follow up with "compress this to 1 month" or "swap the labs for courses" — the plan is a conversation, not a one-shot output.

## Why a skill instead of a prompt?

The skill encodes the process (read activity first, prefer paths, always include practice) so results are consistent every time, for everyone on your team. Compare with the raw-prompt version in [what-to-learn-next](../02-intermediate/what-to-learn-next.md).
