# Deep-Dive on a Subtopic

**Goal:** Find a full course on a topic AND the exact clips covering the specific part you care about.

## Prompt

```text
I need to learn React state management, specifically React Query. Find me a
solid course on React state management, and also find the specific clips or
modules that cover React Query so I can jump straight to them.
```

## Tools used

1. `search_pluralsight_library` — catalog search for the broad topic (React state management courses).
2. `query_pluralsight_content_index` — semantic clip search for the narrow subtopic (React Query).

## What to expect

A two-part answer: a recommended course for structured learning, plus direct pointers to the clips/modules on your specific subtopic. This pattern — **broad catalog search plus narrow semantic search** — is the fastest way to unblock yourself mid-project while still finding proper learning material.
