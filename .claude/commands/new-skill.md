---
description: Scaffold and author a new cookbook skill, prompt example, or subagent
argument-hint: <kebab-case-name> [skill|prompt|subagent]
---

Author a new piece of cookbook content named `$1`, as a `$2` (default: skill).

Follow the `cookbook-skill-creator` skill end to end — it is in this repo at
`.claude/skills/cookbook-skill-creator/SKILL.md` and loads automatically. Do not skip its two
steps that are easy to skip: confirming tool behavior against the live server, and the
public-repo review.

Specifically:

1. **Interview before scaffolding.** Ask for the three real phrasings a user would type and the
   near-misses it must stay quiet on. Don't guess these — a guessed description is the single
   most common reason a skill never triggers.
2. **Decide the rung.** A one-off workflow is a prompt example, not a skill. A subagent needs
   context isolation or a restricted tool surface to justify itself.
3. **Scaffold with the script**, not by hand:
   `uv run .claude/skills/cookbook-skill-creator/scripts/init_skill.py $1 --kind ${2:-skill}`
   Add `--with references,assets,scripts` only for resource directories the skill genuinely
   needs — empty or unreferenced ones are validation errors.
4. **Draft the body**, under ~150 lines, giving the reason behind each rule rather than
   shouting the rule.
5. **Verify** with `uv run internal/scripts/validate.py` and `claude plugin validate .`, then
   report what you ran against the live server.

If `$1` is empty, ask what the content should be called before doing anything.
