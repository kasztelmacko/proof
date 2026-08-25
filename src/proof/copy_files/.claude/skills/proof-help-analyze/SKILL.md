---
name: proof-help-analyze
description: Use when the human invokes /proof-help-analyze with a named analysis_plan step, to deepen their thinking on that section before they write notes.
disable-model-invocation: true
---

Coach the human, in conversation only, on one named analysis-plan step so they can write their own notes.

Sources, in this order: the named step in `analysis_context/analysis_plan.md`, then the human's files under `analysis_notes/` for that part (if any), then the question or thoughts in the invoke. Notebook output is only a fact already on screen — use it as source of truth alongside those.

If which step is unclear, ask; then coach. Missing notes are fine: start from their question and the screen.

## Reply

Stay on this step. Start from what they already think. Point to what the visible output supports, contradicts, or leaves open. Name what is still worth putting in their notes.

Do not write `analysis_notes/`, `analysis_overview.md`, or notebook cells. Other skills do that.

This invoke is that coaching. Other asks in the same message wait until after it. One invoke = one step.
