# Case Study: From One PRD to a Self-Converged Codebase

**How an AI-first delivery pipeline generated a Python library, then a self-driving
convergence loop hardened it — surfacing a defect that 99% test coverage had hidden.**

---

## TL;DR

- One PRD was run through a reusable, AI-first pipeline (`PRD → intent → architecture
  → build spec → task slices → coding → verify → accept`) to generate **CodeTrace**,
  a zero-dependency Python function tracer: **43 tests, 98% coverage, accepted**.
- A **convergence loop** then hardened the green milestone across three rounds,
  driven by machine-checkable gates rather than self-assessment.
- The headline finding: **99% line coverage but only 64.5% mutation score** — the
  lines ran, but a third of the logic wasn't actually asserted. Hardening lifted
  mutation to **77.3%**, past the gate, and the loop stopped.
- Every round left an evidence file and a commit. The loop escalated to a human
  when a gate couldn't be measured, and it stopped at the defined bar instead of
  polishing forever.

---

## 1. What this repository actually is

The visible product is CodeTrace, a small tracing library. But the real deliverable
is the **pipeline** under `.claude/` — a version-controlled system of agents, skills,
commands, rules, and memory that turns a product requirement into architecture,
build contracts, code, tests, and acceptance evidence. CodeTrace is just the payload
used to prove the pipeline end to end.

That framing matters for this case study: the interesting engineering is not the
tracer, it's the **process that produced and then hardened it**.

## 2. Part one — one PRD, one working MVP

Running `/seechen --run` against `docs/PRD.md` executed all seven stages, each with a
dedicated command, skill, and agent, and each writing a reviewable artifact:

| Stage | Output |
| --- | --- |
| Intent | `specs/intent/brief.md` |
| Architecture | `specs/architecture/SA.md` (frozen before build specs) |
| Build spec | `specs/build/*` (interfaces, file plan, artifact schema, failure policy, test matrix) |
| Task slices | `specs/build/tasks.md` (13 ordered slices) |
| Coding | `src/codetrace/`, `tests/` |
| Verify | verification evidence |
| Accept | `specs/acceptance/*` (10 blocking gates, all pass) |

Result: a four-layer library (Core / Adapter / Utility / Contract) with strict
failure isolation, **43 passing tests and 98% line coverage**, formally accepted.

By every normal measure, this was "done."

## 3. Part two — the problem with "all green"

A green suite proves the code does what the tests check. It does not prove the code
is hard to break, easy to extend, or free of latent defects. High coverage is
especially seductive: it says a line *executed*, not that its behavior was
*asserted*.

So the pipeline was extended with a **convergence loop**: after acceptance, keep
iterating — `audit → score → stop-check → re-plan → implement → verify` — until a
composite quality bar is met, then stop.

The design deliberately matches the loop-engineering primitives that the industry
has converged on for autonomous coding agents:

| Primitive | In this system |
| --- | --- |
| Loop mechanism / driver | native `/loop` or `ScheduleWakeup` firing `/converge --resume` |
| Decision-maker | `audit-agent` + controller reading `convergence-state.md` |
| Feedback gate | machine-checkable gates + a regression guard |
| State persistence | `convergence-state.md` + one commit per round + append-only reports |
| Goal / convergence | composite score + explicit stop conditions |
| Anchor context | `CLAUDE.md`, `frozen-decisions.md`, `SA.md`, `brief.md` |
| Escalation path | human-in-the-loop checkpoints |

Two decisions kept the loop honest:

1. **The score is mostly machine-checkable** — 70% objective gates (tests,
   coverage, mutation, lint, types, complexity), 30% evidence-cited review. The
   loop *cannot* converge on its own opinion.
2. **A regression guard** reverts any round that worsens a gate, and stop
   conditions (converged / plateau / budget) guarantee termination.

## 4. Part three — the run, round by round

| Round | Composite | Mutation | Complexity | Tests | What happened |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.82 | unmeasured | `_execute` **D(21)** | 43 | Found and fixed a **type-safety hole** (`mypy` error) with a zero-behavior change; the type gate went red → green. Carried the complexity and mutation findings. |
| 2 | 0.97 | 64.5% (measured after) | `_execute` **A(5)** | 46 | **Refactored** the D-grade orchestrator into focused helpers (behavior-preserving); **added tests** for previously-uncovered session paths (89% → 100%). |
| 3 | 0.97 | **77.3%** ✅ | A | 77 | Added **31 assertion-hardening tests** to kill surviving mutants; mutation cleared the 70% gate → **converged**. |

Each round ran on its own commit, so every change is diffable and revertible.

### The escalation that proves the loop isn't a rubber stamp

In round 2 the loop reached composite 0.97 with five of six objective gates green —
but the **mutation gate could not be measured**: the mutation-testing tool doesn't
run on native Windows. A naive loop would either skip the gate or declare victory.
This one **stopped and asked a human**, then the score was measured under WSL.

That measurement is the whole story.

## 5. Part four — the coverage illusion

The mutation run: **251 mutants, 161 killed + 1 timeout, 89 survived → 64.5%.**

Against 99% line coverage, that's the punchline: **almost every line executed, but
a third of the logic could be changed with no test failing.** Coverage measured
*reach*; mutation measured *assertion strength*. They disagreed by 35 points.

The survivors clustered where tests checked behavior but not exact values — record
structures, config defaults, timing fields, failure dictionaries. Round 3 added
tests that pin those exact values, killing 32 more mutants and lifting mutation to
**77.3%** (57 survivors, some of them equivalent mutants in Protocol docstrings that
are unkillable by design).

## 6. Why the result is trustworthy

- **Machine gates, not vibes.** Convergence required real tool runs: `pytest`,
  `coverage`, `mutmut`, `ruff`, `mypy`, `radon`. The subjective axes were capped and
  had to cite specific files and lines.
- **No reward hacking.** Loosening a test to raise a score is forbidden; the
  regression guard rejects any round that worsens a gate.
- **Honest about the unmeasurable.** The mutation gate was recorded as `unmeasured`,
  not passed, until it could actually be run.
- **It stops at "good enough," not "perfect."** 77.3% cleared the 70% bar and the
  loop terminated, logging the residual survivors as an optional backlog rather than
  churning indefinitely.

## 7. Final state

**All six objective gates pass, both subjective axes clear the threshold:**

tests 77/77 · line coverage 99% · **mutation 77.3% (≥70%)** · ruff clean ·
mypy 0 errors · complexity no block worse than B · extensibility 9/10 ·
maintainability 9/10.

Composite **0.97**, status **CONVERGED**.

## 8. Takeaways

1. **"All tests pass" is a floor, not a finish line.** A convergence loop makes the
   step past it explicit and evidence-backed.
2. **Coverage can lie; mutation testing catches it.** If you measure only one thing
   about test strength, measure whether your tests actually *fail* when the code is
   wrong.
3. **Loop quality > model quality.** The value here is the loop's design — a goal
   function, machine gates, a regression guard, and an escalation path — not any
   single clever generation.
4. **Delegate repetition; own the goal.** The loop rides on a native scheduler and
   contributes only the part that's actually domain-specific: what one round does
   and when to stop.

## 9. Reproduce it

```bash
# generate the MVP from the PRD
/seechen --run

# harden the green milestone until it converges
/converge --run          # unattended; escalates only when it must
# or one round at a time:
/converge --resume
```

Mutation testing runs under WSL (`mutmut`), since it does not support native
Windows — a limitation the loop surfaces and records rather than hides.

## 10. Evidence

- Per-round reports: [`specs/audit/round-1.md`](../specs/audit/round-1.md),
  [`round-2.md`](../specs/audit/round-2.md), [`round-3.md`](../specs/audit/round-3.md)
- Capstone: [`specs/audit/convergence-summary.md`](../specs/audit/convergence-summary.md)
- Loop contract: [`.claude/docs/Convergence-Loop.md`](../.claude/docs/Convergence-Loop.md)
- Durable state: [`.claude/memory/convergence-state.md`](../.claude/memory/convergence-state.md)
- Acceptance: [`specs/acceptance/report.md`](../specs/acceptance/report.md)
