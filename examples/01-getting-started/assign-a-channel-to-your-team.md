# Assign a Channel to Your Team

> **Leader only.** This tool requires a Pluralsight leader/team-management plan. If you don't manage a team, this prompt will error rather than return results.

**Goal:** Give your whole team viewer access to a learning path in one step, with an optional heads-up email.

## Prompt

```text
Assign my "Onboarding" channel to my team, with a note telling them to
finish it by the end of the month.
```

Variations:

```text
Add my team as viewers on channel <channel_id>, but don't send them an email.
```

## Tools used

- `list_channels` — resolve the channel name to a `channel_id` first, if you only know it by name.
- `assign_team_to_channel` — with `channel_id` and `instructions` (the message included in the notification email). Your team is resolved automatically from your leader plan; if you manage more than one team, the tool tells you your teams so you can pick one. Set `send_notification_email: false` to skip the email.

## What to expect

Every member of the resolved team gets viewer access to the channel. Unless you set `send_notification_email: false`, each of them also gets an email containing your `instructions` — the assistant should confirm the exact wording with you before sending, since this reaches real people. If you manage more than one team, expect a follow-up question asking which one to use.
