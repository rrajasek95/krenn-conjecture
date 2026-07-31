# Scalar-unit pivots have a strict global anchor potential, but good-pair abundance does not make them recur

## 1. Outcome

Let \(B\) have even size \(N\), let the endpoint-colour spaces have the
fixed bases \(e_0,e_1,e_2\), and let the aggregate blocks \(A_{uv}\) be an
exact ternary source.  At a good physical pair \(p,q\), suppose

\[
 A_{pq}=\alpha E_{aa},\qquad \alpha\ne0,                 \tag{1}
\]

and use the full-nine notation

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
      +R_{ij}q^{[h-1]}=\delta_{ij}X_i,\qquad
 R_{ij}=p_i s_j.                                         \tag{2}
\]

Put

\[
 G=\alpha q+R_{aa},\quad
 U=G^{[h]}-\alpha^{h-1}X_a,\quad
 \Theta=G^{[h-1]}-\alpha^{h-1}q^{[h-1]}.                 \tag{3}
\]

If

\[
 U=0,\qquad R_{ij}\Theta=0\quad(i,j\in\{b,c\}),          \tag{4}
\]

then the proposed scalar-unit pivot is exact: replace

\[
 q\longmapsto q^\#=q+\alpha^{-1}p_as_a                 \tag{5}
\]

and set the complete residual star rows \(p_a,s_a\) to zero, leaving the
direct cell \(\alpha E_{aa}\) and all complementary rows unchanged.  The
result is another exact ternary source on the same physical sites.

There is a strict global potential for this move.  Form the scalar support
graph whose vertices are the \(3N\) physical coordinate channels

\[
                         (u,i),\qquad u\in B, i\in\{0,1,2\},             \tag{6}
\]

and whose edges are the nonzero aggregate scalar cells
\(A_{uv}(i,j)\).  Call an edge a **mutual coordinate anchor** if both of
its coordinate endpoints have degree one in this graph, and write
\(\nu(A)\) for the number of such edges.  Then

\[
                    \boxed{\nu(A^\#)\geq\nu(A)+1.}        \tag{7}
\]

Every old mutual coordinate anchor survives literally.  The new one is

\[
                         (p,a)---(q,a).                    \tag{8}
\]

Thus \(\nu\), or lexicographically
\(\bigl(\nu,-|\operatorname{supp}A|\bigr)\), is
a well-founded global pivot potential.  Since the anchor edges are
vertex-disjoint,

\[
                              \nu(A)\leq {3N\over2}.       \tag{9}
\]

The endpoint statement is stronger than ordinary essential-neighbour
status: after the pivot the selected coordinate at each endpoint is
carried by the other endpoint and by no other scalar cell.

Every degree-one coordinate channel in an exact source is necessarily
monochromatic.  Indeed, the nonzero all-\(i\) target coefficient must use
the unique cell incident to \((u,i)\), so that cell's other endpoint also
has colour \(i\).  Hence the anchor potential decomposes as
\(\nu=\nu_0+\nu_1+\nu_2\), with \(\nu_i\leq N/2\), and a colour-\(a\)
pivot raises \(\nu_a\).  This refinement is sometimes useful when the
selected scalar-unit colour is controlled.

At the top value in (9), no exact ternary source exists for \(N\geq6\).
Indeed, exactness forces the anchor graph to be three monochromatic
perfect matchings.  The standard three-one-factors lemma supplies a fourth,
mixed perfect matching, and its coefficient fibre is a singleton of
nonzero weight.  This contradicts the diagonal target.  The threshold is
sharp: the three one-factors of \(K_4\) give an exact saturated source at
\(N=4\).

Consequently the scalar pivot would close the conjecture if it were
**recurrent**:

> If every same-order exact pivot descendant admitted another good
> scalar-unit pair satisfying (4), repeated pivots would reach (9) after
> at most \(3N/2-\nu(A)\) steps, contradicting the terminal theorem.

Equivalently, among all exact sources of a fixed order choose one maximizing
\(\nu\).  At every intrinsic good scalar-unit pair of that representative,

\[
 \boxed{U\ne0\quad\hbox{or}\quad
       (R_{bb}\Theta,R_{bc}\Theta,R_{cb}\Theta,R_{cc}\Theta)\ne0.}      \tag{10}
\]

This is an exact global alternative, not a local Taylor heuristic.

The current theorems do not supply recurrence.  The
[essential-star theorem](target-flattening-essential-star-pair-bound.md)
produces many good physical pairs, but says nothing about their direct
blocks being nonzero scalar units, and the
[curvature-line theorem](unconditional-curvature-line-selection.md) uses
a minimum-entry-support representative rather than a maximum-\(\nu\)
representative.  A sharp carrier model below has the maximum possible
anchor count and still has quadratically many good pairs, every one with
zero direct block.  Thus good-pair counting alone cannot bridge this
selection gap.

There is nevertheless a useful support-minimal refinement.  Choose first
a minimum-entry-support exact representative and then maximize \(\nu\)
inside that minimum stratum.  If (4) holds, its pivot must strictly
increase entry support.  If

\[
 r=|\operatorname{supp}p_a|,\qquad
 t=|\operatorname{supp}s_a|,                              \tag{11}
\]

then

\[
                         \boxed{(r-1)(t-1)\geq2.}          \tag{12}
\]

In particular both selected star rows have at least two scalar cells and
one has at least three.  Without the secondary maximum-\(\nu\) choice,
plain minimum support still gives \(r,t\geq2\).  These bounds are sharp for
the support-transfer ledger: a \(2\)-by-\(3\) fresh rank-one rectangle adds
six internal cells while deleting five star cells.  Hence entry support
does not itself orient the pivot in the desired direction.

This note proves a global potential and isolates its exact missing input;
it does not prove recurrence, an active clean cap, or Krenn's conjecture.

## 2. Exactness of the same-order pivot

Since \(q^\#=\alpha^{-1}G\), the unary equality in (4) gives

\[
                  \alpha(q^\#)^{[h]}=X_a.                \tag{13}
\]

At adjacent power,

\[
 (q^\#)^{[h-1]}-q^{[h-1]}
             =\alpha^{-(h-1)}\Theta.                     \tag{14}
\]

Therefore, for \(i,j\in\{b,c\}\), equations (2), (4), and (14) give

\[
 R_{ij}(q^\#)^{[h-1]}
   =R_{ij}q^{[h-1]}+\alpha^{-(h-1)}R_{ij}\Theta
   =\delta_{ij}X_i.                                      \tag{15}
\]

After setting \(p_a=s_a=0\), every response with exactly one endpoint
label \(a\) is zero, as its target row is.  The \(aa\)-row is (13), carried
only by the direct edge, and the four complementary rows are (15).
Expanding the complete matching tensor at \(p,q\) proves that all nine
target rows are unchanged.  Thus the pivot is an exact aggregate source;
expanding each nonzero aggregate cell as one decorated quadratic source
gives a finite decorated source as usual.

No cancellation of a matching power is used.  Conditions (4) are exactly
what is needed for this construction; goodness is used below to make its
potential increase strict.

## 3. The anchor-persistence lemma

For \(x\in W=B\setminus\{p,q\}\), write

\[
 P_x=(p_a)|_{V_x},\qquad S_x=(s_a)|_{V_x}.                \tag{16}
\]

In scalar block form the only internal changes are

\[
 A^\#_{xy}=A_{xy}+\alpha^{-1}
        (P_x\otimes S_y+S_x\otimes P_y),\qquad x\ne y,   \tag{17}
\]

with endpoint order restored in the displayed tensors.  Same-site terms
are zero in the site-square-zero algebra.  The \(a\)-row at \(p\) and the
\(a\)-row at \(q\) are deleted off the direct pair; all other incident rows
are unchanged.

**Lemma 3.1 (anchor persistence).** Every mutual coordinate anchor of
\(A\) is a mutual coordinate anchor of \(A^\#\), with the same coefficient.

**Proof.** Let an old anchor join \(u,i\) to \(v,j\).

Suppose first that \(u,v\in W\).  Since \(u,i\) has no incident support
other than this edge and neither \(p\) nor \(q\) is \(v\),

\[
                         P_u(i)=S_u(i)=0.                 \tag{18}
\]

The identical statement holds at \(v,j\).  Formula (17) consequently
has zero complete \(i\)-row at \(u\) and zero complete \(j\)-row at \(v\).
It neither changes the anchor coefficient nor creates another cell at
either endpoint.

Now suppose \(u=p\) and \(v\in W\).  One cannot have \(i=a\): the direct
cell in (1) would be a second edge at \(p,a\).  Hence \(i\ne a\), so the
anchor row at \(p\) is not deleted.  At its other endpoint, degree one
implies

\[
                         P_v(j)=S_v(j)=0,                 \tag{19}
\]

because a nonzero \(P_v(j)\) would be a second cell from \((v,j)\) to
\((p,a)\), while a nonzero \(S_v(j)\) would be a cell to \(q\).  Thus (17)
creates no new cell at \(v,j\).  The cases with \(q\), or with the
endpoint order reversed, are identical.  The direct block (1) contains no
old anchor in any other coordinate, and its \(aa\)-cell was not an old
anchor because goodness gives \(p_a\ne0\) and \(s_a\ne0\).  This exhausts
the cases. \(\square\)

After the pivot, (1) is the only cell at either \(p,a\) or \(q,a\), so
it is a new mutual anchor.  Goodness makes both old residual rows nonzero,
so neither selected coordinate was previously anchored.  Lemma 3.1 proves
(7).

The mutual qualifier is essential.  A coordinate vertex of degree one
whose other endpoint has larger degree need not remain degree one: a later
pivot can remove its sole cell and redistribute that coordinate through
the rank-one rectangle (17).  Counting all one-sided essential or
degree-one channels is therefore not a monotone substitute for \(\nu\).

## 4. Global potential and the recurrence theorem

The anchor edges form a matching on the \(3N\) coordinate vertices, which
proves (9).  The lexicographic integer pair

\[
                         (\nu(A),-|\operatorname{supp}A|)               \tag{20}
\]

strictly increases at every pivot.  If a scalar-valued potential is
preferred, put

\[
 M=9\binom N2,\qquad
 \Phi(A)=(M+1)\nu(A)-|\operatorname{supp}A|.              \tag{21}
\]

Since an aggregate source has at most \(M\) scalar cells, (7) gives

\[
                         \Phi(A^\#)>\Phi(A).              \tag{22}
\]

In fact the simpler quantity \(\nu\) already bounds the length of every
pivot chain.

**Theorem 4.1 (conditional recurrent-pivot contradiction).** Let \(N\ge6\)
be even.  There is no nonempty class of exact ternary sources on \(B\)
which is closed under the pivot of Section 2 and in which every member has
an admissible good scalar-unit pair satisfying (4).

**Proof.** Start with any member and repeatedly use the assumed pair.  By
(7), after at most \(3N/2-\nu(A)\) moves one obtains an exact member with
\(\nu=3N/2\).  Section 5 proves that no such exact member exists. \(\square\)

Since \(\nu\) takes finitely many values, any nonempty set of exact sources
has a maximum-\(\nu\) member.  Applying (7) to such a member proves (10).
Notice the quantifier: (10) constrains scalar-unit good pairs which already
exist on that chosen representative.  It does not transport the
minimum-support curvature pair to the maximum-\(\nu\) representative.

## 5. The saturated-anchor terminal obstruction

**Theorem 5.1.** If \(N\ge6\) is even and
\(H_B(A)=\Delta_{B,3}\), then

\[
                              \nu(A)<{3N\over2}.           \tag{23}
\]

**Proof.** If equality held, every physical coordinate vertex would be an
endpoint of a mutual anchor.  Fix a colour \(c\).  The coefficient of
\(X_c\) is one, so some perfect-matching monomial uses a nonzero \(cc\)-cell
at every site.  The unique cell incident to each \((u,c)\) must therefore
be such a \(cc\)-cell.  These cells form a perfect matching \(P_c\), and
their product is one.  Doing this for all three colours exhausts the scalar
support as three occurrence-disjoint monochromatic perfect matchings
\(P_0,P_1,P_2\); their underlying physical pairs need not be disjoint.

For even \(N\ge6\), the standard three-one-factors lemma gives a fourth
source perfect matching \(P\) in their occurrence union.  It is not one of
the \(P_c\), hence its induced vertex colouring is mixed.  At every vertex,
the coordinate selected by this colouring has only its \(P\)-edge
available.  Thus \(P\) is the unique monomial in that mixed coefficient.
Its weight is a product of nonzero anchor cells, so the coefficient is
nonzero, contrary to \(\Delta_{B,3}\). \(\square\)

At \(N=4\), put one colour on each of the three one-factors of \(K_4\).
There is no fourth physical perfect matching, and the result is exactly
\(\Delta_{4,3}\) with \(\nu=6\).  At \(N=2\), the single block \(I_3\) is
the analogous saturated source.  Hence neither the strict inequality nor
the recurrent-pivot contradiction can be extended below six.

## 6. The minimum-support ledger and its sharp limit

Let

\[
 \begin{aligned}
 {\cal P}&=\operatorname{supp}p_a,&r&=|{\cal P}|,\\
 {\cal S}&=\operatorname{supp}s_a,&t&=|{\cal S}|,\\
 T&=\alpha^{-1}p_as_a.
 \end{aligned}                                             \tag{24}
\]

Only the two star rows and the internal quadratic change.  Define the
fresh and cancelled internal sets

\[
 \begin{aligned}
 F&=\operatorname{supp}(q+T)\setminus\operatorname{supp}q,\\
 C&=\operatorname{supp}q\setminus\operatorname{supp}(q+T).
 \end{aligned}                                             \tag{25}
\]

The exact scalar-cell ledger is

\[
 |\operatorname{supp}A^\#|-|\operatorname{supp}A|
                         =|F|-|C|-r-t.                    \tag{26}
\]

Every cell of \(T\) comes from a pair consisting of one supported
coordinate of \(p_a\) and one of \(s_a\).  Same-site products vanish and
two ordered products can merge or cancel in one internal cell, so

\[
                              |F|\leq|\operatorname{supp}T|\leq rt.       \tag{27}
\]

If \(A\) has minimum entry support among exact sources, the left side of
(26) is nonnegative.  Thus

\[
                  |F|\geq r+t+|C|,\qquad rt\geq r+t.      \tag{28}
\]

Goodness gives \(r,t>0\); (28) then forces \(r,t\ge2\).

Now maximize \(\nu\) among the minimum-support sources.  Equality in
(26) would leave \(A^\#\) in the same minimum-support stratum while (7)
raises \(\nu\), a contradiction.  Hence

\[
                  |F|\geq r+t+|C|+1,\qquad rt\geq r+t+1, \tag{29}
\]

which is precisely (12).

This is the strongest conclusion available from the two lexicographic
statistics alone.  At the support-transfer level it is sharp.  For example,
at even order \(N\geq8\), take \(r=2,t=3\), put the five supported star
coordinates on disjoint residual sites, and leave all six cross cells absent
from \(q\).  Then \(T\) has a fresh \(2\)-by-\(3\) rectangle,
\(C=\varnothing\), and

\[
                   |\operatorname{supp}A^\#|-|\operatorname{supp}A|
                                =6-2-3=1.                 \tag{30}
\]

Complementary star rows can be placed on independent residual coordinates
to make both deleted star maps injective.  This is a sharp local carrier
model, not an exact ternary source; the top-degree equations may impose
additional restrictions.  It proves that support arithmetic by itself
cannot make the pivot nonincreasing.

## 7. Why many good pairs do not accumulate anchors

The essential-star count and the anchor potential concern different
quantifiers.  Pivots at two different good pairs generally produce two
different exact sources.  Their new anchors do not coexist unless the
second pair remains admissible after the first pivot.  Neither goodness
nor the count of good pairs proves that persistence.

There is a sharp incidence model.  On even \(N\geq4\), choose three
edge-disjoint physical perfect matchings \(P_0,P_1,P_2\), and put a single
\(E_{ii}\)-cell on every edge of \(P_i\).  Then

\[
                         \nu={3N\over2}.                  \tag{31}
\]

Every physical pair outside \(P_0\cup P_1\cup P_2\) is good: deleting its
zero direct block leaves the three coordinate carriers at both endpoints.
Thus the model has

\[
                         \binom N2-{3N\over2}             \tag{32}
\]

good pairs, but every one of them has zero direct block and none is an
intrinsic scalar-unit pivot pair.  The three matching edges at each site
are exactly its essential neighbours, so the dimension-three essential
budget is saturated as well.

For \(N\ge6\) this carrier model is not an exact ternary source: the fourth
matching in Section 5 is its uncancellable mixed coefficient.  That is the
point.  Target flattening, essential-neighbour budgets, and good-pair
abundance see only the local carrier incidence and all hold in this model;
excluding it uses the higher matching equation.  Therefore a recurrence
theorem must use such a global coefficient relation (or a source-faithful
normal/four-cut comparison), not the existing good-pair count alone.

## 8. Exact scope and audit

The pivot identity in Section 2 uses the complete nine rows, including the
exceptional unary row.  The potential theorem uses only the literal
rank-one block update (17), scalar-unit direct block, and goodness.  It is
valid over any field for support purposes; characteristic zero enters the
surrounding divided-power normal-jet setup.

The dependency-free checker
[`verify_scalar_unit_pivot_global_potential_anchor_matching.py`](../computations/verify_scalar_unit_pivot_global_potential_anchor_matching.py)
audits the block pivot, planted-anchor persistence, the exact support ledger
and its \(2\)-by-\(3\) sharp case, the potential bounds, the saturated good
graph, and the order-four/order-at-least-six terminal matching behaviour on
deterministic instances.  The uniform results are the proofs above, not the
finite smoke checks.
