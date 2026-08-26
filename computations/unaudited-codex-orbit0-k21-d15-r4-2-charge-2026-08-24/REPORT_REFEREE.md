# Independent referee: grouped D15 `R:4-2` K21 charge

## Verdict

`PASS_INDEPENDENT_GROUPED_D15_R4_2_K21_REFEREE` for exactly

```text
D15:{223,232,322}|R:4-2.
```

The independently reduced scalar is

```text
-105580126744994119680 / 400591699200
  = -2333827745792/8855.
```

Full and irreducible counts and charges agree.  This referee did not rerun the
full fold and did not inspect or infer another K21 path.

## Frozen checkpoint

The referee streamed the entire retained source checkpoint independently:

- magic `K15CHK1\0`;
- byte length `169,958,768 = 16 + 32 * 5,311,211`;
- SHA-256
  `e79b752f94ad3b16ce4cf7d3f044e8887bda54bba5c6298ab31338bb121fa20f`;
- 5,311,211 strictly increasing canonical literal rows;
- every coefficient nonzero;
- signed coefficient sum `322,486,272`;
- coefficient L1 sum `3,083,240,448`.

Each record is exactly a 24-byte canonical row and an `i64` collected
coefficient.  The producer stores no packet label, so the grouped result is
source-faithful and `individual_id_charges=null` is mandatory.

## Eleven-interval assembly

The 11 atomic intervals are exactly

```text
[0,524288), [524288,1048576), ...,
[4718592,5242880), [5242880,5311211).
```

Their endpoints join without a gap or overlap, and their record counts sum to
5,311,211.  The referee independently rehashed every shard and matched the
hash table in the assembled result.

Exact summed counts are:

| quantity | value |
|---|---:|
| first pivot uses | 44,342,881 |
| K4 candidates | 2,660,572,860 |
| pivotable K19 children | 972,495,600 |
| second pivot uses | 1,549,305,840 |
| terminal K2/K21 occurrences | 18,591,670,080 |

The first-denominator histogram has 5,311,211 entries and its weighted sum is
44,342,881.  The second-denominator histogram has 972,495,600 entries and its
weighted sum is 1,549,305,840.  The product-denominator histogram also has
972,495,600 entries, and every denominator divides `U=400591699200`.

Each shard independently satisfies

```text
K4 candidates = 60 * p1 uses
K21 occurrences = 12 * p2 uses
full = irreducible
cache hits + misses = p2 uses.
```

## Sign, terminality, and strict scope

The pinned fold source uses

```text
w19 = -w15*U/m1
w21 = -w19/m2 = +w15*U/(m1*m2),
```

with an exact `U mod (m1*m2) = 0` assertion.  It contains exactly the three
requested lineage literals and a null individual-charge field.

Terminality is both structural and sampled literally.  Every K0 pivot has
anchor sum 4, while every realized K21 signature has anchor sum 3, so no K21
child is pivotable.

## Independent 257-parent literal replay

The sample referee source was recompiled with the two include-main features
disabled and rerun.  The 257 parent indices are
`floor(j*(5311211-1)/256)`, `j=0,...,256`; the first and last are 0 and
5,311,210.

The Python referee then sought every sample directly in the frozen checkpoint,
matched its literal row and coefficient, recomputed its K15 anchor signature
and first-pivot set, and checked the TSV arithmetic.  The Rust literal replay
independently produced:

| quantity | value |
|---|---:|
| p1 uses | 2,137 |
| K4 candidates | 128,220 |
| pivotable K19 children | 47,280 |
| p2 uses | 74,160 |
| literal K21 children | 889,920 |
| sampled U-scaled charge | 9,921,235,611,893,760 |

All 889,920 sampled children were asserted nonpivotable, and every literal
cycle key equaled its abstract terminal-profile key.

## Replay

```sh
python3 computations/unaudited-codex-orbit0-k21-d15-r4-2-charge-2026-08-24/audit_k21_d15_r4_2_independent_referee.py
```

The referee logical SHA-256 is
`ee260bce8fe7912780b931117b96520f5e4547dc2a8bc6593281fb008efb2bed`.
