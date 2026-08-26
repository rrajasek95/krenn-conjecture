# Complete K14 composition DAG through K20

This report supersedes the incomplete logical result `ea7964f7...`.  No K18
prefix or K20 run was launched after the scope guard.

Every ordered composition of shifts in `{2,3,4}` is:

| degree | ordered paths from K14 |
|---|---|
| K14 | `()` |
| K15 | none |
| K16 | `(2)` |
| K17 | `(3)` |
| K18 | `(2,2)`, `(4)` |
| K19 | `(2,3)`, `(3,2)` |
| K20 | `(2,2,2)`, `(2,4)`, `(3,3)`, `(4,2)` |

The starting K14 coefficient is negative; every pivot flips sign.  Hence
length-one paths are positive, length-two paths negative, and `(2,2,2)` is
positive.  The first pivot always uses the frozen K14 valid-pivot average;
later pivots use all available heads.

## Provenance status

- `(2)`: 75,691,040 pivotable K16 occurrences were discarded and not
  serialized.  Only 3,740,320 irreducible occurrences fed the frozen normal.
- `(3)`: 197,414,400 pivotable K17 occurrences were discarded by the K17
  normal, but the later K19 profile census reconstructed their response keys.
- `(4)`: 357,580,800 pivotable K18 occurrences are known, but the K18 pass
  retained only scalar charges/counts.
- `(2,2)` and `(2,3)` are absent because their `(2)` parents are missing.
- `(3,2)` has an exact profile/weight charge interface.
- `(3,3)` is recoverable from that interface by changing tail degree 2 to 3;
  it has 815,482,880 outgoing pivot uses and 26,095,452,160 source-linear K3
  tail operations.
- `(4,2)` lacks the outgoing K18 parent profiles.
- `(2,4)` and `(2,2,2)` are missing.  The triple path additionally needs the
  pivotable `(2,2)` K18 children.

The independent pivot-depth arithmetic DP resolves the provisional scale
concern: the `(2,2,2)` path has 142 possible denominator products, maximum
2,240, and exact LCM `U=400591699200`.  Thus U remains sufficient through
depth three, with occurrencewise remainder assertions.  This arithmetic fact
does not repair the missing source lineage.

The smallest next computation is not the four-lineage K18 prefix.  First
replay the discarded `(2)` K16 occurrences, census their K2/K3/K4 outgoing
pivots, serialize `(2,2)` parent profiles, and audit triple denominator
products.  This is a composition/provenance audit only, not a K20 result.

Logical digest:
`8d2277b51975bb14186bb9b12bd9f4625a850c78e93274886bff9aab15dddefa`.
