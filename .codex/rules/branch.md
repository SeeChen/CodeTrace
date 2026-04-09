# Rule 2: Branch Protection Rules

This rule defines the protection rules for branches in the CodeTrace-AI repository.

## Main Branch Protection

- `main` branch requires:
  - At least 1 approval for PRs
  - All CI checks to pass
  - No unresolved conversations

## Branch Management

- Feature branches should be created from `main`
- No direct commits to `main` except for hotfixes
- Branch names must follow the convention: `feature/*` or `fix/*`
