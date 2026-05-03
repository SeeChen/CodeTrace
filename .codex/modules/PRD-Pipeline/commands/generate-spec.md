# Command: generate-spec

## Purpose

Generate the build-spec layer from the normalized intent pack and system architecture.

## Direct Invocation

- `/generate-spec`
- `/generate-spec --refresh`

## Read First

1. `specs/intent/brief.md`
2. `specs/architecture/SA.md`
3. `.codex/modules/PRD-Pipeline/skills/generate-build-spec/SKILL.md`
4. `.codex/modules/PRD-Pipeline/memory/frozen-decisions.md`

## Execute

1. Translate architecture into implementation-facing contracts.
2. Write the required `specs/build/*` files.
3. Record frozen contracts and unresolved issues.
4. Update `memory/pipeline-state.md`.

## Output

- `specs/build/module-map.md`
- `specs/build/interfaces.md`
- `specs/build/file-plan.md`
- `specs/build/artifact-schema.md`
- `specs/build/failure-policy.md`
- `specs/build/test-matrix.md`
