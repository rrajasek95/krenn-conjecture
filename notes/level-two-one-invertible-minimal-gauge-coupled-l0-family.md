# A minimal gauge-coupled (1I+5Z) family completes L0 only at rank (38)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

There is a natural exact family which couples the two separate factored
pure assignments from the
[factored-pure boundary](level-two-one-invertible-five-zero-factored-pure-slice-boundary.md)
into one shared endpoint-star assignment. Every member satisfies

\[
 (T_{00},T_{01},T_{10},T_{11})
   =(e_{0^6},0,0,e_{1^6}),                                    \tag{1}
\]

and retains the all-zero-potential (1I+5Z) selected block and literal
selected residual R2. However,

\[
 \operatorname{rank}d\Psi_M=38,
 \qquad \operatorname{rank}(d\Psi_M)_{\rm mixed}=36            \tag{2}
\]

identically on the family. Thus this minimal literal-cell-plus-gauge
coupling cannot reach the required rank-(55) frontier.

This is a rigorous obstruction only for the diagonal-torus family defined
below. It does not exclude denser residual packets, endpoint stars with
additional support, non-gauge mixed kernel directions, or the full
(1I+5Z) component.

## The canonical residual packet

Write (E_{ab}=e_ae_b^{\mathsf T}). All unlisted residual blocks vanish,
and the nonzero blocks are

\[
\begin{aligned}
 M_{02}=M_{13}&=E_{11},\\
 M_{23}=M_{45}&=E_{00},\\
 M_{04}=M_{05}=M_{14}=M_{15}&=E_{01}.                         \tag{3}
\end{aligned}
\]

The two literal pure tangent cells remain

\[
 K^{00}_{01}=E_{00},\qquad K^{11}_{45}=E_{11}.                 \tag{4}
\]

Indeed, on the complements of (01) and (45), respectively,

\[
 \Psi(M|_{\{2,3,4,5\}})=E_{00}^{23}E_{00}^{45}=e_{0^4},
 \qquad
 \Psi(M|_{\{0,1,2,3\}})=E_{11}^{02}E_{11}^{13}=e_{1^4}.       \tag{5}
\]

Hence (d\Psi_M(K^{00})=e_{0^6}) and
(d\Psi_M(K^{11})=e_{1^6}).

## One shared endpoint-star assignment

Let (p,q) be the two endpoint sites and use

\[
 N_{ru}^{st}
 =U_r^s(V_u^t)^{\mathsf T}+V_r^t(U_u^s)^{\mathsf T}.           \tag{6}
\]

The nonzero endpoint rows are

\[
\begin{array}{c|cc}
 &\text{first site}&\text{second site}\\ \hline
U^0&U_0^0=e_0&U_1^0=-e_0\\
V^0&V_0^0=-\frac12e_0&V_1^0=\frac12e_0\\
U^1&U_4^1=\frac12e_1&U_5^1=\frac12e_1\\
V^1&V_4^1=e_1&V_5^1=e_1.
\end{array}                                                     \tag{7}
\]

All other rows and the direct endpoint block (W) vanish. Formula (6)
gives exactly the two pure tangents in (4). For the mixed tangents, put

\[
 g=(1,-1,-1,1,0,0),qquad
 G(g)_{ru}=(g_r+g_u)M_{ru}.                                   \tag{8}
\]

The four (E_{01}) cross blocks in (3) give

\[
 N^{01}=G(g),\qquad N^{10}=-\frac14G(g).                       \tag{9}
\]

Every other nonzero block in (3) joins vertices whose (g)-weights sum
to zero. Therefore (9) holds on all (60) residual cells. Vertex gauges
lie in (ker d\Psi_M), so both mixed L0 slices vanish. Equations
(4)--(9) prove (1) using one shared set of endpoint stars.

The direct eight-site expansion agrees: summing all (105) perfect
matchings on each of the (4\cdot64=256) binary endpoint slices yields
exactly (1).

## Selected (1I+5Z) data and R2

Put the sole invertible selected matrix at site (2):

\[
 X_2=I_2,qquad X_0=X_1=X_3=X_4=X_5=0,qquad
 \nu_0=\cdots=\nu_5=0.                                      \tag{10}
\]

Every residual edge has a zero selected endpoint, so all (60)
generic-kernel identities and all (64) selected level-two rows vanish.
The selected rare/rare endpoint slice also vanishes literally, since the
two endpoint edges cannot both meet the sole selected site (2) in a
perfect matching.

At the active root (2), the oriented internal blocks

\[
 M_{23}=E_{00},\qquad M_{20}=E_{11}                            \tag{11}
\]

are pure in complementary output columns on distinct neighbours. Their
complementary four-site cofactors are nonzero. Thus they give the two
literal residual R2 witnesses. At the other five roots, the selected rare
columns vanish and the preservation alternative holds.

## The diagonal-torus family and its rank obstruction

For arbitrary nonzero scalars (x_r,y_r), set

\[
 D_r=\operatorname{diag}(x_r,y_r),\qquad
 M^D_{ru}=D_rM_{ru}D_u^{\mathsf T}.                            \tag{12}
\]

Let (P_D) scale the output coordinate indexed by
(w\in\{0,1\}^6) by

\[
 p_w=\prod_{r=0}^5 D_r(w_r,w_r),                               \tag{13}
\]

and let (Q_D) send a tangent block (K_{ru}) to
(D_rK_{ru}D_u^{\mathsf T}). Every perfect matching uses each residual
site exactly once, hence

\[
 \Psi(M^D)=P_D\Psi(M),\qquad
 d\Psi_{M^D}\circ Q_D=P_D\circ d\Psi_M.                       \tag{14}
\]

Both (P_D) and (Q_D) are invertible. Thus differential rank and
mixed-row rank are constant on the whole family and equal the exact
canonical ranks in (2). This proves the rank obstruction, rather than
merely observing rank (38) at one specialization.

The endpoint completion also transports without square roots. Put

\[
 X_*=\prod_rx_r,\qquad Y_*=\prod_ry_r,                          \tag{15}
\]

and transform the stars by

\[
 \widetilde U_r^0=X_*^{-1}D_rU_r^0,
 \quad \widetilde V_r^0=D_rV_r^0,
 \qquad
 \widetilde U_r^1=Y_*^{-1}D_rU_r^1,
 \quad \widetilde V_r^1=D_rV_r^1.                             \tag{16}
\]

The two pure outputs in (14) acquire factors (X_*) and (Y_*), which
(16) cancels. The mixed tangents remain scalar multiples of
(G(g;M^D)), so (1) persists. Diagonal transformations preserve the pure
column supports and nonvanishing cofactors in (11), hence R2 persists as
well.

## Exact audit

The standard-library checker
[verify_level_two_one_invertible_minimal_gauge_coupled_l0_family.py](../computations/verify_level_two_one_invertible_minimal_gauge_coupled_l0_family.py)

- reconstructs (3) and (7), checks both mixed gauge identities on all
  residual cells, and obtains all four outputs in (1);
- verifies (2) over the rationals and
  (mathbf F_{101},\mathbf F_{32003},\mathbf F_{1000003});
- audits the formal diagonal weight on every live differential monomial
  and all (3840) entries of (14) at a nontrivial exact rational family
  member;
- transports the endpoint stars by (16), then directly sums all (256)
  binary endpoint slices and the selected rare/rare slice;
- checks endpoint ranks ((0,0,2,0,0,0)), all generic-kernel and selected
  rows, both active internal R2 witnesses, their cofactors, and preservation
  at the remaining roots.

It passes normal, optimized, and isolated Python.
