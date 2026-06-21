---
description: From a PRD, run the full pipeline then self-iterate an audit/hardening loop until composite quality converges, with user checkpoints.
argument-hint: "[--run | --resume | --max-rounds <n> | --threshold <n>]"
---

# Command: converge

## Purpose

`/converge` drives the project past "all tests pass" toward a composite quality
bar. From a given PRD it runs the baseline active flow, then enters a self-
iterating loop: `audit -> score -> (stop?) -> re-plan -> implement -> verify`.

It is autonomous between checkpoints but pauses for user decisions. Full rubric,
gates, stop conditions, and report layout live in
`.claude/docs/Convergence-Loop.md` — read it before running.

## Direct Invocation

- `/converge --run` — run baseline pipeline (if not done) then start the loop
- `/converge --resume` — resume an in-progress loop from `convergence-state.md`
- `/converge --max-rounds <n>` — override the round budget
- `/converge --threshold <n>` — override the subjective pass threshold

Also reachable as `/seechen --converge`.

## Read First

1. `.claude/docs/Convergence-Loop.md`
2. `.claude/memory/pipeline-state.md`
3. `.claude/memory/convergence-state.md`
4. `.claude/memory/frozen-decisions.md`
5. `specs/build/test-matrix.md`
6. `.claude/agents/audit-agent.md`
7. `.claude/skills/audit-quality/SKILL.md`

## Execution Model

### Phase A — Baseline

1. If `pipeline-state.md` is not `completed`, run the active flow to `accept`
   (delegate to `/seechen --run`).
2. Confirm a green baseline exists before looping.

### Phase B — Enter loop (checkpoint 1)

1. Ensure work is on a `feature/*` branch, never `main`.
2. Ask the user to confirm scope, thresholds, and round budget.
3. Initialize `convergence-state.md`.

### Phase C — Iterate each round

1. **Audit** — run the `audit-quality` skill: measure every objective gate,
   score subjective axes with cited evidence.
2. **Score** — compute the composite; write `specs/audit/round-<n>.md`.
3. **Stop check** — evaluate all stop conditions from the doc. If any holds,
   exit to Phase D.
4. **Checkpoint 2** — show the round summary; ask continue / stop / adjust.
5. **Re-plan** — turn accepted findings into a minimal change set (do not
   reopen frozen decisions; route those to checkpoint 3).
6. **Implement + verify** — apply changes via `/seechen --implement` and
   `/seechen --verify` on a fresh commit.
7. **Regression guard** — if any gate regressed, revert the round and record it.
8. Update `convergence-state.md`; increment the round.

### Phase D — Exit

1. Write a final convergence summary (which stop condition fired, final scores).
2. Update `pipeline-state.md` and `convergence-state.md`.
3. Leave merge to `main` as a user decision (checkpoint 4).

## Checkpoints

- Before the loop: confirm scope / thresholds / budget.
- Each new round: continue / stop / adjust thresholds.
- On audit uncertainty or any frozen-decision impact: present options, let the
  user decide (use `AskUserQuestion`).
- Before merging: never auto-merge.

## Guardrails

- Never loosen a test or gate to raise a score (reward-hacking is forbidden).
- Never accept a round that worsens any objective gate.
- Never treat an unmeasured gate as a pass; record it.
- Never reopen frozen decisions inside the loop without a user checkpoint.
- Always honor plateau and budget stop conditions; the loop must terminate.
- Never commit to `main`; one commit per accepted round on the feature branch.
