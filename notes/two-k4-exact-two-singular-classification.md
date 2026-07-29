# Exact-two singular blocks are severely rank-collapsed

> **Superseded frontier.**  The later rank-independent erasure argument in
> [`two-k4-no-exact-two-singular.md`](two-k4-no-exact-two-singular.md)
> excludes the entire exact-two stratum.  The classifications below remain
> valid intermediate results but no listed survivor is realizable.

## 1. Result

Suppose the sixteen cross blocks of the two-`K_4` chart satisfy all left and
right dead-slab equations, and suppose exactly two of those blocks are
singular.  The following strengthens the two-singular boundary theorem.

**Theorem 1.1.**  Both singular blocks have rank at most one.  Thus their
unordered rank pair belongs to

\[
                         \boxed{\ \{1,1\},\ \{1,0\},\ \{0,0\}\ }. \tag{1}
\]

In particular:

* rank pairs `22` and `21` exceed even the coarse incidence capacity in every
  relative position; and
* the correlated row-matroid audit in
  [`two-k4-rank2-three-singular-boundary.md`](two-k4-rank2-three-singular-boundary.md)
  also excludes the residual pair `20`.

Thus the exact-two boundary has only two maps of rank at most one.  The
present rank-two incidence count does not force the two remaining blocks to
be aligned.  The subsequent low-rank audit in
[`two-k4-exact-two-low-rank-normal-forms.md`](two-k4-exact-two-low-rank-normal-forms.md)
excludes the pair `11` and gives the sharp positional row/column support
forced in the pair `10`.  The exact finite audits are

```text
computations/verify_two_k4_exact_two_singular_classification.py
computations/verify_two_k4_rank2_three_singular_boundary.py
computations/verify_two_k4_exact_two_low_rank_normal_forms.py
```

## 2. Rank-one statuses with zero coordinate images

For an oriented left triangle and a right block column, collect its three
selected row vectors into a local map `A:C^3 -> V`.  Call the triangle-column
pair a **rank-one status** if `rank A<=1`.  When one selected row is zero,
this means that the other two rows are proportional; when two are zero it
is automatic.  Hence the status is determined by the projective row
matroids in that block column, retaining zero rows rather than discarding
them.

We use two consequences of the zero-`Per_3` lemmas.

1. If a zero three-factor restriction has no zero coordinate image, at
   least two of its three local maps have rank one.
2. If some coordinate image is zero but the triple contains a map with no
   zero coordinate image, at least one local map has rank one.  Indeed, if
   all three ranks were at least two, the rank-two classification would
   make all three maps kill one common coordinate basis vector, contrary to
   the nonvanishing map.

Every column triple considered below contains a structurally invertible
block column, so the second assertion always applies in a dirty triple.
If all four complementary `Per_3` tensors vanish, these rules force at least
three rank-one statuses for a clean oriented triangle and at least two for a
dirty one.

## 3. Exact projective capacities

There are only eight oriented triangles.  Their possible simultaneous
rank-one statuses can be enumerated by union-find on the twelve labels
`(vertex,colour)`.  At an invertible block, its three labels must remain in
distinct projective classes.  At a singular block, use its exact row
matroid:

* rank two: three distinct nonzero points, one proportional pair and a
  transverse point, or one zero row and two distinct points;
* rank one: an arbitrary nonempty set of nonzero rows, all in one class;
* rank zero: all three rows absent.

Joining the nonzero selected labels of any requested triangle and rejecting
forbidden within-vertex identifications gives the following exact maximum
capacities.

For a block column containing one singular block, counting every rank-one
status including those with a selected zero row,

\[
\begin{array}{c|ccc}
\operatorname {rank}&2&1&0\\ \hline
\text{maximum statuses}&4&5&6.
\end{array}                                              \tag{3}
\]

For a block column containing two singular blocks at different vertices,

\[
\begin{array}{c|cccccc}
\text{rank pair}&22&21&20&11&10&00\\ \hline
\text{maximum statuses}&5&5&6&6&6&6.
\end{array}                                              \tag{4}
\]

The checker exhausts every zero-row support and every allowed proportional
row partition, not merely the generic matroid in each rank.

## 4. Singular blocks in disjoint positions

Put the two exceptional blocks at `B_00` and `B_11`.  The other two block
columns are good and contribute capacity at most eight.  Let `z_0,z_1` be
the numbers of zero rows in the exceptional blocks.  A zero row is selected
by exactly two of the eight oriented triangle contexts, so the number `u`
of dirty contexts satisfies

\[
                         u\le\min(8,2(z_0+z_1)).         \tag{5}
\]

Every block row contains at most one singular reference block.  The
restricted syzygy theorem therefore makes all four complementary tensors
zero when that block has positive rank.  For a zero reference block, the
three complements containing its block column vanish; these still require
three statuses in a clean context and two in a context dirtied by the other
exceptional block.  Thus total demand is at least

\[
                              24-u.                     \tag{6}
\]

Use `z<=1,2,3` in ranks `2,1,0`, respectively, together with (3).  The six
rank pairs give:

\[
\begin{array}{c|rrrrrr}
\text{rank pair}&22&21&20&11&10&00\\ \hline
\text{demand at least}&20&18&16&16&16&16\\
\text{capacity at most}&16&17&18&18&19&20.
\end{array}                                              \tag{7}
\]

Only the first two columns are contradictory.  Thus disjoint rank pairs
`22` and `21` are impossible.  The lower-rank columns are retained as
honest survivors of this coarse incidence count, not silently discarded.

## 5. Two blocks in one block row or column

Now suppose the exceptional blocks are aligned.  Transpose if necessary so
that, for the incidence count, they occupy one block column at two different
vertices.  The other three block columns have total capacity twelve.  For
rank pairs `22` and `21`, every singular reference block has positive rank,
so all four cofactors vanish.  Equations (5)--(6) still apply, while (4)
supplies the exceptional-column capacity:

\[
\begin{array}{c|rr}
\text{rank pair}&22&21\\ \hline
\text{demand at least}&20&18\\
\text{capacity at most}&12+5=17&12+5=17.
\end{array}                                              \tag{8}
\]

Both cases are impossible.  Along with the disjoint calculation, this
excludes rank pairs `22` and `21` in every relative-position orbit.  The
coarse extrema leave `20`, but the correlated enumeration in the companion
rank-two note installs only all-good cofactor constraints and compares their
demand with the exact joint matroid capacity configuration by configuration.
Its minimum demand-capacity gap for `20` is two in the same-column orbit and
one in the different-column orbit.  Hence `20` is impossible as well, which
proves (1).

## 6. Subsequent closure of the low-rank locus

The result proved here is the rank-two exclusion.  Its coarse count leaves
pairs `11`, `10`, and `00`.  The companion low-rank audit cited above goes
further by excluding `11` and forcing sparse normal forms in pair `10`.
Finally, the later rank-independent erasure certificate cited at the top
excludes all of these residual cases at once.  Thus the current boundary
starts with at least three singular blocks.
