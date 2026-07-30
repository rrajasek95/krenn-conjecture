# Cubic packet propagation: six exceptional types and an order-eighteen core

## 1. Outcome

Let \(B\) have even size \(N\geq8\), let an entry-minimal aggregate source
satisfy

\[
                         H_B(A)=\Delta_{B,3},                    \tag{1}
\]

and suppose \(p\) is cubic.  Use the cubic normal form

\[
 A_{pa_c}=\lambda_c e_c^{(p)}\otimes e_c^{(a_c)},\qquad
 H_{B\setminus\{p,a_c\}}(A)
   =\lambda_c^{-1}e_c^{\otimes(B\setminus\{p,a_c\})}            \tag{2}
\]

for distinct anchors \(a_0,a_1,a_2\), and put

\[
                 R=B\setminus\{p,a_0,a_1,a_2\}.                \tag{3}
\]

For \(q\in R\), let
\(E_q=\{c:\dim\ker\Phi_{q,c}=1\}\) be the set of nullity-one anchor
colours in the cubic leave-one-anchor web.  The map \(\Phi_{q,c}\) is
defined on the fixed site set \(B\setminus\{p,q,a_c\}\), so \(E_q\)
depends on \(q\), not on any later choice of \(q'\).  Thus
\(|E_q|\leq1\).  For distinct \(q,q'\in R\), use the faithful-surplus
versus pure-crossing dichotomy of
[the preceding cubic reduction](cubic-two-nonneighbour-faithful-surplus-dichotomy.md).

**Theorem 1 (six-type propagation).**  Either some residual pair
\(q\ne q'\) in \(R\) is in the faithful-surplus alternative, or there is a set

\[
                         X\subseteq R,\qquad |X|\leq6,           \tag{4}
\]

with all of the following properties.

1. Every \(x\in X\) has a unique ordered type
   
   \[
                         \tau(x)=(c,\rho),\qquad c\ne\rho,       \tag{5}
   \]
   
   and the six possible types are used at most once.
2. The complete colour-\(\rho\) row of the \(x\)-star is supported only
   at \(a_c\).  In fact, for a nonzero scalar \(\mu_x\),
   
   \[
   (e_\rho^*\otimes\operatorname{id})A_{x\mid a_c}
       =\mu_xe_\rho^{(a_c)},\qquad
   H_{B\setminus\{x,a_c\}}(A)
       =\mu_x^{-1}e_\rho^{\otimes(B\setminus\{x,a_c\})}.        \tag{6}
   \]
   
   Thus every exceptional type is a literal monochromatic pure port,
   not merely a zero row in a residual block.
3. If \(I=R\setminus X\), then
   
   \[
                              A_{qq'}=0\qquad(q\ne q'\text{ in }I). \tag{7}
   \]
   
   Hence \(X\) is a vertex cover of the aggregate support induced on
   \(R\), and every \(q\in I\) has block degree at most
   
   \[
                               d_A(q)\leq |X|+3\leq9.            \tag{8}
   \]
4. The pure anchor cofactors in (2) force
   
   \[
                              |I|\leq |X|+2.                    \tag{9}
   \]
   
   Consequently
   
   \[
                              N\leq18.                          \tag{10}
   \]

In particular, at every even order \(N\geq20\), an entry-minimal exact
source with a cubic centre has a faithful residual pair.  No assumption
about canonical-transition flatness elsewhere in the source is used.
For the bounded orders, avoidance of the faithful chart forces

\[
 |X|\geq {N-6\over2};                                      \tag{11}
\]

thus the lower bounds on \(|X|\) at orders
\(8,10,12,14,16,18\) are respectively \(1,2,3,4,5,6\).

If the source is also order-minimal above four, the cubic selectors give a
more localized statement.  For each \(r\in\{0,1,2\}\), with
\(\{r,s,t\}=\{0,1,2\}\), there are distinct

\[
                         u_{r,s},u_{r,t}\in R                  \tag{12}
\]

such that

\[
 H_{R\setminus\{u_{r,s},u_{r,t}\}}(A)\ne0.                 \tag{13}
\]

If \(d_r\) of these two endpoints lie in \(I\), then

\[
                 |I|-d_r\leq |X|-(2-d_r).                    \tag{14}
\]

At the extremal order \(N=18\), avoidance of the faithful chart therefore
forces all six types to occur and, for every \(r\), both selected selector
endpoints to lie in \(I\).  Every nonzero matching witnessing (13) then matches
\(I\setminus\{u_{r,s},u_{r,t}\}\) bijectively into \(X\).

This is a propagation theorem, not a completion of the cubic branch.  At
\(N=8\) it guarantees at least one pure exceptional port and the cover
(7), but it does not contradict the remaining four-site residual core.
At orders at most eighteen it leaves a bounded typed core; at larger
orders it forces the faithful-Hessian packet, whose closure remains a
separate gate.

## 2. An exceptional nullity-one map is a pure physical port

Assume henceforth that no pair in \(R\) takes the faithful-surplus
alternative, and define

\[
                         X=\{q\in R:E_q\ne\varnothing\}.         \tag{15}
\]

Fix \(q\in X\), write \(E_q=\{c\}\), and use the exact nullity-one
classification in
[the cubic nullity web](cubic-vertex-leave-one-anchor-nullity-web.md).
It supplies a unique wrong colour \(\rho\ne c\) whose entire \(q\)-star
row, after deleting \(p\), is supported at \(a_c\).  Since \(A_{qp}=0\),
this is also the support of the full physical row:

\[
 (e_\rho^*\otimes\operatorname{id})A_{q\mid v}=0
                    \qquad(v\notin\{q,a_c\}).                  \tag{16}
\]

Expand the full target at \(q\) and contract its \(q\)-slot by
\(e_\rho^*\).  Equation (16) leaves one term:

\[
 \bigl((e_\rho^*\otimes\operatorname{id})A_{q\mid a_c}\bigr)
       \otimes H_{B\setminus\{q,a_c\}}(A)
       =e_\rho^{\otimes(B\setminus\{q\})}.                    \tag{17}
\]

Both factors on the left are nonzero.  Uniqueness of the factors of a
nonzero decomposable tensor proves (6).  This step uses the full target
row; the residual zero-row statement alone would not imply purity.

The type map \(\tau(q)=(c,\rho)\) is injective.  Indeed, suppose distinct
\(q,q'\in X\) had the same type.  At the common physical centre \(a_c\),
the two nonzero scalar cells of colour \(\rho\) at both endpoints have
unweighted derivative tensors

\[
 \begin{aligned}
 T_q&=e_\rho^{(a_c)}\otimes e_\rho^{(q)}\otimes
       H_{B\setminus\{a_c,q\}}(A)
          =\mu_q^{-1}e_\rho^{\otimes B},\\
 T_{q'}&=e_\rho^{(a_c)}\otimes e_\rho^{(q')}\otimes
       H_{B\setminus\{a_c,q'\}}(A)
          =\mu_{q'}^{-1}e_\rho^{\otimes B}.
 \end{aligned}                                               \tag{18}
\]

They are proportional.  Star irredundancy at \(a_c\) says that derivative
tensors belonging to nonzero entries on one physical star are linearly
independent.  Equivalently, because every matching uses only one edge at
\(a_c\), a suitable simultaneous variation of these two cells preserves
the full tensor exactly and can zero one of them.  Either formulation
contradicts entry-minimality.  There are only the six ordered pairs
\((c,\rho)\) with \(c\ne\rho\), proving (4)--(6).

## 3. Overlapping residual pairs produce a six-vertex cover

Take distinct \(q,q'\in I=R\setminus X\).  Then

\[
                              E_q=E_{q'}=\varnothing.            \tag{19}
\]

For this pair put

\[
 P_c(q,q')=H_{B\setminus\{p,a_c,q,q'\}}(A).                    \tag{20}
\]

The two-nonneighbour dichotomy is exact: because the faithful alternative
has been excluded, its concentrated alternative gives

\[
                              P_c(q,q')=0\qquad(c=0,1,2).       \tag{21}
\]

Expand the complete cofactor of the physical block \(qq'\) at the cubic
centre \(p\).  Using (2) only for the three incident blocks gives

\[
 \begin{aligned}
 H_{B\setminus\{q,q'\}}(A)
   &=\sum_{c=0}^2\lambda_c e_c^{(p)}\otimes e_c^{(a_c)}
                      \otimes P_c(q,q')\\
   &=0.                                                       \tag{22}
 \end{aligned}
\]

If \(A_{qq'}\ne0\), any one of its nonzero scalar entries would have zero
global derivative tensor by (22), contrary to star irredundancy.  Hence
(7) holds.  Since \(A_{qp}=0\) and every other site belongs to either the
three anchors, \(X\), or \(I\setminus\{q\}\), equation (8) follows.

This is where overlap matters.  The exceptional set and its types are
attached to a single residual vertex \(q\), independently of the second
vertex \(q'\).  Treating every pair as an unrelated abstract Hessian
packet would not produce the common cover \(X\).

## 4. The three pure anchor cofactors bound the core

Fix \(c\in\{0,1,2\}\).  The coefficient of the constant-\(c\) word in the
second identity of (2) is nonzero.  Therefore at least one physical
perfect matching with nonzero cell product occurs on

\[
              B\setminus\{p,a_c\}
                 =R\mathbin{\dot\cup}\{a_s,a_t\},
              \qquad\{c,s,t\}=\{0,1,2\}.                     \tag{23}
\]

This conclusion is cancellation-safe: a nonzero complete coefficient
cannot be a sum of only zero matching products.  No assertion is made that
the other products fail to cancel.

By (7), no two vertices of \(I\) can be paired together.  In the matching
from (23), every vertex of \(I\) must consequently be paired either with a
distinct vertex of \(X\) or with one of the two surviving anchors
\(a_s,a_t\).  This injects \(I\) into a set of size \(|X|+2\) and proves
(9).  Since

\[
                         N=4+|X|+|I|,                           \tag{24}
\]

equations (4), (9), and (24) give (10), while rearranging them gives
(11).

The argument is entirely local to the cubic centre and its three actual
pure cofactors.  Curvature or nonflat transition data elsewhere neither
enters nor invalidates it.

## 5. The selectors leave a near-perfect residual matching

Now assume in addition that the source is order-minimal above four.  For
fixed \(r\), [the cubic-selector theorem](cubic-selector-reduction.md)
defines

\[
 Q_r=D^2H_{B\setminus\{p,a_r\}}(A)[R_s,R_t],
                 \qquad\{r,s,t\}=\{0,1,2\},                    \tag{25}
\]

and proves \(Q_r\ne0\).  Expand \(Q_r\) as the finite sum over pairs of
disjoint selector edges.  Since the sum is nonzero, at least one raw
summand is a nonzero tensor; this uses no termwise noncancellation
assumption.  Such a summand chooses an \(R_s\)-edge from \(a_s\) to a
residual endpoint \(u_{r,s}\), an \(R_t\)-edge from \(a_t\) to a distinct
residual endpoint \(u_{r,t}\), and a nonzero complete matching tensor on
the sites left over.  Those sites are exactly

\[
 B\setminus\{p,a_r,a_s,a_t,u_{r,s},u_{r,t}\}
       =R\setminus\{u_{r,s},u_{r,t}\}.                         \tag{26}
\]

This proves (12)--(13), including their physical common-edge provenance.
Choose a nonzero coefficient of (13) and one contributing matching.  If
\(d_r\) deleted endpoints belong to \(I\), the remaining sides of the
cover have sizes

\[
                        |I|-d_r,\qquad |X|-(2-d_r).             \tag{27}
\]

Every remaining \(I\)-vertex must be matched to a distinct remaining
\(X\)-vertex, so (14) follows.

At \(N=18\), equations (4), (9), and (24) force

\[
                         |X|=6,\qquad |I|=8.                    \tag{28}
\]

Substitution in (14) gives \(8-d_r\leq4+d_r\), hence \(d_r=2\).
After deleting the two \(I\)-endpoints, both sides have size six, so the
witnessing matching is a bijection from the remaining \(I\) to \(X\).
This proves the extremal statement without enumerating the six types or
their incidences.

## 6. Scope and remaining gate

The theorem removes the possibility that pure-crossing packets can remain
independent across an arbitrarily large residual set.  Their physical
provenance forces one of two uniform outcomes:

1. a faithful tensor-valued Hessian packet already occurs; or
2. all activity internal to \(R\) is incident with six typed pure ports,
   every other residual star is sparse, and the full source has order at
   most eighteen.

It does not classify the one-dimensional cross-image on the faithful
chart.  It also does not eliminate the bounded nonfaithful cores at orders
\(8\) through \(18\).  In particular, the \(N=8\) consequence is the
existence of at least one typed pure port together with (7), rather than a
proof of impossibility.  These qualifications are essential: neither raw
Hessian nullity nor one isolated pure \(3\times3\) packet implies the
global cover or the order bound without the shared physical maps,
entry-minimality, and the three cubic cofactors used above.
