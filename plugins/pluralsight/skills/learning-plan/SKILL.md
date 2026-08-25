---
name: learning-plan
description: Build a personalized Pluralsight learning plan based on the user's recent activity and goals. Use when the user asks what to learn next, wants a study plan or curriculum, or wants to level up in a technology.
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

Call `search_pluralsight_library` one or more times to gather content for the plan:

- Search with `sort: "relevance"` and the goal as the query.
- Use `levels` filters to match their inferred level, and run a second search at the next level up so the plan has progression.
- Search with `content_type: "path"` first — an existing learning path may already cover the goal. Supplement with `"video-course"`, `"lab"`, and `"skilliq"` searches to fill gaps.

## Step 3: Assemble the plan

Present an ordered plan with 3–7 items:

1. **Baseline** (optional): a Skill IQ assessment to measure their starting point.
2. **Core learning**: courses or a path, ordered from their current level upward.
3. **Practice**: at least one hands-on lab if available for the topic.
4. **Validation** (optional): a practice exam or re-taking the Skill IQ to measure progress.

For each item include the title, content type, level, and a one-line reason it is in the plan. Estimate a realistic sequence (what to do first, what can be parallel). Close by offering to adjust the plan for a different timeframe or depth.
