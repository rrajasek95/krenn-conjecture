# A single live uniform cross does not rescue the one-column boundary

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Consider the rank-\(55\), kernel-equals-gauges \(3I+1R+2Z\) branch with
exactly one selected column at \(t\). This note closes the following
pre-terminal live-cross subcase:

* \(P_t=0,\ Q_t\ne0\);
* exactly one \(t\)-to-zero block \(B=M_{tz}\) is nonzero;
* \(z\) has one active P/V endpoint family whose three \(I\)-spoke
  multiples are equal; and
* the other zero \(w\) is endpoint-inactive and \(M_{tw}=0\).

No terminal complementary-purity hypothesis and no R2 conclusion from a
normalized selected basis is used. The symmetric \(Q_t=0\), active-Q/U
case follows by interchanging the selected families. Nonuniform live
crosses and configurations with two active/live zero sites remain outside
this theorem.

## Two stars reduce to the live edge

L1 alignment gives

\[
 U_i^s=a_sP_i,\quad V_i^s=b_sQ_i,\qquad
 U_t^s=0,\quad V_t^s=d_sQ_t.
\]

Let

\[
 (S_t)_{it}=P_iQ_t^{\mathsf T}=2\tau M_{it}.
\]

At the active P/V zero, write

\[
 U_z^s=0,\qquad V_z^s=f_sv_z,\qquad
 M_{iz}=mP_iv_z^{\mathsf T}\quad(i\in I),             \tag{1}
\]

with \(m\ne0\). Define \((S_z)_{iz}=P_iv_z^{\mathsf T}\), and let \(T\)
be the tangent supported only on \(tz\), with \(T_{tz}=B\).

Because \(M_{tw}=M_{zw}=0\), the two exact radial identities are

\[
\begin{aligned}
 S_t&=2\tau G(e_t)-2\tau T,\\
 S_z&=m^{-1}G(e_z)-m^{-1}T.                           \tag{2}
\end{aligned}
\]

Thus, modulo generalized gauges, every endpoint slice has just one
possible correction,

\[
                 -a_s\eta_uT,\qquad
 \eta_u=2\tau(d_u-b_u)+f_u/m.                         \tag{3}
\]

No nonzero multiple of \(T\) is a generalized gauge. Indeed, vanishing on
the invertible \(I\)-triangle, the nonzero \(I\)-to-\(t\) blocks, and the
nonzero \(I\)-to-\(z\) blocks forces all vertex weights at \(I,t,z\) to
zero; the live \(tz\) block then kills the coefficient of \(T\).

The two mixed target-zero slices consequently give

\[
                         a_0\eta_1=a_1\eta_0=0.       \tag{4}
\]

If both pure coefficients \(a_s\eta_s\) vanish, the two pure targets are
collinear with \(H=\Psi(M)\), which is impossible. The only remaining
zero patterns have a colour \(s\) with

\[
 a_s=0,\quad \eta_s=0,\qquad
 a_k\ne0,\quad\eta_k\ne0,\qquad k=1-s.               \tag{5}
\]

The \(ss\) pure equation then forces

\[
                         H=h\,e_s^{\otimes6},\qquad h\ne0.       \tag{6}
\]

## The first pure flattening isolates \(B\)

The differential of the literal edge tangent factors as

\[
                         d\Psi_M(T)=B\otimes C,        \tag{7}
\]

where \(C\) is the four-site matching tensor on
\(R\setminus\{t,z\}=I\sqcup\{w\}\).

The pure-\(k\) equation is

\[
 e_k^{\otimes6}=\kappa H-a_k\eta_k\,B\otimes C.       \tag{8}
\]

Across the physical cut \(\{t,z\}\mid(I\sqcup\{w\})\), the correction has
rank one. The pure \(2\times2\) minor forces \(\kappa=0\), and singleton
outer-product support gives

\[
                 B=\beta E_{kk},\qquad
                 C=\gamma e_k^{\otimes4},\qquad
                 -a_k\eta_k\beta\gamma=1.             \tag{9}
\]

## The full matching tensor gives a second, incompatible flattening

Every nonzero perfect matching has one of two forms.

First, it uses \(tz\), contributing \(B\otimes C\). Otherwise \(t\) and
\(z\) must meet two distinct vertices of \(I\), while the remaining
\(I\)-vertex meets \(w\). Since

\[
 M_{it}=(2\tau)^{-1}P_iQ_t^{\mathsf T},\qquad
 M_{jz}=mP_jv_z^{\mathsf T},
\]

all six terms of the second kind share the physical factor
\(Q_t\otimes v_z\). Hence, for a four-site tensor \(K\),

\[
                         H=B\otimes C+
                           (Q_t\otimes v_z)\otimes K. \tag{10}
\]

Equations (6) and (9) turn (10) into

\[
 (Q_t\otimes v_z)\otimes K
   =h\,e_s^{\otimes6}-\beta\gamma e_k^{\otimes6}.     \tag{11}
\]

The left side has rank at most one across the same physical shore cut.
The right side has rank two: its pure \(2\times2\) minor is, up to sign,
\(h\beta\gamma\ne0\). This contradiction closes the subcase.

The standard-library checker
[verify_level_two_three_invertible_one_column_single_live_uniform_cross_closure.py](../computations/verify_level_two_three_invertible_one_column_single_live_uniform_cross_closure.py)
audits the two radial identities on all residual edges, the exact
single-edge support system, every scalar zero pattern, both physical
flattening determinants, and the complete \(3+6+6\) matching
decomposition.
