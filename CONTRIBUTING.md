# Contributing

Thanks for helping make the Pluralsight MCP Cookbook better. Contributions land as pull requests against `main`.

## What to contribute

| Contribution | Guide |
| --- | --- |
| A new prompt example | [docs/adding-examples.md](docs/adding-examples.md) |
| A new skill | [docs/adding-skills.md](docs/adding-skills.md) |
| A new agent | [docs/adding-agents.md](docs/adding-agents.md) |

## Ground rules

- **Test against the live server.** Every prompt, skill, and agent must work against `https://mcp.pluralsight.com/mcp` as written.
- **Use only the documented tools**: `search_pluralsight_library`, `query_pluralsight_content_index`, `query_pluralsight_help_center_index`, `get_user_content_activity`, `list_channels`, `create_channel`, `get_channel_details`, `update_channel`, `assign_team_to_channel`, `analytics_explore`, `analytics_execute`, `submit_user_feedback`. `assign_team_to_channel`, `analytics_explore`, and `analytics_execute` are leader-only — test them with a leader account.
- **Never commit credentials.** Local MCP configs with tokens (like a root `.mcp.json`) are gitignored — keep it that way. The plugin's bundled [`plugins/pluralsight/.mcp.json`](plugins/pluralsight/.mcp.json) must contain only the server URL.
- **Follow the Agent Skills spec** for skills — `SKILL.md` plus optional `scripts/`, `references/`, and `assets/`. Bundled scripts declare their dependencies inline (PEP 723), run via `uv run`, and must be non-interactive with `--help` output. Details in [docs/adding-skills.md](docs/adding-skills.md).
- **Don't hardcode course titles.** The catalog changes; let the tools return results.
- **Validate plugin changes** before submitting:

  ```shell
  claude plugin validate ./plugins/pluralsight
  uvx --from skills-ref agentskills validate ./plugins/pluralsight/skills/<skill-name>
  ```

- **Update the indexes**: new examples go in their level's `README.md` table; new skills/agents go in the [plugin README](plugins/pluralsight/README.md) tables.

## Requesting MCP server features

This repo covers the cookbook content, not the MCP server itself. For server feature requests or bugs, use the `submit_user_feedback` tool ([example](examples/01-getting-started/send-feedback.md)) — it goes straight to the team building the server.
