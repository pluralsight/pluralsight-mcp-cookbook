# Run the Learning-Advisor Agent

**Goal:** Delegate open-ended curriculum design to a dedicated agent with its own focused context.

## Prompt

In Claude Code, mention the agent or describe a matching task:

```text
Use the learning-advisor agent to design a curriculum for me to move from
backend development into a platform engineering role over the next 6 months.
```

## What happens

The [learning-advisor agent](../../plugins/pluralsight/agents/learning-advisor.md) runs as a subagent restricted to the Pluralsight search and activity tools. It:

1. Assesses your current level from `get_user_content_activity`.
2. Narrows vague goals into concrete technologies and milestones.
3. Researches paths, courses, labs, and assessments at multiple levels.
4. Verifies specific subtopics are covered using `query_pluralsight_content_index`.
5. Returns a milestone-based curriculum sized to your timeframe.

## What to expect

A more thorough result than a single prompt: the agent iterates on searches in its own context and reports back only the finished curriculum. Use the agent for big, fuzzy goals (career moves, certifications); use the [learning-plan skill](use-learning-plan-skill.md) for quicker single-topic plans.

## Skill vs. agent

- **Skill** = a repeatable procedure injected into your current conversation.
- **Agent** = a delegate with its own context, tool restrictions, and persona, best for open-ended research-heavy tasks.
