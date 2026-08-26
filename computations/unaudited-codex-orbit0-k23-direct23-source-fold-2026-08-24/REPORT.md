# K23 direct D17--D19 physical-source fold: bounded gate report

Status: **PASS** for the four exact grouped scalars covering exactly 23 frozen K23 IDs: seven `D17:*|R:2-4`, seven `D17:*|R:3-3`, six `D18:*|R:2-3`, and three `D19:*|R:4`. This is a strict partial K23 fragment, not the complete 59-ID result, and it does not compute or emit K24 data or individual rows.

The source is the frozen 485-record physical `R8` ledger parsed by the retained K18 engine. Every D17/D18 occurrence constructs the literal K19/K20 intermediate row, enumerates its actual pivots, divides the exact scale `U=400591699200` by both realized pivot multiplicities, and charges only its literal terminal K23 children. D19 uses one response and exact `U/m1`. With the inherited direct source coefficient `-M`, the signs are `-M/(m1*m2)` for D17/D18 and `+M/m1` for D19.

Terminality is exhaustive over realized abstract response keys: before caching a response, the engine checks every one of its 32 or 60 tails and asserts that the child signature has no frozen pivot. The cache stores equal full and irreducible counts/charges only after these assertions. Distributed samples additionally retain a nonzero literal terminal row and charge, rather than only an aggregate response value.

## Gates and production plan

The one-record/one-worker gate passed in 7.762317 seconds with peak per-record caches of 1,640,960 literal first-response keys and 312,826 terminal keys. The evenly distributed eight-record/eight-worker gate selected source indices `0,69,138,207,276,345,414,484`; it passed in 10.760670 seconds with peaks 1,640,960 and 493,731, and performed 109,333,740 terminality assertions. Both peaks are below the hard 2,000,000 / 1,000,000 key caps.

The representative projection for a single 485-record run is 652.365631 seconds, so a broad pass is rejected by the 600-second gate. Production is fixed to three atomic, non-overlapping intervals:

1. `[0,161)` (161 records), projected about 217 seconds.
2. `[161,323)` (162 records), projected about 218 seconds.
3. `[323,485)` (162 records), projected about 218 seconds.

`merge_k23_direct23_shards.py` accepts only those exact intervals, the exact four ID arrays, and the exact terminal multiplicities `60*p2`, `32*p2`, `32*p2`, and `60*p1`. It sums degree-separated scalars and denominator histograms, rejects gaps/overlaps, verifies full=irreducible, enforces cache caps, and requires the global witness ordinals to be exactly `0..256`, with every group represented. The preferred group is `ordinal mod 4`; if that group has no nonzero response on the selected record, the producer advances cyclically to the first group having a nonzero literal terminal child. This source-record fallback is necessary at record 429, whose preferred D19/R4 response sum is zero, and is recorded explicitly by the group column rather than hidden.

Resource clearance was given before production. The three shards completed atomically in 192.827068, 183.521579, and 212.132176 seconds. Their exact no-gap merge has SHA-256 `e84a39d027e07ad56d1c4d67dd9cab733ef25575aa324c892157deb80272767f`.

## Exact result

| group | IDs | terminal K23 occurrences | scaled charge | exact charge |
|---|---:|---:|---:|---:|
| D17 R2-4 | 7 | 86,936,832,000 | -603757293605464965120 | -52750731776/35 |
| D17 R3-3 | 7 | 26,953,646,080 | -283096452568920883200 | -4946870272/7 |
| D18 R2-3 | 6 | 7,390,003,200 | -51016487368812134400 | -127352832 |
| D19 R4 | 3 | 6,704,640,000 | -3960127758414643200 | -9885696 |

The strict 23-ID subtotal is scaled `-941830361301612625920`, or `-82288431616/35`. Full and irreducible values agree groupwise and in the subtotal. Across the three shards, 7,194,103,212 terminal-child assertions were made on realized response keys; peak per-record caches were 1,640,960 literal first keys and 522,062 terminal keys.

The merged witness ledger has SHA-256 `5968ec8c82678f79887cc208420108ec2878d9ab820793e818dd4c16402a804f`. The independent Rust referee replayed all 257 source records (group counts 66/64/64/63), checked physical source-family membership and mass, rebuilt 194 literal intermediates and all 257 recorded terminal rows, rechecked exact `m1/m2` and `U` division, and exhaustively checked 11,836 terminal tails. Its only preferred-group fallback is the explicitly recorded ordinal 227 / source record 429 case.

`k23_direct23_fragment_manifest.json` is directly consumable by the frozen strict 59-ID assembler. Its partial-integration audit must report exactly 23 covered IDs, four groups, no duplicate or extra ID, and the remaining 36 IDs; it must not claim a complete K23 result.
