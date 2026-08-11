# The three same-hole unit losses have a six-chart carrier cover

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_same_hole_unit_loss_carrier_cover.py`

## Exact finite cover

Keep the endpoint-star/direct normal form of the same-hole branch.  The
`tt` target fixes `q23:22=1` and all other decorations of `23` to zero.
The two genuine pure cofactor equations then have leading carrier sums

```text
Qc(all c): q12:11*q34:11 + q13:11*q24:11 = 1,
Ra(all a): q01:00*q34:00 + q03:00*q14:00
                                 + q04:00*q13:00 = 1.
```

At every residue point of the completed local ring, one summand of each
sum is a unit.  Thus the three unit-loss branches from `d231004` are covered
by exactly `2*3=6` carrier charts.  Write

```text
C1=12|34, C2=13|24,
A1=01|34, A2=03|14, A3=04|13.
```

The six charts form three exact site-relabel orbits:

```text
{(C2,A1),(C1,A3)}   Nakayama orbit,
{(C1,A1),(C2,A3)}   shared C/A carrier orbit,
{(C1,A2),(C2,A2)}   middle A/T carrier orbit.
```

The nonbase Nakayama chart `(C1,A3)` is the image of `(C2,A1)` under the
common-site permutation `1 <-> 4`; applying the permutation to the entire
source packet transports the proved Nakayama theorem exactly.

## What happens in the other two orbits

The pure equations themselves give a sharper dichotomy than a support
census.  On the representative shared chart `(C1,A1)`, the mixed `Qc` word
`11100` is exactly

```text
q12:11*q34:00 + q13:10*q24:10 = 0.                 (1)
```

The first product is a unit on this chart.  Hence either (1) is an ordinary
localized source unit, or the unique crossed internal-`q` repair matching
`q13:10*q24:10` is itself a unit.  The relabelled `(C2,A3)` chart has the
same conclusion.

On the middle orbit, `A2` and the fixed `tt` carrier produce the mixed `Qc`
word `10220`:

```text
q12:02*q34:20 + q13:02*q24:20
                  + q14:00*q23:22 = 0.             (2)
```

The last product is a unit.  Therefore at least one of the first two
crossed A/T repair products is a unit, unless (2) already gives an ordinary
source unit.

Consequently all five alternatives to the base `(C2,A1)` chart are now
source-faithfully classified: one is the same Nakayama chart after relabel,
and the other four force a crossed internal carrier repair or a unit.

## Scope guard

This does **not** yet close the four crossed-repair charts.  The repair cells
in (1)--(2) are internal common-`q` cells.  They are not the two outer
endpoint-star cells in the already audited crossed quadratic-mate chart, so
identifying them with that known branch would require a new source-valid
reselection theorem.  The exact remaining same-hole gate is therefore much
smaller: prove that one of these crossed internal carriers reselects to a
known crossed/good pair, or use the remaining full rows to turn it into an
ordinary unit.  Arbitrary extra endpoint-star components are outside this
cover, as requested.
