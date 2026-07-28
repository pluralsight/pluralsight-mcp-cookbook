# <Rung>: <what this prompt does>

One line on where this sits: single-shot, scoped by parameters, or multi-step. Prompt files
are numbered so they read in order — pick the next number in `prompts/`.

## The prompt

```
<The literal text a customer pastes. Real and runnable — no placeholders they
have to figure out, and no internal context they don't have.>
```

## Why it's written that way

Explain the non-obvious choices. This is the part that teaches; the prompt itself is just an
artifact.

- **<Choice>.** <What goes wrong without it.>

## What happens

Which tools get called and in what order. Name them exactly as the server exposes them.

## Verifying the output

How the reader knows it worked, and what a *plausible but wrong* result looks like. Include
the benign explanations — thin results are usually license scope, not a missing library.

## Where this stops working

The limitation that motivates the next rung, and a link to it. Every prompt file should hand
off somewhere.
