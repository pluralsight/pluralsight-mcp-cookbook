---
description: Run the cookbook validators and explain any failures
allowed-tools: Bash(uv:*) Bash(claude:*) Read Grep
---

Run both validators and report the result:

```bash
uv run internal/scripts/validate.py
claude plugin validate .
```

The first is exactly what CI runs on every pull request
(`.github/workflows/validate.yml`), so a green run here means a green run there.

If anything fails, read the offending file and explain the cause rather than only quoting the
message. Two failure classes need interpretation:

- **A sensitive-data finding** may be a false positive — some patterns match ordinary
  authoring words, the environment-name ones especially.
  Rewrite the prose to sidestep the term where you can. Only append `validate:allow` when the
  line genuinely has to name it, and say why; suppressions stay visible as warnings so they get
  reviewed rather than quietly burying a real finding.
- **A frontmatter field rejected as unknown** is usually a real Claude Code field that this repo
  bans on purpose, because one copy of each skill has to work in VS Code Copilot too. See
  `.claude/skills/cookbook-skill-creator/references/spec.md` for the tiers before removing the
  check.

Warnings do not fail the build, but report them — a skill over ~150 lines or a link that
escapes its directory is worth fixing while you are here.
