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

## Addendum — Mutation Re-measured (WSL, cache cleared)

```
251/251  🎉 193  ⏰ 1  🤔 0  🙁 57  🔇 0
```

- Mutation score = (193 killed + 1 timeout) / 251 = **77.3%** → **above the 70% gate → PASS**.
- Journey: round 2 **64.5%** (89 survivors) → round 3 **77.3%** (57 survivors);
  the +31 hardening tests killed **32** more mutants (killed 162 → 194).
- The headline is now closed: 99% coverage *and* 77.3% mutation — lines are both
  executed and asserted.

### Residual survivors (57) — logged, not blocking

The gate is met, so the loop converges rather than polishing to zero. Remaining
survivors are an optional round-4 backlog:

- `contracts.py` (2: 38-39) — Protocol `save_summary` stub/docstring: **equivalent
  mutants** (no behavior), not killable by design.
- `tracer.py` (27), `session.py` (7), `recorder.py` (8), `timing.py` (6), others —
  killable with more end-to-end assertions on exact persistence call arguments;
  deferred as diminishing-returns beyond the gate.

## Composite Score (all gates measured)

- Objective: **6 / 6** gates pass (mutation now included) = `1.00`
- Subjective: (9 + 9) / 2 = 9.0 → `0.90`
- Composite = 0.70 × 1.00 + 0.30 × 0.90 = **`0.97` (97 / 100)** — now fully measured.

## Stop-Condition Check

- Converged? **YES** — all six objective gates pass (mutation 77.3% ≥ 70%) and
  both subjective axes clear the threshold.
- **Next Round Scheduled: `no`** — stop condition `converged` fired. Loop complete.
