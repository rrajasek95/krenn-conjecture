# K24 exact charge-only fast-route audit (2026-08-24)

## Outcome

The frozen K24 interface partitions exactly into **10 group scalars / 35 lineage IDs / 6 physical source families**.  Every family now has an exact scalar-only producer and a successful bounded gate.  No producer emits K24 rows or columns.  The direct D17/D18 family is complete and independently validated; the other five remain held.

This package is charge-only.  It does not supply the residual row-orbit data needed for terminal-span membership and does not prove the conjecture.

## Exact family partition and schedule

| family | frozen groups | IDs | gate | production geometry |
|---|---:|---:|---|---|
| hidden collected K18 | 1 | 1 | 1,000,000 rows, 2.909s; full linear projection 460.843s | 3 no-gap intervals of about 52.8m rows |
| hidden decorated K16 pair | 1 | 1 | 1,000,000 rows, 3.736s; full projection 379.365s | 3 no-gap intervals of about 33.85m rows |
| K14 source formula | 2 | 2 | 8 distributed R8 slices, 4.116s; full projection 249.527s | complete in 180.344s; 257 literal samples per sink; independently validated |
| grouped direct K15 source | 2 | 6 | 8 slices, 11.689s; monolithic projection 708.663s | 16 no-gap intervals of at most 31 slices, about 45.5s projected each |
| grouped direct K16 checkpoint | 2 | 12 | 262,144 rows: R2-2-4 6.983s / R4-4 4.793s | 6 no-gap intervals; run the two exact sinks separately, about 107s and 74s per interval |
| direct D17/D18 formula | 2 | 13 | 61 slices, 41.508s; full projection 330.021s; observed RSS 4,954,496 KiB | complete in 299.831s; independently validated |

The first attempted grouped K16 R4-4 full run was rejected with no result: after completing its traversal, the producer's full-only witness assertion found only 37 of 257 equal-index-bin nonzero samples. It exited 101 before any JSON, sample ledger, or temporary output was published. The atomic guard therefore worked, but the earlier full-launch acceptance is retracted. K16 R4-4 adds zero coverage until a sample-only repair is independently frozen and replayed.

Every atomic job has a 600-second hard watchdog and must remain below 8 GiB family RSS.  Interval assembly is fail-closed on gap or overlap.  Exact interval lists, source/binary hashes, and gate hashes are in `results_k24_charge_only_fast_schedule.json`.

## Exactness and compression

All recurrence steps before the terminal response retain literal source rows, pivot occurrences, signs, and occurrencewise divisor products.  Only the final K4 response is cached, keyed by the complete profile/signature/pivot/degree tuple.  Thus retained profiles/checkpoints avoid all K24 row/column output without using or prolonging K22/K23 charge scalars.

Every immediate K20 parent has active-anchor mass 4.  Removing the selected pivot subtracts 4 and a K4 tail adds 0, so every K24 child has mass 0 and cannot contain another frozen pivot.  Producers also exhaustively assert this on every newly realized terminal response key.  Hence full charge equals irreducible charge for all 35 IDs.

The charge-only direct D17/D18 prefix1 agrees exactly with the independent factorized residual provider:

- D17 R3-4: 1,736,704 selected pivots, 104,202,240 terminal occurrences, scaled charge 825,568,674,132,787,200 = 14,426,112/7.
- D18 R2-4: 476,160 selected pivots, 28,569,600 terminal occurrences, scaled charge -85,322,827,196,006,400 = -212,992.

## Coverage and assembler contract

The schedule audit re-derives the group partition from the sealed availability DAG and proves exact equality: 10 unique groups, 35 unique IDs, no missing or extra ID.  It pins every producer, binary, and gate result.

The existing strict assembler is reused unchanged.  Each group scalar is consumed exactly once, never multiplied by the number of IDs sharing that scalar.  Its hostile replay rejects missing, duplicate, extra, regrouped, reordered, wrong-U, nonterminal, inconsistent rational, and stale-hash inputs.  The new schedule audit additionally rejects interval gaps/overlaps and unsafe shard projections.

## Provenance limits

- Early `/usr/bin/time` max-RSS accounting was unavailable in the sandbox.  The direct 61-slice gate was sampled live at 4.725 GiB.  Each other family remains subject to a live first-shard RSS gate in addition to explicit cache caps.
- The upstream hidden include chain now contains two colliding dormant `main` functions and is not directly recompilable.  This package pins local copies that only rename those dormant entrypoints and redirect the include; recurrence logic is unchanged.
- The K15 and K16 retained sources support only their frozen grouped scalars, not individual packet charges.
- No charge-only artifact is sufficient for K24 terminal-span membership; the separate residual provider remains required.

## Scope

Exact K24 filtered charge only.  No K25, no membership claim, no terminal-span claim, and no conjecture verdict.

The completed direct D17/D18 and K14 source families cover 15/35 IDs.  Their strict partial subtotal is `1224664502489728/1053745` (scaled `465568457266494996480`).  The assembler correctly labels this as an incomplete 20-ID-gap result, not a complete K24 aggregate.
