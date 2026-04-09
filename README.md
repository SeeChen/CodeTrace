# CodeTrace-AI

An AI-first development repository for building software through PRD-driven documentation, reusable system constraints, and staged specification generation. The project focuses on turning a single PRD into an executable document system that can later drive coding, testing, and acceptance.

## Overview

CodeTrace-AI explores a modular workflow in which AI agents collaborate through explicit rules, skills, commands, memory, and staged specifications. The repository emphasizes:

- **PRD-Driven Planning**: Start from one PRD and derive the document system from actual project boundaries
- **Specification-Driven Development**: Build global, domain, testing, and acceptance documents before implementation
- **Reusable AI Constraints**: Keep system prompts, rules, commands, skills, and memory under version control
- **Resumable Workflow**: Track progress so work can continue from the latest completed document task

## Documentation

- [Product Requirements Document (PRD)](docs/PRD.md)
- [AI Development Workflow](docs/Workflow.md)
- [PRD to Coding Orchestration](docs/PRD-to-Coding-Orchestration.md)
- [Document System Todo Plan](docs/todo-plan.md)

## Getting Started

This repository is designed for AI-assisted development where the document system comes first. The current setup focuses on planning and generating the specification tree from the PRD before moving into code.

### Prerequisites

- Access to AI development tools that can read repository files and follow structured instructions
- A project PRD as the primary source of truth
- Basic familiarity with staged specification workflows

### Usage

1. Read the [PRD](docs/PRD.md) and [Workflow](docs/Workflow.md).
2. Use the planning and orchestration documents in `docs/` to understand the intended document pipeline.
3. Use the reusable assets under `.qoder/`:
   - `agents/` for system-prompt roles
   - `skills/` for task-specific generation workflows
   - `commands/` for reusable task entry points
   - `rules/` for repository constraints
   - `memory/` for stable project context
4. Generate `specs/ref/`, `specs/global/`, `specs/domains/`, `specs/testing/`, and `specs/acceptance/` in stages.

## Project Structure

```
CodeTrace-AI/
├── .github/
│   └── rules/                  # Repository rules mirrored for GitHub-side workflow control
├── .qoder/
│   ├── agents/                 # Reusable agent system prompts
│   ├── commands/               # Reusable command entry points
│   ├── memory/                 # Stable workflow memory
│   ├── rules/                  # Repository rules for AI workflows
│   └── skills/                 # Task-specific generation skills
├── docs/
│   ├── PRD.md                          # Product Requirements Document
│   ├── Workflow.md                     # High-level workflow reference
│   ├── PRD-to-Coding-Orchestration.md  # Document orchestration design
│   └── todo-plan.md                    # Progress tracker for document-system setup
├── LICENSE
└── README.md
```

## Current Scope

The repository currently includes the document-system foundation for:

- PRD boundary analysis
- document-tree planning
- Phase 0 reference generation
- global specification generation
- domain planning and one-domain-at-a-time expansion
- testing-plan generation
- acceptance-criteria generation

Implementation code generation is intentionally downstream from these document phases.

## Contributing

Contributions should preserve the AI-first workflow. Please:

1. Follow the rules in `.github/rules/` and `.qoder/rules/`.
2. Keep reusable system-constraint files in English unless there is a documented exception.
3. Use a task-appropriate branch instead of reusing an unrelated branch.
4. Update progress-tracking documents when document-generation work is completed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by modular AI-assisted development practices
- Built to demonstrate how PRD-driven document systems can structure later coding work
