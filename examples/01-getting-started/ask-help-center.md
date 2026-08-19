# Ask a Help Center Question

**Goal:** Get an answer about the Pluralsight platform from official documentation instead of the model's memory.

## Prompt

```text
Using Pluralsight's Help Center, how do I download courses for offline viewing?
```

Variations:

```text
What does my Pluralsight subscription include? Check the Help Center.
```

```text
How do I add users to my Pluralsight team plan?
```

## Tools used

- `query_pluralsight_help_center_index` — semantic search over official Help Center articles covering account management, billing, subscriptions, and platform support.

## What to expect

An answer grounded in Help Center articles, ideally citing which article it came from. Because it searches current documentation, this is more reliable than asking the model directly about Pluralsight policies or features.
