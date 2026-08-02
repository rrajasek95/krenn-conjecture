# The inactive asymmetric one-column L0 residue is an antisymmetric cofactor-kernel shore

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Continue the dense-potential \(2I+2R+2Z\) chart of the
[asymmetric one-column L1 boundary](level-two-two-invertible-asymmetric-one-column-l1-boundary.md):

\[
 I=\{0,1\},\qquad T=\{t,u\},\qquad Z=\{4,5\},
\]

where \(X_0,X_1\) are invertible, \(X_t,X_u\) are nonzero of rank one,
and

\[
 P_t=0,\quad Q_t\ne0,\qquad P_u\ne0,\quad Q_u\ne0.             \tag{1}
\]

Assume both zero sites are L1-inactive. For a rank-\(55\),
kernel-equals-gauges survivor, the exact L0 equations imply:

> **Inactive-inactive reduction.** There are complementary physical
> colours \(s,k=1-s\) such that
> \[
>       \Psi(M)=h e_s^{\otimes6},\qquad
>       d\Psi_M(S_t)=q e_k^{\otimes6},\qquad hq\ne0.             \tag{2}
> \]
> For each zero \(z\), let
> \(\Phi_z:(\mathbf C^2)^3\to(\mathbf C^2)^{\otimes3}\) send its
> three \(\{0,1,u\}\)-spoke columns to the corresponding four-site
> cofactor. The two maps are copies of one covariant rank-five map
> \(\Phi\) with one-dimensional kernel \(\mathcal K\). Every rank-\(55\)
> survivor contains a nonzero shore column in \(\mathcal K\), or a
> nonzero difference of its two shore columns in \(\mathcal K\).

In a normalized inner chart,

\[
                   \mathcal K=\mathbf C\,(p,-p,0).              \tag{3}
\]

Thus the only remaining inactive-inactive escape is an exact
antisymmetric correction on the two invertible spokes, with no correction
on the \(u\)-spoke. If this correction vanishes at both zero shores, the
coordinate-shore path theorem gives

\[
                         \operatorname{rank}d\Psi_M\le49.       \tag{4}
\]

This is a rigorous reduction, not a closure of the nonzero-kernel residue.
It makes no claim about a one-active chart or about the chart in which both
rank-one sites miss a selected column.

The subsequent
[inactive-inactive fixed-root theorem](level-two-two-invertible-asymmetric-one-column-inactive-l0-closure.md)
uses the full mixed-coordinate purity of the star cofactor to remove this
nonzero-kernel residue.

## The one-star L0 system is complementary pure

Put

\[
                         \delta_v=\beta_v-b_v,
\]

using the L1 normal form from the preceding note. For an inactive-inactive
endpoint slice, the exact boundary identity is

\[
 N^{rv}=G(c_{rv}\sigma)+2\tau a_r\delta_v S_t.                  \tag{5}
\]

Write

\[
                         H=\Psi(M),\qquad K=d\Psi_M(S_t).
\]

After absorbing the generalized-gauge coefficients, the two mixed and two
pure L0 equations have the form

\[
\begin{aligned}
 0&=\kappa_{01}H+a_0\delta_1K,&
 0&=\kappa_{10}H+a_1\delta_0K,\\
 e_0^{\otimes6}&=\kappa_{00}H+a_0\delta_0K,&
 e_1^{\otimes6}&=\kappa_{11}H+a_1\delta_1K.                    \tag{6}
\end{aligned}
\]

The two pure targets are independent, so \(H,K\) must be independent.
The mixed equations therefore give

\[
                         a_0\delta_1=a_1\delta_0=0.             \tag{7}
\]

Both diagonal products cannot vanish, since then both pure targets would
be multiples of \(H\). They cannot both be nonzero by (7). Hence exactly
one survives. Label its colour \(k\), and put \(s=1-k\). The \(s\)-equation
first makes

\[
                             H=h e_s^{\otimes6},\qquad h\ne0,   \tag{8}
\]

while the \(k\)-equation writes

\[
                     K=\alpha e_k^{\otimes6}+\beta e_s^{\otimes6},
                     \qquad \alpha\ne0.                        \tag{9}
\]

Every block of \(S_t\) has the fixed \(t\)-factor \(Q_t\), so
\(K=Q_t\otimes C_t\) has \(t\)-flattening rank at most one. The minor on
columns \(e_k^{\otimes5},e_s^{\otimes5}\) in (9) is, up to sign,
\(\alpha\beta\). Thus \(\beta=0\), and singleton outer-product support
forces

\[
                   Q_t\parallel e_k,\qquad
                   C_t\parallel e_k^{\otimes5},                \tag{10}
\]

which proves (2). This conclusion is in the original physical colour
axes.

## Every nonzero star term uses both zero shores

The star \(S_t\) is supported on the three edges

\[
                              t0,\quad t1,\quad tu.              \tag{11}
\]

For each marked edge, its four-site cofactor has three matchings, giving
nine raw derivative terms. In one matching the two zero sites pair across
the block \(M_{45}\), but the generic-kernel equation gives

\[
                              M_{45}=0.                          \tag{12}
\]

The other two matchings pair the two remaining inner sites separately to
4 and 5. Hence three terms die and all six potentially live terms use one
spoke at each zero shore. Since \(K(e_k^{\otimes6})\ne0\), at each zero
\(z\) the \(k\)-column triple

\[
 W_z^k=\bigl(M_{0z}(-,k),M_{1z}(-,k),M_{uz}(-,k)\bigr)          \tag{13}
\]

is nonzero. This does not assert that \(L_z^k=\Phi(W_z^k)\) is nonzero:
that cofactor may vanish precisely along the kernel isolated below.

## The inner cofactor map has one antisymmetric kernel

For a zero \(z\) and shore colour \(a\), put
\(W_z^a=(M_{0z}(-,a),M_{1z}(-,a),M_{uz}(-,a))\), and define the
three-site tensor

\[
 L_z^a(x_0,x_1,x_u)=
 \sum_{i\in\{0,1,u\}}M_{iz}(x_i,a)M_{j\ell}(x_j,x_\ell),
 \qquad\{i,j,\ell\}=\{0,1,u\}.                                \tag{14}
\]

This is the value of a covariant linear map \(\Phi\) on the three spoke
columns \(W_z^a\). To calculate its kernel, make independent local basis
changes on \(0,1,u\) in this calculation only, taking \(X_0=X_1=I_2\).
These changes are not applied to the physical-purity identity (2). Up to
harmless nonzero scalars, the inner blocks become

\[
 M_{01}=J=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 M_{0u}=M_{1u}=p a^{\mathsf T},                                \tag{15}
\]

where \(a\ne0\), and both coordinates of \(p=(p_0,p_1)\) are nonzero
because \(P_u,Q_u\ne0\). Consequently

\[
 \Phi(U_0,U_1,U_u)
 =U_0\otimes p\otimes a+p\otimes U_1\otimes a
   +J\otimes U_u.                                               \tag{16}
\]

The map has rank five for every such \(p,a\). Indeed, if \(a_0\ne0\) one
explicit \(5\times5\) minor is

\[
                         -2p_0p_1^2a_0^3,                       \tag{17}
\]

and if \(a_1\ne0\), the analogous minor is

\[
                         -2p_0p_1^2a_1^3.                       \tag{18}
\]

Order the columns as

\[
 U_0(0),U_0(1),U_1(0),U_1(1),U_u(0),U_u(1).
\]

For (17), take rows \(000,010,011,100,110\) and columns
\(U_0(0),U_0(1),U_1(0),U_u(0),U_u(1)\); for (18), replace the rows by
\(001,010,011,101,111\). There is always the kernel vector

\[
                              (p,-p,0).                          \tag{19}
\]

For completeness, it is the whole kernel. Projecting (16) at the \(u\)
factor modulo the line \(\mathbf C a\) first gives \(U_u=-c a\). The
remaining matrix equation is

\[
                         U_0p^{\mathsf T}+pU_1^{\mathsf T}=cJ.  \tag{20}
\]

Writing \(p=(r,w)\) with \(rw\ne0\), the two diagonal equations give
\(U_1=-U_0\). The two off-diagonal equations are negatives of each other,
so characteristic zero gives \(c=0\); they then make \(U_0\parallel p\).
This proves (3).

The normalization in (15) is used only to compute the covariant line
\(\mathcal K=\ker\Phi\). In particular, \(p\) is not identified with either
physical target axis \(e_s,e_k\).

## Three forbidden corners force a kernel carrier

Evaluate \(H\) at colour \(s\) on site \(t\). By (10), every inner-to-\(t\)
block vanishes on this slice, and (12) kills the remaining unwanted
matching. Put

\[
 x_a=M_{t4}(s,a),\qquad y_b=M_{t5}(s,b).
\]

The four zero-shore corners are exactly

\[
                             T_{ab}=x_aL_5^b+y_bL_4^a.          \tag{21}
\]

Purity of \(H\) requires

\[
                     T_{sk}=T_{ks}=T_{kk}=0,\qquad T_{ss}\ne0. \tag{22}
\]

Suppose \(L_4^s,L_4^k\) are independent and \(L_5^k\ne0\). The first and
third zero corners give

\[
 x_sL_5^k+y_kL_4^s=0,\qquad
 x_kL_5^k+y_kL_4^k=0.                                         \tag{23}
\]

If \(y_k\ne0\), the independent tensors \(L_4^s,L_4^k\) would both be
proportional to \(L_5^k\). Thus \(y_k=0\), after which (23) gives
\(x_s=x_k=0\). The remaining forbidden corner gives \(y_s=0\), contradicting
\(T_{ss}\ne0\). Therefore

\[
 L_4^s,L_4^k\text{ independent}\quad\Longrightarrow\quad L_5^k=0. \tag{24}
\]

The symmetric implication exchanges 4 and 5. Both shore pairs cannot be
independent. Moreover, (13), (24), and \(\ker\Phi=\mathcal K\) show that
an independent shore immediately forces a nonzero \(\mathcal K\)-carrier
at the opposite shore.

It remains to consider two dependent pairs. If \(L_z^k=0\), then (13)
again gives a nonzero carrier \(W_z^k\in\mathcal K\). Otherwise there is a
scalar \(\alpha_z\) with \(L_z^s=\alpha_zL_z^k\), and exactness of the
kernel gives, in the normalized chart,

\[
 W_z^s=\alpha_zW_z^k+\lambda_z(p,-p,0).                         \tag{25}
\]

Equivalently, component by component,

\[
\begin{aligned}
 M_{0z}(-,s)&=\alpha_zM_{0z}(-,k)+\lambda_zp,\\
 M_{1z}(-,s)&=\alpha_zM_{1z}(-,k)-\lambda_zp,\\
 M_{uz}(-,s)&=\alpha_zM_{uz}(-,k).                              \tag{26}
\end{aligned}
\]

If \(\lambda_z=0\), the three full-column spokes at \(z\) share one fixed
right factor. If this happens at both zeros, use the inner set
\(\{0,1,u\}\) and shore \(\{t,4,5\}\). The \(t\)-spokes have fixed factor
\(Q_t\), the two zero spokes have their factors from (25), the blocks
\(M_{t4},M_{t5}\) form the exceptional path \(4-t-5\), and \(M_{45}=0\).
The exact coordinate-shore theorem yields (4).

Thus a rank-\(55\) inactive-inactive survivor must have
\(\lambda_z\ne0\) at some dependent shore, or have a nonzero \(k\)-column
already in \(\mathcal K\). These are precisely the antisymmetric
cofactor-kernel residues asserted above.

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_asymmetric_one_column_inactive_l0_reduction.py](../computations/verify_level_two_two_invertible_asymmetric_one_column_inactive_l0_reduction.py)

- imports the exact generalized-gauge-plus-one-star identity;
- enumerates all sixteen scalar zero patterns and the two complementary
  terminal charts, then checks the two pure \(t\)-flattening minors;
- enumerates the \(9=3+6\) raw/dead/live star terms and verifies that every
  live term uses both zero shores;
- proves rank five using the two symbolic minors (17), (18), checks the
  universal kernel generator, and tests representative rational points;
- verifies all 64 physical matching identities in (21);
- audits the forbidden-corner dichotomy, the sign in (25), and the
  \(\lambda=0\) fixed-shore specialization; and
- imports all 64 coordinate-shore path identities and the \(28+21=49\)
  bound.

It passes normal, optimized, and isolated Python.
