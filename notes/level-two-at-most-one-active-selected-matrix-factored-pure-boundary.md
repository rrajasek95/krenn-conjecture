# The rank-(55) factored-pure boundary also covers (1R+5Z)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

The sharp residual packet (M^\sharp) and its two separate factored-pure
endpoint-star assignments work unchanged when at most one selected matrix
is nonzero, regardless of whether that matrix has rank one or two.  Thus
the endpoint-rank patterns

\[
                         6Z,\qquad 1R+5Z,\qquad 1I+5Z          \tag{1}
\]

all reach the same exact boundary:

\[
 \operatorname{rank}d\Psi_{M^\sharp}=55,\qquad
 \operatorname{rank}(d\Psi_{M^\sharp})_{\rm mixed}=53,        \tag{2}
\]

and two separate literal endpoint-star assignments realize

\[
 (e_{0^6},0,0,0),\qquad (0,0,0,e_{1^6}).                     \tag{3}
\]

The preimages in (3) are not one shared four-slice assignment.  The same
four-edge unit-ideal certificate excludes simultaneous compatibility on
this fixed residual packet.  Hence (1) reaches both individual factored
faces at rank (55), while the known shared coupling on the same endpoint
patterns has rank (38).

## Selected equations and R2

Put (X_i=0) for (i\ne0), let (X_0) be arbitrary, and set every
potential to zero.  Because the generic-kernel numerator is pairwise,
(X_iJX_j^{\mathsf T}=0) for every edge.  All sixty scalar identities and
all selected level-two output rows therefore vanish.  The rare/rare slice
also vanishes: a perfect matching cannot attach both selected endpoints to
the sole active residual site.

When (X_0\ne0), residual root (0) has the same two internal pure-column
witnesses (03/E_{00}) and (02/E_{11}), with nonzero complementary
cofactors.  This argument is independent of the rank of (X_0).  The
other five roots preserve the residual binary pair.  When (X_0=0), all
six roots preserve.

The standard-library checker
[verify_level_two_at_most_one_active_selected_matrix_factored_pure_boundary.py](../computations/verify_level_two_at_most_one_active_selected_matrix_factored_pure_boundary.py)
tests exact selected matrices of ranks zero, one, and two; reruns the
rational and three modular rank calculations; directly sums both sets of
256 literal endpoint slices; and checks the generic-kernel, selected, and
R2 conditions.  It passes normal, optimized, and isolated Python.

## Scope

This is a boundary witness, not a full-source survivor or a closure of any
stratum.  It sharpens the (1R+5Z) map and unifies the previously separate
(1I+5Z) and (6Z) rebindings.  Arbitrary residual packets, simultaneous
four-slice compatibility at rank (55), and endpoint patterns with two or
more active selected matrices remain open.
