# Orbit-zero `K16`: one attachment of the smallest replacement dual

## Verdict

The exported four-row class does not fill after one complete exact
attachment.  Its prior page had 327 source columns; the four support rows see
247 columns, only five old, so this step adjoins 242 new columns.  On the
resulting 569-column page,

```text
rank_Q(M) = 436,
rank_Q([M | q]) = 437.
```

An exact replacement dual remains, with support 23 and coefficients only
`+1/-1`.  The class therefore **stays sparse on this page**.

## Literal attachment

The input is the smallest certificate from the fourteen-type first-page
ledger:

```text
+ q
- r0
- r1
- r2.
```

The checker replays the six-row predecessor page, then enumerates every
degree-24 mixed source column incident to any of these four rows.  Every output
of `K`-degree at most 16 is retained.  The exact census is

| quantity | value |
|---|---:|
| old columns | 327 |
| four-row incident columns | 247 |
| overlap | 5 |
| newly adjoined columns | 242 |
| union columns | 569 |
| complete `K<=16` rows | 19,495 |
| matrix nonzeros | 24,843 |
| target remainder support | 11 |

The column minimum-degree histogram is

```text
K10:2, K11:2, K12:40, K13:31, K14:210, K15:103, K16:181.
```

No row, column, or incidence from a subsequent attachment is used.

## Next dual

Exact sparse back-substitution produces a 23-row functional that annihilates
all 569 columns and pairs `q` to one.  Its profiles are

```text
degree:       K10:2, K11:1, K12:9, K13:3, K14:5, K16:3
coefficient:  -1:16, +1:7.
```

All rows and coefficients are frozen in
`results_k16_smallest_dual_next_page.json`; their support digest is

```text
a5f93c06b5c4dc82ddbb1df7a4fd73dbb7a86cd772690d44bf0f0dd28a815121.
```

## H-canonical referee

The literal rank calculation is not replaced by an anchor-signature quotient.
Independently, every column is canonicalized under the exact order-384 factor
stabilizer.  The old 327, support-page 247, new 242, and union 569 columns all
remain pairwise distinct in their respective H-canonical ledgers.  Thus this
page gets no local symmetry compression.

The certificate remains small, but it now spans `K10` through `K16`, while the
page already has 19,495 rows and 569 distinct H-types.  This is a warning that
the *next* attachment enters the broad global frontier; it is not evidence
from a second-page enumeration.

## Scope

This is exact only for the union of the prior restricted page and the complete
first attachment of the four-row replacement support.  It is not full
component membership or nonmembership.  No columns incident to the new
23-row dual, no 701-million-row residual, localization, or another chart are
tested.

## Replay

```sh
python3 audit_k16_smallest_dual_next_page.py
python3 -O audit_k16_smallest_dual_next_page.py
python3 -I -S audit_k16_smallest_dual_next_page.py
python3 audit_k16_smallest_dual_next_page.py --mutate  # must fail
```

Logical digest:

```text
c2dcada21b5904500e2d979bb4759cefbf6bdf449f81bef87ffb71b9827e7199
```
