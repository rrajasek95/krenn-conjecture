# Site-4 one-cell lifts cannot combine transverse incidence with full R2

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let \(M^\circ\) be the full-R2 packet underlying the
[dense transverse linear-incidence survivor](level-two-two-invertible-transverse-column-l0-incidence-survivor.md):
before the lift \(M_{04}(0,0)=1\), it has

\[
 \operatorname{rank}d\Psi_{M^\circ}=54,\qquad
 \operatorname{rank}(d\Psi_{M^\circ})_{\rm mixed}=52,           \tag{1}
\]

and both pure target directions lie in its tangent image.  This note
classifies the eight affine one-cell lines

\[
                     M^\circ+tE_c                              \tag{2}
\]

where \(c\) is a zero entry on one of the four spokes
\(04,14,24,34\) to zero site \(4\).

No member of these eight lines with \(t\ne0\) simultaneously has

\[
 \operatorname{rank}D=55,\qquad
 \operatorname{rank}D_{\rm mixed}=53,\qquad
 e_{0^6},e_{1^6}\in\operatorname{im}D,
 \quad\text{and full literal R2}.                              \tag{3}
\]

This is a complete obstruction for the stated one-cell family, not for
arbitrary simultaneous changes of the eight free transverse blocks.

## The eight directions

The zero entries on the site-\(4\) spokes are exactly

\[
\begin{array}{c|c}
\text{block}&\text{zero cells}\\ \hline
M_{04}&(0,0),(1,0)\\
M_{14}&(0,0),(1,0)\\
M_{24}&(0,0),(1,0)\\
M_{34}&(0,0),(1,1).
\end{array}                                                     \tag{4}
\]

They split into three exact classes.

\[
\begin{array}{c|c|c}
\text{directions }c&\text{obstruction for }t\ne0&
  \text{unit calibration }(\operatorname{rank}D,
  \operatorname{rank}D_{\rm mixed})\\ \hline
04(0,0),04(1,0)&\text{R2 fails at root }0&(55,53)\\
14(0,0),14(1,0)&\text{R2 fails at root }1&(55,53)\\
24(0,0)&\operatorname{rank}D\le54&(54,52)\\
34(0,0),34(1,1)&\operatorname{rank}D\le54&(54,52)\\
24(1,0)&\operatorname{rank}D_{\rm mixed}\ge54&(55,54).
\end{array}                                                     \tag{5}
\]

Every moved edge has zero potential sum on the dense ray.  Thus all eight
families retain the exact generic-kernel equation and all 64 selected
level-two rows.  The obstruction in (5) occurs only when the necessary L0
rank/incidence and R2 conditions are intersected.

## Why the four incidence lifts lose R2

At each invertible root \(0,1\), the base packet has core output-zero
witnesses and exactly one output-one witness: the spoke to site \(4\).
The blocks \(M_{04}\) and \(M_{14}\) have zero first column and nonzero
second column.  Adding \(t\ne0\) to either zero first-column entry makes
that block non-pure.  Hence the corresponding root has no output-one
witness.

These are precisely the four one-cell directions with the desired unit
rank signature \(55/53\).  The lift recorded in the incidence-survivor
note is the first row of (5).

## Polynomial kernels on three lines

Write

\[
       D_c(t)=D^\circ+tD_c^{(1)}.                               \tag{6}
\]

For \(c=34(0,0),34(1,1)\), the sixth kernel vector of the rank-\(54\)
base packet remains a fixed kernel vector of \(D_c(t)\).  Together with
the five universal vertex gauges, it gives six independent vectors over
\(\mathbf Q(t)\).

For \(c=24(0,0)\), the exact audit supplies a degree-one vector

\[
                         x_c(t)=x_0+t x_1                       \tag{7}
\]

and checks coefficientwise

\[
 D^\circ x_0=0,\qquad
 D^\circ x_1+D_c^{(1)}x_0=0,\qquad
 D_c^{(1)}x_1=0.                                                \tag{8}
\]

At \(t=2\), (7) and the five gauges have rank six, proving their
independence over \(\mathbf Q(t)\).  Therefore every \(55\)-minor of
\(D_c(t)\) vanishes identically.  Specialization cannot increase rank,
so \(\operatorname{rank}D_c(t)\le54\) for every \(t\).

The certificate vectors are integral and are recorded literally in the
checker.  Their large coefficients reflect the deliberately generic
integer base packet; no numerical reconstruction is used.

## Two mixed minors on the last line

For \(c=24(1,0)\), two exact \(54\times54\) minors \(A(t),B(t)\) of the
mixed differential factor as

\[
\begin{aligned}
 \det A(t)
  &=C_A t^{11}(634878t+1508087)
                   (276626208t-1193709223),\\
 \det B(t)
  &=C_B t^{12}(116590108t-677131063),
\end{aligned}                                                   \tag{9}
\]

with nonzero integers \(C_A,C_B\).  The two nonzero roots of the first
minor,

\[
 -\frac{1508087}{634878},\qquad
  \frac{1193709223}{276626208},                                 \tag{10}
\]

are both distinct from the nonzero root
\(677131063/116590108\) of the second.  Consequently at least one minor
in (9) is nonzero for every \(t\ne0\), and

\[
                       \operatorname{rank}D_c(t)_{\rm mixed}
                       \ge54.                                  \tag{11}
\]

This excludes the required mixed rank \(53\), including the two exceptional
parameters at which the first minor alone vanishes.

The standard-library exact checker
[verify_level_two_two_invertible_transverse_column_one_cell_r2_obstruction.py](../computations/verify_level_two_two_invertible_transverse_column_one_cell_r2_obstruction.py)
audits the zero-cell census, generic-kernel and selected-row coefficients,
the literal R2 tables, the three polynomial-kernel identities, independence
from the five gauges, both minor factorizations, and the rational root
separation.  It verifies each degree-\(\le15\) determinant identity at
sixteen exact integer values.

## Remaining scope

The other zero site \(5\), nonzero-cell deformations, two-cell moves, and
general simultaneous changes of the 32 free scalars are not classified
here.  In particular, this note does not prove that the full dense
transverse incidence locus is disjoint from full R2, nor does it address
factored L0 or overlapping L1.
