#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Scaffold a new skill, prompt example, or subagent for the cookbook.

Writes from the templates in ../assets/ so there is exactly one copy of each
skeleton. Creates optional resource directories only when asked, and seeds each
with a real file plus a reference to it in SKILL.md -- the validator errors on an
empty resource directory and on an unreferenced scripts/ or references/ file, so a
scaffold that lies does not pass CI.

    uv run init_skill.py my-new-skill
    uv run init_skill.py my-new-skill --with references,scripts
    uv run init_skill.py find-labs --kind prompt
    uv run init_skill.py lab-scout --kind subagent --dry-run

Standard library only -- uv provisions the interpreter from the metadata above.
"""

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_MAX = 64

ASSETS = Path(__file__).resolve().parent.parent / "assets"
SKILLS_DIR = "plugins/pluralsight-learning/skills"
AGENTS_DIR = "plugins/pluralsight-learning/agents"
PROMPTS_DIR = "prompts"

RESOURCE_DIRS = ("scripts", "references", "assets")

# Seeded when --with names the directory. Each entry is (filename, body, section
# text appended to SKILL.md) so the new file is referenced from the moment it exists.
SEEDS = {
    "references": (
        "REFERENCE.md",
        "# Reference\n\nDetail the skill body should not carry: parameter tables, enum "
        "values, response\nfields. Loaded only when something reaches for it, so length "
        "is cheaper here than\nin SKILL.md.\n",
        "Read [the reference](references/REFERENCE.md) when you need the full parameter list.",
    ),
    "assets": (
        "output-example.md",
        "# Output example\n\nA hand-written, obviously generic example of the shape this "
        "skill produces. Never\npaste real tool output here.\n",
        "`assets/output-example.md` shows the output shape.",
    ),
    "scripts": (
        None,  # named after the skill
        None,  # generated below
        None,
    ),
}


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def find_repo():
    """Walk up from the working directory looking for the marketplace manifest.

    Deliberately not derived from __file__: this skill can be copied elsewhere, and
    guessing a parent count would then silently target the wrong tree."""
    for d in [Path.cwd().resolve()] + list(Path.cwd().resolve().parents):
        if (d / ".claude-plugin" / "marketplace.json").is_file():
            return d
    die("not inside the mcp-cookbook checkout (no .claude-plugin/marketplace.json "
        "found in this directory or any parent) -- cd into the repo and retry")


def read_template(filename):
    path = ASSETS / filename
    if not path.is_file():
        die(f"template {path} is missing")
    return path.read_text(encoding="utf-8")


def script_seed(name):
    return (
        f"{name}.py",
        "#!/usr/bin/env python3\n"
        "# /// script\n"
        '# requires-python = ">=3.8"\n'
        "# dependencies = []\n"
        "# ///\n"
        f'"""<What this does, and why it is code rather than instructions.>\n\n'
        f"    uv run {name}.py --help\n\n"
        'Standard library only -- uv provisions the interpreter from the metadata above.\n"""\n\n'
        "import argparse\n\n\n"
        "def main():\n"
        "    parser = argparse.ArgumentParser(description=__doc__)\n"
        "    parser.parse_args()\n"
        "    raise SystemExit('not implemented')\n\n\n"
        'if __name__ == "__main__":\n'
        "    main()\n",
        f"Run `scripts/{name}.py` to <what it does>.",
    )


def next_prompt_number(prompts_dir):
    highest = 0
    if prompts_dir.is_dir():
        for p in prompts_dir.glob("*.md"):
            m = re.match(r"^(\d+)-", p.name)
            if m:
                highest = max(highest, int(m.group(1)))
    return highest + 1


def plan_skill(repo, name, into, with_dirs, description):
    """Return {path: (text, mode)} for a new skill directory."""
    root = repo / (into or SKILLS_DIR) / name
    heading = name.replace("-", " ").capitalize()
    body = (read_template("skill.template.md")
            .replace("skill-name-here", name)
            .replace("# Skill name", f"# {heading}"))
    if description:
        body = re.sub(r"^description:.*$", f"description: {description}", body,
                      count=1, flags=re.M)

    files = {}
    references = []
    for d in with_dirs:
        if d == "scripts":
            fname, content, ref = script_seed(name)
        else:
            fname, content, ref = SEEDS[d]
        files[root / d / fname] = (content, 0o755 if d == "scripts" else 0o644)
        references.append(ref)

    if references:
        body = body.rstrip("\n") + "\n\n## Resources\n\n" + \
            "\n".join(f"- {r}" for r in references) + "\n"

    files[root / "SKILL.md"] = (body, 0o644)
    return root, files


def plan_prompt(repo, name):
    n = next_prompt_number(repo / PROMPTS_DIR)
    path = repo / PROMPTS_DIR / f"{n:02d}-{name}.md"
    return path.parent, {path: (read_template("prompt.template.md"), 0o644)}


def plan_subagent(repo, name, description):
    path = repo / AGENTS_DIR / f"{name}.md"
    body = read_template("subagent.template.md").replace("agent-name-here", name)
    if description:
        body = re.sub(r"^description:.*$", f"description: {description}", body,
                      count=1, flags=re.M)
    return path.parent, {path: (body, 0o644)}


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name", help="kebab-case name; becomes the directory or filename")
    parser.add_argument("--kind", default="skill",
                        choices=("skill", "prompt", "subagent"),
                        help="which rung to scaffold (default: skill)")
    parser.add_argument("--into", metavar="DIR",
                        help=f"parent directory for a skill (default: {SKILLS_DIR})")
    parser.add_argument("--with", dest="with_dirs", default="", metavar="LIST",
                        help="comma-separated resource dirs to seed: "
                             + ",".join(RESOURCE_DIRS) + " (default: none)")
    parser.add_argument("--description", help="replace the template's description line")
    parser.add_argument("--dry-run", action="store_true",
                        help="print what would be created and exit")
    args = parser.parse_args()

    if not NAME_RE.match(args.name):
        die(f"name {args.name!r} must be lowercase letters, digits, and single hyphens "
            "(no leading, trailing, or doubled hyphen)")
    if len(args.name) > NAME_MAX:
        die(f"name is {len(args.name)} chars, max {NAME_MAX}")

    with_dirs = [d.strip() for d in args.with_dirs.split(",") if d.strip()]
    for d in with_dirs:
        if d not in RESOURCE_DIRS:
            die(f"unknown resource dir {d!r}; choose from {', '.join(RESOURCE_DIRS)}")
    if with_dirs and args.kind != "skill":
        die("--with applies to skills only; prompts and subagents are single files")

    repo = find_repo()

    if args.kind == "skill":
        root, files = plan_skill(repo, args.name, args.into, with_dirs, args.description)
    elif args.kind == "prompt":
        root, files = plan_prompt(repo, args.name)
    else:
        root, files = plan_subagent(repo, args.name, args.description)

    existing = [p for p in files if p.exists()]
    if existing:
        die("refusing to overwrite: "
            + ", ".join(str(p.relative_to(repo)) for p in existing))
    if args.kind == "skill" and root.exists():
        die(f"{root.relative_to(repo)} already exists")

    for path in sorted(files):
        rel = path.relative_to(repo)
        if args.dry_run:
            print(f"would create  {rel}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        text, mode = files[path]
        path.write_text(text, encoding="utf-8")
        path.chmod(mode)
        print(f"created  {rel}")

    if args.dry_run:
        return

    print("\nNext:")
    print("  1. Fill in the template. Write the description last, from three real")
    print("     phrasings a user would type -- it is the whole triggering mechanism.")
    print("  2. Confirm every tool call against https://mcp.pluralsight.com/mcp")
    print("     before documenting its parameters.")
    print("  3. Check triggering in a clean session, then the near-misses.")
    print("  4. uv run internal/scripts/validate.py && claude plugin validate .")


if __name__ == "__main__":
    main()
