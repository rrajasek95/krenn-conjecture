# Independent audit of the normalized one-hot torus quotient

The claims in commit `798bd72` are sound with two important scope labels:
the acting group is the full vertex--colour port torus (T_\Delta), not in
general the smaller local \(\prod_v\mathrm {SL}_3\) torus, and the
properness conclusion concerns the affine categorical quotient by this
torus alone.  Within that scope, transitivity, the integral one-parameter
subgroup, source polystability, equality of target quotient points, and the
failure of quotient properness alone to recover an exact source all follow.
This audit does not prove Krenn's conjecture.

## 1. Independent reconstruction

Let (G=(B,E)) be cubic with a proper three-edge-colouring

\[
                         E=P_0\sqcup P_1\sqcup P_2.
\]

Each (P_c) is automatically a perfect matching: every vertex has exactly
one incident edge of colour (c).  The sparse source coordinates are

\[
                         A_{uv}=w_{uv}e_c\otimes e_c
                         \quad(uv\in P_c),               \tag{1}
\]

with (w_{uv}\ne0), normalized by

\[
                         \prod_{uv\in P_c}w_{uv}=1.       \tag{2}
\]

The target-fixing port torus is

\[
 T_\Delta=\{(\lambda_{v,c}):
                 \prod_v\lambda_{v,c}=1\text{ for each }c\}.       \tag{3}
\]

The independent executable reconstructs the prism seed and six successive
vertex-to-triangle expansions without importing the original checker.  It
uses the larger endpoint of every edge for all gauges and cocharacters,
opposite to the endpoint convention used in `798bd72`.  It obtains the same
orders and matching counts

\[
\begin{array}{c|rrrrrrr}
|B|&6&8&10&12&14&16&18\\ \hline
\#\operatorname {PM}(G)&4&5&6&8&10&12&16.
\end{array}                                               \tag{4}
\]

All stages have an extra matching, so their all-unit output is not GHZ.

## 2. Transitivity and the orientation caveat

Orient every edge independently.  For (u\to v\) in (P_c), set

\[
                         \lambda_{u,c}=w_{uv}^{-1},
                         \qquad\lambda_{v,c}=1.           \tag{5}
\]

There is no cycle compatibility condition in (5).  The variables are
vertex--colour **ports**, and every port lies on exactly one edge of its
colour matching.  Thus (5) assigns every \(\lambda_{v,c}\) exactly once.
By (2),

\[
 \prod_v\lambda_{v,c}=\prod_{uv\in P_c}w_{uv}^{-1}=1,
\]

so (5) belongs to (T_\Delta), and

\[
              \lambda_{u,c}\lambda_{v,c}w_{uv}=1        \tag{6}
\]

on every supported coordinate.  This proves actual transitivity, over the
ground field and without taking roots.  It is stronger than a tangent-rank
calculation.

The orientation need not be coherent across colours.  Such coherence would
matter for a smaller vertex torus sharing one scalar across colours; that is
not the group (3).  Likewise, the resulting gauge need not satisfy

\[
                         \prod_c\lambda_{v,c}=1
                         \quad\text{at each }v,           \tag{7}
\]

so the all-order statement is not automatically a statement for
\(\prod_v\mathrm {SL}_3\).  The primary note consistently formulates its
new transitivity result for (T_\Delta).

For completeness, eliminate one reference port in each colour from the
cocharacter lattice of (3).  The supported edge (uv\in P_c) has restricted
character (e_{u,c}+e_{v,c}).  Exact row reduction gives

\[
 \operatorname {rank}(T_\Delta\curvearrowright (\mathbb G_m)^E)
                  =|E|-3={3|B|\over2}-3.                 \tag{8}
\]

This equals the dimension of the normalized chart (2).  The torus has
dimension (3(|B|-1)), and its stabilizer on the chart has dimension

\[
 3(|B|-1)-(|E|-3)={3|B|\over2}=|E|.                     \tag{9}
\]

Thus there is a large stabilizer, but it is not an obstruction: (5) proves
that the orbit is nevertheless the entire normalized chart.  Dimension
equality alone would not have proved this, because a finite lattice cokernel
could have left multiple orbits.

## 3. Integral one-parameter subgroup

Let \(\nu_e\in\mathbb Z\) be normalized edge exponents,

\[
                         \sum_{e\in P_c}\nu_e=0.         \tag{10}
\]

Using the orientation opposite to the primary checker, put

\[
 h_{v,c}=\nu_{uv},\qquad h_{u,c}=0
                         \quad(u\to v\in P_c).           \tag{11}
\]

Again every port is assigned once.  Equation (10) gives

\[
                         \sum_vh_{v,c}=0,                 \tag{12}
\]

so (11) is an integral cocharacter of (T_\Delta), and its weight on the
edge coordinate is

\[
                         h_{u,c}+h_{v,c}=\nu_{uv}.        \tag{13}
\]

No division by two, ramified parameter, cycle parity, or orientation choice
appears.  The independent checker verifies (10)--(13) at every stage.

If (M) is a supported perfect matching and (m(M)) its induced colour
word, then proper colouring makes the word determine (M): at each vertex,
the word selects the unique incident edge of that colour.  Hence different
matchings produce different output coordinates, and their coefficients at
the unit source are all one.  The output weight is

\[
 \sum_vh_{v,m(M)_v}=\sum_{e\in M}\nu_e.                 \tag{14}
\]

For the expansion family the three colour matchings have weight zero and
every mixed matching has positive weight.  Thus

\[
 \lim_{t\to0}h(t)H(A_*)=\Delta.                          \tag{15}
\]

The source itself has both positive and negative edge exponents, so this
particular (h(t)A_*) has no affine source limit.  Applying (h(t)^{-1})
removes all Laurent powers and returns the constant source (A_*), but its
mixed output terms then have coefficient one.

The all-order assertion is structural, not extrapolated from (4).  A
vertex-to-triangle expansion preserves proper colouring.  For each colour,
the shift added to its new external edge is cancelled by the opposite
triangle edge, so (10) persists.  A new perfect matching either uses one
external edge and the complementary triangle edge, reproducing an old
matching with unchanged weight, or it uses all three external edges.  The
chosen new shift makes every matching of the second kind positive.  This
also preserves the existence of an extra mixed matching.

## 4. Source polystability

In the character lattice of (T_\Delta), the supported weights satisfy the
strictly positive relation

\[
 \sum_{c=0}^2\sum_{uv\in P_c}(e_{u,c}+e_{v,c})
       =\sum_{v,c}e_{v,c}=0\quad\text{in }X^*(T_\Delta). \tag{16}
\]

Every supported weight occurs with coefficient one.  Therefore zero lies in
the relative interior of their convex hull: any supporting functional that
is nonnegative on all weights and zero on their positive sum must vanish on
all of them.  By the affine torus orbit criterion, (T_\Delta A_*) is
closed.  This proves polystability even though the stabilizer (9) is
positive-dimensional.

The independent checker constructs the restricted character matrix and
verifies both its rank (8) and the coefficient-one relation (16) exactly.
This is a polystability certificate in the full affine source space, not
merely in the sparse torus: orbit closure depends only on the nonzero
coordinate support of (A_*).

## 5. Source and output quotients

Let \(\pi_X,\pi_Y\) denote affine categorical quotients by (T_\Delta).
Equations (6) and (13) imply

\[
                         \pi_X(h(t)A_*)=\pi_X(A_*).       \tag{17}
\]

By (15), the closure of the output orbit contains \(\Delta\).  The tensor
\(\Delta\) is fixed by (3), so its orbit is a closed singleton.  Two points
of an affine torus representation have the same quotient point exactly when
their orbit closures meet the same closed orbit.  Consequently

\[
                         \pi_Y(H(A_*))=\pi_Y(\Delta).     \tag{18}
\]

When (G) has an extra matching, word injectivity gives

\[
                         H(A_*)\ne\Delta.                 \tag{19}
\]

Moreover, the source-quotient point \(\pi_X(A_*)\) cannot contain an exact
source.  If (H(B)=\Delta) and \(\pi_X(B)=\pi_X(A_*)\), uniqueness of the
closed orbit in an affine reductive quotient fiber and the closedness proved
above would give

\[
 A_*\in\overline{T_\Delta B}.
\]

Equivariance and continuity would then imply

\[
 H(A_*)\in\overline{T_\Delta H(B)}
          =\overline{T_\Delta\Delta}=\{\Delta\},
\]

contrary to (19).  Therefore

\[
 \pi_X\bigl(H^{-1}(\Delta)\bigr)
   \subsetneq \bar H^{-1}(\pi_Y(\Delta)),                \tag{20}
\]

where \(\bar H:X/\!/T_\Delta\to Y/\!/T_\Delta\) is the induced quotient
map; its right-hand side contains \(\pi_X(A_*)\).

This makes the properness conclusion precise.  Properness of \(\bar H\)
alone controls the larger fiber on the right of (20).  Along the Laurent
family, the punctured-disc source quotient is already the constant point
\(\pi_X(A_*)\); separatedness makes its extension the same point, and (20)
shows that this does not provide a member of the exact fiber.  The argument
does not rule out properness combined with additional source-faithful data,
a non-invariant covariant, a gauge slice, a different group, or a theorem
that separately identifies the two fibers in (20).  It rules out the
affine-(T_\Delta)-quotient properness shortcut by itself.

The discrepancy also requires an extra perfect matching.  On a properly
coloured cubic graph with exactly the three colour matchings,
\(H(A_*)=\Delta\), so (19)--(20) do not apply.  Every expansion stage in
this audit satisfies the required extra-matching hypothesis.

## 6. Executable audit

The dependency-free checker
[`audit_one_hot_torus_quotient_border_collapse_independent.py`](../computations/audit_one_hot_torus_quotient_border_collapse_independent.py)
uses no code from `798bd72`.  It independently verifies the graph and
matching ledgers, finite transitivity on unrelated rational normalized
points, the integral cocharacter, output weights and limit, character rank,
stabilizer dimension, and positive polystability relation through eighteen
vertices.  Normal, optimized, isolated, and no-site-library runs agree.  Its
combined exact ledger digest is

```text
7c2ba6d1edbc3a38c5d34f3689ca13ccc02d5630723d83d5d211a017c406df81
```
