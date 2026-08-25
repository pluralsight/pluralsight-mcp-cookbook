# Beginner-to-Advanced Course Sequence

**Goal:** Get an ordered sequence of courses that takes you from novice to advanced on one topic.

## Prompt

```text
Build me a course sequence on Terraform that goes from beginner to advanced.
Check if a learning path already covers this, and fill any gaps with
individual courses. Order everything and tell me roughly what each step teaches.
```

## Tools used

- `search_pluralsight_library`, called several times with different filters:
  - `content_type: "path"` — an existing learning path may already provide the spine.
  - `levels: ["beginner"]`, then `["intermediate"]`, then `["advanced"]` — to find courses at each stage.

## What to expect

Either "there's a path that covers exactly this — start there" or an ordered course list with a level progression. Good responses avoid overlap between steps and note where a path already covers a level so you don't double up.
