# OBEY Clean Code

This file defines mandatory working rules for agent. Follow these instructions before making any code, refactor, review, or documentation change.

## Priority and behavior

- Treat every unqualified rule in this file as `MUST`; treat `Prefer` as `SHOULD`; treat `Do not`, `Avoid`, and `Never` as `MUST NOT` unless the user explicitly overrides it.
- Prefer readability, maintainability, correctness, and safe change over cleverness or speed hacks.
- Optimize for the next human reader.
- When trade-offs exist, choose the option that reduces long-term complexity.
- Never preserve bad structure just because it already exists.
- Apply the Boy Scout Rule: leave touched code cleaner than you found it.

## Core clean code principles

- Write code primarily for humans, not just for execution.
- Keep code simple, direct, and easy to modify.
- Avoid accidental complexity.
- Avoid surprising behavior.
- Prefer explicit intent over implicit magic.
- Prefer local reasoning: a reader should understand code with minimal jumping across files.
- Reduce technical debt instead of moving it around.
- One notebook cell is for one narrow topic.
- If given analysis part should be viewed in a table and as a plot, those two should be in different cells.

## Naming rules

- Use intention-revealing names.
- Names must explain purpose, role, or behavior without requiring extra comments.
- Avoid misleading names, overloaded meanings, and visually confusable identifiers.
- Make distinctions meaningful. Do not create names that differ only cosmetically.
- Use pronounceable, searchable names.
- Avoid abbreviations unless they are established domain or platform standards.
- Avoid encodings in names, including type prefixes, implementation hints, and Hungarian notation.
- Avoid unnecessary context in identifiers.
- Add context through modules, classes, namespaces, or types when that is cleaner than longer names.
- Use one word per concept across the codebase.
- Do not use multiple synonyms for the same operation or concept.
- Do not reuse a familiar word for a different meaning.
- Class, type, and module names should be nouns or noun phrases.
- Function and method names should be verbs or verb phrases.
- Use problem-domain names for domain concepts.
- Use solution-domain names for technical concepts.
- Do not use cute, funny, cryptic, or private-joke names.
- Do not use short names that are only the first letters of the actual words. Better to name "high_volatility" than "hv".

## Function rules

- Keep functions small.
- Each function must do one thing.
- A function should have one clear reason to change.
- Keep each function at one level of abstraction.
- Organize code top-down so readers see the high-level story before details.
- Prefer descriptive names over short names.
- Minimize the number of parameters.
- Avoid boolean flag parameters. Split behavior into separate functions instead.
- Avoid output parameters unless language conventions make them necessary.
- Eliminate hidden side effects.
- Separate commands from queries.
- A function that answers a question should not also mutate state.
- Prefer exceptions or explicit result types over ad hoc error codes, according to project language norms.
- Isolate error handling from main logic.
- Eliminate duplication aggressively.
- Prefer straightforward control flow over clever control flow.
- Refactor deep nesting into clearer structure.

## Comment rules

- Do not use comments inside any cell unless it is necessary to understand that cell.
- Do not use comments to compensate for bad naming or bad structure.
- First improve the code, then decide whether a comment is still needed.
- Prefer self-explanatory code.
- Remove redundant, obsolete, obvious, noisy, and misleading comments.
- Do not narrate the code line by line.

## Formatting and structure

- Use consistent formatting across the repository.
- Format code to reveal structure and intent.
- Keep related concepts close together.
- Keep files, classes, and functions reasonably small.
- Use vertical ordering to tell the story from higher level to lower level.
- Use indentation to clarify scope, not to hide complexity.
- Avoid excessive line length when it hurts readability.
- Avoid decorative alignment that is brittle during edits.
- Preserve a layout that supports fast scanning.

## Objects, modules, and data structures

- Separate behavior-rich objects from plain data carriers intentionally.
- Do not mix data containers and business behavior arbitrarily.
- Hide implementation details behind clear interfaces.
- Expose behavior, not representation.
- Use DTO-like structures as simple carriers when appropriate.
- Avoid train-wreck call chains and unnecessary knowledge of internal structure.
- Respect loose coupling and local boundaries.
- Keep persistence, framework, and third-party details from obscuring business behavior or core logic.

## Class and module design

- Keep classes and modules small.
- Each class or module should have one primary responsibility.
- Favor high cohesion.
- Split classes that accumulate unrelated behavior.
- Organize code so likely changes remain local.
- Public APIs should be small, obvious, and hard to misuse.
- Prefer composition over complex inheritance unless inheritance is clearly the simpler and more stable model.
- Keep constructors and setup logic from overwhelming domain behavior.


## Boundaries and external dependencies

- Isolate third-party libraries behind local adapters or wrappers when practical.
- Avoid coupling core logic directly to unstable external APIs.
- Create narrow interfaces around dependencies.
- When a dependency does not exist yet, define interfaces from local needs, not from guesses about future implementations.

## System construction rules

- Separate constructing a system from using it.
- Keep object graph assembly, dependency injection, factories, and framework bootstrapping out of ordinary business behavior.
- Put startup wiring in an explicit main or composition area.
- Use factories when construction policy is meaningful or complex.
- Do not let cross-cutting concerns obscure ordinary code flow.
- Use standards, frameworks, proxies, or AOP-style mechanisms only when they add demonstrable value.
- Test-drive architectural decisions with executable slices, not only diagrams or configuration.
- Use domain-specific languages only when they make system intent clearer than general-purpose code.

## Tests

- Dont add tests inside the current session. We are analysing data, not creating an app.


## Implementation preferences

- Prefer explicit, boring, maintainable solutions.
- Prefer standard library and existing project patterns over new dependencies.
- Reuse established project conventions unless they conflict with these rules or the user explicitly asks otherwise.
- For data / statistics / data science analysis dont build own tools unless needed. Always prefer tools built externaly.
- Keep interfaces small.
- Keep state transitions obvious.
- Avoid premature optimization.
- Optimize only when there is evidence or a known requirement.


## Hard rules

- Do not introduce misleading names.
- Do not keep duplicated logic without a strong reason.
- Do not add comments where better code would remove the need.
- Do not mix querying with mutation without a strong reason.
- Do not silently broaden scope beyond the requested task.
- Do not leave touched code less readable than before.