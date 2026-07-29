# Every exact-three path block is zero

> **Superseded frontier.**  The companion obstruction
> [`two-k4-exact-three-allzero-path-obstruction.md`](two-k4-exact-three-allzero-path-obstruction.md)
> excludes the literal all-zero path as well.  The theorem below remains the
> reduction that makes that final local argument possible.

## 1. Result

Normalize the sole remaining exact-three position orbit to the path

\[
                         B_{00},B_{01},B_{10}.                 \tag{1}
\]

The corner is `B_00`.  The incidence boundary says that one arm is zero,
the other has rank at most one, and the corner has rank at most two.

**Theorem 1.1.**  Every exact-three path survivor of the left and right
dead-slab equations satisfies

\[
                         B_{00}=B_{01}=B_{10}=0.               \tag{2}
\]

The main new input is a sparse-reference version of the dead-line cofactor
collapse.  It handles the block row containing two singular blocks, which
the earlier restricted four-vector syzygy deliberately skipped.  A finite
projective audit then closes the only residual rank-one arm types.

Only actual dead four-cross equations are used.  The two-cross sector and
the live target normalizations remain available for the all-zero path (2).
The exact checker is
[`verify_two_k4_exact_three_path_zero_collapse.py`](../computations/verify_two_k4_exact_three_path_zero_collapse.py).

## 2. Sparse-reference cofactor collapse

Fix an oriented-triangle dead coordinate line with free left row `i`.
After contracting the four right factors by vectors `y_j`, its three scalar
equations combine into

\[
                 \sum_{j=0}^3 A_jy_j\,C_j
                 (y_0,\ldots,\widehat y_j,\ldots,y_3)=0,
                                                               \tag{3}
\]

where `A_j=B_ij`, and `C_j` is the complementary local `Per_3` tensor.

**Lemma 2.1.**  Let `S` be the set of nonzero maps among the `A_j`.  If
`|S|<=3` and the vectors `(A_jy_j)_(j in S)` are linearly independent on a
nonempty Zariski-open set, then

\[
                              C_j=0\qquad(j\in S).             \tag{4}
\]

**Proof.**  On that open set, (3) is a linear combination of independent
vectors, so every scalar coefficient is zero.  Each `C_j` is polynomial in
the `y` variables; vanishing on a dense open set makes it identically zero.
\(\square\)

Two instances will be used repeatedly.

1. One nonzero map of rank at least one together with two invertible maps
   has generically independent images: choose a nonzero vector in the first
   image and complete it to a basis using the two arbitrary invertible
   images.
2. Two invertible maps have generically independent images.

Thus (4) requires neither the four-vector Koszul classification nor an
invertible singular block.

## 3. A nonzero corner is impossible

Use transposition, if necessary, to put the zero arm at `B_01`.  Suppose
`B_00` is nonzero.  In reference block row 0 the maps are

\[
                 (A_0,A_1,A_2,A_3)
                 =(B_{00},0,B_{02},B_{03}),                    \tag{5}
\]

where `A_0` has rank one or two and `A_2,A_3` are invertible.  Lemma 2.1
applied to each of the two triangle orientations with hole 0 gives

\[
                              C_0=C_2=C_3=0.                   \tag{6}
\]

These are genuine complementary `Per_3` equations.  The usual conservative
translation is enough:

* a clean zero `Per_3` demands at least two rank-at-most-one factor maps;
* if a selected zero row dirties a factor while another factor is wholly
  good, it demands at least one such map.

Combine (6) with every cofactor condition already used in the exact-three
incidence audit.  The earlier two-shore rank restriction leaves four rank
patterns, written in path order `(corner, horizontal arm, vertical arm)`.
The complete exact counts are

\[
\begin{array}{c|r|r|r}
\text{rank pattern}&\text{row-matroid triples}&
 \text{old status models}&\text{models satisfying (6)}\\ \hline
(1,0,0)&6&50\,564&0\\
(1,0,1)&20&69\,370&0\\
(2,0,0)&7&6\,340&0\\
(2,0,1)&7&3\,268&0.
\end{array}                                                   \tag{7}
\]

The status domains are simultaneous projective-equivalence closures in
each physical block column; they reject every identification of two
distinct rows of one block.  The rank-two three-distinct-row type is
relaxed by forgetting its linear dependence, and the zero-`Per_3`
conditions are only necessary.  Hence the 129,542 old models form an
enlargement of all actual arrays.  Their empty intersection with (6) proves

\[
                                  B_{00}=0.                    \tag{8}
\]

## 4. A rank-one arm is impossible

Assume one arm remains nonzero.  It has rank one.  Transpose so that the
path ranks are

\[
                                  (0,1,0),                    \tag{9}
\]

with the nonzero arm at `B_01`.  Reference row 0 now has

\[
                 (A_0,A_1,A_2,A_3)
                 =(0,B_{01},B_{02},B_{03}).                   \tag{10}
\]

Lemma 2.1 gives

\[
                              C_1=C_2=C_3=0                   \tag{11}
\]

on both hole-zero triangle orientations.

The incidence audit has only three row-matroid triples of ranks `(0,1,0)`:

\[
                         (0,S1,0),\quad(0,S2,0),\quad(0,S12,0).
                                                               \tag{12}
\]

Here `Sc` or `Scd` records the coordinate-row support of the rank-one arm.
Adding (11) leaves respectively

\[
                               176,\qquad176,\qquad0           \tag{13}
\]

status models.  Every one of the remaining 352 models is contradicted by a
projective-frame singleton in an actual dead four-cross tensor, using the
contraction lemma from
[`two-k4-exact-three-matching-obstruction.md`](two-k4-exact-three-matching-obstruction.md).

Representative certificates are

\[
\begin{array}{c|c|c}
\text{type}&(m_0,m_1,m_2,m_3)&
 (\text{dead word},\text{ contracted columns},\pi)\\ \hline
(0,S1,0)&(f5,60,8a,9a)&(2001,023,2103)\\
(0,S2,0)&(fa,25,65,90)&(0102,012,2103).
\end{array}                                                   \tag{14}
\]

The complete sorted witness table has SHA-256 digest

```text
ceb25b1f89cbacaa0438b621d5f216c88f37464b0910ca599086c2c470fe2af7
```

The selected projective lines in each contracted factor are rows of a
specified invertible block.  Therefore accidental cross-block
proportionalities cannot merge the singleton signature.  Contracting the
zero tensor leaves a nonzero scalar times a nonzero fourth-factor row, a
contradiction.  Thus the remaining arm is zero, proving (2).

## 5. Exact-three frontier

The matching, star, and star-plus-isolated position orbits are already
impossible.  Theorem 1.1 reduces the entire exact-three stratum to one
literal support boundary:

\[
                    B_{00}=B_{01}=B_{10}=0,qquad
                    B_{ij}\text{ invertible otherwise}.       \tag{15}
\]

This all-zero path is not asserted to exist.  It is the unique exact-three
case that survives the present dead-slab analysis.  Its corner-row identity
has only the two invertible summands in columns 2 and 3, so Lemma 2.1 also
supplies `C_2=C_3=0` on the two hole-zero triangle lines.  A continuation
must exploit the resulting one-defect `Per_3` equations more sharply, couple
the left and right projective data, or use the two-cross and live pure
normalizations.
