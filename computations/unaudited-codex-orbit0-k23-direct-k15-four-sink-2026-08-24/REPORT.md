# K23 grouped direct-K15 four-sink / twelve-ID prefix gates

## Verdict

`PASS_K23_GROUPED_DIRECT_K15_12_ID_PREFIX_GATES_FULL_HELD` for the four strict grouped paths `R:2-2-4`, `R:2-3-3`, `R:3-2-3`, and `R:4-4`, each over the frozen packet labels `223`, `232`, and `322`. This is exactly 12 unique K23 lineage IDs. The 1/8/32-slice gates and an independent 257-source literal referee pass. Full production was not launched.

## Source-linear recurrence

The producer reconstructs exactly 13,824 labelled direct-K15 heads from each of the 485 frozen R8 slices in `filtered_k16_structure.bin` (SHA-256 `55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b`). It preserves packet provenance throughout and groups only at the three labels required by the frozen DAG; it does not claim individual packet scalar splits.

Each sink walks every literal tail and every available pivot occurrence:

- `R:2-2-4`: K2 -> pivotable -> K2 -> pivotable -> terminal K4.
- `R:2-3-3`: K2 -> pivotable -> K3 -> pivotable -> terminal K3.
- `R:3-2-3`: K3 -> pivotable -> K2 -> pivotable -> terminal K3.
- `R:4-4`: K4 -> pivotable -> terminal K4.

The direct-K15 head coefficient is `-positive`; every selected pivot flips the sign and divides by its realized multiplicity. Every recorded denominator product divides `U=400591699200` exactly. Every realized final response cache key is exhaustively expanded: every K23 child has anchor-signature mass 1, below pivot mass 4, so all are terminal and full equals irreducible.

## Prefix gates

| Slices | Heads | Wall (s) | Linear full projection (s) |
|---:|---:|---:|---:|
| 1 | 13,824 | 24.708038 | 11983.398592 |
| 8 | 110,592 | 28.181263 | 1708.489057 |
| 32 | 442,368 | 117.827111 | 1785.817144 |

The 32-slice gate is the production sizing authority. It evaluated 45,279,805,440 / 12,610,174,976 / 6,798,966,784 / 7,726,694,400 terminal K23 occurrences in the listed sink order, with exact full=irreducible charge and occurrence identities.

## Independent literal referee

The referee sampled 257 distributed R8 slices spanning indices 0 through 484. For each source it selected packet label `322`, `232`, or `223` cyclically, giving 86/86/85 witnesses per sink, and found a nonzero literal continuation through every pivot stage. It expanded 1,028 sink witnesses without the producer cache, asserted every division, rebuilt every final row, verified terminal anchor-signature mass 1 and no available pivot, and retained the complete literal continuation ledger.

## Held production schedule

The exact atomic intervals are `[0,60)`, `[60,121)`, `[121,181)`, `[181,242)`, `[242,303)`, `[303,363)`, `[363,424)`, and `[424,485)`. They are gap-free and non-overlapping.

Scaling the 32-slice gate to the largest 61-slice shard and applying a 2x safety factor gives 449.216 seconds, below the 540-second launch gate and 600-second hard stop. The per-family RSS gate is 8 GiB and aggregate gate is 16 GiB. Each worker keeps a reusable recurrence plan and a terminal response cache scoped to one source slice; the cache is dropped between slices and no rows are emitted. Full shards require explicit clearance and must be retained atomically for an exact interval merge.

The machine-readable authority is `results_k23_direct_k15_four_sink_gate_audit.json`, logical SHA-256 `76421930a84a304fcf3e23a0dfd54b60866c6704f966df0a04b9a49bead7d50d`. Scope excludes K24, membership, and a conjecture verdict.
