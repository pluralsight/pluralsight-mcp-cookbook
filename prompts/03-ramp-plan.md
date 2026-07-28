# Multi-step: a ramp plan in one prompt

Four tool calls, one prompt — a multi-step workflow you can run by hand, chaining activity
lookup, targeted search, and lab search into one sequenced plan.

## The prompt

```
I'm joining a team that runs everything on Kubernetes and I start on their
migration work in two weeks. Build me a ramp plan:

1. Check my recent Pluralsight activity first, and tell me what you inferred
   about my starting level.
2. Search for clips on the specific sub-topics I'll need — deployments and
   services, health checks and probes, rolling updates and rollbacks, secrets
   and config maps. Three results each.
3. Find beginner-to-intermediate hands-on labs on Kubernetes.
4. Give me a phased plan that alternates watching and doing, with links, a
   rough time estimate per phase, and an explicit list of anything you
   couldn't find good content for.
```

## Why it's written that way

- **Activity first.** Asking for the inference out loud ("tell me what you inferred") makes a
  wrong read visible immediately. Without it, an incorrect skill-level assumption silently
  shapes everything downstream.
- **Sub-topics spelled out.** "Kubernetes" as one query returns the most generic clip in each
  area. Four narrow queries return four useful ones. If you don't know the breakdown, ask for
  it first and paste it back.
- **Labs requested separately.** Clip search and library search hit different indexes. Only
  library search filters by `content_type` and `levels`, so hands-on content needs its own step.
- **Gaps requested explicitly.** Assistants default to filling every slot. Asking for what's
  missing is what makes the plan trustworthy.

## Verifying the output

- Every item should have a working `app.pluralsight.com` link.
- Watching and doing should alternate — four videos in a row means step 3 came back thin.
- Phase 1 should reflect something real from your activity. Generic Phase 1 usually means
  `get_user_content_activity` returned little, which is expected on a new or lightly-used
  account.
- Thin results overall are more often license scope than a gap in the library. Content is
  filtered to the libraries your plan licenses.

## The cost of doing it this way

It works, and you have to retype it every time — the ordering rules, the score threshold, the
gap requirement. Everyone on your team writes a slightly different version, and the weakest
one is the one that gets used.

Packaging it fixes that — run `/new-skill` or see [CONTRIBUTING.md](../CONTRIBUTING.md) for
turning a prompt like this one into a skill.
