# The asymmetric one-column L1 boundary has one defect and an active-zero path closure

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Work in the dense-potential \(2I+2R+2Z\) normal form

\[
 \nu=(\tau,\tau,\tau,\tau,-\tau,-\tau),\qquad \tau\ne0,
 \qquad I=\{0,1\},\quad T=\{t,u\},\quad Z=\{4,5\}.                \tag{1}
\]

Assume \(X_0,X_1\) are invertible, \(X_t,X_u\) are nonzero of rank one,
and, after exchanging selected families if necessary,

\[
 P_t=0,\quad Q_t\ne0,\qquad P_u\ne0,\quad Q_u\ne0.              \tag{2}
\]

Suppose the rank-\(55\), kernel-equals-gauges packet has passed the
overlapping L1 equations. This note gives its exact asymmetric L1 normal
form and closes the subcase in which both zero endpoints are L1-active:

> **Active-zero path closure.** If both zero sites have a nonzero L1
> endpoint family, then
> \[
>                         \operatorname{rank}d\Psi_M\le49.       \tag{3}
> \]

Thus any rank-\(55\) survivor in this asymmetric one-column chart has at
least one L1-inactive zero site. If every inactive zero's three
full-column spokes nevertheless share a fixed nonzero right factor, the
same path bound applies, because each active zero already has such a
factor. A genuine remaining singular-cross escape must therefore contain
an inactive zero whose full-column spokes have no common right factor.

This theorem explicitly excludes the transverse chart in which both
rank-one endpoints miss a selected column. It does not claim a closure of
the inactive-zero residue.

## The two-column endpoint still kills both skew modes

Use independent local bases at sites \(0,1\) to solve the L1 system with
\(X_0=X_1=I_2\). On the edge \(01\), the P/V family has the two modes

\[
 V_0^s=b_sQ_0+x_sP_0,\qquad
 V_1^s=b_sQ_1-x_sP_1,                                  \tag{4}
\]

and the transposed Q/U family has

\[
 U_0^s=a_sP_0+y_sQ_0,\qquad
 U_1^s=a_sP_1-y_sQ_1.                                  \tag{5}
\]

The two edges from \(0,1\) to the two-column rank-one site \(u\) are
exactly the propagation system from the two-column L1 theorem.
Because \(P_u,Q_u\ne0\), they force

\[
 x_s=y_s=0,\qquad
 U_u^s=a_sP_u,\qquad V_u^s=b_sQ_u.                    \tag{6}
\]

The normalization of \(X_0,X_1\) is used only to solve this covariant
linear system. Equation (6) is translated back to the original selected
vectors; no normalized line is identified with a physical target axis.

## The one-column endpoint retains exactly one scalar

At \(t\), the P/V equations on \(0t,1t\) become

\[
                         P_i(V_t^s)^{\mathsf T}
              =d_{it}P_iQ_t^{\mathsf T}.                       \tag{7}
\]

They give one site-local scalar \(\beta_s\), independent of \(i\):

\[
                         V_t^s=\beta_sQ_t.                       \tag{8}
\]

They do not relate \(\beta_s\) to the core scalar \(b_s\), because
\(P_t=0\). The transposed equations are

\[
 Q_i(U_t^s)^{\mathsf T}+a_sP_iQ_t^{\mathsf T}
              =d'_{it}P_iQ_t^{\mathsf T},                       \tag{9}
\]

and comparison of the independent \(P_i,Q_i\) lines gives

\[
                         U_t^s=0=a_sP_t.                         \tag{10}
\]

The edge \(tu\) is compatible with arbitrary \(\beta_s\): its P/V scalar
is \(\beta_s\), while its Q/U scalar is \(a_s\). Therefore the complete
core normal form is

\[
\begin{array}{c|cc}
 r&U_r^s&V_r^s\\ \hline
 0,1,u&a_sP_r&b_sQ_r\\
 t&0&\beta_sQ_t.
\end{array}                                                       \tag{11}
\]

## An inactive-zero slice has one star defect

First suppose \(U_z^s=V_z^s=0\) at both zero sites. For an endpoint slice
\((s,v)\), put

\[
 c_{sv}=\tau a_sb_v,\qquad
 q_{sv}=2\tau a_s(\beta_v-b_v),\qquad
 \sigma=(1,1,1,1,-1,-1).                                      \tag{12}
\]

Let \(S_t\) be the tangent whose blocks on \(t0,t1,tu\) equal the
corresponding residual blocks and whose other blocks vanish. Direct
substitution in the endpoint formula gives

\[
                         N^{sv}=G(c_{sv}\sigma)+q_{sv}S_t.       \tag{13}
\]

The defect is supported on exactly the three-edge core star

\[
                              t0,\quad t1,\quad tu.              \tag{14}
\]

In particular, the asymmetric one-column boundary does not produce two
uncontrolled skew families: after the two-column site has done its work,
only the scalar differences \(\beta_v-b_v\) remain. Equation (13) is a
boundary map, not by itself an L0 obstruction.

## Exact zero-site L1 types

At a zero site \(z\), the two L1 equations against a full-column site
\(r\in\{0,1,u\}\) are

\[
 P_r(V_z^s)^{\mathsf T}=\rho_{rz}M_{rz},\qquad
 Q_r(U_z^s)^{\mathsf T}=\rho'_{rz}M_{rz}.             \tag{15}
\]

At the invertible sites \(0,1\), the lines \(P_r,Q_r\) are independent.
Consequently nonzero P/V and Q/U endpoint factors cannot coexist at one
zero: the same nonzero block cannot have both left lines. Across the two
endpoint colours, every zero therefore has one of three covariant types:

\[
\begin{array}{c|cc|c}
\text{type}&U_z^s&V_z^s&\text{full-column spokes}\\ \hline
\mathrm I&0&0&\text{unrestricted by (15)}\\
\mathrm P&0&f_sv_z&M_{rz}=m_rP_rv_z^{\mathsf T}\\
\mathrm Q&f_su_z&0&M_{rz}=m_rQ_ru_z^{\mathsf T}.
\end{array}                                                       \tag{16}
\]

The nonzero factors for different endpoint colours share one line because
they factor the same base spokes. If one spoke from a full-column site has
rank two, both endpoint factors vanish by (15), so the zero is type I.

There is an important asymmetry on the edge \(tz\). In type P, \(P_t=0\)
makes both selected sides of its P/V L1 equation vanish, so \(M_{tz}\)
is unrestricted. In type Q, \(Q_t\ne0\) forces the \(u_z\) shore when the
block is selected by L1. For the upper bound below, both \(tz\) blocks may
be relaxed to arbitrary matrices.

## Two active zeros form the coordinate-shore path

Take the three full-column sites

\[
                              I'=\{0,1,u\}                         \tag{17}
\]

as the inner set and

\[
                              T'=\{t,4,5\}                         \tag{18}
\]

as the shore. The selected generic-kernel equation and \(P_t=0\) give

\[
                         M_{rt}=w_rQ_t^{\mathsf T}
                         \qquad(r\in I').                         \tag{19}
\]

If \(z\) is active, (16) supplies a fixed shore factor
\(\xi_z=v_z\) in type P or \(\xi_z=u_z\) in type Q:

\[
                         M_{rz}=w_{rz}\xi_z^{\mathsf T}
                         \qquad(r\in I').                         \tag{20}
\]

Finally, the generic-kernel equation on the two zero endpoints is

\[
 0=(\nu_4+\nu_5)M_{45}=-2\tau M_{45},
 \qquad M_{45}=0.                                                \tag{21}
\]

Thus when both zeros are active, every inner-to-shore block has a fixed
factor at its shore endpoint. The arbitrary internal blocks \(M_{t4}\)
and \(M_{t5}\) are precisely the exceptional path

\[
                              4-t-5,                              \tag{22}
\]

while \(M_{45}=0\) has the required coordinate support. The exact
coordinate-shore path theorem gives

\[
                         \operatorname{rank}d\Psi_M\le49,         \tag{23}
\]

proving (3). The same argument applies if an inactive site's three
\(I'\)-spokes happen to share a nonzero right factor, provided every other
inactive zero has a fixed shore factor as well.

The coordinate-shore theorem is a support statement for an arbitrary
three-versus-three split; it does not require the three inner endpoint
matrices to be invertible. Thus the rank-one inner site \(u\) is an allowed
specialization.

The local shore bases inside the path theorem are used only to preserve
and bound differential rank. No physical-axis or R2 conclusion is
transported through them.

## Remaining boundary

The nine ordered zero-type charts split exactly as follows:

- the four active-active charts
  \((P,P),(P,Q),(Q,P),(Q,Q)\) satisfy (23); and
- the five charts containing an inactive zero remain after the L1/support
  reduction, unless every inactive zero in the chart already has a common
  shore factor.

Hence a rank-\(55\) asymmetric survivor must contain an inactive zero
whose three spokes from \(0,1,u\) do not share a right factor. On an
inactive-inactive chart, its endpoint slices have the exact one-star form
(13). A one-active chart additionally carries the single common physical
factor from (16). These are the scoped inputs for a subsequent mixed-L0
analysis.

For \(Q_t=0,\ P_t\ne0\), interchange the selected families:

\[
 (P,U,a,v)\longleftrightarrow(Q,V,b,u).
\]

No assertion is made about a chart where both \(t\) and \(u\) are
one-column, whether their missing columns agree or are transverse.

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_asymmetric_one_column_l1_boundary.py](../computations/verify_level_two_two_invertible_asymmetric_one_column_l1_boundary.py)

- imports and reruns the exact two-column skew-killing systems;
- computes the one-column P/V and Q/U system ranks \(3\) and \(4\), their
  two-versus-one kernel modes, and the unconstrained \(\beta_s-b_s\), then
  independently expands all six core edges as \(24\times14\) systems of
  ranks \(12\) and \(13\);
- checks all fifteen blocks in the generalized-gauge-plus-star identity
  (13), including its exact three-edge support;
- audits the inactive/P/V/Q/U zero-type dictionary and the asymmetric
  \(tz\) behavior; and
- imports all 64 formal path-factorization identities and the
  \(28+21=49\) rank count for all four active-active charts.

It passes normal, optimized, and isolated Python.
