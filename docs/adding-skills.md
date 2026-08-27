# Adding Skills

Skills are reusable instructions that teach the assistant a procedure. They live in `plugins/pluralsight/skills/<skill-name>/` and are portable across Claude Code and VS Code.

Skills in this repo follow the open [Agent Skills specification](https://agentskills.io/specification.md). A skill is a directory with a required `SKILL.md` plus optional `scripts/`, `references/`, and `assets/` subdirectories.

## Recommended: use skill-creator

Anthropic ships a [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) skill that scaffolds, evaluates, and optimizes skills. Install it, then ask Claude to create the skill for you:

```shell
# In Claude Code
/plugin marketplace add anthropics/skills
/plugin install skill-creator@anthropic-agent-skills
```

Then:

```text
Use skill-creator to create a new skill in plugins/pluralsight/skills/ that
<what your skill should do>, using the Pluralsight MCP tools.
```

skill-creator handles frontmatter conventions, description optimization (critical for reliable auto-triggering), and can run evals to measure whether the skill actually improves results.

## Manual authoring

### Structure

```text
plugins/pluralsight/skills/
└── my-skill-name/          # kebab-case, must match the `name` in frontmatter
    ├── SKILL.md            # required: frontmatter + instructions
    ├── scripts/            # optional: executable code the assistant runs
    ├── references/         # optional: detail loaded on demand
    └── assets/             # optional: templates and static resources
```

[`learning-plan`](../plugins/pluralsight/skills/learning-plan/) is the reference implementation in this repo — it uses all three optional directories.

### SKILL.md format

```markdown
---
name: my-skill-name
description: What the skill does AND when to use it. This is how the model decides to trigger the skill — include the phrases users would actually say.
license: MIT
metadata:
  author: Pluralsight
  version: "1.0"
---

# Skill Title

Instructions to the assistant. Use "$ARGUMENTS" to capture text the user
passes after the skill name (e.g. /pluralsight:my-skill-name some topic).

## Steps

1. Concrete, ordered steps naming the exact MCP tools to call and which
   parameters to set.
2. ...
```

Frontmatter fields, per the spec:

| Field | Required | Notes |
| --- | --- | --- |
| `name` | Yes | Max 64 chars, lowercase letters/numbers/hyphens only, no leading, trailing, or consecutive hyphens. Must match the directory name. |
| `description` | Yes | Max 1024 chars. Covers both what it does and when to use it. |
| `license` | No | Use `MIT` to match this repo. |
| `compatibility` | No | Max 500 chars. Only add it if the skill has real environment requirements (e.g. a script needing Python or uv). |
| `metadata` | No | String-to-string map. Use `author` and `version` here. |
| `allowed-tools` | No | Experimental; support varies by client. Skip it unless you need it. |

### Progressive disclosure

Clients load skills in stages: the `name` and `description` at startup, the `SKILL.md` body when the skill activates, and everything in `scripts/`, `references/`, and `assets/` only when the instructions call for it. Structure your skill to take advantage of that:

- Keep `SKILL.md` focused on the workflow — the steps, the tools, the decisions. Under 500 lines, and ideally far shorter.
- Move lookup material (parameter tables, formats, domain detail) into `references/*.md` and link it from the step that needs it.
- Put output templates and static resources in `assets/`.
- Reference bundled files with **relative paths from the skill root** (`references/plan-design.md`), and keep references one level deep — no long chains.

### Bundling scripts

Add a script when the task involves logic the model shouldn't improvise: date arithmetic, parsing, format conversion, deterministic transforms. See the [Agent Skills scripting guide](https://agentskills.io/skill-creation/using-scripts.md) for the full rationale.

Conventions for this repo:

- **Declare dependencies inline** with [PEP 723](https://peps.python.org/pep-0723/) so there's no install step, and run scripts with [uv](https://docs.astral.sh/uv/):

  ```python
  # /// script
  # requires-python = ">=3.10"
  # dependencies = ["beautifulsoup4>=4.12,<5"]
  # ///
  ```

  ```shell
  uv run scripts/my_script.py --help
  ```

- **For one-off tools that already exist**, skip `scripts/` entirely and call the packaged tool from `SKILL.md` with a pinned version: `uvx ruff@0.8.0 check .`
- **List scripts in `SKILL.md`** under an "Available scripts" heading so the assistant knows they exist, and show the exact invocation.
- **Declare runtime needs** in the `compatibility` frontmatter field.

Design scripts for an assistant, not a human at a terminal:

- **Never prompt interactively** — agents run in non-interactive shells and a TTY prompt hangs forever. Take all input via flags, environment variables, or stdin.
- **Support `--help`** with a description, flags, and usage examples. That output is how the assistant learns the interface.
- **Write actionable errors**: say what was wrong, what was expected, and what to try. `Error: --format must be one of: json, csv. Received: "xml"` beats `invalid input`.
- **Emit structured output** (JSON/CSV) on stdout and diagnostics on stderr.
- **Use distinct exit codes** for distinct failure classes, and document them in `--help`.
- **Be idempotent and bounded**: safe to retry, with predictable output size (paginate or summarize rather than dumping tens of thousands of characters).

### Guidelines

- **Description is the trigger.** Write it as "does X. Use when the user Y" — cover both the capability and the situations that should invoke it. Look at the [existing skills](../plugins/pluralsight/skills/) for the pattern.
- **Name exact tools and parameters.** "Call `search_pluralsight_library` with `content_type: "path"` first" beats "search for paths".
- **Only reference the five documented tools** (see [plugin README](../plugins/pluralsight/README.md)).
- **Handle the empty case**: if the skill takes `$ARGUMENTS`, say what to do when it's empty (usually: ask the user).
- **Don't hardcode course titles.** The catalog changes; let the tools return results.

## Test

```shell
# Load the plugin locally
claude --plugin-dir ./plugins/pluralsight
```

- Invoke directly: `/pluralsight:my-skill-name test topic`
- Test auto-triggering: phrase a request naturally and confirm the skill activates.
- Exercise any bundled script on its own, including its failure paths: `uv run plugins/pluralsight/skills/my-skill-name/scripts/my_script.py --help`
- After edits, run `/reload-plugins` to pick up changes.

Validate before submitting:

```shell
claude plugin validate ./plugins/pluralsight
uvx --from skills-ref agentskills validate ./plugins/pluralsight/skills/my-skill-name
```

The second command runs [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref), the reference validator for the Agent Skills spec — it checks frontmatter and naming conventions. (The PyPI package is `skills-ref`; the executable it installs is `agentskills`.) CI runs both commands on every pull request.

## Submit

Add a row to the skills table in [`plugins/pluralsight/README.md`](../plugins/pluralsight/README.md), then open a pull request.
