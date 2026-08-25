# 02 — Intermediate

Prompts that combine multiple MCP tools in one request. The assistant chains tool calls and synthesizes the results.

| Example | Tools exercised |
| --- | --- |
| [What should I learn next?](what-to-learn-next.md) | `get_user_content_activity` + `search_pluralsight_library` |
| [Beginner-to-advanced course sequence](progressive-course-sequence.md) | `search_pluralsight_library` (multiple filtered calls) |
| [Deep-dive on a subtopic](deep-dive-subtopic.md) | `search_pluralsight_library` + `query_pluralsight_content_index` |
| [Assess then practice](assess-then-practice.md) | `search_pluralsight_library` (skilliq + lab) + `get_user_content_activity` |
