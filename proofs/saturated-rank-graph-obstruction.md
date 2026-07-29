# Exact obstruction for both saturated six-vertex rank graphs

This note closes the `|F|=6` branch left in
`notes/six-vertex-rank-graph.md`.  The argument retains arbitrary complex
weights, arbitrary endpoint-color asymmetry, and arbitrary zero patterns in
the matrices not known to have rank one.

Assume throughout that

\[
 H_6(A)=\Delta_{6,3}.
\]

Let `R` be the graph of nonzero rank-one aggregate matrices, let `H` be the
graph of matrices of rank at least two, let `Z` be the graph of zero
matrices, and put

\[
                         F=H\mathbin\cup Z.
\]

The directed slice-cover theorem gives `d_R(v)>=3`, hence `d_F(v)<=2`.
If `|F|=6`, every vertex has `F`-degree two and `R`-degree three.  The defect
budget in `notes/six-vertex-rank-graph.md` then says that every matrix on
`R` is a nonzero coordinate-coordinate basis tensor.  Its two endpoint
colors may differ.  Moreover, for every vertex `u`, the colors at the
opposite endpoints of its three `R`-edges are `0,1,2` in some order.

A two-regular simple graph on six vertices is either `C_6` or
`C_3 disjoint-union C_3`.  We rule out both.

## 1. Exact coefficient-support rules

For a coloring `c in {0,1,2}^6`, call a perfect matching *supported* if
every matrix entry selected by `c` on its three edges is nonzero.  Two
elementary rules hold in every exact realization:

1. if `c` is constant, at least one perfect matching is supported, since
   its target coefficient is one;
2. if `c` is mixed, its number of supported perfect matchings is not one,
   since a unique supported monomial is a product of nonzero complex
   numbers and cannot have target coefficient zero.

The second rule deliberately permits zero supported matchings and every
possible cancellation among two or more supported matchings.  It uses no
positivity, sign, or termwise-vanishing assumption.

A matrix of rank at least two has two nonzero entries in distinct rows and
distinct columns.  Indeed, otherwise its bipartite support has matching
number at most one and is contained in one row or one column.  This gives a
finite Boolean relaxation of matrix rank.

The exact checker
`computations/verify_saturated_rank_graph_obstruction.py` encodes only these
necessary facts.  For completeness, its variables and clauses are as
follows.

* `x_(e,i,j)` says that the `(i,j)` entry on an `F`-edge is nonzero.
* A rank-witness variable selects two true `x` variables in distinct rows
  and columns.  Their disjunction is required on every edge known to have
  rank at least two.
* In the `C_6` branch, an additional variable `t_e` permits the whole matrix
  to be zero; `not t_e` forces all nine entries false, while `t_e` requires
  a rank witness.
* For every coloring and every matching compatible with the fixed basis
  edges, a monomial variable is equivalent, by clauses in both directions,
  to the conjunction of its selected `F`-entry variables.
* A constant coloring gets a disjunction requiring a supported matching.
  For a mixed coloring, every supported matching implies the disjunction of
  all the other supported matchings.  Pure basis matchings are accounted for
  as identically true monomials.

Every putative complex realization therefore gives a satisfying assignment:
set `x` according to its actual nonzero entries, choose a rank witness in
each rank-at-least-two support, and set each monomial variable to its actual
support status.  Consequently an UNSAT result, or an entry forced true in
all satisfying assignments, is an exact implication for the original
matrices.

## 2. Exhaustive anchor-color reduction

Write the color at the head of a directed rank-one edge `u -> v` for the
coordinate factor at `v`.  For each fixed tail `u`, its three head colors
form a permutation of `0,1,2`.  The six choices are independent, so there
are exactly

\[
                         (3!)^6=46656                       \tag{1}
\]

raw asymmetric endpoint-color patterns.

For `F=C_6`, the dihedral group of the cycle and the simultaneous global
color permutations preserve the target and the coefficient-support rules.
Their action partitions (1) into exactly `718` orbits.  For
`F=C_3 disjoint-union C_3`, the graph automorphism group is
`S_3 wreath C_2`, and including global color permutations gives exactly
`134` orbits.

The checker constructs all 46656 patterns as a set, constructs each full
group orbit, removes it, and asserts that exactly 46656 patterns were
removed.  Thus the orbit reduction is not a heuristic canonicalizer and
cannot omit a pattern.

## 3. The six-cycle branch

Relabel so that

\[
 F=\{01,12,23,34,45,05\}.
\]

The Boolean support audit proves the following.

**Lemma 3.1 (full-support propagation).**  For every one of the 718
asymmetric basis-color orbits, the coefficient-support rules and the
alternative "zero matrix or rank at least two" on every edge of `F` force
all six matrices to be nonzero and force all 54 of their entries to be
nonzero.

**Exact audit.**  For each orbit representative, the checker first verifies
that the relaxed formula is satisfiable.  It then assumes `not t_e`, one
cycle edge at a time, and obtains UNSAT in all six cases.  Finally it assumes
`not x_(e,i,j)`, one of the 54 entries at a time, and obtains UNSAT in every
case.  These are incremental exact SAT calls, not optimization or random
search. `QED`

There are exactly two perfect matchings using only cycle edges:

\[
 M_0=\{01,23,45\},\qquad M_1=\{05,12,34\}.                 \tag{2}
\]

Call a mixed coloring *free* if no matching containing a basis edge is
compatible with its endpoint colors.  On such a coloring, only (2) can
contribute, and its coefficient equation is

\[
\begin{split}
 &A_{01}(c_0,c_1)A_{23}(c_2,c_3)A_{45}(c_4,c_5)\\
 &\qquad{}+A_{05}(c_0,c_5)A_{12}(c_1,c_2)A_{34}(c_3,c_4)=0.
                                                               \tag{3}
\end{split}

The second finite lemma supplies enough free colorings to read every minor.

**Lemma 3.2 (free rectangles).**  Fix any of the 718 anchor-color orbits,
any cycle edge `uv`, any two colors `i,k` at `u`, and any two colors `j,l`
at `v`.  There is an assignment of colors to the other four vertices for
which all four colorings obtained from

\[
 (c_u,c_v)\in\{(i,j),(i,l),(k,j),(k,l)\}                   \tag{4}
\]

are mixed and free.  In fact the exhaustive audit finds at least twelve
such assignments in every case.

**Exact audit.**  For each orbit, edge, and pair of two-element color sets,
the checker enumerates the `3^4=81` assignments on the other vertices.  It
tests all fifteen perfect matchings directly against the basis endpoint
labels, and asserts that the witness count is positive.  The minimum over
all cases is twelve. `QED`

We can now finish without computation.  Consider first `uv=01`, fix a free
rectangle supplied by Lemma 3.2, and abbreviate the product on the other two
edges of `M_0` by the nonzero number

\[
 K=A_{23}(c_2,c_3)A_{45}(c_4,c_5).
\]

Lemma 3.1 makes `K` and every other factor below nonzero.  Equation (3) on
the four corners reads

\[
 A_{01}(a,b)K
 =-A_{05}(a,c_5)A_{12}(b,c_2)A_{34}(c_3,c_4),             \tag{5}

for `a in {i,k}` and `b in {j,l}`.  Multiply (5) at the corners
`(i,j),(k,l)` and compare with the product at `(i,l),(k,j)`.  Every factor
other than the displayed `A_01` entries occurs with the same multiplicity
on the two sides.  Since `K` is nonzero, cancellation gives

\[
 A_{01}(i,j)A_{01}(k,l)
 =A_{01}(i,l)A_{01}(k,j).                                  \tag{6}

The same argument works for an edge of `M_1`, with the roles of the two
matchings exchanged.  Lemma 3.2 supplies (6) for every `2 by 2` minor of
every cycle matrix.  All six matrices therefore have rank at most one,
contradicting Lemma 3.1 and their membership in `H`.

Notice why no hidden vanishing invalidates this binomial cancellation:
Lemma 3.1 was proved first and says that every one of the 54 possible cycle
entries is nonzero.  Basis-edge terms do not vanish accidentally in (3);
they are absent because their endpoint colors are incompatible by the
definition of a free coloring.

## 4. The two-triangle branch

Now suppose

\[
 F=K_{\{0,1,2\}}\mathbin\sqcup K_{\{3,4,5\}},
 \qquad R=K_{3,3}.                                        \tag{7}

First, no edge of `F` can be zero.  Within either triangle, a zero edge and
two rank-at-least-two edges would be a higher-rank two-path with a zero
chord, contrary to Lemma 3.1 of `notes/six-vertex-rank-graph.md`.  If at
most one of the other edges has rank at least two, the one remaining
bilinear equation plainly has a coordinate-torus zero.  That also
contradicts the universal torus-zero condition.  Hence all six edges of
`F` lie in `H`.

**Lemma 4.1 (two-triangle support obstruction).**  For every asymmetric
anchor-color pattern on the basis `K_(3,3)`, the coefficient-support rules
are inconsistent with rank at least two on all six internal edges.

**Exact audit.**  Reduce the 46656 raw patterns to the 134 exact orbits from
Section 2.  For each representative, require a distinct-row/distinct-column
support witness on every internal matrix and add all constant/mixed
coefficient-support clauses from Section 1.  The resulting formula is UNSAT
for every representative. `QED`

As stressed in Section 1, the formula permits every possible cancellation
whenever two or more matching monomials are supported.  Its contradiction
comes only from unavoidable zero or singleton coefficients, so Lemma 4.1
applies to arbitrary complex entries and weights.

## 5. Conclusion and reproducibility

Sections 3 and 4 prove:

**Theorem.**  In a putative six-vertex three-color realization, the graph
formed by the zero and rank-at-least-two aggregate matrices cannot have six
edges.  Equivalently, the saturated `F=C_6` and
`F=C_3 disjoint-union C_3` rank patterns are both impossible.

Run the complete exact audit from the project root with

```sh
uv run python computations/verify_saturated_rank_graph_obstruction.py
```

On the reference run it reports

```text
C6: 46656 raw patterns, 718 orbits; all 54 entries forced; minimum free-rectangle witness count = 12
C3+C3: 46656 raw patterns, 134 orbits; every rank>=2 support formula is UNSAT
exact saturated-chart audit passed in 27.55s
```

The only external engine is a deterministic exact SAT solver.  Orbit
coverage, the 81-assignment rectangle searches, and all matching
compatibility tests are independently asserted by ordinary integer/Boolean
code in the same checker.
