# PRD-Pipeline Rules Index

This document indexes the active workflow rules for the CodeTrace-AI repository.

## Rules Overview

- [Workflow](workflow.md) - Core Git workflow steps
- [Branch Protection](branch.md) - Branch protection and management
- [Branch Selection](branch-selection.md) - Choose a suitable task branch before starting work
- [Commit Guidelines](commit.md) - Commit message format and standards
- [AI Development](ai.md) - Special considerations for AI assistance
- [Agent and Skill Design](agent-skill-design.md) - Keep agents and skills lightweight, navigational, and docs-backed
- [Document Scope](doc-scope.md) - Determine the artifact set from the actual project boundary
- [Summary Sync](summary-sync.md) - Update durable workflow state after each completed stage
- [System Constraint Language](system-constraint-language.md) - Use English for reusable AI system constraint files
- [Exceptions](exceptions.md) - Exceptions to standard rules

## Quick Reference

- Always work on a task-appropriate branch, never directly on `main`
- Use conventional commit messages (`<type>(<scope>): <description>`)
- Require PR review before merging to `main`
- Keep agents and skills compact and docs-backed
- Update `memory/pipeline-state.md` after each completed stage

For detailed information, refer to the individual rule files.
