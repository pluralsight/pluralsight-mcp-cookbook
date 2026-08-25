---
name: pluralsight-support
description: Answer questions about the Pluralsight platform, accounts, billing, subscriptions, and features using official Help Center documentation. Use when the user asks how Pluralsight works, has an account or billing question, or needs platform support.
license: MIT
metadata:
  author: Pluralsight
  version: "1.0"
---

# Pluralsight Support

Answer the user's Pluralsight platform question using official Help Center documentation. The question is: "$ARGUMENTS" (if empty, ask what they need help with).

## How to answer

1. Call `query_pluralsight_help_center_index` with a query phrased as the underlying question (for example "how to cancel a subscription" rather than the user's full sentence). Use the default `result_count` of 5; raise it up to 10 for broad or ambiguous questions.
2. Answer from the returned articles only. Do not answer platform, billing, or account questions from general knowledge — policies and features change.
3. Cite which Help Center article the answer comes from, and include links when the results provide them.
4. If the articles don't cover the question, say so plainly and suggest contacting Pluralsight Support directly rather than guessing.

## Scope notes

- This tool covers account management, billing, subscription details, and platform support topics.
- For questions about finding courses or learning content, use the library search tools instead of the Help Center index.
- If the user reports a problem with the MCP server itself (broken tools, missing capabilities), offer to record it with `submit_user_feedback`.
