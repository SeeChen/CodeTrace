# Workflow Memory

## Active Principle

The repository follows a delivery-oriented PRD workflow:

`PRD -> intent -> architecture -> build -> tasks -> coding -> verify -> accept`

## Stable Rules

1. `docs/PRD.md` is the primary product source of truth.
2. Architecture must be frozen before build-spec generation.
3. Build specs must be frozen before coding starts.
4. Coding should follow task slices instead of broad PRD reinterpretation.
5. Open questions must be written down instead of silently guessed.
6. Agents and skills should stay lightweight and load deeper docs only on demand.

## Active Reusable Assets

- `/seechen` (unified entry point; `/prd-pipeline` is a deprecated alias)
- stage commands: `/pipeline-init`, `/generate-sa`, `/generate-spec`, `/slice-work`, `/implement`, `/verify`, `/accept`
- skills: `normalize-prd`, `generate-sa`, `generate-build-spec`, `slice-build-tasks`, `implement-from-task`, `verify-build`, `accept-milestone`
- agents: `prd-analyst-agent`, `architect-agent`, `spec-builder-agent`, `coding-agent`, `qa-acceptance-agent`
- workflow memory files under `.claude/memory/`

## Active Output Focus

The primary target outputs are:

1. `specs/intent/brief.md`
2. `specs/architecture/SA.md`
3. `specs/build/*`
4. `specs/build/tasks.md`
5. `specs/acceptance/criteria.md` and `specs/acceptance/report.md`

## Resume Principle

Long-running workflow execution must resume from repository artifacts, especially:

- `.claude/memory/pipeline-state.md`
- `.claude/memory/frozen-decisions.md`
- `.claude/memory/open-questions.md`
- `.claude/memory/implementation-log.md`
