# Installation

Two ways to use this cookbook:

1. **Install the plugin** (recommended) — one step configures the MCP server, skills, and agent.
2. **Manual MCP setup** — connect only the MCP server, no skills/agents.

Either way, on first tool use you'll be prompted to authenticate with your Pluralsight account.

## Claude Code

Add this repo as a plugin marketplace, then install the plugin:

```shell
/plugin marketplace add pluralsight/pluralsight-mcp-cookbook
/plugin install pluralsight@pluralsight
```

If the install summary says `Run /reload-plugins to activate.`, run `/reload-plugins`.

Verify:

- `/mcp` — the `pluralsight` server is listed (complete authentication if prompted).
- `/pluralsight:find-learning-content python` — the skill runs and returns courses.
- `/context` — `learning-advisor` appears under Custom Agents.

## VS Code (GitHub Copilot)

VS Code supports the Claude plugin format natively via [agent plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins). Requires the `chat.plugins.enabled` setting.

1. Add this repo as a plugin marketplace in your settings:

   ```json
   "chat.plugins.marketplaces": [
     "pluralsight/pluralsight-mcp-cookbook"
   ]
   ```

2. Open the Extensions view, search `@agentPlugins`, and install **pluralsight** (or use the Agent Customizations editor).

The plugin's MCP server is trusted on install; skills are available to the agent automatically.

## Manual MCP setup (without the plugin)

### Claude Code

```shell
claude mcp add --transport http pluralsight https://mcp.pluralsight.com/mcp
```

### VS Code

Add to `.vscode/mcp.json` in your workspace (or run **MCP: Add Server**):

```json
{
  "servers": {
    "pluralsight": {
      "type": "http",
      "url": "https://mcp.pluralsight.com/mcp"
    }
  }
}
```

### Other MCP clients

Any client supporting streamable HTTP transport can connect to `https://mcp.pluralsight.com/mcp`.

## Troubleshooting

- **Authentication errors**: run the [check-recent-activity example](../examples/01-getting-started/check-recent-activity.md) — it's the quickest end-to-end auth test. Re-authenticate via your client's MCP management UI (`/mcp` in Claude Code).
- **Skills not appearing** (Claude Code): run `/reload-plugins`, then check `/help` → Custom commands.
- **Plugin errors** (Claude Code): check the `/plugin` manager's Errors tab.
- **Something else**: use the [send-feedback example](../examples/01-getting-started/send-feedback.md) to report it to the Pluralsight team.
