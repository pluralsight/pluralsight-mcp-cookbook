# Pluralsight MCP Cookbook

Prompts, skills, and agents for the **Pluralsight MCP Server** — connect your AI assistant to Pluralsight to search the learning library, build personalized learning plans, and get platform support without leaving your editor.

The [Pluralsight MCP Server](https://mcp.pluralsight.com/mcp) exposes tools to search courses, labs, paths, and assessments; find specific tutorial clips; check your learning activity; search Help Center docs; manage learning paths (channels); pull team analytics; and send feedback. This cookbook shows how to use them, from single prompts to full agent workflows. Some tools — team analytics and assigning channels to a team — require a Pluralsight leader account and won't appear for every user.

## Quick start

### Claude Code

```shell
/plugin marketplace add pluralsight/pluralsight-mcp-cookbook
/plugin install pluralsight@pluralsight
```

### VS Code (GitHub Copilot)

Add to your settings, then install **pluralsight** from the Extensions view (`@agentPlugins`):

```json
"chat.plugins.marketplaces": ["pluralsight/pluralsight-mcp-cookbook"]
```

Installing the plugin configures the MCP server, three skills, and a learning-advisor agent. Authenticate with your Pluralsight account on first use. Full instructions (including MCP-only setup without the plugin): [docs/installation.md](docs/installation.md).

### Try it

```text
What have I been learning on Pluralsight recently?
```

```text
Find me an intermediate course on Terraform.
```

```text
/pluralsight:learning-plan become a Kubernetes administrator in 3 months
```

## What's in this repo

| | |
| --- | --- |
| [`plugins/pluralsight/`](plugins/pluralsight/README.md) | The installable plugin: MCP server config, skills, and agents |
| [`examples/01-getting-started/`](examples/01-getting-started/README.md) | Single-tool prompts — start here |
| [`examples/02-intermediate/`](examples/02-intermediate/README.md) | Multi-tool prompts and patterns |
| [`examples/03-advanced/`](examples/03-advanced/README.md) | Skill- and agent-driven workflows |
| [`docs/`](docs/installation.md) | Installation and contributor guides |
| [`docs/agent-integration-guidelines.md`](docs/agent-integration-guidelines.md) | Copy-paste system-prompt guidance for wiring the MCP server into your own agent on any platform |

## MCP server tools

| Tool | What it does | Access |
| --- | --- | --- |
| `search_pluralsight_library` | Find courses, labs, learning paths, Skill IQ assessments, and practice exams, with level and sort filters | All users |
| `query_pluralsight_content_index` | Semantic search over course clips and tutorial content | All users |
| `query_pluralsight_help_center_index` | Search official Help Center articles (account, billing, platform) | All users |
| `get_user_content_activity` | Fetch your last 3 interactions across all Pluralsight content types | All users |
| `list_channels` | List the learning channels (paths) the current user owns, edits, or views | All users |
| `create_channel` | Create a new learning path (channel) from real library content ids (`enable_analytics` requires a leader account) | All users |
| `get_channel_details` | Get a channel's full content list and item count | All users |
| `update_channel` | Update a channel's title/description or append content (`enable_analytics` requires a leader account) | All users |
| `assign_team_to_channel` | Assign your team to a channel as viewers, with a notification email | **Leader only** |
| `analytics_explore` | Discover available leader-analytics queries and their filters/fields | **Leader only** |
| `analytics_execute` | Run a leader-analytics query and get rows back | **Leader only** |
| `submit_user_feedback` | Send structured feedback about the MCP server to Pluralsight | All users |

Tools marked **Leader only** require a Pluralsight leader/team-management plan — they won't be available or return results for other accounts.

## Contributing

We welcome new examples, skills, and agents — see [CONTRIBUTING.md](CONTRIBUTING.md). Skills follow the open [Agent Skills specification](https://agentskills.io/specification.md); [`learning-plan`](plugins/pluralsight/skills/learning-plan/SKILL.md) is the reference implementation.

## Feedback

The fastest way to reach the team building the MCP server is through the server itself: ask your assistant to *"send feedback about the Pluralsight MCP server"* ([example](examples/01-getting-started/send-feedback.md)). For issues with this cookbook, open a GitHub issue.

## License

[MIT](LICENSE)
