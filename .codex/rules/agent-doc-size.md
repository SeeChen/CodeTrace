# Rule 6: Agent Document Size

This rule defines how AI agent markdown files should be structured in the CodeTrace-AI project.

## Purpose

Agent markdown files should remain lightweight and readable. They are intended to act as navigation maps or operating manuals, not as full knowledge bases.

## Guidelines

- Keep each agent markdown file preferably between 80 and 120 lines
- Treat each agent file as a concise map, not a complete specification
- Put detailed background, reference material, examples, and extended workflows in `docs/`
- Load detailed documents only when the current task requires them
- Prefer linking to supporting documents instead of copying large sections into agent files

## Expected Split of Responsibility

- `agents/*.md`: role, mission, inputs, outputs, boundaries, handoff rules
- `docs/*.md`: detailed methodology, extended references, domain knowledge, and long-form explanations

## Anti-Patterns

- Do not turn an agent file into a large reference manual
- Do not duplicate long workflow text that already exists in `docs/`
- Do not embed extensive examples, schemas, or research notes directly in the agent file unless they are essential

## Review Check

Before merging an agent markdown file, verify:

1. The file is still acting as a compact operating guide
2. The file stays roughly within the 80 to 120 line target
3. Detailed material has been moved to `docs/` or another reference file when appropriate

