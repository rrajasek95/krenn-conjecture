# A K8 countermodel to global witness-incidence counting

## 1. Outcome

The two-hole anchor-rectangle theorem is a genuine new consequence of the
full contraction equations, but its compressed incidence alternative does
not by itself give a global combinatorial contradiction.  There is an exact
zero-one block array on eight vertices satisfying all of the following.

1. Its support graph is `K_8`.
2. Four disjoint blocks are identities; the other twenty-four blocks are
   nonzero singleton rank-one matrices.
3. For every identity block `A_pq`, all six outside vertices are zero-cross
   witnesses for every color.  Thus every high-rank pair lies in the
   `at least three witnesses` branch of the anchor-rectangle theorem, with
   ample slack.
4. Every ordered vertex/color port has two forced-anchor-form edges, and
   every complementary cofactor is nonzero.
5. The nine nonzero scalar-cell contribution tensors at each star are
   linearly independent over `Q`; explicit `9 by 9` minors have nonzero
   integer determinant.
6. Every rank-one edge satisfies both factor-witness alternatives of the
   one-hole theorem.

The array is not a realization of `Delta_(8,3)`.  It proves that the
witness hypergraph, forced anchors, activity, complete support, and
entry-minimal star independence are jointly consistent.  A global proof
must retain the full two-hole polynomial equations or compatibility among
different cofactors, not just count witness incidences.

## 2. Construction by four paired groups

Partition the vertices into

\[
 X_0=01,\qquad X_1=23,\qquad X_2=45,\qquad X_3=67,         \tag{1}
\]

and put `I_3` on each paired block.  For every group `X_a` and every vertex
`u notin X_a`, choose a label `ell_(a,u)` by

\[
\begin{array}{c|rrrrrr}
a&\multicolumn{6}{c}{u:\ell_{a,u}}\\ \hline
0&2:2&3:1&4:0&5:1&6:2&7:0\\
1&0:2&1:0&4:2&5:1&6:0&7:1\\
2&0:1&1:0&2:1&3:2&6:0&7:2\\
3&0:1&1:0&2:2&3:2&4:0&5:1.
\end{array}                                                \tag{2}
\]

If `x in X_a`, `y in X_b`, and `a!=b`, orient the block from `x` to `y`
and set

\[
                 A_{xy}=e_{\ell_{b,x}}e_{\ell_{a,y}}^T.   \tag{3}
\]

Equation (3) is consistent with transposition on reversing the edge.  All
entries are zero or one.

## 3. High-rank witness hypergraphs

Fix an identity pair `pq=X_a` and an outside vertex `u`.  Both blocks from
the two endpoints to `u` have the same right factor at `u`:

\[
 A_{pu}=e_i e_{\ell_{a,u}}^T,qquad
 A_{qu}=e_j e_{\ell_{a,u}}^T.                             \tag{4}
\]

Consequently, for every color `r`,

\[
 A_{pu}K_rA_{qu}^T
 =e_i\bigl(e_{\ell_{a,u}}^TK_re_{\ell_{a,u}}\bigr)e_j^T
 =0.                                                       \tag{5}
\]

Thus the witness set `S_r(p,q)` is the full six-vertex complement for all
twelve identity-pair/color instances.  The minimum two-witness branch of
the anchor-rectangle theorem never arises.

For every row of (2), each color occurs twice.  Hence every vertex in
`X_a` has two incident singleton blocks whose opposite factor is `e_r`, for
each `r`.  These are forced-anchor-form blocks.  Since the underlying graph
is complete and every entry is nonnegative, deletion of any pair leaves a
six-vertex complete support with a positive matching monomial.  Every
complementary matching tensor is therefore nonzero, so all selected anchors
are active.

## 4. Rank-one witnesses and star independence

For an oriented singleton edge `A_pq=e_i e_j^T`, exact evaluation of

\[
 C_{u,r}=A_{pu}K_rA_{qu}^T                                \tag{6}
\]

gives at least two outside matrices with column space in `C e_i` whenever
`r!=i`, and at least two with row space in `C e_j^T` whenever `r!=j`.
These are exactly the two rank-one factor-witness conclusions; colors
`i,j` are supplied by the coordinate factors of the deleted block.

Every star has nine nonzero cells: three diagonal cells on its identity
partner and one singleton cell on each of the other six blocks.  For each
cell form the full contribution tensor

\[
 e_i^{(p)}\otimes e_j^{(u)}\otimes
 H_{B\setminus\{p,u\}}(A).                                \tag{7}
\]

The checker selects nine coloring rows at each star.  The determinants of
the resulting `9 by 9` integer matrices, in vertex order, are

\[
                    4,-4,1,-4,-2,2,-1,1.                 \tag{8}
\]

All are nonzero, so the nine contribution tensors are linearly independent
over `Q`.  The array therefore satisfies the exact local-irredundancy
conclusion required of an entry-minimal realization.

## 5. Consequence and exact audit

This construction generalizes the six-site array in
`notes/leave-one-out-rank-countermodel.md`.  It shows at the first unknown
order `n=8` that no counting argument on the witness-incidence hypergraph
can force a minimum two-witness pair: every high-rank pair can have all
outside vertices as witnesses while all forced anchors and local
independence conditions remain valid.

Run

```text
python computations/verify_witness_incidence_k8_countermodel.py
```

The checker constructs all blocks over the integers, enumerates every
six-site cofactor, checks the `24` forced-anchor ports with multiplicity two,
checks all high-rank and rank-one witness alternatives in both orientations,
and verifies the eight exact minors (8).

The uncompressed audit is continued in
[`full-two-hole-k8-audit.md`](full-two-hole-k8-audit.md).  The same model
passes all `168` one-hole systems and `407/420` full two-hole systems; the
remaining failures isolate a single coefficient-level cofactor obstruction
and an exact eleven-branch boundary alternative.
