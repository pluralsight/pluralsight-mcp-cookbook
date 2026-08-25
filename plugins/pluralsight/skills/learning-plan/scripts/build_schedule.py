#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Turn a learning plan into a dated week-by-week schedule.

Reads a JSON learning plan and distributes its items across calendar
weeks based on estimated hours and the learner's available hours per
week. Run with `uv run scripts/build_schedule.py` (or plain python3 —
there are no third-party dependencies).
"""

import argparse
import json
import sys
from datetime import date, timedelta

VALID_TYPES = {"skilliq", "video-course", "lab", "path", "practice-exam"}

USAGE_EXAMPLES = """\
Input format (file via --input, or stdin):
  {
    "goal": "Become a Kubernetes administrator",
    "items": [
      {"title": "Kubernetes Skill IQ", "type": "skilliq", "level": "intermediate", "hours": 0.5},
      {"title": "Kubernetes Administration", "type": "video-course", "level": "intermediate", "hours": 8}
    ]
  }

  Each item needs "title" and "hours" (> 0). "type" must be one of:
  skilliq, video-course, lab, path, practice-exam. "level" is optional.

Examples:
  uv run scripts/build_schedule.py --input plan.json --start-date 2026-09-01 --hours-per-week 5
  echo "$PLAN_JSON" | uv run scripts/build_schedule.py --start-date 2026-09-01 --hours-per-week 3 --format json

Exit codes:
  0  success
  2  invalid arguments (bad date, non-positive hours)
  3  invalid plan JSON (parse error or missing/invalid fields)
"""


def fail(code: int, message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(code)


def load_plan(raw: str) -> dict:
    try:
        plan = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(3, f"input is not valid JSON ({exc}). Expected format:\n{USAGE_EXAMPLES}")
    if not isinstance(plan, dict) or not isinstance(plan.get("items"), list):
        fail(3, 'plan must be a JSON object with an "items" array. Run with --help for the format.')
    if not plan["items"]:
        fail(3, '"items" is empty — nothing to schedule.')
    for i, item in enumerate(plan["items"]):
        if not isinstance(item, dict) or not item.get("title"):
            fail(3, f'items[{i}] must be an object with a non-empty "title".')
        hours = item.get("hours")
        if not isinstance(hours, (int, float)) or hours <= 0:
            fail(3, f'items[{i}] ("{item.get("title")}") needs numeric "hours" > 0. Received: {hours!r}')
        item_type = item.get("type")
        if item_type is not None and item_type not in VALID_TYPES:
            fail(3, f'items[{i}] "type" must be one of: {", ".join(sorted(VALID_TYPES))}. Received: "{item_type}"')
    return plan


def build_weeks(items: list, start: date, hours_per_week: float) -> list:
    """Fill weeks sequentially; an item spans multiple weeks when it exceeds the remaining capacity."""
    weeks = []
    current = {"start": start, "entries": [], "hours": 0.0}
    remaining_in_week = hours_per_week
    for item in items:
        left = float(item["hours"])
        first_chunk = True
        while left > 0:
            if remaining_in_week <= 0:
                weeks.append(current)
                current = {"start": current["start"] + timedelta(weeks=1), "entries": [], "hours": 0.0}
                remaining_in_week = hours_per_week
            chunk = min(left, remaining_in_week)
            current["entries"].append(
                {
                    "title": item["title"],
                    "type": item.get("type"),
                    "level": item.get("level"),
                    "hours": round(chunk, 2),
                    "continued": not first_chunk,
                }
            )
            current["hours"] = round(current["hours"] + chunk, 2)
            remaining_in_week -= chunk
            left -= chunk
            first_chunk = False
    weeks.append(current)
    return weeks


def render_markdown(plan: dict, weeks: list, hours_per_week: float) -> str:
    total = sum(float(i["hours"]) for i in plan["items"])
    n_items, n_weeks = len(plan["items"]), len(weeks)
    lines = [f"# Schedule: {plan.get('goal', 'Learning plan')}", ""]
    lines.append(
        f"{n_items} item{'s' if n_items != 1 else ''}, ~{total:g} hours total "
        f"at {hours_per_week:g} h/week → {n_weeks} week{'s' if n_weeks != 1 else ''}."
    )
    for n, week in enumerate(weeks, start=1):
        end = week["start"] + timedelta(days=6)
        lines += ["", f"## Week {n} — {week['start'].isoformat()} to {end.isoformat()} ({week['hours']:g} h)", ""]
        for entry in week["entries"]:
            meta = ", ".join(str(v) for v in (entry["type"], entry["level"]) if v)
            suffix = " *(continued)*" if entry["continued"] else ""
            meta_str = f" ({meta})" if meta else ""
            lines.append(f"- **{entry['title']}**{meta_str} — {entry['hours']:g} h{suffix}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Turn a JSON learning plan into a dated week-by-week schedule.",
        epilog=USAGE_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input", help="Path to the plan JSON file (default: read stdin)")
    parser.add_argument("--start-date", required=True, help="First day of week 1, ISO format (e.g. 2026-09-01)")
    parser.add_argument("--hours-per-week", type=float, required=True, help="Study hours available per week (> 0)")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="Output format (default: md)")
    args = parser.parse_args()

    try:
        start = date.fromisoformat(args.start_date)
    except ValueError:
        fail(2, f'--start-date must be an ISO date like 2026-09-01. Received: "{args.start_date}"')
    if args.hours_per_week <= 0:
        fail(2, f"--hours-per-week must be > 0. Received: {args.hours_per_week:g}")

    if args.input:
        try:
            with open(args.input, encoding="utf-8") as fh:
                raw = fh.read()
        except OSError as exc:
            fail(2, f"cannot read --input file: {exc}")
    else:
        if sys.stdin.isatty():
            fail(2, "no input: pass --input plan.json or pipe the plan JSON on stdin. Run with --help for the format.")
        raw = sys.stdin.read()

    plan = load_plan(raw)
    weeks = build_weeks(plan["items"], start, args.hours_per_week)

    if args.format == "json":
        out = {
            "goal": plan.get("goal"),
            "hours_per_week": args.hours_per_week,
            "total_hours": sum(float(i["hours"]) for i in plan["items"]),
            "weeks": [
                {
                    "week": n,
                    "start": w["start"].isoformat(),
                    "end": (w["start"] + timedelta(days=6)).isoformat(),
                    "hours": w["hours"],
                    "entries": w["entries"],
                }
                for n, w in enumerate(weeks, start=1)
            ],
        }
        print(json.dumps(out, indent=2))
    else:
        print(render_markdown(plan, weeks, args.hours_per_week))


if __name__ == "__main__":
    main()
