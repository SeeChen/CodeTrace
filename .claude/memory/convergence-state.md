# Convergence Loop State

Durable, resumable state for the `/converge` hardening loop. Update after every
round. See `.claude/docs/Convergence-Loop.md` for the rubric and stop conditions.

## Status

- Loop Status: `paused`        <!-- not-started | running | paused | converged | stopped -->
- Autonomy Mode: `attended`    <!-- auto (unattended + escalation) | attended -->
- Current Round: `1`
- Max Rounds: `6`
- Subjective Threshold: `8`    <!-- per-axis pass mark, 0–10 -->
- Plateau Window (N): `2`
- Working Branch: `feature/convergence-loop`
- Last Accepted Commit: `(round-1 fix — see git log)`
- Next Round Scheduled: `yes`  <!-- driver: yes (round n+1 queued) | no (stopped / not running) -->
- Stop Reason: `none`          <!-- converged | plateau | budget | user-halt | hard-blocker -->

Note: single-round demo. Round 1 signalled `yes` (not converged) but the loop was
paused by user scope rather than firing round 2. Resume with `/converge --resume`.

## Score History

| Round | Tests | Coverage | Mutation | Lint | Types | Complexity | Extensibility | Maintainability | Composite | Δ | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 43/43 | 98% | unmeasured | pass | pass (fixed) | D(21) fail | 9 | 8 | 0.82 | n/a | accepted |

<!-- Outcome: accepted | reverted (regression) -->

## Open Findings (carried to next round)

| ID | Severity | Location | Proposed Fix | Status |
| --- | --- | --- | --- | --- |
| F2 | medium | `tracer.py:110` `_execute` | Extract persistence/compare/record phases into helpers to bring CC ≤ C | open (round 2) |
| F3 | low | `session.py` atexit path | Add a test for the atexit flush, or justify the coverage exclusion | open (round 2) |
| F4 | low (process) | tooling | Measure mutation via WSL `mutmut` or `cosmic-ray` on Windows | open (needs env decision) |

## Round Reports

<!-- One line per round, newest last: round-<n> -> specs/audit/round-<n>.md -->

- round-1 -> specs/audit/round-1.md (composite 0.82, accepted, F1 fixed)

## Checkpoints Log

<!-- Record each user decision: round, question, choice. -->

- Before loop: user requested a single-round demo (`/converge --run`, scoped to one round).

## Notes

- Never mark `converged` unless all objective gates pass (or are justified `n/a`)
  AND every subjective axis meets the threshold.
- A round may only be `accepted` if it worsens no objective gate.
- Frozen decisions are out of scope; changing one is a user checkpoint, not a loop action.
