---
name: learning-guide-from-context
description: Turn any free-form context — a README, a meeting transcript, a PRD, a Slack thread, pasted notes, or any other document someone hands to an AI tool — into a structured Markdown learning guide with real Pluralsight courses and labs per topic. Use when someone asks to "make a learning guide for my team based on this repo," "what should my team learn to work on this codebase," "turn these meeting notes into a learning plan," or "generate a Pluralsight learning path for our stack." Not limited to codebases — any context describing a goal, gap, or unfamiliar subject qualifies. Do not use for a single-topic course lookup ("find me a course on Kubernetes" — go straight to search_pluralsight_library) or for personal learning-history questions ("what have I been learning lately" — that's get_user_content_activity or a personal digest tool, not context-based guide generation).
---

# Learning guide from context

Turns any unstructured context — a README, an architecture doc, meeting notes, a PRD, a Slack
thread, or plain pasted text — into a skill-leveled Markdown guide, with real Pluralsight clips
and labs linked under each topic. Not scoped to a codebase or a stack: the context can describe
a project, a role, a goal, or just an unfamiliar subject someone was discussing. Different from
asking the question directly: it forces topic extraction to happen first, so the guide reflects
what the context actually implies someone needs to learn, rather than a flat list of technology
names.

**Experimental.** `extract_learning_topics_from_context` and `generate_learning_guide` are beta
tools in active development, not part of the five generally-available tools documented in
`docs/tools-reference.md`. Their names, parameters, and response shape may change without
notice. Tell the person you're running this for that it's experimental before you start, and if
either call errors or the shape looks different from what's documented below, stop and say so
rather than guessing at a workaround.

## Steps

### 1. Gather the context

Ask for whatever describes the situation if it wasn't already given. This can be anything: a
README or architecture doc, but just as easily meeting notes, a PRD, a Slack thread, a job
description, or a few sentences typed directly into the conversation. It doesn't need to
reference a codebase at all. Read any attached files in full rather than skimming; this is the
only input the topic extraction has to work with.

### 2. Extract topics

Call `extract_learning_topics_from_context`:

```
context: "<the gathered context, pasted close to verbatim>"
audience_hint: "<optional — who this is for, e.g. 'mid-level backend engineers new to Go'>"
```

This returns a list of topics, each with `topic`, `opportunity_description`, `skill_level`, and
`rationale`, plus a `context_summary`. `audience_hint` matters more than it looks — it's what
calibrates `skill_level` per topic, so skip it only when there's genuinely no useful detail
about who's learning.

If the returned topics list is long (more than ~6), don't pass all of them to the next step
automatically — check with the person running this whether to cover everything or focus on a
subset. Padding the final guide with marginal topics makes it harder to act on.

### 3. Generate the guide

Call `generate_learning_guide` with the topics from step 2, unmodified:

```
topics: [<the topic objects from step 2>]
result_count_per_topic: 3
```

Each topic must include `topic`, `opportunity_description`, `skill_level`, and `rationale` — the
same shape returned by the extraction call. This returns `guide_markdown` (the finished guide),
`topics_extracted`, and `result_count`.

If a topic's section comes back thin, say so when presenting the guide rather than padding it
with a loosely related course pulled from elsewhere.

## Output

Present `guide_markdown` directly — it already comes back as a complete, well-formed guide with
a title, a per-topic breakdown (level badge, watch links, practice links), and a closing note on
sequencing. Don't paraphrase or restructure it; the value of this skill is that the server
already did that formatting work.

Add one thing the tool output doesn't include: a one-line note at the top flagging that this
guide was generated from an experimental tool pair, so anyone who saves or shares it downstream
knows to expect possible drift if the tools change shape later.

## Notes

- Both tools are beta and separate from the five generally-available tools the rest of this
  repo's examples use. If they aren't reachable in a given environment yet, say so rather than
  substituting `search_pluralsight_library` and calling it equivalent.
- `content_library_ids` is optional on both calls and defaults to resolving from the user's
  license — only pass it if the person running this already knows the specific library UUIDs
  they want.
- `result_count_per_topic` caps at 5 per topic; each topic's section can still come back with
  fewer results than requested when the library has thin coverage for that specific phrasing.
