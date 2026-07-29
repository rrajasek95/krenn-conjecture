# The two-`K_4` dead slabs force a determinantal boundary

## 1. Result

Let the two shores be copies of `F_2^2`, with the standard ternary
one-factorization, and let

\[
                 B_{ij}\in\operatorname {Mat}_{3\times3}(\mathbb C)
                 \qquad(0\le i,j<4)
\]

be the sixteen arbitrary cross blocks.  For shore words `a,b`, put

\[
 P(a,b)=\operatorname {per}
       \bigl(B_{ij}[a_i,b_j]\bigr)_{0\le i,j<4}.       \tag{1}
\]

The sector reduction in
[`two-k4-composition-sectors.md`](two-k4-composition-sectors.md) shows that
every two-`K_4` realization must have `P(a,b)=0` whenever either shore word
is one of the thirty words containing no compatible factor edge.

**Theorem 1.1.**  There is no system of sixteen invertible cross blocks
which satisfies even the thirty left-shore dead-slab equations

\[
                         P(a,b)=0
       \qquad(a\text{ dead},\ b\in\{0,1,2\}^4).       \tag{2}
\]

Consequently every point of the full 144-parameter two-`K_4` chart lies on
the explicit determinantal boundary

\[
                         \prod_{i,j}\det B_{ij}=0.      \tag{3}
\]

No internal-edge weight, target normalization, right-shore dead equation,
or numerical genericity is used.  The exact finite audit is

```text
computations/verify_two_k4_dead_slice_determinantal_boundary.py
```

The proof has three parts: a universal four-vector syzygy reduces a dead
coordinate line to four zero `Per_3` restrictions; the rank-two geometry of
`Per_3` turns those restrictions into projective triangle incidences; and a
seven-binomial certificate excludes the only incidence pattern left by
double counting.

## 2. The eight dead coordinate lines

Identify the three colours with the three nonzero differences in `F_2^2`.
A shore word directs every vertex toward the neighbour selected by its
colour.  It is dead exactly when this fixed-point-free functional digraph
has no directed two-cycle.  The thirty dead words split as follows.

* Twenty-four are a directed triangle with one arbitrary tail.  They form
  eight full coordinate lines: for each omitted vertex `i`, the other
  three vertices may form a directed triangle in either orientation.
* The remaining six are the directed Hamilton four-cycles.

Fix one of the eight lines, with omitted vertex `i`, and denote its fixed
colours by `a_k`, `k!=i`.  Contract the four right tensor factors against
arbitrary column vectors `y_j`.  The three equations obtained by varying
`a_i` say, as one vector identity in `C^3`,

\[
       \sum_{j=0}^3 B_{ij}y_j\,C_j(y_0,\ldots,\widehat y_j,\ldots,y_3)=0,
                                                               \tag{4}
\]

where `C_j` is the three-by-three vector permanent on the other three left
rows and other three right columns.

Assume for contradiction that every `B_ij` is invertible and put

\[
 x_j=B_{ij}y_j,\qquad
 q_{kj}=e_{a_k}^{\mathsf T}B_{kj}B_{ij}^{-1}\quad(k\ne i).       \tag{5}
\]

Thus `C_j` is trilinear, misses `x_j`, and is the local image of `Per_3`
under the three maps `e_k mapsto q_kj`.

## 3. The four-vector syzygy

We use the following elementary square-free Koszul fact.

**Lemma 3.1.**  If `x_0,...,x_3` are generic vectors in a three-space and
`C_j` is trilinear of degree one in every `x_l`, `l!=j`, then

\[
                         \sum_jx_jC_j=0                \tag{6}
\]

implies

\[
 C_j=\alpha(-1)^j
       \det(x_0,\ldots,\widehat x_j,\ldots,x_3)        \tag{7}
\]

for one scalar `alpha` (with an immaterial simultaneous sign convention).

Indeed, the map from the `4*3^3=108` coefficients of the four `C_j` to
the vector-valued quadrilinear coefficients has rank 107.  The alternating
cofactor identity supplies its nonzero kernel vector, so the kernel is
exactly that line.  The checker verifies the integer rank and the generator.

In (4), `alpha` must be zero.  If it were nonzero, all three local maps in
any `C_j` would be invertible by multilinear flattening rank.  This would
make `Per_3` locally equivalent to `Det_3`.  But the first slice space of
`Per_3` is

\[
 \left\{\begin{pmatrix}0&c&b\\c&0&a\\b&a&0\end{pmatrix}:a,b,c\in\mathbb C
 \right\},                                               \tag{8}
\]

which contains an invertible matrix, whereas every matrix in the
corresponding skew-symmetric slice space of `Det_3` is singular.  Hence

\[
                              C_0=C_1=C_2=C_3=0.         \tag{9}
\]

## 4. Rank-two restrictions of `Per_3`

We next need a small classification.

**Lemma 4.1.**  Let `A_1,A_2,A_3` be three local maps, each of rank at
least two.  If

\[
                    (A_1\otimes A_2\otimes A_3)\operatorname {Per}_3=0,
                                                               \tag{10}
\]

then all three maps have rank two and kill the same coordinate basis
vector.

**Proof.**  In dual form, let `W_l` be the image plane or three-space and
write

\[
 f(x,y,z)=\sum_{\sigma\in S_3}x_{\sigma(0)}y_{\sigma(1)}z_{\sigma(2)}.
                                                               \tag{11}
\]

If one `W_l` is the full three-space, contraction by a nonzero vector in a
second factor gives a symmetric zero-diagonal matrix of rank at least two.
Its kernel has dimension at most one, so it cannot annihilate the
two-dimensional third space.

Thus all three `W_l` are planes.  For `x in W_1`, the matrix of the
bilinear contraction is

\[
 M(x)=\begin{pmatrix}0&x_2&x_1\\x_2&0&x_0\\x_1&x_0&0\end{pmatrix},
 \qquad \det M(x)=2x_0x_1x_2.                           \tag{12}
\]

Its image on `W_2` must lie in the one-dimensional annihilator of `W_3`.
Therefore `W_1` contains no vector with three nonzero coordinates.  Over
an infinite field, a plane contained in the union of the three coordinate
planes is one coordinate plane.  The same holds for all three factors.
The restriction of (11) to three coordinate planes is zero precisely when
the three missing coordinates agree (equivalently, the allowed three-by-
three bipartite graph has no perfect matching).  Dualizing gives the
claim. `QED`

Return to one directed-triangle context in (5).  Each `q_kj` is nonzero,
because both blocks in (5) are invertible.  If three of the four maps

\[
                         e_k\longmapsto q_{kj}          \tag{13}
\]

had rank at least two, (9) and Lemma 4.1 would make one of their displayed
nonzero rows vanish.  Hence at least two right columns `j` have rank one.
Right multiplication by `B_ij^{-1}` preserves row rank, so:

> For every one of the eight oriented left triangles, at least two right
> columns make its three selected rows of the blocks `B_kj` proportional.

## 5. The only projective incidence pattern

Fix a right column `j`.  It contains twelve projective row vectors, three
at each left vertex; the three at a fixed vertex are independent.  Among
the eight oriented-triangle equalities, at most four can therefore hold.
The exact `2^8` union-find check has histogram

\[
             (1,8,16,8,2)\quad\text{for }0,1,2,3,4
             \text{ simultaneous equalities}.          \tag{14}
\]

The two four-element maxima are the two orientation parities.  In either
maximum, the twelve labels split into four proportionality classes, each
class containing one oriented triangle.  Calling their projective vectors
`p_0,...,p_3`, the rows at vertex `k` use exactly the three `p_h` with
`h!=k`; invertibility says that every three of the four `p_h` are
independent.

There are at least `8*2=16` triangle-column incidences, while four columns
can carry at most `4*4=16`.  Equality holds throughout.  Every column is
one of the two parity types, every triangle occurs exactly twice, and
there are exactly two columns of each parity.  Permuting right tensor
factors, write their types as

\[
                              +,+,-,-.                  \tag{15}
\]

For nonzero scalars `s_icj`, the row `e_c^T B_ij` is therefore

\[
             e_c^{\mathsf T}B_{ij}=s_{icj}p_{\phi_\epsilon(i,c),j},
                                                               \tag{16}
\]

where the two finite maps are

\[
\begin{array}{c|ccc|ccc}
 i&\phi_+(i,0)&\phi_+(i,1)&\phi_+(i,2)
  &\phi_-(i,0)&\phi_-(i,1)&\phi_-(i,2)\\ \hline
0&3&1&2&2&3&1\\
1&2&0&3&3&2&0\\
2&1&3&0&0&1&3\\
3&0&2&1&1&0&2
\end{array}.                                             \tag{17}
\]

## 6. Seven Hamilton-slice binomials give `1=-1`

Take any of the six remaining dead words, i.e. a directed Hamilton cycle.
In a column of either parity, (17) makes its four selected rows occupy two
projective frame points, twice each.  A dual vector may select either one
of those two points.  With two columns of each parity, every nonzero such
contraction has exactly two cross perfect matchings.  Its vanishing is a
binomial in the nonzero scalars `s_icj`.

The checker constructs the 48 distinct binomials.  Seven suffice.  Write
`s_icj` compactly as `s(icj)`, and let `R_E` denote the first displayed
monomial divided by the second.  The required equations `R_E=-1` are:

\[
\begin{array}{c|c|c}
E&a&\text{numerator}\;/\;\text{denominator}\\ \hline
1&0110&s(110)s(001)s(212)s(303)\;/\;s(110)s(001)s(302)s(213)\\
2&0110&s(300)s(001)s(212)s(113)\;/\;s(110)s(211)s(302)s(003)\\
3&0110&s(300)s(001)s(112)s(213)\;/\;s(110)s(211)s(002)s(303)\\
9&0202&s(320)s(001)s(122)s(203)\;/\;s(320)s(001)s(202)s(123)\\
10&0202&s(200)s(001)s(122)s(323)\;/\;s(320)s(121)s(202)s(003)\\
11&0202&s(200)s(001)s(322)s(123)\;/\;s(320)s(121)s(002)s(203)\\
25&1122&s(220)s(011)s(112)s(323)\;/\;s(220)s(011)s(322)s(113)
\end{array}.                                             \tag{18}
\]

Their exponent vectors satisfy the exact integer relation

\[
             d_1-d_2+d_3-d_9+d_{10}-d_{11}-d_{25}=0.   \tag{19}
\]

Multiplying the corresponding Laurent equations therefore gives `1` on
the left, but

\[
             (-1)^{1-1+1-1+1-1-1}=-1                 \tag{20}
\]

on the right.  This contradiction proves Theorem 1.1.

## 7. Consequence for the full chart

The full two-`K_4` problem has not been excluded by this lemma alone: one
or more singular cross blocks remain possible, and a singular nonzero
block need not be coordinate-sparse.  What is now rigorous is that every
putative point lies on the union of the sixteen determinant hypersurfaces
(3).  Thus all dense searches and future symbolic classifications may be
restricted from the outset to a genuine rank-collapse boundary.
