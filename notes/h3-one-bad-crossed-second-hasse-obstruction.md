# A six-row source separator kills every quadratic crossed rank repair

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_crossed_second_hasse_obstruction.py`

## Outcome

The first-order obstruction in `3c63ec6` persists through the complete
bounded quadratic Hasse module requested for the crossed chart.  Use the
`36` physical coordinates in the two missing selected-colour endpoint rows
and the exact seven-dimensional kernel of the full source Jacobian.  After
adjoining every square and cross Hasse monomial in these `43` directions,
the exact ranks are

```text
rank J                              245
rank (J + quadratic Hasse)          340
rank (J + quadratic Hasse | -F)     341.
```

Thus the ten-row crossed residual `F` remains outside the augmented
degree-two source image.

Concretely, for a second-order arc

\[
 A(\epsilon)=A_0+\epsilon u+\epsilon^2v,
\]

the degree-two source term is `Jv+Q(u)`.  An output-preserving first face has
`u in ker J`, while a rank repair may occur in the repair component of `v`.
The checker tests the larger Newton--Hasse equation

\[
                   F+Jv+Q(u)=0                       \tag{1}
\]

with `v` arbitrary and with `u` allowed to range over repair plus gauge.
Failure of this enlarged equation therefore also excludes the genuine-jet
subcase `u in ker J`.

## The complete bounded module

The deterministic rational echelon basis of `ker J` has free physical
cells

```text
17:11, 27:00, 34:00, 47:22, 56:00, 57:11, 67:10
```

and support sizes

```text
8, 8, 7, 4, 10, 4, 7.
```

The checker forms Hasse coefficients directly from physical perfect
matchings, without differentiating a declared response tensor.  Among the
`630` unordered pairs of distinct repair cells, `216` give nonzero columns.
After adding repair--gauge and gauge--gauge squares/crosses, there are `351`
nonzero quadratic columns with `873` entries.  Their output support remains
inside the same `639` literal word rows as the Jacobian.

Allowing the `351` columns independent coefficients is stronger than asking
for a decomposable quadratic jet.  Hence the rank jump already excludes all
genuine squares and cross terms in the chosen repair/gauge space.

## Primitive quadratic obstruction

The entire result has a six-row ordinary source witness:

```text
  00111110 - 00222112 - 11012112
 +11111111 + 21012122 - 21111121.
```

This covector pairs to zero with

1. all `252` physical Jacobian columns;
2. all `351` nonzero repair/gauge Hasse columns;

but pairs with the crossed residual `F` to `-1`.  Its coefficients are
primitive integers.  No quotient basis, floating rank, finite-field lift,
or decomposability assumption is needed for the certificate.

## Consequence and scope

Within the exact crossed calibration, neither a single-cell/linear repair
nor a quadratic repair built from the missing rows and gauge freedom can
restore the deficient `pq` star while closing the full source labels.  The
next possible local mechanism is cubic interaction, a direction outside the
repair-plus-gauge module, or reselection to another physical shared pair.

As in `3c63ec6`, the base calibration has ten mixed residuals and is not a
GHZ source.  This is a degree-two correction obstruction at that physical
packet, not the completed tangent complex of a hypothetical exact source.

## Reproduction

```bash
python3 computations/verify_h3_one_bad_crossed_second_hasse_obstruction.py
python3 -O computations/verify_h3_one_bad_crossed_second_hasse_obstruction.py
```
