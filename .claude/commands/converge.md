---
description: From a PRD, run the full pipeline then drive an unattended audit/hardening loop until composite quality converges, pausing only at escalation points. Repetition is delegated to a native scheduler; this command supplies the goal and per-round policy.
argument-hint: "[--run | --auto | --attended | --resume | --max-rounds <n> | --threshold <n>]"
---

# Command: converge

## Purpose

`/converge` drives the project past "all tests pass" toward a composite quality
bar via the loop: `audit -> score -> (stop?) -> re-plan -> implement -> verify`.

It is the **goal + per-round policy** layer, not a scheduler. Repetition is owned
by a native driver (`/loop` or `ScheduleWakeup`); `/converge` never implements its
own timer or repeat mechanism. `--resume` runs **exactly one round** and reports
whether another round should follow. This keeps a clean split:

- **Driver (native):** how to repeat / self-pace / survive across turns.
- **`/converge` (this file):** what one round does, what "done" means, when to
  escalate.

Full rubric, gates, stop conditions, and report layout live in
`.claude/docs/Convergence-Loop.md` — read it before running.

## Direct Invocation

- `/converge --run` — run baseline pipeline (if needed), set up state, then hand
  the loop to the driver
- `/converge --auto` — unattended mode (default): escalation-only pauses
- `/converge --attended` — pause for continue/stop/adjust after each round
- `/converge --resume` — run **one** round from `convergence-state.md`, then stop
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

- The loop repeats until a stop condition fires (converged / plateau / budget /
  hard-blocker) or the user halts it.
- Pause and ask the user **only** at escalation points (see Checkpoints).

`--attended` restores a per-round continue/stop/adjust gate for supervised runs.

## Driver (repetition is not this command's job)

`/converge` does not loop by itself. One round = one `--resume`. The native driver
repeats it:

- **Launch:** `/loop /converge --resume` (model self-paces each round), or
  schedule the next round with `ScheduleWakeup` firing `/converge --resume`.
- **Continue signal:** each round ends by writing `Next Round Scheduled: yes|no`
  to `convergence-state.md`. `yes` means the driver should fire another
  `--resume`; `no` means a stop condition fired — the driver stops scheduling.
- **Termination = stop scheduling.** There is no separate kill switch; the loop
  ends precisely when a round reports `no`.

This separation is why the command is not redundant with `/loop`: `/loop` knows
how to repeat, `/converge` knows what to repeat and when to quit.

## Execution Model

### Phase A — Baseline (`--run` only)

1. If `pipeline-state.md` is not `completed`, run the active flow to `accept`
   (delegate to `/seechen --run`).
2. Confirm a green baseline exists before looping.

### Phase B — Set up + hand off (`--run` only, one-time checkpoint)

1. Ensure work is on a `feature/*` branch, never `main`.
2. Confirm scope, thresholds, budget, and mode **once**.
3. Initialize `convergence-state.md` (Loop Status `running`, round `0`, mode).
4. Hand the loop to the driver (`/loop /converge --resume` or a scheduled
   `--resume`). Do not run rounds inline as a hand-written repeat.

### Phase C — One round (the loop body, `--resume`)

Idempotent and safe to re-fire. A round does exactly this, then returns:

1. **Read** `convergence-state.md`; determine the next round number `n`.
2. **Audit** — run the `audit-quality` skill: measure every objective gate,
   score subjective axes with cited evidence.
3. **Score** — compute the composite; write `specs/audit/round-<n>.md`.
4. **Stop check** — evaluate all stop conditions. If any holds, go to step 8
   with `no`.
5. **Re-plan** — turn accepted findings into a minimal change set. If a finding
   needs a frozen-decision change, an API change, or is genuinely ambiguous,
   **escalate** (pause and ask) instead of guessing.
6. **Implement + verify** — apply changes via `/seechen --implement` and
   `/seechen --verify` on a fresh commit.
7. **Regression guard** — if any objective gate regressed, revert the round and
   record "regression rejected".
8. **Write state + signal** — update `convergence-state.md` (round result, score
   history, `Next Round Scheduled: yes|no`, and `Stop Reason` when `no`). Return.

The round does not start round `n+1` itself; the driver decides based on the
signal. (`--attended` adds a continue/stop/adjust checkpoint before returning.)

### Phase D — Exit (when a round signals `no`)

1. Write a final convergence summary (which stop condition fired, final scores).
2. Set Loop Status + Stop Reason in `convergence-state.md`; update
   `pipeline-state.md`.
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

- Do not implement a custom scheduler / timer / retry loop; delegate repetition
  to the native driver.
- One round per `--resume`; keep it idempotent so a re-fire cannot double-apply.
- Never loosen a test or gate to raise a score (reward-hacking is forbidden).
- Never accept a round that worsens any objective gate.
- Never treat an unmeasured gate as a pass; record it.
- Never reopen frozen decisions inside the loop without an escalation checkpoint.
- Always honor plateau and budget stop conditions; the loop must terminate.
- Never commit to `main`; one commit per accepted round on the feature branch.
- An unattended loop must still escalate on genuine ambiguity, not guess.
