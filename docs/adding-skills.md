# Adding Skills

Skills are reusable instructions that teach the assistant a procedure. They live in `plugins/pluralsight/skills/<skill-name>/SKILL.md` and are portable across Claude Code and VS Code.

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
└── my-skill-name/          # kebab-case, must match usage
    └── SKILL.md
```

### SKILL.md format

```markdown
---
description: What the skill does AND when to use it. This is how the model decides to trigger the skill — include the phrases users would actually say.
---

# Skill Title

Instructions to the assistant. Use "$ARGUMENTS" to capture text the user
passes after the skill name (e.g. /pluralsight:my-skill-name some topic).

## Steps

1. Concrete, ordered steps naming the exact MCP tools to call and which
   parameters to set.
2. ...
```

### Guidelines

- **Description is the trigger.** Write it as "does X. Use when the user Y" — cover both the capability and the situations that should invoke it. Look at the [existing skills](../plugins/pluralsight/skills/) for the pattern.
- **Name exact tools and parameters.** "Call `search_pluralsight_library` with `content_type: "path"` first" beats "search for paths".
- **Only reference the five documented tools** (see [plugin README](../plugins/pluralsight/README.md)).
- **Handle the empty case**: if the skill takes `$ARGUMENTS`, say what to do when it's empty (usually: ask the user).
- Keep it under ~150 lines; skills are loaded into context when triggered.

## Test

```shell
# Load the plugin locally
claude --plugin-dir ./plugins/pluralsight
```

- Invoke directly: `/pluralsight:my-skill-name test topic`
- Test auto-triggering: phrase a request naturally and confirm the skill activates.
- After edits, run `/reload-plugins` to pick up changes.

Validate before submitting:

```shell
claude plugin validate ./plugins/pluralsight
```

## Submit

Add a row to the skills table in [`plugins/pluralsight/README.md`](../plugins/pluralsight/README.md), then open a pull request.
