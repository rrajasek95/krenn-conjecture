# Exact K23 59-lineage availability and bounded schedule

## Verdict

**PASS as an availability, terminality, and execution-schedule theorem. No K23 charge was run.**

The frozen recurrence DAG has exactly 59 reachable K23 lineage IDs. The machine ledger partitions them with no omission, duplicate, or extra:

| Current usable interface | IDs | Consequence |
|---|---:|---|
| retained immediate K19/K20 terminal-profile interface | 0 | no K23 group may start from a profile artifact |
| exact source replay required | 59 | reconstruct the literal K19 or K20 parent and fold its final response |
| genuinely missing provenance | 0 | every replay has a pinned literal checkpoint or frozen R8/factor source |

The zero in the first row is material. Existing enriched terminal profiles have immediate parent degree K18 and close named K22 K4 sinks only. The frozen K19 charge profiles encode an incoming terminal response and scalar; they do not retain literal K19 rows or an outgoing selected pivot. K20--K22 scalar outputs, caches, and sample ledgers are likewise not parent interfaces.

The result ledger is `results_k23_availability_schedule.json`, SHA-256 `45550f92ea0cae4d988e1cc1c13117134a6c78a66d68c3e4950d3ec24e2dbb15`, logical SHA-256 `ddab2f6c3c445fe27d83d7587b1d89afe0af078842b4c99ecd53c615864b9562`. It is derived from frozen DAG file SHA-256 `469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa` and DAG logical SHA-256 `ad59639716fe2a2cc04fca83a189d74ff8c1f5bbe6d7257676dd458f4c768a66`.

## Exact 59-ID shape

Every K23 path ends at a parent earlier than K21:

| Immediate parent | Final response | IDs |
|---|---:|---:|
| K19 | K4 | 24 |
| K20 | K3 | 35 |

There is no K21-to-K23 K2 response. Every realized K21 child already has anchor mass 3, below pivot mass 4, so it has no outgoing pivot.

The strict scalar-group partition is:

| Direct family | Frozen response sequences | IDs |
|---|---|---:|
| D14:222 | `2-2-2-3`, `2-3-4`, `2-4-3`, `3-2-4`, `3-3-3`, `4-2-3` | 6 |
| D15:{223,232,322} | `2-2-4`, `2-3-3`, `3-2-3`, `4-4` | 12 |
| D16:{224,233,242,323,332,422} | `2-2-3`, `3-4`, `4-3` | 18 |
| D17:{234,243,324,333,342,423,432} | `2-4`, `3-3` | 14 |
| D18:{244,334,343,424,433,442} | `2-3` | 6 |
| D19:{344,434,443} | `4` | 3 |
| **Total** | **17 scalar groups** | **59** |

The JSON includes a 59-entry individual lineage ledger with its exact group, source family, immediate parent, final shift, frozen provenance state, and terminality proof. The three DAG-era discarded descendants `D14:222|R:2-2-2-3`, `D14:222|R:2-3-4`, and `D14:222|R:2-4-3` are no longer provenance gaps: the hidden `H18PIV2` and decorated `H16ORM1` sources are present and pinned.

## Universal terminality

For a final response of shift `s` from parent degree `p=23-s`, anchor mass changes by

```text
(24-p) - 4 + (4-s) = 24-(p+s) = 1.
```

Every frozen pivot needs anchor mass 4, so every realized K23 child is terminal. Full K23 charge must therefore equal irreducible K23 charge. The audit checks this formula, the unique frozen parent edge, response tail count, sign flip, exact `U` divisor class, and reachability separately for all 59 IDs.

## Why K22 scalars are not inputs

K22 children have anchor mass 2 and are terminal. They cannot be prolonged at all, and the K23 DAG does not name them as parents. K23 instead fans K4 or K3 tails from the same K19/K20 parents that earlier K22 source folds reconstructed for different terminal tails. Actual K22 producers explicitly emitted scalar/count/sample JSON only and no K23 rows or scalar.

Accordingly, this schedule recomputes every K23 sink from its pinned source lineage. It reuses source-linear engine structure, never a K22 scalar. The earlier one-pass multiplex proposal is planning evidence only; it is not treated as evidence that multiplexing ran.

## Pinned authoritative inputs

| Artifact | Geometry | SHA-256 |
|---|---:|---|
| frozen R8/factor structure | 485 R8 records, 115,275 bytes | `55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b` |
| K2/K3 response auxiliary | 78 pivots, 14,364 bytes | `f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab` |
| K4 response table | 60 tails/pivot, 18,727 bytes | `4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3` |
| frozen 77-cycle table | 2,637 bytes | `8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7` |
| direct K15 canonical rows, available alternative | 5,311,211 records | `e79b752f94ad3b16ce4cf7d3f044e8887bda54bba5c6298ab31338bb121fa20f` |
| direct K16 canonical rows | 24,097,095 records | `93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3` |
| decorated hidden K16/pivot orbits | 101,545,723 × 53 bytes | `22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8` |
| collected hidden K18 parents | 158,439,965 × 80 bytes | `442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8` |

The audit rehashes all small inputs, validates every large file's byte geometry and magic, and reuses its upstream sealed full-file hash. Five completed source-engine references are also full-hash pinned; they are implementation starting points, not K23 results. The grouped K16 physical fold deliberately requires a new combined K23 producer over the pinned checkpoint rather than treating its still-evolving K22 producer sources as authoritative.

## Six bounded physical folds

The 17 scalar groups are scheduled as six scans with every response-sequence sink kept distinct:

| Physical fold | IDs | Exact planned intervals | Conservative initial maximum |
|---|---:|---|---:|
| collected hidden K18 | 1 | `[0,52813321)`, `[52813321,105626643)`, `[105626643,158439965)` | 345 s |
| decorated hidden K16/pivot pairs | 2 | `[0,33848574)`, `[33848574,67697148)`, `[67697148,101545723)` | 497 s |
| K14 R8 source | 3 | `[0,121)`, `[121,242)`, `[242,363)`, `[363,485)` | 300 s |
| grouped direct K15 R8 source | 12 | 8 balanced intervals over `[0,485)` | 451 s |
| grouped direct K16 checkpoint | 18 | 8 balanced intervals over `[0,24097095)` | 240 s |
| direct D17--D19 R8 sectors | 23 | `[0,161)`, `[161,323)`, `[323,485)` | 366 s |

This is 29 restartable atomic shards. The listed walls are conservative planning values from measured K22 source engines and the exact terminal-tail ratios `60/32` or `32/12`; they are not launch authority.

Each new K23 producer must pass its tiny, 4,096-or-equivalent, and named representative prefix. An interval launches only if the new measured conservative projection is at most 540 seconds. Otherwise it is bisected and re-gated. A watchdog discards a non-atomic attempt at 570 seconds; no shard may exceed 600 seconds, a single family cache may not exceed 8 GiB, aggregate live RSS may not exceed 16 GiB, and only one physical shard runs at a time. Merge requires exact gap-free source coverage, separate named sinks, integer accumulation before division by `U=400591699200`, atomic output, and no parent-row emission.

## Strict 59-ID assembler

`assemble_k23_59_exact.py` freezes all 17 group identities and the exact ordered IDs within each group. It additionally requires degree 23, the exact scale `U`, full/irreducible equality, agreement between scaled integers and reduced rationals, and an existing evidence file with a matching complete SHA-256.

Standard, optimized (`-O`), and isolated/no-site (`-I -S`) hostile selftests agree. They reject missing and duplicated groups, an unknown/extra group, regrouping, ID reordering, wrong `U`, full/irreducible disagreement, a rational mismatch, and evidence-hash mutation. The grouped scalar is counted once.

The availability-only manifest intentionally assembles to `REJECT_INCOMPLETE_K23_59_ID_GATE` with 0/59 covered, all 59 IDs missing, and zero placeholder total. `k23_expected_scalar_groups.json` names the future evidence fields but contains no charge values.

Replays:

```sh
python3 computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/audit_k23_availability.py
python3 computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/assemble_k23_59_exact.py --self-test
python3 computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/assemble_k23_59_exact.py --audit-incomplete \
  computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/k23_manifest_availability_only.json \
  computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/results_k23_0_of_59_gap.json
```

This package makes no K23 scalar, residual, membership, or conjecture claim.
