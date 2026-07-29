# The exact-three incidence boundary and its subsequent closure

## 1. Result

Assume that the sixteen cross blocks in the two-`K_4` chart satisfy both
families of dead-slab permanent equations and that exactly three blocks are
singular.  Up to independent permutations of the four block rows and
columns and transposition, the three exceptional positions have four
orbits:

\[
\begin{array}{c|c|c}
\text{orbit}&\text{normal form}&\text{number of labelled supports}\\ \hline
\text{three-star}&(0,0),(1,0),(2,0)&32\\
\text{two-star plus isolated}&(0,0),(1,0),(2,1)&288\\
\text{three-edge path}&(0,0),(0,1),(1,0)&144\\
\text{matching}&(0,0),(1,1),(2,2)&96.
\end{array}                                                     \tag{1}
\]

The orbit sizes sum to `560=binom(16,3)`.

**Theorem 1.1.**  The three-star and the two-star-plus-isolated position
orbits are impossible.  Hence every exact-three survivor has its singular
positions on either a three-edge path or a three-edge matching.

The matching survivor of this incidence relaxation is subsequently
excluded by the projective-frame contraction theorem in
[`two-k4-exact-three-matching-obstruction.md`](two-k4-exact-three-matching-obstruction.md).
Consequently the three-edge path is the only remaining exact-three orbit.

The same audit gives strong rank restrictions on the two survivors.

1. On a matching, either all three singular blocks have rank at most one,
   or exactly one has rank two and the other two are zero.  If at least two
   rank-one blocks are nonzero, their nonzero coordinate-row supports are
   the same singleton; applying the transposed audit gives the analogous
   common singleton column support.  Thus all nonzero rank-one blocks are
   scalar multiples of one common matrix unit.
2. On a path, call the degree-two block position the corner and the other
   two positions the arms.  At least one arm block is zero, every nonzero
   arm has rank one, and the corner has rank at most two.

The later path rank-`(2,1,0)` obstruction strengthens the second statement:
if the corner has rank two, both arms are zero.

The still stronger sparse-reference collapse in
[`two-k4-exact-three-path-zero-collapse.md`](two-k4-exact-three-path-zero-collapse.md)
shows that every exact-three path block must in fact be zero.

Finally,
[`two-k4-exact-three-allzero-path-obstruction.md`](two-k4-exact-three-allzero-path-obstruction.md)
uses the exact one-defect `Per_3` equations to exclude that literal zero
path.  Thus the full exact-three stratum is empty.

These are necessary conditions, not constructions.  The exact checker is
[`verify_two_k4_exact_three_incidence_boundary.py`](../computations/verify_two_k4_exact_three_incidence_boundary.py).

## 2. Status constraints and their monotone relaxation

Use the eight oriented triangles `t=0,...,7` in the order displayed in
[`two-k4-no-exact-two-singular.md`](two-k4-no-exact-two-singular.md).
For a fixed triangle and physical block column, its three selected row
vectors form a local map.  A **status** means that this map has rank at most
one.

Whenever a reference block row contains at most one singular block, the
restricted square-free syzygy theorem supplies every complementary
cofactor, except possibly the cofactor omitting a zero reference block
itself.  A zero `Per_3` cofactor then has the following consequences.

* If all its coordinate images are nonzero, at least two of its three
  column maps are statuses.
* If one of its three column maps has all coordinate images nonzero, at
  least one column map is a status.

For position-only arguments we erase every row vector contributed by an
exceptional physical block.  A genuine status remains a status after this
erasure.  A clean zero cofactor therefore demands two relaxed statuses; a
dirty cofactor containing at least one wholly invertible column demands
one.  This forgets all ranks and projective data of the singular blocks and
is a monotone relaxation.

For the sharper rank audit, retain the complete projective row matroid of
each singular matrix.  There are fifteen relaxed types:

* seven rank-two types: three distinct nonzero row points, one prescribed
  proportional pair and a third point, or one zero row and two distinct
  points;
* seven rank-one types, indexed by their nonempty coordinate-row support;
  and
* the zero type.

In the first rank-two type the checker forgets the linear dependence of
the three distinct points.  This only enlarges the feasible set.
Union-find exhausts all `2^8` simultaneous status patterns in each physical
column, and a 32-variable Boolean check couples the four columns to every
available cofactor constraint.

## 3. Two-star plus isolated: a hand contradiction

Normalize the exceptional positions to

\[
                              (0,0),(1,0),(2,1).         \tag{2}
\]

Erase vertices 0 and 1 in column 0 and vertex 2 in column 1.  For each of
lines `t=1,2`, the three universally available cofactors omitting columns
1, 2, and 3 give

\[
 r_{t0}=1\quad\text{or}\quad
 r_{t1}+r_{t2}+r_{t3}\geq2,                             \tag{3}
\]

where `r_tj` is the relaxed status bit.  For lines `t=4,5`, the cofactor
omitting column 0 is clean and gives

\[
                       r_{t1}+r_{t2}+r_{t3}\geq2.       \tag{4}
\]

The two statuses `r_10,r_20` cannot coexist.  After the two erasures their
triples share the row `(2,0)` but use different rows `(3,1),(3,2)` of the
invertible block at vertex 3.

Suppose first that neither line 1 nor line 2 uses column 0.  Equations
(3)--(4) demand eight statuses across columns 1, 2, and 3.  Each of those
columns has capacity at most two on the four lines `1,2,4,5`: the disjoint
incompatible pairs are `(1,5)` and `(2,4)`.  Thus the total capacity is six,
a contradiction.

Exactly one of lines 1 and 2 may therefore use column 0.  If it is line 1,
then lines `2,4,5` each demand two statuses across the three remaining
columns.  Equality with capacity six is forced.  In every one of those
columns the pair `(2,4)` is incompatible, so every saturated two-status
choice contains line 5.  Line 5 would occur in all three columns, although
equality forces it to occur exactly twice.  This is impossible.  If line 2
uses column 0, the incompatible pair `(1,5)` similarly forces line 4 into
all three columns.  This excludes (2), independently of the three ranks.

## 4. Three-star: first zero, then transpose

Put the exceptional blocks at `B_00,B_10,B_20`.  There is at most one in
each reference block row.  The exact projective-matroid audit enumerates
all

\[
                              15^3=3375                       \tag{5}
\]

ordered row-type triples.  The only feasible triple is

\[
                                  (0,0,0).                    \tag{6}
\]

Thus all three exceptional blocks would have to be literal zero matrices.
This finite statement uses every available clean and dirty cofactor
constraint and exact simultaneous projective capacity; no comparison of
uncorrelated extrema is made.

Transpose.  The zero blocks now occupy `B_00,B_01,B_02`.  On each of lines
0 and 1, the reference-row syzygy is simply

\[
                              B_{03}y_3C_3=0.                 \tag{7}
\]

Since `B_03` is invertible, `C_3=0`.  Its columns `0,1,2` are clean because
the reference row is omitted, so each line demands two statuses there.

For each of lines 5 and 7, the three cofactors omitting columns `0,1,2`
are zero.  They say

\[
 r_{t3}=1\quad\text{or}\quad
 r_{t0}+r_{t1}+r_{t2}\geq2.                             \tag{8}
\]

Lines 5 and 7 cannot both be statuses in the invertible column 3: they
share `(1,0)` and would identify the distinct rows `(0,2),(0,1)`.  Hence at
least one of them, call it `ell`, demands two statuses in columns `0,1,2`.
Together with lines 0 and 1, this is demand six.  Each of the three columns
has capacity two on these three lines.  If `ell=5`, the pair `(1,5)` is
incompatible after vertex 0 is erased, so saturation forces line 0 into
all three columns, contradicting its exact equality count two.  If
`ell=7`, the incompatible pair `(0,7)` instead forces line 1 into all three.
Thus the all-zero possibility (6) is also impossible, and the three-star
orbit is closed.

## 5. Matching survivor of the incidence audit (subsequently excluded)

For the matching positions `(0,0),(1,1),(2,2)`, the row-matroid audit leaves
28 of the 3375 triples.  Their rank histogram is

\[
\begin{array}{c|ccccccccccc}
(d_0,d_1,d_2)&000&001&002&010&011&020&100&101&110&111&200\\ \hline
\#&1&4&1&4&3&1&4&3&3&3&1.
\end{array}                                                     \tag{9}
\]

In particular, a rank-two block can occur only alone, with the other two
blocks zero.  The permitted rank-two row type has one prescribed zero
coordinate row.  If two or three rank-one blocks are nonzero, all their
row supports are the same singleton.  Applying the identical audit after
transposition gives a prescribed zero coordinate column in the rank-two
case and a common singleton column in the multiple-rank-one case.  This
proves the matching assertions in Theorem 1.1.

These 28 relaxed row patterns are all incompatible with the actual
four-cross tensor equation.  The companion matching-obstruction note
enumerates their 3,591 non-all-zero status models and gives a direct
all-zero contraction, thereby closing this entire position orbit.

## 6. Path survivor

For the path positions

\[
                         (0,0),(0,1),(1,0),                    \tag{10}
\]

write the ranks in that order, with the corner first.  One shore leaves 74
row-matroid triples.  Intersecting its rank patterns with the transposed
audit, which exchanges the two arms, leaves exactly

\[
\begin{split}
 &(0,0,0),(0,0,1),(0,1,0),\\
 &(1,0,0),(1,0,1),(1,1,0),\\
 &(2,0,0),(2,0,1),(2,1,0).                              \tag{11}
\end{split}
\]

Thus one arm is zero, the other has rank at most one, and the corner has
rank at most two.  This proves the path assertion.

The actual four-cross tensor equations subsequently eliminate every
nonzero block on the path; see
[`two-k4-exact-three-path-zero-collapse.md`](two-k4-exact-three-path-zero-collapse.md).
The exact one-defect obstruction then eliminates the literal all-zero path
as well.

## 7. Frontier

The two-`K_4` dead slabs force at least four singular cross blocks.  All four
exact-three position orbits are closed.  Further progress starts on the
four-or-more-singular boundary; the two-cross and live target equations
remain unused in this singularity count.
