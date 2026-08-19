# Search the Library

**Goal:** Find Pluralsight content on a topic — the most common starting point.

## Prompt

```text
Search Pluralsight for beginner courses on Python.
```

Variations:

```text
Find the most popular hands-on labs for Docker.
```

```text
Are there any learning paths for AWS certification? Show me the newest ones.
```

## Tools used

- `search_pluralsight_library` — the assistant should map your wording to parameters: "beginner" → `levels: ["beginner"]`, "labs" → `content_type: "lab"`, "learning paths" → `content_type: "path"`, "most popular" → `sort: "popularity"`, "newest" → `sort: "newest"`.

## What to expect

A short list of matching content with titles, content types, and levels. Ask follow-ups like "only show intermediate ones" or "which should I take first?" — the assistant will re-search with different filters.
