# Independent audit of the common-coloop residual coupling

Audit date: 2026-07-29.

## Verdict

**PASS.**  The common-coloop note proves the claimed uniform lift/descent
and reduces every non-descending support pattern to the stated one- or
two-corner quotient.  It does not claim closure of those final corners.

## Checks

1. The Taylor expansion

   \[
   q^{[h]}=\rho q_0^{[h-1]},\qquad
   q^{[h-1]}=q_0^{[h-1]}+\rho q_0^{[h-2]}
   \]

   is exact in the site-square-zero algebra.  Degree and collision remove
   precisely the terms omitted in equations (21)--(22); no cancellation
   of a common power is used.
2. Contracting by the two off-site kernel vectors gives equations
   (25)--(26).  For every label in either kernel support, these equations
   put \(Y_i\) in
   \(I=\operatorname{im}(z\mapsto zq_0^{[h-1]})\).
3. If all three \(Y_i\) lie in \(I\), the constructed quadratic
   \(\widetilde q\) satisfies
   \(\widetilde q^{[h]}=X_0+X_1+X_2\) literally.  This is the claimed
   exact two-site descent, not only a selected-coefficient identity.
4. Modulo \(V_x\otimes I\), the top power and both first jets vanish.
   The surviving table is exactly
   \(\overline\Gamma_{ij}
   =\delta_{ij}e_i^{(x)}\otimes\overline Y_i\).
5. The support classification is exhaustive: disjoint \(2+1\) supports
   descend; a non-descending disjoint branch is singleton--singleton;
   binary pure support leaves at most one corner; unary support leaves at
   most two.
6. In the nondegenerate singleton--singleton branch, the two anchor planes
   coincide, the local vectors are independent, and solving in that
   two-plane gives the crossed form (45) with the displayed coefficients.
7. The formal full-nine guard is explicitly not asserted to come from
   consecutive powers.  The consecutive-power guard is explicitly not
   asserted to satisfy the anchors or all nine rows.  Together they justify
   the stated limitation without purporting to be counterexamples.

## Remaining boundary

The crossed target-zero row is invariant under the relative label torus and
therefore does not identify the surviving curvature corner with an overlap
minor.  The note correctly leaves source-faithful two-chart
curvature-corner injectivity open.
