# A common isotropic pencil reaches rank (55) through (4R+2Z)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

On the sharp residual packet (M^\sharp), activate any subset of sites
(0,1,2,3) with nonzero rank-one selected matrices

\[
                         X_i=h_i e_0^{\mathsf T},               \tag{1}
\]

and set the other selected matrices and all potentials to zero.  For every
one of the sixteen subsets, the packet satisfies generic-kernel, selected,
and residual-R2 conditions and retains

\[
 \operatorname{rank}d\Psi_{M^\sharp}=55,\qquad
 \operatorname{rank}(d\Psi_{M^\sharp})_{\rm mixed}=53.        \tag{2}
\]

The two separate literal endpoint-star assignments still realize the pure
faces

\[
                         (e_{0^6},0,0,0),qquad
                         (0,0,0,e_{1^6}).                      \tag{3}
\]

Consequently this one common-isotropic-pencil family supplies exact
rank-(55/53) boundary points in every pattern

\[
                         kR+(6-k)Z,qquad 0\le k\le4.           \tag{4}
\]

As before, the two assignments in (3) are not simultaneous; the fixed
four-edge unit-ideal certificate excludes their shared compatibility on
(M^\sharp).  This is a boundary family, not a full-source survivor or a
closure of any stratum.

## Selected equations

The common input line in (1) is isotropic for
(J=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)):

\[
                         e_0^{\mathsf T}Je_0=0.
\]

Therefore every pair-pencil numerator vanishes,

\[
 X_iJX_j^{\mathsf T}
       =(e_0^{\mathsf T}Je_0)h_ih_j^{\mathsf T}=0.             \tag{5}
\]

This proves all sixty generic-kernel scalar identities and makes every
selected level-two row zero.  It also makes the selected rare/rare
eight-site slice zero, since that slice is the residual differential of
the same pairwise tangent.  The checker additionally verifies this
literally for both endpoint-star assignments and all sixteen active
subsets.

## The four R2-capable roots

Each active root must use the two-internal-witness alternative.  The sharp
packet has the following physical pure-column edges:

\[
\begin{array}{c|cc}
\text{root}&\text{output }0&\text{output }1\\ \hline
0&03&02\\
1&12&13\\
2&23&20\\
3&32&31.
\end{array}                                                     \tag{6}
\]

Every displayed edge has a nonzero complementary four-site cofactor.  The
checker audits the full binary cofactor census, not merely the nonzero
edge entry.  Thus any subset of roots (0,1,2,3) may be activated; the
other roots preserve because their selected matrices vanish.

Roots (4,5) have a pure-zero mutual edge but no residual pure-one edge on
this packet, so this argument deliberately stops at four active rank-one
sites.  It makes no claim that (5R+1Z) or (6R) is impossible.

The standard-library checker
[verify_level_two_up_to_four_rank_one_isotropic_pencil_factored_pure_boundary.py](../computations/verify_level_two_up_to_four_rank_one_isotropic_pencil_factored_pure_boundary.py)
exhausts the subset counts (1,4,6,4,1), directly audits both sets of 256
literal slices in each case, and reruns the rational and three modular rank
signatures.  It passes normal, optimized, and isolated Python.
