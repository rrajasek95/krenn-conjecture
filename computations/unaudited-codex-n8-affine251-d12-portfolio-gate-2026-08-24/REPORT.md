# D12 exact sparse continuation and portfolio gate

This package continues the exact affine-251 D12 CEGAR computation from the
sealed round-538 state.  It does not claim D12 membership or nonmembership.

## Accepted continuation

The warm-cache run advanced from round 538 / 147,230 exposed columns / 233
dual rows to round 634 / 221,914 columns / 307 rows.  It stopped only at the
540-second wall gate (`INCOMPLETE_RESOURCE_GATE`, `WALL_CAP`), with peak RSS
6,083,536 KiB.  `audit_continuation.py` independently checks the result,
checkpoint and `AFF12VEC1` cache headers, sizes and hashes.  The five hostile
mutations all fail before an audit artifact is written.

The authoritative continuation artifacts are:

- `results_continuation_round700.json`;
- `period1_checkpoint.bin`; and
- `period1_vectors.bin` (221,914 vectors, 476,801,635 bytes).

Both mathematical verdict fields remain null.

Subsequent exact cold/rare continuations and periodic exact portfolio audits
advance the accepted state through rounds 660, 697, 698, 730, 731, and 748.
The current accepted endpoint is round 748 / 333,199 exposed columns / 436
dual rows, with checkpoint SHA-256
`fe44b33e74b7e9ce00a7654fe8f027b0024b15e464bbaa372ec85ea92bc097c6`
and vector-cache SHA-256
`7af04cecc244e158af1df5b782cbe5b2e23d191b4d06b43a1c0c33911e5c6cab`.
The extended audit validates every intermediate result/checkpoint/cache triple
and their exact resume chain.  Its five hostile mutations still reject before
an audit artifact is written.  This endpoint remains incomplete: both
mathematical verdict fields are null.

## Rejected every-round portfolio

Starting from the identical round-538 checkpoint, an exact six-way portfolio
was run every round through round 546.  Every one of the eight rounds still
selected `cold/rare`; it changed no selected search strategy while increasing
solve cost and transient memory.  The production period therefore remains 32.

## Rejected ranked-vector elimination

A temporary exact kernel ordered every sparse row by the same rarity priority
as the accepted B-tree solver and used linear vector merges.  At round 635 it
produced the identical state (222,676 columns, 315 support rows), byte-identical
checkpoint, and byte-identical vector cache.  Its solve took 7.580372 seconds
versus 6.230818 seconds for the tree kernel (1.2166x slower), so it was fully
reverted and is not promoted.

The original main source and release binary were restored byte-for-byte after
the rejected experiment.  Their hashes again match the sealed parent package:

- source `241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0`;
- binary `a3761406b3ce0fc0ef658bfc876dcdb7727e6d6b10bae42a981f6e6a8c71f47a`.

No higher-degree inference is made.
