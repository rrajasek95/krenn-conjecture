# L1 alignment excludes the cross-invertible three-invertible interior

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

The interior \(3I+1R+2Z\) subbranch isolated in
[the L1/L0 cut normal form](level-two-three-invertible-l1-l0-cut-normal-form.md)
has no full L0 completion. The decisive condition is stronger and simpler
than a symbolic cut-minor cover: after L1 alignment, every endpoint slice
is collinear with the same residual matching tensor, whereas the two pure
L0 targets are independent coordinate vectors.

This closes exactly the normal-form subbranch with:

* differential rank \(55\) and kernel equal to the five vertex gauges;
* potentials
  \(\nu=(\tau,\tau,\tau,\tau,-\tau,-\tau)\), \(\tau\ne0\);
* both selected columns nonzero at the rank-one site; and
* an invertible spoke from the invertible triangle to each zero site.

The rank-55 gauge boundary has since been removed by
[the gauge-boundary closure](level-two-three-invertible-gauge-boundary-closure.md).
The two genuine geometric boundaries have also been closed separately. The
one-column boundary reduces to two pure-cofactor charts, excluded by the
[pure-tensor obstruction](level-two-three-invertible-one-column-pure-tensor-obstruction.md),
and those terminal charts have no singular-spoke escape by the
[terminal-overlap theorem](level-two-three-invertible-one-column-singular-overlap.md).
With both selected columns nonzero at \(t\), the singular-cross boundary
reduces to two covariant common-factor types, excluded by the
[common-factor closure](level-two-three-invertible-common-factor-l1-closure.md).
What remains outside the combined results is the pre-terminal intersection
where the rank-one site is one-column, a zero site simultaneously lacks an
invertible triangle spoke, and at least one \(t\)-to-zero residual block is
live.  The complementary subcase with a dead \(t\)-to-zero star is closed by
the
[dead-\(tZ\) common-factor theorem](level-two-three-invertible-one-column-dead-tz-common-factor-closure.md).
The
[single-live flattening theorem](level-two-three-invertible-one-column-single-live-uniform-cross-closure.md)
also removes the uniform common-factor chart with one active/live zero and
the other endpoint inactive.  The endpoint-inactive single-live chart is
closed as well, with arbitrary singular triangle spokes, by the
[inactive-cross flattening theorem](level-two-three-invertible-one-column-single-live-inactive-cross-closure.md).
The live residue therefore has active nonuniform/opposite-type endpoint
data or a second active/live zero site.  The active nonuniform P/V and
opposite Q/U single-live charts are subsequently closed by the
[nonuniform-cross theorem](level-two-three-invertible-one-column-single-live-nonuniform-cross-closure.md).
Thus every single-live chart with the other zero endpoint inactive is now
excluded.  The
[fixed-shore theorem](level-two-three-invertible-one-column-single-live-other-active-cross-closure.md)
also closes every single-live chart with the other zero endpoint active.
A remaining pre-terminal overlap must therefore have both \(tZ\) blocks
live.

## Every aligned slice is a generalized cut gauge

Put \(C=\{0,1,2,3\}\), \(Z=\{4,5\}\), and
\(\sigma=(1,1,1,1,-1,-1)\). L1 alignment gives, for every endpoint slice
\((s,u)\),

\[
 U_r^s=a_sP_r,\qquad V_r^u=b_uQ_r\quad(r\in C),
 \qquad U_z^s=V_z^u=0\quad(z\in Z).
\]

Set \(c_{su}=\tau a_sb_u\). The selected generic-kernel equation yields

\[
 N^{su}_{rv}=2c_{su}M_{rv}\quad(r,v\in C),
 \qquad N^{su}_{rz}=0.
\]

On the zero-zero edge, \(X_4=X_5=0\) and
\(\nu_4+\nu_5=-2\tau\ne0\), so the same generic-kernel equation forces

\[
                              M_{45}=0.
\]

Consequently, on all fifteen residual blocks,

\[
             N^{su}=G(\lambda^{su}),\qquad
             \lambda^{su}=c_{su}\sigma.              \tag{1}
\]

These weights are not trace zero:

\[
                         \sum_r\lambda_r^{su}=2c_{su}.
\]

For any vertex weights \(\lambda\), each perfect matching counts every
vertex once, hence

\[
                d\Psi_M(G(\lambda))
                =\left(\sum_r\lambda_r\right)\Psi(M). \tag{2}
\]

Writing \(H=\Psi(M)\), equations (1)--(2) turn every L0 slice into

\[
 T_{su}=W_{su}H+d\Psi_M(N^{su})
       =(W_{su}+2c_{su})H.                            \tag{3}
\]

## The two pure targets contradict collinearity

For the pure slices, (3) would require scalars \(\kappa_0,\kappa_1\) with

\[
                 \kappa_0H=e_{0^6},\qquad
                 \kappa_1H=e_{1^6}.                  \tag{4}
\]

The targets are nonzero and linearly independent, so (4) is impossible.
Equivalently, using only the two pure coordinates \(h_0,h_1\), the four
equations

\[
 f_{00}=\kappa_0h_0-1,\quad f_{01}=\kappa_0h_1,\quad
 f_{10}=\kappa_1h_0,\quad f_{11}=\kappa_1h_1-1
\]

have the explicit unit certificate

\[
 1=f_{01}f_{10}-f_{00}f_{11}-f_{00}-f_{11}.          \tag{5}
\]

Thus a pure-zero cut-minor search or a mixed shared-factor solve is
unnecessary on this aligned subbranch. The exact incidence survivors found
separately do not contradict this theorem: linear incidence alone supplies
no aligned L1 endpoint stars, and those packets are already excluded at the
factored-L0 cut stage.

The standard-library checker
[verify_level_two_three_invertible_l1_pure_l0_collinearity_obstruction.py](../computations/verify_level_two_three_invertible_l1_pure_l0_collinearity_obstruction.py)
audits all fifteen aligned block coefficients, the forced \(M_{45}=0\),
all fifteen perfect matchings in (2), the non-trace-zero factor \(2c\), and
the polynomial identity (5). It has no external dependency.
