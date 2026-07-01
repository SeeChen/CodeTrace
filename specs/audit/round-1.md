# Convergence Audit — Round 1

- Round: `1`
- Timestamp: `2026-07-02T00:33:50`
- Base commit: `d30d434`
- Mode: `attended` (single-round demo; driver not handed off)
- Autonomy: escalation checkpoints active

## Objective Gates

| Gate | Tool | Measured value | Result |
| --- | --- | --- | --- |
| Tests green | pytest 8.x | 43/43 pass, 0 error | ✅ pass |
| Coverage (line) | coverage 7.x | 98% total | ✅ pass (95% target) |
| Coverage (core floor) | coverage 7.x | `session.py` 89% < 90% | ⚠️ sub-threshold → F3 |
| Self-regression (mutation) | mutmut | — | ⛔ unmeasured → F4 |
| Lint / style | ruff 0.15.20 | All checks passed | ✅ pass |
| Types | mypy 2.1.0 | 1 error → **0 after fix** | ✅ pass (fixed F1) |
| Complexity | radon cc 6.0.1 | `_execute` grade **D (21)**; avg A (1.96) | ❌ fail → F2 |

Mutation is `unmeasured`, not skipped: `mutmut` does not run on native Windows
(requires WSL). Recorded honestly rather than reported as a pass. Remediation in
F4.

## Subjective Axes (evidence-cited)

| Axis | Score | Evidence |
| --- | --- | --- |
| Extensibility | `9/10` | Extension points are real, not nominal: `contracts.py` defines `PersistenceAdapter`/`MetricsCollector` Protocols; `config.py` injects `compare`, `record`, `persistence`, `metrics_collectors`; `tracer._execute` resolves `compare_override or cfg.compare or default_compare` (and same for record). A new adapter/compare/record strategy is addable without editing core. |
| Maintainability | `8/10` | `radon mi` is grade A for every module; average CC A (1.96); naming and docstrings are clear; failure isolation is explicit in `_isolated`. Docked 2 for the one hotspot: `_execute` CC D (21) / MI 64.21 — the lowest in the tree (F2). |

## Composite Score

- Objective sub-score: 4 / 5 measurable gates pass (complexity fails; mutation excluded as unmeasured) = `0.80`
- Subjective sub-score: (9 + 8) / 2 = 8.5 → `0.85`
- Composite = 0.70 × 0.80 + 0.30 × 0.85 = **`0.82` (82 / 100)**
- Δ vs previous round: `n/a` (first round — this is the baseline)

## Findings

| ID | Severity | Location | Proposed fix | Status |
| --- | --- | --- | --- | --- |
| F1 | medium | `tracer.py:125` | Coerce `qualname` to `str` so `resolve_trace_name(str)` is satisfied; no behavior change | ✅ fixed this round |
| F2 | medium | `tracer.py:110` `_execute` | Extract persistence / compare / record phases into small helpers to bring CC ≤ C; keep guarantees identical, verify tests unchanged | ⏭️ deferred to round 2 |
| F3 | low | `session.py` (atexit path) | Add a test exercising the atexit flush, or justify the exclusion in the coverage config | ⏭️ deferred to round 2 |
| F4 | low (process) | tooling | Run mutation under WSL, or adopt `cosmic-ray` which runs on Windows, to measure self-regression | ⏭️ deferred (needs env decision) |

## Decisions

- **Taken:** applied F1 (minimal, zero-behavior type fix). It flips the Types
  gate FAIL → PASS; tests stayed 43/43; no other gate regressed.
- **Deferred:** F2 refactors the central orchestrator `_execute` — larger and
  regression-prone; not something to guess at in one unattended pass. Carried.
- **Deferred:** F3 (coverage top-up) and F4 (mutation tooling) carried; F4 needs
  an environment decision (WSL vs cosmic-ray) → escalation-class.

## Regression Guard

- Round outcome: **accepted** — Types improved, no objective gate worsened.
- No changes reverted this round.

## Stop-Condition Check

- Converged? **No** — complexity gate fails; mutation unmeasured; open findings remain.
- Plateau? No (round 1 of budget). Budget? No (1 / 6). Hard blocker? No.
- **Next Round Scheduled: `yes`** (findings remain) — but this run is a scoped
  single-round demo, so the loop halts here and hands control back to the user
  instead of firing round 2.
