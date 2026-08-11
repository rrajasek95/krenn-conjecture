# One source order globalizes every pair/triple killer

Date: 2026-08-11

Checker:
`computations/verify_n8_one_bad_axis_pure_global_killer_weight_order.py`

## Exact common-order result

Expand the unary top tensor and all four response tensors with all `90`
off-diagonal residual q cells present simultaneously.  Reinsert the complete
pair and primitive-triple elimination ledgers:

```text
44 pair-killer occurrences,
174 triple-killer occurrences.
```

The `218` occurrences collapse to `54` literal original source rows and `54`
distinct selected carrier cells, bijectively.  There is one positive integer
source valuation for which every selected unit-times-carrier term has
strictly smaller weight than every other term in its full literal row.

The carrier weights are `1`, except for

```text
weight 3:
  01:10, 02:10, 04:12;

weight 2:
  01:12, 03:10, 03:21, 04:10, 04:20, 05:20,
  12:21,
  14:01, 14:02, 14:20,
  15:01, 15:02, 15:20,
  24:01, 24:02, 24:10,
  25:01, 25:02, 25:10,
  34:10, 35:10,
  45:12, 45:21.
```

The chart units

```text
A,B,C,D,p0,p2,s1,s2,z03,z12,z45
```

have coefficient weight zero.  Every nonlocalized pure coefficient and
`p5` has weight one.  Thus the calculation does not silently discard the
`p5` contaminant or treat arbitrary pure coefficients as units.

Across the full source expansions there are `465` literal comparisons,
with `106` distinct inequality normals.  The displayed integral valuation
has exact minimum margin `1`; no floating-point feasibility claim remains.

## Initial-ideal consequence

Use the convention that lowest positive source weight is initial.  Each of
the `54` rows has initial term

```text
unit * one mixed carrier.
```

The carrier variables are distinct, so these initials are pairwise
coprime.  The product criterion therefore makes the selected rows a local
standard basis over the localized pure-chart coefficient ring.  In
particular the filtered initial ideal contains all `54` selected carrier
variables at once.  This is stronger than running the pair and triple
specializations independently: every possible mixed-cell contaminant was
already present when the common order was checked.

Exactly `36` carrier rays remain.  In the 13-dimensional quotient-character
coordinates of `9913c00`, the integral cocharacter

```text
(0,0,0,0,0,0,0,-1,-1,0,-1,-1,0)
```

pairs to `1` with `32` of them and to `2` with the other `4`.  Hence those
surviving rays lie in one strict open halfspace and support no positive
integer circuit of any degree.

Consequently no degree-four-or-higher Hilbert-basis enumeration is needed
for this localized associated-graded carrier-normalization step: a higher
circuit either uses one of the `54` initial variables or would have to be a
positive relation among the strictly separated `36`, which is impossible.

## Scope

This is a source-labelled, coefficient-exact statement using literal rows
from the five tensors.  It is a local/associated-graded theorem after
localizing the pure-chart units.  It does not claim an affine global ideal
equality away from that chart, nor does it replace any separate argument
needed to land an arbitrary source in this localized filtered setting.
