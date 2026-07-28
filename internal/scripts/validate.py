#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Validate the cookbook: skill, agent, and command frontmatter, naming, bundled
skill resources, marketplace JSON, the VS Code bridge, and a sensitive-data sweep.

One pass, one exit code. CI and humans run the same command:

    uv run internal/scripts/validate.py

Standard library only -- uv provisions the interpreter from the metadata above,
so there are no dependencies to install.
"""

import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# Skill/agent names: lowercase letters, digits, hyphens. Both Claude Code and
# VS Code enforce this and require the name to match its file or directory.
#
# This one pattern already encodes every naming rule in the Agent Skills spec
# (agentskills.io/specification.md): lowercase alphanumerics and hyphens only, no
# leading hyphen, no trailing hyphen, no consecutive hyphens. Don't "simplify" it
# to `[a-z0-9-]+` -- that would let all three of those through.
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_MAX = 64
DESC_MAX = 1024

SKILL_FIELDS = {"name", "description"}
# Optional frontmatter defined by the Agent Skills spec. Neither Claude Code nor
# VS Code rejects unknown keys, so these pass through both hosts -- but VS Code
# documents none of them, so nothing load-bearing should depend on them.
SKILL_SPEC_OPTIONAL = {"license", "compatibility", "metadata", "allowed-tools"}
# Optional fields Claude Code and VS Code Copilot BOTH document. Claude-Code-only
# fields (model, effort, hooks, ...) stay out: one file has to work in both.
SKILL_HOST_OPTIONAL = {"argument-hint", "user-invocable", "disable-model-invocation", "context"}
SKILL_OPTIONAL = SKILL_SPEC_OPTIONAL | SKILL_HOST_OPTIONAL
AGENT_FIELDS = {"name", "description"}
AGENT_OPTIONAL = {"tools", "model"}
# Slash commands in .claude/commands/. `description` is what the picker shows.
COMMAND_OPTIONAL = {
    "name", "description", "argument-hint", "user-invocable",
    "disable-model-invocation", "allowed-tools", "context", "model",
}

COMPAT_MAX = 500        # spec: compatibility is 1-500 chars
SKILL_LINES_MAX = 500   # spec: keep SKILL.md under 500 lines
SKILL_LINES_WARN = 150  # this repo's own convention, tighter than the spec

# The only frontmatter key the spec allows to be a nested block.
NESTED_FIELDS = {"metadata"}
BLOCK_SCALARS = {">", "|", ">-", "|-", ">+", "|+"}

# Bundled resource directories a skill may ship alongside SKILL.md.
RESOURCE_DIRS = ("scripts", "references", "assets")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

# Reserved by Anthropic for official marketplaces.
RESERVED_MARKETPLACES = {
    "claude-code-marketplace", "claude-code-plugins", "claude-plugins-official",
    "claude-plugins-community", "claude-community", "anthropic-marketplace",
    "anthropic-plugins", "agent-skills", "anthropic-agent-skills",
    "knowledge-work-plugins", "life-sciences", "claude-for-legal",
    "claude-for-financial-services", "financial-services-plugins",
    "first-party-plugins", "healthcare",
}

# This repo is public. Each pattern is something that must never ship.
SENSITIVE = [
    (re.compile(r"\bstaging\b|\bstage\b(?!\s*(one|two|three|\d))", re.I),
     "staging reference"),
    (re.compile(r"inferences-sb|\bsandbox\b(?!\s*(es)?\b.{0,40}(lab|Pluralsight|AWS|cloud))", re.I),
     "sandbox/non-production environment reference"),
    (re.compile(r"\bIRIS\b"), "internal codename"),
    (re.compile(r"[A-Za-z0-9._%+-]+@pluralsight\.com"), "internal email address"),
    (re.compile(r"pluralsight\.atlassian\.net|/browse/[A-Z]{2,}-\d+"), "internal ticket link"),
    (re.compile(r"\b(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,})"),
     "API token"),
    (re.compile(r"(?i)\b(api[_-]?key|secret|password|bearer)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"),
     "hardcoded credential"),
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
     "bare UUID (may be real account or content data)"),
    (re.compile(r"\.(internal|corp|local)\b|\bmcp-[a-z]+\.pluralsight\.(io|net)\b"),
     "internal hostname"),
]

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}
TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".py", ".sh", ".txt"}

# Gitignored local files. They cannot reach the public repo, and sweeping them
# produces findings on a maintainer's machine that CI will never reproduce.
SKIP_FILES = {".claude/settings.local.json", ".vscode/mcp.json", ".mcp.json"}

# Escape hatch for lines that legitimately name a forbidden term -- documentation
# about these checks, mainly. Suppressions are reported as warnings so they stay
# visible in CI output and can't be used to quietly bury a real finding.
ALLOW_MARKER = "validate:allow"

errors: list = []
warnings: list = []


def err(path, msg):
    errors.append(f"{path.relative_to(REPO) if path else '-'}: {msg}")


def warn(path, msg):
    warnings.append(f"{path.relative_to(REPO) if path else '-'}: {msg}")


def parse_frontmatter(path):
    """Return (dict, error). Minimal YAML: flat `key: value` pairs, plus exactly one
    level of indented pairs under the keys in NESTED_FIELDS (`metadata`, the only
    nested field the Agent Skills spec defines), returned as a dict of str -> str.

    Deliberately not a YAML parser -- stdlib only, so there is no install step and
    no reason for anyone to skip running this."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, "missing YAML frontmatter (file must start with ---)"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "frontmatter is not closed with ---"

    data = {}
    nested_key = None      # key whose block we are inside, or None
    nested_indent = None   # column that block's entries sit at

    for i, line in enumerate(text[4:end].split("\n"), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\t" in line[:len(line) - len(line.lstrip())]:
            return None, f"line {i}: YAML forbids tabs for indentation; use spaces"
        if ":" not in line:
            return None, f"line {i}: expected `key: value`, got {line.strip()!r}"

        key, _, value = line.partition(":")
        indent = len(key) - len(key.lstrip(" "))
        key, value = key.strip(), value.strip().strip("'\"")

        if indent:
            if nested_key is None:
                return None, (f"line {i}: unexpected indented line -- nesting is only "
                              f"supported one level deep under {sorted(NESTED_FIELDS)}")
            if nested_indent is None:
                nested_indent = indent
            elif indent != nested_indent:
                return None, (f"line {i}: inconsistent indentation under `{nested_key}` "
                              f"(expected {nested_indent} spaces, got {indent}); only one "
                              "level of nesting is supported")
            if not key:
                return None, f"line {i}: nested entry under `{nested_key}` has an empty key"
            data[nested_key][key] = value
            continue

        nested_key, nested_indent = None, None
        if value in BLOCK_SCALARS:
            return None, (f"line {i}: multi-line block scalars are not supported; "
                          f"keep `{key}` on one line")
        if key in NESTED_FIELDS and value == "":
            data[key] = {}
            nested_key = key
        else:
            data[key] = value
    return data, None


def check_name_and_description(path, fm, expected, kind, required, optional):
    name = fm.get("name")
    if not name:
        err(path, f"{kind} frontmatter is missing required field `name`")
    else:
        if not NAME_RE.match(name):
            err(path, f"name {name!r} must be lowercase letters, digits, and hyphens only")
        if len(name) > NAME_MAX:
            err(path, f"name is {len(name)} chars, max {NAME_MAX}")
        if name != expected:
            err(path, f"name {name!r} must match {expected!r}")

    desc = fm.get("description")
    if not desc:
        err(path, f"{kind} frontmatter is missing required field `description`")
    elif len(desc) > DESC_MAX:
        err(path, f"description is {len(desc)} chars, max {DESC_MAX}")
    elif len(desc) < 40:
        warn(path, "description is very short; it is the only trigger signal the model gets")

    for key in set(fm) - required - optional:
        err(path, f"unknown frontmatter field `{key}`")


def check_spec_fields(path, fm):
    """Constraints on the Agent Skills spec's optional frontmatter fields."""
    if "license" in fm and not (isinstance(fm["license"], str) and fm["license"]):
        err(path, "`license` must be a non-empty string (a license name, or the name "
                  "of a bundled license file)")

    if "compatibility" in fm:
        compat = fm["compatibility"]
        if not (isinstance(compat, str) and compat):
            err(path, "`compatibility` must be a non-empty string")
        elif len(compat) > COMPAT_MAX:
            err(path, f"compatibility is {len(compat)} chars, max {COMPAT_MAX}")

    if "metadata" in fm:
        md = fm["metadata"]
        if not isinstance(md, dict):
            err(path, "`metadata` must be an indented block of `key: value` lines, not "
                      f"an inline value ({md!r})")
        elif not md:
            err(path, "`metadata` is present but has no entries -- remove it or fill it in")
        else:
            for k, v in md.items():
                if " " in k:
                    err(path, f"metadata key {k!r} must not contain spaces")
                if not v:
                    err(path, f"metadata key {k!r} has an empty value; the spec is a "
                              "string -> string map")

    if "allowed-tools" in fm:
        tools = fm["allowed-tools"]
        if not (isinstance(tools, str) and tools):
            err(path, "`allowed-tools` must be a non-empty space-separated string")
        elif tools.startswith("["):
            err(path, "`allowed-tools` must be a space-separated string, not a YAML list "
                      "-- Claude Code accepts a list but VS Code does not document it")
        else:
            if "," in tools:
                warn(path, "`allowed-tools` uses commas; the spec says space-separated")
            if "mcp__" in tools:
                warn(path, "`allowed-tools` names an MCP tool by full name. Pluralsight "
                           "tool names carry the server name chosen at install time, so "
                           "the rule silently misses for anyone who registered it under "
                           "a different name -- same trap as a hardcoded agent `tools:`")


def check_skill_resources(skill):
    """Bundled scripts/, references/, and assets/ per the Agent Skills spec: one level
    deep, actually referenced from SKILL.md, never an empty placeholder."""
    root = skill.parent
    body = skill.read_text(encoding="utf-8")
    lines = body.splitlines()

    if len(lines) > SKILL_LINES_MAX:
        err(skill, f"SKILL.md is {len(lines)} lines; the spec says keep it under "
                   f"{SKILL_LINES_MAX}. Move detail into references/")
    elif len(lines) > SKILL_LINES_WARN:
        warn(skill, f"SKILL.md is {len(lines)} lines; this repo aims for under "
                    f"~{SKILL_LINES_WARN}. Consider splitting into references/")

    # Relative links must resolve. The body is always loaded, so a dead link here is
    # a dead end the model follows at runtime. Fenced code blocks are excluded first --
    # a `[<placeholder>](<url>)` inside an output template is illustrative, not a link.
    prose = re.sub(r"```.*?```", "", body, flags=re.S)
    for target in LINK_RE.findall(prose):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        rel = target.split("#")[0]
        if not rel:
            continue
        if not (root / rel).exists():
            err(skill, f"link target {target!r} does not resolve")
        elif ".." in Path(rel).parts:
            warn(skill, f"link {target!r} escapes the skill directory; the spec wants "
                        "paths relative to SKILL.md, and this breaks if the skill is "
                        "copied somewhere else")

    for name in RESOURCE_DIRS:
        d = root / name
        if not d.exists():
            continue
        if not d.is_dir():
            err(skill, f"{name} must be a directory")
            continue
        entries = [p for p in sorted(d.rglob("*"))
                   if p.name != ".gitkeep"
                   and not any(part in SKIP_DIRS for part in p.relative_to(d).parts)]
        files = [p for p in entries if p.is_file()]
        if not files:
            err(skill, f"{name}/ is empty -- do not scaffold directories a skill "
                       "does not use")
            continue
        for p in entries:
            if p.is_dir():
                err(skill, f"{p.relative_to(root).as_posix()}/ nests below {name}/; the "
                           "spec wants bundled resources one level deep")
        for p in files:
            ref = p.relative_to(root).as_posix()
            if ref not in body:
                if name == "assets":
                    warn(skill, f"{ref} is never mentioned in SKILL.md; if a script "
                                "loads it, say so")
                else:
                    err(skill, f"{ref} is never mentioned in SKILL.md, so nothing will "
                               "ever load it -- reference it or delete it")
            if name == "scripts" and p.suffix in (".py", ".sh"):
                first = p.read_text(encoding="utf-8", errors="replace").split("\n", 1)[0]
                if not first.startswith("#!"):
                    warn(skill, f"{ref} has no shebang")
                if not os.access(str(p), os.X_OK):
                    warn(skill, f"{ref} is not executable (git tracks the mode bit)")


def check_skills():
    found = []
    for skill in sorted(REPO.glob("**/skills/*/SKILL.md")):
        if any(p in SKIP_DIRS for p in skill.parts):
            continue
        found.append(skill)
        fm, error = parse_frontmatter(skill)
        if error:
            err(skill, error)
            continue
        check_name_and_description(
            skill, fm, skill.parent.name, "skill", SKILL_FIELDS, SKILL_OPTIONAL
        )
        check_spec_fields(skill, fm)
        check_skill_resources(skill)
    if not found:
        err(None, "no SKILL.md files found -- check the layout")
    return found


def check_agents():
    for agent in sorted(REPO.glob("**/agents/*.md")):
        if any(p in SKIP_DIRS for p in agent.parts):
            continue
        fm, error = parse_frontmatter(agent)
        if error:
            err(agent, error)
            continue
        check_name_and_description(
            agent, fm, agent.stem, "agent", AGENT_FIELDS, AGENT_OPTIONAL
        )


def check_commands():
    """Slash commands in .claude/commands/. Nothing else in this file globbed them,
    so they were shipping unvalidated."""
    cmd_dir = REPO / ".claude" / "commands"
    if not cmd_dir.is_dir():
        return
    for cmd in sorted(cmd_dir.glob("*.md")):
        if not NAME_RE.match(cmd.stem):
            err(cmd, f"command filename {cmd.stem!r} must be lowercase letters, digits, "
                     "and hyphens -- it is the slash command name")
        fm, error = parse_frontmatter(cmd)
        if error:
            err(cmd, error)
            continue
        if not fm.get("description"):
            err(cmd, "command frontmatter is missing `description` -- it is what the "
                     "command picker shows")
        name = fm.get("name")
        if name and name != cmd.stem:
            err(cmd, f"name {name!r} must match the filename {cmd.stem!r}")
        for key in set(fm) - COMMAND_OPTIONAL:
            err(cmd, f"unknown frontmatter field `{key}`")


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, f"invalid JSON: {e}"


def check_marketplace():
    mp_path = REPO / ".claude-plugin" / "marketplace.json"
    if not mp_path.exists():
        err(None, ".claude-plugin/marketplace.json is missing")
        return
    mp, error = load_json(mp_path)
    if error:
        err(mp_path, error)
        return

    for field in ("name", "owner", "plugins"):
        if field not in mp:
            err(mp_path, f"missing required field `{field}`")
    name = mp.get("name", "")
    if name and not NAME_RE.match(name):
        err(mp_path, f"marketplace name {name!r} must be kebab-case")
    if name in RESERVED_MARKETPLACES:
        err(mp_path, f"marketplace name {name!r} is reserved by Anthropic")
    if isinstance(mp.get("owner"), dict) and "name" not in mp["owner"]:
        err(mp_path, "owner.name is required")

    listed = set()
    for entry in mp.get("plugins", []):
        pname = entry.get("name")
        if not pname:
            err(mp_path, "a plugin entry is missing `name`")
            continue
        listed.add(pname)
        if not NAME_RE.match(pname):
            err(mp_path, f"plugin name {pname!r} must be kebab-case")

        source = entry.get("source")
        if source is None:
            err(mp_path, f"plugin {pname!r} is missing `source`")
        elif isinstance(source, str):
            if not source.startswith("./"):
                err(mp_path, f"plugin {pname!r}: relative source must start with './'")
            elif ".." in source:
                err(mp_path, f"plugin {pname!r}: source must not escape the marketplace root")
            else:
                resolved = REPO / source[2:]
                if not resolved.is_dir():
                    err(mp_path, f"plugin {pname!r}: source path {source} does not exist")
                else:
                    check_plugin_manifest(resolved, pname, entry, mp_path)

    for manifest in sorted(REPO.glob("plugins/*/.claude-plugin/plugin.json")):
        pname = manifest.parents[1].name
        if pname not in listed:
            err(manifest, f"plugin {pname!r} exists on disk but is not listed in marketplace.json")


def check_plugin_manifest(plugin_dir, pname, entry, mp_path):
    manifest = plugin_dir / ".claude-plugin" / "plugin.json"
    if not manifest.exists():
        err(mp_path, f"plugin {pname!r}: missing {manifest.relative_to(REPO)}")
        return
    data, error = load_json(manifest)
    if error:
        err(manifest, error)
        return
    if data.get("name") != pname:
        err(manifest, f"name {data.get('name')!r} must match marketplace entry {pname!r}")
    if not data.get("description"):
        err(manifest, "missing `description`")
    mv, pv = entry.get("version"), data.get("version")
    if mv and pv and mv != pv:
        err(manifest, f"version {pv!r} disagrees with marketplace.json {mv!r}")
    if not (plugin_dir / "skills").is_dir() and not (plugin_dir / "agents").is_dir():
        warn(manifest, "plugin ships neither skills/ nor agents/")


def check_vscode_bridge():
    """The bridge is load-bearing for VS Code users: if these paths stop resolving,
    Copilot silently finds no skills. See docs/setup.md."""
    path = REPO / ".vscode" / "settings.json"
    if not path.exists():
        err(None, ".vscode/settings.json is missing -- VS Code Copilot will not find the skills")
        return
    # settings.json is JSONC; strip line comments before parsing.
    raw = re.sub(r"^\s*//.*$", "", path.read_text(encoding="utf-8"), flags=re.M)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        err(path, f"invalid JSON: {e}")
        return
    locations = data.get("chat.agentSkillsLocations")
    if not isinstance(locations, dict) or not locations:
        err(path, "`chat.agentSkillsLocations` must be a non-empty object of path -> boolean")
        return
    for loc, enabled in locations.items():
        if not (REPO / loc).is_dir():
            err(path, f"skill location {loc!r} does not exist")
        elif not enabled:
            warn(path, f"skill location {loc!r} is present but disabled")
        elif not list((REPO / loc).glob("*/SKILL.md")):
            warn(path, f"skill location {loc!r} currently has no skills -- fine while "
                       "it's an empty scaffold, but check this once new skills are added")


def check_sensitive_data():
    for path in sorted(REPO.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if any(p in SKIP_DIRS for p in path.parts):
            continue
        if path.relative_to(REPO).as_posix() in SKIP_FILES:
            continue  # gitignored; can't reach the public repo, and CI never sees it
        if path.resolve() == Path(__file__).resolve():
            continue  # this file necessarily contains the patterns
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(lines, start=1):
            for pattern, label in SENSITIVE:
                if pattern.search(line):
                    if ALLOW_MARKER in line:
                        warn(path, f"line {n}: {label} suppressed by {ALLOW_MARKER}")
                    else:
                        err(path, f"line {n}: {label} -- {line.strip()[:90]}")


def main():
    check_skills()
    check_agents()
    check_commands()
    check_marketplace()
    check_vscode_bridge()
    check_sensitive_data()

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"ERROR: {e}")

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK -- validation passed ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
