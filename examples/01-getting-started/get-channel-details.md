# Inspect a Channel

**Goal:** See everything inside one of your learning channels before editing it.

## Prompt

```text
What's in my "Kubernetes Ramp-Up" channel?
```

Variations:

```text
Show me the content list for channel <channel_id>.
```

## Tools used

- `get_channel_details` — takes a `channel_id` (resolve it first with `list_channels` if you only know the channel by name); returns the channel's ordered `content` list, each item's `content_id`, `content_type`, and `title`, plus `content_count`.

## What to expect

An ordered list of everything in the channel — courses, labs, and any other content types it holds — with a total count. Channels cap out at 200 items, so `content_count` is also a quick way to check how much room is left before calling `update_channel` to add more. This is a good precondition check before `update_channel`, since it shows you exactly what's already there so you don't add duplicates.
