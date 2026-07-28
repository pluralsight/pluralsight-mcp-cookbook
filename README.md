# Pluralsight MCP Cookbook

Worked examples for the [Pluralsight MCP server](https://mcp.pluralsight.com/mcp) — prompts,
and Agent Skills and subagents built on top of them.

Works with **Claude Code**, **Claude Desktop**, and **VS Code Copilot**. Some of it installs;
all of it reads as reference.

```bash
claude mcp add --transport http --scope user pluralsight https://mcp.pluralsight.com/mcp
```

Full setup for all three tools, including Desktop and Copilot: **[docs/setup.md](docs/setup.md)**.

## What's here

| | |
| --- | --- |
| **[prompts/](prompts/)** | Copy-paste examples, single-shot → scoped → multi-step. Start here. |
| **[docs/tools-reference.md](docs/tools-reference.md)** | The five tools, their parameters, and the response quirks that matter. |
| **[plugins/pluralsight-learning/](plugins/pluralsight-learning/)** | The installable plugin — one skill so far. |
| **[docs/setup.md](docs/setup.md)** | Setup and the per-tool support matrix. |
| **[internal/](internal/)** | The validator and the maintainer authoring guide. Not for customers. |

## The content

**[`team-learning-plan`](plugins/pluralsight-learning/skills/team-learning-plan/SKILL.md)** —
for a manager, not the learner: turns a report's Job Description and Midyear Performance Review
into a 6-month development plan, mapping the gaps between the two to real Pluralsight courses
and clips, with a 30/60/90-day milestone timeline and success criteria.

## Install (Claude Code)

```
/plugin marketplace add pluralsight/pluralsight-mcp-cookbook
/plugin install pluralsight-learning@pluralsight-mcp-cookbook
/reload-plugins
```

Skills load automatically when a request matches, or invoke one directly:

```
/pluralsight-learning:team-learning-plan
```

**Claude Desktop** has no plugin support; use the prompts directly and paste skill bodies into
a Project. **VS Code Copilot** picks up the skills from the committed workspace setting, or copy
them into your own `.github/skills/`. Both paths are in [docs/setup.md](docs/setup.md).

## Notes

Everything here uses the five generally available tools only, so the examples don't break when
tools in development change.

Results are scoped to the libraries your Pluralsight license covers — thin results usually mean
license scope rather than a gap in the library.

Contributions: [CONTRIBUTING.md](CONTRIBUTING.md) · See [LICENSE](LICENSE).
