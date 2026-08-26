# K21 remaining-22 exact computation design

## Verdict

`PASS_ONE_RETAINED_PATH_COMPLETE_AND_EXACT_BOUNDED_SCHEDULE_FOR_REMAINING_21`.

The retained literal path `D14:222|R:2-2-3` is now computed and independently
refereed.  Together with the previously accepted direct 16 and profile-ready
14, this raises strict K21 coverage from 30/52 to **31/52**.  The strict
assembler still correctly returns `REJECT_INCOMPLETE_K21_52_ID_GATE`; the
remaining work is exactly the 21 IDs listed below.  This is progress on the
K21 charge page, not a proof or disproof of the conjecture.

## Closed retained path

The exact source was the literal `H18PIV2` checkpoint
`checkpoint_k18_22_pivotable.bin` (158,439,965 canonical K18 rows,
12,675,197,280 bytes, SHA-256
`442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8`).
The hardened consumer read the complete checkpoint, made 399,275,484 selected
third-pivot evaluations and 12,776,815,488 K3 tail evaluations, and used an
exact 5,173,958-key response cache.  Its result is:

```text
D14:222|R:2-2-3
U                                      400591699200
full charge = irreducible charge       -1965744419617576058880 / U
reduced                                 -511912609275410432/104320755
elapsed                                 108.083473 s
```

For all 5,173,958 realized abstract response keys, the producer checked all
32 tails with
`!pivotable_sig(child_sig(parent_sig,pivot,tail,3),3)`, giving 165,566,656
exhaustive abstract terminal checks.  A separate referee also proves
terminality structurally: the K18 parent anchor sum is 6, a four-anchor pivot
removes 4, and every K3 tail restores 1, so every child has anchor sum 3 and
cannot contain a four-anchor pivot.  The 257 spaced literal samples replayed
21,664 children and independently agreed with the abstract cycle key.

Pinned producer/result evidence:

| item | SHA-256 |
|---|---|
| `run_k21_hidden_223_charge.rs` | `3a9d6f821e72d9782311b3e96378134df203099f3ef04d4c9f4b741d07c7062a` |
| `run_k21_hidden_223_charge` | `65d976e8ee0b7d9c4b49653300558108c1b800f179c7528ef5a98f689b823963` |
| `results_hidden_223_k21_charge.json` | `3bff6d8b0bcb7fc2c3508ab69f18d8df60f5d5ffa0aead0db33d3b40c677313d` |
| literal samples | `768e8e877e2d278be14563cf4ae78f7e4599c1e6a197389447f24763ce01be33` |
| independent referee report | `8a7d71de1047950b56b3d1e1638151c8a4cbe93cb4fc6205f48c93099aa8a276` |

The strict 31/52 manifest and rejected partial result are
`k21_manifest_direct16_profile14_hidden1_partial.json` (file SHA-256
`d31cd33f31401595be94d6878a408c0b18c58e5881a1ee3c41c50c4a0830d957`)
and `results_k21_direct16_profile14_hidden1_21_gap.json` (SHA-256
`050e76bc80243d09facafbea9cbdf1aa5eaaca2cee28a73db6b91b6869e625b1`).
They contain nine disjoint scalar groups and the exact current subtotal
`-9095494420915397632/521603775` for both full and irreducible charge.

### Post-design landed result

While this schedule was being sealed, the seven-ID group
`D17:{234,243,324,333,342,423,432}|R:2-2` landed separately at
`-196205097632820756480/U = -17142587904/35`, with 17,387,366,400 terminal
K21 occurrences.  Its result SHA-256 is
`9c217ea0a646ae8f7bceec1c1dd946d54b991b454046496fd7280127096a758c`
and producer-source SHA-256 is
`7999b1797e3103f254977b17f60ff42088f4eee6726ba4e7006b86f08cff05b7`.

The independent bounded referee in this package passed source hashes, exact
seven-ID set/order, factor-derived head counts, equality with the prior
independent K19 direct census, response/histogram/cache arithmetic, signs,
exact U division, and result reduction.  It explicitly found that the
producer's 257 spaced TSV witnesses all choose a zero-continuation first
pivot, so those samples are accepted only as source-row/mass/first-pivot
witnesses.  To avoid a vacuous terminal sample claim, the referee separately
derived one nonzero literal continuation for every one of the seven IDs at
source records `0,80,160,242,322,403,484`, then replayed both responses, all
216 resulting K21 children, terminality, and cycle charges.  The referee
result SHA-256 is
`fc6335ff4c0dd554322b01e4e84a4a79a0b73d2a7a024ca71c32fda73aeed789`.

This group is ready for the strict assembler.  The frozen strict artifact in
this directory remains the pre-landing 31/52 snapshot; after an assembler
adds the refereed seven-ID scalar, expected coverage is 38/52 and the live
computational gap is 14 IDs.  The 21-ID schedule below is retained as the
exact pre-landing design and workload ledger.

## Exact remaining-21 schedule

Every remaining path ends at a K19 parent followed by a terminal K2 response.
No complete global K19 or K21 row checkpoint is needed for the immediate
H-invariant charge: each source shard can apply the linear response operator,
divide exactly by its realized pivot multiplicities, and return only a scalar
and audit ledger.  Literal/decorated rows may be collected *within a bounded
shard* to remove duplicate work, but no multi-terabyte child stream is part of
this design.

| stage/source group | exact IDs | frozen source | exact known work before aggregation | collection decision |
|---|---:|---|---:|---|
| hidden D14 R2-3-2 | 1 | `hidden_k16_decorated_pair_orbits_full.bin`, 101,545,723 nonzero 53-byte decorated `(K16,pivot)` H-orbits, 5,381,923,399 bytes, SHA-256 `22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8` | 3,249,463,136 representative K3-to-K19 tails (the uncompressed literal count would be 16,367,267,840) | reuse the already complete decorated ledger; emit K3 tails shard-locally, then terminal K2; do not replay 75,691,040 parents or write K19 rows globally |
| direct D15 R4-2 | 3 | `checkpoint_direct_k15.bin`, 5,311,211 canonical rows, 169,958,768 bytes, SHA-256 `e79b752f94ad3b16ce4cf7d3f044e8887bda54bba5c6298ab31338bb121fa20f` | 44,342,881 selected pivots; 2,660,572,860 K4-to-K19 tails | stream record-index shards; optional shard-local decorated-pair/K19 folding only |
| direct D16 R3-2 | 6 | `checkpoint_direct_k16.bin`, 24,097,095 canonical rows, 771,107,056 bytes, SHA-256 `93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3` | 129,939,187 selected pivots; 4,158,053,984 K3-to-K19 tails | stream record-index shards; optional shard-local decorated-pair/K19 folding only |
| direct D17 R2-2 | 7 | literal direct-K17 formula in `run_k19_weight_runs.rs` (SHA-256 `dd3d885aa780bc99a4e8420bb84669141a14ea2df9cf097e11832b40830387b3`) over `filtered_k16_structure.bin` (115,275 bytes, SHA-256 `55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b`) | 82,938,880 K17 parents; 81,076,480 pivotable; 267,564,800 selected pivots; 3,210,777,600 K2-to-K19 tails | partition the 485 R8-prime source records; fuse both K2 responses and return scalar shards |
| D14 R3-2-2 | 1 | audited K14/R3 literal formula in the same pinned replay source and R8-prime structure | 838,080 heads; 211,816,960 K17 children; 197,414,400 pivotable; 815,482,880 selected K17 pivots; 9,785,794,560 K2-to-K19 tails | partition individual R8-prime records; two-level shard-local fold is optional, no global K17/K19 collection |
| D15 R2-2-2 | 3 | audited K15/R2 literal formula in the same pinned replay source and R8-prime structure | 6,704,640 heads; 671,208,960 K17 children; 451,445,760 pivotable; 1,876,057,600 selected K17 pivots; 22,512,691,200 K2-to-K19 tails | partition individual R8-prime records; two-level shard-local fold is optional, no global K17/K19 collection |

The exact 21 IDs are:

```text
D14:222|R:2-3-2  D14:222|R:3-2-2
D15:223|R:2-2-2  D15:223|R:4-2
D15:232|R:2-2-2  D15:232|R:4-2
D15:322|R:2-2-2  D15:322|R:4-2
D16:224|R:3-2    D16:233|R:3-2    D16:242|R:3-2
D16:323|R:3-2    D16:332|R:3-2    D16:422|R:3-2
D17:234|R:2-2    D17:243|R:2-2    D17:324|R:2-2
D17:333|R:2-2    D17:342|R:2-2    D17:423|R:2-2
D17:432|R:2-2
```

The table accounts for 45,577,353,340 planned pre-aggregation tail
evaluations.  Materializing one 40-byte `(K19 row,i128 weight)` record per
evaluation would require 1,823,094,133,600 bytes (about 1.66 TiB), so the
production contract forbids that output.  This is a workload ceiling, not a
disk projection: persistent production output is bounded shard JSON plus
samples and hashes.  Compression ratios, peak RSS, and exact output bytes are
measured at the prefix gate rather than guessed.

## Reusable exact engine contract

1. `ParentOrbit` supplies the literal row, signed coefficient at
   `U=400591699200`, orbit/stabilizer or literal multiplicity, lineage group,
   and exact source interval.
2. `DecoratedPairKey = canonical_H(parent_row, selected_pivot)` is the only
   valid H quotient for prolongation.  The 29-byte coarse profile is a cache
   key for an immediate invariant scalar only; it is not a source-faithful
   parent generator.
3. `ResponseEngine` supplies all 78 pivots, exact available-pivot count,
   `child_sig`, literal anchor replacement, K2/K3/K4 tail tables, H action on
   rows and selected pivots, and the guard `U % product(m_i) == 0`.
4. `TerminalK2Cache(profile29,signature12,pivot)` returns the unweighted sum
   over the 12 K2 tails and checks every realized child signature is
   nonpivotable before setting full equal to irreducible.
5. `fold_shard` streams a pinned source interval, optionally aggregates exact
   decorated pairs or canonical children within the shard, removes exact
   zeros, applies all remaining responses, and atomically emits a small JSON
   ledger.  It never emits a global child-row file.
6. `merge_scalars` verifies disjoint interval coverage, source and engine
   hashes, record/use/mass conservation, exact denominators, deterministic
   literal samples, and the exact ID union before summing over `Q`.

## Mandatory gates and launch order

1. Freeze source, engine, DAG, and tail-table hashes.  Exhaustively check H
   equivariance on all `384*78*tail_count` action cases, exact denominator
   products, and literal-versus-abstract cycle keys.  Include a hostile test
   proving a coarse-profile collision cannot be used to generate children.
2. For each of the six source groups, run only one R8-prime record, 10,000
   direct-checkpoint records, or 100,000 decorated-pair records.  The literal
   occurrence fold and optimized shard fold must agree exactly in counts,
   masses, charge, and samples.
3. A pilot is refused or stopped above 8 GiB RSS or 300 seconds.  It may write
   only an atomic result, bounded samples, and restart metadata.  Use its
   measured pair/child compression to select production shard sizes.
4. Run production shards independently with interval manifests; merge only
   after complete no-overlap/no-gap coverage and an independent source/formula
   referee.  Add the resulting six disjoint group scalars to the strict 52-ID
   manifest only when their exact 21-ID union passes.

The principal blocker is compute throughput for the two deep replay groups,
especially the 22.5-billion-tail D15 R2-2-2 group, not missing mathematical
provenance.  If K21 rows are later needed for K22, this charge-only schedule is
not sufficient: a separate canonical K21 coefficient checkpoint must be
collected.
