---
name: sync-mcp-tools
description: Sync this cookbook's docs, examples, skills, and agents with the Pluralsight MCP server's current tool list. Use whenever the Pluralsight MCP server has added, removed, renamed, or changed the arguments/description of a tool, when the user asks to "update the docs for the new tools", "sync the tool list", "add support for the new MCP tool", or before a release to check the repo hasn't drifted from what the server actually exposes. This is a maintainer workflow for this repo, not something end users of the installed plugin would invoke.
license: MIT
metadata:
  author: Pluralsight
  version: "1.0"
---

# Sync MCP Tools

This repo hardcodes the Pluralsight MCP server's tool list in a lot of places —
tables, prose ("the five documented tools"), skill instructions, agent tool
allowlists, examples. When the server's real tool surface changes, all of
those go stale unless something walks the repo and fixes them deliberately.
That's what this skill does. It is a five-stage pipeline with two human
approval gates — don't skip the gates, since both the "what's OK to publish
externally" call and the "which files actually need edits" call are ultimately
the user's to make, not something to infer silently.

## Stage 1 — Get the live tool list

Use whatever Pluralsight MCP connection is actually available in this
session — the fully-qualified tool prefix varies by how it's connected
(`mcp__pluralsight__`, `mcp__plugin_pluralsight_pluralsight__`,
`mcp__claude_ai_Pluralsight_MCP_beta__`, or something else entirely), so
don't hardcode one. Run `ToolSearch` with a query like `"pluralsight"` to
discover what's present, then look for a live tool set (not just an
`authenticate`/`complete_authentication` pair) whose tools match the
server's shape — `search_pluralsight_library`,
`query_pluralsight_content_index`, etc. Any Pluralsight MCP connection with
live tools is an acceptable source for this skill, including the claude.ai
beta connector — prefer a directly-installed server
(`mcp__pluralsight__`/`mcp__plugin_pluralsight_pluralsight__`) when more than
one is live, since that's what this repo's own install instructions point
users at, but fall back to whichever one is actually available rather than
blocking on it.

- If a Pluralsight MCP server is found but only its
  `authenticate`/`complete_authentication` tools are visible, call its
  `authenticate` tool and walk the user through completing the OAuth flow
  before continuing.
- If no Pluralsight MCP connection is found at all, stop and tell the user
  it isn't installed in this session. Ask them to add and authenticate one
  first — either `/plugin install pluralsight@pluralsight` (or
  `claude mcp add --transport http pluralsight https://mcp.pluralsight.com/mcp`)
  in Claude Code, or the equivalent MCP connector setup in Claude Desktop —
  then re-run this skill. Don't try to fake the tool list from memory or
  from the repo's existing docs.

Once a live tool set is found, use `ToolSearch` with `select:<the discovered
prefix>*` to pull the full, current schema for every tool: name, description, and
every parameter with its type/required-ness/description. This is the ground
truth — prefer it over anything cached in this skill, in memory, or in the
repo's existing docs.

**Don't trust the first keyword search as complete.** A plain keyword
`ToolSearch` (e.g. `"pluralsight"`) can silently return a truncated list —
there's no "N more available" signal, so a short result looks identical to a
complete one. Call it with a generous `max_results` (50+), and afterward
sanity-check completeness: if the names you got back suggest a family (e.g.
`list_channels` and `create_channel` strongly imply `get_channel_details`,
`update_channel`, `assign_team_to_channel` might also exist), run a follow-up
search for that family specifically before locking in the list. Getting
Stage 1 wrong means Stage 2 never even offers the user a tool to include or
exclude — it's the one mistake this skill can't recover from downstream.

## Stage 2 — Curate what's safe to publish externally

This repo is public. Not every tool the server exposes is necessarily meant
for the public cookbook (e.g. write tools, anything still labelled
experimental/beta, or anything whose description signals it's
internal-only). Present the user with the **full** live list from Stage 1 —
one line per tool with its name and one-sentence description — and ask them
to mark each one include / exclude for the external docs. Don't use a
multiple-choice UI that caps the option count; just list them in the
conversation and let the user respond (e.g. "include all but X and Y", or a
per-tool yes/no). If a tool is brand new since the last sync, call that out
explicitly so it doesn't get silently waved through.

Two signals are worth surfacing explicitly rather than judging silently:

- **Naming/namespace signals for exclude-by-default.** A namespace suffix
  like `-sandbox`, or a tool description that says something like "only
  registered when `ENABLE_X=true`", is a strong signal the tool isn't part
  of the stable public surface. Flag these to the user as a block with a
  recommended default (exclude), rather than presenting them exactly like
  every other tool and making the user do the pattern-matching themselves.
- **Family gaps.** If the approved tools from a past sync belong to an
  obvious family (channel management, analytics, etc.) and this run's list
  is missing a member that family would be expected to have, that's more
  likely a Stage 1 miss than a deliberate server-side removal — go back and
  search for it before asking the user to curate an incomplete set.

## Stage 3 — Lock the approved spec

From the user's answer, build the final approved list: for each included
tool, its exact name, its full parameter list (name, type, required/default,
description), and the description text to use in the docs (the server's
wording verbatim unless the user asks to reword it). Read this list back to
the user as the thing you're about to build a plan against, since everything
downstream depends on it being right. Treat their confirmation here as
locking the spec — don't reopen Stage 2 without asking.

## Stage 4 — Find what needs to change

Compare the approved spec against what the repo currently says. Start from
[references/repo-touchpoints.md](references/repo-touchpoints.md) — it's a
checklist of files known to name tools, as of the last time this skill was
updated — but don't trust it blindly, since files get added, renamed, or
moved. Confirm and extend it with a fresh sweep, e.g.:

```shell
grep -rln --include='*.md' --include='*.json' -E 'search_pluralsight_library|query_pluralsight_content_index|query_pluralsight_help_center_index|get_user_content_activity|submit_user_feedback' . --exclude-dir=node_modules --exclude-dir=.git
```

(swap in the actual current + approved tool names, since the point of this
grep is partly to find files still mentioning tools that no longer exist).

Run a second grep alongside it for files that assert a *count* without
naming any tool — these are easy to miss because the tool-name grep above
walks right past them:

```shell
grep -rln --include='*.md' -iE '\b(five|six|seven|eight|nine|ten)\b.*document(ed)?|document(ed)?.*\b(tools?)\b' . --exclude-dir=node_modules --exclude-dir=.git
```

`.github/PULL_REQUEST_TEMPLATE.md` and `.github/ISSUE_TEMPLATE/*.md` are
known to fall in this category — they assert a tool count in a checklist
item but don't name individual tools, so a fresh contributor's PR checklist
can go stale even when every doc page is correct.

For each file that references the tool list, work out concretely what has to
change: a new row in a table, a removed tool name from a "the five
documented tools" style sentence (update the count too — don't leave a
number that's now wrong), a changed parameter in a skill's instructions or a
`references/*.md` parameter table, an agent's `tools:` frontmatter allowlist,
a new example under `examples/01-getting-started/` for a newly-added tool
that has no worked example yet, or a version bump in
`.claude-plugin/marketplace.json` / `plugins/pluralsight/.claude-plugin/plugin.json`.

For the version bump, use a simple rule rather than eyeballing "materially
changed": newly-approved tool(s) added with nothing removed → minor bump.
A tool removed, renamed, or given a breaking parameter change → ask the user
which bump they want, since that's a judgment call about how the cookbook's
own versioning should communicate the break. Pure doc/example wording fixes
with no change to the approved tool set → no bump.

Also flag anything the repo's own conventions call for that goes beyond pure
text edits — e.g. `docs/adding-examples.md` requires "only use the documented
tools", so a newly-approved tool with zero examples is a gap worth surfacing,
even if writing the example itself needs the user's product judgment.

Write this up as a concrete, file-by-file plan: file path, what changes, and
why (tie each change back to a specific Stage 3 spec entry or a stale
reference you found). Present the plan and **stop — wait for explicit
approval before editing anything**. If the user wants changes to the plan,
revise and re-present rather than partially executing.

## Stage 5 — Execute

Once approved, make exactly the changes in the plan. A few repo-specific
things worth keeping straight while editing:

- Table rows for tools live in two places that must stay identical in
  substance: `README.md` and `plugins/pluralsight/README.md`.
- `docs/adding-agents.md` lists tool names twice — once per fully-qualified
  prefix (`mcp__plugin_pluralsight_pluralsight__` and `mcp__pluralsight__`).
  Both need the same set of bare tool names appended.
- Skills follow the conventions in `docs/adding-skills.md` (frontmatter
  shape, `references/` for parameter tables, no hardcoded course titles).
  If you're adding a new tool's usage into an existing skill, match its
  existing structure rather than introducing a new pattern.
- After edits, re-run the same grep from Stage 4 to confirm no stale tool
  name or wrong count survived, and skim
  [references/repo-touchpoints.md](references/repo-touchpoints.md) to see if
  it needs updating for next time (a genuinely new touchpoint file should be
  added to that checklist).
- Don't run `claude plugin validate` or open a PR unless the user asks —
  finishing the edits is the deliverable; let the user decide on
  validation/submission timing per `docs/adding-skills.md` /
  `CONTRIBUTING.md`.

Summarize what changed, file by file, when done.
