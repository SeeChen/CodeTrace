# Pipeline State

## Status

- Pipeline Status: `in_progress`
- Current Stage: `legacy_cleanup`
- Last Completed Stage: `migration_scaffold`
- Next Stage: `pipeline-init`
- Active Flow Version: `refactor-v1`

## Stage Checklist

- [ ] Stage 0: Pipeline Init
- [ ] Stage 1: Generate SA
- [ ] Stage 2: Generate Build Spec
- [ ] Stage 3: Slice Work
- [ ] Stage 4: Implement
- [ ] Stage 5: Verify
- [ ] Stage 6: Accept

## Current Focus

- Land the refactored workflow assets.
- Remove legacy pipeline assets while preserving external reviewable documents.
- Move future work to the new stage model.

## Blockers

- `none`

## Notes

- Update this file after every completed stage.
- If a stage is blocked, record the blocker before stopping.
- If the workflow shape changes materially, update the active flow version.
