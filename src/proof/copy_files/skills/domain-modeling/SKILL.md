---
name: domain-modeling
description: Use when discussing codebase terminology, editing CONTEXT.md, capturing analysis questions or hypotheses, or writing analysis_plan.md.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline — challenging terms, inventing edge-case scenarios, and writing glossary entries and analysis questions down the moment they crystallise. (Merely *reading* `CONTEXT.md` for vocabulary is not this skill. This skill is for when you're changing the model or the analysis plan, not just consuming them.)

## During the session

Write to files lazily — only when you have something to write. Two files, two jobs:

| File | Write when | Never |
|------|------------|-------|
| `CONTEXT.md` | A glossary term or project explainer crystallises | Analysis questions, hypotheses, method, scope, success criteria |
| `analysis_context/analysis_plan.md` | An analysis question/hypothesis is identified, or grilling settles a note on one | Glossary terms |

An empty `analysis_plan.md` is the plan file, not unused scaffold. A second file is the split, not a problem. The user saying "keep one working doc" or "capture notes at the end" does not move analysis questions into `CONTEXT.md`.

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` is a glossary and project explainer — nothing else. Do not treat it as a spec, a scratch pad, a home for "Open questions", or a place for analysis scope/method.

### Update analysis_plan.md inline

When an analysis question or hypothesis is identified, write a step stub to `analysis_context/analysis_plan.md` right there. Don't batch. Don't wait until grilling ends.

A step is a question the analysis itself must answer. Grilling frontier questions are not steps; when they settle, they become Notes on the step they belong to.

When grilling later settles a decision for an existing step (scope, method, data, success criteria, caveats), append it as synthesized Notes. Use the format in [ANALYSIS_PLAN.md](./ANALYSIS_PLAN.md).

## File mix-ups

| Excuse | Reality |
|--------|---------|
| "CONTEXT.md is the working doc" | Glossary only. Questions go in `analysis_plan.md`. |
| "project scope belongs in CONTEXT.md" | Analysis scope/method is Notes on a step, not glossary. |
| "analysis_plan.md is empty scaffold" | Empty means write the first step now. |
| "a second file splits the record" | The split is the design. |
| "user said keep one file / capture at the end" | Still write the right file as it happens. |
| "I'll dump the plan when grilling finishes" | Stub the question when it is identified. |

## Red flags

- Analysis questions under CONTEXT.md headings like "Open questions"
- Method, scope, or success criteria in CONTEXT.md
- Waiting until the session ends to write `analysis_plan.md`
- Treating empty `analysis_plan.md` as unused
- Pasting grilling transcripts into Notes
