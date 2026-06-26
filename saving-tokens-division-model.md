# Model Division — Save Tokens, Cut Costs

A three-tier routing strategy for AI-assisted projects. Route every task to the
cheapest model that can handle it correctly. Most tasks never need a cloud API.

---

## The Three Tiers

| Tier | Model | Runs where | Cost |
|------|-------|-----------|------|
| 1 — Parse & extract | **Gemma 4** | Local (Ollama) | Free |
| 2 — Code & calculate | **Qwen3-Coder** | Local (Ollama) | Free |
| 3 — Reason & summarize | **Claude Sonnet** | Anthropic API | Paid |

> **Rule of thumb**: if the task is mechanical (extract, validate, transform, count),
> it stays local. Only send to Claude when you genuinely need judgment.

---

## When to Use Each Model

### Tier 1 — Gemma 4 (parse & extract)

Use for any task where the model only needs to recognize structure, not understand meaning:

- Parsing raw data exports (CSV, JSON, XML, PDF text, bank statements)
- Extracting fields from unstructured text (dates, amounts, names, categories)
- Validating schema correctness (required fields present, types correct)
- Deduplicating records by key
- Simple classification: income vs. expense, active vs. inactive, etc.
- Currency or unit normalization
- Formatting output into a target JSON schema

**Gemma does not need to understand the domain — only to extract and structure.**

Example prompt pattern:
```
Extract all [ITEMS] from the following [SOURCE TYPE].
Return ONLY a JSON array. Each item: {"field1": type, "field2": type, ...}
Do not explain. Do not add commentary.

[RAW DATA]
```

---

### Tier 2 — Qwen3-Coder (code & calculate)

Use whenever the task is fundamentally "write code to do X" or "compute Y":

- Writing Python/JS/SQL scripts for data pipeline steps
- Aggregating totals by category, time period, or dimension
- Computing deltas, percentages, running totals
- Generating SQL queries
- Building data transformation logic
- Any arithmetic or statistical operation over structured data

**Do not ask Claude to write utility code. That belongs here.**

Example prompt pattern:
```
Write a [LANGUAGE] function that receives [INPUT DESCRIPTION].
Returns [OUTPUT DESCRIPTION].
Input schema: [SCHEMA]
Return only the function, no explanation.
```

---

### Tier 3 — Claude Sonnet (reason & summarize)

Use only when the task requires genuine judgment, context, or user-facing prose:

- Interpreting aggregated results and drawing conclusions
- Detecting anomalies that require domain context
- Generating summaries and recommendations for a human reader
- Making decisions that depend on the project's full context
- Answering open-ended questions where the answer isn't computable

**At this point, data must already be structured and aggregated. Never send raw data.**

Example prompt pattern (what Claude should receive — clean, compact):
```
[DOMAIN] summary ([TIME PERIOD]):
- Metric A: [value]
- Metric B: [value] (over/under target by [delta])
- Notable: [2-3 bullet facts]

[QUESTION OR REQUEST]
```

---

## Pipeline Flow

```
Raw input (CSV / JSON / PDF / API response)
        |
    [Gemma 4]
    Extract → structured JSON
        |
    [Qwen3-Coder]
    Aggregate → calculations → code outputs
        |
    [Claude Sonnet]
    Analyze → user-facing summary / recommendation
```

Each stage hands off a **smaller, cleaner payload** to the next.
Claude receives hundreds of tokens, not thousands.

---

## Decision Tree

```
New task arrives
    |
    ├── Is it: extract / parse / validate / deduplicate / format?
    |       → Gemma 4
    |
    ├── Is it: write code / compute / aggregate / transform?
    |       → Qwen3-Coder
    |
    └── Is it: interpret results / explain / recommend / summarize for a human?
            → Claude Sonnet  (only after Gemma + Qwen3 have already processed)
```

---

## Hard Rules

1. **Never send raw data to Claude Sonnet.** Pre-process with Gemma first.
2. **Never ask Claude Sonnet to write utility code.** That is Qwen3-Coder's job.
3. **Gemma output must be valid JSON** before passing downstream. Validate before proceeding.
4. **Qwen3-Coder output is executable code** — run it locally, pass the result forward.
5. **Keep Claude Sonnet prompts short.** Target: < 500 tokens in, < 300 tokens out.
6. **A failed local model is a retry, not a fallback to Claude.** Fix the prompt, not the tier.

---

## Token Budget Targets

| Stage | Model | Target |
|-------|-------|--------|
| Parsing raw data | Gemma (local) | Unlimited — free |
| Aggregation code | Qwen3-Coder (local) | Unlimited — free |
| Final analysis | Claude Sonnet | < 500 tokens input |
| User summary | Claude Sonnet | < 300 tokens output |

**Goal: Claude Sonnet sees < 800 tokens per full pipeline run.**

---

## Adapting to a New Project

When you copy this pattern to a new project:

1. **Replace the models** if your local stack is different — the routing logic stays the same.
   The tiers are: *dumb-but-fast extractor* → *code generator* → *reasoning model*.

2. **Define your JSON schema** for Tier 1 output before writing any prompts.
   Everything downstream depends on that contract.

3. **Write Tier 2 aggregators first**, before connecting Tier 3.
   Claude should never see raw Tier 1 output.

4. **Set a token budget target for Claude upfront** (e.g., 800 tokens/run).
   Design backward from that limit.

5. **Log what each tier receives and returns** during development.
   It reveals where tokens are wasted and where the pipeline breaks.

---

## Example: Finance Pipeline (this repo)

| Step | Model | Task |
|------|-------|------|
| 1 | Gemma 4 | Parse bank export CSV → structured transactions JSON |
| 2 | Qwen3-Coder | Aggregate by category, compute budget vs. actual |
| 3 | Claude Sonnet | Interpret monthly summary, flag overspend, suggest action |

Claude sees only: `{ income: X, expenses: {cat: Y}, budget_delta: Z, top_overspend: ... }`
