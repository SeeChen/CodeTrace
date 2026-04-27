# Workflow Memory

## Active Principle

The repository now follows a delivery-oriented PRD workflow:

`PRD -> intent -> architecture -> build -> tasks -> coding -> verify -> accept`

## Stable Rules

1. `docs/PRD.md` is the primary product source of truth.
2. Architecture must be frozen before build-spec generation.
3. Build specs must be frozen before coding starts.
4. Coding should follow task slices instead of broad PRD reinterpretation.
5. Open questions must be written down instead of silently guessed.
6. Agents and skills should stay lightweight and load deeper docs only on demand.

## Active Reusable Assets

- `/prd-pipeline`
- `/pipeline-init`
- `/generate-sa`
- `/generate-spec`
- `/slice-work`
- `/implement`
- `/verify`
- `/accept`
- `PRD-Pipeline Refactor Blueprint`
- `Agent and Skill Design` rule
- workflow memory files under `.codex/modules/PRD-Pipeline/memory/`

## Active Output Focus

The primary target outputs are:

1. `specs/intent/brief.md`
2. `specs/architecture/SA.md`
3. `specs/build/*`
4. `specs/build/tasks.md`
5. `specs/acceptance/report.md`

## Resume Principle

Long-running workflow execution must resume from repository artifacts, especially:

- `.codex/modules/PRD-Pipeline/memory/pipeline-state.md`
- `.codex/modules/PRD-Pipeline/memory/frozen-decisions.md`
- `.codex/modules/PRD-Pipeline/memory/open-questions.md`
- `.codex/modules/PRD-Pipeline/memory/implementation-log.md`

## Migration Note

Legacy generated `specs/` outputs may still be used as supporting review material, but the active pipeline assets no longer expose the removed legacy stage model.
