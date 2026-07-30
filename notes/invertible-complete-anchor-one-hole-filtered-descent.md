# Complete anchors force a common-site filtered one-hole packet

## 1. Outcome

Work at the first \(8\to6\) boundary with the two literal charts \(pq\)
and \(pr\).  On the \(pq\)-chart write

\[
 d_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2,                                  \tag{1}
\]

and suppose that \(d\) is invertible.  For a residual site \(w\), put

\[
 P_w\xi=\sum_i\xi_i(p_i)_w,\qquad
 S_w\eta=\sum_j\eta_j(s_j)_w,
 \qquad N_{w,e}=P_w^{\mathsf T}J_eS_w.                  \tag{2}
\]

Assume failure of the full-selector dark-cut descent, so

\[
 T_e=\{w:N_{w,e}=0\},\qquad |T_e|\geq3
 \quad(e=0,1,2),                                        \tag{3}
\]

and retain the incidence consequence

\[
                         2L+C\geq3.                       \tag{4}
\]

Here \(L\) counts sites aligned at at least two labels and satisfying
\(\operatorname {rank}P_w+\operatorname {rank}S_w\leq3\), while \(C\)
counts sites at which both images are the same literal coordinate plane.

The complete diagonal anchors and an off-diagonal full-nine row do give a
strict further descent, although not a complete exclusion.

> **Common-site filtered one-hole theorem.**  Let
> \(D\) be the five sites common to the residual sets of the \(pq\)- and
> \(pr\)-charts.  Under (3)--(4), there is a site \(w\in D\) at which one
> of the following two literal packets occurs.
>
> 1. **Physical-channel hole.**  For some physical colour \(c\), every
>    \(p\)- and \(q\)-endpoint row has zero \(c\)-coefficient at \(w\).
>    On \(D_0=D\setminus\{w\}\), the \(c\)-scalar coefficient of the
>    complete three-endpoint overlap is
>    \[
>       \boxed{
>       g_kA_{ij}+\lambda B_{ijk}
>          =\delta_{ic}\delta_{jc}\delta_{kc}X_c^{D_0}.}
>                                                               \tag{5}
>    \]
>    The terms \(A_{ij}\in{\cal A}_4(D_0)\) and
>    \(B_{ijk}\in{\cal A}_3(D_0)\) are displayed in (13) below.
>    In particular, for every off-diagonal pair \(i\ne j\), the same
>    literal anchor coefficient and crossed row give
>    \[
>       g_cA_{cc}+\lambda B_{ccc}=X_c^{D_0},\qquad
>       g_cA_{ij}+\lambda B_{ijc}=0.                       \tag{6}
>    \]
>    If \(g_c\ne0\), then
>    \[
>                         A_{ij}=-g_c^{-1}\lambda B_{ijc} \tag{7}
>    \]
>    is a genuine lower-order divisibility statement.  If \(g_c=0\),
>    then
>    \[
>                    B_{ijc}\in\operatorname {Ann}_3(\lambda).
>                                                               \tag{8}
>    \]
>    Whenever \(B_{ijc}\ne0\), (8) is an explicit nonzero filtered
>    colon class.  If it is zero, that particular overlap bracket has
>    already vanished before multiplication by the spoke \(\lambda\).
>
> 2. **Total-wedge shore.**  All cross products
>    \(u\times v\), \(u\in\operatorname {im}P_w\),
>    \(v\in\operatorname {im}S_w\), vanish.  There is a rank-one
>    direct-zero selector \(\xi\eta^{\mathsf T}\), with a nonzero
>    off-diagonal entry, and at least two physical colours \(c\) for
>    which
>    \[
>                         (P_w\xi)_c=(S_w\eta)_c=0.        \tag{9}
>    \]
>    For each such \(c\), contraction of the same literal overlap gives
>    \[
>       \boxed{
>       g_kA+\lambda_cB_k
>          =\delta_{kc}\xi_c\eta_cX_c^{D_0}.}             \tag{10}
>    \]
>    Thus every \(k\ne c\) again gives either the lower-order
>    divisibility \(A\in\lambda_c{\cal A}_3(D_0)\), or an explicit
>    class \(B_k\in\operatorname {Ann}_3(\lambda_c)\); a zero
>    representative is an unsuspended lower-order row.

No factor in (5) or (10) is cancelled.  In (7), membership in the image
of multiplication by \(\lambda\) is proved by an explicit representative;
it does not assert that multiplication by \(\lambda\) is injective.  In
(8), the possible noninjectivity is exactly the conclusion.

The theorem retains the complete diagonal ledger.  The colour \(c\) is
determined only after the aligned site is found, so availability of all
three anchors supplies the literal \(c\)-anchor in the first equation of
(6), not a scalar replacement.  The second equation is any one of the six
off-diagonal rows with the third exposed label fixed to \(c\).  In the
total-wedge packet, every diagonal target seen by
\(\xi\eta^{\mathsf T}\) remains on the right side of (10).  The theorem
also retains both charts: the witness lies in their common five-site
complement, and \(B\) contains the actual \(pr\)-direct and \(qr\)-direct
terms.  A selected nonzero physical curvature is not set to zero or
replaced by a formal scalar.  Except in the coefficient coincidence
(15a)--(15b), the argument does not show that curvature kills the colon
class.

Consequently this is a **filtered rank/colon descent, not a complete-nine
exclusion**.  It does not construct the common degree-five Macaulay
functional required by the rootless contradiction.  What remains is to
show that the nonzero classes in (8) or (10) die under the other site
coefficients/prolongations, or that their vanishing representatives force
a physical dark cut.

## 2. Why (4) supplies a site in the literal overlap

The sets counted by \(L\) and \(C\) are disjoint.  A \(C\)-site has two
rank-two images and hence rank sum four, whereas an \(L\)-site has rank
sum at most three.  Therefore

\[
  3\leq2L+C\leq2(L+C)
  \quad\Longrightarrow\quad L+C\geq2.                    \tag{11}
\]

The \(pq\)-residual set consists of the cross site \(r\) and the five
common sites \(D\).  At most one of the at least two sites in (11) can be
\(r\).  Hence at least one lies in \(D\).  This is the only overlap
counting needed; no target-set pattern is enumerated.

Fix such a common site \(w\), aligned at two different target labels
\(e,f\), and let \(c\) be the third label.  Every cross product of the two
local images is perpendicular to both \(e_e\) and \(e_f\), so

\[
 \operatorname {span}\{u\times v:
     u\in\operatorname {im}P_w,
     v\in\operatorname {im}S_w\}\subseteq\mathbb Ce_c.  \tag{12}
\]

If the span in (12) is nonzero, choose \(u_0\times v_0\ne0\).  Then
\(u_0,v_0\in E_{ef}=e_c^\perp\).  For any \(u\) in the first image,
\(u\times v_0\in\mathbb Ce_c\), which forces \(u\in E_{ef}\); the
same argument applies to the second image.  Thus both local \(c\)-rows
vanish, giving alternative 1.  This includes every \(C\)-site and every
nonzero-cross-product \(L\)-site.

If the span in (12) is zero, all cross products vanish.  When both images
are nonzero they are contained in one common line; otherwise one image is
zero.  This is precisely the total-wedge shore of alternative 2.  The
rank-sum hypothesis attached to an \(L\)-site is retained in the
zero-image case.

## 3. The physical-channel site coefficient

Expose the third endpoint \(r\).  On the common five sites \(D\), write

\[
 d=A_{pq},\qquad d'=A_{pr},\qquad T=A_{qr},
\]

and let \(x_i,y_j,t_k\) be the \(p,q,r\) endpoint-star rows.  Let \(z\)
be the internal quadratic on \(D\).  The complete 27 literal rows are

\[
 (d_{ij}t_k+d'_{ik}y_j+T_{jk}x_i)z^{[2]}
      +x_i y_jt_kz=\mathbf1_{i=j=k}X_i^D.                \tag{13a}
\]

This is a coefficient identity of the same physical source in the two
charts; no new cap or replacement quadratic has been introduced.

Now assume the physical-channel hole at \(w\), and scalarize every site
of \(D\) at the physical colour \(c\).  In the scalar site-square-zero
algebra decompose

\[
\begin{aligned}
 z&=z_0+z_w\lambda,&
 x_i&=\bar x_i,&y_j&=\bar y_j,\\
 t_k&=\bar t_k+z_wg_k,
\end{aligned}                                             \tag{13b}
\]

where all barred objects and \(z_0,\lambda\) live on \(D_0\).  Define

\[
\begin{aligned}
 A_{ij}&=d_{ij}z_0^{[2]}+\bar x_i\bar y_jz_0,\\
 B_{ijk}&=(d_{ij}\bar t_k+d'_{ik}\bar y_j
                 +T_{jk}\bar x_i)z_0
                 +\bar x_i\bar y_j\bar t_k .             \tag{13}
\end{aligned}
\]

The divided-power expansion is

\[
             z^{[2]}=z_0^{[2]}+z_w\lambda z_0.            \tag{14}
\]

Taking the \(z_w\)-coefficient of (13a) and using (13)--(14) gives (5)
term by term.  The right side is nonzero exactly when the three retained
source labels and the physical coefficient label are all \(c\); hence the
four Kronecker conditions in (5) are literal label bookkeeping.

There is an equivalent pair-chart reading.  On the \(pq\)-chart, the
constant-\(c\) coefficient of all nine rows is

\[
                    P_c^{\mathsf T}H_cS_c=E_{cc}-F_cd.    \tag{15}
\]

Exposing the residual site \(r\) first gives the label-\(k\) refinement
(5).  At \(k=c\), taking the \(w\)-coefficient splits the constant-word
identity (15) into \(g_cA_{ij}\), where \(w\) is occupied by the
\(r\)-star, and \(\lambda B_{ijc}\), where \(w\) is occupied by its
internal spoke.  The \(d'\)- and \(T\)-terms in \(B\) are the literal
overlap companions.  Thus (6) is exactly one site coefficient of (15)
coupled to an off-diagonal full-nine overlap row.

If \(g_c\ne0\), rearrangement proves (7).  This is division by the
nonzero scalar \(g_c\), not by \(\lambda\).  If \(g_c=0\), equation (6)
is exactly (8).  These are exhaustive and require no support census.

There is one direct curvature refinement.  Suppose the selected physical
four-cut uses the same site \(w=s\) and the same fourth-site colour \(c\):

\[
 A=d_{ab},\qquad B=d'_{ak},\qquad
 F=(A_{qs})_{bc},\qquad U=(A_{rs})_{kc},\qquad
 \kappa=AU-BF\ne0.                                      \tag{15a}
\]

At a physical-channel hole, \(F=(y_b)_w(c)=0\), while
\(U=(t_k)_w(c)=g_k\).  Hence

\[
                         \kappa=A g_k\ne0.                \tag{15b}
\]

The \(k\)-instance of every off-diagonal equation in (5) is therefore in
the divisibility branch.  If also \(k=c\), this is the same branch paired
with the literal anchor in (6).  When the forced witness or its missing
colour differs from the selected curvature coefficient, (15b) is
unavailable; nonzero curvature alone then does not decide between (7)
and (8).

## 4. The total-wedge selector and its coefficient

First construct the promised selector.  If both local images are nonzero,
total-wedge vanishing puts them in one line.  Therefore both
\(\ker P_w\) and \(\ker S_w\) have dimension at least two.  On

\[
 \mathbf P(\ker P_w)\times\mathbf P(\ker S_w)
\]

the equation \(\xi^{\mathsf T}d\eta=0\) has dimension at least one over
\(\mathbb C\) (or is identically zero).  The rank-one matrices with no
off-diagonal entry form at most three points, so an isotropic pair can be
chosen outside them.  It satisfies \(P_w\xi=S_w\eta=0\).

Suppose instead that \(S_w=0\); the transposed case is identical.  If
\(P_w\) is singular, choose \(0\ne\xi\in\ker P_w\).  Since \(d\) is
invertible, the isotropic choices of \(\eta\) form a two-plane, from which
one may avoid the sole possible diagonal rank-one direction.  If \(P_w\)
is invertible, choose \(\xi=P_w^{-1}e_a\) for any physical coordinate
axis and again choose \(\eta\) in the two-dimensional isotropic
hyperplane, avoiding the diagonal direction.  Then \(P_w\xi=e_a\) and
\(S_w\eta=0\), so (9) holds for the other two physical labels.  This
proves the selector assertion in every total-wedge case.

Contract (13a) in \(i,j\) against \(\xi_i\eta_j\).  Put

\[
 L=x(\xi),\qquad S=y(\eta),\qquad
 \alpha_k=(\xi^{\mathsf T}d')_k,\qquad
 \beta_k=(\eta^{\mathsf T}T)_k.
\]

The \(d_{ij}t_k\)-term vanishes by isotropy, and the exact contracted row
is

\[
       (\alpha_kS+\beta_kL)z^{[2]}+LSt_kz
                   =\xi_k\eta_kX_k^D.                    \tag{16}
\]

Choose a physical label \(c\) satisfying (9), scalarize at \(c\), and
write

\[
 L=\bar L,\qquad S=\bar S,\qquad
 t_k=\bar t_k+z_wg_k,\qquad z=z_0+z_w\lambda_c.
\]

Set

\[
 A=\bar L\bar Sz_0,\qquad
 B_k=(\alpha_k\bar S+\beta_k\bar L)z_0
                         +\bar L\bar S\bar t_k.           \tag{17}
\]

Taking the \(z_w\)-coefficient of (16) proves (10).  For \(k\ne c\), its
right side is zero.  If \(g_k\ne0\), solve only for the scalar multiple
\(A=-g_k^{-1}\lambda_cB_k\).  If \(g_k=0\), retain
\(B_k\in\operatorname {Ann}_3(\lambda_c)\).  If a displayed factor is
already zero, that is an honest lower-order vanishing, not evidence for
cancelling another factor.

The selector has a nonzero off-diagonal cell, so (16)--(17) genuinely use
at least one off-diagonal full-nine row together with whatever diagonal
targets \(\xi_k\eta_kX_k\) survive.  No change of source-label basis has
been made.

## 5. Exact scope and next step

Equations (6) and (10) are the first forced objects beyond the incidence
normal form (4).  They live on four sites, keep the direct/star/internal
filtration, and distinguish two logically different outcomes:

* an explicit representative proving membership in
  \(\lambda{\cal A}_3(D_0)\); or
* an explicit representative in the colon kernel
  \(\operatorname {Ann}_3(\lambda)\).

They do not imply that a nonzero colon representative survives in every
configuration.  When it vanishes, the corresponding lower overlap row is
already zero, and a further argument must use the remaining coefficients.
They also do not identify the four-site site-degree colon with the
degree-five parameter-space Macaulay cokernel.  A grade-preserving
prolongation is still required for that passage.

In particular, all nine rows and both unused anchors force more than
\(2L+C\geq3\): they force the common-site packet (5) or (10).  What is not
proved is a dark cut, curvature vanishing, a nonzero class in every branch,
or complete exclusion of the invertible alignment residue.

The dependency-free checker
[`verify_invertible_complete_anchor_one_hole_filtered_descent.py`](../computations/verify_invertible_complete_anchor_one_hole_filtered_descent.py)
audits the divided-power coefficient formulas, the refinement of the pure
sandwich by the exposed third endpoint, the contracted selector formula,
the local cross-product classification over a finite field, the isotropic
off-diagonal selector lemma, and the count which places a witness in the
five-site overlap.
