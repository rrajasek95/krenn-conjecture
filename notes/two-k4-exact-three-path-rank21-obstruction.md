# A rank-two path corner cannot have a nonzero arm

> **Superseded frontier.**  The later sparse-reference collapse in
> [`two-k4-exact-three-path-zero-collapse.md`](two-k4-exact-three-path-zero-collapse.md)
> proves that the corner and both arms must all be zero.  The rank-`(2,1,0)`
> certificate below remains an independently checked intermediate theorem.

## 1. Result

Normalize an exact-three path of singular cross blocks to

\[
                         B_{00},B_{01},B_{10}.                 \tag{1}
\]

The block `B_00` is the corner and the other two blocks are the arms.  The
incidence boundary proves that one arm is zero, the other has rank at most
one, and the corner has rank at most two.

**Theorem 1.1.**  If `B_00` has rank two, then both arms in (1) are zero.

Equivalently, the terminal path split consisting of a rank-two corner, one
rank-one arm, and one zero arm is impossible.  The proof uses only the dead
four-cross tensor equations.  Thus it is stronger than a contradiction
using the two-cross or live target equations.

The exact checker is
[`verify_two_k4_exact_three_path_rank21_obstruction.py`](../computations/verify_two_k4_exact_three_path_rank21_obstruction.py).

## 2. Put the rank-one arm in the corner row

Suppose, toward a contradiction, that one arm has rank one.  Transposition
exchanges `B_01` and `B_10` and preserves the corner rank.  We may therefore
assume

\[
             (\operatorname {rank}B_{00},
              \operatorname {rank}B_{01},
              \operatorname {rank}B_{10})=(2,1,0).            \tag{2}
\]

Apply the left dead-slab incidence audit in this orientation.  Of all
relaxed projective row-matroid triples, only

\[
                         (Z1,S1,0),\qquad (Z2,S2,0)            \tag{3}
\]

survive its clean and dirty zero-`Per_3` constraints.  Here `Zc` denotes a
rank-two matrix whose coordinate row `c` is zero and whose other two rows
are projectively distinct, while `Sc` denotes a rank-one matrix supported
only on coordinate row `c`.

Thus the corner and the nonzero arm would have complementary row support:
the row supporting the arm is precisely the zero row of the corner.  This
is only a necessary normal form, not yet a contradiction.

## 3. Projective-frame singleton closure

For a dead left word `a`, the actual four-cross tensor is

\[
 T_a=
 \sum_{\pi\in S_4}\ \bigotimes_{j=0}^3
 e_{a_{\pi^{-1}(j)}}^{\mathsf T}
 B_{\pi^{-1}(j),j}=0.                                   \tag{4}
\]

The projective-frame singleton lemma from
[`two-k4-exact-three-matching-obstruction.md`](two-k4-exact-three-matching-obstruction.md)
says that (4) is impossible if contractions in three right factors isolate
one active permutation.  The contractions used here are certified duals
to the three row lines of specified invertible physical blocks.  Hence
unrecorded proportionalities between different blocks cannot merge two
signature classes.

For each type in (3), the checker enumerates all simultaneous eight-bit
oriented-triangle status masks in the four physical columns, imposes every
cofactor constraint from the restricted four-vector syzygy, and searches
the dead words in (4).  The exact counts are

\[
\begin{array}{c|c|c}
\text{row-matroid triple}&\text{admissible status models}&
 \text{models with a singleton}\\ \hline
(Z1,S1,0)&480&480\\
(Z2,S2,0)&480&480.
\end{array}                                                   \tag{5}
\]

Two representative certificates are displayed below.  Bit `t` of a mask
is the status on oriented triangle `t`; a witness is
`(dead word, contracted columns, unique permutation)`.

\[
\begin{array}{c|c|c}
\text{type}&(m_0,m_1,m_2,m_3)&(a,J,\pi)\\ \hline
(Z1,S1,0)&(8c,f0,60,98)&(1120,013,1203)\\
(Z2,S2,0)&(2c,f0,64,90)&(1001,012,2310).
\end{array}                                                   \tag{6}
\]

For every model, contracting (4) with the three selected frame duals leaves
a nonzero scalar times a nonzero row vector in the fourth factor.  This
contradicts `T_a=0`.  The complete sorted table of 960 certificates is
frozen by SHA-256 digest

```text
420539678a6c51017cbc3d85cf2768fe08b31b3088f6cc7132b366d0d889ef5a
```

The row-matroid and status enumerations are conservative: the dependent
three-row rank-two type is relaxed, and only necessary cofactor constraints
are imposed.  Therefore exhausting this larger finite set proves the claim
for every actual complex matrix array.  Transposing back completes the
proof of Theorem 1.1.

## 4. Reduced path frontier

Every exact-three path survivor now has one of the following forms:

1. the corner has rank at most one, one arm is zero, and the other has rank
   at most one; or
2. the corner has rank two and both arms are zero.

The second case is the sole remaining rank-two path boundary.  The first
case contains only rank-at-most-one singular blocks.  Neither statement is
a construction; both remain subject to the four-cross, two-cross, and live
target equations not yet used in the incidence relaxation.
