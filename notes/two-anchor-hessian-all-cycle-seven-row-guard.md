# Every dark cycle can fail before the two unused anchors

## 1. Outcome

The corank-one guard in
[the physical dark-cut audit](physical-dark-cut-hessian-kernel-counterlift.md)
does not by itself refute an *existential* Hessian pullback: its
complementary matching has a second edge which gives a compatible cycle.
The packet below repairs that weakness.

On six residual sites it has a literal full-selector cap

\[
             \beta=p_0s_0=x_{0,a}x_{1,a},\qquad
             \beta q^{[2]}=X_a,                         \tag{1}
\]

an invertible direct block, injective endpoint triples, exactly two
target-blocked sites, and a unique complementary dark perfect matching

\[
                              25\mid34.                  \tag{2}
\]

There are four possible four-cycle covectors obtained by choosing either
edge of (2) and either cross pairing with the cap edge \(01\).  The scalar
\(K_6\) Hessian has corank one, and **all four covectors fail to annihilate
its kernel**.  Thus choosing the other edge or reversing the orientation
cannot repair aggregate compatibility.

This assertion is deliberately about the four individual choices.  The
subsequent [cycle-span mixing lemma](k6-cycle-span-hessian-mixing.md) shows
that a linear combination of two orientations *does* annihilate the kernel
while retaining nonzero cap detection.  Source-validity of that mixture is
a separate filtered-overlap question.

The decorated packet satisfies the selected diagonal row and all six
off-diagonal rows.  It fails exactly the other two diagonal tensor anchors:

\[
                       0\ne X_b,\qquad 0\ne X_\delta.   \tag{3}
\]

Consequently neither an existential choice among the dark matching's
cycles, nor endpoint injectivity, nor invertibility of the direct block can
replace those two anchors.  Conversely, this is still a seven-row boundary,
not a complete full-nine source.  Proving that the two independent tensors
in (3) force a compatible selector is the genuine one-chart eight-site
step; asserting it from this guard would be circular.  A second chart could
instead contribute a grade-preserving relation coupling one of (3) to the
same scalar Hessian kernel.  No such overlap datum is present here.

This note concerns only the aggregate Hessian condition.  Even a compatible
cycle would still have to pass the separate filtered-provenance and
Macaulay-prolongation tests.

## 2. The decorated seven-row packet

Let \(W=\{0,\ldots,5\}\), with local basis
\(e_a,e_b,e_\delta\).  In the site-square-zero algebra put

\[
\begin{aligned}
 Q=\{&01,02,03,04,05,13,14,23,25,34\},\\
 q&=\sum_{ij\in Q}x_{i,a}x_{j,a}.                       \tag{4}
\end{aligned}
\]

Use the endpoint triples

\[
 (p_0,p_1,p_2)=(x_{0,a},x_{1,a},x_{2,a}),\qquad
 (s_0,s_1,s_2)=(x_{1,a},x_{0,a},x_{3,a}).               \tag{5}
\]

Both maps from the row-label space to the direct sum of the six local
spaces are injective.  There are four supported perfect matchings in
\(q^{[3]}\):

\[
 01\mid25\mid34,\quad03\mid14\mid25,\quad
 04\mid13\mid25,\quad05\mid14\mid23.                    \tag{6}
\]

Hence \(q^{[3]}=4X_a\).  The response coefficients are

\[
 p_i s_jq^{[2]}=T_{ij}X_a,\qquad
 T=\begin{pmatrix}
 1&0&1\\
 0&1&1\\
 1&0&1
 \end{pmatrix}.                                         \tag{7}
\]

Set

\[
 d={E_{00}-T\over4}
  =\begin{pmatrix}
     0&0&-1/4\\
     0&-1/4&-1/4\\
     -1/4&0&-1/4
    \end{pmatrix},qquad \det d={1\over64}.             \tag{8}
\]

Then, simultaneously for all nine cells,

\[
              d_{ij}q^{[3]}+p_i s_jq^{[2]}
                         =(E_{00})_{ij}X_a.              \tag{9}
\]

Thus (9) is exactly the six off-diagonal full-nine equations and the
\((0,0)\) diagonal equation with \(0=a\).  Its \((1,1)\) and \((2,2)\)
left sides are zero rather than \(X_b\) and \(X_\delta\).  These are the
only failed rows.

The selector \(\ell=E_{00}\) is rank one and direct zero because
\(\ell(d)=d_{00}=0\).  It gives (1).  Its local cap planes are

\[
 H_0=H_1=\mathbb C e_a,\qquad H_2=H_3=H_4=H_5=0,         \tag{10}
\]

so \(B_a=\{0,1\}\).  Contract sites \(0,1\) by \(e_a^*\).  On the other
four sites the unique supported matching is precisely (2), and hence the
blocked-site quotient is the pure identity

\[
 \beta_{01}(e_a^*,e_a^*)
       (q|_{\{2,3,4,5\}})^{[2]}
      =x_{2,a}x_{3,a}x_{4,a}x_{5,a}.                    \tag{11}
\]

At edge \(01\), the two oriented endpoint products from (5) are
\(E_{00}\) and \(E_{11}\).  Since \(q_{01}=1\), the selected functional
detects the first transition \(d-E_{00}\) with value \(-1\).  Thus the
packet also retains same-edge transition visibility.

## 3. All four Hessian failures

Probe every residual site by \(e_a^*\), and let the resulting scalar edge
array again be denoted \(q\).  Its support is \(Q\).  The complementary
four-set to \(01\) has exactly the matching (2).  For a matched edge
\(uv\in\{25,34\}\), write its two four-cycle functions as

\[
\begin{aligned}
 \kappa_{uv}^{(0)}(r)&=r_{01}r_{uv}-r_{0u}r_{1v},\\
 \kappa_{uv}^{(1)}(r)&=r_{01}r_{uv}-r_{0v}r_{1u}.        \tag{12}
\end{aligned}
\]

Every one detects the selected cap:

\[
                   d\kappa_{uv}^{(\epsilon)}{}_q(\beta)=q_{uv}=1.
                                                               \tag{13}
\]

The hafnian Hessian \(H_q\), indexed by the fifteen edges, has

\[
                 \operatorname{rank}H_q=14,
 \qquad
 z=\mathbf e_{01}-\mathbf e_{04}-\mathbf e_{12}
                         +\mathbf e_{24}\in\ker H_q.    \tag{14}
\]

Direct evaluation gives

\[
\begin{array}{c|cccc}
 (uv,\epsilon)&(25,0)&(25,1)&(34,0)&(34,1)\\ \hline
 d\kappa_{uv}^{(\epsilon)}{}_q(z)&1&2&1&2.
\end{array}                                               \tag{15}
\]

All four values are nonzero.  Since \(H_q\) is symmetric, (14)--(15)
prove

\[
 d\kappa_{uv}^{(\epsilon)}{}_q\notin\operatorname{row}H_q
 \qquad(uv\in\{25,34\},\ \epsilon\in\{0,1\}).          \tag{16}
\]

This exhausts the literal coefficient-cut choices supplied by the unique
dark matching.  In particular the obstruction is not tied to a prescribed
matching edge or orientation.

## 4. Exact scope

The guard proves that the following seven-row data do not imply even one
aggregate-compatible dark cycle:

* a rank-one, direct-zero, target-active full selector;
* the pure two-site blocked-target quotient and a unique dark matching;
* all choices of matching edge and cross orientation;
* injective endpoint triples, an invertible direct block, and a visible
  literal transition;
* the selected diagonal equation and all six off-diagonal equations.

The omitted hypothesis is not a scalar normalization.  It is the pair of
sitewise independent tensor identities

\[
 d_{11}q^{[3]}+p_1s_1q^{[2]}=X_b,qquad
 d_{22}q^{[3]}+p_2s_2q^{[2]}=X_\delta.                  \tag{17}
\]

In the guard both left sides are zero and every nonzero top tensor lies on
the single line \(\mathbb C X_a\).  The seven-row packet alone therefore
does not satisfy a scalar replacement which assigns nonzero values to the
two omitted targets.  There is, however, an exact scalar shadow showing
that such a replacement still cannot close the gap.  For arbitrary
\(c_b,c_\delta\), replace (8) by

\[
 d(c_b,c_\delta)=d+{c_b\over4}E_{11}+{c_\delta\over4}E_{22}.
                                                               \tag{18}
\]

All endpoint stars, the selected cap, the dark matching, and the Hessian
are unchanged, while the complete scalar row ledger becomes

\[
 d(c_b,c_\delta)_{ij}q^{[3]}+p_i s_jq^{[2]}
  =\operatorname {diag}(1,c_b,c_\delta)_{ij}X_a.          \tag{19}
\]

Taking, for example, \((c_b,c_\delta)=(2,3)\) makes all three scalar
targets nonzero and leaves the direct block invertible, with determinant
\(-1/64\).  Thus even all nine equations after collapsing the targets to
one tensor line retain the four Hessian failures.  What distinguishes the
physical missing rows (17) is their six sitewise colour factors.  A proof
must retain those factors, or import an equivalent same-label relation
from an overlapping chart; a cofactor-rank condition alone also cannot
close the gap.

The dependency-free checker
[`verify_two_anchor_hessian_all_cycle_seven_row_guard.py`](../computations/verify_two_anchor_hessian_all_cycle_seven_row_guard.py)
audits the matching expansions, the nine-cell ledger, the exact missing
tensor rows, the all-nine scalar shadow, the dark quotient, the direct
determinants, the Hessian kernel, and all four augmented-rank failures.
