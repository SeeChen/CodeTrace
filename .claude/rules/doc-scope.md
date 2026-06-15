# Rule: Artifact Scope from Project Boundary

This rule defines how AI agents should decide which artifacts to generate in the active delivery pipeline.

## Purpose

The active flow `PRD -> intent -> architecture -> build -> tasks -> coding -> verify -> accept` and its artifact layout are reference patterns. AI agents must decide the actual artifact set from the current project's PRD and intent brief, not from a fixed checklist.

## Guidelines

- Read `docs/PRD.md` and `specs/intent/brief.md` before choosing the artifact set
- Identify project scale, system shape, complexity drivers, and delivery goals first
- Use the workflow's target layout as a baseline pattern, not as a mandatory checklist
- Generate only the build-spec artifacts the current project can justify
- Expand the build-spec set when the project clearly requires more structure
- Merge or omit artifacts when a smaller project does not justify full separation

## Required Questions

Before generating an artifact set, answer:

1. What kind of system is this?
2. How complex is the implementation surface?
3. Which constraints or risks justify additional artifacts?
4. Which baseline artifacts are unnecessary for the current milestone?
5. Which missing artifacts are needed because of the actual project shape?

## Expected Output Behavior

- Mark artifacts as required, optional, deferred, or unnecessary
- Explain why each major artifact exists
- Explain why each omitted or merged artifact is acceptable
- Keep every generated artifact traceable to upstream inputs (`brief.md`, `SA.md`, `specs/build/*`)

## Anti-Patterns

- Do not copy the target artifact layout without analysis
- Do not generate artifacts only because they appear in the reference layout
- Do not omit important artifacts just to keep the tree small
- Do not generate build-spec detail before the architecture in `SA.md` is frozen
