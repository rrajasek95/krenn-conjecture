# Independent audit: cubic-packet six-type boundary core

## Verdict

**PASS.**  The six-type propagation theorem in
[the primary note](cubic-packet-six-type-boundary-core.md) is correct over
the intended field \(\mathbb C\), conditional on the three results it cites:

1. the
   [cubic leave-one-anchor nullity web](cubic-vertex-leave-one-anchor-nullity-web.md);
2. the
   [two-nonneighbour faithful-surplus dichotomy](cubic-two-nonneighbour-faithful-surplus-dichotomy.md);
3. for the optional order-minimal refinement only, the
   [cubic-selector theorem](cubic-selector-reduction.md).

The remaining use of entry-minimality is exactly the local star
irredundancy lemma.  No canonical-transition flatness, genericity,
supportwise noncancellation, or order-minimality is hidden in the main
six-type and \(N\leq18\) conclusions.  Order-minimality first enters in the
selector refinement.

During the audit, the primary note received only definite local
clarifications: the definition of \(E_q\) was made explicitly independent
of \(q'\), residual pairs were declared distinct, the selector extraction
was stated in cancellation-safe form, and the scope phrase "all residual
activity" was narrowed to activity internal to \(R\).  None changes the
proof.

## 1. Site ledger and the one-vertex exceptional set

Let \(B\) have even size \(N\geq8\), and let the cubic centre \(p\) have
the three distinct anchors \(a_0,a_1,a_2\).  Then

\[
 R=B\setminus\{p,a_0,a_1,a_2\},\qquad |R|=N-4\geq4,
\]

so \(R\) is even and contains distinct pairs.

For fixed \(q\in R\) and colour \(c\), the map \(\Phi_{q,c}\) in the
nullity-web theorem is defined on the site set

\[
 K_{q,c}=B\setminus\{p,q,a_c\}.
\]

It is determined before any second residual vertex is chosen.  Hence

\[
 E_q=\{c:\dim\ker\Phi_{q,c}=1\}
\]

is genuinely attached to \(q\), independently of \(q'\).  The nullity-web
theorem gives \(|E_q|\leq1\).

For distinct \(q,q'\in R\), the common cofactor in the two-site theorem is

\[
 P_c(q,q')=H_{L_c}(A),\qquad
 L_c=B\setminus\{p,a_c,q,q'\}.
\]

Here \(|L_c|=N-4\) is even.  Also
\(K_{q,c}=L_c\mathbin{\dot\cup}\{q'\}\) and
\(K_{q',c}=L_c\mathbin{\dot\cup}\{q\}\), so the two maps used by the
dichotomy have exactly the advertised common exterior port.  There is no
site-set or parity mismatch.

## 2. Nullity one gives a literal pure port

Assume no residual pair is in the faithful-surplus alternative, and put

\[
 X=\{q\in R:E_q\ne\varnothing\}.
\]

For \(q\in X\), write \(E_q=\{c\}\).  The exact nullity-one
classification supplies one unique wrong colour \(\rho\ne c\) whose
endpoint-\(q\) star row, after deleting \(p\), is supported only at
\(a_c\).  Since \(q\) is a nonneighbour of the cubic centre,
\(A_{qp}=0\); thus the same support statement holds on the full physical
star.

Contracting the exact target row at \(q\) by \(e_\rho^*\) leaves the
single star term

\[
 \bigl((e_\rho^*\otimes\operatorname{id})A_{q\mid a_c}\bigr)
 \otimes H_{B\setminus\{q,a_c\}}(A)
 =e_\rho^{\otimes(B\setminus\{q\})}.
\]

The right side is nonzero and decomposable.  Uniqueness of factors in a
nonzero two-factor pure tensor therefore gives a scalar \(\mu_q\ne0\)
with

\[
 (e_\rho^*\otimes\operatorname{id})A_{q\mid a_c}
   =\mu_qe_\rho^{(a_c)},\qquad
 H_{B\setminus\{q,a_c\}}(A)
   =\mu_q^{-1}e_\rho^{\otimes(B\setminus\{q,a_c\})}.
\]

This deduction uses the complete target row, not a selected matching and
not merely the residual zero-row statement.

The type \(\tau(q)=(c,\rho)\) is injective.  If two distinct residual
vertices \(q,q'\) had the same type, the nonzero \((\rho,\rho)\) cells on
the two edges incident with the common anchor \(a_c\) would have
unweighted global derivatives

\[
 \mu_q^{-1}e_\rho^{\otimes B},\qquad
 \mu_{q'}^{-1}e_\rho^{\otimes B}.
\]

They are proportional derivative tensors belonging to two nonzero scalar
entries on the same physical star.  This contradicts star irredundancy at
\(a_c\).  Since there are exactly six ordered pairs
\((c,\rho)\) with \(c\ne\rho\), one obtains

\[
 |X|\leq6.
\]

No order-minimality or flatness hypothesis is used here; entry-minimality
enters only through star irredundancy.

## 3. The exceptional vertices form a common residual cover

Let \(I=R\setminus X\), and take distinct \(q,q'\in I\).  Then
\(E_q=E_{q'}=\varnothing\).  On the nonfaithful branch, the concentrated
alternative of the two-nonneighbour theorem says

\[
 \{c:P_c(q,q')\ne0\}\subseteq E_q\cup E_{q'}=\varnothing.
\]

Thus every \(P_c(q,q')\) vanishes.  Expanding the full complementary
cofactor of the block \(qq'\) at the cubic centre gives

\[
 H_{B\setminus\{q,q'\}}(A)
 =\sum_{c=0}^2\lambda_c e_c^{(p)}\otimes e_c^{(a_c)}
       \otimes P_c(q,q')=0.
\]

If \(A_{qq'}\) had a nonzero scalar entry, that entry would consequently
have zero global derivative tensor, contradicting star irredundancy.
Therefore \(A_{qq'}=0\).  This holds for every pair in \(I\), so \(X\)
is one common vertex cover of the support induced on \(R\); it is not a
pair-dependent collection of exceptional vertices.

For \(q\in I\), its possible nonzero neighbours are the three anchors and
the vertices in \(X\).  It is not adjacent to \(p\), and it has no
neighbour in \(I\).  Hence

\[
 d_A(q)\leq |X|+3\leq9.
\]

This degree statement does not assert that anchor-to-\(I\) blocks vanish.
Accordingly, the primary note now states only that activity *internal to*
\(R\) is incident with \(X\).

## 4. Pure anchor cofactors give the order-eighteen bound

For each colour \(c\), cubic rigidity supplies the exact pure cofactor

\[
 H_{B\setminus\{p,a_c\}}(A)
 =\lambda_c^{-1}e_c^{\otimes(B\setminus\{p,a_c\})}.
\]

The constant-\(c\) coefficient is nonzero.  It is a finite sum of scalar
cell products over physical perfect matchings, so at least one contributing
matching has nonzero product.  This is the only matching selected in this
step; the proof makes no claim that other products do not cancel.

The matched site set is

\[
 B\setminus\{p,a_c\}
 =R\mathbin{\dot\cup}\{a_s,a_t\},
 \qquad\{c,s,t\}=\{0,1,2\}.
\]

Because \(I\) is independent, each \(I\)-vertex in that matching is paired
with a distinct vertex of \(X\) or with one of the two surviving anchors.
Therefore

\[
 |I|\leq |X|+2.
\]

Together with \(N=4+|X|+|I|\) and \(|X|\leq6\), this yields

\[
 N\leq4+|X|+(|X|+2)\leq18.
\]

Equivalently, avoidance of the faithful chart gives

\[
 |X|\geq\frac{N-6}{2}.
\]

At the even orders \(8,10,12,14,16,18\), this is respectively
\(1,2,3,4,5,6\).  In particular, the \(N=8\) statement is exactly that
there is at least one typed pure port and a covered four-site residual
core.  It is not a contradiction, and the primary note does not claim one.

## 5. Selector refinement and the extremal order

This section alone assumes that the source is order-minimal above four.
For fixed \(r\), with \(\{r,s,t\}=\{0,1,2\}\), the selector theorem works
on

\[
 U=B\setminus\{p,a_r\}.
\]

The family \(R_s\) is supported on a star centred at \(a_s\), and
\(R_t\) on a star centred at \(a_t\).  Order-minimality gives
\(Q_r=D^2H_U(A)[R_s,R_t]\ne0\).  Expanding this finite sum over pairs of
disjoint selector edges, a nonzero \(Q_r\) implies that at least one raw
summand is a nonzero tensor.  No termwise noncancellation hypothesis is
needed for that implication.

Such a raw summand uses an \(R_s\)-edge \(a_su_{r,s}\) and an
\(R_t\)-edge \(a_tu_{r,t}\).  Disjointness forces the free endpoints to
be distinct, and the deleted sites \(p,a_r\) together with the two selector
centres force

\[
 u_{r,s},u_{r,t}\in R.
\]

The remaining physical matching tensor is therefore exactly

\[
 H_{U\setminus\{a_s,u_{r,s},a_t,u_{r,t}\}}(A)
 =H_{R\setminus\{u_{r,s},u_{r,t}\}}(A)\ne0.
\]

Its site set has even size \(N-6\), including size two when \(N=8\).
Choose a nonzero coefficient of this complete tensor and one nonzero
cell-product matching contributing to it.  If \(d_r\in\{0,1,2\}\) of the
deleted endpoints lie in \(I\), then the matching sees

\[
 |I|-d_r\quad\hbox{remaining \(I\)-vertices},\qquad
 |X|-(2-d_r)\quad\hbox{remaining \(X\)-vertices}.
\]

There are no \(I\)-to-\(I\) edges, so the first set injects into the
second:

\[
 |I|-d_r\leq |X|-(2-d_r).
\]

At \(N=18\), the earlier inequalities force
\(|X|=6\) and \(|I|=8\).  Substitution gives

\[
 8-d_r\leq4+d_r.
\]

Since \(d_r\leq2\), equality forces \(d_r=2\).  Thus for every \(r\),
both selected endpoints lie in \(I\).  The remaining sets have six
vertices each, and every witnessing matching pairs the remaining \(I\)
bijectively with \(X\).  Six vertices with an injective six-valued type
map also mean that all six ordered types occur.  No enumeration of their
incidences is required.

## 6. Scope

The audited theorem proves the following exact fork for an entry-minimal
source with a cubic centre:

1. some residual pair carries the faithful-surplus Hessian packet; or
2. the nonfaithful branch has a six-vertex typed cover of its internal
   residual support and can occur only at even orders at most eighteen.

It does not close the faithful packet, eliminate the bounded cores at
orders \(8\) through \(18\), or control anchor-to-\(I\) activity beyond
the degree bound.  These limitations are stated in the primary note.

The repository route-integrity checker passed after the local repairs.
