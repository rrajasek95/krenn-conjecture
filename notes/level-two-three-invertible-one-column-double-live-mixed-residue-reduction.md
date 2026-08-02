# Mixed L0 closes the inactive double-live chart and isolates the P/V residue

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Continue from the
[double-live factor-complete closure](level-two-three-invertible-one-column-double-live-factor-complete-closure.md)
with

\[
 P_t=0,\quad Q_t\ne0,\quad M_{t4}\ne0,\quad M_{t5}\ne0.
\]

Each zero now has type I (endpoint-inactive) or P (active P/V), and every
P site's live block is misaligned with its physical zero factor. This note
derives the exact generalized-gauge quotient seen by mixed L0 for all four
type pairs. It closes the \((\mathrm I,\mathrm I)\) chart completely and
isolates the scalar and three-shore tensor survivors for the P-containing
charts. No L0 existence is claimed for those survivors.

## Endpoint packets and the exact gauge equations

Put \(T_z\) for the literal tangent supported on \(tz\), and for each
active P site put

\[
 (S_z)_{iz}=P_iv_z^{\mathsf T}\quad(i\in I).
\]

The exceptional \(t\)-star satisfies

\[
                 S_t=2\tau G(e_t)-2\tau(T_4+T_5).    \tag{1}
\]

After removing the aligned core gauge and using (1), every endpoint packet
has residual class

\[
 R_u=\sum_{z\in A} f_{zu}S_z-c_u(T_4+T_5),
 \qquad c_u=2\tau(d_u-b_u),                          \tag{2}
\]

multiplied by \(a_s\), where \(A\) is the set of active P sites.

Consider a generalized-gauge relation

\[
             \sum_{z\in A}q_zS_z+r(T_4+T_5)=G(\lambda).           \tag{3}
\]

The invertible \(I\)-triangle and the nonzero \(I\)-to-\(t\) blocks force
\(\lambda_i=\lambda_t=0\). The two live \(tZ\) blocks then give

\[
                         \lambda_4=\lambda_5=r.       \tag{4}
\]

At an active P site,

\[
                         q_z=r\,m_{iz}\quad(i\in I).  \tag{5}
\]

Thus either \(r=q_z=0\), or its three spoke multiples are uniform. The
exact pair certificate is

\[
 m_j(rm_i-q_z)-m_i(rm_j-q_z)=q_z(m_i-m_j).           \tag{6}
\]

At an inactive site, (3) instead gives

\[
                         rM_{iz}=0\quad(i\in I).      \tag{7}
\]

Consequently a nonzero relation exists if and only if:

* every active P spoke triple is uniform; and
* every inactive zero has all three \(I\)-spokes equal to zero.

In that case the relation is the radial identity

\[
 \sum_{z\in A}m_zS_z+T_4+T_5
                         =G(e_4+e_5),                \tag{8}
\]

where an inactive site contributes only its radial \(T_z\). If either
condition fails, the displayed tangents are independent modulo generalized
gauges.

## Mixed L0 leaves one pure colour

Let \([R_u]\) denote the class of (2) in this quotient. The two mixed
target-zero equations give

\[
                         a_0[R_1]=a_1[R_0]=0.         \tag{9}
\]

If both pure classes \(a_s[R_s]\) vanish, the two pure targets are
collinear with \(H=\Psi(M)\), which is impossible. Therefore every
survivor has complementary colours \(s,k=1-s\) with

\[
 a_s[R_s]=0,\qquad a_k[R_k]\ne0,\qquad
                         H=h\,e_s^{\otimes6}.        \tag{10}
\]

This is an exact support statement, independent of the dimension of the
tangent quotient. In the radial case, (8) gives the corresponding scalar
conditions. For example, with two uniform active sites,

\[
 [R_u]=-\left(c_u+\frac{f_{4u}}{m_4}\right)[T_4]
       -\left(c_u+\frac{f_{5u}}{m_5}\right)[T_5].     \tag{11}
\]

## The inactive-inactive chart reaches the terminal theorem

If both sites are inactive and all six \(I\)-spokes vanish, then
\(T_4+T_5=G(e_4+e_5)\). Every residual packet is a generalized gauge, so
the two pure targets contradict collinearity.

Otherwise \(T_4+T_5\) is nongauge, and (9)--(10) give one of the two usual
one-column scalar charts. Before the radial rewrite, the surviving pure
correction is a nonzero multiple of

\[
                         d\Psi_M(S_t)=Q_t\otimes C_t.             \tag{12}
\]

The \(t\)-flattening of the other pure equation kills its \(H\)
coefficient and forces, with nonzero scalars,

\[
 Q_t=q e_k,\qquad C_t=c e_k^{\otimes5},\qquad
                         H=h e_s^{\otimes6}.          \tag{13}
\]

These are exactly the hypotheses of the
[terminal singular-overlap theorem](level-two-three-invertible-one-column-singular-overlap.md).
That theorem needs no invertible zero spoke: independent cofactor shores
contradict the pure tensor, while two dependent shores have
\(\operatorname{rank}d\Psi_M\le49\). Thus the double-live
\((\mathrm I,\mathrm I)\) chart is closed.

## Exact tensor survivor with two P/V sites

For the \((\mathrm P,\mathrm P)\) chart, the
[three-shore decomposition](level-two-three-invertible-one-column-double-live-factor-complete-closure.md)
and (2) give the following exact source map for the sole possible pure
correction:

\[
\begin{array}{c|cc}
\text{physical shore}&\text{sources}&\text{term counts}\\ \hline
B_4v_5&-c\,T_4,\ f_5S_5&3+3\\
B_5v_4&-c\,T_5,\ f_4S_4&3+3\\
Q_tv_4v_5&f_4S_4,\ f_5S_5&6+6.
\end{array}                                           \tag{14}
\]

Thus mixed L0 does not by itself kill the three physical components
separately: it confines their entire combination to one endpoint colour
and imposes

\[
 e_k^{\otimes6}=\kappa h e_s^{\otimes6}+d\Psi_M(R_k).             \tag{15}
\]

Equations (10), (14), and (15), together with the misalignment of both
\(B_z\), are the exact remaining scalar/tensor survivor conditions for
this chart. The one-P charts use the same quotient equations (3)--(10)
with one \(S_z\) omitted. No flattening independence among the three rows
of (14) is asserted.

For \(Q_t=0,\ P_t\ne0\), interchange

\[
                         (P,U,a)\longleftrightarrow(Q,V,b).
\]

The standard-library checker
[verify_level_two_three_invertible_one_column_double_live_mixed_residue_reduction.py](../computations/verify_level_two_three_invertible_one_column_double_live_mixed_residue_reduction.py)
audits the exceptional-star identity, localization certificates, all
sixteen uniform/zero-spoke cases across the four I/P type pairs, the exact
mixed scalar census, the terminal flattening and imported covariant
terminal closure, and every source and term count in (14).
