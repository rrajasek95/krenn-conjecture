# The first five-tail coherence is not an ordinary triple cube

## Result

For the labelled five-edge tail

\[
       23\mid45\mid67\mid89\mid AB,
\]

the first generator of the rational four-dimensional
\(\operatorname {sgn}\otimes\operatorname {Std}_5\) coherence module has
an exact literal candidate boundary.  It uses all ten two-edge window/fine
idempotents, four word idempotents, four inherited \(h=4\) presentation
triangles and twelve disjoint-edge Beck--Chevalley squares.  It is not the
boundary of an ordinary fixed-window triple restriction/Koszul cube: even
after granting the entire space of all fifteen BC-square coordinates, its
addition raises rank from 15 to 16.  The coefficient of \(T_{123}\) is a
primitive separating covector and has value \(-1\).

Thus the natural \(h=6\) filler is a genuinely new *higher
Hasse-linearity/coherence cell for the already isolated \(\Phi_{KS,r_0}/P_f\)
schema*.  It is neither an ordinary triple BC cube nor evidence for a second
response-to-cap operation.  The physical cell is not yet constructed.

The executable certificate is
[`verify_h6_signed_standard_three_cell_physical_label_gate.py`](../computations/verify_h6_signed_standard_three_cell_physical_label_gate.py).

## Literal five-tail lift

Number the five tail edges by \(0,\ldots,4\).  For a window
\(W=\{i,j\}\), relabel the committed \(h=4\) word template by

\[
 w_W=0121\,c_0c_1c_2c_3c_4,
 \qquad
 c_k=\begin{cases}12,&k=\min W,\\22,&k\ne\min W.\end{cases}
\]

The fine label is

\[
  T_{W^c}\,q_{(v,W)},
\]

with the three edges in \(W^c\) retained as ordered removed/reinserted
spectator labels.  Its repeated parent is \(P_3+K_2\), together with three
labelled spectator \(K_2\) factors, and its operation parent is the prolonged
PP/AugP2 presentation of \(\Phi_{KS,r_0}/P_f\).  Every three-edge
restriction gives exactly the committed \(h=4\) pattern: for
\(a<b<c\), presentations \(bc,ac,ab\) mark tail pairs \(b,a,a\),
respectively.  The global packet contains ten distinct fine idempotents and
four literal words.

This is an exact consistent relabelling of all local \(h=4\) restrictions.
It does **not** itself prove that a decorated full-source \(h=6\) generator
with these faces exists.

## The signed-standard boundary

With the face conventions of the uniform Johnson checker, take

\[
\begin{aligned}
B_0={}&-T_{123}+T_{124}-T_{134}+T_{234}\\
 &-Q_{0123}^{0}+Q_{0123}^{1}-Q_{0123}^{2}\\
 &+Q_{0124}^{0}-Q_{0124}^{1}+Q_{0124}^{2}\\
 &-Q_{0134}^{0}+Q_{0134}^{1}-Q_{0134}^{2}\\
 &+Q_{0234}^{0}-Q_{0234}^{1}+Q_{0234}^{2}.
\end{aligned}
\]

Its edge boundary is zero.  The four triangle coefficients sum to zero, as
do the twelve square coefficients.  The ten window vertices in the faces
use all ten literal fine labels and all four literal words above.

For \(a=0,\ldots,4\), signed relabelling gives
\(B_a=\operatorname {sgn}(p_a)p_aB_0\), with
\(\sum_a B_a=0\).  These span the four-dimensional
\(\operatorname {sgn}\otimes\operatorname {Std}_5\) module.  Hence one
physical labelled cell \(K_0\), plus signed \(S_5\)-naturality, would supply
the five cells \(dK_a=B_a\) with their single relation.

## Exact ordinary-cube counterguard

An ordinary cube in three fixed spectator directions:

- remains in one word and one fine-window idempotent;
- has six codimension-one square faces; and
- has no presentation-triangle coordinate.

The checker makes the strictly stronger grant of every one of the fifteen
BC-square coordinate directions in the five-tail packet.  That square-only
space has rank 15.  Adjoining \(B_0\) gives rank 16.  The coordinate dual
\([T_{123}]\) vanishes on the whole square-only grant and evaluates
\(-1\) on \(B_0\).  Therefore no combination of ordinary fixed-window
triple cubes can have this boundary.  A mixed mapping cylinder which also
has the four \(h=4\) triangles would be precisely the new higher
Hasse-linearity datum, not an ordinary cube already present in the current
constructor grammar.

## Protected-row debt

Every constant face readout cancels on \(B_0\), including the constant
\(r_0\) vector.  So the packet exposes no immediate scalar obstruction on
target, private \(B\), reduced Eq, \(q/\)anchor, \(W\), pointed \(P_f\),
ordinary residue, or ridge/\(\eta/\sigma\).  The first unresolved law is
rowwise.  If the three square types on each four-support share the
transported readout \(R_Q\), it is

\[
\begin{aligned}
0={}&-R_T(123)+R_T(124)-R_T(134)+R_T(234)\\
   &-R_Q(0123)+R_Q(0124)-R_Q(0134)+R_Q(0234).
\end{aligned}
\]

The first mismatch is therefore at the word/fine/operation-parent lift,
before a nonzero protected scalar readout is forced.  A positive proof must
construct one literal \(K_0\) with the sixteen faces above and verify this
alternating identity on every protected row.  Signed naturality then gives
the other four instances.

## Scope

This is an exact rational one-five-tail label/support/rank audit, pinned to
the committed \(h=4\), \(h=5\), and uniform Johnson calculations.  It does
not construct the physical \(K_0\), determine arbitrary nonconstant
two-face readouts, prove a full higher Hasse tower, or supply the separate
full matching-cover descent datum.
