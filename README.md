# CodeTrace

> One PRD in. Architecture, code, tests, and acceptance evidence out — then a
> self-converging loop hardens it until it clears a measurable quality bar.

**CodeTrace** is an AI-first delivery pipeline: a reusable, version-controlled system
of agents, skills, commands, rules, and memory under `.claude/`. To prove the pipeline
works, it generates its own payload — a lightweight, local-first, zero-dependency
Python function tracer under `src/`.

**The pipeline is the deliverable. The library is the proof.**

## Flow

```
PRD → Intent → Architecture → Build Spec → Task Slices → Coding → Verify → Accept → ⟳ Converge
```

Every stage is three files: a **command** (entry), a **skill** (how), an **agent** (who),
wrapped in non-negotiable rules and resumable memory.

```bash
/seechen --run      # run the full pipeline from docs/PRD.md
/converge --run     # harden a green milestone until it converges
```

## Proven run

The pipeline generated the library end to end, then the convergence loop hardened it
across three rounds:

**77/77 tests · 99% line coverage · 77.3% mutation · ruff clean · mypy 0 errors ·
complexity ≤ B → CONVERGED**

The loop caught what a green suite hid — a type-safety hole, a complexity hotspot, and
a **coverage illusion**: 99% of lines executed, but only **64.5%** of the logic was
actually asserted. Hardening lifted mutation to 77.3%, past the gate, and the loop stopped.

→ [Case Study](docs/Case-Study.md) — the full narrative · [Audit evidence](specs/audit/) — per-round reports

## Documentation

| Document | What it covers |
| --- | --- |
| [PRD](docs/PRD.md) | Product source of truth |
| [Workflow](docs/Workflow.md) | Stage-by-stage definitions |
| [Pipeline Components](docs/Pipeline-Components.md) | **Every agent and skill in detail** — inputs, outputs, boundaries |
| [Case Study](docs/Case-Study.md) | The end-to-end run, round by round |
| [Convergence Loop](.claude/docs/Convergence-Loop.md) | Rubric, gates, stop conditions, driver |
| [Diagrams](docs/diagrams/) | PlantUML flow + sequence diagrams |

## Structure

```
CodeTrace/
├── .claude/          # the pipeline: agents, skills, commands, rules, memory, docs
├── docs/             # PRD, workflow, component reference, case study, diagrams
├── specs/            # generated outputs: intent, architecture, build, acceptance, audit
├── src/ tests/       # the generated library and its test suite
└── CLAUDE.md         # repository entry point
```

## Contributing

Follow the rules in [`.claude/rules/`](.claude/rules/): task-appropriate branches,
Conventional Commits, English for reusable constraint files, and update
`.claude/memory/pipeline-state.md` after each completed stage.

## License

MIT — see [LICENSE](LICENSE).
