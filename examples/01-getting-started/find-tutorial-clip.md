# Find a Specific Tutorial Clip

**Goal:** Find the exact course content that answers a narrow technical question — more precise than a catalog search.

## Prompt

```text
Find Pluralsight content that explains how to set up dependency injection in ASP.NET Core.
```

Variations:

```text
I'm stuck on Kubernetes ingress controllers. What Pluralsight clips cover that specifically?
```

## Tools used

- `query_pluralsight_content_index` — semantic search over course clips and tutorial content. Results are automatically filtered to your licensed content libraries.

## What to expect

Pointers to specific clips or modules within courses, not just course titles. Use this when you have a "how do I..." question mid-task; use [library search](search-the-library.md) when you want a whole course, lab, or path.
