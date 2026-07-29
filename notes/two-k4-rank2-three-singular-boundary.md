# A rank-two cross block forces at least three singular blocks

## 1. Result

Consider the full two-`K_4` chart with arbitrary complex cross blocks

\[
                         B_{ij}\in\operatorname {Mat}_3(\mathbb C),
                         \qquad 0\leq i,j<4.              \tag{1}
\]

The dead-slab equations say that the four-cross permanent coefficient
`P(a,b)` vanishes whenever either shore word is dead.  The previous boundary
theorem in
[`two-k4-two-singular-boundary.md`](two-k4-two-singular-boundary.md)
shows that these equations require at least two singular blocks.

**Theorem 1.1.**  If one cross block has rank two, then at least three of the
sixteen cross blocks are singular.

Equivalently, an array with exactly two singular cross blocks cannot have a
rank-two member.  If the full chart has exactly two singular blocks, both
must have rank at most one.

Only the left and right dead-slab permanent equations are used.  The
two-cross sector, the six Hamilton dead words, and the nonzero target
coefficients are not needed.  The exact finite audit is
[`verify_two_k4_rank2_three_singular_boundary.py`](../computations/verify_two_k4_rank2_three_singular_boundary.py).

## 2. Put the two exceptional blocks in distinct block rows

Suppose exactly two blocks are singular and one has rank two.  If their
positions have distinct left indices, retain the left dead-slab equations.
If they share a left index, their right indices are distinct; transpose the
array and use the right dead-slab equations.  Thus in either case the
relevant orientation has at most one singular block in each block row.

After relabelling positions, write the exceptional blocks as

\[
                         B_{00},\qquad B_{1\epsilon},
                         \qquad \epsilon\in\{0,1\},       \tag{2}
\]

where `epsilon=0` is the same-column case and `epsilon=1` is the
different-column case.  The first block has rank two; let the second rank be
`d in {0,1,2}`.

For each of the eight oriented-triangle dead coordinate lines, with free
left site `i`, contraction of the right factors gives

\[
                         \sum_{j=0}^3B_{ij}y_jC_j=0.      \tag{3}
\]

The restricted square-free syzygy theorem from the preceding note applies
because row `i` contains at most one singular block.

* If the exceptional reference block has rank one or two, all four
  complementary `Per_3` tensors `C_j` vanish.
* If it is the zero block in column `k`, the three `C_j` with `j != k`
  vanish.  This is the only missing-cofactor case.

Rows without an exceptional block use the ordinary four-vector cofactor
collapse.  Hence every triangle comes with three or four certified zero
`Per_3` restrictions.

## 3. The finite row-matroid types

At a fixed right block column, an incidence means that the three selected
nonzero row vectors in an oriented triangle are proportional.  It is
equivalent to the corresponding local `Per_3` map having rank one.

Only the projective row matroid of an exceptional block matters for the
incidence count.  The possibilities are finite.

* A rank-two block has one of seven relaxed types: three distinct nonzero
  row points; one of the three possible proportional pairs plus a distinct
  third point; or one of the three possible zero rows plus two distinct
  points.
* A rank-one block has one nonempty subset of nonzero rows, all proportional.
  There are seven such supports.
* A rank-zero block has no active row point.

For the first rank-two type, the audit forgets the linear dependence among
the three distinct row points.  This enlarges the admissible incidence set,
so an upper bound proved in this relaxed model is valid for an actual
rank-two matrix.

## 4. Incidence demand from the zero cofactors

Fix one oriented triangle.  Call a right column **good** if all three of its
selected row vectors are nonzero.  A singular block can make its column bad
only when the triangle selects one of that block's zero rows.

For every known zero cofactor `C_j` whose three constituent columns are
good, the strengthened zero-`Per_3` lemma says that at least two of those
three column maps have rank one.  In incidence bits `r_0,...,r_3`, this is

\[
                   \sum_{k\ne j}r_k\geq2.               \tag{4}
\]

The audit installs (4) for each available all-good cofactor and minimizes
`sum r_k` over the sixteen incidence masks.  It then sums this exact minimum
over the eight triangles.

This formulation automatically handles all degeneracies:

* with four good cofactors it recovers the demand of at least three
  incidences;
* if one selected row is zero, the complementary all-good triple still
  demands at least two; and
* for a zero reference block it omits precisely the one cofactor not supplied
  by the restricted syzygy theorem.

No incidence is demanded from a triple containing a zero selected row, so
the count is deliberately conservative.

## 5. Incidence capacity of a block column

For each right column, place the twelve row labels `(i,c)` into a union-find
structure.  Selecting an oriented-triangle incidence identifies its three
labels.  A mask is admissible only when these identifications do not merge
two initially distinct row points belonging to the same physical block;
zero rows are absent, and prescribed rank-one or rank-two proportionalities
are pre-identified.

Exhausting the `2^8` triangle masks gives the following sharp joint capacity
bounds for a column containing the displayed exceptional row matroids:

\[
\begin{array}{c|cccc}
\text{exceptional ranks}&\text{none}&(2,2)&(2,1)&(2,0)\\ \hline
\text{maximum incidences}&4&4&3&2.
\end{array}                                               \tag{5}
\]

In particular, putting two singular blocks in one right column never
increases the ordinary capacity four.  The capacities of the four right
columns add, since each incidence belongs to exactly one column.

## 6. Demand always exceeds capacity

The checker enumerates all positions with distinct block rows, both column
relations in (2), and every pair of row-matroid types.  There are 20,160
configurations.  The exact extrema are:

| ranks | position | minimum demand | maximum capacity | minimum `demand-capacity` |
|---|---|---:|---:|---:|
| `(2,2)` | same column | 20 | 16 | 6 |
| `(2,2)` | different columns | 19 | 16 | 5 |
| `(2,1)` | same column | 18 | 15 | 5 |
| `(2,1)` | different columns | 16 | 14 | 3 |
| `(2,0)` | same column | 15 | 14 | 2 |
| `(2,0)` | different columns | 14 | 14 | 1 |

The demand and capacity extrema in a row need not occur for the same
matroid pair; the last column is minimized on correlated configurations and
is the decisive quantity.  It is strictly positive in all six cases.

Thus the zero-cofactor equations demand more oriented-triangle incidences
than the four physical block columns can carry.  This contradiction excludes
exactly two singular blocks whenever either has rank two.  Combining with
the prior at-least-two theorem proves Theorem 1.1.

## 7. Boundary left after this step

A putative full-chart point now lies in one of two narrower strata:

1. at least three cross blocks are singular; or
2. exactly two are singular and both have rank at most one.

The support nondegeneration example in
[`two-k4-rank2-support-nondegeneration.md`](two-k4-rank2-support-nondegeneration.md)
remains relevant: a single kernel contraction does not produce this
incidence contradiction.  The new result comes from simultaneous permanent
cofactor propagation across all eight oriented triangles, not from deletion
of an edge in the transversal graph.
