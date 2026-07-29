# Cubic nullity compatibility: the common-cofactor-zero boundary

## 1. Outcome

The leave-one-anchor nullity web does not, by itself, give a kernel
direction on the star shared by two nonneighbours.  There is one exact
boundary that must first be removed.

Keep the hypotheses and notation of
[the cubic nullity-web theorem](cubic-vertex-leave-one-anchor-nullity-web.md).
Fix an anchor colour \(c\), two distinct nonneighbours \(q,q'\) of the
cubic vertex \(p\), and put

\[
 S_c=B\setminus\{p,a_c\},\qquad
 L=S_c\setminus\{q,q'\},\qquad
 P_c=H_L(A).
 \tag{1}
\]

Thus \(|L|=N-4\) is even.  The two leave-one-anchor maps have odd physical
site sets

\[
 K_{q,c}=L\mathbin{\dot\cup}\{q'\},\qquad
 K_{q',c}=L\mathbin{\dot\cup}\{q\}.
 \tag{2}
\]

**Theorem 1.1 (local-port classification).**  Restore all tensor slots to
physical order.  Then

\[
 \begin{aligned}
 \ker\Phi_{q,c}\cap V_{q'}&=
 \begin{cases}V_{q'},&P_c=0,\\0,&P_c\ne0,\end{cases}\\
 \ker\Phi_{q',c}\cap V_q&=
 \begin{cases}V_q,&P_c=0,\\0,&P_c\ne0.\end{cases}
 \end{aligned}
 \tag{3}
\]

Here a local space is embedded as the corresponding one-site summand of
the domain.  If \(P_c\ne0\), restriction of either kernel to the common
port space \(\bigoplus_{v\in L}V_v\) is injective.  If \(P_c=0\), both
maps automatically have nullity at least three, but the guaranteed
three-spaces are supported at opposite local ports and both have zero
restriction to \(L\).

This is an exact matching identity, not a generic-rank assertion.  It
retains arbitrary complex cancellation, zero entries, asymmetric endpoint
blocks, and the complete matching cofactors.

The boundary is sharp in every even order.  For every even \(N\ge8\) there
is a connected, complete-support aggregate array on
\(S_c=L\dot\cup\{q,q'\}\) such that

\[
 P_c=0,\qquad
 \ker\Phi_{q,c}=V_{q'},\qquad
 \ker\Phi_{q',c}=V_q,                                  \tag{4}
\]

while every double-deletion cofactor \(H_{L\setminus\{v,w\}}\) is nonzero.
Thus even exact nullity three on both sides, dense support, and full lower
cofactor activity do not force a nonzero compatible direction on the
shared \(L\)-star.  The construction is a countermodel to that proposed
inference, not a realization of the ternary target: it intentionally fails
all three cubic pure-cofactor equations.  The surviving next datum is the
nine-equation pure two-crossing Hessian system (9), together with the fact
that its direct coefficients are one endpoint-ordered physical block and
are transposed when the two endpoints are reversed.

## 2. Exact two-deletion gluing formula

Write \(x\) for the quadratic formed by blocks internal to \(L\).  Orient
the blocks from \(q'\) into \(L\), and for \(j=0,1,2\) put

\[
 b^{q'}_j=\sum_{w\in L}b^{q'}_{j,w},\qquad
 b^{q'}_{j,w}=(e_j^*\otimes\operatorname{id})A_{q'\mid w}\in V_w.
 \tag{5}
\]

For \(z=(z_{q'},z_L)\in V_{q'}\oplus\bigoplus_{v\in L}V_v\), define the
complete polarized lower-cofactor response

\[
 \Theta_c(z_L,b^{q'}_j)=
 \sum_{\substack{v,w\in L\\v\ne w}}
 z_v^{(v)}\otimes b^{q'}_{j,w}{}^{(w)}\otimes
 H_{L\setminus\{v,w\}}(x).
 \tag{6}
\]

Every factor in (6) is restored to its physical slot.  Expanding the
cofactor in \(K_{q,c}\setminus\{v\}\) along the unique edge at \(q'\)
gives, coefficient by coefficient,

\[
 \boxed{
 (e_j^*)_{q'}\mathbin{\lrcorner}\Phi_{q,c}(z)
   =(e_j^*z_{q'})P_c+\Theta_c(z_L,b^{q'}_j).}
 \tag{7}
\]

The term centered at \(q'\) gives the first summand.  In every term
centered at \(v\in L\), the site \(q'\) must be paired with one
\(w\ne v\); partitioning by that \(w\) gives (6).  This proves (7) with
no division and no selection of an individual matching monomial.

If \(z_L=0\), equation (7) for all three \(j\) says simply

\[
                         \Phi_{q,c}(z_{q'})=z_{q'}\otimes P_c.
 \tag{8}
\]

The tensor-product zero law proves (3).  It also proves injectivity of
kernel restriction when \(P_c\ne0\): a kernel vector restricting to zero
on \(L\) lies in \(V_{q'}\), and hence is zero.  Reversing \(q,q'\) gives
the other half of the theorem.

Equation (7) identifies the next legitimate chart.  On \(P_c\ne0\), all
forced kernel vectors have nonzero, faithfully recorded common-star
restrictions, and compatibility can be attacked through the same Hessian
\(\Theta_c\).  On \(P_c=0\), raw nullity can consist entirely of silent
local ports and contains no such information.

There is, however, a stronger datum than the nullities which survives on
both charts.  Let \(s^q_{d,L}\) and \(s^{q'}_{j,L}\) be the restrictions to
\(L\) of the physical colour rows at \(q\) and \(q'\), respectively.
Expanding the exact pure anchor cofactor
\(H_{S_c}=\lambda_c^{-1}e_c^{\otimes S_c}\) by whether \(q\) is paired
directly to \(q'\), and then contracting their colours by \(d,j\), gives

\[
 \boxed{
 A_{q\mid q'}(d,j)P_c+
 \Theta_c(s^q_{d,L},s^{q'}_{j,L})
 =\delta_{cd}\delta_{cj}\lambda_c^{-1}e_c^{\otimes L}.}
 \tag{9}
\]

The nine equations (9), their use of one endpoint-ordered physical block
\(A_{q\mid q'}\), and the transpose relation seen from \(q'\) are the
compatibility data that survive the countermodel below.  On \(P_c\ne0\)
they couple the faithful common-star restrictions to the entries of that
block.  On \(P_c=0\) they become a pure two-crossing Hessian system: eight
responses vanish and the \((c,c)\)-response is the nonzero pure tensor.
Any continuation on the zero boundary must use those responses, not the
automatic local kernel ports.

## 3. A uniform dense cancellation family

Let \(r=N-4\), so \(r\ge4\) is even, and label
\(L=\{1,\ldots,r\}\).  Put

\[
                         E=e_0e_0^T
\]

and use the nonzero scalar weights

\[
 w_{12}=-(r-2),\qquad w_{uv}=1\quad\text{for every other }u<v\text{ in }L.
 \tag{10}
\]

Set \(A_{uv}=w_{uv}E\) on \(L\).  Every internal block is nonzero.  The
only possible word of \(H_L\) is the constant-zero word, and its scalar is
the hafnian of \((w_{uv})\).  Partitioning matchings according to use of
the edge \(12\) gives

\[
 \begin{aligned}
 \operatorname{haf}(w)
 &=-(r-2)(r-3)!!+\bigl((r-1)!!-(r-3)!!\bigr)\\
 &=0.
 \end{aligned}                                          \tag{11}
\]

So \(P_c=H_L=0\) by exact cancellation.  Nevertheless, for distinct
\(v,w\in L\), write

\[
 H_{L\setminus\{v,w\}}=h_{vw}e_0^{\otimes(L\setminus\{v,w\})}.
\]

Directly from (10),

\[
 h_{vw}=\begin{cases}
 (r-3)!!,&\{v,w\}\cap\{1,2\}\ne\varnothing,\\
 -2(r-5)!!,&\{v,w\}\cap\{1,2\}=\varnothing.
 \end{cases}                                            \tag{12}
\]

Thus every double-deletion cofactor is nonzero.

For each \(t\in\{q,q'\}\) and every \(v\in L\), orient the star block as

\[
                    A_{t\mid v}=e_0^{(t)}\otimes e_1^{(v)}. \tag{13}
\]

The block \(A_{qq'}\) may be any nonzero asymmetric matrix; it is absent
from either odd deletion map.  Taking it nonzero makes the support on
\(S_c\) the complete graph.

Consider \(K=L\dot\cup\{t\}\).  The three columns of its cofactor map
centered at \(t\) are zero by (11).  For a center \(v\in L\), expansion at
\(t\) gives

\[
 H_{K\setminus\{v\}}=
 \sum_{w\ne v}h_{vw}
 e_0^{(t)}\otimes e_1^{(w)}\otimes
 e_0^{\otimes(L\setminus\{v,w\})}.                     \tag{14}
\]

The remaining \(3r\) columns are independent.  Split them by the colour
\(\gamma\) inserted at their center \(v\).

* For \(\gamma=0\), the coefficient matrix, with output marker \(w\), is
  the \(r\)-by-\(r\) matrix \(M=(h_{vw})\) with zero diagonal.
* For \(\gamma=1\), it is the weighted signless incidence matrix of
  \(K_r\).  A column relation would give
  \(h_{vw}(x_v+x_w)=0\) on every edge; a triangle and characteristic zero
  force every \(x_v=0\).
* For \(\gamma=2\), the ordered colour pattern \(v:2,w:1\) identifies the
  center, so the columns are independent.

To see that the first sector is invertible, put \(t_0=r-2\) and
\(d=(r-5)!!\).  On the difference line of the special vertices
\(\{1,2\}\), \(M\) has eigenvalue \(-(t_0-1)d\).  On the sum-zero
subspace of the other \(t_0\) vertices it has eigenvalue \(2d\).  On the
two remaining constant subspaces its determinant is

\[
                    -2(t_0-1)^2(t_0+1)d^2.
\]

Equivalently,

\[
 \det M=2^{r-2}(r-3)^3(r-1)((r-5)!!)^{r}\ne0.            \tag{15}
\]

The three colour sectors have disjoint output supports, so the total rank
is \(3r\).  Its domain has dimension \(3(r+1)\), proving that the kernel
is exactly the local \(V_t\).  Applying this once with \(t=q'\) and once
with \(t=q\) proves (4).

Notice what simultaneous lifting yields here.  After embedding both odd
domains in

\[
 V_q\oplus V_{q'}\oplus\bigoplus_{v\in L}V_v,
\]

every vector compatible with the two displayed kernels is supported only
on \(q,q'\).  It changes the direct \(qq'\)-block and gives no variation
on the common exterior star \(L\).  Dense support and nonzero lower
cofactors do not alter this conclusion.

The scope is deliberately narrower than a cubic target source.  In this
family the complete tensor on \(S_c=L\dot\cup\{q,q'\}\) is

\[
 H_{S_c}=\sum_{\{v,w\}\in\binom L2}2h_{vw}\,
 e_0^{(q)}\otimes e_0^{(q')}\otimes e_1^{(v)}\otimes
 e_1^{(w)}\otimes e_0^{\otimes(L\setminus\{v,w\})}.      \tag{16}
\]

Every coefficient shown is nonzero.  Hence this tensor is mixed and is
not \(\lambda_c^{-1}e_c^{\otimes S_c}\) for any \(c\).  The construction
is an exact internal-quadratic/cofactor countermodel to a rank/nullity
inference only; it does not satisfy even one of the cubic pure-cofactor
equations, and therefore is not a GHZ/Krenn source or counterexample.

## 4. What entry-minimality does and does not remove

For a genuine cubic target source, changing only the aggregate block
\(A_{qq'}\) changes the pure cofactor attached to anchor \(a_c\) by

\[
                         \Delta A_{qq'}\otimes P_c.      \tag{17}
\]

Consequently, if \(P_0=P_1=P_2=0\), the whole block \(A_{qq'}\) is
invisible to all three anchor cofactors.  If it were nonzero, setting it to
zero would preserve the target and reduce support.  Thus an entry-minimal
exact source satisfies the useful but limited implication

\[
 A_{qq'}\ne0\quad\Longrightarrow\quad
                 P_c\ne0\text{ for at least one }c.      \tag{18}
\]

It does not force a prescribed \(P_c\) to be nonzero, nor does it force
two of them to be nonzero.  In particular the two colours carrying the
nullity-web surplus are not excluded from both lying on the boundary
(11).  Also, if either one of the paired maps has nullity at most two,
then (3) immediately forces \(P_c\ne0\); this is a clean way to enter the
faithful-projection chart.

The concrete next step for the cubic route is therefore sharply split:

1. on the open chart \(P_c\ne0\), compare the faithful common-star
   restrictions through the shared nine-equation Hessian system (9),
   including the transpose compatibility of the physical block
   \(A_{qq'}\); and
2. on the boundary \(P_c=0\), use the *pure two-crossing equation* for
   \(H_{S_c}\), not the three units of automatic nullity.  The latter are
   exhausted by the local ports in the sharp family above.

The exact checker
[verify_cubic_nullity_common_cofactor_zero_boundary.py](../computations/verify_cubic_nullity_common_cofactor_zero_boundary.py)
audits (7) with arbitrary asymmetric integral blocks, verifies the
all-even hafnian and determinant formulas, constructs the physical family,
computes both exact deletion maps, and confirms that deleting the direct
\(qq'\)-block is silent precisely because its complete common cofactor is
zero.
