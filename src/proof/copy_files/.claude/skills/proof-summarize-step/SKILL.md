---
name: proof-summarize-step
description: Use when the human invokes /proof-summarize-step or /proof-summarise-step after they have inspected notebook output and written notes for the current analysis_plan step.
disable-model-invocation: true
---

Append one completed analysis-plan step to `analysis_context/analysis_overview.md`.

Sources, in this order: the named step in `analysis_context/analysis_plan.md`, then the human's files under `analysis_notes/`. Notebook output is only a fact already on screen — do not interpret it.

If notes for this step are missing, ask the human to write them; write no files yet.
If which step is unclear, ask; then write.

## Entry

Append this block. Leave every earlier heading untouched.

```md
### {Step name}

**Question**: {from analysis_plan}

**Summary**:
- {what the cells did, one line}
- {what the human concluded, from their notes}
```

This invoke is that entry. Other asks in the same message wait until after it is written. One invoke = one new `###` heading, for the current step only.
