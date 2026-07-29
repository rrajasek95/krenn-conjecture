# An exact target-compatible cap six-plane can be everywhere dirty

## 1. Outcome

At the first descent boundary \(8\to6\), decomposability of the cap
covector does not make the clean-cap equation automatic, even on a
positive-dimensional family on which the selected cap has exactly the
right ternary target.

There is an endpoint-ordered aggregate source \(A\) on

\[
                  \{0,1,2,3,4,5,p,q\}
\]

and a seven-dimensional linear space of cap covectors

\[
 {\cal L}=\{K:K_{00}=K_{11}=K_{22}\}.                    \tag{1}
\]

For every \(K\in{\cal L}\), put

\[
             \lambda=K_{00}=K_{11}=K_{22}.
\]

On the active open set \(\lambda\ne0\),

\[
 s(K)\kappa_0(K)\kappa_1(K)\kappa_2(K)\ne0,
 \qquad
 K\mathbin{\lrcorner}H_8(A)
   =K\mathbin{\lrcorner}\Delta_{8,3}
   =\lambda\Delta_{6,3},                                  \tag{2}
\]

but the exact homogeneous cap error is

\[
 \boxed{
 \mathcal E_{p,q}(K)
   =9\lambda^3\bigl(e_{100100}+6e_{201102}\bigr)\ne0.}    \tag{3}
\]

Projectively, this is an everywhere-dirty active open subset of
\(\mathbf P({\cal L})\cong\mathbf P^6\).  It contains the
two-dimensional torus of rank-one covectors

\[
 K=\phi\otimes\psi,
 \qquad
 \phi_0\psi_0=\phi_1\psi_1=\phi_2\psi_2\ne0.               \tag{1a}
\]

Indeed, after projective normalization its matrices are

\[
 \begin{pmatrix}
 1&t^{-1}&u^{-1}\\
 t&1&t/u\\
 u&u/t&1
 \end{pmatrix}.                                           \tag{1b}
\]

The seven distinct coordinate functions appearing here are the torus characters
\(1,t^{-1},u^{-1},t,t/u,u,u/t\).  Character independence shows that
these rank-one matrices span all of \({\cal L}\).  Thus linearity of the
cap identity upgrades the rank-one family to the full codimension-two
linear statement above.

Thus a projective or resultant argument using only one pair, even on a
projective six-plane of active target-compatible caps, cannot force a clean
point.  The example is local: its full eight-site
matching tensor is not asserted to equal \(\Delta_{8,3}\).  Consequently
it does not refute the global clean-pair target or the conjecture.  It
identifies the missing input as the two target equations transverse to
\({\cal L}\),
or compatibility with other physical pairs.

The universal rank-one specialization makes the obstruction transparent.
For any source and any \(K=\phi\otimes\psi\), put

\[
 P_u=\phi\mathbin{\lrcorner}A_{pu},\qquad
 Q_u=\psi\mathbin{\lrcorner}A_{qu},\qquad
 P=\sum_{u\in U}P_u,\quad Q=\sum_{u\in U}Q_u.
\]

The first-jet correction is exactly

\[
                              r=PQ,                       \tag{3a}
\]

because same-site products vanish and every remaining block is
\(P_uQ_v+Q_uP_v\).  Therefore the \(N=8\) clean equation specializes to

\[
 6\mathcal E_{p,q}(\phi\otimes\psi)
     =\left[P^2Q^2(3s x+PQ)\right]_U.                    \tag{3b}
\]

The square-free algebra has zero divisors, so neither \(P^2Q^2\) nor the
last factor may be cancelled.  The construction below realizes an exact
target-compatible family on which their top-support product is explicitly
nonzero.

## 2. The six-boundary data

Work in the site-square-zero algebra on \(U=\{0,\ldots,5\}\).  Take the
quadratic \(x\) with the following nonzero endpoint-ordered cells:

\[
\begin{array}{c|r@{\qquad}c|r}
(ij;a,b)&x_{ij}(a,b)&(ij;a,b)&x_{ij}(a,b)\\ \hline
(01;1,0)&-1 &(03;0,0)&1\\
(03;1,1)&1 &(04;1,0)&-1\\
(04;1,1)&1 &(05;2,2)&1\\
(12;0,1)&-1 &(12;2,2)&1\\
(13;0,1)&-1 &(14;2,0)&-1\\
(15;1,1)&1/3 &(23;1,1)&1\\
(24;1,0)&-1 &(25;0,0)&1/6\\
(34;1,0)&-1 &(34;2,2)&1/3.
\end{array}                                                 \tag{4}
\]

Let \(P,Q\) be the linear boundary forms with site vectors

\[
\begin{array}{c|cccccc}
u&0&1&2&3&4&5\\ \hline
P_u&0&e_0&0&0&e_0&0\\
Q_u&e_1&e_0+e_2&e_1&e_1&e_0&0.
\end{array}                                                 \tag{5}
\]

The already audited polarized identity for these literal rational data is

\[
                  (x+3PQ){x^2\over2}=\Delta_{6,3}.       \tag{6}
\]

Here \(PQ\) is the square-free product, so its block on \(u<v\) is
\(P_uQ_v+Q_uP_v\).  Equation (6) is coefficientwise on all \(3^6\)
boundary words; it is not a dimension or support-count assertion.

## 3. An actual pair-cap linear space

Put \(x_{uv}\) on the internal blocks of \(A\), and define the cap-incident
blocks by

\[
 A_{pq}=3e_0^{(p)}e_0^{(q)},\qquad
 A_{p u}=3e_0^{(p)}P_u,\qquad
 A_{q u}=e_0^{(q)}Q_u.                                  \tag{7}
\]

All unlisted cap-incident blocks vanish.  For an arbitrary bilinear
covector \(K\), put

\[
 \lambda=K_{00},
 \qquad \kappa_c=K_{cc}.
\]

Because every nonzero cap endpoint in (7) has colour zero, the direct cap
scalar and first-jet quadratic are literally

\[
                         s=3\lambda,
 \qquad                   r=3\lambda PQ.                \tag{8}
\]

Sorting the perfect matchings according to whether they use \(pq\) gives

\[
\begin{aligned}
 K\mathbin{\lrcorner}H_8(A)
   &=3\lambda {x^3\over6}
     +3\lambda PQ{x^2\over2}\\
   &=\lambda (x+3PQ){x^2\over2}
    =\lambda\Delta_{6,3}.                               \tag{9}
\end{aligned}
\]

On the linear space \({\cal L}\), the target cap is also

\[
 K\mathbin{\lrcorner}\Delta_{8,3}
   =\sum_{c=0}^2\kappa_cX_c
   =\lambda\Delta_{6,3},                                \tag{10}
\]

and \(s\prod_c\kappa_c=3\lambda^4\ne0\).  Equations
(7)--(10) prove the source-level and target-level assertions in (2), with
no representative modulo an annihilator.

## 4. Exact failure of cleanliness

The canonical effective quadratic is independent of the active point of
\({\cal L}\):

\[
                         y=x+{r\over s}=x+PQ.            \tag{11}
\]

Exact enumeration of its fifteen perfect matchings gives the particularly
small defect

\[
             3H_6(y)-\Delta_{6,3}
                  =e_{100100}+6e_{201102}.               \tag{12}
\]

Hence

\[
 sH_6(y)-K\mathbin{\lrcorner}H_8(A)
   =\lambda\bigl(e_{100100}+6e_{201102}\bigr).           \tag{13}
\]

At \(h=3\), the definition of the denominator-cleared clean error is

\[
 \mathcal E_{p,q}(K)
   ={s r^2x\over2}+{r^3\over6}
   =s^2\left(sH_6(y)-K\mathbin{\lrcorner}H_8(A)\right). \tag{14}
\]

Substitution of \(s=3\lambda\) into (13)--(14) proves (3).

There is also a one-line saturation certificate.  In the coordinate ring
of all cap covectors put \(\lambda_i=K_{ii}\); the six off-diagonal
coordinates remain free.  Set

\[
 J=(\lambda_1-\lambda_0,\lambda_2-\lambda_0),\qquad
 I=J+(\lambda_0^3).                                     \tag{15}
\]

The nonzero coordinate in (3) makes \(I\) the error ideal on the
target-compatible linear locus.  For the activity polynomial

\[
                         a/3=\lambda_0^2\lambda_1\lambda_2,
\]

the exact identity

\[
 {a\over3}
 =\lambda_0^2\lambda_2(\lambda_1-\lambda_0)
  +\lambda_0^3(\lambda_2-\lambda_0)
  +\lambda_0\lambda_0^3                              \tag{16}
\]

shows \(a\in I\).  Therefore

\[
                              I:a=(1).                   \tag{17}
\]

The active clean locus is empty on the entire projective six-plane, not
merely on its two-dimensional rank-one torus.

## 5. Exact bridge to the all-even problem

This countertheorem closes only a proof strategy, not the descent theorem.
For a genuine exact eight-site source, the equality in (10) holds for
**every** bilinear covector, whereas the local family above agrees with it
only on the codimension-two linear space \({\cal L}\).  Thus the first information capable
of ruling out this obstruction is the full target equation in the two
traceless-diagonal directions transverse to \({\cal L}\), together with
its literal common-edge
source provenance.  A second complete pair slice or its top Bianchi
reindexing does not add that information; an overlapping-pair argument is
useful only if it retains the lower cofactor/source-variable compatibility
discarded by the reindexing.

At arbitrary even order, the same lesson persists: decomposability makes
the first-jet correction \(r=PQ\), but it does not kill the higher
top-support powers of \(r\).  An all-even descent must use simultaneous
source provenance across cap charts; Segre intersection theory for one
active pair cannot supply the missing zero.

The lightweight checker
[`verify_n8_rank_one_clean_cap_local_torus_obstruction.py`](../computations/verify_n8_rank_one_clean_cap_local_torus_obstruction.py)
reuses the frozen rational data in the polarized pair-cap audit, checks
(6) and (12) on all 729 words, verifies (14), checks an exact seven-point
rank certificate for the torus span, and checks the polynomial membership
certificate (16).
