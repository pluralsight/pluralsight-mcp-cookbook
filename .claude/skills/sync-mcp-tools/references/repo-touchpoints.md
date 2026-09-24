# Known repo touchpoints for the MCP tool list

This is a starting checklist of files known (as of the last time this skill was
updated) to name specific Pluralsight MCP tools, describe them, or state how
many there are. Treat it as a head start, not a guarantee — always confirm with
a fresh search (see SKILL.md step 4) because files get added or renamed.

As of the 2026-08-27 sync, the approved public tool list is 7 tools: the
original 5 plus `list_channels` and `create_channel` (a write tool). The
live server also exposes an `inferences-sandbox` namespace (topic
extraction, learning digests, `record_learning_opportunity`,
`sandbox_ping`, etc.) that was deliberately excluded as experimental/dev-only
— don't silently start documenting those without re-running Stage 2.

**Known incomplete spot from that sync:** Stage 1's tool search that day only
surfaced 12 tools total and never found `get_channel_details`,
`update_channel`, `assign_team_to_channel`, `analytics_execute`, or
`analytics_explore` — all of which turned up later, unprompted, in an
unrelated part of the same session. These are almost certainly live on the
server right now and were never presented to the user for a Stage 2
include/exclude call. The next sync should search for these by name
specifically (don't assume a plain keyword search will surface them) and
treat this as unfinished business, not a hypothetical.

## Tables listing every tool (name + description)

- `README.md` — "MCP server tools" table.
- `plugins/pluralsight/README.md` — "MCP server tools" table under "What's included".

## Prose that names the tools or asserts a count

- `docs/adding-examples.md` — "Rules" section: "Only use the documented tools: `search_pluralsight_library`, ...".
- `docs/adding-skills.md` — "Guidelines" section: "Only reference the seven documented tools (see [plugin README](...))".
- `docs/adding-agents.md` — "Tool names" section: bullet list of "The seven available tool names to append to either prefix".
- `CONTRIBUTING.md` — "Ground rules": "Use only the documented tools: ...".
- `.github/PULL_REQUEST_TEMPLATE.md` — checklist item "Uses only the seven documented MCP tools".
- `.github/ISSUE_TEMPLATE/example_proposal.md` — tool list comment + "seven documented MCP tools" checkbox.

## Skill and agent files that call specific tools

- `plugins/pluralsight/skills/find-learning-content/SKILL.md` — names `search_pluralsight_library` and `query_pluralsight_content_index`, explains when to use each.
- `plugins/pluralsight/skills/find-learning-content/references/search-parameters.md` — parameter tables for `search_pluralsight_library`.
- `plugins/pluralsight/skills/learning-plan/SKILL.md` and its `references/*.md` — likely calls multiple tools; check for tool names and parameter tables.
- `plugins/pluralsight/skills/pluralsight-support/SKILL.md` — names `query_pluralsight_help_center_index` and `submit_user_feedback`.
- `plugins/pluralsight/agents/learning-advisor.md` — frontmatter `tools:` field lists fully-qualified tool names in two prefix forms; body may also narrate tool use.

## Examples that demonstrate a tool

- `examples/01-getting-started/*.md` — each is built around one tool. Includes `list-channels.md` (added 2026-08-27).
- `examples/02-intermediate/*.md` — each chains multiple tools. Includes `build-a-learning-path.md` (added 2026-08-27, chains `search_pluralsight_library` + `create_channel`).
- `examples/03-advanced/*.md` — uses tools via skills/agents, may not name them directly.

## Other

- `.claude-plugin/marketplace.json` and `plugins/pluralsight/.claude-plugin/plugin.json` — version numbers; bump if tool surface changes materially.
- `CONTRIBUTING.md` — check for any tool-count or tool-list mentions.

None of these are a substitute for grepping the repo fresh — new examples or a
new skill may exist that this list hasn't caught up with yet.
