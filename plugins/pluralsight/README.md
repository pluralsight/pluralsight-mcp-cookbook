# Pluralsight Plugin

Connects your AI coding assistant to the [Pluralsight MCP Server](https://mcp.pluralsight.com/mcp) and adds skills and an agent for working with Pluralsight learning content.

Installing this plugin configures the MCP server automatically — see [installation](../../docs/installation.md) for Claude Code and VS Code instructions. On first use you'll be prompted to authenticate with your Pluralsight account.

## What's included

### MCP server tools

| Tool | What it does | Access |
| --- | --- | --- |
| `search_pluralsight_library` | Find courses, labs, learning paths, Skill IQ assessments, and practice exams by topic, with level and sort filters | All users |
| `query_pluralsight_content_index` | Semantic search over course clips and tutorial content, filtered to your licensed libraries | All users |
| `query_pluralsight_help_center_index` | Search official Help Center articles (account, billing, subscriptions, platform support) | All users |
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
