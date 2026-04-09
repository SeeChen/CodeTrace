# Rule 8: System Constraint Language

This rule defines the default language for repository-level AI system constraint files in the CodeTrace-AI project.

## Purpose

System constraint files should use a consistent language so they are easier for AI agents to read, reuse, and compose across workflows.

## Scope

This rule applies to files such as:

- `agents/*.md`
- `skills/**/SKILL.md`
- `commands/*.md`
- `memory/*.md`
- `rules/*.md`

## Guidelines

- Write system constraint files in English by default
- Keep role definitions, instructions, boundaries, and handoff rules in English
- Use English for stable reusable prompts and workflow constraints
- If business requirements or product documents are written in another language, reference them as sources without forcing translation of the source material itself

## Exceptions

- User-facing product documents may follow the language most suitable for the team
- Quotes, file names, and source excerpts may keep their original language when needed
- If a task explicitly requires a bilingual or non-English system constraint file, document that reason clearly

## Review Check

Before merging a system constraint file, verify:

1. The file is written primarily in English
2. Reusable instructions are not mixed across multiple natural languages without reason
3. Source material in another language is referenced cleanly rather than copied into the constraint file in bulk
