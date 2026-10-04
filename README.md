```
██████╗ ██████╗  ██████╗  ██████╗ ███████╗
██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗██╔════╝
██████╔╝██████╔╝██║   ██║██║   ██║█████╗  
██╔═══╝ ██╔══██╗██║   ██║██║   ██║██╔══╝  
██║     ██║  ██║╚██████╔╝╚██████╔╝██║     
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝     
```

**proof** is a personal agentic workflow for data analysis / data science work. It hands off the coding to the agent, while the user can focus on understanding the data and lead the analysis.
The whole purpose is to enhance the user understanding rather than redirecting the conclusion to the agent.

## Command

`proof init` Create proof root folder \
`proof create <analysis_name>` Create a new analysis \
`proof start <analysis_name> <notebook_name>` Start a marimo notebook session \
`proof add notebook <analysis_name> <notebook_name>` Add a notebook to an analysis \
`proof add symlink <analysis_name> <path>` Symlink a project file into an analysis

## Skill

`/proof-plan` Plan analysis based on user provided context \
`/proof-summarize` Write the summary of currently analyzed step to `analysis_overview.md` \
`/proof-understand` Analyze step or deepen user understanding
