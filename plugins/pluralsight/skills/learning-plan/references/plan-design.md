# Designing a good learning plan

Detailed guidance for assembling the plan in Step 3 of the skill.

## Plan shape

Present an ordered plan with 3–7 items in this arc:

1. **Baseline** (optional): a Skill IQ assessment to measure the starting point. Include it when the user's level is uncertain or they asked to "see where I stand".
2. **Core learning**: courses or a path, ordered from their current level upward. Prefer a single existing learning path as the spine when one covers the goal — it is already sequenced by Pluralsight.
3. **Practice**: at least one hands-on lab if available for the topic. A plan with no hands-on work rarely sticks.
4. **Validation** (optional): a practice exam (for certification goals) or re-taking the Skill IQ to measure progress.

## Level progression

- Anchor the first core item at the user's inferred current level.
- Include at least one item at the next level up so the plan has progression, not repetition.
- Never jump two levels in adjacent items (beginner → advanced) without an intermediate step.

## Per-item requirements

For each item include:

- Title (exactly as it appeared in tool results — never invent or "correct" titles)
- Content type and level
- A one-line reason it is in the plan (what capability it builds toward the goal)

## Sequencing and sizing

- State what to do first and what can run in parallel (e.g. a lab alongside its companion course).
- Right-size to the user's timeframe. A plan they won't finish is a bad plan — cut items rather than compress them.
- Skip anything that appears in the user's recent activity unless they explicitly want to revisit it.
- Close by offering to adjust for a different timeframe or depth, or to turn the plan into a dated schedule (see `scripts/build_schedule.py` in the skill).
