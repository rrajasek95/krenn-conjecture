# A sharp local countermodel to the leave-one-out rank constraints

## Outcome

The new two-vertex witness conditions do not combine with forced rank-one
anchors, cofactor activity, or entry-minimal star irredundancy to give a
finite graph/rank contradiction.  There is an exact zero-one array on six
vertices with all of the following properties.

1. Its underlying support graph is `K_6`.
2. A perfect matching of its edge blocks is invertible; every other block
   is a nonzero singleton rank-one matrix.
3. For every invertible block `A_pq`, every outside vertex `u`, and every
   color `r`,
   \[
                    A_{pu}K_rA_{qu}^{T}=0.                \tag{1}
   \]
   Thus all four outside vertices are zero witnesses, stronger than both
   the two-witness and three-vertex-union conclusions.
4. Every ordered vertex/color port has a forced-anchor-form active edge.
5. Every complementary matching tensor is nonzero.
6. The seven nonzero cell contributions at every star are linearly
   independent over the rationals; a `7 by 7` minor has determinant
   `+1` or `-1`.
7. Every rank-one edge also satisfies both factor-witness conclusions of
   the leave-one-out theorem.

This is not a realization of `Delta_(6,3)`.  It is a countermodel to a
specific proposed inference: the currently extracted witness/rank data,
even supplemented by the strongest local conditions available from
entry-minimality, do not force a cubic vertex, a low-rank-free pair, or a
nontrivial support cut.  Further use of the coefficient identities must
retain more than these ranks and activity flags.

## 1. The array

Use vertices `0,...,5` and standard coordinate columns `e_0,e_1,e_2`.
Put the identity matrix on the perfect matching

\[
                              02|14|35.                   \tag{2}
\]

Every remaining upper-oriented block has one unit cell, as follows:

\[
\begin{array}{c|cccccccccccc}
uv&01&03&04&05&12&13&15&23&24&25&34&45\\ \hline
\text{cell}&01&10&02&12&11&02&01&00&12&02&22&21.
\end{array}                                                \tag{3}
\]

Thus, for example, `A_03=e_1e_0^T`; reverse orientation always means
transpose.  All entries are zero or one.

There is a structural way to read (3).  Group the vertices into the three
identity pairs

\[
 X_0=\{0,2\},\qquad X_1=\{1,4\},\qquad X_2=\{3,5\}.       \tag{4}
\]

For `u notin X_a`, assign a coordinate label `ell_(a,u)` by

\[
\begin{array}{c|rrrr}
a&\multicolumn{4}{c}{u:\ell_{a,u}}\\ \hline
0&1:1&3:0&4:2&5:2\\
1&0:0&2:1&3:2&5:1\\
2&0:1&1:0&2:0&4:2.
\end{array}                                                \tag{5}
\]

For `x in X_a`, `y in X_b`, `a != b`, set

\[
                 A_{xy}=e_{\ell_{b,x}}e_{\ell_{a,y}}^T.  \tag{6}
\]

Equations (5)--(6) reproduce (3).

## 2. Every invertible-edge cross matrix vanishes

Fix the identity edge `pq=X_a` and an outside vertex `u`.  Formula (6)
gives

\[
 A_{pu}=e_i e_{\ell_{a,u}}^T,
 \qquad A_{qu}=e_j e_{\ell_{a,u}}^T                       \tag{7}
\]

for coordinates `i,j` which may depend on the endpoints.  The right
factor at `u` is deliberately identical.  Since every `K_r` is skew,

\[
 A_{pu}K_rA_{qu}^T
 =e_i\bigl(e_{\ell_{a,u}}^TK_re_{\ell_{a,u}}\bigr)e_j^T
 =0.                                                       \tag{8}
\]

This proves (1) simultaneously for all three colors and all four outside
vertices.  It also makes the projected-rank consequence transparent: the
two off-`r` column ranks are each zero or one and their sum is at most two.
The same four witnesses show that the union over the three colors is not
confined to two vertices.

Only the blocks in (2) have rank at least two.  Hence (8) audits every
instance of the invertible/rank-at-least-two witness theorem in this array.

## 3. Anchors and active cofactors

For each pair `X_a`, the multiset of labels on its four outside vertices
in (5) contains all three colors.  Therefore, for every `p in X_a` and
every color `r`, some outside `u` has `ell_(a,u)=r`, and (7) has the
forced-anchor form

\[
                           A_{pu}=z e_r^T\ne0.             \tag{9}
\]

The three colors require distinct singleton blocks, so every vertex has at
least three distinct rank-one anchors.

Every underlying pair is present.  After deleting the endpoints of any
edge, choose any perfect matching of the remaining `K_4`.  Every selected
edge block has a nonzero cell, and the matching edges are vertex-disjoint,
so those cells define one nonzero decorated matching monomial.  All entries
are nonnegative integers, hence no cancellation can remove it.  Thus every
complementary matching tensor is genuinely nonzero, including those of all
chosen anchors.

The support graph is `K_6`; in particular it has no cubic vertex.  It also
has no nontrivial tight odd cut: a three-vertex shore has perfect matchings
crossing its boundary in either one or three edges.

## 4. Rank-one factor witnesses and local irredundancy

For completeness, apply the rank-one branch of the leave-one-out theorem
to every ordered singleton block `A_pq=e_i e_j^T`.  Direct exact evaluation
of

\[
                         C_{u,r}=A_{pu}K_rA_{qu}^T        \tag{10}
\]

shows:

* whenever `r != i`, at least two outside vertices have
  `C_(u,r)=e_i d_u^T`; and
* whenever `r != j`, at least two outside vertices have
  `C_(u,r)=c_u e_j^T`.

These are precisely the two factor-allocation conclusions; the exempt
cases `r=i` and `r=j` are supplied by the explicit coordinate factors of
`A_pq`.  The checker evaluates both orientations of all twelve rank-one
edges, rather than inferring one from endpoint symmetry.

There are seven nonzero scalar cells incident with each vertex: three on
its identity-pair block and one on each of its other four blocks.  For a
cell `(pu;i,j)`, form its full contribution atom

\[
 e_i^{(p)}\otimes e_j^{(u)}\otimes
                         H_{B\setminus\{p,u\}}(A).        \tag{11}
\]

Exact row reduction in the standard coloring basis gives rank seven at
all six vertices.  More sharply, the determinants of the selected
`7 by 7` minors, in vertex order, are

\[
                         -1,\ 1,\ 1,\ -1,\ -1,\ -1.       \tag{12}
\]

Thus the array satisfies the local-irredundancy lemma forced by an
entry-minimal exact representative; the conclusion does not fail because
of a hidden same-star linear dependence.

## 5. Exact audit and consequence

Run

```text
python computations/verify_leave_one_out_rank_countermodel.py
```

The checker constructs all fifteen oriented blocks over the integers,
evaluates all cross matrices (10), checks every invertible and rank-one
witness count, enumerates every four-site complementary matching tensor,
finds an active rank-one anchor at each of the eighteen ordered
vertex/color ports, and verifies the six unimodular minors in (12) by exact
rational row reduction.

Therefore a counting proof based on the following compressed data is
blocked: edge ranks, the zero/proportional witness incidences, active versus
inactive cofactors, forced rank-one anchors, the support graph, and
same-star entry-minimality.  A successful continuation of the two-vertex
identities must use their actual contraction polynomials (or compatibility
among cofactor tensors across different deleted pairs), not only the rank
consequences extracted from them.
