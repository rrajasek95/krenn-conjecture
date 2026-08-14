# The first-collision minimal EqSystem-to-AugP2 bimodule gate

## Statement

Fix the canonical first forbidden pair

\[
 a=(01{:}11),\qquad b=(07{:}11),
\]

and retain the two literal root labels \(\rho\in\{AB,AC\}\).  Consider the
smallest mapping-cylinder candidate whose response and cap pieces are

\[
 \langle C_{ab,\rho}\rangle\xrightarrow{d}
 \langle R_{ab,\rho}\rangle,
 \qquad
 \langle r_{0,\rho}\rangle\xrightarrow{d}
 \langle E_\rho\rangle,
\]

and which adds only components forced by \(d\Phi=\Phi d\).  At the aggregate
two-term level there is exactly one monic, root-natural chain map:

\[
 \Phi_1(C_{ab,\rho})=r_{0,\rho},\qquad
 \Phi_0(R_{ab,\rho})=E_\rho.
\]

This aggregate map does **not** lift to a source-provenant literal dg
bimodule in the present constructors.  The earliest missing operation face
is the fixed-window DQ/PS mate

\[
 A_{[a\mid b]}\longrightarrow B.
\]

The four required mates form the expected rank-three \(K_{2,2}\) incidence
orbit, but the physical fixed-window constructor implements none of the four.
If all four mates are granted formally, the next debt is an exact 66-term
cap-Eq complement for each root label.

The executable certificate is
`computations/verify_h3_first_collision_minimal_augp2_bimodule_candidate_gate.py`.

## Aggregate uniqueness

Write

\[
 \Phi_1(C_{ab,AB})=a_{AB}r_{0,AB},\quad
 \Phi_0(R_{ab,AB})=b_{AB}E_{AB}
\]

and similarly over \(AC\).  The two chain-map equations are
\(a_{AB}=b_{AB}\) and \(a_{AC}=b_{AC}\).  Literal root naturality gives
\(a_{AB}=a_{AC}\) and \(b_{AB}=b_{AC}\).  Together with the monic
normalization \(a_{AB}=1\), these equations have rank four in four variables;
their unique solution is

\[
 (a_{AB},b_{AB},a_{AC},b_{AC})=(1,1,1,1).
\]

Thus there is no scalar freedom with which to repair any later fine or
operation-labelled face.

## Complete literal boundary

The official mixed collision has 30 signed terms before restriction to the
direct-free physical chart.  In the complete 90-term cap row:

* 12 matchings contain \(a\);
* 12 matchings contain \(b\);
* no matching contains both, because they repeat site 0;
* 66 matchings contain neither.

Consequently the two ordered collision branches retain exactly 12 terms
each.  Private deletion followed by reinsertion reconstructs 24 distinct cap
terms with coefficient \(+1\): the boundary sign and map sign occur twice.
All repeated-site and fine monomials are retained before collection.  The
remaining 66 terms are exactly the matchings containing neither \(a\) nor
\(b\), not an unexplained rank count.

Root labels are a literal direct sum, so no AB/AC cancellation is allowed.
The complete boundary therefore consists of 48 root-labelled collision
faces and leaves 132 root-labelled cap-Eq faces unmatched.

## Operation provenance

The required fixed-window mate orbit is

\[
 A_{[a\mid b]}\to B,\quad A_{[a\mid b]}\to C,\quad
 A_{[b\mid a]}\to B,\quad A_{[b\mid a]}\to C.
\]

In the ordered vertex basis
\((A_{[a\mid b]},A_{[b\mid a]},B,C)\), their incidence columns have rank
three and are killed by the balanced covector \((1,1,-1,-1)\).  The current
fixed-window packet has 100 internal columns of rank 46 and zero
cross-profile edges.  One formal switch raises rank to 47 and the second
switch type raises it to 48.

The root-endpoint covariance orbit does not supply an absolute replacement:
canonical transport to a fixed object makes the fold boundary zero, while
the raw fold changes \(H_0\).  Its presentation-safe form retains the
relative carriers

\[
 d\Gamma_B=t_B-(B-A),\qquad d\Gamma_C=t_C-(C-A).
\]

Hence the first missing physical datum is a genuine mixed
EqSystem-to-AugP2 DQ/PS mate constructor, beginning with
\(A_{[a\mid b]}\to B\).  If such a natural four-mate constructor is added,
one must still fill the separate 66-term Eq complement per root; the mate
orbit alone does not do so.

## Scope and terminal use

This is exact for the canonical first pair, the direct-free 90-term chart,
both root labels, and the current literal source APIs.  It is a dg-bimodule
test, not another objectwise Tate cell.  No arbitrary dense
\(90\times24\) formal landing map is admitted.  The four augmented packaging
directions (hidden lower/P2, central Eq, mixed incidence, shifted ridge) are
checked only downstream and cannot manufacture the missing DQ/PS mates.

Therefore the sharp terminal alternative is ordered:

1. operation debt: construct the four source-valid DQ/PS mates;
2. coefficient debt: extend their cylinder across the exact 66-term
   neither-\(a\)-nor-\(b\) cap complement, independently for AB and AC.
