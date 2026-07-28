# Scoped search: parameters that change the answer

Still one tool call, but you control the filters. Most of the value people miss in the
Pluralsight MCP server is here — the parameters, not extra prompting.

## Filter by type and level

```
Find beginner hands-on labs on Kubernetes — labs only, no videos.
```

Uses `search_pluralsight_library` with `content_type: "lab"` and `levels: ["beginner"]`.
Without the filters you get courses, paths, and assessments mixed together and have to sort
them yourself.

Valid `content_type` values: `video-course`, `lab`, `path`, `skilliq`, `practice-exam`.
Valid `levels` values: `beginner`, `intermediate`, `advanced` (you can pass more than one).

## Sort by recency when versions matter

```
Show me the newest AWS certification practice exams.
```

Uses `sort: "newest"`. This matters for certifications and fast-moving tooling, where
`relevance` will happily surface a retired exam version. For everything else, `relevance`
is the better default.

`sort` is required on every `search_pluralsight_library` call.

## Ask for specifics, not surveys

```
Find me the specific clips that explain Kubernetes rolling updates and rollbacks.
```

Uses `query_pluralsight_content_index`, which searches individual course clips rather than
whole courses. You get a link that starts at the five-minute explanation instead of a
six-hour course you have to scrub through.

Ask for more or fewer with "give me 10 clips on..." — `result_count` accepts `1`–`20` and
defaults to `5`.

## Point it at a curated path first

```
Is there an existing Pluralsight path for Kubernetes developers, and what does it not cover?
```

Uses `content_type: "path"`. Worth asking before you assemble anything by hand — a curated
path often covers 80% of the request, and the interesting question becomes the remaining 20%.

## Where this stops working

You can now get precise results from one call. You still can't get a *plan* — that needs the
learner's current level, several searches, and an ordering decision. Doing that by hand means
retyping the same five prompts every time.

Next: [03-ramp-plan.md](./03-ramp-plan.md) runs the whole chain in one prompt.
