# Agent Skills spec — digest, and where this repo differs

Source: <https://agentskills.io/specification.md>. Read this when you need the exact
constraint rather than the convention. The validator (`internal/scripts/validate.py`) is the
enforcement mechanism for everything below.

## Directory structure

A skill is a directory whose only required member is `SKILL.md`:

```
skill-name/
├── SKILL.md          # required: frontmatter + instructions
├── scripts/          # optional: executable code
├── references/       # optional: documentation read on demand
└── assets/           # optional: templates, schemas, data files
```

## Progressive disclosure

This is the reason the structure exists, and the thing to design around:

1. **Metadata** (~100 tokens) — `name` and `description` are loaded at startup for *every*
   installed skill. This is why the description is the whole triggering mechanism.
2. **Body** — the full `SKILL.md` is loaded once the skill activates. Spec ceiling is 500
   lines; this repo aims for ~150, because the body competes with the actual conversation.
3. **Resources** — files under `scripts/`, `references/`, `assets/` are loaded only when
   something reaches for them.

A skill that puts reference detail in the body pays for it on every activation. That's what
`references/` is for.

## Frontmatter

| Field | Required | Constraint |
| --- | --- | --- |
| `name` | yes | 1–64 chars, `a-z0-9-` only, no leading/trailing/consecutive hyphens, matches the parent directory |
| `description` | yes | 1–1024 chars, non-empty; says what it does *and* when to use it |
| `license` | no | A license name, or the name of a bundled license file |
| `compatibility` | no | ≤500 chars; environment requirements — intended product, system packages, network access |
| `metadata` | no | Map of string → string, for anything the spec doesn't define |
| `allowed-tools` | no | Space-separated string of pre-approved tools. Experimental; support varies |

### What this repo adds

**Tier 3 — documented by both hosts, safe to rely on:** `argument-hint`, `user-invocable`,
`disable-model-invocation`, `context`.

**Tier 4 — rejected by the validator:** every other field in Claude Code's table (`model`,
`effort`, `agent`, `background`, `hooks`, `paths`, `arguments`, `disallowed-tools`). These are
real Claude Code fields. They're rejected because this repo ships **one copy** of each skill to
both Claude Code and VS Code Copilot — see `docs/setup.md`. A field only one host understands
makes that arrangement conditional, which is what the single-source rule exists to prevent.

On the spec's optional four: neither host *rejects* unknown keys, so they pass through
harmlessly. But VS Code documents none of them, so use them for provenance — authorship,
versioning, license — not for behavior the skill depends on.

**`allowed-tools` and MCP tools.** Pluralsight tool names carry the server name chosen at
install time. A rule naming `mcp__<server>__search_pluralsight_library` silently matches
nothing for anyone who registered the server under a different name. Same trap as a hardcoded
`tools:` on a subagent — see the note at the end of `assets/subagent.template.md`.

## Bundled resources

**`scripts/`** — executable code. Self-contained, or documenting its dependencies; helpful
error messages; handles edge cases. Give it a shebang and the executable bit.

**`references/`** — documentation loaded on demand. Keep individual files focused; smaller
files mean less context consumed when one is read.

**`assets/`** — static resources: templates, images, schemas, lookup tables.

### File references

Use paths relative to the skill root, one level deep:

```markdown
See [the reference guide](references/REFERENCE.md) for details.
Run scripts/extract.py to pull the tables.
```

Avoid deeply nested reference chains, and avoid `..` — a path that escapes the skill directory
breaks the moment the skill is copied somewhere else. The validator errors on a link that
doesn't resolve and warns on one that escapes.

**Empty or unreferenced resource directories are errors here**, not style notes. A `scripts/`
directory created "just in case" is a promise the skill doesn't keep; a `references/` file that
SKILL.md never names is a file nothing will ever load. `scripts/init_skill.py` therefore only
creates a resource directory when asked, and seeds it with a real file *and* a reference to it.

## Validating

```bash
uv run internal/scripts/validate.py    # this repo: skills, agents, commands, resources, secrets
claude plugin validate .               # plugin structure
```

The upstream reference validator (`skills-ref validate ./my-skill`, from the
[agentskills repo](https://github.com/agentskills/agentskills)) checks frontmatter and naming
against the spec alone. This repo's script is a superset for the checks that matter here.
