# Adding Examples

Examples are copy-paste markdown files in `examples/`, organized by complexity level.

## Choose the level

| Level | Criteria |
| --- | --- |
| `01-getting-started` | One prompt, one MCP tool. Teaches what a single tool does. |
| `02-intermediate` | One prompt, multiple MCP tools chained or combined. Teaches a pattern. |
| `03-advanced` | Uses the plugin's skills or agents, multi-step workflows, or combines MCP tools with the assistant's other capabilities (code, git). |

## Use the template

Create `examples/<level>/<kebab-case-name>.md`:

```markdown
# Title (imperative, e.g. "Search the Library")

**Goal:** One sentence — what the user accomplishes.

## Prompt

​```text
The exact prompt to copy-paste.
​```

(Optional) Variations:

​```text
Alternative phrasings that exercise different parameters.
​```

## Tools used

- `tool_name` — what it does in this example and which parameters matter.

## What to expect

The shape of a good response, plus useful follow-up prompts.
```

## Rules

- **Only use the documented tools**: `search_pluralsight_library`, `query_pluralsight_content_index`, `query_pluralsight_help_center_index`, `get_user_content_activity`, `submit_user_feedback`.
- **Test the prompt** against the live MCP server before submitting — prompts must work as written.
- **Don't hardcode course titles** in expected output; the library changes.
- **Add the example to its level's `README.md`** table.

## Submit

Open a pull request. See [CONTRIBUTING.md](../CONTRIBUTING.md).
