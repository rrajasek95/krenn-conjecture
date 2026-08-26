# Exact K24 35-lineage availability, schedule, and residual contract

## Verdict

**PASS as an exact availability, recurrence, terminality, and bounded scheduling theorem. No K24 charge or row residual was run.**

The frozen DAG contains exactly 35 reachable K24 lineage IDs. The machine ledger partitions all 35 into 10 strict scalar groups and six physical source folds with no missing, duplicated, or extra ID:

| Usable interface | IDs |
|---|---:|
| retained immediate K20 outgoing-pivot profile | 0 |
| exact source replay from pinned literal/factor input | 35 |
| genuine provenance gap | 0 |

The result is `results_k24_availability_schedule.json`, file SHA-256 `ec91fa81b164d1ecd83d234f5aa5d6c8ae5921f76f7b6d5c2145c4be3737f733`, logical SHA-256 `3cd80f27b12cdaafc0cb74d4e33736e2318a6f0df4d9fdfb0f4503c4de96224a`. It pins the frozen recurrence DAG at file SHA-256 `469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa` and logical SHA-256 `ad59639716fe2a2cc04fca83a189d74ff8c1f5bbe6d7257676dd458f4c768a66`.

## Exact 35-ID partition

Every K24 edge is a K4 response from an immediate K20 parent. The strict source groups are:

| Direct family | Frozen response sequences | IDs |
|---|---|---:|
| D14:222 | `2-2-2-4`, `2-4-4`, `3-3-4`, `4-2-4` | 4 |
| D15:{223,232,322} | `2-3-4`, `3-2-4` | 6 |
| D16:{224,233,242,323,332,422} | `2-2-4`, `4-4` | 12 |
| D17:{234,243,324,333,342,423,432} | `3-4` | 7 |
| D18:{244,334,343,424,433,442} | `2-4` | 6 |
| **Total** | **10 scalar groups** | **35** |

The audit checks each ID against its unique frozen parent edge, shift 4, 60 K4 tails per selected pivot, occurrencewise `-parent/pivot_count` rule, sign flip, reachability, and exact denominator-product LCM divisibility by `U=400591699200`. The two DAG-era discarded descendants (`D14:222|R:2-2-2-4` and `D14:222|R:2-4-4`) are repaired by the now-retained hidden `H18PIV2` and decorated `H16ORM1` sources.

## Universal terminality

Every immediate K20 parent has anchor mass 4. A response removes a mixed K0 pivot of anchor mass 4 and inserts a K4 tail of anchor mass 0:

```text
child anchor mass = 4 - 4 + 0 = 0.
```

Every possible pivot requires anchor mass 4, so all 35 K24 outputs are terminal. A future K24 charge must therefore have full charge equal to irreducible charge. This statement does not imply that the terminal residual belongs to the literal mixed ideal; that is the separate span test described below.

## Actual prolongable inputs

No K22 or K23 scalar is an input. Those terminal scalar outputs retain neither literal K20 parent rows nor outgoing selected-pivot occurrences. The schedule instead pins and replays the following literal/factor sources:

| Input | Geometry | SHA-256 |
|---|---:|---|
| frozen R8/factor structure | 485 R8 records; 115,275 bytes | `55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b` |
| K2/K3 response auxiliary | 14,364 bytes | `f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab` |
| K4 response table | 60 tails/pivot; 18,727 bytes | `4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3` |
| direct K16 canonical rows | 24,097,095 records | `93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3` |
| decorated hidden K16/pivot orbits | 101,545,723 records | `22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8` |
| collected hidden K18 pivotable rows | 158,439,965 records | `442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8` |

The direct K15 checkpoint is pinned as an available alternative, but it is not selected: the grouped K15 fold replays the frozen 485-slice R8/factor source. Every selected group names its actual source artifact in the ledger. Five completed K22 producer sources are hash-pinned only as reader/source-linear engine starting points; none of their scalar results is evidence for K24.

## Six bounded physical folds

All ten named sinks remain separate through shard production and audit. The exact integer half-open intervals are recorded in `physical_schedule` in the result JSON.

| Physical fold | IDs | Initial shards | Conservative initial maximum |
|---|---:|---:|---:|
| collected hidden K18 | 1 | 6 balanced over 158,439,965 records | 390 s |
| decorated hidden K16/pivot pairs | 1 | 6 balanced over 101,545,723 records | 465 s |
| K14 R8 source | 2 | 8 balanced over 485 slices | 300 s |
| grouped direct K15 R8 source | 6 | 16 balanced over 485 slices | 430 s |
| grouped direct K16 checkpoint | 12 | 6 balanced over 24,097,095 records | 380 s |
| direct D17/D18 R8 sectors | 13 | 8 balanced over 485 slices | 385 s |

This is 50 initial restartable atomic shards. The walls are conservative planning extrapolations from the measured lower-degree source engines and the exact final-tail multiplicity; they are not launch authority. Every new mode must pass its named tiny, intermediate, and representative prefix. A shard launches only if its newly measured projection is at most 540 seconds and family RSS at most 8 GiB; otherwise it is bisected and re-gated. The watchdog is 570 seconds, hard wall 600 seconds, aggregate live RSS 16 GiB, and shards run sequentially. Merge requires exact gap-free/no-overlap coverage, atomic outputs, separate sinks, 257 distributed nonzero literal replays per family/mode, and exact `U` arithmetic.

Charge mode may source-fold to integers without emitting parents. Residual mode is separately gated: it uses the same source intervals but writes sorted exact H-row-orbit runs and measures unique-row rate, bytes per row, wall, RSS, and disk on every prefix. A projected materialization at or above 1 TiB is not launched without explicit capacity approval.

## Literal K24 residual required for the terminal span test

`literal_k24_residual_interface.schema.json` (SHA-256 `9d6183177027a4bd08d53488f3da4acfd3fc4e01aed408f579764a1d4fcc523b`) freezes the load-bearing contract. Each separately named group/shard run must retain:

- the H-canonical sorted 24-cell row (48 lowercase hex characters), H-orbit size, and total exact rational mass on that orbit;
- group ID, physical source family and exact source interval, all source and engine digests, recurrence and H-canonicalization policy IDs, exact-zero/run/row counts, and content digest; and
- for the distributed referee samples, the source cursor, lineage, ordered pivot indices and tail ordinals, emitted literal row, canonical row and H-action witness, and exact signed fraction.

Runs must survive until a cross-group exact external merge. Only an exactly zero accumulated orbit mass may be removed. The final merged target needs complete 35-ID coverage and every nonzero H-row-orbit mass.

This row data is strictly stronger than a charge. The corrected Gram interface indexes literal columns by `(mixed word w, 20-cell multiplier U)`, not by the 1,757 decorated-matching H-orbits. A charge scalar, support-only set, anchor signature, or decoration index cannot seed the target-rooted literal-column closure. After the residual exists, every literal column incident to its nonzero rows must seed the multiplier-aware Gram provider, every reached component must close to `COMPLETE`, and any rank equality or separator must be replayed over Q.

## Strict future charge assembler

`assemble_k24_35_exact.py` freezes the ten group identities and ordered IDs, exact degree and `U`, evidence hashes, rational/scaled agreement, and terminal full/irreducible equality. Standard, optimized, and isolated/no-site hostile selftests reject missing, duplicate, extra, regrouped or reordered IDs, wrong `U`, full/irreducible disagreement, scalar/rational mismatch, and evidence-hash mutation. A grouped scalar is counted once, and every charge result explicitly remains `terminal_span_ready=false`.

The availability-only manifest intentionally assembles to `REJECT_INCOMPLETE_K24_35_ID_GATE` with 0/35 charge paths and zero placeholder total. No K24 charge, row residual, span-membership, or conjecture claim is made here.

Replay:

```sh
python3 computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/audit_k24_availability.py
python3 computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/assemble_k24_35_exact.py --self-test
python3 computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/assemble_k24_35_exact.py --audit-incomplete \
  computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/k24_manifest_availability_only.json \
  computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/results_k24_0_of_35_gap.json
```
