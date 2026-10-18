This file defines mandatory working rules for the analysis session.

# Roles
- The human inspects the notebook and writes notes. The human approves a cell brief before any cells are written.
- The harness only routes. It does not plan, write cells, coach, or edit the overview.
- The planner grills the analysis and writes `CONTEXT.md` and `analysis_context/analysis_plan.md`. When asked, it writes a cell brief for one named step and does not edit the notebook.
- The coder writes notebook cells only from an approved brief, through the live marimo session.
- The summarizer coaches on one step when asked to understand, and appends one overview entry when asked to summarize. It reads the notebook and does not change it.

## Desired workflow
1. Human invokes `/proof-plan`. The harness delegates to the planner until the plan is confirmed.
2. Human names a step from `analysis_context/analysis_plan.md`. The planner proposes the cells. The human approves that brief.
3. The coder implements the approved brief.
4. Human inspects the output and writes notes in `analysis_notes/analysis_notes.md`.
5. Human invokes `/proof-understand`. The summarizer coaches on that step and writes no files.
6. Human invokes `/proof-summarize`. The summarizer appends that step to `analysis_context/analysis_overview.md`.
