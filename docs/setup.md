# Setup

Two separate things to set up, in this order:

1. **The Pluralsight MCP server** — required for everything here. Without it, nothing in this
   repo has any tools to call.
2. **This repo's content** — optional, and how you install it depends on your tool.

Sign in with the Pluralsight account tied to your team's license. Authenticating with a
different or unlicensed account connects successfully but returns little or no content.

If your organization filters outbound traffic, IT may need to allow `mcp.pluralsight.com` before login will complete.

---

## Support matrix

| | Claude Code | Claude Desktop | VS Code Copilot |
| --- | --- | --- | --- |
| Pluralsight MCP server | ✅ | ✅ (admin-added connector) | ✅ |
| Skills | ✅ installed via plugin | ⚠️ copy/paste only | ✅ via workspace setting |
| Subagent | ✅ plugin mechanism, none published yet | ❌ | ❌ |
| Prompts in `prompts/` | ✅ | ✅ | ✅ |

Prompts work everywhere because they're just text. Skills degrade to copy/paste on Desktop.
The subagent mechanism is Claude Code only.

---

## Claude Code

**Step 1 — add the server** (once per machine):

```bash
claude mcp add --transport http --scope user pluralsight https://mcp.pluralsight.com/mcp
```

`--scope user` makes it available in every project. Without it the server is registered only
for the directory you ran the command in.

Start `claude` and a browser window opens for login on first use.

The server name you choose here — `pluralsight` above — becomes the prefix on every tool name
(`mcp__pluralsight__search_pluralsight_library`). Run `/mcp` to see the names your install
produced.

> **If your organization manages Claude Code centrally** (Intune, Jamf, GPO, or server-managed
> settings), `claude mcp add` is rejected with `enterprise MCP configuration is active and has
> exclusive control over MCP servers` until an admin permits Pluralsight in the managed policy.
> See [Control MCP server access for your organization](https://code.claude.com/docs/en/managed-mcp).

**Step 2 — install this repo's content:**

```
/plugin marketplace add pluralsight/pluralsight-mcp-cookbook
/plugin install pluralsight-learning@pluralsight-mcp-cookbook
/reload-plugins
```

Skills load automatically when a request matches, or invoke one directly:

```
/pluralsight-learning:team-learning-plan
```

To pull updates later: `/plugin marketplace update pluralsight-mcp-cookbook`.

---

## Claude Desktop

Desktop, claude.ai, and Cowork share one setup path, and it differs from Claude Code in a way
that matters: **there is no plugin marketplace and no skill or subagent installation.**

**Step 1 — an admin adds the connector.** Requires a Claude Team or Enterprise plan. An Owner
or Primary Owner goes to **Organization Settings → Connectors → Add** and enters
`https://mcp.pluralsight.com/mcp`.

**Step 2 — each person connects individually.** **Settings → Connectors**, select Pluralsight,
and complete the browser login with your own Pluralsight account.

**Step 3 — use this repo as reference.** Everything in [`prompts/`](../prompts/) works as-is —
paste and go. Once skills exist in the plugin, the same pattern applies: open a `SKILL.md` body
and either paste it into the conversation before your request, or put it in a Project's custom
instructions so it applies to every conversation in that Project. The instructions are plain
Markdown and don't depend on anything Claude Code provides.

A subagent has no Desktop equivalent — its value is context isolation, which Desktop doesn't
offer. On Desktop, the equivalent skill or prompt run directly is the fallback, at the cost of a
longer conversation.

---

## VS Code Copilot

**Step 1 — add the server** via `.vscode/mcp.json` in your workspace, or the user-level MCP
config:

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

VS Code opens a browser window for OAuth on first connection. Use Copilot Chat in **agent
mode** — MCP tools aren't available in ask mode.

> If your organization restricts Copilot to registry-only MCP servers (**Settings → Copilot →
> Policies → Restrict MCP access to registry servers**), this fails silently until an admin
> switches it to "Allow all" or adds Pluralsight to your organization's MCP registry.

**Step 2 — get the skills.** Two options:

*Open this repo as your workspace.* [`.vscode/settings.json`](../.vscode/settings.json) is
committed and already points Copilot at the skill files. Nothing to configure.

*Use the skills in your own repo.* Copy the ones you want into a location VS Code scans by
default:

```bash
cp -r plugins/pluralsight-learning/skills/<name> .github/skills/
```

VS Code scans `.github/skills/`, `.claude/skills/`, and `.agents/skills/` in a workspace, and
`~/.copilot/skills/`, `~/.claude/skills/`, and `~/.agents/skills/` for personal skills.

---

## How one set of skill files serves both Claude Code and VS Code

The Claude Code plugin format requires skills at
`plugins/<plugin>/skills/<name>/SKILL.md`. VS Code doesn't scan that path by default — but it
accepts extra locations through the `chat.agentSkillsLocations` setting. So this repo keeps
**one canonical copy** of each skill inside the plugin and points VS Code at it with a
three-line committed `.vscode/settings.json`.

Both tools require the same two frontmatter fields, `name` and `description`, and both require
`name` to match the directory name. The skill files stick to fields both tools understand, so
the same file is valid in both without conditionals.

That's a narrower rule than "only two fields." VS Code documents six fields; Claude Code
documents around nineteen and ignores keys it doesn't know. So the four optional fields in the
[Agent Skills spec](https://agentskills.io/specification.md) — `license`, `compatibility`,
`metadata`, `allowed-tools` — pass through both harmlessly, and are fine for provenance. What
the skills avoid is the Claude-Code-only behavioral fields (`model`, `effort`, `hooks`, and the
rest): those would work in one host and silently do nothing in the other, which is exactly the
conditional this arrangement exists to prevent. The validator draws that line for you.

**The tradeoff.** The setting is workspace-scoped, so it only applies when this repo *is* the
open workspace. A customer vendoring a skill into their own project has to copy the directory
(the `cp -r` above) — which is a real, if small, duplication we've pushed onto the consumer
rather than carrying in the repo.

Two alternatives we rejected:

- **Keeping a second copy of each plugin skill under `.claude/skills/`** so VS Code finds it
  with zero config. This works in both tools with no settings file at all, but creates two
  sources of truth for every skill, and they drift the first time someone edits one and not the
  other. (The repo *does* have a `.claude/skills/` directory — it holds the maintainer-only
  authoring skill, which has exactly one copy and is deliberately not in the plugin. Zero-config
  discovery is the reason it lives there. What's rejected is duplicating a customer-facing
  skill, not using the directory at all.)
- **Canonical skills at the repo root, with `plugin.json` pointing at them** via a `../../`
  path. Plugin component paths aren't supported outside the plugin root.

Single source of truth won. The cost is one settings file and one documented copy step.
