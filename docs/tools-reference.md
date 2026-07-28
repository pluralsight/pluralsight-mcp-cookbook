# Pluralsight MCP tools

The five generally available tools on `https://mcp.pluralsight.com/mcp`, with the parameters
and response shapes the examples in this repo rely on.

Results across all content tools are scoped to the libraries your Pluralsight license covers.
Thin results are more often a license-scope effect than a gap in the library.

---

## `get_user_content_activity`

Your last few interactions across every Pluralsight content type. No parameters.

Returns grouped arrays: `video`, `assessments`, `skill_iq`, `paths`, `code_labs`,
`cloud_labs`, `sandboxes`. Items carry `title`, `content_id`, `content_type`, a timestamp, and
type-specific fields — `progress` for videos and labs, `quintile_level` for Skill IQ,
`cloud_provider` for cloud labs.

Empty or unrelated results are normal on a new or lightly-used account. Treat this as a signal
for personalization, not as a content source.

---

## `query_pluralsight_content_index`

Semantic search over individual **course clips**. Use it to find the specific explanation of a
concept rather than a whole course.

| Parameter | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| `query` | string | yes | — | Natural language. |
| `result_count` | integer | no | `5` | Range `1`–`20`. |

Each result has `content` (the transcript excerpt), `score`, `clip_url`, and `metadata` with
`clip_title` and `course_title`. Scores below roughly `0.7` are usually weak matches.

Responses are large — a handful of queries can run to thousands of tokens.

---

## `query_pluralsight_help_center_index`

Semantic search over Help Center articles: billing, licenses, plan and team administration,
SSO, account settings.

| Parameter | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| `query` | string | yes | — | The support question, close to verbatim. |
| `result_count` | integer | no | `5` | Range `1`–`20`. |

Results carry the article text plus `metadata.title` and `metadata.url` — always cite the URL.

This is the tool for questions about **Pluralsight the product**. Questions about a technology
go to the two content tools, even when they're phrased similarly.

---

## `search_pluralsight_library`

Structured search over whole library items — courses, labs, paths, assessments, practice exams.

| Parameter | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| `query` | string | yes | — | Search terms, max 512 characters. Short and plain works best. |
| `sort` | `relevance` \| `newest` | yes | — | Required on every call. |
| `content_type` | see below \| null | no | `null` | One type only. Omit to search all. |
| `levels` | array of `beginner` \| `intermediate` \| `advanced` | no | `[]` | Empty includes all levels. |

| `content_type` | What it returns |
| --- | --- |
| `video-course` | On-demand video courses |
| `lab` | Hands-on cloud sandbox labs |
| `path` | Curated skill and role paths |
| `skilliq` | Skill IQ assessments |
| `practice-exam` | Certification practice exams |

Results carry `title`, `url`, `contentType`, `level`, and `shortText`. Two things to know:

- **Up to 10 results, and there is no count parameter.** Narrow with `content_type` and
  `levels`, not by asking for fewer.
- **`level` is `null` for paths and practice exams**, and `shortText` is often `null` or empty.
  Don't present a `null` level as "beginner."

---

## `submit_user_feedback`

Submits structured feedback about the MCP server. All five fields are required strings; pass
`"no response"` for any the user declines to answer.

`technical_issues` · `useful_scenarios` · `missing_tools` · `unmet_expectations` ·
`additional_feedback`

This tool **writes**. Nothing in this repo calls it automatically — invoke it only when someone
asks to leave feedback.

---

## Also on the server

The server exposes additional tools for personalized learning — recording learning
opportunities during a work session and generating digests and guides from them — that are in
active development. Their names and parameters may change.

Everything in this repo uses the five tools above only, so the examples don't break when those
evolve. Ask your Pluralsight contact if you want to try them.
