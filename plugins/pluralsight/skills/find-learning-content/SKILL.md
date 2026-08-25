---
name: find-learning-content
description: Search Pluralsight for courses, labs, paths, assessments, or specific tutorial content. Use when the user wants to find learning material on a topic, technology, or skill, or asks "is there a Pluralsight course on X".
license: MIT
metadata:
  author: Pluralsight
  version: "1.0"
---

# Find Learning Content

Help the user find the most relevant Pluralsight content for what they want to learn. The topic to search for is: "$ARGUMENTS" (if empty, ask the user what they want to learn).

## Choosing the right tool

Two Pluralsight MCP tools search for content — pick based on what the user needs:

- **`search_pluralsight_library`** — catalog search. Use when the user wants whole pieces of content: courses, hands-on labs, learning paths, Skill IQ assessments, or practice exams. Supports filtering and sorting.
- **`query_pluralsight_content_index`** — semantic search over course clips and tutorial content. Use when the user has a specific question or narrow subtopic (for example "how do I configure OAuth in ASP.NET Core") and wants the exact clip or module that covers it. Results are automatically filtered to the user's licensed libraries.

For broad requests, start with `search_pluralsight_library`. If the user follows up with a specific "how do I..." question, switch to `query_pluralsight_content_index`.

## Using search_pluralsight_library effectively

Set `sort` (required — `"relevance"` by default) and add `content_type` / `levels` filters when the user's phrasing indicates a format or experience level. Full parameter values and phrasing-to-parameter mappings: [references/search-parameters.md](references/search-parameters.md).

## Presenting results

- Group results by content type when mixed (courses, labs, paths).
- For each result, state the title, level (if available), and one line on why it fits the request.
- If results look off-topic, refine the query and search again rather than presenting weak matches.
- Offer a next step: take a Skill IQ to gauge level, start with a path for structured learning, or a lab for hands-on practice.
