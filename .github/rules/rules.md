# Git Workflow Rules for CodeTrace-AI

This document outlines the standardized Git workflow for the CodeTrace-AI project, ensuring consistent development practices in our AI-driven, prompt and SDD mode environment.

## Workflow Overview

1. **Create a Suitable Branch**
   - Always create a new branch for any changes or features
   - Branch naming convention: `feature/<description>` or `fix/<description>`
   - Base branch: `main` (or `master` if applicable)

2. **Commit Changes**
   - Make atomic commits with clear, descriptive messages
   - Each commit should represent a single logical change
   - Commit message format: `<type>(<scope>): <description>`
     - Types: feat, fix, docs, style, refactor, test, chore
     - Example: `feat(workflow): add AI development guidelines`

3. **Push to Remote**
   - Push the branch to the remote repository
   - Ensure all commits are pushed before creating a PR

4. **Create Pull Request (PR)**
   - Create a PR from the feature branch to the main branch
   - Provide a clear title and detailed description
   - Reference any related issues or specifications
   - Request review from appropriate team members

5. **Review Process**
   - Conduct thorough code review focusing on:
     - Adherence to project specifications
     - Code quality and consistency
     - Documentation completeness
     - Test coverage
   - Address all review comments and make necessary changes

6. **Merge to Main**
   - Once approved, merge the PR using "Squash and merge" to maintain clean history
   - Delete the feature branch after successful merge
   - Ensure CI/CD pipelines pass before merging

## Branch Protection Rules

- `main` branch requires:
  - At least 1 approval for PRs
  - All CI checks to pass
  - No unresolved conversations

## Commit Message Guidelines

- Use imperative mood: "Add feature" not "Added feature"
- Keep first line under 50 characters
- Provide detailed description in commit body if needed

## AI-Driven Development Notes

- All changes should align with the [AI Development Workflow](docs/Workflow.md)
- Use structured prompts for generating commit messages and PR descriptions
- Ensure specifications are updated alongside code changes

## Exceptions

- Hotfixes may be committed directly to main with prior approval
- Documentation-only changes may follow a simplified process