# Exact parallel hierarchical sparse elimination at D12 round 660

## Verdict

`PASS_EXACT_PARALLEL_HIERARCHICAL_ROUND660_PROMOTION_GATE` for the fixed
cold/rare, 16-worker solve kernel.  The promoted fair solve time is 3.342537
seconds versus the sealed sequential tree time of 8.726527 seconds, a
**2.610749x** speedup above the required 2x threshold.  Total source-to-result
wall time was 7.259070 seconds and peak RSS was 1,883,783,168 bytes, safely
inside the 120-second/8-GiB gate.

This is one solve at the already exposed round-660 state.  It performs no
round-661 incident search, materialization, CEGAR continuation, closure, rank,
Krylov, membership, or higher-degree work.

## Frozen inputs and exact result

- vector cache: 529,632,542 bytes, 246,321 strict column records, SHA-256
  `ecbcb26bcb8d2ecbb38cff4cce56457a960b2f11ba944536cd7bcf8d15b01275`;
- sequential checkpoint: round 660, 246,321 columns, support 352, SHA-256
  `92185737bc273f112f91240ee58eb8d0b4cd842739490838ebd30c870b8b6155`;
- prime: 1,073,741,827;
- variable terms: 24,950,813 across 16,179,918 distinct non-target rows.

The hierarchical output checkpoint is byte-for-byte identical to the sealed
sequential checkpoint and therefore has the same SHA-256.  Its candidate has
the same 352 rows, coefficients, and target normalization.  Because both the
exposed-column set and candidate are identical, their provider incidence union
and hence the actual next frontier are necessarily identical; a separate
frontier enumeration is neither needed nor claimed.

## Algorithm

The kernel freezes the native rare order exactly as `(global frequency, natural
Mono order)`, converts each source column into an augmented equation with the
target coefficient on the RHS, and partitions the 246,321 equations into 16
balanced contiguous ranges.  Worker 0 receives 15,396 equations; the remaining
15 workers receive 15,395 each, with exact no-gap coverage.

Each worker inserts equations in source order into a normalized rare-pivot
echelon basis and detects zero-row/nonzero-RHS inconsistency.  All 16 local
bases were consistent.  They are then merged in a deterministic fixed tree:

```text
16 local bases -> 8 -> 4 -> 2 -> 1 final basis
```

For each pair the left basis is retained and right-basis rows are inserted in
ascending rare-pivot order.  All 15 merge records were consistent.  The final
basis has 246,311 pivots and 25,081,520 terms.  Backsolve proceeds in descending
rare order with free variables fixed to zero.

## Fair timing comparison

The initial control exposed a tempting but unfair 31x arithmetic-only number.
It excluded the representation-specific rare-rank/materialization pass, while
the native sequential timer constructs its equation `BTreeMap`s inside
`sparse_solve_correction`.  The sealed promotion accounting therefore includes
both components:

| Fair solve component | Seconds |
|---|---:|
| Rare rank and equation materialization | 3.075534 |
| Parallel local bases, all merges, backsolve, and full verification | 0.267003 |
| Promoted hierarchical solve time | **3.342537** |
| Sealed sequential tree solve | **8.726527** |
| Fair speedup | **2.610749x** |

The remaining non-solve costs are separately reported: 1.581933 seconds for
source hashing, 2.267011 seconds to parse the cache and count frequencies, and
0.033943 seconds to atomically write/hash the identical checkpoint.

## Verification and referee

The producer verifies every augmented equation in parallel after backsolve.
The independent referee additionally:

- proves the 16 worker intervals are balanced, contiguous, non-overlapping,
  and cover exactly `[0,246321)`;
- proves all 15 pairwise records form the required `8/4/2/1` ancestry tree;
- checks all local/merged consistency and basis census identities;
- byte-compares the sequential and hierarchical checkpoints;
- replays the 352-entry candidate directly through every authoritative source
  vector: all 246,321 columns and 24,950,813 variable terms were scanned, 886
  terms hit candidate support, and zero pairings failed;
- rejects hostile speedup, worker-gap, missing-merge, unsatisfied-frontier, and
  unfair-timer mutations.

## Promotion and persistence scope

The fixture harness is intentionally round-660/hash locked; it does not itself
resume arbitrary checkpoints.  The kernel supports arbitrary equation slices
and is ready to integrate into the restored native outer loop for fixed
cold/rare 16-worker continuation.  That integration leaves the existing
checkpoint/vector-cache readers and writers untouched, so their schemas remain
identical.  Exact hook conditions and fail-closed controls are in
`INTEGRATION.md`.

Unsupported modes remain on their current paths: repair, portfolio comparison,
incremental bases, first/last pivots, and non-power-of-two merge trees.

## Evidence pins

- restored native baseline source:
  `241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0`;
- sibling producer source:
  `d289bc12ba16759c10dc5335057e8c8ed8edb476abbacb228af5c44871672579`;
- sibling producer binary:
  `89ae110e58ebbf478ead404d4f69662abc32db6e081cc37958fd808c646875aa`;
- result: `ae9ed09fcb6fd3608eb7eabe1edea42ce72627f9e9501bae06f97f3e2bdf6eb3`;
- independent audit: pinned in `MANIFEST.sha256` after report sealing.

No existing native source, checkpoint, or vector cache was mutated.
