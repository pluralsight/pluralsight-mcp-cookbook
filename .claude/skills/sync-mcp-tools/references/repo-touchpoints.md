# Known repo touchpoints for the MCP tool list

This is a starting checklist of files known (as of the last time this skill was
updated) to name specific Pluralsight MCP tools, describe them, or state how
many there are. Treat it as a head start, not a guarantee — always confirm with
a fresh search (see SKILL.md step 4) because files get added or renamed.

As of the 2026-09-24 sync, the approved public tool list is 12 tools: the
original 7 (from the 2026-08-27 sync) plus `get_channel_details`,
`update_channel`, `assign_team_to_channel`, `analytics_explore`, and
`analytics_execute` — resolving the gap flagged below from that earlier
sync. The live server also exposes an `inferences-sandbox` namespace (topic
extraction, learning digests, `record_learning_opportunity`,
`sandbox_ping`, etc.) that remains deliberately excluded as
experimental/dev-only — don't silently start documenting those without
re-running Stage 2.

**Leader-only access, worth checking on every future sync:** `assign_team_to_channel`,
`analytics_explore`, and `analytics_execute` are fully leader-only (they operate
on the leader's team / the leader-analytics API). `create_channel` and
`update_channel` are available to all users, but their `enable_analytics`
parameter is leader-only. Every doc touchpoint below now carries an
"Access" column or inline "(leader only)" marker — keep that distinction
when adding new tools, since not all users can see or use these.

**Resolved (2026-09-24, same-day follow-up):** worked examples now exist for
all 5 tools, live-tested against the real server with a leader-access
account: `get-channel-details.md` and `update-a-channel.md`
(`examples/01-getting-started/`, available to any account), plus
`assign-a-channel-to-your-team.md` (`examples/01-getting-started/`, leader
only — tested live with `send_notification_email: false` to avoid emailing
a real team) and `check-team-channel-analytics.md`
(`examples/02-intermediate/`, leader only — chains `analytics_explore` +
`analytics_execute`). Example content uses generic placeholder
names/values, not the real account data used to test them, per the
"don't hardcode course titles" / no-PII convention.

**Resolved from the previous sync's flag:** Stage 1's tool search on
2026-08-27 only surfaced 12 tools total and missed the 5 tools above, which
turned up later, unprompted, in an unrelated part of that session. This
sync's Stage 1 found all 5 directly via a generous keyword search plus a
follow-up family search (channel/analytics/team/leader terms) that
confirmed no further undiscovered tools exist.

## Tables listing every tool (name + description + access)

- `README.md` — "MCP server tools" table, now with an "Access" column marking leader-only tools.
- `plugins/pluralsight/README.md` — "MCP server tools" table under "What's included", same "Access" column.

## Prose that names the tools or asserts a count

As of this sync the count is 12 (see the top of this file). Update the count word/number in each of these whenever it changes:

- `docs/adding-examples.md` — "Rules" section: "Only use the documented tools: `search_pluralsight_library`, ...".
- `docs/adding-skills.md` — "Guidelines" section: "Only reference the 12 documented tools (see plugin README)".
- `docs/adding-agents.md` — "Tool names" section: bullet list of "The 12 available tool names to append to either prefix", with leader-only ones marked inline.
- `CONTRIBUTING.md` — "Ground rules": "Use only the documented tools: ...".
- `.github/PULL_REQUEST_TEMPLATE.md` — checklist item "Uses only the 12 documented MCP tools".
- `.github/ISSUE_TEMPLATE/example_proposal.md` — tool list comment + "12 documented MCP tools" checkbox.

## Skill and agent files that call specific tools

- `plugins/pluralsight/skills/find-learning-content/SKILL.md` — names `search_pluralsight_library` and `query_pluralsight_content_index`, explains when to use each.
- `plugins/pluralsight/skills/find-learning-content/references/search-parameters.md` — parameter tables for `search_pluralsight_library`.
- `plugins/pluralsight/skills/learning-plan/SKILL.md` and its `references/*.md` — likely calls multiple tools; check for tool names and parameter tables.
- `plugins/pluralsight/skills/pluralsight-support/SKILL.md` — names `query_pluralsight_help_center_index` and `submit_user_feedback`.
- `plugins/pluralsight/agents/learning-advisor.md` — frontmatter `tools:` field lists fully-qualified tool names in two prefix forms; body may also narrate tool use.

## Examples that demonstrate a tool

- `examples/01-getting-started/*.md` — each is built around one tool. Includes `list-channels.md` (added 2026-08-27); `get-channel-details.md`, `update-a-channel.md`, and `assign-a-channel-to-your-team.md` (added 2026-09-24, the last is leader only).
- `examples/02-intermediate/*.md` — each chains multiple tools. Includes `build-a-learning-path.md` (added 2026-08-27, chains `search_pluralsight_library` + `create_channel`); `check-team-channel-analytics.md` (added 2026-09-24, chains `analytics_explore` + `analytics_execute`, leader only).
- `examples/03-advanced/*.md` — uses tools via skills/agents, may not name them directly.

## Other

- `.claude-plugin/marketplace.json` and `plugins/pluralsight/.claude-plugin/plugin.json` — version numbers; bump if tool surface changes materially.
- `CONTRIBUTING.md` — check for any tool-count or tool-list mentions.

None of these are a substitute for grepping the repo fresh — new examples or a
new skill may exist that this list hasn't caught up with yet.
