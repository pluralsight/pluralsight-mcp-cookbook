---
name: cookbook-skill-creator
description: Author a new skill, prompt example, or subagent for the Pluralsight MCP cookbook following this repo's conventions. Use only when working inside the pluralsight-mcp-cookbook repository itself — adding content to the cookbook, drafting a new SKILL.md for the pluralsight-learning plugin, or converting a proven prompt into a reusable skill.
---

# Cookbook skill creator

Adapted from Anthropic's skill-creator for this repo. Same workflow — capture intent,
interview, draft, test, iterate — with two things added that this repo needs: the content is
public, and it depends on a live MCP server whose behavior you must confirm rather than assume.

## Resources

| Path                          | Use                                                               |
| ----------------------------- | ----------------------------------------------------------------- |
| `scripts/init_skill.py`       | Scaffolds the files. Run it first; don't hand-create directories. |
| `assets/skill.template.md`    | Skeleton for a skill                                              |
| `assets/prompt.template.md`   | Skeleton for a `prompts/` example                                 |
| `assets/subagent.template.md` | Skeleton for a subagent                                           |
| `references/spec.md`          | Agent Skills spec digest, and where this repo is stricter         |

## Before you start

**Does this need to be a skill?** A skill is worth writing when the workflow has been run by
hand several times and has judgment in it that keeps getting lost — an ordering rule, a
threshold, a "don't do X." A workflow you've run once should be a prompt example in
`prompts/`. We would rather ship three skills people rely on than nine nobody triggers.

**Which rung is it?** Prompt examples go in `prompts/`, skills in
`plugins/pluralsight-learning/skills/<name>/`, subagents in
`plugins/pluralsight-learning/agents/`. A subagent is only justified by context isolation or a
restricted tool surface — not by "it feels like a separate job."

## 1. Capture intent

Get answers before drafting. Guessing here is what produces skills that never trigger:

- What request does the user type? Write three real phrasings, not a category.
- What should it _not_ trigger on? The near-misses matter more than the hits.
- Which Pluralsight tools does it call, in what order, and what does it do when one returns
  nothing?
- What does the output look like? Sketch it.

## 2. Confirm the tools against the live server

Non-negotiable, and the step most likely to be skipped. Run the actual sequence against
`https://mcp.pluralsight.com/mcp` before you write instructions about it. Check the parameter
names and enum values in `docs/tools-reference.md` against what the server actually accepts —
the docs can lag the server.

**Production tools only.** The cookbook uses the five GA tools:
`get_user_content_activity`, `query_pluralsight_content_index`,
`query_pluralsight_help_center_index`, `search_pluralsight_library`, `submit_user_feedback`.
Skills built on in-development tools break publicly when those change. If a new skill needs
one, that's a conversation before it's a pull request, not after.

Don't call `submit_user_feedback` while testing. It writes.

## 3. Scaffold

```bash
uv run .claude/skills/cookbook-skill-creator/scripts/init_skill.py <name>
```

Add `--kind prompt` or `--kind subagent` for the other two rungs; `--dry-run` to see the tree
first. The script writes from the templates in `assets/`, so there's one copy of each skeleton
rather than one in a template and one in your head.

**Bundled resources.** A skill is a directory, not a file. Pass `--with` only for the
directories this skill genuinely needs:

- **`references/`** — reference material read on demand. This is the pressure valve when the
  body outgrows ~150 lines: move the detail out, link to it, keep the always-loaded part short.
- **`assets/`** — templates, schemas, lookup tables. Things loaded as data, not read as prose.
- **`scripts/`** — executable code, for deterministic work that shouldn't be re-derived by a
  model each time. Self-contained, or documenting its dependencies.

Don't create one speculatively. The validator errors on an empty resource directory and on a
`scripts/` or `references/` file that SKILL.md never mentions — because a file nothing
references is a file nothing will ever load. Keep resources one level deep and link them with
paths relative to SKILL.md.

## 4. Draft

**The description is the whole triggering mechanism.** It's the only part always in context.
Write what the skill does _and_ when to use it, in specific words a user would actually type.

- Good: `Build a personalized, sequenced Pluralsight ramp plan... Use when someone asks how to
get up to speed on a topic, prepare for a project or migration, or onboard onto a new stack.`
- Bad: `Helps with Pluralsight learning content.` — triggers on everything or nothing.

**Body: under ~150 lines.** Imperative, and explain _why_ a rule exists — a model that
understands the reason generalizes to the case you didn't list. `Drop results scoring below
roughly 0.7 rather than padding the plan with weak matches` beats `ALWAYS FILTER RESULTS`.

**Frontmatter.** `name` and `description` are required, and `name` must match the directory.
Beyond that there are tiers — `references/spec.md` has the full table:

- The spec's `license`, `compatibility`, `metadata`, and `allowed-tools` are accepted. Use them
  for provenance, not for behavior the skill depends on: VS Code documents none of them.
- `argument-hint`, `user-invocable`, `disable-model-invocation`, and `context` are documented by
  both hosts and safe to rely on.
- Everything else in Claude Code's table (`model`, `effort`, `hooks`, ...) is rejected by the
  validator. It's real, it's just Claude-Code-only, and one file has to work in both hosts —
  see `docs/setup.md`.

## 5. Write it public

Assume a reader with no Pluralsight context and a screenshot on social media.

- No internal codenames, environment names, hostnames, ticket links, employee or customer names.
- **Never paste raw tool output.** Live responses carry real account identifiers, progress data,
  and content IDs. Hand-write illustrative examples and keep them obviously generic. Don't put
  an example identifier in a template either — the validator flags them, and rightly.
- Production URLs only: `mcp.pluralsight.com`, `app.pluralsight.com`, `help.pluralsight.com`.

## 6. Test

Run the three trigger phrasings from step 1 in a clean session and check the skill loads
without being named. Then run the near-misses and check it stays quiet. A skill that fires on
every Pluralsight question is worse than no skill — it crowds out the right one.

Then run it end to end and confirm each documented tool call actually happens with the
parameters you specified.

## 7. Validate and ship

```bash
uv run internal/scripts/validate.py
claude plugin validate .
```

Both must pass; CI runs the first one on every PR. If you added a new plugin rather than a new
skill in the existing one, add it to `.claude-plugin/marketplace.json` and bump the version in
both `marketplace.json` and the plugin's `plugin.json` — the validator checks they agree.

Update `README.md`'s content table if you added something a customer should discover.
