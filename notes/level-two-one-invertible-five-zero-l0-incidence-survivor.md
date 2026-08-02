# A \(1I+5Z\) packet survives linear L0 incidence

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and exact scope

The all-zero-potential \(1I+5Z\) component contains an exact selected
level-two packet satisfying

\[
 \operatorname{rank}d\Psi_M=55,\qquad
 e_{0^6},e_{1^6}\in\operatorname{im}d\Psi_M,                    \tag{1}
\]

together with all generic-kernel identities, all selected level-two rows,
and the six selected residual R2 alternatives. Its exact incidence ranks
over
\(\mathbf Q,\mathbf F_{101},\mathbf F_{32003},\mathbf F_{1000003}\) are

\[
\begin{array}{c|c}
\text{matrix}&\text{rank over all four fields}\\ \hline
D=d\Psi_M&55\\
D_{\rm mixed}&53\\
[D\mid e_{0^6}]&55\\
[D\mid e_{1^6}]&55\\
[D\mid e_{0^6}\mid e_{1^6}]&55.
\end{array}                                                     \tag{2}
\]

Thus generic kernel, selected R2, differential rank, and linear L0
incidence do not close the \(1I+5Z\) zero-potential component.

This packet is not a full-source survivor. Its residual \(M\) is exactly the
packet already excluded by the
[factored pure-zero cut](level-two-two-invertible-factored-l0-cut-obstruction.md).
The new result identifies the correct hierarchy on the one-invertible
component: after linear incidence, factored endpoint-star structure or
overlap is genuinely necessary.

## Rebinding an exact residual survivor

Take the integral residual packet from the
[two-invertible linear-incidence survivor](level-two-two-invertible-l0-incidence-survivor.md).
Only its six-site binary blocks are retained. Replace all selected endpoint
data by

\[
 X_0=I_2,\qquad X_1=\cdots=X_5=0,\qquad
 \nu_0=\cdots=\nu_5=0.                                        \tag{3}
\]

Every edge has a zero endpoint matrix, so

\[
 X_uJX_v^{\mathsf T}=0=(\nu_u+\nu_v)M_{uv}.                    \tag{4}
\]

The selected tangent also vanishes: no edge has two nonzero endpoint
matrices. The direct selected value is \(-\sum_u\nu_u=0\). Consequently all
60 generic-kernel scalars and all 64 selected rows are literally zero,
while the residual differential and all ranks in (2) are unchanged.

This rebinding is possible precisely because the zero-potential component
places no condition on \(M\). It does not transport an endpoint-rank or R2
claim through a change of basis.

## Literal selected residual R2

At root 0, the two selected endpoint edges contain the rare outside colour,
so preservation of the binary pair fails. The residual packet has the
literal physical blocks

\[
 M_{02}=\begin{pmatrix}2&0\\1&0\end{pmatrix},\qquad
 M_{04}=\begin{pmatrix}0&85\\0&87\end{pmatrix}.                 \tag{5}
\]

They are supported in distinct output columns, lie on distinct neighbours,
and their complementary four-site cofactors are nonzero. Hence they give
the two R2 witnesses at the sole invertible endpoint root.

At roots \(1,\ldots,5\), both selected endpoint stars vanish. Set every
unlisted ternary cell to zero. All incident assigned residual cells then
use only the binary pair, so each of these roots satisfies the preservation
alternative. This is a direct physical-coordinate audit; no normalized
selected line is called a pure output column.

## Linear L0 survives, but the factored slice does not

For arbitrary endpoint stars and direct endpoint cell, every binary
endpoint slice has the universal form

\[
 T_{st}=W_{st}\Psi(M)+d\Psi_M(N^{st}).                          \tag{6}
\]

Euler's identity \(d\Psi_M(M)=3\Psi(M)\) puts the direct term in the same
differential image. Therefore membership of both pure targets is the exact
linear L0 incidence screen. The ranks (2) show that this packet passes it
sharply: deleting the two pure output rows lowers rank from 55 to 53, and
adjoining either or both pure coordinate vectors does not raise rank.

The screen forgets that

\[
 N^{st}_{ru}
   =U_r^s(V_u^t)^{\mathsf T}
      +V_r^t(U_u^s)^{\mathsf T}                                \tag{7}
\]

must come from two shared endpoint stars. For this exact \(M\), the
committed factored-L0 theorem solves a pure-zero preimage modulo all five
vertex gauges and proves that its
\(\{0,1\}\mid\{2,3,4,5\}\) flattening can never have rank at most two.
Thus (7) fails for the pure-zero slice even though its aggregate
differential preimage exists.

The earlier
[\(1I+5Z\) L0 obstruction](level-two-one-invertible-five-zero-l0-obstruction.md)
used a different residual packet for which neither pure target even reached
the differential image. The two results are complementary, not
contradictory.

## Exact audit

The standard-library checker
[verify_level_two_one_invertible_five_zero_l0_incidence_survivor.py](../computations/verify_level_two_one_invertible_five_zero_l0_incidence_survivor.py)

- reconstructs the exact integral residual packet and verifies endpoint
  ranks \((2,0,0,0,0,0)\), all 60 generic-kernel scalars, and all 64
  selected rows;
- rebinds and checks all \(4\cdot64=256\) universal endpoint-slice
  identities and Euler's identity;
- verifies every rank in (2) over the rationals and three prime fields;
- audits the two active physical R2 witnesses at root 0 and preservation at
  the other five roots; and
- confirms that the eight rebound free blocks are exactly those used by the
  committed factored-cut obstruction.

It passes normal, optimized, and isolated Python.
