# All deleted pairs can lie coherently in the missing-row branch

## 1. Outcome

The pair trichotomy in
[`source-hessian-bipartite-rankdrop.md`](source-hessian-bipartite-rankdrop.md)
does not globalize to a graph-theoretic contradiction using forced anchors,
matching-coveredness, pair overlaps, and the known local consequence of
entry minimality.  There is an exact rational eight-site source with all of
the following properties.

1. Its underlying support is 5-regular, 3-vertex-connected, and
   matching-covered.
2. Every vertex has a same-color coordinate anchor for each of the three
   colors.
3. Every coloring fiber contains two distinct nonzero matching monomials;
   in particular no mixed fiber is a singleton.
4. All three constant coefficients are exactly one.
5. Every supported scalar cell has a nonzero full cofactor, and at every
   vertex its 21 supported derivative atoms are linearly independent.  The
   latter is exactly the star-irredundancy conclusion forced by entry
   minimality.
6. For every one of the 28 deleted pairs, the missing-row alternative holds
   at **both** deleted endpoints, with at least two different internal
   anchor witnesses at each endpoint.

The source is not a GHZ realization: all entries are positive rational and
every mixed fiber has a nonzero term, so every mixed coefficient is
positive.  It is an exact countermodel to the proposed *structural
globalization*, not to Krenn's conjecture.  It shows that a continuation
must use actual mixed-coefficient cancellation identities beyond the
trichotomy and the currently available entry-minimal support data.

## 2. Five one-factors on eight vertices

Let

\[
                         B=\mathbb Z/7\mathbb Z\cup\{\infty\}.
\]

For `r in Z/7Z`, define the standard round

\[
 F_r=\{\{\infty,r\}\}\cup
     \{\{r+k,r-k\}:1\le k\le3\}.                         \tag{1}
\]

The seven rounds form a one-factorization of `K_8`.  Use

\[
             P_0=F_0,\qquad P_1=F_1,
 \qquad      Q_c=F_{c+2}\quad(c=0,1,2).                  \tag{2}
\]

They are pairwise edge-disjoint.  Put

\[
 D=I_3+J_3=
 \begin{pmatrix}2&1&1\\1&2&1\\1&1&2\end{pmatrix}       \tag{3}
\]

on every edge of `P_0 union P_1`, put `E_cc` on every edge of `Q_c`, and
put zero on all other pairs.  Before normalization, direct exact enumeration
of the 105 perfect matchings gives the three constant coefficients

\[
                            (49,53,41).                   \tag{4}
\]

Apply at vertex `0` the invertible diagonal map

\[
                    \operatorname{diag}(1/49,1/53,1/41). \tag{5}
\]

Equivalently, multiply the corresponding endpoint row or column of every
incident block, according to its orientation.  Every perfect matching uses
one cell at vertex `0`, so (5) changes (4) to

\[
                              (1,1,1).                    \tag{6}
\]

All source entries remain nonnegative rational, and every previously
nonzero entry remains nonzero.

## 3. Exact structural properties

Let `G` be the union of the five factors in (2).  Since the omitted two
rounds are also disjoint one-factors, `G` is `K_8` minus a 2-regular graph
and hence is 5-regular.  Every edge of `G` belongs to one of the five
displayed perfect matchings, so `G` is matching-covered.

It is also 3-vertex-connected.  After deleting at most two vertices, an
induced remaining vertex is nonadjacent to at most two other remaining
vertices.  On six remaining vertices the minimum degree is therefore at
least three; on seven or eight it is still larger.  A disconnected graph
with minimum degree at least three has two components of at least four
vertices, which is impossible on six or seven vertices, and the analogous
degree bound excludes it on eight.  Thus deletion of fewer than three
vertices never disconnects `G`.

For every coloring `z:B -> {0,1,2}`, all cells chosen by `P_0` and `P_1`
are nonzero because `D` has full support and (5) is invertible.  Hence the
`z`-fiber contains at least the two distinct matching monomials

\[
                             m_{P_0}(z),\quad m_{P_1}(z). \tag{7}
\]

For each color `c`, every vertex is incident with one `Q_c` edge carrying
`E_cc`.  These are same-color coordinate anchors in both endpoint
orientations.

Every supported scalar cell is active.  A cell on a `P_k` edge has a
nonzero complementary monomial using the other three edges of `P_k`; the
unique cell on a `Q_c` edge has the complementary pure-`c` monomial using
the other three edges of `Q_c`.  Thus no activity inference relies on
positivity or cancellation.

## 4. Coherent missing rows for all 28 pairs

Fix any deleted pair `{p,q}`.  At `p`, the three anchor edges belonging to
`Q_0,Q_1,Q_2` have three different neighbors.  At most one of those
neighbors is `q`, so at least two anchor edges `pi` lead to internal sites

\[
                         i\in B\setminus\{p,q\}.          \tag{8}
\]

An `E_cc` block has two literal zero rows when oriented with endpoint `p`
first.  Hence each edge in (8) witnesses alternative 3 of the pair
trichotomy.  The same argument at `q` gives at least two witnesses there as
well.  This proves the all-pair statement, including every overlap among
the 28 pairs, without choosing witnesses independently.

Notice that this is stronger than merely arranging one exceptional edge
per pair: the witness system is the fixed union `Q_0 union Q_1 union Q_2`
and is globally consistent.

## 5. The entry-minimality shadow also holds

For a vertex `p` and a supported scalar cell on `pi`, let its unweighted
derivative atom be

\[
 e_a^{(p)}\otimes e_b^{(i)}\otimes
                  H_{B\setminus\{p,i\}}(A).              \tag{9}
\]

There are 21 such atoms at every vertex: nine cells on each of its two
full edges and one cell on each of its three anchor edges.  Exact rational
row reduction gives

\[
 \operatorname{rank}\{\text{atoms at }p\}=21
 \qquad\text{for every }p\in B.                           \tag{10}
\]

More finely, the seven atoms in each fixed endpoint-color row have rank
seven.  Thus no nontrivial simultaneous variation supported on the
currently nonzero cells of one star can preserve the output.  Equation
(10) is precisely the local star-irredundancy lemma used at an
entry-minimal exact point.

The calculation in (10) is finite but exact: the matrices have rational
entries, the cofactors are enumerated from the fifteen matchings on each
six-site complement, and Gaussian elimination is performed over
`Fraction`, not floating point.

## 6. Consequence for the global cap route

The model satisfies every currently proposed graph/rank input for combining
the pair trichotomies:

* matching-coveredness and 3-connectivity;
* three forced anchors at every vertex;
* nonzero cofactors for all supported cells;
* absence of singleton coefficient fibers;
* exact normalization of the three constant fibers;
* star irredundancy; and
* a globally coherent missing-row witness system for all deleted pairs.

Therefore those inputs cannot force a pair into the gauge-rigid,
connected, row-full contradiction.  Nor can pair-overlap counting alone
make the missing-row witnesses inconsistent.  A valid globalization must
use the *values* of mixed coefficient equations or cofactor tensors.  In
this model those are exactly what fail: positivity makes every mixed
coefficient nonzero.

The dependency-free verifier
[`verify_all_pair_missing_row_countermodel.py`](../computations/verify_all_pair_missing_row_countermodel.py)
checks (1)--(10) over the rationals, audits all `3^8` coloring fibers, all
28 deleted pairs, all active cofactors, and all eight star derivative
ranks.
