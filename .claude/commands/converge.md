---
description: From a PRD, run the full pipeline then self-iterate an unattended audit/hardening loop until composite quality converges, pausing only at escalation points.
argument-hint: "[--run | --auto | --attended | --resume | --max-rounds <n> | --threshold <n>]"
---

# Command: converge

## Purpose

`/converge` drives the project past "all tests pass" toward a composite quality
bar. From a given PRD it runs the baseline active flow, then enters a self-
iterating loop: `audit -> score -> (stop?) -> re-plan -> implement -> verify`.

By default the loop runs **unattended**: it advances round to round on its own
and pauses only at escalation points or a stop condition. This is the loop-
engineering `/goal` model — the loop decides when it is finished. Full rubric,
gates, stop conditions, and report layout live in
`.claude/docs/Convergence-Loop.md` — read it before running.

## Direct Invocation

- `/converge --run` — run baseline pipeline (if not done) then start the loop
- `/converge --auto` — unattended loop (default): self-advance, escalation-only pauses
- `/converge --attended` — pause for continue/stop/adjust at every round
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

## Autonomy Model

Default mode is **unattended + escalation** (`--auto`):

- After an accepted round, **proceed to the next round automatically** — do not
  wait for user input.
- The loop runs until a stop condition fires (converged / plateau / budget /
  hard-blocker) or the user halts it.
- Pause and ask the user **only** at escalation points (see Checkpoints).

`--attended` restores a per-round continue/stop/adjust gate for supervised runs.

## Driver

The loop self-advances using a native scheduling primitive so it survives across
turns without a human pressing enter:

- **In-session**: after writing round-`n` state, immediately begin round-`n+1`
  unless a stop condition or escalation holds.
- **Unattended / long-running**: launch via `/loop /converge --resume` (model
  self-paces each round) or schedule the next round with `ScheduleWakeup` firing
  `/converge --resume`. **Termination = stop scheduling**: when a stop condition
  fires, do not schedule the next round and exit to Phase D.

## Execution Model

### Phase A — Baseline

1. If `pipeline-state.md` is not `completed`, run the active flow to `accept`
   (delegate to `/seechen --run`).
2. Confirm a green baseline exists before looping.

### Phase B — Enter loop (one-time checkpoint)

1. Ensure work is on a `feature/*` branch, never `main`.
2. Confirm scope, thresholds, round budget, and autonomy mode **once** before
   launching. After this the loop runs unattended.
3. Initialize `convergence-state.md` (set Loop Status `running`, record mode).

### Phase C — Iterate each round (unattended)

1. **Audit** — run the `audit-quality` skill: measure every objective gate,
   score subjective axes with cited evidence.
2. **Score** — compute the composite; write `specs/audit/round-<n>.md`.
3. **Stop check** — evaluate all stop conditions. If any holds, exit to Phase D.
4. **Re-plan** — turn accepted findings into a minimal change set. If a finding
   needs a frozen-decision change, an API change, or is genuinely ambiguous,
   **escalate** (pause and ask) instead of guessing.
5. **Implement + verify** — apply changes via `/seechen --implement` and
   `/seechen --verify` on a fresh commit.
6. **Regression guard** — if any objective gate regressed, revert the round and
   record "regression rejected".
7. Update `convergence-state.md`; increment the round; **advance automatically**.

### Phase D — Exit

1. Write a final convergence summary (which stop condition fired, final scores).
2. Update `pipeline-state.md` and `convergence-state.md` (Loop Status + reason).
3. Leave merge to `main` as a user decision (final checkpoint).

## Checkpoints

The unattended loop pauses only here:

- **Before the loop** — confirm scope / thresholds / budget / mode once.
- **On escalation** — a finding touches a frozen decision or public API, a fix
  is a genuine design trade-off, or an objective gate cannot be measured.
  Present options with `AskUserQuestion` and let the user decide.
- **Before merging** — never auto-merge to `main`.

(`--attended` adds a per-round continue/stop/adjust pause on top of these.)

## Guardrails

- Never loosen a test or gate to raise a score (reward-hacking is forbidden).
- Never accept a round that worsens any objective gate.
- Never treat an unmeasured gate as a pass; record it.
- Never reopen frozen decisions inside the loop without an escalation checkpoint.
- Always honor plateau and budget stop conditions; the loop must terminate.
- Never commit to `main`; one commit per accepted round on the feature branch.
- An unattended loop must still escalate on genuine ambiguity, not guess.
