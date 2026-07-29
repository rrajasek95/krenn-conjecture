# Six-vertex rank graph and directed coordinate anchors

This note combines two necessary conditions for a hypothetical identity

\[
H_6(A)=\Delta_{6,3}.
\]

All matrices are arbitrary asymmetric complex `3 by 3` matrices.  The two
inputs are the forced incident-edge theorem of `notes/slice-cover.md` and the
coordinate-torus-zero obstruction of `notes/determinant-split-route.md`.
The combination gives a useful finite classification near the extremal
rank pattern, but it does **not** by itself give a contradiction.  Section 5
gives exact local models witnessing that limitation.  The subsequent use of
the full coefficient-support equations in
`proofs/saturated-rank-graph-obstruction.md` rules out both saturated
`|F|=6` cases completely.

## 1. Rank-one graph, defects, and a global budget

Partition the fifteen pairs into

\[
 R=\{uv:\operatorname{rank}A_{uv}=1\},\qquad
 H=\{uv:\operatorname{rank}A_{uv}\ge2\},\qquad
 Z=\{uv:A_{uv}=0\},
\]

and put `F=H union Z`, so `R` is the complement of `F` in `K_6`.
For an edge in `R`, write

\[
 A_{uv}=a_{uv,u}\otimes a_{uv,v}.
\]

Call the incidence `(v,uv)` *coordinate* if
`a_(uv,v) in C^* e_r` for some `r`.  Call `uv` a *basis edge* if both
incidences are coordinate.  The two endpoint colors need not agree.  The
bilinear form belonging to a basis edge is nowhere zero on the coordinate
torus.

The slice-cover theorem says that, for every vertex `v`, there are three
distinct rank-one neighbors `u_0,u_1,u_2` such that the incidence at `u_r`
on `vu_r` is the coordinate line `e_r`.  In particular,

\[
 d_R(v)\ge3,\qquad d_F(v)\le2.                              \tag{1}
\]

Thus not only the rank-at-least-two graph `H`, but the larger graph formed by
the higher-rank and zero pairs together, has maximum degree two.

It is helpful to keep the asymmetry in (1).  Orient an incidence from `v`
across `vu` and call it a *defect* if the factor at the opposite endpoint
`u` is noncoordinate.  Of the `d_R(v)` outgoing incidences, at least three
are coordinate, using the three different colors.  Hence

\[
 \#\{\hbox{defects leaving }v\}\le d_R(v)-3=2-d_F(v).       \tag{2}
\]

If `f=|F|` and `D` is the total number of directed defects, summing (2)
gives

\[
 D\le\sum_v(2-d_F(v))=12-2f.                               \tag{3}
\]

Every non-basis edge of `R` consumes at least one defect.  Since
`|R|=15-f`, the number `U` of basis edges therefore satisfies

\[
 |U|\ge |R|-D\ge3+f.                                       \tag{4}
\]

Equations (1)--(4) are often more informative than merely saying that `H`
has maximum degree two.  For example, if `f=6`, there are no defects at all
and all nine rank-one matrices are basis matrices.

## 2. Four-term star cover

Here is the degree-four refinement used below.  A *retained star term* at a
vertex means an incident edge whose complementary hafnian tensor is nonzero,
so that the term really occurs in the star expansion.  In an edge-minimal
realization every nonzero incident edge is retained.

**Lemma 2.1 (four-term cover).**  Suppose exactly four star terms are
retained at a vertex `p`.  Among the three globally axial rank-one terms
forced by slice covering, at least one has a coordinate factor also at `p`.
Consequently at least one of the four incident matrices is a basis edge.

More precisely, after naming three of the contraction maps by their image
axes, they have the form

\[
 L_r(\lambda)=a_r(\lambda)e_r\quad(r=0,1,2),
 \qquad L(\lambda)=\sum_{r=0}^2 b_r(\lambda)e_r.            \tag{5}
\]

At most two of the linear forms `a_r` are noncoordinate.  If exactly two,
say `a_0,a_1`, are noncoordinate, then they are nonproportional, `a_2` is
coordinate, and, for nonzero constants `alpha,beta`,

\[
 L(\lambda)=\alpha a_1(\lambda)e_0+
             \beta a_0(\lambda)e_1.                        \tag{6}
\]

**Proof.**  For every `lambda` in the coordinate torus and every `r`, the
one-slice covering lemma says that one of the four maps in (5) is a nonzero
multiple of `e_r`.  If `a_r` is noncoordinate, its zero hyperplane meets the
coordinate torus densely.  On this intersection `L_r` vanishes, while the
two selected axial maps of the other colors cannot cover color `r`.
Therefore `L` is a nonzero `e_r`-axis vector there.  It follows that

\[
 b_s\in\mathbb C a_r\quad(s\ne r),
 \qquad b_r\notin\mathbb C a_r.                            \tag{7}
\]

If all three `a_r` were noncoordinate, (7) would first force every `b_r` to
be nonzero and then force two nonproportional `a_r` to be proportional.
(Proportional `a_r` are themselves impossible: on their common torus zero
the fourth map would have to lie nontrivially on two different axes.)  Thus
at most two are noncoordinate.

If `a_0,a_1` are the two noncoordinate forms, they are nonproportional.
Equation (7) gives `b_2 in C a_0 intersect C a_1`, hence `b_2=0`, while
`b_0` is a nonzero multiple of `a_1` and `b_1` is a nonzero multiple of
`a_0`.  This is (6).  The remaining `a_2` is coordinate, so its edge has a
coordinate factor at `p` and the factor `e_2` at the opposite endpoint.
It is a basis edge.  With zero or one noncoordinate `a_r`, at least two or
three of the selected edges are basis edges.  The same argument includes
the case in which the fourth map is globally axial. `QED`

The qualification "retained" matters: a nonzero aggregate edge whose
complementary hafnian is zero does not occur in the star identity and can be
deleted before applying the lemma.

## 3. What the torus obstruction adds to the rank graph

The following consequences are valid without any genericity assumptions.

**Lemma 3.1 (a higher-rank two-path cannot have a zero chord).**  If
`uv,vw in H`, then `uw` is nonzero.  Hence, unless `uw in H`, it belongs to
`R`.

**Proof.**  Suppose `A_uw=0`.  Because `rank(A_uv)>=2`, for a dense open set
of `y` in the coordinate torus the vector `A_uv y` has at least two nonzero
coordinates.  Otherwise the irreducible torus would map into one coordinate
axis and `A_uv` would have rank at most one.  The analogous statement holds
for the row `y^T A_vw`.  Choose `y` in the intersection of the two dense
opens.  There are coordinate-torus vectors `x,z` orthogonal to these two
vectors.  Then all three internal bilinear forms on `{u,v,w}` vanish,
contrary to the torus-zero obstruction. `QED`

For the next statements orient the matrices toward the common third vertex.
Thus, if `A_uw=a_u tensor b_w` and `A_vw=c_v tensor d_w`, the vectors
`b_w,d_w` are the factors at `w`.  Let `K_k` be the rank-two skew matrix in
`notes/determinant-split-route.md`.

**Lemma 3.2 (exceptional identities).**

1. If `uv in H` and both other edges of the triangle are rank one, then
   for some coordinate `k`,
   \[
   b_w^T K_k d_w=0.                                        \tag{8}
   \]
2. If `uv,uw in H` and `vw in R`, then for some `k`
   \[
   A_{uw}K_k d_w=0,                                        \tag{9}
   \]
   where `d_w` is the factor of `A_vw` at `w`.  In particular, if `A_uw`
   is invertible, then `d_w` is a coordinate vector.  Interchanging `u`
   and `v` gives the analogous assertion at the other endpoint of `vw`;
   if both higher-rank edges are invertible, `vw` is a basis edge.
3. A triangle contained in `H` has at most one invertible edge.  For each
   choice of a distinguished edge of rank at least two, one of the
   exceptional proportionality identities
   \[
   B K_k C^T=\mu A                                         \tag{10}
   \]
   must hold.  Thus an all-higher-rank triangle is confined to the
   all-rank-two locus or the `(3,2,2)` locus, together with these identities.

**Proof.**  Apply the algebraic alternative (10) of
`notes/determinant-split-route.md` to the distinguished rank-at-least-two
edge.  In parts 1 and 2 the left side of (10) has rank at most one, whereas
the right side has rank at least two unless `mu=0`.  Hence the product
vanishes.  Expanding rank-one factors gives (8) and (9).  If `A_uw` is
invertible, (9) says `K_k d_w=0`, whose kernel is the coordinate line
`C e_k`.  Part 3 is the rank consequence already proved in that note: two
invertible matrices and a third matrix of rank at least two are impossible.
`QED`

There is also a useful zero-edge sharpening.

**Lemma 3.3.**  In a triangle consisting of an invertible edge, a zero edge,
and a rank-one edge, the rank-one edge must be a basis edge.  A triangle
with one invertible edge and two zero edges is impossible.

**Proof.**  Let the invertible form be `x^T A y` and the rank-one form be
`(a^T x)(b^T z)`.  If `a` is noncoordinate, choose a torus point on
`a^perp` away from the finite set on which `x^T A` is supported on one
coordinate; invertibility guarantees that this exceptional set cannot fill
the projective line `a^perp`.  Then choose torus `y` orthogonal to `x^T A`.
If instead `b` is noncoordinate, first choose torus `z in b^perp`, and then
choose a generic torus `x` and a torus `y` orthogonal to `x^T A`.  In either
case all three forms vanish.  Thus both `a,b` must be coordinate.  Omitting
the rank-one form gives the final assertion. `QED`

Basis edges make the torus obstruction vacuous on every triangle containing
them.  This is the main reason the preceding constraints do not close the
six-vertex problem.

## 4. Exact classification at `|F|=6` and `|F|=5`

Because `F` has maximum degree two, `f<=6`.

### The saturated case `f=6`

Every vertex has `F`-degree two, every vertex has exactly three rank-one
neighbors, and (3) gives no defects.  Therefore all nine edges of `R` are
basis edges.  The only two possibilities for `F` are

\[
 F=C_6\quad\hbox{or}\quad F=C_3\sqcup C_3.                 \tag{11}
\]

If `F=C_6`, every three-vertex set contains a basis edge, so the torus-zero
condition imposes no additional restriction whatsoever on the six matrices
on the cycle.

If `F=C_3 union C_3`, the only triangles not already killed by a basis edge
are the two components of `F`.  Neither component may contain a zero edge:
with a zero edge it has at most two nonzero higher-rank forms, and Lemma 3.1
(or the same dense-open proof) produces a torus zero.  Thus all six edges of
`F` lie in `H`.  Each of the two triangles is independently confined by
Lemma 3.2(3): it has at most one invertible edge and satisfies the exceptional
identities (10).

### The near-saturated case `f=5`

There are at most two directed defects and hence at most two non-basis edges
in `R`.  Up to isomorphism,

\[
 F=P_6,\qquad C_3\sqcup P_3,\qquad C_4\sqcup P_2,
 \quad\hbox{or}\quad C_5\sqcup P_1.                        \tag{12}
\]

The defect allowance is supported at the two path endpoints in the first
three cases, and twice at the isolated vertex in the last case.  More
precisely, a noncoordinate factor at the head of an oriented rank-one edge
can occur only when its tail is one of these deficient vertices.

Consequently every triangle containing no basis edge is of one of the
following forms:

* a component `C_3` of `F` (only in `C_3 union P_3`);
* two consecutive `F`-edges and their one non-basis rank-one chord, with at
  least one endpoint of the two-path deficient; or
* one `F`-edge and the two non-basis rank-one edges, consuming the entire
  global defect budget.

A triangle with zero `F`-edges would require three non-basis rank-one edges
and is impossible.  The `C_3` component, when present, must consist of three
higher-rank edges and is subject to Lemma 3.2(3).  This localizes every
remaining torus-sensitive triangle in the `f=5` case.

For `f<=4`, equations (1)--(4), the four-term lemma, and Lemmas 3.1--3.3
remain exact, but the defect budget permits enough non-basis edges that no
comparably short graph-only list results.

## 5. Residual models: why these two inputs cannot suffice

The saturated cases above are genuinely nonempty as systems of necessary
conditions.

First let

\[
 F=\{01,12,23,34,45,05\}=C_6
\]

and put an arbitrary invertible matrix, say the identity, on every edge of
`F`.  Its complementary triangular prism is the union of the three perfect
matchings

\[
\begin{aligned}
 Q_0&=\{02,14,35\},\\
 Q_1&=\{03,15,24\},\\
 Q_2&=\{04,13,25\}.
\end{aligned}                                                \tag{13}
\]

Put `e_r tensor e_r` on the three edges of `Q_r`.  Every vertex sees the
three coordinate colors on its rank-one neighbors, the higher-rank graph is
a six-cycle, and every triangle contains a basis edge.  Thus both universal
constraints, including all their rank consequences above, hold.  This does
not assert the matching-tensor identity; it proves that the two constraints
alone cannot yield a contradiction.

There is an equally explicit `C_3 union C_3` model.  Put properly
three-edge-colored basis matrices on the complementary `K_(3,3)`.  On each
internal triangle, with variables `x,y,z`, use the three rank-two forms

\[
 x_0y_2-x_2y_0,\qquad x_0z_2-x_2z_0,
 \qquad y_0z_2-2y_2z_0.                                   \tag{14}
\]

They have no common coordinate-torus zero: the first two equations equate
the three nonzero ratios, while the third says one of them is twice itself.
Every other triangle contains a basis edge.  Hence the exceptional
all-rank-two residual locus in (11) is also nonempty.

These examples satisfy only the two local necessary conditions, not the
matching-tensor identity.  The full coefficient-support audit in
`proofs/saturated-rank-graph-obstruction.md` supplies the missing global
information and proves that neither saturated pattern can occur in an exact
realization.  Thus every remaining putative solution has `|F|<=5`.
