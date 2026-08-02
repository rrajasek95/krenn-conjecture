# A dead \(t\)-to-\(Z\) star closes the one-column/singular-cross overlap

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Work in the rank-\(55\), kernel-equals-gauges \(3I+1R+2Z\) branch with

\[
 \nu=(\tau,\tau,\tau,\tau,-\tau,-\tau),\qquad\tau\ne0,
\]

and suppose exactly one selected column at the rank-one site \(t\) vanishes.
If both residual \(t\)-to-zero blocks vanish, then no L1/L0 completion
exists, even when either zero site lacks an invertible spoke to the
invertible triangle and retains an active common-factor endpoint family.

This closes a pre-terminal double-boundary subcase. It does not assume the
complementary-purity terminal conditions from the separate one-column
reduction, and it makes no R2 inference from a normalized selected basis.
The live \(t\)-to-\(Z\) overlap remains outside this note.

## The exceptional \(t\)-star is radial

Treat

\[
                         P_t=0,\qquad Q_t\ne0
\]

and assume

\[
                         M_{t4}=M_{t5}=0.             \tag{1}
\]

L1 alignment on \(I=\{0,1,2\}\) gives

\[
 U_i^s=a_sP_i,\quad V_i^s=b_sQ_i,\qquad
 U_t^s=0,\quad V_t^s=d_sQ_t.
\]

The exceptional packet \(S_t\) has

\[
 (S_t)_{it}=P_iQ_t^{\mathsf T}=2\tau M_{it}.
\]

Because of (1), it is exactly \(2\tau\) times the radial generalized gauge
at \(t\). Thus the free scalars \(d_s-b_s\) contribute only generalized
gauges and can be removed from every L0 slice.

## Active zero sites have only P/V type

At a zero site \(z\), an active Q/U family would have

\[
 U_z^s=d_{zs}u_z\ne0.
\]

Its \(t\)-to-\(z\) L1 equation would read

\[
 Q_t(U_z^s)^{\mathsf T}=\rho_{tz}^sM_{tz}=0,
\]

impossible because both factors on the left are nonzero. Hence every active
zero site has the covariant P/V form

\[
 U_z^s=0,\qquad V_z^s=d_{zs}v_z,\qquad
 M_{iz}=m_{iz}P_iv_z^{\mathsf T}\quad(i\in I),        \tag{2}
\]

with \(v_z\ne0\) and every \(m_{iz}\ne0\). Inactive zero sites contribute no
endpoint star and require no spoke-rank hypothesis.

Define

\[
 (S_z)_{iz}=P_iv_z^{\mathsf T},\qquad
 (S_z)_{ru}=0\quad\text{otherwise}.                  \tag{3}
\]

If the three multiples \(m_{iz}\) are equal to \(m_z\), then

\[
                         m_zS_z=G(e_z),               \tag{4}
\]

because (1) and \(M_{45}=0\) kill the two other incident blocks. Uniform
active zero-stars are therefore radial generalized gauges.

## Mixed L0 kills every nonuniform star

After removing the aligned core gauge, the radial \(t\)-star, and all
uniform zero-stars, the remaining endpoint slice is

\[
                 \sum_{z\in A}a_sd_{zu}S_z,          \tag{5}
\]

where \(A\) is the set of nonuniform active zero sites.

For a mixed target-zero slice, (5) must be a generalized gauge
\(G(\lambda)\). Its vanishing on the invertible \(I\)-triangle and the
nonzero \(I\)-to-\(t\) blocks forces

\[
                 \lambda_0=\lambda_1=\lambda_2=\lambda_t=0.
\]

On the three \(I\)-to-\(z\) blocks, writing \(q_z=a_sd_{zu}\), equality
with \(G(\lambda)\) gives

\[
                         q_z=\lambda_zm_{iz}\quad(i\in I).       \tag{6}
\]

Since the three multiples at a site in \(A\) are not all equal, (6) forces
\(q_z=\lambda_z=0\). The two mixed slices therefore impose, independently
at every nonuniform site,

\[
                         a_0d_{z1}=a_1d_{z0}=0.       \tag{7}
\]

Consequently nongauge pure corrections occur in at most one physical
endpoint colour \(k\). If there is no such correction, both pure targets
would be collinear with \(H=\Psi(M)\), which is impossible. Otherwise the
other pure slice, \(r=1-k\), forces

\[
                         H=h\,e_r^{\otimes6},\qquad h\ne0.       \tag{8}
\]

## The remaining pure correction has physical common factors

For one active P/V zero,

\[
                         d\Psi_M(S_z)=v_z\otimes C_z.
\]

With two active P/V zeros, every nonzero derivative term from either star
contains both factors \(v_4,v_5\): the tangent supplies one, while
\(M_{45}=0\) and (1) force the other zero to meet an \(I\)-vertex in the
cofactor. This remains true if one active star is uniform and removed
modulo gauges; its residual spoke blocks still supply its physical factor.
Thus the full pure-\(k\) correction has rank one across the cut separating
all active zeros from the other residual sites.

The physical \(2\times2\) pure-coordinate minor then kills the coefficient
of \(H\) in that equation. Singleton outer-product support forces every
active zero factor occurring in the correction to equal the physical
coordinate \(e_k\).

Choose a nonuniform active zero \(z\). At the all-\(r\) word in (8), every
edge incident with \(z\) vanishes: an \(I\)-edge contains
\(v_z(r)=0\), the \(t\)-edge vanishes by (1), and \(M_{45}=0\). Hence every
perfect matching term is zero, contradicting \(h\ne0\).

For \(Q_t=0,\ P_t\ne0\), interchange

\[
                         (P,U,a)\longleftrightarrow(Q,V,b).
\]

The standard-library checker
[verify_level_two_three_invertible_one_column_dead_tz_common_factor_closure.py](../computations/verify_level_two_three_invertible_one_column_dead_tz_common_factor_closure.py)
audits the L1 type exclusion, both radial-gauge identities, mixed
generalized-gauge rigidity, the nonuniform localization identities, all
scalar support patterns, every nonzero common-factor derivative term, the
physical pure flattening, the complementary matching zeros, and the
symmetric P/Q dictionary.
