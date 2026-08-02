# The inactive-inactive asymmetric one-column chart closes at a fixed rank-one root

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Continue the dense-potential \(2I+2R+2Z\) chart of the
[inactive L0 reduction](level-two-two-invertible-asymmetric-one-column-inactive-l0-reduction.md).
Thus

\[
 I=\{0,1\},\qquad T=\{t,u\},\qquad Z=\{4,5\},
\]

\[
 P_t=0,\quad Q_t\ne0,\qquad P_u\ne0,\quad Q_u\ne0,              \tag{1}
\]

both zeros are L1-inactive, and a putative rank-\(55\),
kernel-equals-gauges survivor has complementary physical colours
\(s,k=1-s\) with

\[
 H=\Psi(M)=h e_s^{\otimes6},\qquad
 d\Psi_M(S_t)=q e_k^{\otimes6},\qquad hq\ne0.                   \tag{2}
\]

The preceding reduction found a covariant rank-five cofactor map
\(\Phi\) whose normalized kernel is

\[
                         \ker\Phi=\mathbf C\,(p,-p,0).          \tag{3}
\]

The remaining residue is now empty:

> **Inactive-inactive closure.** No rank-\(55\) packet satisfying (1),
> the inactive-inactive L1 normal form, and the full L0 equations exists.
> A chart with no nonzero kernel correction has
> \(\operatorname{rank}d\Psi_M\le49\). A chart with a nonzero correction
> either contradicts the two complementary physical axes in (2), or has
> every block incident with \(u\) on one fixed \(u\)-root and hence
> \[
>                         \operatorname{rank}d\Psi_M\le42.       \tag{4}
> \]

The proof uses the full mixed-coordinate purity of the five-site star
cofactor, not only its all-\(k\) value. Residual R2 is compatible with the
forced geometry at the invertible roots but is not needed for the rank
bound.

Together with the earlier active-active path closure and the companion
one-active results, this removes the inactive-inactive part of the
asymmetric one-column boundary. The \(Q_t=0,P_t\ne0\) case follows by
interchanging the selected families. No claim is made about a chart where
both rank-one sites miss a selected column.

## The pure \(H\)-corner fixes the physical \(s\)-root at \(u\)

Use the physical corner factorization from the reduction:

\[
                       T_{ab}=x_aL_5^b+y_bL_4^a,                \tag{5}
\]

where \(L_z^a=\Phi(W_z^a)\) is the three-site cofactor on
\(\{0,1,u\}\). Make local basis changes on these three inner sites for this
calculation only. Then

\[
 M_{01}=J=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 M_{0u}=M_{1u}=p h_u^{\mathsf T},                              \tag{6}
\]

where both coordinates of \(p\) are nonzero. Choose the normalized
\(u\)-coordinate \(e_1\) to annihilate the line \(h_u\).

On the \(u=e_1\) slice, the two terms of \(\Phi(W_z^s)\) using \(M_{0u}\)
or \(M_{1u}\) vanish. The remaining term is

\[
                 \Phi(W_z^s)|_{u=e_1}
                          =W_{z,u}^s(e_1)J.                    \tag{7}
\]

Consequently the left side of the nonzero \(ss\)-corner is a scalar
multiple of the rank-two matrix \(J\). The right side is

\[
 h\,\eta_0^s\otimes\eta_1^s\,\eta_u^s(e_1),                   \tag{8}
\]

where \(\eta_i^s\) is the image of the physical vector \(e_s\) under the
inner basis change. If \(\eta_u^s(e_1)\ne0\), (8) is a nonzero rank-one
matrix, impossible. Therefore

\[
                              e_s|_u\parallel h_u.              \tag{9}
\]

This is a physical-axis conclusion obtained from the pure tensor before
the normalized line is translated back; no R2 column is transported
through the basis change.

## A literal kernel column contradicts the pure star cofactor

Let \(\mathcal K=(p,-p,0)\), and suppose first that one all-\(k\) spoke
triple is a nonzero literal kernel column, say

\[
                              W_4^k=\lambda\mathcal K,\qquad
                              \lambda\ne0.                      \tag{10}
\]

Factor \(d\Psi_M(S_t)=Q_t\otimes C_t\). Equation (2) gives the full
five-site identity

\[
                              C_t=\gamma e_k^{\otimes5},
                              \qquad\gamma\ne0.                 \tag{11}
\]

At zero colours \((k,k)\), the three marked star edges pair one column
from shore 4 with one from shore 5. On the \(u=e_1\) slice, the marked
\(tu\) term vanishes because its \(u\)-factor is \(h_u\), while direct
expansion of the marked \(t0,t1\) terms gives

\[
 C_t^{kk}|_{u=e_1}
   =\lambda W_{5,u}^k(e_1)
       \bigl(p\otimes e_0-e_0\otimes p\bigr).                  \tag{12}
\]

The matrix in parentheses is

\[
 p_1\begin{pmatrix}0&-1\\1&0\end{pmatrix},                    \tag{13}
\]

and has rank two because \(p_1\ne0\). But (11) makes the same slice a
nonzero rank-one product: by (9), the physical \(e_k\)-axis is transverse
to \(h_u\), so its \(e_1\)-coordinate is nonzero. Whether the scalar on
the right of (12) vanishes or not, equality is impossible. The same
argument applies with the two zero shores exchanged.

Thus

\[
                  L_z^k=0\quad\Longrightarrow\quad\text{no survivor},
                  \qquad z=4,5,                               \tag{14}
\]

because the preceding theorem already showed that \(W_z^k\ne0\), and
\(\ker\Phi\) is exactly the line (3).

An independent cofactor pair at one shore forced \(L_z^k=0\) at the
opposite shore. Hence (14) also removes every independent-shore branch.

## Full mixed purity sees the difference kernels

The only possible residue now has two nonzero dependent cofactor pairs:

\[
\begin{aligned}
 W_4^s&=\alpha_4W_4^k+\lambda_4\mathcal K,\\
 W_5^s&=\alpha_5W_5^k+\lambda_5\mathcal K.                     \tag{15}
\end{aligned}
\]

Let \(B(A,B)\) denote the inner three-tensor in the star cofactor obtained
from zero-shore triples \(A,B\). It is bilinear. The four zero-colour
slices of (11) are

\[
 B(W_4^k,W_5^k)=P\ne0,\qquad
 B(W_4^s,W_5^k)=B(W_4^k,W_5^s)=B(W_4^s,W_5^s)=0,               \tag{16}
\]

where \(P\) is the physical all-\(k\) product on \(\{0,1,u\}\). Put

\[
 X=B(\mathcal K,W_5^k),\quad
 Y=B(W_4^k,\mathcal K),\quad
 Z=B(\mathcal K,\mathcal K).
\]

Substitution of (15) into the three zero equations in (16), followed by
elimination of \(X,Y\), gives the exact identity

\[
                         \lambda_4\lambda_5 Z
                              =\alpha_4\alpha_5P.               \tag{17}
\]

The complete star expansion, including the marked \(tu\)-edge, is

\[
                         Z=-2\rho\,p\otimes p\otimes h_u,
                         \qquad\rho\ne0.                       \tag{18}
\]

Thus \(Z\) is a nonzero product rooted at \(h_u\). If both
\(\lambda_4,\lambda_5\) were nonzero, (17) would make the physical
all-\(k\) product \(P\) proportional to \(Z\), forcing
\(e_k|_u\parallel h_u\). This contradicts (9). Therefore

\[
                              \lambda_4\lambda_5=0.             \tag{19}
\]

For example, if \(\lambda_4\ne0\), then \(\lambda_5=0\), and the
\((k,s)\)-equation in (16) gives \(\alpha_5P=0\). Hence
\(\alpha_5=0\) and

\[
                              W_5^s=0.                          \tag{20}
\]

Symmetrically, a live correction at shore 5 forces \(W_4^s=0\). Full
star purity therefore permits at most one difference carrier, and makes
the opposite shore a physical coordinate shore. This sharpening is not
needed for the final rank bound, but records exactly how \(C_t\) detects
the otherwise cofactor-invisible direction.

## The remaining cofactor line fixes every \(u\)-block

Write

\[
                         A=L_4^k,\qquad B=L_5^k.                \tag{21}
\]

Both tensors are nonzero by (14), and dependence within each shore gives

\[
                         L_4^s=\alpha_4A,\qquad
                         L_5^s=\alpha_5B.                      \tag{22}
\]

If \(A,B\) were independent, the forbidden \(kk\)-corner in (5) would
force \(x_k=y_k=0\). The forbidden \(sk\) and \(ks\) corners would then
force \(x_s=y_s=0\), contradicting \(T_{ss}\ne0\). Therefore
\(A,B\) are proportional.

The nonzero \(ss\)-corner is consequently a nonzero scalar multiple of
both \(A\) and \(B\). Since \(H=h e_s^{\otimes6}\), there are nonzero
scalars \(\gamma_4,\gamma_5\) such that

\[
                     L_z^k=\gamma_z\,
                        \eta_0^s\otimes\eta_1^s\otimes h_u,
                     \qquad z=4,5.                             \tag{23}
\]

Slice (23) again at \(u=e_1\). Its right side vanishes by (9), while the
left side is \(W_{z,u}^k(e_1)J\) by (7). Hence

\[
                         W_{z,u}^k\parallel h_u.                \tag{24}
\]

The kernel correction in (15) has zero \(u\)-component, so (24) also gives

\[
                         W_{z,u}^s\parallel h_u.                \tag{25}
\]

Thus both \(M_{u4}\) and \(M_{u5}\) have the fixed factor \(h_u\) at \(u\).
The blocks \(M_{u0},M_{u1},M_{ut}\) already have that factor by the
generic-kernel normal form. Every base block incident with \(u\) is now on
one fixed root.

Every differential column from an edge not incident with \(u\) lies in
the \(32\)-dimensional output slice with \(u\)-factor \(h_u\). Each of the
five incident edges has only two tangent cells transverse to that slice.
Therefore

\[
                         \operatorname{rank}d\Psi_M
                              \le32+5\cdot2=42,                 \tag{26}
\]

proving (4).

## Literal residual R2

The physical statement (9) also makes the literal R2 alternatives
transparent at the two invertible roots. At each \(i\in\{0,1\}\),

\[
 M_{iu}\text{ is a nonzero pure-}s\text{ output block},\qquad
 M_{it}\text{ is a nonzero pure-}k\text{ output block}.        \tag{27}
\]

These lie on distinct incident edges, so they are exactly the two required
pure-column witnesses after the live endpoint stars rule out preservation.
Thus R2 does not kill the residue at roots \(0,1\); the full L0 slices
already give the stronger fixed-root bound (26). No R2 statement at \(u\)
is inferred through a normalized basis.

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_asymmetric_one_column_inactive_l0_closure.py](../computations/verify_level_two_two_invertible_asymmetric_one_column_inactive_l0_closure.py)

- imports the exact rank-five cofactor kernel, all 64 physical corner
  identities, and the earlier corner/path dichotomy;
- checks the rank-two-versus-rank-one \(H\)-slice forcing (9);
- expands the literal kernel slice (12), including its nonzero skew
  determinant;
- expands the complete bilinear star, verifies
  \(B(\mathcal K,\mathcal K)=-2\rho p\otimes p\otimes h_u\), and audits the
  mixed-purity elimination (17);
- checks the independent-\(A,B\) forbidden-corner system has rank four for
  every \(\alpha_4,\alpha_5\);
- audits the pure-line extraction (23)--(25);
- imports the exact \(32+10=42\) fixed-root bound and a sharp integral
  rank-\(42\) calibration; and
- checks the two literal physical R2 witnesses at both invertible roots
  and for both labelled colour charts.

It passes normal, optimized, and isolated Python.
