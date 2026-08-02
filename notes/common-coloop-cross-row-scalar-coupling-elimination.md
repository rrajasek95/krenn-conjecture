# Simultaneous cross rows leave a one-sided common-coloop cokernel

Research evidence only. Krenn's conjecture remains open, the dashed
clean-point implication is not proved, and the certified spine is
untouched.

## Outcome

Retain a disjoint singleton common-coloop branch

\[
                 c=e_r,\qquad d=e_s,\qquad r\ne s,           \tag{1}
\]

and let \(t\) be the third label. The two full-nine rows omitted by the
diagonal-complete \(7/9\) guard are

\[
                              (r,t),\qquad(t,s).              \tag{2}
\]

Adding them simultaneously gives a genuine source-level relation. Put

\[
 Q=q^{[h]},\qquad
 H_j=\bar s_jq_0^{[h-1]},\qquad
 G_i=\bar p_iq_0^{[h-1]},                                   \tag{3}
\]

and let

\[
 u=P(e_r)\in V_x,\qquad v=S(e_s)\in V_x.                    \tag{4}
\]

The two cross rows, together with the \(r\)- and \(s\)-diagonal rows,
imply

\[
 \boxed{\qquad
 Q\ne0\quad\Longrightarrow\quad a_{rt}a_{ts}=0.
 \qquad}                                                     \tag{5}
\]

Thus the shared top tensor forbids both missing direct-scalar directions
from surviving simultaneously. If the local tensor rank of \(Q\) is at
least two, both coefficients vanish. If \(Q\) has local rank one, at
most one coefficient survives, and the corresponding \(A\)-arm is
forced to be a scalar multiple of \(Q\); the other arm is
\(A\)-annihilated. If \(Q=0\), both coefficients remain invisible to the
physical rows, although both \(A\)-arms vanish.

This is not a complete contradiction. Substitution into the
[scalar-extended polar cokernel](common-coloop-scalar-extended-polar-cokernel-boundary.md)
leaves four exact residual branches:

\[
\begin{array}{c|c|c|c}
\text{branch}&(a_{rt},a_{ts})&
 (u\bar s_tA,\bar p_tvA)&
 \text{polar pairing}\\ \hline
Q=0&\text{arbitrary}&(0,0)&
 (\mu a_{rt},\mu a_{ts})\\
\operatorname{rank}_xQ\ge2&(0,0)&(0,0)&(0,0)\\
\text{left rank one}&(a,0),\ a\ne0&(-aQ,0)&(\mu a,0)\\
\text{right rank one}&(0,b),\ b\ne0&(0,-bQ)&(0,\mu b).
\end{array}                                                  \tag{6}
\]

The last column means

\[
 \Lambda(u\bar s_tD_{\bar K}(z)),\quad
 \Lambda(\bar p_tvD_{\bar K}(z)).                           \tag{7}
\]

Exact rational guards realize a detecting affine residual on every row
of (6) at the linear elimination level. Therefore the two source rows
close the simultaneous two-scalar stratum but do not close the polar
cokernel. The next source datum is now one-sided: relate the surviving
raw arm's actions through \(A\) and \(D_{\bar K}(z)\), or exclude the
zero-top/rank-two \(A\)-annihilator branches by the remaining
consecutive-power structure.

For the particular consecutive-power \(7/9\) packet, both added rows do
give an immediate contradiction: each failed arm tensor is linearly
independent of \(Q\), so no direct coefficient repairs either row. That
packet has no full-nine extension.

## 1. The four-row elimination inside the full-nine system

Because \(\bar p_r=0\) and \(\bar s_s=0\), the local endpoint rows are
exactly \(p_r=u\) and \(s_s=v\). Expanding the four relevant full-nine
equations at \(x\) gives

\[
 \begin{aligned}
 a_{rr}Q+uH_r&=X_r,\\
 a_{rt}Q+uH_t&=0,\\
 a_{ss}Q+vG_s&=X_s,\\
 a_{ts}Q+vG_t&=0.
 \end{aligned}                                               \tag{8}
\]

No common power was cancelled. These are literal fixed-label rows of the
same quadratic \(q\). The other five equations can further constrain
the branch, but the direct entries \(a_{rt},a_{ts}\) occur nowhere else
in the nine-row table.

Assume \(Q\ne0\) and \(a_{rt}a_{ts}\ne0\). The two cross equations in
(8) express the same nonzero tensor as

\[
               Q=-a_{rt}^{-1}uH_t
                 =-a_{ts}^{-1}vG_t.                         \tag{9}
\]

Equality of nonzero pure tensors forces \(u\parallel v\), and \(Q\) has
that common local factor. The two diagonal equations then have left
sides with the same local factor. Since

\[
 X_r=e_r^{(x)}\otimes Y_r,\qquad
 X_s=e_s^{(x)}\otimes Y_s,                                  \tag{10}
\]

they force \(u\parallel e_r^{(x)}\) and
\(v\parallel e_s^{(x)}\). This contradicts \(r\ne s\), proving (5).

The argument uses all the shared provenance that was absent after scalar
contraction: the same \(Q\) occurs in both cross rows and both diagonal
rows.

## 2. Exhaustive local-rank branches

Equations (8) give more than the product relation.

### Zero top

If \(Q=0\), the cross rows reduce to

\[
                         H_t=G_t=0,                          \tag{11}
\]

because \(u,v\ne0\). The coefficients \(a_{rt},a_{ts}\) multiply zero
and remain arbitrary. The diagonal rows separately force the usual pure
anchors \(uH_r=X_r\) and \(vG_s=X_s\).

### Local rank at least two

If \(\operatorname{rank}_xQ\ge2\), either nonzero cross coefficient
would express \(Q\) as a tensor with one local factor. Therefore

\[
                  a_{rt}=a_{ts}=0,\qquad H_t=G_t=0.          \tag{12}
\]

### Local rank one

Suppose \(Q\ne0\) has one local factor. If \(a_{rt}\ne0\), the first
cross row forces

\[
                   Q=u q_t,\qquad H_t=-a_{rt}q_t.            \tag{13}
\]

Theorem (5) gives \(a_{ts}=0\), and the second cross row gives \(G_t=0\).
This is the left one-sided branch in (6). The transposed argument gives
the right branch. If neither coefficient is nonzero, both arms vanish
through \(A\).

These alternatives are exhaustive. In particular, the two missing rows
do not produce a two-variable resultant: their direct coefficients are
independent, while their common tensor \(Q\) enforces the rank
dichotomy (11)--(13).

## 3. Substitution into the scalar-extended cokernel

Write the two raw arm responses as

\[
                    \alpha=u\bar s_t,\qquad
                    \beta=\bar p_tv.                        \tag{14}
\]

The cross rows state

\[
                   \alpha A=-a_{rt}Q,\qquad
                   \beta A=-a_{ts}Q.                        \tag{15}
\]

An augmented cokernel pair \((\Lambda,\nu)\), with
\(\mu=-\nu\), must satisfy

\[
 \boxed{
 \begin{aligned}
 \Lambda(\alpha D_{\bar K}(z))&=\mu a_{rt},\\
 \Lambda(\beta D_{\bar K}(z))&=\mu a_{ts},\\
 \Lambda(C_{\bar K}(z))+\mu(z-\sigma_0)&\ne0.
 \end{aligned}}                                             \tag{16}
\]

Combining (15)--(16) gives exactly table (6).

On the left rank-one branch, normalize the surviving arm by
\(\widetilde\alpha=\alpha/a_{rt}\). Then

\[
        \widetilde\alpha A=-Q,\qquad
        \Lambda(\widetilde\alpha D_{\bar K}(z))=\mu,         \tag{17}
\]

while \(\beta A=0\) and
\(\Lambda(\beta D_{\bar K}(z))=0\). This is the smallest exact coupled
residual after both source rows are restored: one source-provenant arm
interpolates the common top tensor between \(A\) and \(D\), while the
opposite arm is annihilated at both displayed coordinates. The right
branch is its endpoint transpose.

On the rank-at-least-two branch, both direct coefficients and both
\(A\)-arm images vanish, so (16) asks \(\Lambda\) to annihilate both
\(D\)-arm images while detecting the affine residual. On the zero-top
branch, both \(A\)-arm images vanish but the two direct coefficients
remain free. Neither conclusion contradicts the clean-error formula
without another consecutive-power or overlap relation.

The missing diagonal row does not contain \(a_{rt}\) or \(a_{ts}\). It
can further constrain \(Q,H_t,G_t\) and the curvature corner, but it
cannot undo (5) or by itself remove all four branches in (6).

## 4. The literal \(7/9\) packet is excluded

For completeness, specialize to the consecutive-power packet from the
[two-arm kernel boundary](common-coloop-two-arm-polar-kernel-boundary.md):

\[
 \begin{aligned}
 q_0={}&z_{00}z_{10}+z_{20}z_{30}
       +z_{01}z_{21}+z_{11}z_{41}+z_{32}z_{42},\\
 \rho={}&e_2^{(x)}z_{02},\qquad q=q_0+\rho,                 \tag{18}\\
 p={}&(e_0^{(x)},z_{31},z_{22}),\\
 s={}&(z_{40},e_1^{(x)},z_{12}).
 \end{aligned}
\]

In site order \(0,1,2,3,4,x\), exact multiplication gives

\[
 Q=q^{[3]}=210012,\qquad
 p_0s_2q^{[2]}=121220,\qquad
 p_2s_1q^{[2]}=002221.                                     \tag{19}
\]

These are three different basis monomials. Hence

\[
 a_{02}Q+p_0s_2q^{[2]}\ne0,\qquad
 a_{21}Q+p_2s_1q^{[2]}\ne0                                \tag{20}
\]

for every \(a_{02},a_{21}\). Adding either missing row already excludes
this packet; adding both confirms that it is exactly \(7/9\), not a
full-nine counterexample.

## 5. Exact checker and scope

The dependency-free checker
[verify_common_coloop_cross_row_scalar_coupling_elimination.py](../computations/verify_common_coloop_cross_row_scalar_coupling_elimination.py)
uses exact rational local tensors, independent row reduction, and a
separate site-square-zero reconstruction. It verifies:

* all four source equations (8) on sharp zero-top, local-rank-two, left
  rank-one, and right rank-one branches;
* the impossibility of simultaneous nonzero cross coefficients under
  both diagonal anchors;
* exact augmented polar-cokernel witnesses on every residual branch in
  (6); and
* all nine pair rows, the top power, and both failed cross rows in the
  literal consecutive-power packet (18)--(20).

The frozen checker ledgers have SHA-256 values

    aef2f08ba8e8ef6b6c984d48e09bb4a32bd95fc81c85eea11b7e074513b09df6
    8f7b16ddf4f84058c7eae7b4faac961b1a0282fc638e2a4db695ec4db5ed0d38
    dbc8582caf3c51c8045bd32cb53cc356d174c86ba93c3f1728f7d54ea75a61c1

They are respectively the cross-row branch ledger, coupled cokernel
ledger, and literal \(7/9\) source ledger. The checker is live under
normal Python, -O, and -I -S.

The result is an exact full-nine elimination, not a closure of the
common-coloop branch. It proves that the two restored rows cannot both
carry scalar motion when \(Q\ne0\), and it replaces the former
two-missing-row frontier by the four coupled residuals in (6). Closing
those residuals requires the actual higher-power relation between the
same arm's \(A\)- and \(D_{\bar K}(z)\)-images, or a source-faithful
overlap that detects the affine term in (16).
