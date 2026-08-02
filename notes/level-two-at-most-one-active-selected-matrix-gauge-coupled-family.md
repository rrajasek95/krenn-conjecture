# One gauge-coupled family covers selected ranks (0), (1), and (2)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

The shared four-slice rank-(38) packet and its enlarged sparse deformation
chart work with an arbitrary selected matrix at one site and zero selected
matrices at the other five sites.  With all potentials zero, this uniformly
covers the endpoint-rank patterns

\[
                         6Z,\qquad 1R+5Z,\qquad 1I+5Z.          \tag{1}
\]

For each pattern one shared binary endpoint-star assignment realizes

\[
 (T_{00},T_{01},T_{10},T_{11})=(e_{0^6},0,0,e_{1^6}),         \tag{2}
\]

all generic-kernel and selected level-two rows vanish, and residual R2
holds at every root.  The residual differential ranks remain

\[
                  \operatorname{rank}D=38,\qquad
                  \operatorname{rank}D_{\rm mixed}=36.         \tag{3}
\]

Moreover, the enlarged natural sparse-support chart has the same exact
(40\)-by-(34) Jacobian of rank (25): seven residual tangent directions
integrate to the diagonal-torus orbit and two are endpoint-only
rescalings.  Thus the whole nonzero chart stays at rank (38/36) for all
three selected ranks.

This is a boundary construction and rigidity result, not a closure of any
endpoint-rank stratum.  It allows only the residual and endpoint support of
the gauge-coupled ansatz and requires the mixed tangents to lie on the
canonical vertex-gauge line.

## Pairwise selected equations

Let (X_2) be arbitrary and put (X_i=0) for (i\ne2), with
(\nu_i=0) for every (i).  Every generic-kernel numerator is pairwise:

\[
                         X_iJX_j^{\mathsf T}.
\]

Since no pair contains two active matrices, all sixty numerators vanish,
as do their potential-sum right sides.  Their differential image is the
zero selected row.  The selected rare/rare eight-site slice also vanishes:
a perfect matching would have to attach the two selected endpoints to two
distinct residual sites, whereas only site (2) has a nonzero selected
matrix.

## Residual R2

The five zero selected sites preserve the residual binary pair.  At site
(2), the residual packet has two fixed internal witnesses:

\[
                         23/E_{00},\qquad 20/E_{11},            \tag{4}
\]

and both complementary four-site cofactors are nonzero.  Hence the active
root satisfies the two-internal-witness alternative regardless of whether
(X_2) has rank one or two.  When (X_2=0), it preserves as well.

The standard-library checker
[verify_level_two_at_most_one_active_selected_matrix_gauge_coupled_family.py](../computations/verify_level_two_at_most_one_active_selected_matrix_gauge_coupled_family.py)
tests exact representatives of ranks zero, one, and two; directly sums all
binary and selected endpoint slices; checks generic-kernel, selected, and
R2 rows; and verifies the ranks over the rationals and three prime fields.
It passes normal, optimized, and isolated Python.
