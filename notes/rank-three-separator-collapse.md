# All-pair Hessian rigidity forces the rank-three graph to disconnect

## 1. Outcome

Let

\[
                  R=\{uv:\operatorname {rank}A_{uv}=3\}
\]

be the graph of invertible aggregate blocks of an exact ternary source.
Assume that the internal source Hessian is equal to its vertex-expansion
gauge kernel after every deletion of two vertices.  Then \(R\) is not
connected.

For the residual analysis also write

\[
                  S=\{uv:\operatorname {rank}A_{uv}\ge2\}.             \tag{0}
\]

This closes both positive-connectivity separator branches:

* a 2-vertex cut cannot occur, because even 2-connectivity was already
  incompatible with the missing-row propagation;
* a cut vertex cannot occur either.  In fact, the argument below treats
  every connected \(R\), including graphs with rank-three leaves.

The proof retains the actual mixed pair equations.  Choose two leaves of a
spanning tree of \(R\); deleting them leaves \(R\) connected.  The
connected pair obstruction forces a zero row.  A rank-three boundary of
its global zero set must be a leaf of \(R\).  The other deleted endpoint
then supplies two off-color zero rows at that leaf.  Repeating the boundary
equation with every other endpoint makes all remaining incident blocks
literally zero.  The leaf consequently has exactly three neighbors in the
aggregate support graph.  Cubic-vertex rigidity makes all three blocks rank
one, contradicting the rank-three boundary block.

Thus the all-pair gauge-rigid branch has an honest zero-vertex cut:
\(R\) has at least two connected components.  Section 6 gives a further
component-channel restriction.  For one deleted pair, a row-full
rank-three graph with no isolated sites must have at least three connected
components.  With only one or two components, the synchronized star rows
have a common color annihilator, and the diagonal pair equations would
make one internal tensor proportional to two distinct pure colors.

After merging components across rank-two and misaligned rank-one blocks,
at least three channel classes are still necessary.  Globally this gives a
second separator dichotomy: either the rank-at-least-two graph \(S\) is
disconnected, or some two-deletion chart has an isolated vertex in its
internal rank-three graph.  In particular, connected \(S\) is incompatible
with minimum rank-three degree at least three.  At such an isolate, one
invertible deleted star already forces a multiplicity-two cover by the six
missing-row sets; the earlier second-invertibility hypothesis is needed
only to turn a rank-two spoke into six zero rows and two direct holes.
Consequently a 3-connected \(S\) forces a globally isolated vertex of
\(R\).

No entry-minimality is needed for the contradiction.  Section 5 records
the active-cofactor interpretation when an entry-minimal source has been
chosen.

## 2. Oriented pair equations

Let \(B\) have even cardinality at least six and suppose

\[
                         H_B(A)=\Delta_{B,3}.
\]

For deleted vertices \(p,q\), put \(W=B\setminus\{p,q\}\) and orient all
incident matrices with their deleted endpoint first:

\[
 A_{p\mid i}\in V_p\otimes V_i,\qquad
 A_{q\mid i}\in V_q\otimes V_i.
\]

Let \(p_{c,i}\) be row \(c\) of \(A_{p\mid i}\), let \(s_{d,i}\) be
row \(d\) of \(A_{q\mid i}\), and set

\[
 p_c=\sum_{i\in W}p_{c,i},\qquad
 s_d=\sum_{i\in W}s_{d,i}.
\]

Writing \(q_0\) for the internal quadratic, \(|W|=2r\), and

\[
 Q={q_0^r\over r!},\qquad
 \mathcal H_{q_0}(Z)={Zq_0^{r-1}\over(r-1)!},
\]

the exact nine pair equations are

\[
 \boxed{\quad
 \mathcal H_{q_0}(p_cs_d)+a_{cd}Q
       =\delta_{cd}X_c,\qquad
 X_c=\bigotimes_{i\in W}e_c^{(i)}.
 \quad}                                                   \tag{1}
\]

Gauge rigidity and an off-diagonal equation first give, on every internal
block \(xy\), a scalar \(\lambda_{cd,xy}\) such that

\[
 p_{c,x}\otimes s_{d,y}+s_{d,x}\otimes p_{c,y}
                 =\lambda_{cd,xy}A_{xy}\qquad(c\ne d).   \tag{2a}
\]

On every internal rank-three edge, the rank comparison forces
\(\lambda_{cd,xy}=0\), and hence

\[
 p_{c,x}\otimes s_{d,y}+s_{d,x}\otimes p_{c,y}=0
 \qquad(c\ne d).                                         \tag{2}
\]

Indeed, the left side of (2a) is a sum of two simple tensors
and has matrix rank at most two, whereas its gauge expression is a scalar
multiple of the invertible block \(A_{xy}\).  This is the
cancellation-aware local equation from
[zero-row-pair-propagation.md](zero-row-pair-propagation.md).

## 3. Every rank-three zero-set boundary is a leaf

For a globally named endpoint and color define

\[
 Z_c(p)=\{x\in B\setminus\{p\}:p_{c,x}=0\}.               \tag{3}
\]

This set is intrinsic; it does not depend on which second endpoint is
deleted.

**Lemma 3.1 (boundary-leaf lemma).**  Assume every two-deletion internal
Hessian is gauge-rigid.  If

\[
 x\in Z_c(p),\qquad y\notin Z_c(p),\qquad xy\in R,         \tag{4}
\]

then \(x\) is a leaf of \(R\), with unique neighbor \(y\).

**Proof.**  A zero row makes \(A_{px}\) singular, so \(px\notin R\).
If \(x\) had another rank-three neighbor \(q\ne y\), then the four
vertices \(p,q,x,y\) would be distinct.  Delete \(p,q\) and apply (2) on
the internal edge \(xy\).  Since \(p_{c,x}=0\) and \(p_{c,y}\ne0\),
equation (2) gives

\[
                         s_{d,x}=0\qquad(d\ne c).
\]

In endpoint order this is

\[
 A_{q\mid x}=e_c^{(q)}\otimes v,\qquad
 A_{x\mid q}=v\otimes e_c^{(q)},                          \tag{5}
\]

including \(v=0\).  Hence \(\operatorname {rank}A_{qx}\le1\), contrary
to \(qx\in R\).  Thus no second rank-three neighbor exists.
\(\square\)

The same rank comparison has a useful rank-two version.

**Lemma 3.2 (rank-two boundary cap).**  Under the same all-pair rigidity,
if (4) holds with \(xy\in S\), then

\[
                         N_S(x)\subseteq\{p,y\}.           \tag{5a}
\]

**Proof.**  Let \(q\notin\{p,x,y\}\) be any other \(S\)-neighbor of
\(x\), delete \(p,q\), and inspect the \(xy\) block of the gauge
relation.  Because \(p_{c,x}=0\), its star-product side is the single
simple tensor \(s_{d,x}\otimes p_{c,y}\), of rank at most one.  The other
side is a scalar multiple of \(A_{xy}\), of rank at least two.  Therefore
\(\lambda_{cd,xy}=0\), and then the simple tensor itself vanishes.  Thus
\(A_{q\mid x}\) again has the form (5) and rank at most one, contradicting
\(qx\in S\).  Only the named endpoint \(p\) and the boundary neighbor
\(y\) can remain.  \(\square\)

The all-zero alternative in (3) is impossible: the color-\(c\) first
contraction at \(p\) would be zero, whereas its target is
\(e_c^{\otimes(B\setminus\{p\})}\).  Consequently, whenever \(R-p\) is
connected, every nonempty \(Z_c(p)\) has a boundary and hence contains a
rank-three leaf on its boundary.

## 4. A connected rank-three graph collapses at a leaf

We need one elementary graph fact.

**Lemma 4.1 (nonseparating pair).**  Every connected graph on at least
three vertices has distinct non-cut vertices \(p,q\) such that
\(R-\{p,q\}\) is connected.

**Proof.**  Take any spanning tree and choose two of its leaves.  Removing
either leaf, or both leaves, leaves the remaining tree connected.  The
same deletions therefore leave the ambient graph connected.
\(\square\)

**Theorem 4.2 (connected-rank-three obstruction).**  Under the hypotheses
of Section 2 and all-pair gauge rigidity, \(R\) is disconnected.

**Proof.**  Suppose \(R\) is connected.  Choose \(p,q\) by Lemma 4.1 and
put \(W=B\setminus\{p,q\}\).  The internal rank-three graph \(R[W]\) is
connected.  The connected pair obstruction of
[source-hessian-bipartite-rankdrop.md](source-hessian-bipartite-rankdrop.md)
therefore forces a literal zero row on one deleted star.  Interchange
\(p,q\) if necessary and write

\[
                         p_{c,x}=0                        \tag{6}
\]

for some \(x\in W\).

First exclude the relative selector case.  If \(p_{c,i}=0\) for every
\(i\in W\), the diagonal and off-diagonal instances of (1) make the direct
row on \(pq\) consist of one nonzero \((c,c)\) cell: explicitly,
\(a_{cc}Q=X_c\), so \(a_{cc}\ne0\), \(Q\ne0\), and
\(a_{cd}=0\) for \(d\ne c\).  Thus globally \(Z_c(p)=W\).
Since \(R-p\) is connected, some rank-three edge joins
\(q\) to \(W\); write it \(xq\).  Lemma 3.1 makes \(x\) a rank-three
leaf with sole neighbor \(q\).  But deleting \(p,q\) then isolates \(x\),
contrary to the connectedness of \(R[W]\) (and \(|W|\ge4\)).

Hence the zero set inside \(W\) is a nonempty proper subset.
Connectedness of \(R[W]\) supplies a boundary edge

\[
 xy\in R[W],\qquad p_{c,x}=0,\quad p_{c,y}\ne0.            \tag{7}
\]

Lemma 3.1 says that \(x\) is a leaf of \(R\), with sole rank-three
neighbor \(y\).  Applying (2) for the original deleted pair gives, with
endpoints kept in order,

\[
                         A_{q\mid x}=e_c^{(q)}\otimes v.   \tag{8}
\]

Fix one color \(d\ne c\).  Its row at \(x\) in (8) is zero.  We claim
that

\[
                         s_{d,y}\ne0.                     \tag{9}
\]

If it were zero, the global zero set \(Z_d(q)\) would contain both \(x\)
and \(y\).  It is proper by the color-\(d\) first contraction at \(q\).
Because \(q\) is a non-cut vertex, \(R-q\) is connected.  Follow a path
in \(R-q\) from \(x\) to a site outside \(Z_d(q)\).  Since \(x\) is a
global rank-three leaf with sole neighbor \(y\), the path begins with
\(xy\); at the first edge leaving the zero set, its zero-side endpoint
has both a predecessor and a successor on the path and hence rank-three
degree at least two.  Lemma 3.1 says that the same endpoint has degree one,
a contradiction.  This proves (9).

Now take any

\[
                         t\in B\setminus\{p,q,x,y\}.       \tag{10}
\]

Delete \(p,t\) and use (7) in (2); this gives

\[
                         A_{t\mid x}=e_c^{(t)}\otimes v_t.
\]

Delete \(q,t\) and use the color-\(d\) zero at \(x\) together with (9);
this gives

\[
                         A_{t\mid x}=e_d^{(t)}\otimes w_t.
\]

Since \(c\ne d\), the two row-supported subspaces intersect only in zero.
Therefore

\[
                         A_{tx}=0
 \qquad(t\notin\{p,q,x,y\}).                              \tag{11}
\]

Thus the aggregate support degree of \(x\) is at most three, with
possible neighbors only \(p,q,y\).  The exact support graph has minimum
degree at least three, so these are exactly its three neighbors.
Cubic-vertex rigidity for the exact ternary matching tensor now says that
all three incident matrices at \(x\) are rank-one same-color coordinate
tensors.  This contradicts \(xy\in R\), which says
\(\operatorname {rank}A_{xy}=3\).

The assumption that \(R\) was connected is impossible.
\(\square\)

The proof deals uniformly with connectivity two and one.  In the
2-connected branch, Lemma 3.1 already excludes every zero-row boundary.
In the cut-vertex branch, the leaf chase (8)--(11) closes the only new
escape.

## 5. Endpoint activity and literal holes

Equation (8) is oriented with \(q\) first.  Reversing the stored endpoint
order gives

\[
                         A_{x\mid q}=v\otimes e_c^{(q)}.
\]

If \(v=0\), this is a literal zero block.  If \(v\ne0\) and the exact
source is entry-minimal, every nonzero scalar cell of the block has a
nonzero complementary matching tensor; it is an active directed
color-\(c\) anchor into \(q\).  The second propagation does not merely
produce another anchor: two different endpoint-coordinate row lines
intersect in zero, giving the literal holes (11).  The final cubic-support
argument then makes all three surviving blocks active and rank one, which
is incompatible with the invertible block \(xy\).

## 6. The surviving zero-cut branch

Disconnectedness is not just a failure of the connected proof.  The pair
equations give an exact lower bound on the number of component channels
needed in a row-full chart.

**Lemma 6.1 (row annihilator).**  For any fixed deleted pair satisfying
(1), suppose

\[
                         \sum_{c=0}^2\ell_cp_c=0.          \tag{12}
\]

If at least two coordinates of \(\ell\) are nonzero, the pair equations
are inconsistent.

**Proof.**  Multiply the equation in row \(c\), column \(d\) of (1) by
\(\ell_c\) and sum over \(c\).  The Hessian product term vanishes by
(12), so

\[
       \left(\sum_c\ell_ca_{cd}\right)Q=\ell_dX_d
       \qquad(d=0,1,2).                                  \tag{13}
\]

For every \(d\) in the support of \(\ell\), equation (13) makes the same
tensor \(Q\) proportional to the nonzero pure tensor \(X_d\).  Two such
pure tensors are linearly independent, a contradiction.  The case
\(Q=0\) is already contradictory in any supported coordinate.
\(\square\)

**Theorem 6.2 (at least three component channels).**  Fix a deleted pair
whose internal Hessian is gauge-rigid.  Suppose every color row of both
deleted stars is nonzero at every internal site, and suppose the internal
rank-three graph has no isolated vertices.  Then it has at least three
connected components.

**Proof.**  On each connected component, equation (2) and the six-row
antipodal synchronization lemma give nonzero local vectors \(z_i\) and
nonzero scalars \(t_c^{(h)},u_d^{(h)}\) such that

\[
 p_{c,i}=t_c^{(h)}z_i
 \quad\hbox{and}\quad
 s_{d,i}=u_d^{(h)}\sigma_i z_i
 \qquad(i\in C_h).                                       \tag{14}
\]

Every component must be bipartite; a nonbipartite component is already
inconsistent with all rows nonzero.  Put

 \[
                         z_h=\sum_{i\in C_h}z_i.
 \]

Each \(z_h\) is nonzero, and the \(z_h\)'s are linearly independent:
they occupy disjoint direct sums of the site spaces \(V_i\).

If there are \(k\) components, (14) puts all three linear elements \(p_c\)
in \(\operatorname {span}\{z_1,\ldots,z_k\}\).  For \(k\le2\) they have
a nontrivial relation (12).  Because every \(t_c^{(h)}\) is nonzero, no
one-coordinate vector can be a relation; its coefficient vector \(\ell\)
has support at least two.  Lemma 6.1 gives a contradiction.  Hence
\(k\ge3\).
\(\square\)

Singleton rank-three components are excluded from Theorem 6.2 for a real
reason: with no rank-three edge, the three local rows at that site need
not be collinear and can supply up to three color channels by themselves.

Rank-two blocks between rank-three components reduce the channel count
further.  They are the exact low-rank analogue of a Schur bridge.

**Theorem 6.3 (rank-two component merger).**  Retain the hypotheses of
Theorem 6.2.  Contract every connected component of the internal
rank-three graph to a node, and join two nodes when some block between
them has rank two.  The resulting quotient graph has at least three
connected components.

More precisely, if \(C_h,C_k\) are joined by a rank-two block
\(A_{ij}\), \(i\in C_h,j\in C_k\), then the two synchronization columns

\[
 t^{(h)}=(t_0^{(h)},t_1^{(h)},t_2^{(h)})^T,\qquad
 t^{(k)}=(t_0^{(k)},t_1^{(k)},t_2^{(k)})^T                \tag{15}
\]

are proportional; the same holds for the two \(u\)-columns.

**Proof.**  Use (14), and write \(\sigma_i,\sigma_j\in\{1,-1\}\) for the
two local bipartition signs.  On the \(ij\) block, the off-diagonal gauge
relation has the form

\[
 \bigl(t_c^{(h)}u_d^{(k)}\sigma_j+
       u_d^{(h)}\sigma_i t_c^{(k)}\bigr)
                         z_i\otimes z_j
             =\lambda_{cd}A_{ij}.                         \tag{16}
\]

The left side has rank at most one and \(A_{ij}\) has rank two.  Hence
both sides vanish.  For two colors \(c,c'\), choose the third color
\(d\ne c,c'\).  All displayed scalars are nonzero, and the two resulting
instances of (16) give

\[
 {t_c^{(h)}\over t_c^{(k)}}
       ={t_{c'}^{(h)}\over t_{c'}^{(k)}}.                 \tag{17}
\]

Thus the columns in (15) are proportional.  Interchanging the roles of
the \(p\)- and \(q\)-stars proves the assertion for \(u\).

On each connected component of the quotient graph, combine the
corresponding \(z_h\)'s using these proportionality scalars.  The three
global rows \(p_c\) then lie in the span of one combined linear element
per quotient component.  If there were at most two quotient components,
the three \(p_c\)'s would have an annihilator.  Row-fullness makes every
coefficient of every synchronized column nonzero, so a one-coordinate
annihilator would say that a nonzero \(p_c\) is zero.  The annihilator
therefore has support at least two, and Lemma 6.1 rules it out.  There
must be at least three quotient components.  \(\square\)

There is a sharp rank-one continuation.  If \(A_{ij}\) has rank one and
is not proportional, in endpoint order, to \(z_i\otimes z_j\), then the
two rank-one tensors in (16) are linearly independent.  Their coefficients
must both vanish for every \(c\ne d\), and the same calculation (17)
again makes the two component columns proportional.  Therefore:

**Corollary 6.4 (aligned rank-one survivor).**  In a row-full pair chart
with no rank-three isolates, form channel classes by merging rank-three
components across every rank-two block and every rank-one block not
aligned with the synchronized local lines.  At least three channel classes
remain.  Every nonzero block between distinct surviving classes is
necessarily of the endpoint-oriented form

\[
                         A_{ij}=\lambda_{ij}z_i\otimes z_j.             \tag{18}
\]

These aligned rank-one blocks are the exact residual Schur/complement
channels.  They cannot be discarded as support zeros: matchings may cross
between classes through them, but every such crossing uses one fixed local
line at each endpoint.

The rank-two merger also globalizes, provided no rank-three isolate is
created by the chosen deletion.

**Theorem 6.5 (connected-\(S\) collapse outside the isolate branch).**
Suppose all two-deletion Hessians are gauge-rigid.  If there are distinct
vertices \(p,q\) such that

\[
 S-p,\quad S-q,\quad S-\{p,q\}\quad\hbox{are connected}       \tag{18a}
\]

and \(R-\{p,q\}\) has no isolated vertex, then a contradiction follows.
Consequently, if \(S\) is connected, then \(R\) has a vertex of degree at
most two.  Equivalently, some two-deletion chart has an internal
rank-three isolate.  Thus every all-pair gauge-rigid source satisfies the
global alternative

\[
 \boxed{\quad S\text{ is disconnected, or some pair deletion isolates a
 vertex of }R.\quad}                                      \tag{18b}
\]

**Proof.**  Put \(W=B\setminus\{p,q\}\).  If all six deleted-star color
rows were nonzero at every site of \(W\), Theorem 6.3 would apply.  But
connectedness of \(S[W]\) says that rank-three components become connected
after adjoining their rank-two links, so its quotient would have one
component, contrary to Theorem 6.3.  After interchanging \(p,q\) if needed,
there are therefore a color \(c\) and a site \(x\in W\) with

\[
                         p_{c,x}=0.                         \tag{18c}
\]

First suppose \(p_{c,i}=0\) for all \(i\in W\).  The pair equations give
the clean selector \(a_{cc}Q=X_c\), \(a_{cd}=0\) for \(d\ne c\); in
particular \(p_{c,q}\ne0\).  Since \(S-p\) is connected, \(q\) has an
\(S\)-neighbor \(x\in W\).  Lemma 3.2 gives
\(N_S(x)\subseteq\{p,q\}\), whereas connectedness of \(S[W]\) gives \(x\)
an internal \(S\)-neighbor.  This is impossible.

The zero set in \(W\) is therefore proper.  Connectedness of \(S[W]\)
supplies a boundary

\[
 xy\in S[W],\qquad p_{c,x}=0,\quad p_{c,y}\ne0.            \tag{18d}
\]

Lemma 3.2 gives \(N_S(x)\subseteq\{p,y\}\).  Applying (2a) to (18d) for
the original deleted pair shows, for every \(d\ne c\), that
\(s_{d,x}=0\), and hence \(A_{q\mid x}\) has only its color-\(c\) row.
Fix one such \(d\).  We claim \(s_{d,y}\ne0\).  Otherwise the global zero
set \(Z_d(q)\) contains both \(x\) and \(y\), but it is proper by the
color-\(d\) first contraction at \(q\).  Follow a path in the connected
graph \(S-q\) from \(x\) to its complement.  At the first boundary, the
zero-side endpoint has a predecessor different from \(q\) and the boundary
neighbor; if the boundary is the first edge, use the other neighbor \(y\)
of \(x\).  Either case contradicts Lemma 3.2.  This proves the claim.

For any \(t\notin\{p,q,x,y\}\), delete \(p,t\) and use the boundary
(18d) in (2a).  Rank at least two versus rank at most one gives

\[
                         A_{t\mid x}=e_c^{(t)}\otimes v_t.
\]

Deleting \(q,t\) and using \(s_{d,x}=0\), \(s_{d,y}\ne0\) gives instead

\[
                         A_{t\mid x}=e_d^{(t)}\otimes w_t.
\]

The two distinct endpoint-row subspaces meet only in zero, so \(A_{tx}=0\).
Thus \(x\) has at most the three support neighbors \(p,q,y\).  Exactness
gives support degree at least three, and cubic-vertex rigidity then makes
all three incident matrices rank one, contradicting \(xy\in S\).

Finally, if \(S\) is connected, choose two leaves \(p,q\) of a spanning
tree.  They satisfy (18a).  If every vertex had \(R\)-degree at least three,
deleting two vertices could not isolate a remaining vertex of \(R\), so the
first part would give a contradiction.  Hence some vertex has
\(R\)-degree at most two.  Deleting all of its rank-three neighbors (and
an arbitrary additional vertex when fewer than two are present) produces
an internal rank-three isolate.  This proves (18b).  \(\square\)

The isolate alternative has its own rigid local normal form as soon as one
deleted endpoint is a global rank-three neighbor.

**Lemma 6.6 (one-invertible isolate zero cover).**  Fix a gauge-rigid
deleted pair \(p,q\), and let \(x,y\in W\) be distinct.  If \(A_{px}\) is
invertible while \(\operatorname {rank}A_{xy}\le2\), then at least two of
the six rows

\[
             p_{0,y},p_{1,y},p_{2,y},s_{0,y},s_{1,y},s_{2,y}             \tag{18e}
\]

are zero.  In particular, if \(x\) is isolated in the internal graph
\(R[W]\) and \(A_{px}\) is invertible, the six global zero sets based at
\(p,q\) cover \(W\setminus\{x\}\) with multiplicity at least two.

If, in addition, \(A_{qx}\) is invertible and \(A_{xy}\) has rank two,
all six rows vanish and

\[
                 A_{py}=A_{qy}=0,qquad N_S(y)=\{x\}.       \tag{18f}
\]

**Proof.**  Orient the \(xy\) block with \(x\) first and abbreviate

\[
 a_c=p_{c,x},\quad b_d=s_{d,x},\quad
 P_c=p_{c,y},\quad S_d=s_{d,y},\quad A=A_{x\mid y}.
\]

The triple \((a_c)\) is a basis of \(V_x\); no independence or
nonvanishing is assumed for the \(b_d\)'s.  For every \(c\ne d\), the
arbitrary-block gauge identity (2a) says

\[
                 a_c\otimes S_d+b_d\otimes P_c=\lambda_{cd}A.           \tag{18g}
\]

We first prove the two-zero assertion.  Suppose, to the contrary, that at
least five of the six rows \(P_c,S_d\) are nonzero.

Assume initially that all six are nonzero and \(\operatorname {rank}A=2\).
Let \(\alpha\ne0\) be the relation among the three rows of \(A\), and put
\(\beta_d=\alpha(b_d)\).  Contracting (18g) by \(\alpha\) gives

\[
                   \alpha_cS_d+\beta_dP_c=0
                              \qquad(c\ne d).               \tag{18h}
\]

Every \(\alpha_c\) is nonzero.  Indeed, if \(\alpha_k=0\), then
\(\beta_d=0\) for both \(d\ne k\); using those two columns in (18h) kills
the other two coordinates of \(\alpha\).  Equation (18h) then also makes
every \(\beta_d\) nonzero and makes all six rows \(P_c,S_d\) proportional,
because the off-diagonal incidence graph on the two color triples is
connected.  The left side of (18g) consequently has rank at most one.
Rank two of \(A\) forces every \(\lambda_{cd}=0\).  For a fixed \(d\), the
two resulting equations make \(b_d\) proportional to each of the two
distinct basis vectors \(a_c\), \(c\ne d\), a contradiction.

If all six rows are nonzero and \(\operatorname {rank}A\le1\), quotient
\(V_x\) by \(L=\operatorname {im}A\).  Writing bars for quotient vectors,
(18g) becomes

\[
                 \bar a_c\otimes S_d+\bar b_d\otimes P_c=0.             \tag{18i}
\]

The images of the basis vectors \(a_c\) span the quotient, whose dimension
is at least two.  If one \(\bar a_c\) vanished, (18i) would first kill the
two \(\bar b_d\)'s with \(d\ne c\), and then the remaining equations would
kill the other two \(\bar a\)'s.  Otherwise simple-tensor uniqueness in
(18i) makes all three \(\bar a_c\)'s proportional.  Either conclusion
contradicts their spanning a quotient of dimension at least two.  Thus all
six rows cannot be nonzero.

Suppose next that the unique zero row is \(P_k\).  For \(d\ne k\), (18g)
reads \(a_k\otimes S_d=\lambda_{kd}A\).  Its left side is nonzero and rank
one, so \(A\) has rank one with image \(\mathbb Ca_k\).  Quotienting by
that line and using the two equations with \(d=k\) makes \(\bar b_k\)
proportional to each of the two independent images
\(\bar a_c\), \(c\ne k\), a contradiction.

Finally suppose the unique zero row is \(S_k\).  If
\(\operatorname {rank}A=2\), use \(\alpha,\beta\) as in (18h).  The
equations with \(d=k\) give \(\beta_k=0\).  If \(\alpha_k=0\), the other
four equations force \(\beta_i=\beta_j=\alpha_i=\alpha_j=0\), impossible.
Thus \(\alpha_k\ne0\); those same equations make the five nonzero rows
\(P_0,P_1,P_2,S_i,S_j\) proportional.  Rank comparison in (18g), first
with \((c,d)=(k,i)\) and then \((j,i)\), makes \(b_i\) proportional to
both distinct basis vectors \(a_k,a_j\), again impossible.  If
\(\operatorname {rank}A\le1\), quotient by its image.  The two equations
with \(d=i\) make \(\bar a_k,\bar a_j\) proportional (or both zero), and
those with \(d=j\) make \(\bar a_k,\bar a_i\) proportional (or both zero).
The three images cannot then span the at-least two-dimensional quotient.
This excludes the last one-zero case and proves the first assertion.

For the rank-two sharpening assume now that \((b_d)\) is also a basis.
Use the basis \((a_c)\), write \(b_d=\sum_e C_{ed}a_e\) with \(C\)
invertible, and let \(A_e\) be row \(e\) of \(A\).  For \(e\ne c\), row
\(e\) of (18g) is

\[
                         C_{ed}P_c=\lambda_{cd}A_e.          \tag{18j}
\]

Let \(\alpha\) span the relation among the rows \(A_e\).  Whenever
\(\alpha_c\ne0\), the two complementary rows are independent.  Equation
(18j) then rules out \(\lambda_{cd}\ne0\).  If \(P_c\ne0\), it makes both
columns \(d\ne c\) of \(C\) supported only in row \(c\), contradicting
invertibility.  Hence \(\alpha_c\ne0\) implies \(P_c=0\).

If \(\alpha\) has support three, this kills every \(P_c\), and (18g),
rank one versus rank two, kills every \(S_d\).  If its support is two, say
\(\{0,1\}\), then \(P_0=P_1=0\); the pairs
\((0,1),(0,2),(1,0)\) kill \(S_1,S_2,S_0\), and the remaining equations
kill \(P_2\).  If its support is one, say \(\{2\}\), then
\(A_2=0\), \(A_0,A_1\) are independent, and \(P_2=0\).  The pairs
\((2,0),(2,1)\) kill \(S_0,S_1\), the pairs \((0,1),(1,0)\) kill
\(P_0,P_1\), and \((0,2)\) kills \(S_2\).  Thus all six rows vanish.

Under the additional hypotheses of the sharpening, we proved
\(A_{py}=A_{qy}=0\), while invertibility gives
\(p_{c,x}\ne0\) and \(s_{d,x}\ne0\) for every color.
Lemma 3.2 applied from \(p\) gives \(N_S(y)\subseteq\{p,x\}\), and its
application from \(q\) gives \(N_S(y)\subseteq\{q,x\}\).  Their
intersection is \(\{x\}\), and \(xy\in S\), proving (18f).  \(\square\)

**Corollary 6.7 (global residual trichotomy).**  Combining Theorem 6.5 and
Lemma 6.6 gives a concise global classification.
Every all-pair gauge-rigid exact source at order at least six lies in at
least one of these three branches:

1. \(S\) is disconnected, so every cross-component aggregate block has
   rank at most one;
2. \(S\) is connected and \(R\) has a globally isolated vertex; or
3. \(S\) is connected and some vertex \(x\) has one or two global
   rank-three neighbors.  Choose an invertible neighbor \(p\), and choose
   \(q\) to be the other one when it exists (arbitrary otherwise).  After
   deleting \(p,q\), the six zero sets based at them cover every other
   internal site at least twice.  In the two-neighbor case, every rank-two
   edge incident with \(x\) ends at an \(S\)-leaf as in (18f).

This classification is exact but not yet a contradiction: branch 1 still
permits rank-one matching channels across the \(S\)-cut, while branches 2
and 3 retain the unsynchronized local three-dimensional channel carried by
an isolated rank-three site.

There is a useful robust-\(S\) consequence.  If \(S\) is
2-vertex-connected and has minimum degree at least three, then no endpoint
row can vanish.  Indeed, for a zero row based at \(p\), its global zero set
is nonempty and proper; connectedness of \(S-p\) supplies a boundary edge,
and Lemma 3.2 makes the boundary site have \(S\)-degree at most two.  The
zero cover in branch 3 is therefore impossible.  Hence in this regime
\(R\) must have a globally isolated vertex.  In particular:

\[
 \boxed{\quad S\text{ 3-vertex-connected }
          \Longrightarrow R\text{ has an isolated vertex}.\quad}       \tag{18k}
\]

At order six, the two-neighbor part of branch 3 is even narrower.  A
rank-two neighbor \(y\) of \(x\) would have \(A_{py}=A_{qy}=0\), leaving
only \(x\) and the other two internal sites as possible support neighbors
of \(y\).  Minimum support degree three would make \(y\) cubic, and
cubic-vertex rigidity would contradict
\(\operatorname {rank}A_{xy}=2\).  Hence all three remaining blocks at
\(x\) have rank at most one.  The three-color slice-cover theorem forces
three distinct nonzero rank-one neighbors, so these are exactly the other
three internal sites; each carries at least two of the six missing rows in
(18e).  In the one-neighbor part, the multiplicity-two cover still holds,
but the rank-two-spoke all-six-zero conclusion need not.

There is also a useful all-or-nothing consequence of Lemma 3.2.  Let
\(C\) be a connected component of \(S\) having minimum internal
\(S\)-degree at least two, and let \(p\notin C\).  For fixed \(p,c\),
either every row \(p_{c,x}\), \(x\in C\), is zero or none is zero.
Otherwise a boundary edge inside \(C\) would have a zero-side endpoint
with a second \(S\)-neighbor different from \(p\), contradicting
Lemma 3.2.  The same statement holds for \(C-p\) when it is connected and
every one of its vertices has two global \(S\)-neighbors other than the
possible deleted endpoint.

At the rank-three level, Lemma 3.1 gives the analogous statement without
the possible neighbor \(p\): on a connected component of \(R\) of minimum
rank-three degree at least two, a deleted-star row is either zero
everywhere or nowhere.  It also applies to a connected vertex-deleted
component when all its vertices retain global rank-three degree at least
two.

**Lemma 6.8 (complete rank-one joins between thick \(S\)-components).**
Let \(C,D\) be distinct connected components of \(S\), each of minimum
internal \(S\)-degree at least two.  Then the aggregate support between
\(C\) and \(D\) is either empty or the complete bipartite graph
\(K_{C,D}\).  Every block in a nonempty join has rank one.

More precisely, for each \(p\in C\) there is a fixed set of endpoint colors
\(U_p^D\subseteq\{0,1,2\}\) such that, for every \(q\in D\), row \(c\) of
the endpoint-oriented block \(A_{p\mid q}\) is nonzero exactly when
\(c\in U_p^D\).  There is an analogous fixed mask \(U_q^C\) at the other
endpoint.  If one cross block is nonzero, all these masks are nonempty.

**Proof.**  Fix \(p\in C\) and a color \(c\).  The all-or-nothing
consequence of Lemma 3.2 says that the row \(p_{c,q}\) is zero for every
\(q\in D\), or nonzero for every \(q\in D\).  This defines \(U_p^D\).
Suppose \(A_{pq}\ne0\) for one \(p\in C,q\in D\).  Some row at \(p\) is
nonzero, so the same row is nonzero toward every \(q'\in D\); hence every
\(A_{pq'}\) is nonzero.  For each such \(q'\), some row at \(q'\) is
nonzero toward \(p\).  Applying the same argument to the component \(C\)
makes \(A_{p'q'}\ne0\) for every \(p'\in C\).  Thus the join is complete.
It lies outside \(S\), so every one of its nonzero blocks has rank one.
The same argument gives the masks at \(D\).  \(\square\)

Since the exact aggregate support is connected, if every \(S\)-component
has minimum internal degree two, contracting the \(S\)-components gives a
connected skeleton, and every skeleton edge expands to one of the complete
rank-one joins in Lemma 6.8.  Thus the disconnected-\(S\) residual is a
rank-one blow-up system, not an arbitrary sparse collection of cross edges.

The target-specific continuation is
[complete-rank-one-join-triple-degeneracy.md](complete-rank-one-join-triple-degeneracy.md).
It no longer requires an invertible internal edge: in every nondegenerate
triple-shore normal-form branch, two nonzero rank-one sides meeting at one
vertex have different endpoint coordinate masks.  Lemma 6.8 gives equal
masks across a thick complete join.  Consequently every triple with two
vertices in one thick component and one in an adjacent thick component has
a named constant-row degeneracy and an exact pure three-cross selector,
regardless of the rank (or vanishing) of its third block.

**Corollary 6.9 (six-site disconnected-\(S\) reduction).**  At order six,
an exact all-pair gauge-rigid source with disconnected \(S\) has a vertex
of internal \(S\)-degree at most one.

**Proof.**  Otherwise every \(S\)-component has at least three vertices.
There are exactly two components of size three, and minimum internal degree
two makes both of them triangles.  Exact support is connected, so Lemma 6.8
makes all nine cross blocks nonzero rank-one matrices.  The six internal
triangle blocks have rank at least two.  This is precisely the saturated
\(C_3\sqcup C_3\) rank pattern excluded, with arbitrary endpoint colors and
complex cancellation retained, by
[saturated-rank-graph-obstruction.md](../proofs/saturated-rank-graph-obstruction.md).
\(\square\)

Combining this with Theorem 6.5 and the order-six conclusion after
Corollary 6.7 leaves only three six-site shapes: a low-degree vertex of
\(S\) in the disconnected branch; a vertex of global \(R\)-degree at most
one in the connected branch; or the double-invertible rank-one fan of
Corollary 6.7.

Consequently, if the residual graph \(R\) has exactly two 2-connected
components, choose one non-cut deleted endpoint in each component.  The
internal graph has two nontrivial components, so Theorem 6.2 forces a zero
row.  That row vanishes on an entire component channel, not at an isolated
collection of sites.  For this fixed deleted-pair chart, any surviving
all-pair gauge-rigid source must therefore lie in one of the following
explicit zero-cut subbranches:

1. at least three nontrivial component channels survive even after the
   rank-two and misaligned-rank-one mergers of Theorem 6.3 and
   Corollary 6.4;
2. the internal rank-three graph has isolated sites;
3. a deleted-star color row vanishes identically on a whole rank-three
   component; if it vanishes on all of \(W\), this is the clean-selector
   subcase \(a_{cc}Q=X_c\), \(a_{cd}=0\) for \(d\ne c\), while otherwise
   its zero set is a proper union of component channels; or
4. some global rank-three component has a global \(R\)-leaf, allowing the
   boundary-leaf pattern before the global cubic collapse is available.

This is the sharp structural reduction obtained here.  Removing these
disconnected component-routing branches requires identities coupling the
rank-at-most-two matrices between different components; ordinary support
separator factorization is unavailable because those cross blocks need
not vanish.

### 6.10. Sharp order-four boundary: an exact empty-\(R\) source

The residual empty-\(R\) branch is not a formal artefact of the Hessian
method.  At order four there is an exact source satisfying every
two-deletion gauge-rigidity hypothesis.  On vertices \(0,1,2,3\), put

\[
\begin{array}{c|c}
 \{01,23\}&A_{ij}=e_0\otimes e_0\\
 \{02,13\}&A_{ij}=e_1\otimes e_1\\
 \{03,12\}&A_{ij}=e_2\otimes e_2 .
\end{array}                                                \tag{19}
\]

The three perfect matchings of \(K_4\) are exactly the three displayed
one-factor classes.  Hence their matching tensors are respectively
\(e_0^{\otimes4},e_1^{\otimes4},e_2^{\otimes4}\), and

\[
                         H_{{0,1,2,3}}(A)=\Delta_{4,3}.
\]

Every aggregate block in (19) has rank one, so both \(R\) and \(S\) are
empty, while the aggregate support graph is the 3-connected cubic graph
\(K_4\).  After deleting any pair, the internal set \(W=\{i,j\}\) has
size two, so \(r=1\) and

\[
                         \mathcal H_{q_0}(Z)=Z.
\]

Its kernel is zero.  The vertex-gauge expression is
\((\alpha_i+\alpha_j)A_{ij}\) with \(\alpha_i+\alpha_j=0\), so the gauge
space is also zero.  Thus all six pair Hessians are gauge-rigid.

This example is below the standing order \(|B|\ge6\), and therefore is
not a counterexample to the desired conjecture.  It is a sharp warning
about the remaining proof obligation: all-pair Hessian rigidity, full
support 3-connectivity, minimum support degree three, and even exactness
do not by themselves create a rank-three or rank-two edge.  Any closure
of the empty-\(R\) branch at order at least six must use the extra global
matching identities available at larger order, rather than only the
local gauge-kernel axioms used above.

### 6.11. Six-site empty-\(S\) anchor permutations

At six sites, the empty-\(S\) branch has one further exact local normal
form.

**Lemma 6.11 (endpoint-line injectivity).**  Suppose \(|B|=6\), every
two-deletion Hessian is gauge-rigid, and every aggregate block has rank at
most one.  At any vertex \(v\), the endpoint factors at \(v\) of two
distinct nonzero incident blocks lie on distinct projective lines.

**Proof.**  Suppose the nonzero blocks \(va,vb\) have proportional factors
at \(v\).  Choose a fourth vertex \(w\), and delete the other two vertices,
leaving \(W=\{v,a,b,w\}\).  After absorbing the proportionality scalar,
write

\[
 A_{v\mid a}=x\otimes u,qquad A_{v\mid b}=x\otimes z.
\]

For a nonzero \(t\in V_w\), define a quadratic variation supported on the
two complementary edges by

\[
                         Z_{bw}=z\otimes t,qquad
                         Z_{aw}=-u\otimes t.               \tag{19a}
\]

On four sites \(\mathcal H_{q_0}(Z)=Zq_0\).  The first variation in (19a)
pairs only with \(A_{va}\), the second only with \(A_{vb}\), and their
four-site tensors cancel exactly.  Hence \(Z\) is in the Hessian kernel.
Choose \(t\) outside the at most two endpoint lines at \(w\) belonging to
\(A_{aw},A_{bw}\) (a zero block imposes no line).  Then a nonzero block of
\(Z\) is not proportional to the corresponding aggregate block, so \(Z\)
is not a vertex-gauge variation.  This contradicts gauge rigidity.
\(\square\)

Now add exactness, hence the active coordinate anchors from the slice-cover
theorem.  For each tail \(v\) and color \(c\), let \(\pi_c(v)\) be a
chosen distinct neighbor whose endpoint factor is \(e_c\).  There are
eighteen directed anchor incidences.  Lemma 6.11 permits at most one
incoming incidence of color \(c\) at any fixed head, hence at most three
incoming anchors per vertex.  The total capacity is exactly eighteen, so
every capacity is filled.  Consequently each \(\pi_c\) is a derangement of
the six vertices, and

\[
 \pi_0(v),\pi_1(v),\pi_2(v)\quad\hbox{are distinct for every }v.         \tag{19b}
\]

Thus the empty-\(S\) branch is not combinatorially arbitrary: its forced
anchors form three directed permutation systems, and every vertex receives
the three coordinate lines exactly once.

**Lemma 6.12 (the endpoint factors form a projective arc).**  Under the
hypotheses of Lemma 6.11, any three nonzero rank-one endpoint factors at a
fixed vertex are linearly independent.

**Proof.**  In a four-site chart \(W=\{v,a,b,w\}\), write the three star
blocks as

\[
 A_{v\mid a}=x_a\otimes u_a,quad
 A_{v\mid b}=x_b\otimes u_b,quad
 A_{v\mid w}=x_w\otimes u_w.
\]

If \(\lambda_ax_a+\lambda_bx_b+\lambda_wx_w=0\), define a variation on
the complementary triangle by

\[
 Z_{bw}=\lambda_a u_b\otimes u_w,qquad
 Z_{aw}=\lambda_b u_a\otimes u_w,qquad
 Z_{ab}=\lambda_w u_a\otimes u_b.                         \tag{19c}
\]

Multiplication by the complementary star edge gives the same tensor
\(u_a\otimes u_b\otimes u_w\) at the other three sites, tensored with the
displayed linear relation at \(v\).  Hence
\(\mathcal H_{q_0}(Z)=0\).  Lemma 6.11 lets us assume the three star lines
are distinct, so every coefficient in a dependence is nonzero.  If (19c)
were a gauge variation, each of its three blocks would be proportional to
the corresponding aggregate block.  At vertex \(a\), for example, both
complementary blocks \(ab,aw\) would then have endpoint line \(\mathbb C
u_a\), the same as \(av\), contradicting Lemma 6.11.  Thus (19c) is an
extra Hessian-kernel vector.  Gauge rigidity forbids the dependence.
\(\square\)

With exactness, the incident endpoint lines at every vertex therefore form
a projective arc containing the three coordinate points.  Every additional
line has all three coordinates nonzero, and any two additional lines have
distinct projections away from each coordinate point.

### 6.13. Sharp order-six Hessian/anchor countermodel

Even at the target order, the local Hessian and support axioms alone do not
eliminate the empty-\(S\) branch, even after adding all coordinate anchors
forced by one-slice covering.  On \(K_6\), put
\(A_{uv}=l_{uv}\otimes r_{uv}\), with the following nonnegative integer
factors, oriented with the smaller endpoint first:

\[
\begin{array}{c|cc@{\quad}c|cc@{\quad}c|cc}
01&(0,0,1)&(23,33,85)&02&(1,0,0)&(0,1,0)&03&(28,35,30)&(0,0,1)\\
04&(0,1,0)&(87,16,73)&05&(31,34,11)&(1,0,0)&12&(0,1,0)&(81,27,71)\\
13&(1,0,0)&(68,61,48)&14&(55,94,67)&(1,0,0)&15&(0,0,1)&(0,1,0)\\
23&(30,94,92)&(40,65,13)&24&(0,0,1)&(0,0,1)&25&(1,0,0)&(23,88,40)\\
34&(1,0,0)&(0,1,0)&35&(0,1,0)&(0,0,1)&45&(76,95,65)&(40,98,40)
\end{array}                                                \tag{20}
\]

Every block has rank one and every pair is supported, so \(R=S=\varnothing\)
and the aggregate support is the 5-connected graph \(K_6\).  Nevertheless,
after each of the fifteen pair deletions, the four-site Hessian has rank
\(51\) in its \(54\)-dimensional quadratic domain, and its kernel is exactly
the three-dimensional vertex-gauge space.

The certificate is exact.  The verifier below exhibits rank \(51\) modulo
the prime \(1{,}000{,}003\), which is a characteristic-zero lower bound;
the three universal gauge directions give the matching upper bound and are
checked independently.  Thus all fifteen Hessians are simultaneously
gauge-rigid over \(\mathbb Q\).

It also satisfies the full incidence conclusion of the slice-cover
theorem.  For tail \(v\), the factor at the opposite endpoint
\(\pi_c(v)\) is \(e_c\), where

\[
 \begin{aligned}
 (\pi_0(0),\ldots,\pi_0(5))&=(5,4,0,1,3,2),\\
 (\pi_1(0),\ldots,\pi_1(5))&=(2,5,1,4,0,3),\\
 (\pi_2(0),\ldots,\pi_2(5))&=(3,0,4,5,2).
 \end{aligned}                                             \tag{21}
\]

The three neighbors are distinct at every tail.  Every anchor is active:
all blocks are nonzero, the support is complete, and nonnegativity prevents
cancellation of every complementary matching tensor.

This is still not an exact matching source.  For example, its coefficient
at the mixed word \(200000\) is the positive integer \(84{,}630{,}000\),
whereas the target coefficient is zero.  The model therefore pinpoints the
remaining input: an empty-\(S\) contradiction at order six or above must
use more of the target star or full coefficient identities than the
coordinate-anchor conclusion alone.

### 6.14. The full coefficients close the empty-\(S\) branch

The missing input isolated above is now supplied by
`rank-one-complete-six-chart-obstruction.md`.  Lemmas 6.11--6.12 and the
eighteen exact anchors force three mutual same-colour coordinate perfect
matchings.  Their union is one of the two cubic graphs on six vertices;
every other supported edge has full support at both endpoints.  An exact
orbit table over all subsets of the six complementary edges gives a mixed
singleton in every case except the complete triangular prism.  Four mixed
fibres exclude that last case by a vertexwise multiplicative rectangle.

Consequently there is no exact six-site empty-\(S\) chart for which every
pair-deleted Hessian is gauge-rigid.  The numerical model (20) is therefore
sharp only for the Hessian-and-anchor relaxation: its positive mixed
coefficient is exactly the obstruction detected by the new argument.

## 7. Exact audit

[verify_rank_three_separator_collapse.py](../computations/verify_rank_three_separator_collapse.py)
is a dependency-free audit.  It exhausts all labeled connected graphs
through six vertices, constructs two spanning-tree leaves, and verifies
that deleting either or both leaves preserves connectivity.  It separately
exhausts the minimum-degree-three graphs and verifies that no deletion pair
can isolate a remaining vertex, the graph core of Theorem 6.5.  It verifies
that the only disconnected six-vertex graphs of minimum degree two are the
ten labeled copies of \(C_3\sqcup C_3\), the graph core of Corollary 6.9.
It also checks all endpoint-color intersections used in (11), and exhausts the
nonzero small-integer one- and two-component synchronization matrices,
verifying that every color annihilator has support at least two.  It also
checks the rank-two merger scalar equations, exhausts the finite
projective geometry behind Lemma 6.6 over \(\mathbb F_2\), including all
\(7{,}680\) canonical one-invertible cases with an arbitrary second star,
and verifies the exact order-four empty-\(R\) source (19), including all of
its two-site Hessians.  These finite checks supplement, but do not replace,
the uniform proofs above.

[verify_rank_one_all_pair_hessian_model.py](../computations/verify_rank_one_all_pair_hessian_model.py)
checks (20).  It constructs every pair-deleted Hessian, certifies rank
\(51/54\) and three independent killed gauge vectors in all fifteen charts,
checks all eighteen active anchor incidences (21) and all sixty local
three-line determinants from Lemma 6.12, and evaluates the stated mixed
coefficient exactly.
