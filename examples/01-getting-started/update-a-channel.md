# Update a Channel

**Goal:** Refresh a channel's description or add newly-found content to it, without disturbing what's already there.

## Prompt

```text
Update the description on my "Kubernetes Ramp-Up" channel to mention it now
covers Helm, and add the intermediate Helm course we just found.
```

Variations:

```text
Rename my "Onboarding" channel to "Q1 Onboarding" — leave everything else alone.
```

## Tools used

- `get_channel_details` — check what's already in the channel first, to avoid duplicates and confirm there's room under the 200-item cap.
- `search_pluralsight_library` — find the new content id, if adding content.
- `update_channel` — with `channel_id` and any combination of `title`, `description`, and `content_to_add`. Content is always appended to the end; existing content is never replaced, removed, or reordered.

## What to expect

The assistant should confirm the proposed changes with you before calling `update_channel` — it's a write tool that edits a real channel. The response lists which fields were updated and how many content items were added; anything the tool couldn't add (practice exams, hands-on content that isn't a lab, or an id already in the channel) comes back in `skipped_content` with the reason, which the assistant should relay to you. Removing or reordering content, and deleting the channel itself, aren't supported here — the assistant should point you to the Pluralsight UI for those. Note: the `enable_analytics` option on this tool requires a leader account; everything else works for any channel editor or owner.
