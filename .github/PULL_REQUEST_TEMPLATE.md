## What this changes

<!-- One or two lines. Link any related issue. -->

## Type of change

- [ ] New prompt example
- [ ] New or updated skill
- [ ] New or updated agent
- [ ] Docs
- [ ] Repo tooling / CI

## How you tested it

<!-- The prompt you ran and what the assistant did. For skills and agents, note
     whether you tested direct invocation, auto-triggering, or both. -->

```text

```

## Checklist

- [ ] Tested against the live server (`https://mcp.pluralsight.com/mcp`) as written
- [ ] Uses only the five documented MCP tools
- [ ] No credentials committed — the bundled `plugins/pluralsight/.mcp.json` still contains only the server URL
- [ ] No hardcoded course titles (the catalog changes; let the tools return results)
- [ ] `claude plugin validate ./plugins/pluralsight` passes
- [ ] Skill changes: `uvx --from skills-ref agentskills validate <skill-dir>` passes, and any `scripts/` are non-interactive with `--help` output
- [ ] Indexes updated — new examples added to their level's `README.md` table; new skills/agents added to the [plugin README](../plugins/pluralsight/README.md) tables
- [ ] Relative links resolve
