# Learn From Your Codebase

**Goal:** Combine your assistant's view of the code you're working on with Pluralsight search to close skill gaps that actually matter for your project.

## Prompt

Run this inside a real project in Claude Code or VS Code:

```text
Look at this repository's tech stack and the parts of the codebase I've been
changing recently (check git history for my commits). Identify the 2-3
technologies where deeper knowledge would help me most, then find Pluralsight
content for each - specific clips for quick wins and a course for the
biggest gap.
```

## Tools used

- Your assistant's built-in code and git tools — to detect the stack and your recent work.
- `search_pluralsight_library` — course/lab recommendations per identified gap.
- `query_pluralsight_content_index` — specific clips for narrow, immediately-useful topics.

## What to expect

Recommendations tied to evidence from your own repo ("your recent commits touch the Terraform modules but follow older patterns — this course covers the current approach"). This is the pattern that makes an MCP-connected assistant more useful than the Pluralsight website: it knows what you're building.
