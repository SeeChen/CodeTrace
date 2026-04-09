# Rule 9: Document Scope from Project Boundary

This rule defines how AI agents should determine which documents belong in the specification tree.

## Purpose

The example workflow and directory structure are reference patterns. AI agents must decide the actual document set from the current project's PRD and boundary conditions.

## Guidelines

- Read the PRD before choosing the document set
- Identify project scale, system shape, complexity drivers, and delivery goals first
- Use the workflow example as a baseline pattern, not as a fixed checklist
- Create only the documents that the current project can justify
- Expand the document set when the project clearly requires more structure
- Merge or omit documents when a smaller project does not justify full separation

## Required Questions

Before planning documents, answer:

1. What kind of system is this?
2. How complex is the implementation surface?
3. Which constraints or risks justify additional documents?
4. Which example documents are unnecessary for the current phase?
5. Which missing documents are needed because of the actual project shape?

## Expected Output Behavior

- Mark documents as required, optional, deferred, or unnecessary
- Explain why each major document exists
- Explain why each omitted or merged document is acceptable
- Keep downstream document generation traceable to the PRD and upstream specs

## Anti-Patterns

- Do not copy the example document tree without analysis
- Do not generate documents only because they exist in the example workflow
- Do not omit important documents just to keep the tree small
- Do not add domain documents before global boundaries are clear
