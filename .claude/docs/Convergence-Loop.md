# Convergence Loop — Reference

This document defines the self-iterating hardening loop that runs after the
baseline active flow (`PRD -> ... -> Accept`) produces a passing milestone.

It is the detailed reference (the "warehouse"). The command, skill, and agent
files stay compact and link here on demand.

## Why This Exists

A green test suite proves the code does what the current tests check. It does
not prove the code is hard to break, easy to extend, or free of latent defects.
The convergence loop keeps iterating *after* "all pass" to raise a composite
quality bar, while staying safe and terminating reliably.

## Where It Sits

```
PRD -> Intent -> SA -> Build Spec -> Tasks -> Implement -> Verify -> Accept
                                                                       |
                                                                       v
                                              [ CONVERGENCE LOOP starts ]
              audit -> score -> (stop?) -> re-plan -> implement -> verify -> audit ...
```

The loop reuses existing stages (`implement`, `verify`) for changes and adds one
new stage, `audit`, plus a controller that decides whether to continue.

## The Composite Score

The score is **mostly machine-checkable**. LLM judgement is a minority weight and
must cite evidence. This is the single most important safeguard against the loop
inflating its own grade or churning forever.

### Objective gates (machine-checkable — the majority of the score)

| Gate | Tool (use what is available) | Pass condition |
| --- | --- | --- |
| Tests green | `pytest` | 100% pass, 0 errors |
| Coverage | `coverage` (or `pytest-cov`) | line >= 95%, no core module < 90% |
| Self-regression | mutation testing: `mutmut` / `cosmic-ray` | mutation score >= target (start 70%) |
| Lint / style | `ruff` (or `flake8`) | 0 errors |
| Types | `mypy` | 0 errors on `src/` |
| Complexity | `radon cc` | no block worse than grade C |
| Property tests | `hypothesis` (where applicable) | declared properties hold |

Tool availability mirrors how the baseline run handled `pytest-cov`: if a tool is
not installed, try to install it; if it cannot be installed, **record the gap in
the round report and mark that gate `unmeasured`** rather than silently skipping
or faking a pass.

### Subjective axes (LLM-judged — minority weight, capped)

- **Extensibility** — can a new adapter / compare / record strategy be added
  without editing core? Score against the SA extension points, with a concrete
  example diff sketch as evidence.
- **Maintainability** — naming, cohesion, docstrings, failure-isolation clarity.

Each subjective score must quote specific files/lines as justification. A score
without evidence is treated as `unscored`, not as a high score.

### Scoring weights (default; tune in this file, not in code)

- Objective gates: 70% of composite
- Subjective axes: 30% of composite, and the loop **cannot terminate on subjective
  score alone** — every objective gate must also be `pass` or justified `n/a`.

## Stop Conditions

The loop ends when **any** of these is true:

1. **Converged** — all objective gates `pass` (or justified `n/a`) AND every
   subjective axis >= threshold (default 8/10).
2. **Plateau** — composite score shows no net improvement for `N` consecutive
   rounds (default `N = 2`). Stop and report diminishing returns.
3. **Budget** — `max_rounds` reached (default 6).
4. **User halt** — the user declines to continue at a checkpoint.
5. **Hard blocker** — an objective gate cannot be measured and cannot be made
   measurable; stop and escalate.

## Regression Guard

Every round runs on its own commit.

- If a round makes **any** objective gate worse than the previous round, the
  round's change is **reverted** (the commit is rolled back) and the finding is
  recorded as "regression rejected".
- A round may only be accepted if it improves at least one axis and worsens none.

## Human-in-the-Loop Checkpoints

The loop is autonomous but not unattended. It must pause and ask the user:

1. **Before entering the loop** — confirm scope and the score thresholds to use.
2. **At the start of every new round** — show last round's report summary and
   ask "continue / stop / adjust thresholds".
3. **On audit uncertainty** — when a finding's severity or the right fix is
   genuinely ambiguous (e.g. a design trade-off, an API change, anything that
   would touch a frozen decision), present options and let the user decide
   instead of guessing.
4. **Before any merge to `main`** — the loop never merges on its own.

Use `AskUserQuestion` for checkpoints 2 and 3 so the choice is explicit.

## Per-Round Report

Each round writes `specs/audit/round-<n>.md` containing:

- round number, timestamp, base commit
- gate-by-gate result table (value + pass/fail/unmeasured)
- subjective scores with cited evidence
- composite score and delta vs previous round
- findings list (id, severity, location, proposed fix)
- decisions taken / deferred this round
- stop-condition check result
- accepted vs reverted changes (regression guard outcome)

Reports are append-only history; never overwrite a prior round's file.

## Loop State

`.claude/memory/convergence-state.md` is the durable, resumable state:

- current round, max rounds, thresholds
- score history table (one row per round)
- last accepted commit
- active stop-condition status
- open findings carried to next round

This is the convergence-loop analogue of `pipeline-state.md` and follows the
same Summary-Sync rule: update it after every round, never leave state only in
chat or commit messages.

## Git Discipline

- The whole loop runs on a `feature/*` (or `fix/*`) branch, never `main`.
- One commit per accepted round: `chore(audit): round <n> — <one-line outcome>`.
- Reverted rounds leave a recorded reason, not a dangling dirty tree.
- Frozen decisions in `memory/frozen-decisions.md` are **out of scope** for the
  loop; if a finding implies changing one, that is a checkpoint-3 user decision.

## Anti-Patterns

- **Reward hacking** — raising a score by weakening a test or gate. Forbidden;
  the regression guard and "tests may not be loosened to pass" rule block it.
- **Score inflation** — high subjective scores without cited evidence.
- **Churn** — rewriting working, frozen code for cosmetic deltas.
- **Re-litigation** — reopening frozen decisions inside the loop instead of at a
  user checkpoint.
- **Silent skips** — treating an unmeasurable gate as a pass.
- **Non-termination** — ignoring plateau / budget stop conditions.
