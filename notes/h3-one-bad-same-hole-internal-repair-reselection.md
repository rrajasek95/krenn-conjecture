# Internal same-hole repairs expose new active doubly-good pairs

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_same_hole_internal_repair_reselection.py`

## Outcome

The two crossed internal-`q` obligations isolated by `e326827` do not land
in the old endpoint-star crossed affine packet.  On the finite carrier-only
charts they expose genuinely different physical shared pairs: their four
deleted-star ranks are `(3,3,3,3)`, and both arm cofactors are active.

For the shared C/A repair

```text
q13:10*q24:10 != 0,
```

the pair with head `1` and arms `12,13` has direct cells `12:11,13:10`,
distinct outer target lines `c,a`, star ranks `(3,3,3,3)`, and respectively
`4,2` nonzero cofactor coefficients in the pinned calibration.

For the right middle A/T repair

```text
q13:02*q24:20 != 0,
```

the pair with head `1` and arms `13,14` has direct cells `13:02,14:00`,
distinct outer lines `t,a`, star ranks `(3,3,3,3)`, and `2,4` nonzero
cofactor coefficients.

These signatures differ from the already audited outer crossed affine
packet, whose selected deleted-star ranks are `(2,2,3,3)`.

## The left A/T repair

The alternative product

```text
q12:02*q34:20 != 0
```

puts two decorations on each of the old carrier edges `12,34`; consequently
there is no rank-one shared-pair reselection touching either repair edge at
this first stage.  But the complete `Qc` coefficient `10211` is exactly

```text
q12:02*q34:11 + q13:01*q24:21 = 0.
```

The first product is a unit, so the second product is forced to be a unit.
After adjoining that forced secondary matching, the pair with head `1` and
arms `13,14` has direct cells `13:01,14:00`, outer lines `c,a`, star ranks
`(3,3,3,3)`, and `2,4` nonzero cofactor coefficients.

Thus all three internal-repair choices reach the same structural outcome.
For an exact source, the uniform flat-bicase theorem makes a shared literal
rank-one pair with distinct outer target lines nonflat.  Hence an exact
completion of any of these finite carrier charts enters the existing curved
doubly-good overlap route.

This is **not** an active clean cap outright, and it is not a completed
contradiction.  The general theorem transporting an arbitrary active curved
doubly-good overlap to the minimum full-nine unit packet remains open.  The
present result supplies exactly that still-open route's rank, activity, and
nonflatness hypotheses on the finite carrier calibrations.

## Complete-row audit and scope

The checker expands every coefficient of the two diagonal and two crossed
common-`q` tensor rows.  Before invoking reselection their residual counts
are:

```text
chart                         Qc  Ra  ca  tt
shared C/A                    0   1   2   0
middle A/T left               2   0   2   0
middle A/T right              0   0   2   0
middle left + forced second   1   0   3   0
```

The reselection census is exhaustive among rank-one physical shared pairs
touching a repair edge in these literal calibrations: respectively
`7,0,11,7` candidates.

This is not a general-support theorem.  It keeps the endpoint-star/direct
normal form fixed and treats the finite carrier-only residue calibrations.
Arbitrary extra endpoint-star components and arbitrary additional residue
support could change the rank-one direct blocks and require a separate
minimum-support/reselection argument.  Within the requested finite charts,
however, no new crossed affine or higher carrier layer remains.
