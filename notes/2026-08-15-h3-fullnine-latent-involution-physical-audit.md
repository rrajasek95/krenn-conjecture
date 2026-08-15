# Physical audit of the full-nine latent involution

## Verdict

The physical implication asserted in commit `0902a62` is correct:

\[
 \text{literal full-nine equations}
 \quad\Longrightarrow\quad
 C(P,S)\subseteq W=\operatorname{span}{q^{[3]},X_0,X_1,X_2}.
\]

It is a direct rearrangement of the nine equations; rootlessness,
scalar-zero, and activity are not used.  In the complementary rank-six
physical-star branch and for an invertible channel matrix (K), it is
equivalent to the stated (J)-skew involution/anticommutator equations.

Two scope corrections are essential.

1. The six-dimensional physical latent space is defined by the **chosen
   endpoint-star factorization**, not by the square-free response quadratic
   (r) alone.  The latter has forgotten same-site products and need not have
   a canonical ordinary symmetric-matrix lift.
2. The involution is equivalent only to target-span containment.  It forgets
   the prescribed coefficients of all nine rows.  The physical guard below
   satisfies every anticommutator with diagonal target multipliers
   ((0,0,1)), rather than the exact ((1,1,1)).  Thus the involution cannot
   replace the downstream full-nine normalization/compatibility test.

The exact companion checker is
[`verify_h3_fullnine_latent_involution_physical_audit.py`](../computations/verify_h3_fullnine_latent_involution_physical_audit.py).
It contains no auxiliary (B/\mathrm{Eq}), (Gamma), AugP2, or operation
coordinates.

## 1. Literal conventions

Let (U) be the six residual sites and work in the site-square-zero algebra

\[
 \mathcal R_U=\bigotimes_{x\in U}(\mathbf Q\oplus V_x).
\]

For ordered physical endpoints (p,q), orient every edge block with the
endpoint mode first.  Thus

\[
\begin{aligned}
 p_i&=\sum_{x\in U}\sum_c A_{px}(i,c)x_{x,c},\\
 s_j&=\sum_{x\in U}\sum_c A_{qx}(j,c)x_{x,c},\\
 a_{ij}&=A_{pq}(i,j).
\end{aligned}                                               \tag{1}
\]

When the numerical site label of an endpoint exceeds that of (x), the
stored edge matrix is transposed before (1) is read.  This is only the usual
physical endpoint orientation; it introduces no algebraic transpose in the
row formula.

Let (q\in\mathcal R_U^2) be the common residual edge quadratic.  Divided
powers are normalized so that every unordered matching occurs once.  In
particular, (p_i s_jq^{[2]}) is the sum over a distinguished endpoint-star
edge and an unordered matching of the remaining four sites, with no factor
of (2).  The literal pair equations are

\[
 a_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,
 \qquad 0\le i,j\le2.                                    \tag{2}
\]

## 2. The polarization and the physical implication

Put

\[
 P=\operatorname{span}(p_0,p_1,p_2),\qquad
 S=\operatorname{span}(s_0,s_1,s_2).
\]

On the span of these stars define the symmetric tensor-valued bilinear map

\[
 C(u,v)=uvq^{[2]}\in\mathcal R_U^6.                       \tag{3}
\]

For (u=v), equation (3) uses the literal ordinary product (u^2), so a
pair of distinct supported ports appears twice.  For (p_i,s_j), the two
different shore factors give exactly the response term in (2).

Rearranging (2) gives, coefficient by coefficient in all 729 residual words,

\[
 \boxed{C(p_i,s_j)=\delta_{ij}X_i-a_{ij}q^{[3]}.}          \tag{4}
\]

Hence every one of the nine cross values belongs to

\[
 W=\operatorname{span}\{q^{[3]},X_0,X_1,X_2\},           \tag{5}
\]

which proves (C(P,S)\subseteq W).  No independence assumption is needed
for this implication as an equation on the labelled stars.

There are two legitimate ways to package the six channel labels.

* The abstract channel space
  (widetilde L=\mathbf Q^3_P\oplus\mathbf Q^3_S) is always six
  dimensional.  The physical star map (phi:\widetilde L\to\mathcal R_U^1)
  pulls (3) back to (widetilde L), even if the six physical stars are
  dependent.
* To regard the involution as acting on the **physical** latent span
  (L=P+S\subset\mathcal R_U^1), one needs

  \[
  \operatorname{rank}(p_0,p_1,p_2,s_0,s_1,s_2)=6.        \tag{6}
  \]

  Otherwise a relation mixing the two shores need not be preserved by the
  shore-sign operator, so it need not descend from (widetilde L) to the
  physical image.

Thus the rank-deficient branch is not a failure of (4); it is only outside
the coordinate-free physical-span interpretation used by `0902a62`.

## 3. The response form and all transpose conventions

Let (K=(K_{ij})) be the channel matrix used in the contracted response

\[
 r_K=\sum_{i,j}K_{ij}p_i s_j.                             \tag{7}
\]

In the ordered basis

\[
 \ell=(p_0,p_1,p_2,s_0,s_1,s_2)
\]

define the symmetric polar form

\[
 J=\begin{pmatrix}0&K\\K^{\mathsf T}&0\end{pmatrix}.     \tag{8}
\]

Then, in characteristic different from two,

\[
 r_K={1\over2}\ell^{\mathsf T}J\ell.                    \tag{9}
\]

The cap/direct contraction convention is

\[
 s(K)=\sum_{i,j}K_{ij}a_{ij}.                             \tag{10}
\]

There is no hidden transpose in (7) or (10).  The transpose in the
lower-left block of (8) is forced solely by symmetry of the bilinear form.
If the endpoint order is reversed, then (P,S) are exchanged and both
(a,K) are transposed; (7)--(10) are unchanged after that simultaneous
transport.

For the selected line (K(u,v)=uE_{ab}+vI), put

\[
 \alpha=a_{ab},\qquad \tau=\operatorname{tr}a.
\]

Its scalar-zero member is

\[
 K_*=\tau E_{ab}-\alpha I,\qquad s(K_*)=0.               \tag{11}
\]

If (a\ne b), then (det K_*=(-\alpha)^3\ne0).  On a diagonal
line,

\[
 \det K_*=\alpha^2(\tau-\alpha),                         \tag{12}
\]

so (	au\ne\alpha) is an additional requirement for the nondegenerate
(J^{-1}) formulation.  Rootlessness by itself should not be silently used
as a replacement for (6) or (det K\ne0).

## 4. Derivation of the involution equations

Assume (6) and (det K\ne0).  Define

\[
 T=\begin{pmatrix}I_3&0\\0&-I_3\end{pmatrix}.            \tag{13}
\]

Then

\[
 T^2=I,qquad\operatorname{tr}T=0,qquad
 T^{\mathsf T}J+JT=0.                                   \tag{14}
\]

For (lambda\in W^\perp\subset(\mathcal R_U^6)^*), let

\[
 C_\lambda=(\lambda(C(\ell_a,\ell_b)))_{a,b},\qquad
 A_\lambda=J^{-1}C_\lambda.                             \tag{15}
\]

Matrix conventions in (15) are column-vector conventions:

\[
 C_\lambda(x,y)=x^{\mathsf T}C_\lambda y,qquad
 J A_\lambda=C_\lambda.
\]

Because (C_\lambda) is symmetric, (A_\lambda) is (J)-self-adjoint:

\[
 A_\lambda^{\mathsf T}J=JA_\lambda=C_\lambda.           \tag{16}
\]

Containment (5) says exactly that the (P\)-by-(S) block of every
(C_\lambda) is zero.  Therefore (C_\lambda) is block diagonal.  Since
(J^{-1}) is block off-diagonal, (A_\lambda) is block off-diagonal, which
is equivalent to

\[
 \boxed{A_\lambda T+TA_\lambda=0\quad(\lambda\in W^\perp).} \tag{17}
\]

Conversely, in characteristic not two, (14) splits (L) into three
dimensional (+1) and (-1) eigenspaces which are (J)-isotropic.
Equation (17) makes every (A_\lambda) off-diagonal, hence every
(C_\lambda=JA_\lambda) block diagonal.  Its cross block vanishes, giving
(C(P,S)\subseteq W).  The checker tests this equivalence on all 21 basis
elements of (operatorname{Sym}^2L^*), rather than on one favorable form.

## 5. Literal rank-six rootless guard

The machine test uses the committed 77-cell site-square-zero N=8 near-source.
It satisfies 6559 of 6561 official EqSystem coefficients and fails only the
global pure (0^8,1^8) normalizations.  Choose endpoints

\[
 (p,q)=(2,3),\qquad U=(0,1,4,5,6,7).
\]

The exact physical star ranks are

\[
 (\operatorname{rank}P,\operatorname{rank}S,
   \operatorname{rank}(P+S))=(3,3,6).                   \tag{18}
\]

The direct block is

\[
 a=\begin{pmatrix}
 13&-34&-7\\263&28&97\\66&66&44
 \end{pmatrix}.                                        \tag{19}
\]

Every one of its nine nonzero selected cap lines is rootless.  The checker
uses (E_{01}+zI), for which

\[
 \alpha=-34,qquad\tau=85,qquad
 \mathsf A(z)=z^3(-34+85z).
\]

The scalar-zero channel is

\[
 K_*=85E_{01}+34I,qquad\det K_*=34^3=39304.             \tag{20}
\]

In the 729-dimensional literal top-word space, (W) has dimension four and
(W^\perp) has dimension 725.  The checker constructs a full basis of that
annihilator.  Only four quotient-coordinate forms are nonzero, spanning a
two-dimensional space, and all of them have zero cross block and satisfy
(16)--(17).  This test is nonvacuous: (C) has genuine nonzero (P\)-by-(P)
and (S\)-by-(S) image modulo (W).

For this guard the nine row left sides have diagonal target multipliers

\[
 (\mu_0,\mu_1,\mu_2)=(0,0,1).                            \tag{21}
\]

Nevertheless (4) with (X_i) replaced by (mu_iX_i) still puts every
cross value in (W), so the entire involution system passes.  Equation (21)
is the exact counterguard to the converse overclaim

\[
 \text{involution}\Longrightarrow\text{literal full nine}.
\]

It also shows what remains after the compression: the common direct matrix
and the exact diagonal coefficients must still be imposed in literal source
coordinates.  The involution alone cannot yield the desired EqSystem
contradiction.

## Reproduction

The checker uses exact rational arithmetic and passes normal, optimized,
isolated, no-site, isolated-no-site, and byte-compilation modes.  Its frozen
ledger digest is

```text
495af6a66a413d9bb39dfdb6d8dda0a3b8775e2677843b437c422d5fdb0afc5d
```

