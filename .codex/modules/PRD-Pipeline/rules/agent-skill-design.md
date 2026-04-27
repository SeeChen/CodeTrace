# Rule: Agent and Skill Design

This rule defines how `agents/*.md` and `skills/*/SKILL.md` should be designed in the PRD-Pipeline workflow.

## Purpose

Agents and skills are navigation assets. They should point AI toward the right materials and decisions without trying to contain the entire knowledge base in one file.

The goal is to keep them:

- compact
- composable
- easy to scan
- safe to load on demand
- efficient in context usage

## Core Principle

An agent or skill file should behave like a map, not like a warehouse.

It should define:
- what this asset is for
- when to use it
- what inputs it expects
- what outputs it should produce
- what supporting documents it should load when needed

It should not try to inline all reference material, examples, schemas, or background explanations.

## Size Guidance

The preferred size target for each agent markdown file is between 80 and 120 lines.

The same guidance should be applied to skill files whenever possible. A skill file may be slightly longer when it needs a compact execution procedure, but it should still stay intentionally small.

If a file keeps growing, move detailed material into supporting documents under `docs/` and link to them.

## Split of Responsibility

### Agents

Agent files should mainly contain:

- role and mission
- ownership boundary
- input sources
- output expectations
- handoff rules
- escalation conditions

### Skills

Skill files should mainly contain:

- trigger conditions
- required inputs
- execution steps
- expected outputs
- guardrails
- references to deeper material

### Docs

Detailed reference content should live under `docs/`.

Examples include:

- extended methodology
- domain references
- long examples
- schemas
- decision records
- workflow explanations
- comparison tables

## On-Demand Loading Rule

Agents and skills should load supporting documents only when the current task needs them.

This means:

1. do not preload all references by default
2. do not duplicate large sections from supporting docs
3. prefer short references to specific documents or sections
4. keep the execution asset readable even without opening every linked document

## Anti-Patterns

Avoid the following:

1. a single agent file that contains the entire workflow, all examples, and all reference notes
2. a skill file that embeds full schemas, full templates, and long rationale sections
3. repeated copying of the same content across agents, skills, and docs
4. turning orchestration files into a substitute for the real documentation set

## Review Checklist

Before adding or updating an agent or skill file, verify:

1. the file still acts like a map
2. the file remains concise
3. detailed material has been moved to `docs/` where appropriate
4. the asset can be used with selective, on-demand reading
5. the file helps reduce context cost rather than increase it

## Recommendation

When in doubt, shorten the agent or skill file and strengthen the supporting documents instead.
