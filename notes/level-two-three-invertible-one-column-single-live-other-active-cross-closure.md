# An active dead-side zero closes the single-live one-column overlap

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Continue in the rank-\(55\), kernel-equals-gauges
\(3I+1R+2Z\) branch with

\[
 P_t=0,\qquad Q_t\ne0,\qquad M_{tz}\ne0,\qquad M_{tw}=0.
\]

Suppose both zero endpoints \(z,w\) are active common-factor L1 types.
This note closes every such chart, including the same-type and
opposite-type combinations, all uniformity patterns of the \(I\)-spoke
multiples, and an unrestricted live block in the compatible same-type
case. No terminal complementary-purity or R2 hypothesis is used.

## L1 leaves exactly two type combinations

At the dead-side zero \(w\), active Q/U data would give

\[
 U_w^s=f_su_w,\qquad
 Q_t(U_w^s)^{\mathsf T}=\rho_sM_{tw}=0.
\]

For an active colour the left side is nonzero, a contradiction. Thus
\(w\) must have P/V form

\[
 U_w^s=0,\qquad V_w^s=g_sv_w,\qquad
 M_{iw}=n_iP_iv_w^{\mathsf T}\quad(i\in I),          \tag{1}
\]

with \(v_w\ne0\) and nonzero \(n_i\). At the live-side zero \(z\), there
are two possibilities:

\[
\begin{array}{lll}
\text{same P/V:}&
 U_z^s=0,\ V_z^s=f_sv_z,&
 M_{iz}=m_iP_iv_z^{\mathsf T},\\[1mm]
\text{opposite Q/U:}&
 V_z^s=0,\ U_z^s=f_su_z,&
 M_{iz}=m_iQ_iu_z^{\mathsf T}.
\end{array}                                           \tag{2}
\]

In the same-type case the \(tz\) L1 selected sides vanish because
\(P_t=U_z^s=0\), so \(B=M_{tz}\) is unrestricted. In the opposite case,
an active colour gives a nonzero \(Q_tu_z^{\mathsf T}\), and L1 forces

\[
                         B=\beta Q_tu_z^{\mathsf T},
                         \qquad\beta\ne0.             \tag{3}
\]

Thus the only combinations are P/V--P/V and Q/U-at-\(z\) with
P/V-at-\(w\). A Q/U family at \(w\) is impossible.

## Every matching tensor has the dead-side physical factor

The selected zero-zero equation forces \(M_{zw}=M_{45}=0\). Together
with \(M_{tw}=0\), this means every nonzero perfect matching must pair
\(w\) to an inner site. By (1), that edge supplies the same physical
factor \(v_w\). Consequently

\[
                         H=\Psi(M)=v_w\otimes H',
                                                               \tag{4}
\]

across the physical cut \(w\mid(R\setminus\{w\})\). Exactly three
matchings use \(tz\), six pair \(t,z,w\) to the three inner sites, and
six use one of the dead edges \(tw,zw\).

The factor persists for every endpoint tangent packet \(N^{su}\).
Indeed:

* if a tangent edge is not incident with \(w\), its four-site cofactor
  still contains \(w\); a nonzero cofactor matching must pair \(w\) to
  \(I\), supplying \(v_w\);
* every actual tangent on an \(iw\) edge has the form
  \(P_i v_w^{\mathsf T}\) and directly supplies \(v_w\);
* in the opposite-type chart, the additional \(zw\) endpoint tangent
  has the form \(u_zv_w^{\mathsf T}\), so it also supplies \(v_w\); and
* the \(tw\) endpoint tangent is zero.

This covers the aligned core packets, the exceptional \(t\)-star, both
zero-stars, the live-edge interaction, and the opposite-type zero-zero
interaction. Term by term,

\[
                         d\Psi_M(N^{su})=v_w\otimes K_{su}.       \tag{5}
\]

No mixed-slice localization or uniform-star reduction is needed.

## The two pure shores are incompatible

The pure L0 equations have the form

\[
 e_s^{\otimes6}=W_{ss}H+d\Psi_M(N^{ss})
                =v_w\otimes L_s,\qquad s=0,1.        \tag{6}
\]

Since both targets are nonzero, the \(w\)-shore of (6) forces

\[
                         v_w\parallel e_0,\qquad
                         v_w\parallel e_1.
\]

This is impossible because \(e_0,e_1\) are independent. Equivalently,
the \(2\times2\) flattening minor formed by the two pure \(w\)-shore
columns has determinant one, while a fixed \(v_w\)-shore has rank at
most one.

For \(Q_t=0,\ P_t\ne0\), interchange

\[
                 (P,U,v)\longleftrightarrow(Q,V,u).
\]

Then the dead-side active type is Q/U and the same fixed-shore argument
uses \(u_w\).

The standard-library checker
[verify_level_two_three_invertible_one_column_single_live_other_active_cross_closure.py](../computations/verify_level_two_three_invertible_one_column_single_live_other_active_cross_closure.py)
audits the L1 type classification, the full \(3+6+6\) base-matching
census, all thirty nonincident tangent cofactors, the incident same- and
opposite-type endpoint tangents, the physical pure-shore determinant,
and the symmetric selected-family dictionary.
