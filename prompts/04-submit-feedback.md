# Single-shot: leave feedback on the MCP server

A different kind of single-shot prompt from [01-find-content.md](./01-find-content.md) — this
one writes instead of reading. `submit_user_feedback` sends structured feedback about the MCP
server itself, not about Pluralsight content.

## The prompt

```
I want to leave feedback on the Pluralsight MCP tools. The search results have been
solid, but I wish there was a way to filter by duration. Please submit that as feedback.
```

## Why it's written that way

- **States the intent to submit, not just a complaint.** `submit_user_feedback` writes data on
  every call — nothing else in this repo's examples does that. Say "submit this as feedback"
  explicitly rather than assuming a general comment about the tools should trigger it.
- **One clear point, not a survey.** The tool takes five separate string fields
  (`technical_issues`, `useful_scenarios`, `missing_tools`, `unmet_expectations`,
  `additional_feedback`). A prompt that only speaks to one of them is fine — the assistant
  fills the rest with `"no response"` rather than inventing content for fields you didn't
  address.

## What happens

The assistant calls `submit_user_feedback` once, mapping your comment to the field it best
fits — a missing filter reads as `missing_tools` or `unmet_expectations` depending on phrasing
— and passing `"no response"` for the four fields you didn't address.

## Verifying the output

- The assistant should confirm the submission happened, and ideally repeat back what it sent
  to each field so you can catch a misclassified comment before it's gone.
- If you only meant to vent about a tool rather than formally submit feedback, and the
  assistant called `submit_user_feedback` anyway, say so — this is the one tool in this repo
  where an over-eager call has a real side effect, not just a wasted lookup.

## Where this stops working

This is a single write, not a workflow — there's no next rung here. If you're testing how the
MCP server responds to a new parameter or tool, don't verify against this tool: it writes, and
CONTRIBUTING.md asks contributors not to call it while testing.
