# Pluralsight MCP Cookbook

Prompts, skills, and agents for the **Pluralsight MCP Server** — connect your AI assistant to Pluralsight to search the learning library, build personalized learning plans, and get platform support without leaving your editor.

The [Pluralsight MCP Server](https://mcp.pluralsight.com/mcp) exposes tools to search courses, labs, paths, and assessments; find specific tutorial clips; check your learning activity; search Help Center docs; and send feedback. This cookbook shows how to use them, from single prompts to full agent workflows.

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

## MCP server tools

| Tool | What it does |
| --- | --- |
| `search_pluralsight_library` | Find courses, labs, learning paths, Skill IQ assessments, and practice exams, with level and sort filters |
| `query_pluralsight_content_index` | Semantic search over course clips and tutorial content |
| `query_pluralsight_help_center_index` | Search official Help Center articles (account, billing, platform) |
| `get_user_content_activity` | Fetch your last 3 interactions across all Pluralsight content types |
| `submit_user_feedback` | Send structured feedback about the MCP server to Pluralsight |

## Contributing

We welcome new examples, skills, and agents — see [CONTRIBUTING.md](CONTRIBUTING.md). Skills follow the open [Agent Skills specification](https://agentskills.io/specification.md); [`learning-plan`](plugins/pluralsight/skills/learning-plan/SKILL.md) is the reference implementation.

## Feedback

The fastest way to reach the team building the MCP server is through the server itself: ask your assistant to *"send feedback about the Pluralsight MCP server"* ([example](examples/01-getting-started/send-feedback.md)). For issues with this cookbook, open a GitHub issue.

## License

[MIT](LICENSE)
