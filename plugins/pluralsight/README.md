# Pluralsight Plugin

Connects your AI coding assistant to the [Pluralsight MCP Server](https://mcp.pluralsight.com/mcp) and adds skills and an agent for working with Pluralsight learning content.

Installing this plugin configures the MCP server automatically — see [installation](../../docs/installation.md) for Claude Code and VS Code instructions. On first use you'll be prompted to authenticate with your Pluralsight account.

## What's included

### MCP server tools

| Tool | What it does |
| --- | --- |
| `search_pluralsight_library` | Find courses, labs, learning paths, Skill IQ assessments, and practice exams by topic, with level and sort filters |
| `query_pluralsight_content_index` | Semantic search over course clips and tutorial content, filtered to your licensed libraries |
| `query_pluralsight_help_center_index` | Search official Help Center articles (account, billing, subscriptions, platform support) |
| `get_user_content_activity` | Fetch your last 3 interactions across all Pluralsight content types |
| `submit_user_feedback` | Send structured feedback about the MCP server to Pluralsight |

### Skills

Skills trigger automatically when your request matches, or invoke them directly:

| Skill | Invoke | Use for |
| --- | --- | --- |
| [find-learning-content](skills/find-learning-content/SKILL.md) | `/pluralsight:find-learning-content <topic>` | Finding the right course, lab, path, or assessment |
| [learning-plan](skills/learning-plan/SKILL.md) | `/pluralsight:learning-plan <goal>` | Building a personalized, ordered study plan |
| [pluralsight-support](skills/pluralsight-support/SKILL.md) | `/pluralsight:pluralsight-support <question>` | Account, billing, and platform questions |

Skills follow the [Agent Skills specification](https://agentskills.io/specification.md). `learning-plan` bundles a [schedule script](skills/learning-plan/scripts/build_schedule.py) that turns a plan into dated weeks, plus [references](skills/learning-plan/references/plan-design.md) and an [output template](skills/learning-plan/assets/plan-template.md).

### Agents

| Agent | Use for |
| --- | --- |
| [learning-advisor](agents/learning-advisor.md) | Open-ended curriculum design — reviews your activity and builds a milestone-based learning plan toward a goal |

## Try it

After installing, ask things like:

- "Find me an intermediate course on Terraform"
- "/pluralsight:learning-plan become a Kubernetes administrator in 3 months"
- "How do I cancel my Pluralsight subscription?"

For a guided tour from simple prompts to full workflows, see the [examples](../../examples/README.md).
