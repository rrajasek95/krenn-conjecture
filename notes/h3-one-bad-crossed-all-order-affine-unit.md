# The crossed repair-plus-gauge chart has an ordinary two-row unit

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_crossed_all_order_affine_unit.py`

## Outcome

The second-order separator from `52cf55d` is not merely quadratic.  On the
entire affine space through the crossed calibration spanned by all `36`
missing-row repair coordinates and all seven Jacobian-kernel directions, its
exact restriction through the full hafnian degree four is

\[
                              \lambda F=-1.             \tag{1}
\]

There are no linear, quadratic, cubic, or quartic terms.  Hence every local
repair order inside this `43`-parameter chart is closed by an ordinary
source unit.

## The factorization is only two rows

The cancellation has a simpler source form than the six-row separator.
On this affine chart the two physical cells

\[
                       A_{06}(1,1),\qquad A_{06}(2,2)   \tag{2}
\]

are the same affine linear form.  This equality includes all seven gauge
directions; none of the `36` repair variables touches either nonselected
endpoint row.

The pure word `11111111` and mixed word `21111121` each retain exactly one
physical matching,

```text
06 | 13 | 24 | 57.
```

Their physical coefficients are therefore the same polynomial

\[
 A_{06}(1,1)A_{13}(1,1)A_{24}(1,1)A_{57}(1,1)
 =A_{06}(2,2)A_{13}(1,1)A_{24}(1,1)A_{57}(1,1).       \tag{3}
\]

After substituting the `43` affine parameters, the common tail in (3) has
`125` terms, with degree histogram

```text
degree       0   1   2   3   4
terms        1   0  26  49  49.
```

The exact GHZ generators are

\[
 G_{11111111}=M-1,
 \qquad G_{21111121}=M.
\]

Consequently

\[
                 \boxed{1=G_{21111121}-G_{11111111}}. \tag{4}

Equation (4) is an ordinary polynomial identity: no localization, Hasse
truncation, quotient rank, finite-field calculation, or decomposability
argument remains.

## Relation to the six-row functional

Direct expansion of all six literal words in the primitive separator gives
an identically zero physical hafnian combination.  The only augmentation is
the pure-1 target in `11111111`, so the residual functional is exactly `-1`.
The checker reconstructs all matchings and all affine linear physical cells;
it does not infer cubic and quartic cancellation from the lower Hessian.

## Scope

This closes every polynomial order in the frozen `h=3` affine
repair-plus-gauge chart.  It does not say that a completion must stay in
that chart: nongauge nonrepair directions or reselection to another physical
shared pair remain logically separate.  The base calibration is still not
itself a GHZ source; (4) says no point of this entire local affine chart can
be one.

## Reproduction

```bash
python3 computations/verify_h3_one_bad_crossed_all_order_affine_unit.py
python3 -O computations/verify_h3_one_bad_crossed_all_order_affine_unit.py
```
