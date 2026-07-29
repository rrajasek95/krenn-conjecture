# The `3+3` contraction and the vector-permanent obstruction

This note records a completely general necessary condition for a putative
six-vertex, three-color identity

\[
 H_6(A)=\Delta_{6,3}=\sum_{c=0}^2 e_c^{\otimes 6}.
\]

All edge tensors `A_uv` below are arbitrary complex `3 x 3` matrices.  In
particular, nothing here assumes same colors at the two endpoints, symmetry,
rank one, or absence of parallel-source cancellation.

## 1. Contracting one side of a `3+3` split

Split the vertices as `L={1,2,3}` and `R={4,5,6}`.  Choose covectors
`x_i in V_i^*` for `i in L`, and set

\[
 s_{ij}=\langle x_i\otimes x_j,A_{ij}\rangle,
 \qquad
 v_{ia}=(x_i\otimes\operatorname{id})A_{ia}\in V_a
 \quad(i\in L,\ a\in R).
\]

Every perfect matching either consists of three cross edges, or consists of
one edge internal to `L`, one edge internal to `R`, and one cross edge.
Consequently contraction at the three vertices in `L` gives

\[
 \sum_{\pi:L\mathbin{\simto}R}\ \bigotimes_{a\in R}
 v_{\pi^{-1}(a),a}
 +\sum_{\{i,j,k\}=L}\ \sum_{a\in R}
 s_{ij}\,v_{ka}\otimes A_{R\setminus\{a\}}.               \tag{1}
\]

Here `A_{R\setminus{a}}` is the tensor on the other two right vertices, all
factors are put back in vertex order, and the first sum runs over the six
bijections from `L` to `R`.  On the target side the same contraction is

\[
 D_x=\sum_{c=0}^2\lambda_c e_c\otimes e_c\otimes e_c,
 \qquad \lambda_c=\prod_{i\in L}x_i(e_c).                    \tag{2}
\]

Thus, if all coordinates of the three `x_i` are nonzero and

\[
 s_{12}=s_{13}=s_{23}=0,                                    \tag{3}
\]

then (1) would say that a `3 x 3` vector permanent equals a GHZ tensor with
three nonzero coefficients.

## 2. A vector permanent is never a three-term GHZ tensor

**Lemma (vector-permanent obstruction).**  Let `v_ia in W_a`, where both
`i` and `a` range over three-element sets and `dim W_a=3`.  Then

\[
 P=\sum_{\sigma\in S_3}
 v_{\sigma(1),1}\otimes v_{\sigma(2),2}\otimes
 v_{\sigma(3),3}                                             \tag{4}
\]

cannot equal a diagonal tensor

\[
 \lambda_1p_1\otimes q_1\otimes r_1+
 \lambda_2p_2\otimes q_2\otimes r_2+
 \lambda_3p_3\otimes q_3\otimes r_3                         \tag{5}
\]

when every `lambda_i` is nonzero and each of the three displayed triples of
vectors is a basis.

**Proof.**  Tensor (5) has flattening rank three in every factor.  Since the
first-factor image of (4) is contained in
`span(v_11,v_21,v_31)`, and cyclically, equality would force each of these
three vector triples to be a basis.  Apply their inverse basis changes.
Then (4) becomes the standard permanent tensor

\[
 \operatorname{Per}_3=\sum_{\sigma\in S_3}
 e_{\sigma(1)}\otimes e_{\sigma(2)}\otimes e_{\sigma(3)}.
\]

Its first-factor slice space consists of the matrices

\[
 \begin{pmatrix}
 0&c&b\\ c&0&a\\ b&a&0
 \end{pmatrix}.                                               \tag{6}
\]

No nonzero matrix in (6) has rank one: its three principal `2 x 2` minors
are `-c^2,-b^2,-a^2`.  In contrast, the first-factor slice space of (5)
contains three nonzero rank-one matrices.  Independent invertible changes in
the three tensor factors preserve matrix rank throughout a slice space, a
contradiction. `QED`

The determinant cubic by itself does **not** distinguish the two tensors.
For (6) it is `2abc`, while for the diagonal GHZ pencil it is `abc`, and a
coordinate rescaling removes the factor two.  The needed invariant is the
rank stratification at the three vertices of that cubic: rank two for (6),
rank one for the diagonal pencil.

Combining the lemma with (1)--(3) gives:

**Corollary (torus-zero obstruction).**  In any putative identity
`H_6(A)=Delta_6,3`, and for every three-vertex set `L`, the equations

\[
 x_i^T A_{ij}x_j=0\qquad(ij\in\binom L2)                     \tag{7}
\]

have no simultaneous solution in which all nine coordinates of the three
covectors are nonzero.

## 3. Invertible internal matrices always have a torus zero

The preceding necessary condition has a useful concrete consequence.

**Lemma (three invertible bilinear forms).**  If `A,B,C` are invertible
`3 x 3` complex matrices, there exist projective vectors
`x,y,z in P^2`, all of whose coordinates are nonzero, such that

\[
 x^TAy=x^TBz=y^TCz=0.                                       \tag{8}
\]

**Proof.**  The hypersurface

\[
 X=\{(x,y)\in\mathbb P^2\times\mathbb P^2:x^TAy=0\}
\]

is irreducible, because a bilinear form factors only when its matrix has
rank one.  For `(x,y) in X`, put `r=x^TB` and `s=y^TC`.  A vector spanning
the common kernel of the two rows `r,s` is their cross product.  Its `k`th
coordinate is a bilinear polynomial

\[
 g_k(x,y)=x^T B K_k C^T y,                                   \tag{9}
\]

where `K_k` is the nonzero rank-two skew matrix selecting the complementary
`2 x 2` minor.

No `g_k` vanishes identically on `X`.  Indeed, since `X` is the irreducible
hypersurface cut out by `f=x^TAy`, such vanishing would imply `g_k` is a
scalar multiple of `f` (both have bidegree `(1,1)`).  But the coefficient
matrix `BK_kC^T` has rank two, whereas a nonzero scalar multiple of `A` has
rank three; the zero scalar is impossible as well.

Hence each condition `g_k != 0` defines a nonempty Zariski-open subset of
the irreducible variety `X`.  The conditions that every coordinate of `x`
and `y` be nonzero are also nonempty opens there.  Their finite intersection
is nonempty.  At a point of that intersection, take `z=r cross s`.  All
coordinates of `z` are the nonzero `g_k`, and (8) follows. `QED`

The proof gives a more general algebraic alternative that remains useful
when some matrices are singular.  Assume only `rank(A)>=2`, so that `X`
is still irreducible.  If the three equations in (8) have no
full-coordinate solution, then for at least one `k`

\[
                 B K_k C^T=\mu A.                            \tag{10}
\]

Indeed, otherwise all three `g_k` define nonempty open subsets of `X`;
intersecting them with the six coordinate-torus opens gives exactly the
solution constructed above.  Thus absence of a torus zero forces one
cross-product coordinate to vanish identically on `X`, which is (10).
This implication is only one-way, because where `r` and `s` are dependent
their common kernel is two-dimensional.

**Proposition (invertible-edge graph is triangle-free).**  If
`H_6(A)=Delta_6,3`, the graph on the six vertices whose edges are those
`uv` for which `A_uv` is invertible contains no triangle.  In particular it
has at most nine edges.

**Proof.**  If a triangle existed, apply the preceding lemma to its three
edge matrices.  The resulting full-support covectors satisfy (3), so the
`3+3` contraction would equate a vector permanent with a three-term GHZ
tensor, contrary to the vector-permanent lemma.  Triangle-freeness follows,
and the numerical bound is Mantel's elementary bound for a triangle-free
graph on six vertices. `QED`

There is a stronger rank consequence.  Applied to any ordered triangle in a
putative solution, (10) says that whenever one edge matrix `A` has rank at
least two, some `B K_k C^T` is proportional to it.  If `rank(A)=3`, the
scalar must be zero, since `K_k` has rank two.  Sylvester's rank inequality
then gives

\[
 0=\operatorname{rank}(BK_kC^T)
 \quad\Longrightarrow\quad
 \operatorname{rank}(B)+\operatorname{rank}(C)\le4.          \tag{11}
\]

In particular, a triangle cannot have edge-rank pattern `(3,3,r)` with
`r>=2`.  More generally, if a triangle has one invertible edge and all
three edges have rank at least two, its other two edges must both have rank
exactly two and obey an exceptional identity (10).

This rules out, for example, every putative solution in which all fifteen
aggregate edge matrices are nonsingular.  It also shows exactly where the
method stops: singular internal matrices need not admit a common torus zero.

## 4. Exact counterexample to unconditional torus killing

It is false even for three rank-two bilinear forms that they always have a
common zero in the coordinate torus.  With coordinates `x,y,z in (C*)^3`,
take

\[
 f_{12}=x_1y_3-x_3y_1,
 \qquad f_{13}=x_1z_3-x_3z_1,
 \qquad f_{23}=y_1z_3-2y_3z_1.                               \tag{12}
\]

Every displayed coefficient matrix has rank two.  In the torus, the first
two equations say

\[
 x_1/x_3=y_1/y_3=z_1/z_3,
\]

while the third says `y_1/y_3=2z_1/z_3`.  Their common nonzero value would
equal twice itself, an impossibility.  Thus (12) is an exact local
counterexample to extending the invertible-matrix lemma merely to rank at
least two.  (It is not asserted that these three matrices extend to a
solution of the full hafnian identity.)
