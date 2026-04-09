---
name: plan-domains
description: Plan the domain breakdown of the project from global specifications and identify what domain-level documents should exist before detailed domain spec generation.
---

# Plan Domains

This skill creates a domain expansion plan from the global specification layer.

Use this skill when the user wants to:

- break global architecture into implementation-facing domains
- decide which domains need separate document sets
- determine the first domains to expand in detail

Do not use this skill for:

- writing detailed domain logic
- generating code
- replacing the global architecture layer

## Required Inputs

Read these files first:

1. `specs/global/*`
2. `specs/ref/*`
3. `docs/PRD.md`
4. `.qoder/rules/doc-scope.md`
5. `.qoder/rules/summary-sync.md`

Also read [references/domain-plan-contract.md](references/domain-plan-contract.md).

## Output Contract

Create or update a domain planning document that includes:

1. domain list
2. purpose and ownership of each domain
3. dependency relationships
4. recommended document set per domain
5. recommended order of domain expansion

Default output:

- `specs/domains/summary.md`

## Workflow

### Step 1: Read the global layer

Identify modules, responsibilities, extension points, and cross-domain dependencies.

### Step 2: Define the domain map

Choose domain boundaries that reduce ambiguity while staying proportional to project complexity.

### Step 3: Assign document needs

For each domain, specify whether it needs:

- `SA.md`
- `layer-core.md`
- `layer-dao.md`
- `layer-biz.md`
- `layer-facade.md`
- another project-specific document

### Step 4: Order the work

Recommend which domains should be expanded first and why.

## Handoff Rules

Before finishing, verify:

1. the domain map follows from the global layer
2. domain count is justified
3. each domain has a clear next step
4. progress tracking will be updated
