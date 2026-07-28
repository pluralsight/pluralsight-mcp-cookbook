# Internal — authoring tooling

**Maintainers only.** Nothing here is meant for customers. It's public because the repo is
public, not because it's part of the offering. Customers should start at the
[root README](../README.md).

## Adding content

Run `/new-skill` in Claude Code, or use the
[`cookbook-skill-creator`](../.claude/skills/cookbook-skill-creator/SKILL.md) skill directly.
It walks the full workflow, including the two steps that are easy to skip: confirming tool
behavior against the live server, and the public-repo review.

The skill lives at `.claude/skills/`, which Claude Code and VS Code both scan by default, so
there is **no install step** — open the repo and it's there. It is deliberately **not** in the
marketplace plugin: customers installing `pluralsight-learning` should not get an authoring
tool aimed at us. (A Copilot user who opens this repo as their workspace will see it. That's
unavoidable, and harmless — the description scopes it to this repository.)

## Authoring tooling

Everything below lives in the skill directory, because a skill is a directory rather than a
single file — see [the spec digest](../.claude/skills/cookbook-skill-creator/references/spec.md).

| File | For |
| --- | --- |
| [`scripts/init_skill.py`](../.claude/skills/cookbook-skill-creator/scripts/init_skill.py) | Scaffolding any of the three. `--dry-run` first. |
| [`assets/skill.template.md`](../.claude/skills/cookbook-skill-creator/assets/skill.template.md) | A new skill in `plugins/pluralsight-learning/skills/` |
| [`assets/prompt.template.md`](../.claude/skills/cookbook-skill-creator/assets/prompt.template.md) | A new example in `prompts/` |
| [`assets/subagent.template.md`](../.claude/skills/cookbook-skill-creator/assets/subagent.template.md) | A new subagent in `plugins/pluralsight-learning/agents/` |

The scaffolder creates `scripts/`, `references/`, or `assets/` only when you ask for them with
`--with`, and seeds each with a real file plus a reference to it from SKILL.md. That isn't
politeness: the validator errors on an empty resource directory and on an unreferenced
`scripts/` or `references/` file, so a scaffold that promises more than it delivers fails CI.

## Validation

```bash
uv run internal/scripts/validate.py
```

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/); standard library only
otherwise — the script's inline metadata pins the Python version uv provisions. This is the
same command CI runs ([`.github/workflows/validate.yml`](../.github/workflows/validate.yml)) —
humans and CI cannot diverge. One pass covers:

- **Skill frontmatter** — parses, `name` is kebab-case and matches its directory, `description`
  present and within limits, and the field is one this repo allows. Required `name` and
  `description`; the Agent Skills spec's `license`, `compatibility`, `metadata`, and
  `allowed-tools`; and the four both hosts document (`argument-hint`, `user-invocable`,
  `disable-model-invocation`, `context`). Anything else — including real but Claude-Code-only
  fields like `model` — is an error, because one copy of each skill has to work in both hosts
- **Agent frontmatter** — same, matched against the filename
- **Command frontmatter** — `.claude/commands/*.md`: kebab-case filename, `description` present
- **Bundled skill resources** — `scripts/`, `references/`, and `assets/` are one level deep,
  non-empty, and actually referenced from SKILL.md; relative links resolve; SKILL.md stays
  under the spec's 500-line ceiling (warning past this repo's own ~150)
- **Marketplace JSON** — required fields, kebab-case names, reserved-name check, `source` paths
  resolve on disk, every plugin on disk is listed, versions agree between `marketplace.json`
  and each `plugin.json`
- **The VS Code bridge** — `chat.agentSkillsLocations` paths exist and contain skills. This one
  fails silently in the wild: Copilot just finds no skills and says nothing.
- **Sensitive data** — non-production environment references, internal codenames and hostnames,
  `@pluralsight.com` addresses, ticket links, tokens and credentials, and bare UUIDs (a live
  tool response pasted into a doc is the realistic way account data leaks into this repo)

Warnings don't fail the build; errors exit non-zero.

A line that legitimately has to name one of those terms can end with `validate:allow`. That
downgrades it to a warning rather than hiding it, so suppressions stay visible in CI output.
Use it for documentation about these checks — not to get a real finding past the build.

Also run `claude plugin validate .` before releasing — it checks the plugin structure itself,
which the script doesn't attempt to duplicate.

## Releasing

1. Bump `version` in both `.claude-plugin/marketplace.json` and the plugin's `plugin.json`.
   They must match; the validator enforces it.
2. Run both validators.
3. Merge to the default branch. Customers pick it up with
   `/plugin marketplace update pluralsight-mcp-cookbook`.

## Scope rules

- **Production tools only** in customer-facing content. In-development tools break publicly
  when they change.
- **Never commit raw tool output.** Live responses contain real account UUIDs and progress
  data. Examples in docs are hand-written and illustrative.
- **Fewer, deeper examples.** Adding a ninth thin skill makes the other eight harder to find.
