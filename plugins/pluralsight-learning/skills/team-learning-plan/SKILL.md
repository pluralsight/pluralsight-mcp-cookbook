---
name: team-learning-plan
description: Build a 6-month professional development plan for a report, mapping gaps from their Job Description and Midyear Performance Review to real Pluralsight courses and clips. Use when a manager or team lead asks for a development or growth plan, an upskilling roadmap, or wants performance-review gaps mapped to Pluralsight content for someone on their team.
---

# Team learning plan

Turns a Job Description and a Performance Review into a structured, 6-month development plan
for the employee — with real Pluralsight courses and clips against each gap, not generic
category names. Different from asking the question directly: it forces the gap analysis to
happen first, so the curriculum maps to what the review actually flagged rather than a guess at
the role in general.

This is the manager-facing counterpart to a self-directed ramp plan: the person running this
skill is planning for someone else, not for themselves.

## Steps

### 1. Get the two source documents

Ask for the file paths to the Job Description and the Midyear Performance Review if they
weren't given. Read both in full before analyzing — don't start the gap analysis from a partial
read of either file.

### 2. Gap analysis

Compare the two documents:

- From the Job Description: the core competencies, technical skills, and responsibilities the
  role requires.
- From the Performance Review: current strengths, explicit areas for improvement, and any
  skill gaps named in constructive feedback.

Pick **2–3 focus areas** — the highest-priority gaps where the role's requirements and the
review's feedback overlap. Don't pad to a round number if only one gap is real; don't split one
gap into three to look thorough.

**Do not call `get_user_content_activity`.** It returns the activity of whichever account is
authenticated to the MCP server — the manager running this skill, not the employee the plan is
for. There is no tool on the server that reads someone else's activity. The gap analysis comes
entirely from the two documents.

### 3. Map each focus area to Pluralsight content

For each focus area, call:

```
search_pluralsight_library
  query: "<the focus area, phrased as what someone would search to learn it>"
  sort: "relevance"
  content_type: "video-course"
```

This is the primary source — it returns a direct course URL and a level, which the plan needs
for its curriculum section. Leave `content_type` off only if a first pass returns nothing useful
and you want to see what else the library has for that query.

Then, only where the review calls out something narrower than a full course covers — a specific
technique, not a whole domain — call:

```
query_pluralsight_content_index
  query: "<the specific technique or sub-skill>"
  result_count: 3
```

This returns clip-level matches with a `clip_url` and a `score`. Drop anything scoring below
roughly `0.7` — it's a weak match, not a real recommendation. Leadership and process topics
(feedback, delegation, 1:1s) return real results here just as often as technical ones; don't
assume this tool is technical-content-only.

**When a focus area comes back thin or empty**, say so in the plan rather than substituting a
loosely related course to fill the slot. `search_pluralsight_library` has no result-count
parameter and can return as few as one match even for a reasonably specific query — that's
normal, not a sign the query needs to be broader.

## Output

```
# Development Plan — <Employee Name>

## Executive Summary
One paragraph: purpose of the plan, and one specific strength pulled from the review by name.

## Core Focus Areas
1. <Focus area> — <one line on why this one, tied to a specific line from the JD or review>
2. <Focus area> — ...

## Pluralsight Curriculum

### <Focus area 1>
- [<Course title>](<url>) — <level>. <one-line learning objective>
- [<Clip title>](<clip_url>), from *<course title>* — <one-line learning objective>

## Milestones
- **Day 30:** <specific, measurable — e.g. "Complete <course> and summarize the three
  biggest takeaways in a 1:1">
- **Day 60:** <builds on day 30>
- **Day 90:** <a concrete artifact or demonstrated behavior, not "continue learning">

## Success Criteria
<How the impact shows up in the role day to day — tied to the JD responsibility or review
feedback each focus area came from, not a generic "will have improved skills.">
```

Rules for filling it in:

- **Name the strength before the gaps.** The Executive Summary should quote or closely paraphrase
  something specific from the review, not a generic compliment — it's what makes the plan read
  as informed rather than templated.
- **Every milestone is checkable.** "Complete X and do Y" beats "continue developing in this
  area" — a milestone a manager can't verify at Day 30 doesn't function as one.
- **Every recommendation traces to a document.** If you can't point to the line in the JD or the
  review that a focus area comes from, it's a guess, not an analysis.
- **State what wasn't found.** A focus area with thin Pluralsight results should say so in that
  section rather than being quietly dropped or padded.

## Notes

- `search_pluralsight_library` results are scoped to the manager's licensed libraries, not the
  employee's — in most organizations both accounts share the same license, but if a course
  looks unexpectedly unavailable, license scope on the _authenticating_ account is why.
- `level` is sometimes `null` on results outside `video-course` (paths, practice exams); this
  skill filters to `video-course` by default specifically to avoid that gap.
- Never paste raw tool output into the plan. Course and clip titles, URLs, and objectives should
  be restated in the plan's own words, and the plan itself may go directly to the employee.
