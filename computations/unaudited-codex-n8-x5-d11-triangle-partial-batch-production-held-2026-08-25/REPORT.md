# Held D11 deterministic partial-batch production continuation

Status: **READY/HELD pending explicit `D12_RESOURCE_CLEAR`; no launch.**

This package freezes one p107 triangle continuation from the independently
replayed 913,636-column / 924,170-support checkpoint using sealed patch manifest
`54c4d29d...`.  The exact source is `261f03cf...`, binary `72c8a091...`,
provider `06df5052...`, seed selected `81b4c5b8...`, and seed dual
`c2c0d95e...`.  The sole resource change from the diagnostic is native 590 /
wrapper 600 seconds; RSS remains 38 GiB.  The runner refuses without an exact
clearance stating that r1587 producer hashing is complete and D12 resources are
clear.

The single allowed run scans the entire source-faithful incident frontier,
retains the natural `(generator,multiplier)` minimum prefix fitting the 336,365
remaining slots, inserts it, recomputes the normalized exact modular dual,
literally verifies every selected pairing, persists dual then selected
atomically, and stops at `INCOMPLETE_COLUMN_CAP`.  No automatic relaunch is
implemented.

Frozen acceptance requires the seed-stable full scan counts already measured by
the top-eight gate (762,110 incident columns and 730,426 violations), exactly
336,365 accepted prefix columns, 1,250,001 selected output columns, seed subset
preservation, every addition nonzero on the seed dual, target coefficient one,
and zero failures when all output columns are replayed.  It also checks that the
first eight additions equal the independently replayed top-eight gate, the
watchdog has no breach, no temporary output remains, and all output hashes are
recorded in the audit.

Prelaunch audit is PASS: exact command/pins, absent production output, runner
refusal without clearance, and nine hostile contract mutations all verified.
The production validator is frozen before arithmetic.  No p2, other branch,
D12 read, or mathematical verdict is authorized.
