# The complementary-purity one-column charts are empty

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

The two terminal charts isolated by
[the one-column boundary reduction](level-two-three-invertible-one-column-t-boundary.md)
are impossible under that theorem's invertible-spoke hypotheses. In fact,
the pure six-site matching tensor alone gives the contradiction; the
complementary pure five-site cofactor is not needed.

Consequently the one-column rank-one-site boundary is closed when each zero
site has an invertible spoke to the invertible triangle. The companion
[singular-overlap theorem](level-two-three-invertible-one-column-singular-overlap.md)
removes the invertibility hypothesis from the terminal complementary-purity
charts: an independent cofactor shore gives the same contradiction, while
two dependent shores have differential rank at most 49.

## Injectivity of the triangle cofactor map

Treat the chart \(P_t=0, Q_t\ne0\); the other chart is symmetric. Let \(s\)
be the colour in which the six-site tensor is pure and let \(r=1-s\). The
boundary reduction gives

\[
                 Q_t=q e_r,\qquad \Psi(M)=h e_s^{\otimes6},
                 \qquad qh\ne0.                              \tag{1}
\]

Normalize the three selected invertible matrices on
\(I=\{0,1,2\}\). Up to a nonzero common scalar, the triangle blocks are

\[
                         M_{ij}=J,
 \qquad J=\begin{pmatrix}0&1\\1&0\end{pmatrix}.             \tag{2}
\]

For \(z\in\{4,5\}\) and a colour \(a\), define the three-site tensor

\[
 L_z^a(x_0,x_1,x_2)=
 \sum_{i\in I}M_{iz}(x_i,a)M_{jk}(x_j,x_k),
 \qquad \{i,j,k\}=I.                                      \tag{3}
\]

The linear map from the three spoke columns \(u_i=M_{iz}(-,a)\) to
\(L_z^a\) is injective. Indeed, its weight-one coefficients are

\[
 L(001)=u_0(0)+u_1(0),\quad
 L(010)=u_0(0)+u_2(0),\quad
 L(100)=u_1(0)+u_2(0),                                  \tag{4}
\]

and the three weight-two coefficients give the identical system for the
colour-one entries. Since the displayed `3 x 3` matrix is invertible in
characteristic zero, all six spoke coordinates are recovered.

If one block \(M_{iz}\) is invertible, its two \(z\)-colour columns are
independent in the direct sum of the three spoke spaces. Injectivity then
gives

\[
                         L_z^0,L_z^1\text{ independent}.          \tag{5}
\]

Thus the two invertible-spoke witnesses assumed in the boundary reduction
imply that \(L_4^s,L_4^r\) are independent and \(L_5^r\ne0\).

## Three zero corners kill the fourth

Evaluate the matching tensor at colour \(s\) on site \(t\). Every matching
using an \(I\)-to-\(t\) edge vanishes because those blocks have the factor
\(Q_t(s)=0\). The block \(M_{45}\) is zero by the nonzero generic-kernel
multiplier \(-2\tau\). The only remaining matchings pair \(t\) to one zero
site and use one triangle edge plus one spoke at the other zero site.

Write

\[
 x_a=M_{t4}(s,a),\qquad y_b=M_{t5}(s,b).
\]

The four \(Z\)-shore slices of the \(t=s\) tensor are exactly

\[
                         T_{ab}=x_aL_5^b+y_bL_4^a.                 \tag{6}
\]

Purity in (1) requires

\[
                         T_{sr}=T_{rs}=T_{rr}=0,
 \qquad T_{ss}\ne0.                                             \tag{7}
\]

The first and third zero equations in (7) are

\[
 x_sL_5^r+y_rL_4^s=0,\qquad
 x_rL_5^r+y_rL_4^r=0.                                            \tag{8}
\]

If \(y_r\ne0\), both independent tensors \(L_4^s,L_4^r\) would be
proportional to the same nonzero tensor \(L_5^r\), a contradiction. Hence
\(y_r=0\). Since \(L_5^r\ne0\), equations (8) then give \(x_s=x_r=0\).
The remaining zero equation \(T_{rs}=0\), together with \(L_4^r\ne0\),
gives \(y_s=0\). Formula (6) now gives \(T_{ss}=0\), contradicting (7).

This proof never uses the additional terminal condition
\(C_t=c e_r^{\otimes5}\). It excludes both labelled scalar charts at once.
If \(Q_t=0, P_t\ne0\), interchange the selected column families; the
same \(t=s\) matching expansion and contradiction apply verbatim.

## Exact audit

The standard-library checker
[verify_level_two_three_invertible_one_column_pure_tensor_obstruction.py](../computations/verify_level_two_three_invertible_one_column_pure_tensor_obstruction.py)
verifies all 64 formal matching identities in (6), computes the triangle
cofactor map's exact rank six and its explicit inverse, and audits the two
cases in the forbidden-corner implication. It passes normal, optimized, and
isolated Python.
