This file defines mandatory working rules for agent. Follow these instructions during the analysis session.

# Human-Agent interaction
- The agent is a tool for user to use. It only does what it is asked to do.
- The analysis flow sets human first approach, where the agent is supposed to mostly create code needed for analysis, and anlyse what it sees only when explicitly asked.
- Always give human time to analyse what is visible in the notebook first. Human analyses the data first, only then agent can be invoked with skill `/proof-help-analyze` to further analyse or fill gaps in human thoughts.
- Default and main agent actions during session is code writing in the cells. Main human action is to understand and analyse the data.

## Desired workflow
1. Human specifies which analysis step from `/analysis_context/analysis_plan` to now start.
2. Agent proposes the code cells and general plan
3. Human verifies and approves the plan
4. Agent implements the cells
5. Human verifies and analyses the output
6. Human makes notes in `/analysis_notes/analysis_notes`
7. Human invokes skill `/proof-summarise-step` and agent adds summary of that analysis step to `/analysis_context/analysis_overview/`.