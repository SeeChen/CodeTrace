---
name: generate-test-design
description: Generate testing design documents from the PRD and specification layers. Use this to define validation intent before or alongside coding.
---

# Generate Test Design

This skill creates or refreshes the testing specification layer for the current project.

Use this skill when the user wants to:

- map specs to test intent
- define performance, edge-case, and reliability validation
- prepare the repository for implementation and automated test execution

Do not use this skill for:

- writing executable test code
- redefining the global or domain architecture

## Required Inputs

Read these files first:

1. `docs/PRD.md`
2. `specs/ref/*`
3. `specs/global/*`
4. `specs/domains/*`
5. `.qoder/rules/summary-sync.md`

Also read [references/test-design-contract.md](references/test-design-contract.md).

## Output Contract

Write or update testing documents under `specs/testing/`.

Possible outputs include:

1. performance-test plans
2. concurrency or idempotency test plans
3. requirement-to-test coverage plans
4. failure-path and boundary-case plans

Choose only the files justified by the project.

## Workflow

### Step 1: Rebuild validation scope

Identify:

- critical requirements
- architecture risks
- edge cases
- acceptance-sensitive constraints

### Step 2: Define testing documents

Map the identified validation needs into clear planning documents.

### Step 3: State coverage intent

Explain what each testing document is responsible for validating and why it matters.

## Handoff Rules

Before finishing, verify:

1. every major risk has a home in the testing layer
2. the output can guide both coding and automated testing
3. unnecessary test documents were not added without reason
4. progress tracking will be updated
