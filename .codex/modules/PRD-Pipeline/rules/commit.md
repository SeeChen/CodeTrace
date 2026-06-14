# Rule 3: Commit Message Guidelines

This rule specifies the format and standards for commit messages in CodeTrace-AI.

## Message Format

- Use Conventional Commits: `<type>(<scope>): <description>`
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Write the description in imperative mood: "add feature", not "added feature"
- Keep the subject line concise; put detail in the commit body when needed
- Make each commit an atomic, single logical change

## AI Attribution

- When a commit is produced with AI assistance, note it in the commit body or as a trailer (for example a `Co-Authored-By` line) so authorship stays transparent
- Keep attribution consistent across AI-assisted commits

## Examples

- `feat(pipeline): add intent brief generation contract`
- `fix(persistence): isolate serialization failures from user code`

  ```
  fix(persistence): isolate serialization failures from user code

  Wrap persistence writes in try-except so artifact failures do not
  interrupt successful user-code execution.

  Co-Authored-By: Assistant <assistant@example.com>
  ```
