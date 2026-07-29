# Binary norm equality does not select the Hamilton cell minimum

This note records a sharp obstruction to upgrading the entry-minimal binary
normal form to a norm-minimal normal form.  There is a uniform flat family
of exact binary equality sources with the same Frobenius norm as the
Hamilton source but with two additional active cells.  At six vertices,
three copies of the non-Hamilton family can coexist so that all three
principal binary restrictions are exact, balanced, and at the Hamilton
norm.  The
failure is visible only in genuinely ternary fibers.

## 1. A uniform flat family at the Hamilton norm

Let `n=2m>=4`.  On vertices `0,...,n-1`, put

\[
\begin{aligned}
 P_0&=01|23|45|67|\cdots,\\
 P_0'&=02|13|45|67|\cdots,\\
 P_1&=12|34|56|\cdots|(n-1)0.
\end{aligned}                                             \tag{1}
\]

Thus `P_0 union P_1` is the standard alternating Hamilton cycle, while
`P_0'` is obtained by switching the first two edges of `P_0`.  Fix real
numbers `c,s` with

\[
                         c^2+s^2=1.                        \tag{2}
\]

Put color-zero cells of weight `c` on `01,23`, color-zero cells of weight
`s` on `02,13`, and color-zero cells of weight one on
`45,67,...`.  Put color-one cells of weight one on `P_1`, and put every
other binary cell equal to zero.

**Proposition 1.1 (flat norm-equality family).**  The resulting source has

\[
                         H_n=e_0^{\otimes n}+e_1^{\otimes n},
 \qquad \|A\|_F^2=n.                                      \tag{3}
\]

For `cs!=0` it has exactly `n+2` nonzero scalar cells, all tensor-active,
and is not in the Hamilton cell normal form.  Nevertheless every
vertex-color port has squared incidence one and every Hermitian cofactor
gap is zero.

**Proof.**  The underlying support has exactly three perfect matchings.
Without the two chords `02,13`, the cycle has only `P_0,P_1`.  If a
matching uses `02`, vertex `1` is forced to `13`, after which the remaining
vertices use the common tail of `P_0,P_0'`; the same argument starts from
`13`.  Hence the only additional matching is `P_0'`.

The two color-zero matching products are `c^2` and `s^2`, and the sole
color-one product is one.  This proves the tensor identity in (3).  The
color-zero energy is

\[
             (m-2)+2c^2+2s^2=m,
\]

and the color-one energy is `m`, proving the norm identity.

At each of vertices `0,1,2,3`, the two incident color-zero cells have
squared magnitudes `c^2,s^2`; every other vertex has one unit color-zero
cell.  Each vertex also has one unit color-one cell.  Thus both port
incidences are one.  The constant-color cofactor vector at a switched
port has the same two entries `c,s` as the incident vector; at a tail or
color-one port both vectors have one unit entry.  All off-diagonal row
energy is zero, so the cofactor-gap identity is an equality at every port.
Every displayed cell occurs in one of the three nonzero matching terms,
which also proves tensor activity. `QED`

For a fixed support, (2) is exactly the equality case of

\[
 |a|^2+|b|^2+|c|^2+|d|^2
 \mathrel{\ge}2(|ab|+|cd|)
 \mathrel{\ge}2|ab+cd|.                                  \tag{4}
\]

Thus the non-Hamilton points are not an accidental nonoptimal weighting:
they form a continuous norm-flat arc joining the two Hamilton endpoints.
In particular, even if the still-open global binary norm bound
`||A||^2>=n` is proved, its equality classification cannot be the Hamilton
cell normal form.

## 2. A sharp six-vertex diagonal norm lemma

There is a useful positive statement at the first relevant order.

**Lemma 2.1 (three-block trace bound with a single factor).**  Suppose a
diagonal exact binary source on six vertices has one color supported on a
single perfect matching.  Then

\[
                              \|A\|_F^2\ge6.               \tag{5}
\]

**Proof.**  Write `x_e=A_e(0,0)` and `y_e=A_e(1,1)`, and suppose without
loss of generality that the all-one sector is supported on the single
matching

\[
                         P=B_1|B_2|B_3                     \tag{6}
\]

with product one.  For an edge `e in P`, color its four
complementary vertices by one and the endpoints of `e` by zero.  Diagonality
factorizes this mixed coefficient as

\[
              x_e\prod_{f\in P\setminus\{e\}}y_f=0.
\]

Every selected `y_f` is nonzero, so `x_e=0` on all three edges of `P`.
Order the two vertices inside every block and let `X_12,X_23,X_31` be the
three `2 by 2` cross-block matrices of the `x`-weights.  With

\[
                         J=\begin{pmatrix}0&1\\1&0\end{pmatrix},
\]

the eight matchings avoiding the block edges give exactly

\[
 1=\operatorname {Haf}(x)
  =\operatorname {tr}(X_{12}JX_{23}JX_{31}J).             \tag{7}
\]

Frobenius Holder and arithmetic-geometric mean imply

\[
 1\le\|X_{12}\|_F\|X_{23}\|_F\|X_{31}\|_F
 \le\left({\|x\|_2^2\over3}\right)^{3/2}.
\]

Hence `||x||_2^2>=3`.  The three nonzero `y`-weights have product one, so
ordinary arithmetic-geometric mean gives `||y||_2^2>=3`, proving (5).
`QED`

Proposition 1.1 attains (5) with `cs!=0`, so even this sharp norm bound with
a single opposite-color factor has equality cases strictly larger than the
Hamilton cell class.  Without the single-factor hypothesis, a chosen
nonzero matching monomial can cancel inside its codimension-one hafnian
cofactors; the argument above does not assert the unrestricted diagonal
bound.

Under the same single-factor hypothesis, more than three blocks give the
analogous equations that every proper union of the selected blocks has zero
complementary hafnian.  Numerical minimization of this exact scalar system gives the
sharp energy `m` through `m=6`, but the three-block trace in (7) is replaced
by a sum of Hamilton block-cycle traces.  A uniform matrix Holder bound for
that connected cycle sum remains unproved.

## 3. Three non-Hamilton binary restrictions coexist

On six vertices use the following three edge-disjoint five-edge families:

\[
\begin{array}{c|c|c}
\text{color}&\text{shared edge}&\text{two remaining pairs}\ \hline
0&01&23|45,\quad24|35\\
1&34&02|15,\quad05|12\\
2&25&03|14,\quad04|13.
\end{array}                                                \tag{8}
\]

Give every shared edge weight one and every other edge weight
`1/sqrt(2)`, always in the same-color diagonal cell.  The three supports
partition all fifteen edges of `K_6`.

**Proposition 3.1 (simultaneous pairwise norm equality).**  Each principal
two-color restriction of (8) is exactly binary equality, has squared norm
six, and neither of its color sectors is a single matching.  The full
three-color source is locally isotropic with

\[
                         R_v=I_3\quad(v=0,\ldots,5).       \tag{9}
\]

It is not ternary equality: its nine remaining perfect matchings give nine
distinct singleton colorings of type `(2,2,2)`, each with nonzero
coefficient.

**Proof.**  A direct six-vertex matching check shows that the union of any
two rows of (8) has exactly the four displayed monochromatic matchings.
Each color coefficient is `1/2+1/2=1`, proving every binary restriction.
The energy and incidence calculations are the same as in Proposition 1.1.

The six displayed monochromatic matchings account for six of the fifteen
perfect matchings of `K_6`.  Pairwise exactness forces each of the other
nine to use all three colors.  Such a matching gives two vertices of each
color.  Its coloring uniquely recovers its three edges, so no two of these
terms lie in the same coefficient fiber.  Their weights are nonzero, and
hence none can cancel. `QED`

This is a stronger compatibility warning than the three-one-factor model:
all three binary restrictions may simultaneously be exact, at the Hamilton norm,
balanced, diagonal, cofactor-gap-free, and non-Hamilton.  Binary
normalization alone therefore cannot yield the ternary contradiction; a
successful argument must retain at least one coefficient using all three
colors.

The exact audits are in
`computations/verify_binary_norm_equality_counterfamily.py`.  The discovery
probes for the full complex binary fiber and the selected-block scalar
problem are respectively `computations/search_binary_norm_general.py` and
`computations/search_hafnian_cofactor_norm.py`.
