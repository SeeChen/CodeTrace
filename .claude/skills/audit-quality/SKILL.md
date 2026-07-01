---
name: audit-quality
description: Audit a passing milestone for latent defects and quality gaps, measure objective gates and score subjective axes on cited evidence, and write the per-round audit report.
---

# Audit Quality

Use this skill to run one audit round inside the convergence loop. It produces
the measured, scored, evidence-backed report the loop uses to decide whether to
keep iterating.

Full rubric, gate definitions, weights, and stop conditions live in
`.claude/docs/Convergence-Loop.md`. Read it first.

## Use When

- a milestone already passes its baseline tests
- the convergence loop is running and needs a scored round
- evidence is needed to decide continue vs stop

## Do Not Use When

- the baseline pipeline has not reached a green `accept` yet
- the task is normal stage work (use the matching stage skill instead)

## Read First

1. `.claude/docs/Convergence-Loop.md`
2. `specs/build/*` and `specs/architecture/SA.md`
3. `src/` and `tests/`
4. `.claude/memory/convergence-state.md`
5. `.claude/memory/frozen-decisions.md`

## Write

- `specs/audit/round-<n>.md`
- updated `.claude/memory/convergence-state.md`

## Execution Steps

1. **Measure objective gates** — run the available tools (tests, coverage,
   mutation, lint, types, complexity). Record each value and pass/fail. If a
   tool is unavailable, try to install it; otherwise mark the gate `unmeasured`
   with the reason.
2. **Score subjective axes** — rate extensibility and maintainability, quoting
   specific files/lines as evidence. No evidence means `unscored`, not high.
3. **Compute composite** — apply the doc's weights; record the delta vs the
   previous round.
4. **List findings** — id, severity, location, proposed minimal fix. Flag any
   that touch frozen decisions or public API as escalation items.
5. **Check stop conditions** — converged / plateau / budget / hard blocker.
6. **Write the round report and update loop state.**

## Required Guarantees

- every gate result is a real tool run or a recorded `unmeasured` reason
- every subjective score cites evidence
- findings are concrete, located, and minimally scoped
- the stop-condition result is explicit
- the report is a new file, never an overwrite of a prior round

## Guardrails

- Never loosen a test or gate to raise a score.
- Never report an unmeasured gate as a pass.
- Never propose changes that reopen frozen decisions; route those to a user
  checkpoint.
- Keep proposed fixes minimal; do not churn working frozen code.
- Write progress to `convergence-state.md`, not only to chat.
