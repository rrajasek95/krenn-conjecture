# Crossed one-bad physical-pair reselection census

Date: 2026-08-11

Checker:
`computations/verify_h3_one_bad_crossed_pair_reselection_census.py`

## Result

Physical pair reselection is **not** the missing structural condition in the
crossed affine chart.  The frozen crossed calibration has 40 literal
shared-arm candidates with distinct outer coordinate lines.  Every candidate
is support-active and nonflat, and 10 have all four deleted-star ranks equal
to three.  Thus the calibration already contains 10 candidates satisfying the
rank/activity/curvature side of the curved doubly-good OO gate.

Over the complete polynomial affine chart with 36 repair parameters and seven
Jacobian-kernel parameters, 11 physical blocks remain literal coordinate
matrix units.  They give exactly 20 shared-arm candidates with distinct outer
lines.  Exact minors over
`Q[z_0,...,z_42]` show that **all 20** generically have deleted-star profile
`(3,3,3,3)`.  Exact residual hafnian coefficients certify both arm cofactors
nonzero, and an explicit rank-one-arm transition minor certifies nonflatness
for every candidate.

This does not produce an exact GHZ source.  The all-order identity from
`bc50cb1` is replayed on the same chart:

```text
1 = F_21111121 - F_11111111.
```

Both rows have the sole physical matching `06|13|24|57`, and the two relevant
forms `x06_11` and `x06_22` agree on all 43 affine directions.  Therefore the
entire source chart is empty, including every proper specialization locus.
The exact number of source-valid reselections in this chart is consequently
zero.  The earlier `(2,2,3,3)` obstruction for the originally selected
`(56,57)` arms is real but is not exhaustive under physical reselection.

## Finite censuses

At the frozen calibration there are 16 literal coordinate-unit blocks and 40
shared distinct-outer-line pairs.  Their deleted-star profile histogram is:

| profile | count |
|---|---:|
| `(2,2,2,2)` | 7 |
| `(2,2,3,2)` | 1 |
| `(2,2,3,3)` | 12 |
| `(2,3,2,2)` | 2 |
| `(3,2,2,2)` | 1 |
| `(3,3,2,2)` | 6 |
| `(3,3,3,2)` | 1 |
| `(3,3,3,3)` | 10 |

The 11 literal blocks persistent over the full affine parameter ring are:

```text
x01_00  x02_10  x12_10  x13_11  x17_11  x23_22
x24_11  x27_00  x34_00  x47_22  x56_00.
```

They yield 20 candidates, recorded individually in the checker ledger.  All
20 have generic profile `(3,3,3,3)`, nonzero arm cofactors, and a nonzero
transition minor.  At the frozen parameter value four of these persistent
candidates are already four-good:

```text
(center,q,r) = (1,2,7), (2,0,7), (2,1,7), (7,1,2).
```

The other six frozen four-good candidates use coordinate-unit blocks which
acquire additional entries along the affine family.

## Minimal escape from the certified unit

There are two minimal ways to evade this *specific* two-row identity; neither
is asserted to solve the remaining source equations.

1. A support-preserving transverse direction may separate the already-present
   forms `x06_11` and `x06_22`.  Every one of the 43 repair/gauge directions
   changes them equally, so this direction is genuinely outside the audited
   affine chart.
2. Among all one-cell support insertions, `x03_11` is the unique cell that
   completes a matching in exactly one of the two unit rows.  The only other
   one-cell near-matching cell, `x35_11`, adds the same matching to both rows
   and leaves the unit unchanged.

Thus the smallest literal outside-support change capable of defeating the
present certificate is `x03_11`; the smallest support-preserving change is one
nonrepair, nongauge coefficient split on edge `06`.  These are escape guards,
not candidate solutions.

## Scope

The census is complete for literal coordinate-unit shared-arm reselections at
the frozen calibration and for literal blocks persisting on the complete
43-parameter affine chart.  It does not classify coordinate-unit blocks that
appear only on arbitrary proper specialization loci.  That omission cannot
hide a source point inside this chart because the ordinary unit is valid on
the entire affine coordinate ring.

The conclusion for the proof spine is sharp: do not spend more effort trying
to manufacture rank/activity/curvature inside this crossed chart.  Any live
continuation must leave the chart by a transverse coefficient split or a new
support cell, after which the OO reselection theorem can be applied afresh.
