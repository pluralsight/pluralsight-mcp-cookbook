# `search_pluralsight_library` parameter reference

| Parameter | Values | Guidance |
| --- | --- | --- |
| `query` | free text | Describe what the user wants to learn in natural language. |
| `sort` (required) | `relevance`, `newest`, `popularity` | `relevance` by default; `newest` when the user asks for up-to-date content on fast-moving technologies; `popularity` when the user wants the most proven or widely-taken content. |
| `content_type` | `video-course`, `lab`, `path`, `skilliq`, `practice-exam` | Set when the user asks for a specific format; omit to search everything. |
| `levels` | array of `beginner`, `intermediate`, `advanced` | Set (single value or combination) when the user indicates their experience level. Omit when unknown. |

## Content types

| Value | What it is |
| --- | --- |
| `video-course` | A single video course |
| `lab` | Hands-on guided practice in a real environment |
| `path` | A structured multi-course journey toward a role or technology |
| `skilliq` | A skill assessment that measures current level |
| `practice-exam` | Certification exam preparation |

## Mapping user phrasing to parameters

| User says | Set |
| --- | --- |
| "I'm new to X" / "beginner" | `levels: ["beginner"]` |
| "hands-on" / "practice" / "lab" | `content_type: "lab"` |
| "a full path" / "structured" / "curriculum" | `content_type: "path"` |
| "test my knowledge" / "where do I stand" | `content_type: "skilliq"` |
| "latest" / "current version" | `sort: "newest"` |
| "best" / "most popular" | `sort: "popularity"` |
