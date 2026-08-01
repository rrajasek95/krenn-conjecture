# Mixed L0 support pairs collapse to a pure-determinantal cover

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Outcome and scope

On the four-cycle-generic invertible residual chart, the 17 possible support
graphs for each factored mixed L0 slice collapse much more sharply than the
support census alone suggests:

* every nonempty star or (K_3\sqcup K_3) support is impossible;
* hence (288) of the (17^2=289) ordered support pairs are excluded; and
* the empty--empty pair forces the two pure slices onto an explicit closed
  determinantal cover.

On the dense subchart where the pure blocks are invertible on one common
residual triangle, the empty--empty pair is impossible too. Thus all 289
support pairs are excluded there.

This is a finite generic theorem, not a new closure of the fully invertible
residual locus. That locus is already excluded by the independent
[fully invertible residual R2 theorem](level-two-fully-invertible-residual-obstruction.md).
The reusable content here is local: it applies whenever the residual blocks
on the live mixed-support edges are invertible, even if other residual blocks
are singular.

## 2. Every nonempty allowed support is impossible

For one mixed slice put

\[
 X_r=[U_r^s\ V_r^t],\qquad
 X_rJX_u^{\mathsf T}
   =a_{ru}M_{ru},\qquad a_{ru}=\lambda_r+\lambda_u,
 \tag{1}
\]

where (J=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)).
If (a_{ru}\ne0) and (M_{ru}) is invertible, then both (X_r) and
(X_u) are invertible. If (a_{ru}=0), the left side of (1) is zero.

Every labelled star and every labelled (K_3\sqcup K_3) in the 17-pattern
list has two properties:

1. every vertex is incident to a live edge; and
2. some pair of live vertices is joined by a dead edge.

If the residual blocks on the live edges are invertible, property 1 makes
all six (X_r) invertible. The dead edge in property 2 would then require
the invertible matrix (X_rJX_u^{\mathsf T}) to equal zero, a contradiction.
Thus the only possible support is empty. Applying this to both mixed slices
leaves only the empty--empty ordered pair.

On a fully invertible four-cycle-generic packet, the hypothesis is automatic.
On a singular packet, the same argument still excludes a candidate star if
its five live spoke blocks are invertible, or a candidate
(K_3\sqcup K_3) if its six live triangle blocks are invertible. No
invertibility is required on the dead witness edge.

## 3. The shared triangle lemma

The empty mixed support means

\[
 U_r^0(V_u^1)^{\mathsf T}+V_r^1(U_u^0)^{\mathsf T}=0
 \qquad(r\ne u).                                      \tag{2}
\]

Suppose three sites (r,u,v) have both pure site factors

\[
 X_x^{00}=[U_x^0\ V_x^0],\qquad
 X_x^{11}=[U_x^1\ V_x^1]                              \tag{3}
\]

invertible. Apply an independent residual basis change at each site so that
(X_x^{00}=I_2), and write

\[
 d_x=(X_x^{00})^{-1}V_x^1=(c_x,e_x)^{\mathsf T}.
\]

Equation (2) on a pair (x,y) becomes

\[
 e_0d_y^{\mathsf T}+d_xe_0^{\mathsf T}
 =\begin{pmatrix}c_x+c_y&e_y\\e_x&0\end{pmatrix}=0. \tag{4}
\]

Hence every (e_x=0) and the three scalars (c_x) are pairwise negatives.
In characteristic zero, the triangle equations force every (c_x=0).
Thus (V_x^1=0) at all three sites, contradicting the invertibility of
(X_x^{11}).

Only one empty mixed slice is used in this argument. The second empty slice
is part of the 17-by-17 reduction but is not needed once a common pure-live
triangle has been found.

## 4. A blockwise closed cover

Let

\[
 N^{ss}_{ru}=X_r^{ss}J(X_u^{ss})^{\mathsf T}
 =K^{ss}_{ru}+(\lambda_r^{ss}+\lambda_u^{ss})M_{ru}. \tag{5}
\]

Since (det J=-1),

\[
 \det N^{ss}_{ru}
 =-\det X_r^{ss}\det X_u^{ss}.                        \tag{6}
\]

If all six pure blocks on a residual triangle (T) were invertible, then
the three sites would satisfy the forbidden hypothesis of Section 3.
Consequently every empty--empty factored completion must obey

\[
 \boxed{
 \prod_{ru\in\binom T2}
   \det N^{00}_{ru}\,\det N^{11}_{ru}=0
 \quad\text{for every }T\in\binom R3.}               \tag{7}
\]

These twenty equations define the promised closed pure-determinantal cover.
When (M_{ru}) is invertible,

\[
 \det(K^{ss}_{ru}+aM_{ru})
 =a^2\det M_{ru}+O(a),                                \tag{8}
\]

so each determinant is a nonzero polynomial in its pure potential sum.
Avoiding the finitely many determinant hypersurfaces is a nonempty Zariski-
open condition. Therefore the common-pure-triangle obstruction excludes the
empty--empty pair on a dense pure-potential subchart, while (7) records the
precise exceptional locus still requiring analysis.

## 5. Exact audit and revised frontier

[verify_level_two_mixed_support_pair_collapse.py](../computations/verify_level_two_mixed_support_pair_collapse.py)
uses only the standard library and verifies exactly:

* the (1+6+10=17) labelled supports and all (289) ordered pairs;
* a dead-edge contradiction for each of the (16) nonempty supports;
* the rank-six normalized mixed-triangle system;
* the formal identity
  (det(XJY^{\mathsf T})=-\det(X)\det(Y));
* all (20) pure-triangle cover equations; and
* the leading coefficient (det M) in (8).

The checker passes normal, optimized, and isolated Python. The remaining
frontier consists of the closed cover (7) on the four-cycle-generic chart
and adjacent charts where a nominally live mixed edge has singular residual
block. Those are the parts of the argument that can transfer to the singular
residual branch; the already-closed fully invertible R2 locus is not being
reopened.
