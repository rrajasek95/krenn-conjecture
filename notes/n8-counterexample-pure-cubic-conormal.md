# The colour-zero lock persists through the quartic jet

## Exact outcome

At the rational point (p) of the five-parameter mixed torus, set

\[
 F=H_0-H_{00000010}.
\]

The quadratic conormal factorization supplies five linear-multiplier
combinations of mixed equations.  Subtract them from (F).  The result
has no terms of degrees zero, one, or two, and its degree-three part
(R_3) has 166 signed ambient monomials.  Exact sparse division proves

\[
 \boxed{R_3=\sum_{j=1}^{33}L_jQ_j,}
\tag{1}
\]

where every (L_j) is in the mixed Jacobian row space and the quadratic
multipliers (Q_j) have 159 terms in total.  All their coefficients are
in \(\{\pm1,\pm2\}\).  The checker retains exact provenance expressing each
echelon conormal (L_j) as a combination of at most seven actual mixed
hafnian gradients.

Replacing each (L_j) by the corresponding combination of full mixed
equations gives a correction whose cubic part is (1).  Since every mixed
equation vanishes along a mixed-fibre arc, this proves

\[
 \boxed{H_0(x(t))\in t^4\mathbf Q[[t]]}
\]

for every formal mixed-fibre arc through (p).  Port-torus transport gives
the same conclusion at every generic point of the five-parameter orbit.

This complements the Hasse-cone calculation in
`verify_n8_counterexample_pure_third_jet.py`: that calculation also proves
(H_1=O(t^4)) on genuine arcs, because its apparent cubic is a tangent
coordinate times an actual second-lift obstruction.  The present result is
stronger for (H_0): after the quadratic equation correction, its cubic
vanishes modulo the linear conormal ideal on the entire tangent space,
without first imposing second-liftability.

## How the certificate is constructed

The 1,312 nonzero mixed gradients have exact rank 196.  Sparse echelon
elimination keeps, for every pivot row, its expression by actual mixed
gradients.  The largest such expression uses seven rows.  Triangular
polynomial division replaces a pivot variable only by variables to its
right, so it terminates after exactly 159 steps.  The remainder is empty,
and multiplying the 33 pivot forms by their recorded quadratic quotients
reconstructs all 166 terms of (R_3) exactly.

No numerical evaluation or finite-field inference enters the certificate.

## The quartic obstruction factorization

After lifting (1) from conormals to full mixed equations and subtracting,
the next residual begins in degree four.  Its ambient quartic part has
1,936 terms with coefficients

\[
 \left\{-4,-2,-1,-\tfrac12,
          \tfrac12,1,2,4\right\}.
\]

Unlike the cubic, this quartic does **not** vanish on the whole
56-dimensional linear tangent space.  In the free-coordinate tangent
basis its entire 1,936-term ambient expansion collapses to the four-term
rectangle

\[
 -2z_{0400}z_{1601}
   (z_{3710}+z_{3711})(z_{6701}-z_{6711}).
\tag{2}
\]

Setting the four coordinates `0400,1601,3710,6701` equal to one and all
other tangent parameters to zero gives the exact value (-2).  The checker
also reconstructs this tangent vector in ambient coordinates and replays
all 1,312 mixed Jacobian rows against it.

That tangent witness does not lift to second order.  Reconstructing the
complete second fundamental form and taking its exact rank-39 row basis
produces the quadratic lift obstruction

\[
 \mathcal O_3=z_{0400}(z_{3710}+z_{3711}).
\tag{3}
\]

Consequently (2) is the one-term ideal identity

\[
 \boxed{R_4|_{\ker J_{\mathrm{mix}}}
 =-2z_{1601}(z_{6701}-z_{6711})\,\mathcal O_3.}
\tag{4}
\]

Every tangent direction of a genuine mixed-fibre arc is second-order
liftable, so all 39 quadratic obstructions, including
\(\mathcal O_3\), vanish.  Equation (4) therefore strengthens the cubic
result to

\[
 \boxed{H_0(x(t))\in t^5\mathbf Q[[t]]}
\]

for every formal mixed-fibre arc through (p).

There is no hidden dependence here on the second and third arc
coefficients.  After (1), the corrections use the **full** mixed hafnian
equations, not merely their Hasse pieces.  The fully corrected residual has
identically zero homogeneous parts in degrees below four.  Substituting

\[
 y(t)=tv+t^2w+t^3u+O(t^4)
\]

therefore makes its coefficient of (t^4) exactly (R_4(v)): the vectors
(w) and (u) could couple only to lower homogeneous pieces, and those
pieces are zero.  Since the full equation corrections vanish along the
arc, the corrected residual equals (H_0) there.

Thus the unconditional statement

\[
 R_4|_{\ker J_{\mathrm{mix}}}=0
\]

is false, but the exact obstruction-ideal statement (4) is true.  This is
the fourth successive osculation lock: linear conormality, quadratic
conormal products, cubic conormal division, and now a quartic factor by a
genuine lift obstruction.

## Reproduction

```sh
python3 computations/verify_n8_counterexample_pure_cubic_conormal.py
python3 -O computations/verify_n8_counterexample_pure_cubic_conormal.py
python3 -I computations/verify_n8_counterexample_pure_cubic_conormal.py
python3 -S computations/verify_n8_counterexample_pure_cubic_conormal.py
```

The frozen ledger records the Jacobian ranks, exact cubic support and
coefficient set, factor and multiplier counts, zero remainder, quartic
support and tangent restriction, the exact tangent witness, the rank-39
second-lift obstruction space, the one-term factorization (4), and the
formal-arc (O(t^5)) conclusion.
