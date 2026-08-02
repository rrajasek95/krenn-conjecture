# Factor-complete active sites close the double-live one-column overlap

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Continue in the rank-\(55\), kernel-equals-gauges
\(3I+1R+2Z\) one-column branch with

\[
 P_t=0,\qquad Q_t\ne0,\qquad
 B_4=M_{t4}\ne0,\qquad B_5=M_{t5}\ne0.              \tag{1}
\]

At each zero site, L1 permits inactivity, active P/V data, or active Q/U
data. This note closes every chart containing an active Q/U zero. It also
closes a P/V chart whenever the live block at one active site has the same
physical zero-side factor as its three \(I\)-spokes. The proof uses no
terminal complementary-purity, R2, spoke-uniformity, or mixed-localization
hypothesis.

The exact remaining L1 geometry is isolated: each endpoint is inactive or
P/V, and every active P/V site's live block is misaligned with its
physical zero factor. For the double-P/V case, the full three-shore
matching and endpoint-star decompositions are recorded below.

## L1 active-type classification

At a zero \(z\), the active forms are

\[
\begin{array}{lll}
\text{P/V:}&
 U_z^s=0,\quad V_z^s=f_sv_z,&
 M_{iz}=m_iP_iv_z^{\mathsf T},\\[1mm]
\text{Q/U:}&
 V_z^s=0,\quad U_z^s=f_su_z,&
 M_{iz}=m_iQ_iu_z^{\mathsf T}.
\end{array}                                           \tag{2}
\]

Because \(P_t=0\), the P/V selected side on \(tz\) vanishes and L1 puts
no restriction on \(B_z=M_{tz}\). For active Q/U data, however,
\(Q_tu_z^{\mathsf T}\ne0\), and the live-edge L1 equation forces

\[
                         B_z=\beta_zQ_tu_z^{\mathsf T},
                         \qquad\beta_z\ne0.           \tag{3}
\]

Thus a Q/U site is automatically **factor-complete**: every nonzero
residual block incident with \(z\) has physical \(u_z\) as its \(z\)-side
factor. A P/V site is factor-complete precisely in the additional subcase

\[
                         B_z=b_zv_z^{\mathsf T}       \tag{4}
\]

for some nonzero physical vector \(b_z\) at \(t\). Its \(I\)-spokes
already have the same \(v_z\) factor.

## A factor-complete site fixes every L0 shore

Fix a factor-complete active site \(z\). The selected zero-zero equation
forces \(M_{45}=0\). In every perfect matching, \(z\) therefore meets
either \(I\), \(t\), or the other zero. The first nine matchings use an
\(I\)-spoke and supply the active physical factor, the next three use the
factor-complete \(tz\) block and supply it again, and the last three use
\(M_{45}=0\). Hence, for a tensor \(H'\),

\[
                         H=\Psi(M)=\xi_z\otimes H',
 \qquad
 \xi_z=
 \begin{cases}
   u_z,&\text{Q/U},\\
   v_z,&\text{aligned P/V}.
 \end{cases}                                         \tag{5}
\]

The same factor occurs in every endpoint derivative. If a tangent edge
is not incident with \(z\), its four-site cofactor still contains \(z\);
each nonzero cofactor matching uses an \(I\)- or \(t\)-edge at \(z\), so
it supplies \(\xi_z\). If a tangent is incident with \(z\), the active
normal forms (2) make its \(z\)-side endpoint factor a multiple of
\(\xi_z\). This includes the zero-zero interaction in opposite-type
charts. Therefore, for all endpoint colours,

\[
                         d\Psi_M(N^{su})=\xi_z\otimes K_{su}.     \tag{6}
\]

The two pure L0 equations would now give

\[
 e_s^{\otimes6}=W_{ss}H+d\Psi_M(N^{ss})
                =\xi_z\otimes L_s,\qquad s=0,1.      \tag{7}
\]

They force \(\xi_z\parallel e_0\) and
\(\xi_z\parallel e_1\), impossible. This closes every active-Q/U chart
and every aligned-live P/V subcase.

## Exact residual type map

Label a zero endpoint by I, P, or Q according as it is inactive, P/V, or
Q/U. Of the nine ordered type pairs, the five containing Q are closed by
(3)--(7). The remaining type pairs are

\[
                         (\mathrm I,\mathrm I),\quad
                         (\mathrm I,\mathrm P),\quad
                         (\mathrm P,\mathrm I),\quad
                         (\mathrm P,\mathrm P).       \tag{8}
\]

For every P entry, (4) must fail. Thus its live block has no common
physical zero-side factor with its \(I\)-spokes. These are exact necessary
conditions for a double-live survivor at the L1/fixed-shore stage; no L0
existence is claimed.

## Three shores in the double-P/V residue

For the final pair in (8), let the active physical factors be \(v_4,v_5\).
All twelve potentially nonzero matchings fall into three physical shore
classes:

\[
\begin{aligned}
 H={}&B_4\otimes v_5\otimes C_4
      +B_5\otimes v_4\otimes C_5\\
    &+(Q_t\otimes v_4\otimes v_5)\otimes K.          \tag{9}
\end{aligned}
\]

The first three matchings use \(t4\), the next three use \(t5\), and six
pair \(t,4,5\) to the three vertices of \(I\). The remaining three use
\(M_{45}=0\).

Let \(T_z\) denote the literal tangent supported on \(tz\), and let
\(S_z\) have blocks \(P_iv_z^{\mathsf T}\) on \(iz\). The derivatives
occupy the same three shores:

\[
\begin{array}{c|ccc}
 &B_4v_5&B_5v_4&Q_tv_4v_5\\ \hline
d\Psi(T_4)&3&0&0\\
d\Psi(T_5)&0&3&0\\
d\Psi(S_4)&0&3&6\\
d\Psi(S_5)&3&0&6.
\end{array}                                           \tag{10}
\]

Equation (10) is a term census, not a linear-independence assertion. It
identifies the exact physical components that a subsequent mixed/pure L0
argument must control and does not assume either live block is rank one.

For \(Q_t=0,\ P_t\ne0\), interchange

\[
                  (P,U,v)\longleftrightarrow(Q,V,u).
\]

The standard-library checker
[verify_level_two_three_invertible_one_column_double_live_factor_complete_closure.py](../computations/verify_level_two_three_invertible_one_column_double_live_factor_complete_closure.py)
audits the nine-chart type grid, the L1 forced and unrestricted live
blocks, all factor-complete base matchings and tangent cofactors, the
pure-shore determinant, the full \(3+3+6+3\) double-P/V matching census,
the four star-derivative shore rows, and the symmetric selected-family
dictionary.
