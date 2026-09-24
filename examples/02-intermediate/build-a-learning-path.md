# Build a Learning Path

**Goal:** Turn a search for relevant content into a new learning channel your team can follow.

## Prompt

```text
Find an intermediate learning path on Kubernetes, plus a couple of
hands-on labs to go with it, then create a channel called "Kubernetes
Ramp-Up" from those.
```

## Tools used

1. `search_pluralsight_library` with `content_type: "path"` and `levels: ["intermediate"]` — find the core path.
2. `search_pluralsight_library` with `content_type: "lab"` — find supporting hands-on labs.
3. `create_channel` with the resulting content ids, in the order learners should work through them.

## What to expect

The assistant should present the proposed channel — name, description, and ordered content list — and ask you to confirm before calling `create_channel`; it's a write tool that creates a real channel in your organization. Content ids only ever come from what `search_pluralsight_library` actually returned, never invented. After confirmation, you'll get the new channel back; use [List Your Channels](../01-getting-started/list-channels.md) to verify it.
