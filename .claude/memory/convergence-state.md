# Convergence Loop State

Durable, resumable state for the `/converge` hardening loop. Update after every
round. See `.claude/docs/Convergence-Loop.md` for the rubric and stop conditions.

## Status

- Loop Status: `not-started`   <!-- not-started | running | paused | converged | stopped -->
- Current Round: `0`
- Max Rounds: `6`
- Subjective Threshold: `8`    <!-- per-axis pass mark, 0–10 -->
- Plateau Window (N): `2`
- Working Branch: `none`
- Last Accepted Commit: `none`
- Stop Reason: `none`          <!-- converged | plateau | budget | user-halt | hard-blocker -->

## Score History

| Round | Tests | Coverage | Mutation | Lint | Types | Complexity | Extensibility | Maintainability | Composite | Δ | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| _none yet_ | | | | | | | | | | | |

<!-- Outcome: accepted | reverted (regression) -->

## Open Findings (carried to next round)

| ID | Severity | Location | Proposed Fix | Status |
| --- | --- | --- | --- | --- |
| _none yet_ | | | | |

## Round Reports

<!-- One line per round, newest last: round-<n> -> specs/audit/round-<n>.md -->

- _none yet_

## Checkpoints Log

<!-- Record each user decision: round, question, choice. -->

- _none yet_

## Notes

- Never mark `converged` unless all objective gates pass (or are justified `n/a`)
  AND every subjective axis meets the threshold.
- A round may only be `accepted` if it worsens no objective gate.
- Frozen decisions are out of scope; changing one is a user checkpoint, not a loop action.
