---
name: personal-learning-digest
description: Generate a personalized Markdown digest of Pluralsight content based on the learning gaps someone has revealed across recent conversations, clustering recurring topics and surfacing courses and labs for each. Use when someone asks to "summarize my recent learning gaps," "give me my weekly learning digest," or "what should I brush up on based on what I've been asking about." Not for content-consumption history ("what have I been learning lately," "what courses have I watched") — that's get_user_content_activity, a different signal (what was consumed) from this skill's (what gaps were revealed).
---

# Personal learning digest

Turns the learning gaps recorded during recent conversations into a Markdown digest of
Pluralsight courses and labs, one section per recurring topic. Different from a raw content
history: this reflects what someone struggled with or asked about, not what they clicked play
on.

**Experimental.** `retrieve_my_learning_opportunities`, `record_learning_opportunity`, and
`generate_weekly_personal_learning_digest` are beta tools in active development, not part of
the five generally-available tools documented in `docs/tools-reference.md`. Their names,
parameters, and response shape may change without notice. Tell the person you're running this
for that it's experimental before you start, and if a call errors or its shape looks different
from what's documented below, stop and say so rather than guessing at a workaround.

One naming note confirmed against the live server: the digest tools' own descriptions refer to
a tool called `identify_learning_opportunity` — that tool doesn't exist under that name. The
tool that actually records opportunities is `record_learning_opportunity`. Use the name
confirmed here, not the one in the digest tools' docstrings.

## Steps

### 1. Check what's already recorded

Call `retrieve_my_learning_opportunities` with `lookback_days` set to match the window the
person asked about (defaults to 30 days back if they didn't say — the tool caps at 30):

```
lookback_days: 7
```

Omitting `lookback_days` restricts the search to the current session only, which is almost
never what "weekly digest" means — pass an explicit value.

If this returns opportunities, skip to step 3. If it returns empty, go to step 2 — don't call
the digest tool against an empty history, it has nothing to work from.

### 2. Nothing recorded yet — ask, then record

Tell the person no learning opportunities are on file for that window, and ask what they'd
want reviewed: a recent debugging session, a concept they had to look up, a decision they were
unsure about. For each thing they describe, call `record_learning_opportunity`:

```
topic: "<2-5 word label, e.g. 'Kubernetes Networking'>"
opportunity_description: "<1-2 sentences as a semantic search query, e.g. 'User is unfamiliar with Kubernetes NetworkPolicy scoping and assumed it applied cluster-wide.'>"
skill_level: "beginner" | "intermediate" | "advanced"
```

Record one call per distinct gap they mention, not one call covering several topics —
`generate_weekly_personal_learning_digest` clusters and scores per-opportunity, so bundling
several topics into one description flattens signal the clustering depends on.

### 3. Generate the digest

Call `generate_weekly_personal_learning_digest`:

```
lookback_days: 7
result_count_per_opportunity: 3
```

`result_count_per_opportunity` caps at 5 — raise it only if the person wants more than 3
suggestions per topic, and expect thinner topics to still come back with fewer than requested.
`content_library_ids` is optional and defaults to resolving from the person's license; only
pass it if they've already named specific library UUIDs.

If the call errors, don't fall back to `generate_personal_learning_digest` (the session-scoped
variant) as a silent substitute — say the weekly tool failed and ask whether a session-only
digest is still useful, since it covers a materially smaller window.

## Output

Present the `plan_markdown` field directly rather than restructuring it — the server already
formats it into per-topic sections with watch and practice links. The response also includes
`opportunities_aggregated`, `total_source_opportunities`, and `result_count`; use those to
sanity-check the digest (e.g. `total_source_opportunities: 1` means the digest is built from a
single recorded gap, not a real cross-session pattern yet) rather than presenting every digest
as equally well-supported:

```
## Kubernetes Networking (intermediate — recurring 3x)
- [Kubernetes Networking Deep Dive](course link) — course
- [NetworkPolicy Labs](lab link) — lab
```

Add one line at the top the tool output doesn't include: a note that this digest was generated
from an experimental tool pair, so anyone who saves or shares it downstream knows to expect
possible drift if the tools change shape later.

- **Don't pad thin topics.** If a topic's section comes back with fewer results than
  requested, say so rather than filling the gap with a loosely related course from elsewhere.
- **Recurring topics matter more than the digest.** The weekly tool boosts priority for
  opportunities that show up across multiple sessions — call that out explicitly rather than
  letting it get lost in a flat list.

## Notes

- `generate_weekly_personal_learning_digest` clusters semantically similar topics and boosts
  priority for recurring ones — that's what distinguishes it from
  `generate_personal_learning_digest`, which only sees the current session and doesn't cluster
  across conversations. Default to the weekly tool; use the session-only one only if the
  person is explicit that they mean just this conversation.
- `lookback_days` maxes at 30 on both `retrieve_my_learning_opportunities` and
  `generate_weekly_personal_learning_digest` — a request for "the last quarter" or similar
  can't be satisfied by either tool as they exist today; say so rather than passing 30 and
  presenting it as the full window.
- If these tools aren't reachable in a given environment yet, say so rather than substituting
  `search_pluralsight_library` and calling it equivalent — that tool has no notion of a
  person's recorded gaps.
- Confirmed live: with only one recorded opportunity, the "Watch" list can repeat the same
  clip across its `result_count_per_opportunity` slots rather than returning distinct items.
  Don't present repeated entries as if they were independently chosen — say the digest is
  thin on source material when that happens.
