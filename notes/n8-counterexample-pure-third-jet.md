# The missing pure coefficients have quartic contact

## Exact outcome

Let (p) be the rational (a=b=c=d=e=1) point on the five-parameter
mixed-ideal torus.  The previous exact calculation proved that the two
missing pure coefficients have cubic contact with the full mixed fibre:

\[
  H_0(x(t)),H_1(x(t))\in t^3\mathbf Q[[t]].
\]

The third-jet calculation strengthens this by one full order:

\[
  \boxed{H_0(x(t)),H_1(x(t))\in t^4\mathbf Q[[t]]}
\]

for every formal mixed-fibre arc (x(t)) through (p).  This is an exact
rational statement in all 252 endpoint-colour variables.

## Genuine lift constraints

Write an arc through order three as

\[
  x(t)=p+t v+t^2 w+t^3 u+O(t^4).
\]

If (J) is the full mixed Jacobian and (q(v)) is the vector of second
Hasse coefficients, the first two mixed equations are

\[
  Jv=0,\qquad Jw+q(v)=0.
\]

The checker constructs the exact signed basis
(v_1,\ldots,v_{56}) of \(\ker J\), then constructs an exact column-echelon
quotient by \(\operatorname{im}J\).  The resulting second fundamental form

\[
  \operatorname{Sym}^2(\ker J)\longrightarrow
  \operatorname{coker}J
\]

has rank exactly (39) over \(\mathbf Q\).  All 56 diagonal basis monomials
lift to second order.  Among the \(\binom{56}{2}=1540\) cross monomials,
59 have nonzero obstruction.  Thus the calculation explicitly distinguishes
arbitrary tangent vectors from genuine second-order jets.

## The cubic factorization

Choose the exact echelon right inverse of (J).  It assigns to each
quadratic tangent monomial a canonical coefficient (w), modulo the
second-order obstruction.  Substituting this (w) into the corrected cubic
pure outputs gives two cubic polynomials in the 56 tangent parameters.

For the mixed word

```text
11001001
```

one scalar component of the exact second-order obstruction is

\[
  \mathcal O
  =2(z_{0410}-z_{0411})(z_{1311}-z_{3711}).
\]

Direct expansion of all 105 matching terms in the two pure coefficients and
their selected mixed conormal partners gives

\[
  \boxed{C_0=0,\qquad C_1=-z_{3511}\,\mathcal O.}
\]

This is a rational polynomial identity, not a finite-field rank observation.
If (v) admits a second-order lift, then its complete cokernel obstruction
vanishes, hence \(\mathcal O(v)=0\) and both corrected cubic outputs vanish.

The chosen (w) is harmless.  Any other solution differs from it by a mixed
tangent vector.  The polar forms of the two corrected quadratics vanish on
the entire tangent space by the second-jet certificate, so changing (w)
does not change (C_0) or (C_1).  The selected mixed equations then
eliminate (dH_i(u)), proving the displayed (O(t^4)) conclusion for every
formal arc.

## Structural interpretation

The first three local tests now line up:

1. the two missing pure differentials are mixed-conormal;
2. their corrected quadratic forms vanish on the full tangent space;
3. their corrected cubic forms vanish on the genuine second-order tangent
   cone, with the only nonzero ambient cubic explicitly factored by a lift
   obstruction.

This is strong evidence that the exceptional torus is controlled by a
successive Hasse-jet or valuation identity, rather than by transversality.
It also explains why evaluating a quartic residual on an arbitrary tangent
vector is not decisive: already at second order, a generic tangent vector
does not lift.  The next valid test must impose both the 39 quadratic lift
conditions and the third-order mixed lift equations before interpreting the
fourth pure coefficient.

## Reproduction

```sh
python3 computations/verify_n8_counterexample_pure_third_jet.py
python3 -O computations/verify_n8_counterexample_pure_third_jet.py
python3 -I computations/verify_n8_counterexample_pure_third_jet.py
python3 -S computations/verify_n8_counterexample_pure_third_jet.py
```

The frozen ledger records the exact Jacobian and tangent dimensions, the
rank-39 second-order obstruction map, the 59 obstructed basis cross terms,
the four-term factored scalar obstruction, and the exact cubic identities.
