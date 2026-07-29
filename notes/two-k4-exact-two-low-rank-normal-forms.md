# Exact-two low-rank normal forms

> **Superseded frontier.**  The later hand certificates in
> [`two-k4-no-exact-two-singular.md`](two-k4-no-exact-two-singular.md)
> exclude the complete exact-two stratum.  The normal forms below remain
> correct necessary intermediate conditions, but none is realized.

## 1. Result

Let

\[
                       B_{ij}\in\operatorname {Mat}_3(\mathbb C),
                       \qquad 0\leq i,j<4,                 \tag{1}
\]

be the sixteen cross blocks in the full two-`K_4` chart, and impose both
families of dead-slab permanent equations.  Suppose exactly two cross
blocks are singular.  The rank-two boundary theorem and its exact
correlated audit already show that both exceptional blocks have rank at
most one.

**Theorem 1.1.**  The two singular blocks cannot both have rank one.  Thus
their unordered rank pair is

\[
                              \boxed{\{1,0\}\text{ or }\{0,0\}}.          \tag{2}
\]

Moreover, if the ranks are `1` and `0`, write `R` for the rank-one block
and `Z` for the zero block.  Their positions force the following necessary
normal forms:

\[
\begin{array}{c|c}
\text{relative block positions of }R,Z&\text{support forced on }R\\ \hline
\text{different block rows and columns}&R=\alpha e_p e_q^{\mathsf T}\\
\text{same block row}&R=u e_q^{\mathsf T}\\
\text{same block column}&R=e_p v^{\mathsf T}.
\end{array}                                                       \tag{3}
\]

Here `alpha` is nonzero, and `u,v` are nonzero but need not be coordinate
vectors.  Thus a disjoint rank-one block is a scalar matrix unit; in the
aligned cases only one coordinate column or row is forced.  These are
necessary boundary normal forms, not constructions of solutions.

The exact finite audit is
[`verify_two_k4_exact_two_low_rank_normal_forms.py`](../computations/verify_two_k4_exact_two_low_rank_normal_forms.py).
It imports the incidence engine from
[`verify_two_k4_rank2_three_singular_boundary.py`](../computations/verify_two_k4_rank2_three_singular_boundary.py).

## 2. A conservative incidence test

Orient the array so that the two exceptional blocks occupy different block
rows.  This is always possible: if they originally share a block row, they
have different block columns, so transposition puts them in different
rows.  After relabelling, their positions are

\[
                          B_{00},\qquad B_{1\epsilon},
                          \qquad \epsilon\in\{0,1\},       \tag{4}
\]

where `epsilon=0` is the same-column orbit and `epsilon=1` the
different-column orbit.

For each of the eight oriented-triangle dead coordinate lines, the
restricted square-free syzygy theorem supplies three or four certified
zero complementary `Per_3` tensors.  A right block column is called good
in that triangle when all three selected row vectors are nonzero.  For
every certified zero `Per_3` involving three good columns, the local
zero-permanent lemma forces at least two of their three local maps to have
rank one.  The checker exhausts the four possible incidence bits and uses
the smallest number satisfying only these certified constraints.  It
discards every constraint containing a selected zero row, so zero
coordinate images cannot create a spurious lower bound.

The capacity side is also exact for the information retained.  In an
invertible block the three row points are distinct.  A rank-one block has a
nonempty support `S` of rows and all points in `S` are proportional; a zero
block has empty support.  Union-find exhausts every simultaneous subset of
the eight oriented-triangle incidences and rejects any identification of
two distinct row points belonging to one invertible block.  Summing these
per-column maxima gives an upper bound on realizable total incidence.

For each individual position-and-matroid configuration the same
configuration supplies both numbers.  Hence a positive correlated gap

\[
                     \text{demand}-\text{capacity}>0                  \tag{5}
\]

is a contradiction; no comparison of unrelated extrema is used in the
proof.

## 3. Two rank-one blocks are impossible

There are seven row-support types for each rank-one block.  Exhausting all
ordered distinct block rows, all columns, and all `7^2` pairs gives:

\[
\begin{array}{c|r|r|r|r}
\text{column orbit}&\#\text{ configurations}&
 \min D&\max C&\min(D-C)\\ \hline
\text{same}&2352&16&14&4\\
\text{different}&7056&14&12&2.
\end{array}                                                       \tag{6}
\]

The last column is strictly positive in both position orbits.  Thus the
rank pair `11` is impossible.  Combined with the preceding rank-two
exclusion, this proves (2).

## 4. A rank-one block next to a zero block

Now let `t` be the number of nonzero rows of the rank-one block in the
orientation (4).  The zero block has its unique row matroid.  Refining the
same audit by `t` gives:

\[
\begin{array}{c|c|r|r|r|r|r}
\text{column orbit}&t&\#&\min D&\max C&\min(D-C)&
 \#\{D-C\leq0\}\\ \hline
\text{same}&1&144&12&13&0&48\\
\text{same}&2&144&15&13&2&0\\
\text{same}&3& 48&18&13&5&0\\
\text{different}&1&432&11&12&-1&432\\
\text{different}&2&432&14&12&2&0\\
\text{different}&3&144&18&12&6&0.
\end{array}                                                       \tag{7}
\]

Every configuration with `t>=2` has positive correlated gap.  Therefore,
whenever the rank-one and zero blocks occupy different block rows, the
rank-one matrix has exactly one nonzero row.  The `t=1` entries are retained
as genuine survivors of this incidence test; the table does not assert
that they solve the remaining equations.

## 5. Returning to the original orientation

The one-row conclusion and its transposed version yield exactly the three
cases in (3).

* If the block positions are disjoint, they have different rows before and
  after transposition.  The rank-one matrix consequently has one nonzero
  row and one nonzero column, hence one nonzero entry.
* If the positions share a block column, the original orientation forces
  one nonzero row.  After transposition the positions share a row, so this
  audit supplies no second support condition.
* If the positions share a block row, transpose first.  The transposed
  rank-one matrix has one nonzero row, so the original matrix has one
  nonzero column.  Again there is no justified condition in the other
  direction.

This is why the matrix-unit conclusion is valid only in the disjoint orbit.

## 6. Subsequent closure

This audit confines every putative exact-two survivor to one of two
endpoint-degenerate loci:

1. two zero cross blocks, in an arbitrary relative-position orbit; or
2. one zero block and one rank-one block with the positional support in
   (3).

Only dead-slab equations were used.  The subsequent rank-independent
erasure argument cited at the top finishes both loci using stronger dirty
zero-cofactor incidence constraints; live and two-cross target equations
are not needed.
