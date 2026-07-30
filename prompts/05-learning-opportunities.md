# Single-shot: recording and retrieving learning opportunities

Two more single-shot prompts, this time for the personalized-learning tools that are still in
active development — their names and parameters may change, so verify against the live server
before relying on the specifics here.

## Recording a learning opportunity

### The prompt

```
I just spent an hour debugging a flaky retry loop in our payments service — turned out
we weren't respecting the Retry-After header. Log this as a learning opportunity: what I
ran into, what the fix was, and what I'd want to review later.
```

### Why it's written that way

- **Concrete incident, not a vague topic.** "Retry loop / Retry-After header" gives the tool
  something specific to file, versus "log that I learned about retries."
- **Names the three parts a good record needs** — what happened, what the fix was, what's
  worth revisiting — since the tool's field names may shift while it's under development.

### What happens

The assistant calls `record_learning_opportunity` with a structured entry describing the
incident.

### Verifying the output

Ask the assistant to read back exactly what it recorded before assuming it matches what you
described — this is a write, and a paraphrase that drifts from your actual incident is worse
than no record at all.

## Retrieving learning opportunities

### The prompt

```
Pull up the learning opportunities I've logged over the last month and group them by
the technology or system they touched.
```

### Why it's written that way

- **Time-boxes the pull.** Without a range, results either default to "everything" or "recent"
  depending on how the tool is implemented — say the window you want.
- **Asks for grouping, not just a list.** A raw list of one-line incidents is hard to act on;
  grouping by system is what turns it into "here's where I keep getting stuck."

### What happens

The assistant calls `retrieve_my_learning_opportunities` and organizes the results by the
technology or system mentioned in each entry.

### Verifying the output

Cross-check a couple of entries against what you actually remember logging — since this tool
is still evolving, confirm it's returning your entries rather than a stale or default-scoped
set.

## Where this stops working

Both of these are single-shot writes and reads on their own. The natural next step — using a
retrieved history of learning opportunities to shape a ramp plan like
[03-ramp-plan.md](./03-ramp-plan.md) — isn't documented yet, since the digest and guide tools
these would feed into are also still in development.
