# Check Your Recent Activity

**Goal:** See what you were last working on across Pluralsight — and verify the server is connected to *your* account.

## Prompt

```text
What have I been learning on Pluralsight recently?
```

Variations:

```text
What was the last course I was watching? Where did I leave off?
```

## Tools used

- `get_user_content_activity` — takes no parameters; returns your **last 3 interactions** across all content types (video courses, ILX experiences, assessments, Skill IQ scores, paths, code labs, cloud labs, sandboxes).

## What to expect

A summary of your 3 most recent learning interactions — a snapshot of where you left off, not your full history, so don't be surprised when older activity doesn't appear. This is a good first test after installing: if it returns your actual courses, authentication is working. If you see an auth error, re-run the connection flow in [installation](../../docs/installation.md).
