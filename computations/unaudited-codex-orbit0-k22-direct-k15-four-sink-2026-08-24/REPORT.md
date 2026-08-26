# Grouped direct-K15 four-sink K22 charge

Status: `PASS_INDEPENDENT_STRICT_GROUPED_DIRECT_K15_FOUR_SINK_K22_AUDIT`.

This package evaluates exactly the following four grouped recurrence sinks, with packet witnesses `223`, `232`, and `322` retained as grouped source classes. Individual packet scalars are deliberately `null`; no split is inferred.

| Sink | Terminal K22 occurrences | Charge scaled by U | Exact charge |
|---|---:|---:|---:|
| `D15:{223,232,322}|R:4-3` | 62,457,446,400 | 208,523,010,296,453,529,600 | 921871950848/1771 |
| `D15:{223,232,322}|R:2-2-3` | 366,011,760,640 | 2,213,434,782,746,883,514,368 | 29111884242777824/5268725 |
| `D15:{223,232,322}|R:2-3-2` | 71,671,111,680 | 397,889,178,859,017,584,640 | 1046636097587904/1053745 |
| `D15:{223,232,322}|R:3-2-2` | 38,642,565,120 | 397,229,342,071,225,466,880 | 19470194083264/19635 |

Here `U = 400591699200`. Every denominator product observed by the producer divides `U` exactly. The two-response path has recurrence sign `−`; each three-response path has sign `+`.

## Coverage and resource gates

The rejected monolithic projection was 1,270.64 seconds, above the 600-second gate. The full source interval of 485 frozen R8 slices was therefore evaluated as four atomic, gap-free shards:

- `[0,122)`: 337.592894 seconds, SHA-256 `4a071a49705c89375343628e1889de2892e9ebe90d28be304ffed33ca1962163`
- `[122,244)`: 325.319662 seconds, SHA-256 `e4ca50de6df955e68afd487f7046bdabb1dac9d0afdbdf9c432d2c218bb8d09e`
- `[244,365)`: 326.472028 seconds, SHA-256 `a9a920f6ca2a9f92cb48403c8a66cee451cd053de93082c65ce79c7bee7aabe4`
- `[365,485)`: 316.467832 seconds, SHA-256 `ea26f855b4e78bc2545d64f5d7ae28814a5dacf75f13db31b96f02c3e9bb212e`

All shards stayed below 600 seconds and sampled RSS stayed below 2.3 GiB. The `/usr/bin/time -l` wrapper around shard 0 returned 1 only because the sandbox denied `sysctl kern.clockrate`; the producer itself completed and atomically wrote the valid JSON checked above.

The merged result covers 6,704,640 direct-K15 source heads per sink. Exact ordered interval and strict 12-ID guards reject missing, duplicate, unexpected, reordered, or individually split groups.

## Terminality and independent replay

Each path removes total anchor mass 7 from a K15 signature of mass 9. Thus every K22 child has anchor mass 2, strictly below pivot mass 4; exhaustive literal checks also found no available child pivot. Consequently full equals irreducible for every sink.

The independent cache-free referee sampled 257 source slices from 0 through 484, with packet witness counts `86/86/85` for `322/232/223` in each sink. Across 1,028 source/sink witnesses it reconstructed every intermediate row, recomputed every signature, preserved source provenance through every pivot, checked each exact denominator, and evaluated 39,120 literal terminal K22 children. A separate Python audit recomputed all 1,028 sampled recurrence signs and `U/(m1*m2*...)` scalars from the TSV.

The referee one-sample gate initially caught an incorrect expected-mass assertion in the referee only (`4−degree` rather than `degree`). It produced no accepted referee result. The corrected guard passed the one-sample gate and the full 257-sample replay; the production shards and merged scalar were unaffected.

## Pinned outputs and scope

- Merged result SHA-256: `50ea88f5da6921db8017f9e2e7e143cc6d0426ddaeb2a6daf8050a07ac33e5da`
- Literal referee SHA-256: `c989e6804c0bc74ccda92999d9976824e85e6484c0747c28f56068c9fb3498de`
- Literal TSV SHA-256: `ab93c4e9c4b3718ea248098ed56572712e3c863e96c13fa823857dfb05303dd6`
- Independent audit SHA-256: `c18e3d234de1f0b6937fcb98bc95dcf048e5a89bbc758413d3257f82816d2612`
- Audit logical SHA-256: `1a343932d82efcfa2b9532d77d912ab947f255de9d88b94f1ad6b422df7c460f`

Scope is exactly these 12 K22 lineage IDs. No parent rows, K23, or K24 were emitted or inferred.

The separate hidden collected-K18 two-ID fragment remains unchanged and outside this merge: result `2c15fbf93a2f33a8d3819b8a8eca281b9b27326aa82e98d5610443937362bde5`, audit `38c41beea1a959c569f42cd18c087820152bc1819c7fe138f14c714897a27901`, logical `52bce2d91e3b59fe0bd78e0bbf8932d307d2b91510d55231b57af8058d24b4b5`, manifest `d31d5251ebc58637ecc1e12358594ee37d69a63268898081c55f1b08a9e209d0`.
