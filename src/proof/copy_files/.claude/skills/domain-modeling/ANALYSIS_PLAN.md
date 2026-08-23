# Analysis Plan Format

## Structure

```md
# {Analysis name}

{One or two sentences: what this analysis is for.}

## Steps

### {Step name}

**Question**: {the analysis question or hypothesis}

**Notes**:
- {synthesized settled decision}
```

## A step

Every step has three parts, in this order:

1. **Name** — short heading (`### Cohort window`)
2. **Question** — the analysis question or hypothesis (`**Question**:`)
3. **Notes** — synthesized grilling decisions (`**Notes**:`)

Write the name and question as soon as the question is identified. Include the **Notes**: heading even when nothing is settled yet. Fill Notes later.

```md
### Cohort window

**Question**: Does churn concentrate in the first 14 days after signup?

**Notes**:
```

After grilling settles decisions for that step:

```md
### Cohort window

**Question**: Does churn concentrate in the first 14 days after signup?

**Notes**:
- Scope: paid signups only, last 12 months
- Method: survival curve with a 14-day cutoff
- Success: if ≥60% of churn events fall inside the window
```

## Rules

- **One step = one analysis question/hypothesis.** Not a glossary term, not a verified fact (table names, file paths), not a grilling frontier question.
- **Stub first.** Create the step when the question is identified. Don't wait until grilling of that question is done.
- **Notes are synthesized.** Scope, method, data, success criteria, caveats. Not a transcript, not a quote of the user's answer.
- **A grilling decision is Notes, not a new step**, unless it is itself a question the analysis must answer. "Paid-only vs all signups" belongs under the step it constrains.
- **Append steps in the order questions are identified.** Don't batch until the session ends.
- **Don't put any of this in `CONTEXT.md`.** That file is the glossary.
