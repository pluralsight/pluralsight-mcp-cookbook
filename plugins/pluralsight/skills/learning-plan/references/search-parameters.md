# `search_pluralsight_library` parameter reference

| Parameter | Values | Guidance |
| --- | --- | --- |
| `query` | free text | Describe what the user wants to learn in natural language. |
| `sort` (required) | `relevance`, `newest`, `popularity` | `relevance` by default; `newest` for fast-moving technologies or when the user asks for up-to-date content; `popularity` for the most proven, widely-taken content. |
| `content_type` | `video-course`, `lab`, `path`, `skilliq`, `practice-exam` | Set when a specific format is needed; omit to search everything. |
| `levels` | array of `beginner`, `intermediate`, `advanced` | Set to the user's level (or level + one up for progression). Omit when unknown. |

## Content types

| Value | What it is |
| --- | --- |
| `video-course` | A single video course |
| `lab` | Hands-on guided practice in a real environment |
| `path` | A structured multi-course journey toward a role or technology |
| `skilliq` | A skill assessment that measures current level |
| `practice-exam` | Certification exam preparation |

## Search strategy for plans

- Search `content_type: "path"` first — an existing path may already cover the goal.
- Supplement with `"video-course"`, `"lab"`, and `"skilliq"` searches to fill gaps.
- Run one search at the user's inferred level and a second at the next level up.
- If results look off-topic, refine the query and search again rather than using weak matches.
