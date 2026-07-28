---
name: skill-name-here
description: What this does, then when to use it. Must match the directory name. Include concrete phrasings a user would actually type — this string is the only trigger signal the model gets.
---

# Skill name

One or two sentences: what this produces, and what makes it different from just asking the
question directly. Delete this comment block and everything bracketed before committing.

## Steps

### 1. <First step>

Which Pluralsight tool, and why this one rather than the similar-looking alternative.

State the parameters that matter and their real constraints — verify against
`docs/tools-reference.md` and the live server, don't copy from memory:

```
query: "<example>"
sort: "relevance"
content_type: "lab"
levels: ["beginner"]
```

Say what to do when the call returns nothing useful. Every step needs this; it's the most
common gap in a first draft.

### 2. <Second step>

...

## Output

Sketch the shape you want. A concrete example does more than a description of one.

```
## Section
- item — why it's here
```

Then the rules that keep it useful, each with its reason:

- **<Rule>.** <Why it matters.>

## Notes

Server behavior that will surprise someone — result caps, fields that come back `null`,
license scoping. Facts you confirmed live, not assumptions.
