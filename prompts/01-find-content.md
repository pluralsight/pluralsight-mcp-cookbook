# Single-shot: find content

The starting point. One question, one tool call, one answer. No setup beyond having the
Pluralsight MCP server connected.

## Prompts

```
Find me Pluralsight courses on Terraform.
```

```
Are there any beginner labs on Kubernetes?
```

```
What have I been working on recently in Pluralsight?
```

```
How do I add a team member to my Pluralsight plan?
```

## What happens

The assistant picks a tool from your phrasing:

| You said | Tool it reaches for |
| --- | --- |
| "courses on X", "labs on X" | `search_pluralsight_library` |
| "explain X", "clips about X" | `query_pluralsight_content_index` |
| "what was I working on" | `get_user_content_activity` |
| "how do I ... my plan/license/billing" | `query_pluralsight_help_center_index` |

## Where this stops working

Single-shot prompts are fine for "is there content on this." They fall over as soon as the
answer depends on more than one search:

- **No personalization.** "Find me Terraform courses" returns the same list for a first-week
  hire and a staff engineer.
- **No sequencing.** You get a list, not an order to work through it in.
- **Broad topics get shallow results.** "Kubernetes" is a dozen distinct sub-topics; one query
  returns the most generic slice of all of them.

Next: [02-scoped-search.md](./02-scoped-search.md) fixes the third problem with parameters.
