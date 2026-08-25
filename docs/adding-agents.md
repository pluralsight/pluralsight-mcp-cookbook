# Adding Agents

Agents are specialized subagents with their own system prompt, tool restrictions, and context. They live in `plugins/pluralsight/agents/<agent-name>.md`.

Use an agent (instead of a skill) when the task is open-ended and research-heavy — the agent iterates in its own context and reports back a finished result. Use a skill when you're encoding a repeatable procedure into the current conversation.

## Format

```markdown
---
name: my-agent-name
description: What the agent does and when to delegate to it. The main assistant uses this to decide when to hand off.
tools: mcp__plugin_pluralsight_pluralsight__inferences___search_pluralsight_library, mcp__pluralsight__inferences___search_pluralsight_library
---

System prompt for the agent. Define:

- Its role and expertise.
- A concrete process (ordered steps naming exact tools).
- Rules and constraints (e.g. "only recommend content that appeared in
  tool results").
- The shape of its final report.
```

### Tool names

The fully-qualified name of an MCP tool depends on **how the server was configured**, so list each tool in both forms (only the matching set resolves at runtime):

| Setup | Prefix |
| --- | --- |
| Plugin install (the normal case) | `mcp__plugin_pluralsight_pluralsight__` |
| Manual `.mcp.json` server named `pluralsight` | `mcp__pluralsight__` |

The five available tool names to append to either prefix:

- `inferences___search_pluralsight_library`
- `inferences___query_pluralsight_content_index`
- `inferences___query_pluralsight_help_center_index`
- `inferences___get_user_content_activity`
- `inferences___submit_user_feedback`

Restrict `tools` to what the agent needs — see [learning-advisor.md](../plugins/pluralsight/agents/learning-advisor.md) for a working example. If you omit the `tools` field entirely, the agent inherits all tools (including every MCP tool), which also works but loses the restriction.

## Guidelines

- **Write the description for the delegator.** The main assistant reads it to decide when to hand work off — include example requests ("use for requests like ...").
- **Demand grounded output**: instruct the agent to only cite content returned by tools, never invented titles.
- **Define the report format** so results are usable without re-reading the agent's process.

## Test

```shell
claude --plugin-dir ./plugins/pluralsight
```

- Check the agent appears in `/context` under Custom Agents.
- Invoke it: "Use the my-agent-name agent to ...".
- Verify it only uses its allowed tools and its report matches the defined format.

## VS Code Copilot variant (optional)

Claude-format agents in `agents/` are the primary format. If an agent needs a Copilot-specific variant, VS Code's agent-plugins format reads `.agent.md` files from `com.github.copilot/agents/` in the plugin root — see the [VS Code agent plugins docs](https://code.visualstudio.com/docs/agent-customization/agent-plugins). Only add this if the Claude-format agent doesn't behave correctly in VS Code.

## Submit

Add a row to the agents table in [`plugins/pluralsight/README.md`](../plugins/pluralsight/README.md), then open a pull request.
