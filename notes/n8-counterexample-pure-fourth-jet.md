# Both missing pure coefficients have fifth-order contact

## Exact colour-one result

At the rational point (p) on the five-parameter (n=8) mixed torus,
the earlier calculations proved

\[
 H_0(x(t)),H_1(x(t))\in t^4\mathbf Q[[t]]
\]

for every formal arc in the mixed fibre.  The colour-zero quartic
factorization upgrades (H_0) to (O(t^5)).  The exact weighted Hasse-jet
calculation here proves the matching statement

\[
 \boxed{H_1(x(t))\in t^5\mathbf Q[[t]].}
\]

Thus both missing pure coefficients have fifth-order contact with the full
mixed fibre along the exceptional torus.

## Cubic normal form

Put (F_1=H_1-H_{11000111}).  The nine quadratic conormal products remove
the degree-two part.  Exact triangular division of the resulting
1,084-term cubic by the mixed Jacobian uses 68 conormals and 1,535
quadratic multiplier terms.  Its four-term tangent remainder is

\[
 -z_{3511}\mathcal O,
 \qquad
 \mathcal O=2(z_{0410}-z_{0411})(z_{1311}-z_{3711}),
\tag{1}
\]

where \(\mathcal O\) is one component of the rank-39 quadratic second-lift
obstruction.  This recovers the third-jet theorem from a full-equation
normal-form calculation.

## The true fourth arc coefficient

Write a second-order jet as

\[
 y(t)=tv+t^2(w_{\mathrm{can}}(v)+s)+O(t^3),
\]

where (w_{\mathrm{can}}) is the exact echelon right-inverse solution and
(s\in\ker J_{\mathrm{mix}}) is the arbitrary tangent part of the second
coefficient.  The canonical solution has zero free tangent coordinates.

After lifting the cubic conormal division to full mixed equations, the
ambient quartic residual has 22,026 terms but only 24 terms on the tangent
space.  Because the corrected residual still has the cubic term (1), its
actual coefficient of (t^4) is

\[
 P_4(v,s)=R_4(v)+D(-z_{3511}\mathcal O)_v(s).
\tag{2}
\]

This weighted-degree-four polynomial has 36 terms.  The third arc
coefficient (u) does not occur: the corrected residual has no terms below
degree three, and inserting (t^3u) into a cubic first contributes in
degree five.

## A literal third-lift equation

The obstruction (1) is not an abstract cokernel coordinate.  It is the
quadratic tangent part of the literal difference of mixed equations

\[
 G=H_{11001001}-H_{11000001}.
\tag{3}
\]

The two summands have identical gradients at (p), so (G) starts in
degree two.  Its coefficient at order three on the jet above is a 34-term
weighted polynomial (K_3(v,s)).  Every third-order lift in the mixed
fibre satisfies

\[
 \mathcal O(v)=0,\qquad K_3(v,s)=0.
\tag{4}
\]

## The quartic ideal identity

The checker reconstructs all 39 quadratic obstruction polynomials over
ℚ and performs exact sparse weighted reduction.  It obtains

\[
 \boxed{P_4+z_{3511}K_3\in(\mathcal O_1,\ldots,\mathcal O_{39}).}
\tag{5}
\]

The reduction takes 19 steps and has zero remainder; replaying the recorded
quadratic multipliers reconstructs the left side exactly.  Equations
(4)--(5) force (P_4=0) for every genuine third-order mixed jet, proving
the displayed (O(t^5)) theorem.  Since all corrections use full mixed
hafnian equations, the corrected residual equals (H_1) along the arc.

## Structural meaning

The two pure coordinates now exhibit a common recursive pattern:

1. their first jets are mixed conormals;
2. their quadratic defects factor through mixed conormals;
3. their cubic defects are conormal or second-lift-obstruction multiples;
4. their quartic defects are second- or third-lift-obstruction multiples.

This makes an all-orders osculation induction plausible: at each order,
the next pure coefficient appears to be controlled by the obstruction to
lifting the same mixed jet one order further.  The computation is not yet
an all-orders proof.  Such a proof needs a coordinate-free recursive
identity, or equivalently a formal-local membership theorem for (H_0)
and (H_1), rather than a separate finite reduction at every order.

## Reproduction

```sh
python3 computations/verify_n8_counterexample_pure_fourth_jet.py
python3 -O computations/verify_n8_counterexample_pure_fourth_jet.py
python3 -I computations/verify_n8_counterexample_pure_fourth_jet.py
python3 -S computations/verify_n8_counterexample_pure_fourth_jet.py
```

The frozen ledger records all Jacobian and obstruction ranks, cubic
normal-form sizes, the 36-term true fourth output, the literal lift
equation and its 34-term obstruction, and the exact zero-remainder ideal
identity (5).
