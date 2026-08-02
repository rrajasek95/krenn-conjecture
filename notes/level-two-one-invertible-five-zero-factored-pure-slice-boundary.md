# The (1I+5Z) frontier reaches a factored pure L0 slice

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and exact scope

The all-zero-potential (1I+5Z) component contains an exact integral
residual packet (M) with

\[
 \operatorname{rank}d\Psi_M=55,
 \qquad \operatorname{rank}(d\Psi_M)_{\rm mixed}=53,             \tag{1}
\]

all selected generic-kernel and residual-R2 alternatives, and a genuine
factored endpoint-star preimage of a pure L0 target. In fact, the same
residual packet admits two separate endpoint-star assignments:

\[
 (T_{00},T_{01},T_{10},T_{11})
   =(e_{0^6},0,0,0),                                            \tag{2}
\]

and

\[
 (T_{00},T_{01},T_{10},T_{11})
   =(0,0,0,e_{1^6}).                                            \tag{3}
\]

Thus each pure target is individually attainable by physical shared
endpoint stars while both mixed slices vanish.

The assignments in (2) and (3) are **different assignments**. This is not
a simultaneous four-slice L0 completion. The committed
[sharp-factor obstruction](level-two-l0-sharp-factor-obstruction.md)
proves that no endpoint stars realize both pure targets and both mixed
zeros at once for this residual packet. The result therefore locates a
strict boundary: individual factored pure slices, even together with
rank (55), selected R2, and vanishing mixed slices, do not imply the
required shared four-slice completion.

A separate
[minimal gauge-coupled family](level-two-one-invertible-minimal-gauge-coupled-l0-family.md)
does realize both pure targets and both mixed zeros with one shared
endpoint-star assignment, but its differential rank is identically 38.
The
[six-zero rebinding](level-two-zero-invertible-six-zero-factored-pure-slice-boundary.md)
also retains the two separate rank-\(55\) factored pure assignments.

## A different exact residual packet

Use the packet `SHARP_M` from the universal tangent-incidence sharpness
calculation, rather than the residual packet in the preceding
[(1I+5Z) linear-incidence survivor](level-two-one-invertible-five-zero-l0-incidence-survivor.md).
The two packets differ in (47) of their (60) binary residual cells.
The sharp packet was constructed so that its four-site cofactors satisfy

\[
 \Psi(M|_{\{2,3,4,5\}})=e_{0^4},
 \qquad
 \Psi(M|_{\{0,1,2,3\}})=e_{1^4}.                               \tag{4}
\]

Consequently the tangent cells

\[
 K^{00}_{01}=E_{00},\qquad K^{11}_{45}=E_{11}                  \tag{5}
\]

obey

\[
 d\Psi_M(K^{00})=e_{0^6},qquad
 d\Psi_M(K^{11})=e_{1^6}.                                    \tag{6}
\]

The exact ranks over

\[
 \mathbf Q,\quad \mathbf F_{101},\quad
 \mathbf F_{32003},\quad \mathbf F_{1000003}
\]

are

\[
\begin{array}{c|c}
\text{matrix}&\text{rank over all four fields}\\ \hline
D=d\Psi_M&55\\
D_{\rm mixed}&53\\
[D\mid e_{0^6}]&55\\
[D\mid e_{1^6}]&55\\
[D\mid e_{0^6}\mid e_{1^6}]&55.
\end{array}                                                     \tag{7}
\]

Its five trace-zero vertex gauges are independent. Since the differential
nullity is (60-55=5), these gauges are the entire kernel.

## Literal endpoint-star factorizations

Let (p,q) be the two endpoint sites and write the binary endpoint rows as

\[
 U_r^s(i)=A_{rp}[i,s],\qquad V_r^t(i)=A_{rq}[i,t].               \tag{8}
\]

For (2), set

\[
 U_0^0=e_0,qquad V_1^0=e_0,                                   \tag{9}
\]

and set every other binary endpoint row and the direct endpoint block
(W) to zero. The shared-star tangent

\[
 N_{ru}^{st}
 =U_r^s(V_u^t)^{\mathsf T}+V_r^t(U_u^s)^{\mathsf T}             \tag{10}
\]

then has the single nonzero cell (N_{01}^{00}=E_{00}). Equations
(4)--(6) give (T_{00}=e_{0^6}), while the absent colour-one endpoint
rows make (T_{01}=T_{10}=T_{11}=0).

For (3), instead set

\[
 U_4^1=e_1,qquad V_5^1=e_1,                                   \tag{11}
\]

with all other rows and (W) zero. Now the only nonzero tangent cell is
(N_{45}^{11}=E_{11}), giving (T_{11}=e_{1^6}) and the other three
slices zero.

These are literal eight-site matching calculations, not merely cut-rank
or differential-image tests. All (105) perfect matchings are summed for
each of the (4\cdot64=256) binary endpoint slices in each assignment.

## Rebinding to the selected (1I+5Z) chart and R2

Set

\[
 X_0=I_2,qquad X_1=\cdots=X_5=0,qquad
 \nu_0=\cdots=\nu_5=0.                                       \tag{12}
\]

Every residual edge has a zero endpoint matrix, so all (60)
generic-kernel identities hold trivially. The selected tangent and direct
selected value vanish, hence all (64) selected level-two rows vanish.
The literal rare/rare endpoint slice is also zero for both assignments:
both endpoint stars would have to meet the sole nonzero selected residual
site (0), which no perfect matching permits.

At the invertible root (0), the residual blocks

\[
 M_{03}=\begin{pmatrix}1&0\\2&0\end{pmatrix},
 \qquad
 M_{02}=\begin{pmatrix}0&0\\0&1\end{pmatrix}                  \tag{13}
\]

are pure in output columns (0) and (1), respectively, on distinct
neighbours. Both complementary four-site cofactors are nonzero. They are
therefore literal residual R2 witnesses. At roots (1,\ldots,5), the
selected rare endpoint columns vanish and the preservation alternative
holds.

## Exact audit

The standard-library checker
[verify_level_two_one_invertible_five_zero_factored_pure_slice_survivor.py](../computations/verify_level_two_one_invertible_five_zero_factored_pure_slice_survivor.py)

- reconstructs the exact sharp packet and proves it differs from the old
  one-invertible incidence packet;
- verifies (1), (6), and every rank in (7) over the rationals and three
  prime fields;
- proves that the five independent vertex gauges fill the differential
  kernel;
- checks the (1I+5Z) selected block, all generic-kernel identities, all
  selected rows, and the six residual-R2 alternatives;
- constructs both endpoint-star assignments (9) and (11), compares the
  factored tangent formula with a direct eight-site matching sum on all
  (512) tested binary slices, and checks the selected rare/rare slices;
  and
- pins the four residual blocks used by the existing simultaneous
  sharp-factor obstruction, without rerunning its external Singular
  certificate.

It uses only the Python standard library and remains live under normal,
optimized, and isolated Python.
