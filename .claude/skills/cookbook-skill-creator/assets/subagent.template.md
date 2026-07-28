---
name: agent-name-here
description: What it does and when to delegate to it. Must match the filename without .md. This is what the main agent reads when deciding whether to hand off.
model: sonnet
---

You are <role>. You <the one thing you do>. You do not <the adjacent things you must not do>.

## Why you exist

State the reason a subagent is justified here rather than a skill. In practice it is one of:

- **Context isolation** — the work produces large output that is read once. Say roughly how
  large, so the tradeoff is legible to whoever maintains this.
- **Restricted tool surface** — the work should not be able to write or edit.

If neither applies, this should be a skill. Delete this file and use `skill.template.md`.

## What to do

Numbered steps. Name the exact tools and the parameters that matter.

## What to return

Show the literal output shape, with a length cap:

```
## <heading>
1. **<item>** — <type>
   <one line>
   <url>

**Not covered:** <gaps, or "none">
```

Then the constraints that make delegation worth it:

- Return the result and stop. No preamble, no offer to continue.
- Never paste raw tool output. Passing the payload back to the caller defeats the reason you
  were invoked.
- Say what you couldn't find rather than padding to reach a count.

---

**On the `tools:` field:** omit it for anything calling Pluralsight MCP tools. Tool names are
prefixed with the server name chosen at install time, so a hardcoded allowlist silently blocks
every call for anyone who registered the server under a different name. Keep `model:` — it's
portable.
