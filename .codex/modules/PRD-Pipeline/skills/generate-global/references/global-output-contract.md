# Global Output Contract

Use this reference when drafting `specs/global/`.

## Expected Files

1. `app-business.md`
2. `SA.md`
3. `project-structure.md`
4. `modules.md`
5. `constraint.md`
6. `API.md`

## File Responsibilities

- `app-business.md`: product flow and business scenario framing
- `SA.md`: high-level architecture and component topology
- `project-structure.md`: repository and package organization guidance
- `modules.md`: module ownership, dependencies, and boundaries
- `constraint.md`: hard technical and policy constraints
- `API.md`: global contracts and stable public-facing interfaces

## Required Cross-Checks

Each file should help answer:

- why it exists
- what decisions it freezes
- what decisions remain deferred to domain specs

## Minimum Depth Expectations

- `app-business.md` should describe the primary lifecycle and major user flows, not only file purpose statements.
- `SA.md` should define topology, component responsibilities, and major failure boundaries.
- `project-structure.md` should connect repository layout to implementation responsibilities.
- `modules.md` should make ownership and dependencies explicit enough for domain planning.
- `constraint.md` should separate non-negotiable rules from recommendations.
- `API.md` should capture stable contract expectations, extension seams, and deferred contract details.


