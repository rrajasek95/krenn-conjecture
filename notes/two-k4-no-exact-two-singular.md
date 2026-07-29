# The two-`K_4` dead slabs force at least three singular blocks

## 1. Result

Let

\[
                       B_{ij}\in\operatorname {Mat}_3(\mathbb C),
                       \qquad 0\leq i,j<4,                 \tag{1}
\]

be the sixteen cross blocks in the full two-`K_4` chart.  Impose the left
and right dead-slab equations for the four-cross permanent tensor.  The
earlier boundary theorem proved that at least two blocks are singular.  The
exact-two stratum is in fact empty.

**Theorem 1.1.**  Every array satisfying both dead-slab families has at
least three singular cross blocks.

The new step uses no live target coefficient, internal-edge weight, or
Hamilton-cycle dead word.  It is a pair of small hand incidence
certificates.  The exact audit is
[`verify_two_k4_no_exact_two_singular.py`](../computations/verify_two_k4_no_exact_two_singular.py).

## 2. Universal cofactor and erasure lemmas

Index the eight oriented-triangle dead coordinate lines by

\[
\begin{array}{c|c|c}
t&\text{hole}&\text{fixed }(\text{vertex},\text{colour})\text{ labels}\\ \hline
0&0&(1,1),(2,2),(3,0)\\
1&0&(1,2),(2,0),(3,1)\\
2&1&(0,1),(2,0),(3,2)\\
3&1&(0,2),(2,1),(3,0)\\
4&2&(0,0),(1,1),(3,2)\\
5&2&(0,2),(1,0),(3,1)\\
6&3&(0,0),(1,2),(2,1)\\
7&3&(0,1),(1,0),(2,2).
\end{array}                                                   \tag{2}
\]

For a line with hole `i`, contraction of the right factors gives

\[
                         \sum_{j=0}^3 B_{ij}y_jC_j=0,          \tag{3}
\]

where `C_j` is the complementary three-factor permanent tensor.  We use
the restricted square-free syzygy theorem from
[`two-k4-two-singular-boundary.md`](two-k4-two-singular-boundary.md) in the
following deliberately weakened form.

**Lemma 2.1 (universal cofactor propagation).**  Suppose a reference block
row contains at most one singular block, in column `s`.  Then

\[
                              C_j=0\qquad(j\ne s).              \tag{4}
\]

If the reference row is entirely invertible, all four `C_j` vanish.

Indeed, a rank-one or rank-two reference block makes all four cofactors
zero, while a zero reference block may leave only `C_s` undetermined.
Forgetting `C_s` in every rank is therefore a valid relaxation.

We also use two forms of the local zero-`Per_3` lemma.  If

\[
                   (A_1\otimes A_2\otimes A_3)\operatorname {Per}_3=0,
                                                                  \tag{5}
\]

then:

1. if every coordinate basis vector has nonzero image under every `A_r`,
   at least two of the three maps have rank at most one; and
2. if at least one `A_r` has all three coordinate images nonzero, at least
   one of the maps has rank at most one.

The first assertion is Lemma 3.1 of the preceding note.  For the second,
if all three ranks were at least two, the rank-two classification of a zero
restriction of `Per_3` would say that all three maps kill the same
coordinate basis vector.  This contradicts the displayed wholly nonzero
map.

For the two exceptional physical blocks, now **erase** their selected row
vectors whenever they occur in a local map.  Call a triangle-column pair a
relaxed status when the remaining selected row vectors span a space of
dimension at most one.  Any genuine rank-at-most-one local map remains a
relaxed status after erasure.  Consequently:

* a clean zero cofactor demands at least two relaxed statuses in its three
  columns; and
* a zero cofactor containing an exceptional block but also a wholly
  invertible column demands at least one relaxed status.

Erasure forgets the ranks, nonzero supports, and projective points of the
two singular matrices.  Thus every capacity bound below is an upper bound
for singular blocks of arbitrary ranks.

## 3. Aligned exceptional blocks: `4>3`

If the exceptional positions share a block row, transpose the array.  We
may therefore assume that they occupy distinct rows.  First suppose they
share a column; normalize their positions to `B_00,B_10`.

Use lines `t=4,6` and, in both, the zero cofactor `C_0`.  The reference rows
2 and 3 are entirely invertible, and the complementary columns are
`{1,2,3}`, so both cofactors are clean.  Each demands two relaxed statuses,
for a total demand of four.

In any fixed column `j in {1,2,3}`, the statuses for lines 4 and 6 cannot
both hold.  Their triples share the row label `(0,0)` but use the two
different labels `(1,1)` and `(1,2)` at vertex 1.  Simultaneous
proportionality would make two rows of the invertible block `B_1j`
proportional.  Thus each of the three columns has capacity one:

\[
                         4\ \leq\ 1+1+1=3,                     \tag{6}
\]

a contradiction.  This closes the same-column orbit and, after
transposition, the same-row orbit.

## 4. Disjoint exceptional blocks: `10>9`

Normalize the remaining position orbit to `B_00,B_11`.  Select the six
zero cofactors in the following table.  `Columns` lists the three local
maps in the cofactor.

\[
\begin{array}{c|c|c|c}
t&\text{cofactor}&\text{columns}&\text{status demand}\\ \hline
0&C_1&0,2,3&2\\
1&C_1&0,2,3&2\\
2&C_0&1,2,3&2\\
3&C_0&1,2,3&2\\
5&C_2&0,1,3&1\\
7&C_2&0,1,3&1.
\end{array}                                                   \tag{7}
\]

For `t=0,1`, Lemma 2.1 supplies `C_1=0`; the row-zero exceptional block is
in the reference row and the other exceptional block lies in the omitted
column.  Hence these cofactors are clean.  The same argument with the
shores interchanged inside the array makes `t=2,3` clean.  Lines 5 and 7
have entirely invertible reference rows, so `C_2=0`; their cofactor contains
both exceptional blocks, but column 3 is wholly invertible.  The dirty
form of Lemma 2.2 therefore gives demand one.  The total demand in (7) is

\[
                              2+2+2+2+1+1=10.                  \tag{8}
\]

The following table partitions every status counted in a physical column
into incompatible pairs.  In columns 0 and 1 the exceptional vertex is
erased; columns 2 and 3 are wholly invertible.

\[
\begin{array}{c|c|c|c}
\text{column}&\text{counted lines}&\text{incompatible pairs}&
 \text{capacity}\\ \hline
0&0,1,5,7&(0,7),(1,5)&2\\
1&2,3,5,7&(2,7),(3,5)&2\\
2&0,1,2,3&(0,3),(1,2)&2\\
3&0,1,2,3,5,7&(0,3),(1,2),(5,7)&3.
\end{array}                                                   \tag{9}
\]

For completeness, each incompatibility is immediate from (2).  The two
statuses share one non-erased row label, so their proportionality classes
merge, while at another physical vertex they contain two different colour
rows of the same invertible block.  For example, in column 0, lines 0 and
7 share `(2,2)` after vertex 0 is erased and would identify `(1,1)` with
`(1,0)`.  The other pairs work identically.  Since the pairs in each row of
(9) are disjoint and cover all counted statuses, the stated capacities
follow.  Summing gives

\[
                              10\ \leq\ 2+2+2+3=9,             \tag{10}
\]

again impossible.

## 5. Consequence

Every pair of distinct block positions is either aligned or disjoint, up
to transposition.  Sections 3 and 4 exclude both orbits without using the
ranks of the two exceptional blocks.  Thus exactly two singular blocks are
impossible.  Combining this with the earlier theorem excluding zero or one
singular block proves Theorem 1.1.

This supersedes the rank-by-rank exact-two boundary classifications: their
normal forms remain correct intermediate statements, but none is realized
even by the dead-slab equations.
