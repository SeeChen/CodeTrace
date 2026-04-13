# Comparison and Reporting Business Layer

## Scope

This layer applies comparison and record-building policies using runtime outputs.

## Responsibilities

- prepare baseline and candidate inputs for compare callables
- choose default compare behavior when no custom hook is provided
- merge runtime, persistence, and comparison data into one trace record
- queue or collect records for final summary emission

## Policy Notes

- default compare behavior should be simple and reviewable
- custom compare logic must be replaceable without runtime rewrites
- summary aggregation should support both explicit flush and exit-time flush

## Open Questions

- Whether the summary recorder should keep in-memory detail entries only or allow streaming append behavior later.
