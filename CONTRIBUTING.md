# Contributing

Issues and pull requests are welcome — especially a prompt or skill you've actually used, and
corrections where the server behaves differently than these docs claim.

## Before you open a PR

```bash
uv run internal/scripts/validate.py
```

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/); no other dependencies —
the script's inline metadata tells uv which Python to provision. This is what CI runs. It checks
skill and agent frontmatter, naming, the marketplace JSON, the VS Code bridge, and sweeps for
content that shouldn't be in a public repo.

If you have Claude Code, also run `claude plugin validate .`.

## What makes a good addition

If you have Claude Code, run `/new-skill` and it will walk you through any of these, scaffold
the files, and check them. The templates it uses are in
[`.claude/skills/cookbook-skill-creator/assets/`](.claude/skills/cookbook-skill-creator/assets/)
if you'd rather start by hand.

**A prompt example** (`prompts/`) — something you ran that worked, with the reasoning behind
how it's phrased. The reasoning is the useful part; the prompt is just the artifact.

**A skill** (`plugins/pluralsight-learning/skills/<name>/SKILL.md`) — a multi-step workflow
you've run enough times to know where it goes wrong. One-off workflows belong in `prompts/`.
A skill is a directory, not just a file: it can bundle `scripts/`, `references/`, and `assets/`
alongside SKILL.md, loaded only when needed. Put reference detail in `references/` rather than
letting the body grow — the body is loaded every time the skill fires.

**A correction** — the most valuable contribution here. If a documented parameter, enum value,
or response field doesn't match what the server does, say what you called and what came back.

We'd rather have three examples people rely on than nine nobody triggers. A PR that improves an
existing skill is usually more welcome than one that adds another.

## Requirements

- **Production tools only.** The five in [docs/tools-reference.md](docs/tools-reference.md).
  Content built on in-development tools breaks publicly when they change.
- **`name` and `description` are required**, with `name` matching the directory or filename.
  Beyond those, the [Agent Skills spec](https://agentskills.io/specification.md) fields
  (`license`, `compatibility`, `metadata`, `allowed-tools`) and the four that Claude Code and
  VS Code both document (`argument-hint`, `user-invocable`, `disable-model-invocation`,
  `context`) are accepted. Claude-Code-only fields like `model` and `effort` are not — one copy
  of each skill has to work in both hosts, see
  [docs/setup.md](docs/setup.md#how-one-set-of-skill-files-serves-both-claude-code-and-vs-code).
  The validator enforces this, so you don't have to memorize it.
- **No raw tool output.** Live responses contain real account identifiers and progress data.
  Write examples by hand and keep them obviously generic.
- **Verify against the live server** before documenting a parameter, and say in the PR what you
  ran. Don't call `submit_user_feedback` while testing — it writes.
- **Readable with no Pluralsight background.** No internal jargon, no assumed context.

## Reporting a problem

Open an issue with the tool name, the parameters you passed, what you expected, and what came
back. Redact account identifiers and anything from your organization.

For problems with the MCP server itself rather than these examples, contact your Pluralsight
representative — this repo is examples only.
