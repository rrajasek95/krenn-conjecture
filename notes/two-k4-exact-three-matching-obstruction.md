# The exact-three matching orbit is impossible

## 1. Result

Let

\[
 B_{ij}\in \operatorname {Mat}_{3\times3}(\mathbb C),
 \qquad 0\leq i,j<4,
\]

be the cross blocks in the two-`K_4` chart, and write

\[
 P(a,b)=\operatorname {per}
       \bigl(B_{ij}[a_i,b_j]\bigr)_{0\leq i,j<4}.
                                                               \tag{1}
\]

Assume the left dead-slab equations

\[
                  P(a,b)=0
       \qquad(a\text{ dead},\ b\in\{0,1,2\}^4).              \tag{2}
\]

**Theorem 1.1.**  There is no array satisfying (2) in which exactly the
three matching blocks

\[
                         B_{00},B_{11},B_{22}                 \tag{3}
\]

are singular.

This closes both matching alternatives left by the incidence boundary:
three rank-at-most-one blocks on a common coordinate support, and one
rank-two block together with two zero blocks.  In fact, only the left dead
four-cross equations are needed; no two-cross equation, live target value,
or right-shore equation enters.

The proof uses an elementary contraction lemma on the actual four-cross
tensor.  A finite projective-matroid audit applies it to every nonzero
singular-row pattern.  The all-zero pattern has a short direct proof.  The
exact checker is
[`verify_two_k4_exact_three_matching_obstruction.py`](../computations/verify_two_k4_exact_three_matching_obstruction.py).

## 2. The four-cross tensor and a frame-singleton lemma

For a left word `a`, put

\[
 q_{ij}(a_i)=e_{a_i}^{\mathsf T}B_{ij}.
\]

Regard these as vectors in the right colour factor at site `j`.  Equation
(2), for a fixed dead `a` and every `b`, is the tensor identity

\[
 T_a=
 \sum_{\pi\in S_4}\ \bigotimes_{j=0}^3
 q_{\pi^{-1}(j),j}\bigl(a_{\pi^{-1}(j)}\bigr)=0.             \tag{4}
\]

A permutation is **active** if its four displayed vectors are nonzero.

**Lemma 2.1 (projective-frame singleton).**  Fix three right columns
`J`.  Suppose that, in every factor `j in J`, all projective lines occurring
among the active terms of (4) belong to a known three-element projective
frame.  If some triple of frame lines is used by exactly one active
permutation, then `T_a` is nonzero.

**Proof.**  In each of the three factors choose the dual covector which is
nonzero on the selected frame line and zero on the other two.  Contracting
(4) by their tensor product kills every active permutation except the
singleton.  What remains is a nonzero scalar times the singleton's nonzero
vector in the fourth factor.  This cannot vanish.  \(\square\)

The word "known" is important.  In the audit below, every relevant line is
identified with one of the three row lines of a specified invertible
physical block.  Consequently unrecorded accidental proportionalities
between different blocks cannot merge two selected lines: that would make
two rows of the invertible anchor block proportional.

## 3. Exact finite reduction for every nonzero row pattern

The preceding incidence audit leaves 28 projective row-matroid triples on
(3).  They use the fifteen relaxed singular types described in
[`two-k4-exact-three-incidence-boundary.md`](two-k4-exact-three-incidence-boundary.md):
seven rank-two types, seven rank-one supports, and the zero type.  The
rank-two type with three distinct nonzero rows is relaxed by forgetting its
linear dependence, so the finite model is an enlargement of the actual
geometric possibilities.

For each physical right column, encode by an eight-bit mask which oriented
triangle maps have rank at most one.  The checker performs the following
exhaustive steps.

1. It enumerates every simultaneous status mask compatible with the three
   prescribed row matroids.  Union-find takes the transitive closure of all
   forced projective identifications and rejects a mask if it identifies
   two distinct rows of one physical block.
2. It imposes every clean and dirty zero-`Per_3` cofactor constraint
   supplied by the restricted four-vector syzygy.  This gives a
   32-variable Boolean formula.  Every actual array with row pattern (3)
   maps to one of its models.
3. For every model and every dead word, it forms the active permutations in
   (4).  It searches three right factors whose relevant union-find classes
   are all anchored in invertible-block row frames, and then groups the
   permutations by their three frame lines.

Apart from the all-zero triple, the 27 surviving row-matroid triples give
exactly 3,591 Boolean models.  Their rank distribution is

\[
\begin{array}{c|c|c}
\text{rank pattern}&\text{number of its permutations}&
  \text{models for each ordered pattern}\\ \hline
(1,0,0)&3&1172\\
(1,1,0)&3&21\\
(1,1,1)&1&6\\
(2,0,0)&3&2.
\end{array}                                                   \tag{5}
\]

Every one of the 3,591 models has a frame-singleton witness

\[
                         (a,J,\pi).                           \tag{6}
\]

Thus Lemma 2.1 contradicts (4) in every case.  Two representative records,
one from each terminal matching alternative, are as follows.  Bit `t` of a
hexadecimal mask is the status on oriented triangle `t`.

\[
\begin{array}{c|c|c}
\text{row types}&(m_0,m_1,m_2,m_3)&(a,J,\pi)\\ \hline
(Z2,0,0)&(65,65,9a,9a)&(0102,012,1032)\\
(S0,S0,S0)&(9a,65,65,9a)&(0110,012,0231).
\end{array}                                                   \tag{7}
\]

Here `Z2` is rank two with coordinate row 2 zero, while `S0` is rank one
supported on coordinate row 0.  The checker verifies the two displayed
records individually and freezes the complete sorted witness table with
SHA-256 digest

```text
d689ff89121dbdec6b2cf708d0143a47ef0028619e9b412e4fba4586449355d8
```

This is a direct audit of the tensor equation (4), not a comparison of
separately optimized incidence demand and capacity.

## 4. Two local zero-`Per_3` defect lemmas

It remains to treat the row-matroid triple `(0,0,0)`.  We first record the
only local facts needed.

Let `A,B,C` be the three factor maps in a zero image of `Per_3`, and write
`a_i=Ae_i`, `b_i=Be_i`, and `c_i=Ce_i`.

**Lemma 4.1 (two defects).**  Suppose `b_1=0` and `c_2=0`, while every
other vector appearing below is nonzero.  Then `b_0` is proportional to
`b_2`, and `c_0` is proportional to `c_1`.

Indeed, only three permanent terms survive:

\[
 a_0\otimes b_2\otimes c_1+
 a_1\otimes b_2\otimes c_0+
 a_2\otimes b_0\otimes c_1=0.                               \tag{8}
\]

If `b_0,b_2` were independent, a covector killing `b_2` but not `b_0`
would leave a nonzero pure tensor.  The identical argument in the third
factor proves the assertion for `c_0,c_1`.

**Lemma 4.2 (three defects).**  Suppose `a_0=b_1=c_2=0` and all six active
vectors are nonzero.  Then each active pair in a common factor is
proportional.

Only the two derangements survive:

\[
 a_1\otimes b_2\otimes c_0+
 a_2\otimes b_0\otimes c_1=0.                               \tag{9}
\]

Equality of two nonzero pure tensors forces proportionality in every
factor.

Both lemmas are invariant under permutations of factors and coordinates.

## 5. Direct exclusion of three zero matching blocks

Now assume

\[
                         B_{00}=B_{11}=B_{22}=0.              \tag{10}
\]

For every oriented triangle, take the known zero cofactor omitting physical
column 3.  If its omitted left vertex is one of `0,1,2`, the resulting
`Per_3` has two distinct diagonal defects, so Lemma 4.1 makes both defective
column maps statuses.  If the omitted vertex is 3, all three diagonal
defects occur, and Lemma 4.2 makes all three column maps statuses.

In the standard triangle order

\[
\begin{array}{c|c}
0&(0;(1,1),(2,2),(3,0))\\
1&(0;(1,2),(2,0),(3,1))\\
2&(1;(0,1),(2,0),(3,2))\\
3&(1;(0,2),(2,1),(3,0))\\
4&(2;(0,0),(1,1),(3,2))\\
5&(2;(0,2),(1,0),(3,1))\\
6&(3;(0,0),(1,2),(2,1))\\
7&(3;(0,1),(1,0),(2,2)),
\end{array}                                                   \tag{11}
\]

the forced masks in physical columns `0,1,2` are therefore

\[
                         (m_0,m_1,m_2)=(fc,f3,cf).            \tag{12}
\]

Taking transitive closures gives the following projective classes.  A pair
`(i,c)` denotes the row `e_c^T B_ij` in the displayed physical column `j`.

\[
\begin{array}{c|ccc}
j&\multicolumn{3}{c}{\text{classes}}\\ \hline
0&\{(1,0),(2,2),(3,1)\}&
  \{(1,1),(2,0),(3,2)\}&
  \{(1,2),(2,1),(3,0)\}\\
1&\{(0,0),(2,1),(3,2)\}&
  \{(0,1),(2,2),(3,0)\}&
  \{(0,2),(2,0),(3,1)\}\\
2&\{(0,0),(1,2),(3,1)\}&
  \{(0,1),(1,0),(3,2)\}&
  \{(0,2),(1,1),(3,0)\}.
\end{array}                                                   \tag{13}
\]

Each row of (13) is a genuine projective frame: its three classes contain
the three distinct rows of the invertible block `B_3j`.  This also shows by
inspection that (12) is maximal.  Either missing triangle status would
merge two of these three anchor rows.

Take the dead left word

\[
                              a=(0,1,0,2).                    \tag{14}
\]

In right columns `0,1,2`, contract onto the respective frame classes

\[
\begin{split}
 L_0&=\{(1,1),(2,0),(3,2)\},\\
 L_1&=\{(0,2),(2,0),(3,1)\},\\
 L_2&=\{(0,1),(1,0),(3,2)\}.                                \tag{15}
\end{split}
\]

The class `L_1` can receive only left row 2 with its colour from (14), and
`L_2` can receive only row 3.  Of the remaining rows, row 0 cannot enter
column 0 because `B_00=0`; hence `L_0` receives row 1.  The unique active
permutation with signature (15) is consequently

\[
                         \pi=(3,0,1,2).                       \tag{16}
\]

The uncontracted fourth factor is
`e_0^T B_03`, which is nonzero because `B_03` is invertible.  Lemma 2.1
therefore gives `T_a != 0`, contradicting (2).  This excludes the all-zero
triple and completes the proof of Theorem 1.1.

## 6. Consequence for the exact-three frontier

The position classification had already excluded the three-star and the
two-star-plus-isolated orbits.  Theorem 1.1 now excludes the matching.
Therefore every array satisfying the dead slabs either has at least four
singular cross blocks or, in the exact-three stratum, has the path support

\[
                         (0,0),(0,1),(1,0),                   \tag{17}
\]

up to block-row and block-column permutations and transposition.  On that
path, one arm is zero, the other arm has rank at most one, and the corner
has rank at most two.  This is the sole exact-three frontier left by the
present matching analysis.  The later sparse-path and one-defect
obstructions close that path as well, so the complete exact-three stratum is
now empty.
