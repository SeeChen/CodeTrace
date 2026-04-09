---
name: generate-domain-spec
description: Generate the detailed specification set for a single domain from the PRD, global layer, and domain plan. Use this after domain planning and before coding.
---

# Generate Domain Spec

This skill creates or refreshes the specification set for one domain.

Use this skill when the user wants to:

- expand a planned domain into detailed documents
- define layer responsibilities and domain behavior
- prepare one domain for implementation and testing

Do not use this skill for:

- planning the full domain map
- writing code
- rewriting the global architecture layer

## Required Inputs

Read these files first:

1. `docs/PRD.md`
2. `specs/ref/*`
3. `specs/global/*`
4. `specs/domains/summary.md` or the current domain plan
5. `.codex/modules/PRD-Pipeline/rules/doc-scope.md`
6. `.codex/modules/PRD-Pipeline/rules/summary-sync.md`

Also read [references/domain-spec-contract.md](references/domain-spec-contract.md).

## Output Contract

Write or update the specification set for one domain under `specs/domains/<domain-name>/`.

Possible files:

1. `SA.md`
2. `layer-core.md`
3. `layer-dao.md`
4. `layer-biz.md`
5. `layer-facade.md`

Use only the files justified by the domain plan and current project shape.

## Workflow

### Step 1: Rebuild the domain boundary

Identify:

- domain purpose
- responsibilities
- dependencies
- key lifecycle steps

### Step 2: Choose the layer set

Decide which layer documents are required for this domain and why.

### Step 3: Write the domain spec

Document:

- internal structure
- responsibilities per layer
- data or control flow
- failure paths
- extension points

## Writing Rules

- Stay specific to one domain.
- Keep consistency with global contracts.
- Prefer explicit responsibilities over vague descriptions.
- Leave open questions when upstream inputs remain unresolved.

## Handoff Rules

Before finishing, verify:

1. the domain's document set matches the domain plan
2. the domain can move to test planning and coding
3. cross-domain assumptions are documented clearly
4. progress tracking will be updated


