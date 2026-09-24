# List Your Channels

**Goal:** See the learning channels (paths) you own or edit as a leader.

## Prompt

```text
What learning channels do I currently own on Pluralsight?
```

Variations:

```text
List my Pluralsight channels.
```

## Tools used

- `list_channels` — takes no parameters; returns each channel you own or edit with its `channel_id`, `name`, and `description`.

## What to expect

A list of your channels by name and description. If you don't own or edit any channels, expect an empty result — that's normal for individual-contributor accounts. This is a good precondition check before asking the assistant to build a new channel with `create_channel`, since you'll want to know what already exists first.
