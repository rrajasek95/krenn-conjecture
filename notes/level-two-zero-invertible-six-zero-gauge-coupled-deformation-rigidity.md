# The shared four-slice (6Z) sparse chart is rigid at rank (38)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

The rank-(38) shared four-slice packet from the
[one-invertible minimal coupling](level-two-one-invertible-minimal-gauge-coupled-l0-family.md)
and its
[enlarged deformation chart](level-two-one-invertible-gauge-coupled-deformation-rigidity.md)
rebind verbatim to the all-zero selected endpoint pattern

\[
                         X_0=\cdots=X_5=0,\qquad \nu_0=\cdots=\nu_5=0.
\tag{1}
\]

The residual packet and endpoint stars realize one shared assignment with

\[
 (T_{00},T_{01},T_{10},T_{11})
                  =(e_{0^6},0,0,e_{1^6}).                    \tag{2}
\]

Thus the (6Z) chart reaches the simultaneous four-slice intersection,
not only the two separate factored pure faces recorded previously.  On the
natural enlarged sparse-support chart containing this point, however,

\[
             \operatorname{rank}d\Psi_M=38,\qquad
             \operatorname{rank}(d\Psi_M)_{\rm mixed}=36.     \tag{3}
\]

The exact (40\)-by-(34) ansatz Jacobian still has rank (25).  Its seven
residual tangent directions integrate only to the diagonal-torus orbit,
and the remaining two kernel directions are endpoint-only rescalings.
Consequently every member on the nonzero sparse chart has the ranks in
(3).

This does not close (6Z).  It excludes only the enlarged support ansatz
with arbitrary blocks on (01,02,13,23,45), scalar (E_{01}) blocks on
(04,05,14,15), endpoint stars on the eight minimal support lines, and
mixed tangents proportional to the canonical vertex gauge.  Activating the
other six residual edges, enlarging endpoint support, or using different
mixed kernel directions remains open.

## Why the rebinding is exact

The residual differential, four factored (L_0) equations, deformation
Jacobian, and diagonal covariance depend only on (M) and the binary
endpoint-star coefficients.  They do not depend on the selected matrices
(X_i).  Therefore the full nonlinear classification of the enlarged
sparse chart carries unchanged from the (1I+5Z) calculation.

After (1), every generic-kernel numerator and every potential-sum right
side vanishes.  Hence all sixty generic-kernel scalar equations and all
sixty-four selected level-two output rows vanish.  Each root also has zero
selected rare column, so all six roots satisfy the preservation alternative
of residual R2.  No internal pure-column witness is needed.

For a nontrivial integrated member, the checker directly sums all 256
binary endpoint slices, separately checks the rare/rare selected slice
after rebinding the six matrices to zero, and obtains the rational and
three modular rank signatures

\[
                 (38,38,38,38),\qquad(36,36,36,36).           \tag{4}
\]

The standard-library checker
[verify_level_two_zero_invertible_six_zero_gauge_coupled_deformation_rigidity.py](../computations/verify_level_two_zero_invertible_six_zero_gauge_coupled_deformation_rigidity.py)
also reruns the (40\)-equation Jacobian and the integrated rank-one cross
rectangle classification.  It stays live under normal, optimized, and
isolated Python.
