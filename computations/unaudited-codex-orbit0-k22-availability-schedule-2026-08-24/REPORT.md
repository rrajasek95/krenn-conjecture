# Exact K22 76-lineage availability and bounded charge schedule

## Verdict

**PASS as an availability/schedule theorem; no K22 charge has been run.**  The
frozen recurrence DAG has exactly 76 reachable K22 lineage IDs, and the strict
ledger partitions them without a duplicate, omission, or extra:

| availability at the final response | IDs | present consequence |
|---|---:|---|
| terminal-ready K18 profile interface | 16 | evaluate one K4 tail family per stored selected-pivot profile |
| retained literal immediate K18 parent checkpoint | 1 | stream the checkpoint directly through K4 |
| source replay required | 59 | reconstruct the literal K19 or K20 parent occurrencewise and scalar-fold its final response |
| genuinely missing provenance | 0 | every replay has a pinned literal checkpoint or frozen R8/factor source |

The 59 replay IDs do **not** have retained immediate K19/K20 parent rows.  That
is a compute gap, not a provenance gap.  Earlier K19/K20 charge scalars,
terminal-only profiles, caches, and sample ledgers cannot be prolonged.

The result ledger has logical SHA-256
`347e67b90584f48577a5613011dbc3342dd8f87fd34a469d2df5af2be4893d19`.
It is derived from frozen recurrence-DAG logical SHA-256
`ad59639716fe2a2cc04fca83a189d74ff8c1f5bbe6d7257676dd458f4c768a66`
(file SHA-256
`469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa`).

## Exact 76-ID shape and terminality

The final response split is exact:

| final parent | response | K22 IDs |
|---|---:|---:|
| K18 | K4 | 17 |
| K19 | K3 | 24 |
| K20 | K2 | 35 |

There is no 77th lineage.  The frozen node `D20:444|R:2` is unreachable with
zero reachable anchor signatures: direct `D20:444|R:direct` is already
irreducible and has no outgoing pivot.

Terminality is universal, rather than sample-based.  If the final parent has
degree `p=22-s` and the response has degree `s`, its anchor sum changes by

```text
(24-p) - 4 + (4-s) = 24-(p+s) = 2.
```

A K0 pivot needs four anchor incidences, so anchor sum `2<4` excludes every
further pivot for every realized K22 row.  Thus full K22 charge must equal
irreducible K22 charge.  The same argument gives anchor sums 3, 2, 1, 0 in
degrees K21--K24, proving all realized children in that degree range terminal.
The audit checks the parent degree, response shift, reachability, sign, and
anchor-sum calculation separately on all 76 frozen DAG edges.

## Terminal-ready interfaces: 16 IDs

All four interfaces retain `(cycle profile, anchor signature, selected pivot,
exact signed weight, witness)` at K18.  Since the K4 child is universally
terminal and the 77-cycle charge is determined by this interface plus the
tail, no K22 row collection is required.

| group | IDs | profile records | exact K4 tail evaluations | input pin |
|---|---:|---:|---:|---|
| direct D18 R4 | 6 | 979,091 | 58,745,460 | `direct_k18_enriched_profiles.bin`, 70,494,808 bytes, SHA `d77f2a84...` |
| D14 R4-4 | 1 | 18,217,226 | 1,093,033,560 | `k14_k4_enriched_profiles.bin`, 1,894,591,760 bytes, SHA `5cc8c15b...` |
| grouped D15 R3-4 | 3 | 25,564,391 | 1,533,863,460 | `checkpoint_k15_k3_profiles_merged.bin`, 2,658,696,792 bytes, SHA `8b05f3fb...` |
| grouped D16 R2-4 | 6 | 6,876,260 | 412,575,600 | `checkpoint_k16_k2_profiles_merged.bin`, 715,131,168 bytes, SHA `d2327118...` |
| **total** | **16** | **51,636,968** | **3,098,218,080** | |

Prior K2 evaluator walls, scaled only by the exact tail ratio `60/12`, suggest
roughly 19, 47, 70, and 18 seconds respectively.  Those are planning
projections, not gates; each interface still starts with a 65,536-record
measured prefix.

## Retained literal immediate parent: 1 ID

`D14:222|R:2-2-4` has the exact collected parent checkpoint
`checkpoint_k18_22_pivotable.bin`: 158,439,965 80-byte `H18PIV2` records,
12,675,197,280 bytes, SHA-256
`442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8`.
The already-refereed pivot census has 399,275,484 selected K18 pivots, so the
K4 terminal pass has exactly 23,956,529,040 representative tails.  The landed
K3 consumer took 108.08 seconds; tail-linear scaling gives about 203 seconds
for K4 before cache effects.  A 1,000,000-record measured prefix remains the
launch authority.

The same checkpoint can be scanned once for the source-replay lineage
`D14:222|R:2-2-2-2`: fan K4 directly to the first sink, and fan K2 to K20,
enumerate every K20 pivot, divide exactly again, and send its K2 tails to a
second sink.  The previous K20 pass saw 4,791,305,808 K20 children, of which
570,281,318 were pivotable; the number of selected K20 pivots is deliberately
left unknown until the bounded prefix.

## Source-replay groups: 59 IDs

The machine ledger lists 17 recurrence groups.  They are scheduled as six
physical source folds so common parent work is not repeated:

| physical fold | K22 source-replay IDs | exact input | response sinks in the pass |
|---|---:|---|---|
| collected hidden K18 | 1 (plus the literal-ready ID above) | `H18PIV2`, 158,439,965 records | R2-2-4 and R2-2-2-2 |
| decorated hidden K16/pivot pairs | 2 | `hidden_k16_decorated_pair_orbits_full.bin`, 101,545,723 53-byte records, 5,381,923,399 bytes, SHA `22f91fc8...` | R2-3-3 and R2-4-2 |
| K14 factor source | 3 | `filtered_k16_structure.bin`, 485 R8 records, SHA `55e38231...` | R3-2-3, R3-3-2, R4-2-2 |
| grouped direct K15 | 12 | `checkpoint_direct_k15.bin`, 5,311,211 rows, SHA `e79b752f...` | R4-3, R2-2-3, R2-3-2, R3-2-2, each over three packet IDs |
| grouped direct K16 | 18 | `checkpoint_direct_k16.bin`, 24,097,095 rows, SHA `93c1b21e...` | R3-3, R4-2, R2-2-2, each over six packet IDs |
| direct D17--D19 factor sectors | 23 | `filtered_k16_structure.bin`, same 485 R8 records | D17 R2-3/R3-2, D18 R2-2, D19 R3 |

The four K19-terminal groups whose inputs share a direct source are evaluated
inside their corresponding physical fold; the table is not permission to mix
their scalars.  Every recurrence-sequence sink remains separately named.

Six of the seven K19-parent recurrence groups already have an exact selected
terminal-pivot census from landed K21 source passes.  Substituting K3 for the
old terminal K2 gives the following exact K22 work counts:

| recurrence group | IDs | selected K19 pivots | exact K3 terminal tails |
|---|---:|---:|---:|
| direct D19 R3 | 3 | 111,744,000 | 3,575,808,000 |
| grouped D15 R4-3 | 3 | 1,549,305,840 | 49,577,786,880 |
| grouped D16 R3-3 | 6 | 2,041,782,688 | 65,337,046,016 |
| direct D17 R2-3 | 7 | 1,448,947,200 | 46,366,310,400 |
| hidden D14 R2-3-3 | 1 | 1,774,721,368 | 56,791,083,776 |
| D14 R3-2-3 | 1 | 5,075,412,480 | 162,413,199,360 |
| **known subtotal** | **21** | | **384,061,234,432** |

The grouped three-ID D15 R2-2-3 census and every final-pivot census for the 35
K20-parent IDs remain prefix-measured quantities.  The audit does not invent
them from `full-irreducible`: that difference counts pivotable K20 children,
not the number of selected pivots.

## Exact source-faithful scalar kernel

All replay families implement one interface:

```text
fold(row, signed_scaled_weight, response_prefix, requested_sinks):
    pivots = every literal dividing K0 pivot of row
    m = len(pivots)
    assert signed_scaled_weight % m == 0
    for pivot in pivots:
        for tail in requested K2/K3/K4 tails:
            child_weight = -signed_scaled_weight / m
            either recurse literally, or (only at a final sink) add
            child_weight * charge77(child) to that degree's accumulator
```

Occurrencewise scalar folding is exact: pivot count, child pivotability, and
77-charge are functions of the literal row and are H-invariant.  Identical
canonical rows therefore have the same divisor, so signed collection commutes
with the linear response operator.  Profiles may replace literal rows only at
the final response.  Every shard retains exact counts by realized divisor
tuple, source interval, recurrence sink, and sign, plus 257 deterministic
distributed nonzero literal continuations for independent replay.

No K19, K20, or K22 rows are written.  Output is an atomic scalar/count/sample
JSON fragment only.

## Bounded gate and staged launch order

No production pass was launched in this audit.  Each family must pass:

1. A self-test/tiny source case with literal pivot enumeration, sign, exact-U
   division, terminality, and 77-charge assertions.
2. A 4,096-source-unit prefix (8 R8 records for factor engines).
3. A representative prefix of at least 1% or the named historical gate:
   1,000,000 hidden records, 131,072 K15 rows, 800,000 K16 rows, or 32 R8
   records.
4. Projection per restartable shard of at most 600 seconds and aggregate live
   RSS at most 16 GiB.  A single chunk cache hard-aborts before 8 GiB.
5. Full interval coverage with no gap/overlap, exact integer merge before one
   final division by `U=400591699200`, 257 distributed nonzero samples per
   scalar group where realized, and independent source/formula/count replay.

Run order is: four terminal profiles; hidden collected K18; decorated hidden
pairs; direct D19/D17/D18 sectors; K15; K16; K14.  This lands small/refereeable
groups first and forces measured gates before the deep K20 continuations.
Historical tail-linear projections place D15 R4-3 near 179 seconds per former
shard, D16 R3-3 near 538 seconds, D17 R2-3 near 388 seconds, hidden R2-3-3 near
594 seconds, and D14 R3-2-3 near 443 seconds.  D15 R2-2-3 projects above 600
seconds without sharding and is therefore shard-only.  These projections do
not cover the new K20 continuations; their prefixes decide shard width.

## One-pass K22/K23/K24 multiplex

Once a literal preterminal parent and its pivot are reconstructed, rescanning
the source for later filtered degrees is unnecessary:

```text
literal K19 parent + pivot -> K2/K3/K4 tails -> K21/K22/K23 sinks
literal K20 parent + pivot -> K2/K3/K4 tails -> K22/K23/K24 sinks
```

K21 and higher children are terminal by the anchor-sum proof.  Multiplexing is
provenance-preserving because only the terminal tail loops are fanned out; the
parent row, pivot set, divisor, coefficient, and source interval are shared.
Every degree nevertheless has a separate accumulator, fragment, manifest,
and strict frozen-DAG ID ledger.  A grouped K22 scalar is never reused as a
K23/K24 scalar.

## Strict 76-ID assembly integration

`assemble_k22_76_exact.py` requires:

- exact equality with all 76 frozen IDs, with grouped scalars counted once;
- `degree=22` and `U=400591699200`;
- both scaled integers and reduced rationals, checked against one another;
- full equals irreducible for every group;
- an existing evidence file whose complete SHA-256 matches the manifest;
- no missing, duplicate, or extra lineage.

Its hostile self-test rejects deletion, duplication, an extra ID, wrong U,
full/irreducible disagreement, and an evidence-hash mutation.  The current
availability-only manifest intentionally assembles to
`REJECT_INCOMPLETE_K22_76_ID_GATE` with 0/76 covered and all 76 IDs listed as
missing.  `k22_expected_scalar_groups.json` freezes the expected 22 scalar
groups and future manifest fields but contains no fabricated values.

Replay:

```sh
python3 computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/audit_k22_availability.py
python3 computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/assemble_k22_76_exact.py --self-test
python3 computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/assemble_k22_76_exact.py --audit-incomplete \
  computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/k22_manifest_availability_only.json \
  computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/results_k22_0_of_76_gap.json
```

This package proves availability, exact terminality, and a bounded execution
contract.  It makes no K22 scalar, residual, membership, or conjecture claim.
