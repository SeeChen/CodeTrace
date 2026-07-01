# Convergence Audit — Round 3

- Round: `3`
- Timestamp: `2026-07-02T01:05:00`
- Base commit: `be668a8`
- Mode: `attended` (single-round `--resume`)
- Target: finding **F6** — kill surviving mutants until mutation ≥ 70%

## Objective

Round 2 measured mutation **64.5%** (89 survivors) against 99% line coverage —
proof that lines ran without being asserted. This round adds assertion-hardening
tests to close that gap. Only +14 kills are needed to cross the 70% gate; the
change targets every high-density module for margin.

## Change

New test module `tests/unit/test_mutation_guards.py` (+31 tests, suite 46 → 77).
It pins exact values/structures so any logic mutation fails a test:

| Module | Survivors (R2) | What the new tests pin |
| --- | --- | --- |
| tracer.py | 32 | `_isolated` exact failure dict + warning; `_run_user_call` success/exception; `_maybe_compare` on/off gating |
| recorder.py | 18 | `default_record_builder` verbatim + missing-key defaults; `build_summary` exact structure and `total == len(records)` |
| config.py | 10 | every default value exact; `ALLOWED_KEYS` membership; `merge` rejects unknown / changes only target |
| timing.py | 9 | fresh fields `None`; `start`/`stop` return self; ISO-microsecond format; `duration ≥ 0` |
| session.py | 7 | (covered via round-2 flush tests + `paths` collision increment) |
| logging_setup.py | 4 | logger name `codetrace`, level `WARNING`, handler present, idempotent |
| persistence.py | 3 | `save_output` `is_none` true/false + value |
| paths.py | 3 | run-id format (no colons); `sanitize`; collision `__2/__3/__4` increment |
| contracts.py | 3 | `runtime_checkable` isinstance for both Protocols (docstring mutants likely equivalent) |

## Objective Gates (measured on Windows)

| Gate | Value | Result |
| --- | --- | --- |
| Tests green | 77/77 pass | ✅ pass |
| Coverage (line) | 99% (unchanged — these assert existing paths) | ✅ pass |
| Lint / style | ruff clean | ✅ pass |
| Types | mypy 0 errors | ✅ pass |
| Complexity | unchanged (no source change) | ✅ pass |
| Self-regression (mutation) | **pending WSL re-run** | ⏳ to confirm |

No production source changed this round — only tests were added — so no
behavior can regress. The complexity/coverage/type gates are unaffected.

## Expectation

The added assertions directly target the survivor clusters; the expected mutation
score is well above the 70% gate. Any residual survivors (e.g. equivalent
docstring mutants in `contracts.py`, or an edge in `session.py`) will be listed
from the next `mutmut results` and addressed or justified as equivalent.

## Stop-Condition Check

- Converged? **Pending** — contingent on the re-measured mutation score.
  If mutation ≥ 70%: all six objective gates pass and both subjective axes clear
  the threshold → mark `converged`, recompute composite (now 6/6 gates).
  If < 70%: round 4 targets the named residual survivors.
- Budget: round 3 / 6. Plateau: no.
- **Next Round Scheduled: `pending-remeasure`** — awaiting the WSL mutation re-run.
