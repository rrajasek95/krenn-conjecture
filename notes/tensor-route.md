# Tensor / multilinear-algebra route

## Outcome of this round

The tensor route gives a completely general proof of the upper bound at four
vertices and several exact necessary identities at arbitrary even order.  Its
most informative negative result is that, for every even `n >= 6`, the
forbidden tensor `Delta_{n,3}` lies in the Zariski (and ordinary Euclidean)
closure of the matching-tensor image, even if every nonzero edge tensor is
rank one and has the same color at its two ends.  Consequently no polynomial
identity in the *output tensor alone* can separate `Delta_{n,3}` from all
hafnian matching tensors.  An affirmative proof must use a non-closed-image
argument, a rational invariant on a carefully justified nonvanishing chart,
or a rigidity theorem that controls unbounded edge parameters.

The closure statement is proved explicitly in Section 6.  It exactly matches
the numerically observed triangular-prism degeneration and extends it to all
even orders.

Throughout, `V_v` is a copy of the color space `V = C^q`, with distinguished
basis `e_1,...,e_q`.

## 1. Exact aggregation and the hafnian tensor

Fix an order on the vertices.  For each pair `u < v`, aggregate all parallel
sources on that pair into

\[
 A_{uv}:=\sum_{a:N(a)=\{u,v\}} w(a)
 e_{k(a,u)}^{(u)}\otimes e_{k(a,v)}^{(v)}
 \in V_u\otimes V_v.                                           \tag{1}
\]

This loses no information relevant to the matching tensor: after a perfect
matching is fixed, choices among parallel sources on its distinct pairs are
independent, so distributivity replaces the sum of products by the product of
the aggregate tensors (1).  Endpoint order is retained, and `A_uv` is an
arbitrary matrix; it need not be symmetric or rank one.

For an even vertex set `S`, define

\[
 H_S(A):=\sum_{M\in\operatorname{PM}(S)}
          \bigotimes_{uv\in M} A_{uv},\qquad H_\varnothing:=1.  \tag{2}
\]

Canonical reordering places the factors in vertex order.  The coefficient of
`tensor_{v in S} e_{c(v)}^(v)` in (2) is exactly the weighted sum of
`c`-consistent matchings.  Thus monochromaticity is precisely

\[
 H_S(A)=\Delta_{S,q}:=\sum_{r=1}^q e_r^{\otimes S}.             \tag{3}
\]

All statements below are about arbitrary matrices `A_uv`, so parallel
sources, asymmetric endpoint colors, and complex cancellation are already
included.

## 2. Partition rank: a general bound and the complete `n=4` upper bound

The following standard lemma is short enough to prove here.

**Diagonal partition-rank lemma.**  If `d >= 2` and

\[
 F(x_1,\ldots,x_d)=\sum_{a\in D}c_a
 \delta_a(x_1)\cdots\delta_a(x_d),\qquad c_a\ne0,
\]

then the unrestricted partition rank of `F` is `|D|` over `C`.

**Proof.**  The displayed sum proves the upper bound.  For the lower bound,
induct on `d`; `d=2` is ordinary matrix rank.  Suppose

\[
 F=\sum_{i=1}^r f_i(x_{S_i})g_i(x_{T_i}),\qquad r<|D|,          \tag{4}
\]

where `S_i,T_i` are nonempty complements.  Swap factors so that
`|S_i| <= d/2`.  If no `S_i` is a singleton, sum (4) over any one
coordinate.  Both factors of every surviving term still contain a variable,
whereas the left side is the same diagonal tensor in `d-1` variables.  This
contradicts induction.

Otherwise choose `j` such that `S_i={j}` for some terms, let `U` be their
index set, and put `u=|U|`.  In the space of functions on the common index
set `X`, take

\[
 W=\{h:\ \sum_x h(x)f_i(x)=0\text{ for all }i\in U\}.
\]

Then `dim W >= |X|-u`.  A vector in `W` of maximal support has support at
least `dim W` (otherwise a nonzero vector in the kernel of restriction to
that support enlarges it).  Contract coordinate `j` against such a vector.
The `u` singleton terms vanish and all other surviving terms remain
partition-rank one.  The result therefore has partition rank at most `r-u`.
But it is a diagonal `(d-1)`-tensor with at least `|D|-u` nonzero entries, so
induction gives `|D|-u <= r-u`, contrary to `r<|D|`.  QED.

Expanding (2) by the partner of a fixed vertex `p` gives

\[
 H_S(A)=\sum_{j\in S\setminus\{p\}}
 A_{pj}\otimes H_{S\setminus\{p,j\}}(A).                      \tag{5}
\]

Every nonzero term has partition rank one across
`{p,j} | S\{p,j}`.  Hence (3) and the lemma imply

\[
 q\le d_p^*:=\#\{j:\ A_{pj}\ne0,
 H_{S\setminus\{p,j\}}(A)\ne0\}\le |S|-1.                  \tag{6}
\]

For four vertices, (2) is the sum of exactly the three pairing tensors

\[
 A_{12}\otimes A_{34}+A_{13}\otimes A_{24}
 +A_{14}\otimes A_{23},                                      \tag{7}
\]

so (6) proves `q <= 3` for completely arbitrary complex edge matrices.  This
settles the substantive `n=4` upper bound without a same-color, positivity,
or simplicity assumption.

### A contracted Hall-type strengthening

Let `J_p` be the active-neighbor set in (6), and define the linear map

\[
 L_{pj}:V_p^*\longrightarrow V_j,qquad
 L_{pj}(\lambda)=(\lambda\otimes\mathrm{id})A_{pj}.            \tag{8}
\]

Contract (5) at `p` by an arbitrary `lambda`.  Its right side is a sum of
at most

\[
 N_p(\lambda)=\#\{j\in J_p:L_{pj}(\lambda)\ne0\}
\]

slice-rank-one tensors, while its left side under (3) is

\[
 \sum_r\lambda(e_r)e_r^{\otimes(S\setminus\{p\})}.
\]

The diagonal lemma therefore gives the exact necessary inequality

\[
 |\operatorname{supp}(\lambda)|\le N_p(\lambda)
 \quad\text{for every }\lambda\in V_p^*.                      \tag{9}
\]

In particular, for every `K subset J_p`,

\[
 \dim\bigcap_{j\in K}\ker L_{pj}\le |J_p|-|K|.               \tag{10}
\]

Indeed a `d`-dimensional subspace of `C^q` contains a vector with at least
`d` nonzero coordinates; apply (9) to such a vector in the intersection.
When `|J_p|=q`, (10) says that every `k` selected incident edge maps have
joint rank at least `k`, and all `q` have trivial common kernel.  This is
strictly stronger than merely requiring `q` active neighbors, although it
does not exclude three full-rank incident matrices.

## 3. All scalar combinations of star expansions

For arbitrary scalars `alpha_v` with `sum_v alpha_v=1`, every perfect
matching uses every vertex once, so

\[
 H_S(A)=\sum_{u<v}(\alpha_u+\alpha_v)
 A_{uv}\otimes H_{S\setminus\{u,v\}}(A).                      \tag{11}
\]

Consequently, if `G_*` is the graph of active pairs from (6),

\[
 q\le \min_{\sum_v\alpha_v=1}
 \#\{uv\in E(G_*):\alpha_u+\alpha_v\ne0\}.                  \tag{12}
\]

This exhausts every universal scalar edge-deletion identity.  Indeed, if
numbers `beta_uv` satisfy `sum_{uv in M} beta_uv=1` for every perfect
matching of the complete graph, comparison of matchings that agree off four
vertices yields

\[
 \beta_{ij}+\beta_{k\ell}=\beta_{ik}+\beta_{j\ell}
 =\beta_{i\ell}+\beta_{jk}.                                  \tag{13}
\]

The four-point relations imply `beta_ij=alpha_i+alpha_j`; the matching sum
then gives `sum alpha_i=1`.  Thus further scalar averaging of star
expansions cannot improve (12).

One useful structural consequence is that every bipartite connected
component of `G_*` is balanced.  If a component had sides of unequal sizes,
put opposite constants on its two sides and zero on all other components,
then rescale to make `sum alpha=1`.  Every active coefficient in (11) would
vanish, falsely giving `H_S=0`.

The limitation is sharp in the critical six-vertex case.  For balanced
`K_{3,3}`, the minimum in (12) is exactly `3`: a one-vertex star attains
three, while deleting only one or two edges leaves a connected balanced
bipartite zero-edge graph, whose equations `alpha_u+alpha_v=0` force total
sum zero.  The triangular prism likewise attains three.  Hence this whole
family of partition-rank identities cannot rule out `q=3,n=6`.

## 4. Exact two-site cap and exterior identity

Fix distinct `p,q`, put `R=S\setminus\{p,q\}`, and let
`C in V_p^* tensor V_q^*`.  Define

\[
 s_C=\langle C,A_{pq}\rangle
\]

and, for distinct `i,j in R`,

\[
 B^C_{ij}=\operatorname{contr}_{p,q}^{C}
 (A_{pi}\otimes A_{qj}+A_{pj}\otimes A_{qi})
 \in V_i\otimes V_j.                                         \tag{14}
\]

Splitting a matching according as it contains `pq` or sends `p,q` to two
different vertices proves

\[
 \operatorname{contr}_{p,q}^{C}H_S(A)
 =s_C H_R(A)+D H_R(A)[B^C],                                   \tag{15}
\]

where

\[
 D H_R(A)[B]=\sum_{M\in\operatorname{PM}(R)}\sum_{ij\in M}
 B_{ij}\otimes\bigotimes_{e\in M\setminus\{ij\}}A_e.       \tag{16}
\]

Under (3), this becomes

\[
 s_C H_R(A)+D H_R(A)[B^C]
 =\sum_{r=1}^q C(e_r,e_r)e_r^{\otimes R}.                     \tag{17}
\]

For `|R|>=2`, the kernel of the cap map is therefore *exactly* the
`q^2-q` dimensional space of bilinear covectors with zero diagonal.  In
particular every alternating `C` gives the syzygy

\[
 s_C H_R(A)+D H_R(A)[B^C]=0.                                  \tag{18}
\]

The derivative term is unavoidable: capping two vertices does not generally
produce a scalar multiple of the smaller matching tensor.  Also `s_C` need
not vanish for alternating `C`, since `A_pq` may be asymmetric.  The exact
signed example in `notes/small-tensor-findings.md` has `s_C H_R` and the
derivative term both nonzero and cancelling.  Thus neither deletion
induction nor an argument that kills antisymmetric parts term by term is
valid.

## 5. A cancellation example that defeats termwise support

For reference, there is an integer-weight realization of `Delta_{6,2}` with
only the following nonzero aggregate tensors:

\[
\begin{array}{c|c}
12&(e_1+e_2)\otimes e_1\\
34,56,24&e_1\otimes e_1\\
13&-e_2\otimes e_1\\
16,23,45&e_2\otimes e_2.
\end{array}
\]

Its support graph has precisely the perfect matchings

\[
 12|34|56,\qquad 13|24|56,\qquad 16|23|45.
\]

Their tensors are respectively

\[
 e_1^{\otimes6}+e_2\otimes e_1^{\otimes5},\quad
 -e_2\otimes e_1^{\otimes5},\quad e_2^{\otimes6}.
\]

They sum exactly to `Delta_{6,2}`.  Hence a mixed coefficient may have two
nonzero integer contributions that cancel, and a bichromatic edge cannot be
deleted merely because the final tensor has diagonal support.  The script
`computations/verify_cancellation_example.py` checks all 64 coefficients.

## 6. Exact border degeneration of `Delta_{n,3}` for every even `n >= 6`

### Six vertices: the triangular prism

On vertices `1,...,6`, take the three edge-disjoint perfect matchings

\[
\begin{aligned}
P_1&=\{14,23,56\},\\
P_2&=\{25,13,46\},\\
P_3&=\{36,12,45\}.
\end{aligned}                                                  \tag{19}
\]

Their union is the triangular prism.  It has exactly one further perfect
matching,

\[
 P_0=\{14,25,36\}.                                             \tag{20}
\]

Color every edge of `P_r` by `r` at both ends and attach a scalar weight.
For `t != 0`, use

\[
 w_{14}=t,\qquad w_{23}=t^{-1},
\]

and give every other edge weight `1`.  Every nonzero aggregate edge tensor
is therefore

\[
 A_{uv}(t)=w_{uv}(t)e_{c(uv)}\otimes e_{c(uv)}.                \tag{21}
\]

The three matchings (19) have products `1`, while (20) has product `t`.
Since there are no other perfect matchings, one has the exact Laurent-family
identity

\[
 H_6(A(t))=\Delta_{6,3}
 +t\,e_1\otimes e_2\otimes e_3\otimes e_1\otimes e_2\otimes e_3. \tag{22}
\]

Thus `Delta_{6,3}` is an ordinary limit of matching tensors, although one
edge parameter diverges.

### Vertex-to-triangle expansion

The construction extends by two vertices at a time.  Suppose `G` is a cubic
graph with a proper three-edge-coloring; its three color classes are perfect
matchings.  Give every edge an integer valuation `nu(e)` and put
`A_e(t)=t^{nu(e)}e_{c(e)} tensor e_{c(e)}`.  Assume the three color-class
matchings have valuation zero and every other perfect matching has strictly
positive valuation.

Choose a vertex `v`, whose incident edge of color `i` is `e_i=vu_i`.
Replace `v` by a triangle on new vertices `t_1,t_2,t_3`: attach `u_i` to
`t_i` by a color-`i` edge `e_i'`, and color the internal edge `t_jt_k` by
the missing color `i`.  Pick integers `a_i` and set

\[
 \nu(e_i')=\nu(e_i)+a_i,\qquad
 \nu(t_jt_k)=-a_i.                                            \tag{23}
\]

A perfect matching of the expanded graph uses either exactly one or all
three external edges `u_it_i`:

* In the one-external case, if it uses `e_i'`, it must also use the opposite
  internal edge `t_jt_k`.  Contracting the triangle gives a unique old
  perfect matching containing `e_i`, and (23) preserves its valuation.
* In the three-external case, it uses no internal triangle edge.  Its
  valuation is shifted by `a_1+a_2+a_3`.

There are finitely many matchings of the second kind, so choose (for example)
`a_1=a_2=0` and `a_3=L` with `L` large enough that all of them have valuation
at least one.  The three extended color classes still have valuation zero,
and all other matchings have positive valuation.  The proper edge coloring
is preserved.  This operation adds exactly two vertices, so induction from
the prism proves:

**Border theorem.**  For every even `n >= 6`, there is a Laurent family of
rank-one, same-color edge tensors `A^(n)(t)` such that

\[
 H_n(A^{(n)}(t))=\Delta_{n,3}+\sum_{k\ge1}t^k T_k             \tag{24}
\]

for fixed tensors `T_k`; in particular the right side tends to
`Delta_{n,3}` as `t -> 0`.

To check the constant term in (24), every color class contributes its
constant-color basis tensor with coefficient one.  It is the only matching
using solely that color because a color class already contains the unique
color-`r` edge incident to every vertex.  Every other matching uses at least
two colors and has positive valuation, so it contributes only a positive
power of `t` to a nonconstant coloring.

Since the parameter-to-output map is polynomial in all edge entries, (24)
places `Delta_{n,3}` in its Zariski closure as well.  Equivalently, any
polynomial in output coefficients that vanishes for every matching tensor
also vanishes at `Delta_{n,3}`: substitute the Laurent family, obtain an
identity for all `t != 0`, and take its constant term.  Therefore a
representation-theoretic or flattening strategy based solely on polynomial
equations cutting out the image closure cannot prove the desired `q <= 2`.

### Exact rigidity on the finite prism chart, with arbitrary edge matrices

The limit cannot be attained with finite edge tensors on the same nine-edge
support, even when all nine matrices are arbitrary.  We first need a small
equality-case lemma for three slice terms.

**Three-slice center lemma.**  Let `X,Y,Z` contain linearly independent
triples `d_i^X,d_i^Y,d_i^Z` for `i=1,2,3`, and put

\[
 D=\sum_{i=1}^3d_i^X\otimes d_i^Y\otimes d_i^Z.
\]

If

\[
 D=x\otimes P+y\otimes Q+z\otimes R,                          \tag{25a}
\]

where the displayed singleton factors lie in `X,Y,Z`, respectively, and the
other factors are arbitrary tensors on the complementary two spaces, then,
up to a permutation of `1,2,3`,

\[
 x\in\mathbb C^*d_1^X,\qquad
 y\in\mathbb C^*d_2^Y,\qquad
 z\in\mathbb C^*d_3^Z.                                       \tag{25b}
\]

**Proof.**  For a nonzero `x`, let

\[
 U_x=\{(\alpha(d_1^X),\alpha(d_2^X),\alpha(d_3^X)):
             \alpha(x)=0\}\subseteq\mathbb C^3,
\]

and define `U_y,U_z` similarly.  Each has dimension at least two.  It has
dimension two exactly when `x` lies in the span of the three `d_i^X`; if
`x` has a component outside that span, arbitrary prescribed values on the
three `d_i^X` can be extended and then adjusted on that outside component to
annihilate `x`, so `U_x=C^3`.

Contracting (25a) against covectors annihilating `x,y,z` gives

\[
 \sum_i u_i v_i w_i=0
 \quad(u\in U_x,v\in U_y,w\in U_z).
\]

Thus the span of all coordinatewise products `u odot v` is contained in
`U_z^perp`, which has dimension at most one.  We use the following elementary
classification.  If `U,V subset C^3` both have dimension at least two and
`span(U odot V)` has dimension at most one, then `U=\{u:u_r=0\}` and
`V=\{v:v_s=0\}` for distinct coordinates `r,s`.  Indeed, if `U` contained a
vector with all three entries nonzero, coordinatewise multiplication by it
would map `V` isomorphically to a space of dimension at least two.  Hence
every vector of `U` lies in one of the three coordinate hyperplanes.  Over
the infinite field `C`, a vector space contained in a finite union of proper
subspaces lies in one of them; dimension at least two then makes `U` equal
that hyperplane.  The same holds for `V`.  The two missing coordinates must
be distinct, since the coordinatewise square/product of one coordinate
hyperplane spans the other two axes.

Apply this classification to `U_x,U_y`.  They are distinct coordinate
hyperplanes, and their products span the remaining coordinate axis, say the
third.  Orthogonality then forces `U_z` to be the hyperplane missing that
third coordinate.  In particular all three `U` spaces have dimension two,
so `x,y,z` lie in the respective diagonal spans; their annihilator
hyperplanes identify them with three distinct diagonal axes.  This proves
(25b).  QED.

Now group the prism vertices into

\[
 X=V_1\otimes V_4,\qquad
 Y=V_2\otimes V_5,\qquad
 Z=V_3\otimes V_6,
\]

and write `d_i^X=e_i tensor e_i`, and similarly in `Y,Z`.  Set

\[
 x=A_{14},\qquad y=A_{25},\qquad z=A_{36}.
\]

After canonical reordering, the products on the three pairs of horizontal
edges give tensors

\[
 U=\mathcal R(A_{23}\otimes A_{56})\in Y\otimes Z,\quad
 V=\mathcal R(A_{13}\otimes A_{46})\in X\otimes Z,\quad
 W=\mathcal R(A_{12}\otimes A_{45})\in X\otimes Y,            \tag{25c}
\]

where `mathcal R` merely groups the two endpoints in the same superparty.
The full prism tensor is exactly

\[
 H_6=x\otimes U+y\otimes V+z\otimes W+x\otimes y\otimes z
    =x\otimes(U+y\otimes z)+y\otimes V+z\otimes W.            \tag{25d}
\]

If one of `x,y,z` were zero, (25d) would have partition rank at most two,
whereas grouped `Delta_{6,3}` has partition rank three.  Hence all are
nonzero.  If (25d) equaled `Delta_{6,3}`, the center lemma would permit a
simultaneous color permutation and nonzero scalars `a,b,c` such that

\[
 x=a d_1^X,\qquad y=b d_2^Y,\qquad z=c d_3^Z.                 \tag{25e}
\]

Let `pi_Y` quotient `Y` by `C d_2^Y` and let `pi_Z` quotient `Z` by
`C d_3^Z`.  Apply `id_X tensor pi_Y tensor pi_Z` to (25d).  The `y`-slice,
the `z`-slice, the vertical term, and the `i=2,3` target summands vanish.
The result is

\[
 (\pi_Y\otimes\pi_Z)U
 =a^{-1}\,\overline d_1^Y\otimes\overline d_1^Z.
\]

Equivalently,

\[
 U\in a^{-1}d_1^Y\otimes d_1^Z
       +(\mathbb C d_2^Y)\otimes Z+Y\otimes(\mathbb C d_3^Z). \tag{25f}
\]

The special crossed-edge product in (25c) now makes (25f) rigid.  In
coordinates,

\[
 U_{(r_2,r_5),(r_3,r_6)}
 =(A_{23})_{r_2,r_3}(A_{56})_{r_5,r_6}.                       \tag{25g}
\]

Its `(d_1^Y,d_1^Z)` coefficient is `a^{-1} != 0`, so both
`(A_23)_{1,1}` and `(A_56)_{1,1}` are nonzero.  If
`(A_23)_{r,s}` were any other nonzero entry, multiplying it by
`(A_56)_{1,1}` would give in (25g) the coordinate

\[
 ((r,1),(s,1)).
\]

This is neither the anchor `((1,1),(1,1))`, nor on the hyperplane
`Y=d_2^Y` (its second component is `1`), nor on the hyperplane
`Z=d_3^Z` (again its second component is `1`).  It is forbidden by (25f).
Thus `A_23` is supported only at `(1,1)`.  Reversing the roles and using its
nonzero anchor shows the same for `A_56`.  Therefore

\[
 U=a^{-1}d_1^Y\otimes d_1^Z.                                 \tag{25h}
\]

The two analogous quotient arguments and the same rectangular-support test
give

\[
 V=b^{-1}d_2^X\otimes d_2^Z,
 \qquad W=c^{-1}d_3^X\otimes d_3^Y.                           \tag{25i}
\]

Substitution in (25d) produces the three desired diagonal summands *plus*

\[
 abc\,d_1^X\otimes d_2^Y\otimes d_3^Z,
\]

whose coefficient is nonzero.  It cannot equal `Delta_{6,3}`.  We have
proved:

**Arbitrary-matrix prism theorem.**  If all aggregate tensors outside the
nine triangular-prism edges are zero, no choice of the nine arbitrary
`3 by 3` complex edge matrices realizes `Delta_{6,3}`.

The proof is cancellation-safe: the matrices in (25c) may have arbitrary
rank and arbitrary asymmetric endpoint colors.  It is the Cartesian-product
form (25g), not termwise positivity, that forces the horizontal matrices onto
their diagonal anchors.

### A shorter rank-one proof on the same chart

The limit cannot be attained with finite rank-one edge tensors on the same
support, even if those edge tensors are arbitrary and asymmetric rather than
same-color basis tensors.

**Prism rank-one lemma.**  Suppose the only possibly nonzero `A_e` are the
nine prism edges in (19), and every `A_e` has matrix rank at most one.  Then
`H_6(A) != Delta_{6,3}`.

**Proof.**  Each of the prism's four perfect matchings contributes a global
CP-rank-one tensor.  If the extra matching `P_0` vanishes, one of its three
vertical edges is zero, which also kills the corresponding `P_i`; at most two
terms remain.  If a color-class term `P_i` vanishes through a horizontal
edge, the three possible remaining terms are `P_0` and the other two
`P_j`.  At either endpoint of a vertical edge shared by `P_0` and a surviving
`P_j`, those two global terms have proportional local factors, so their three
local factors span a space of dimension at most two.  This contradicts the
mode rank three of `Delta_{6,3}`.  Thus all four matching terms would have to
be nonzero.

Group the parties as

\[
 X=\{1,4\},\qquad Y=\{2,5\},\qquad Z=\{3,6\}.
\]

Because every edge tensor has rank one, the three terms (19) can be written

\[
 x_1\otimes y_1\otimes z_1,quad
 x_2\otimes y_2\otimes z_2,quad
 x_3\otimes y_3\otimes z_3.
\]

The extra matching uses the `X`-internal edge of `P_1`, the `Y`-internal
edge of `P_2`, and the `Z`-internal edge of `P_3`.  Its tensor is therefore
*exactly*

\[
 x_1\otimes y_2\otimes z_3.                                  \tag{25}
\]

The grouped tensor `Delta_{6,3}` has multilinear rank `(3,3,3)`, so each of
the families `(x_1,x_2,x_3)`, `(y_1,y_2,y_3)`, and `(z_1,z_2,z_3)` must be
linearly independent.  Apply invertible maps on the three grouped spaces to
make them standard bases.  The four-term tensor becomes

\[
 T=e_1\otimes e_1\otimes e_1+e_2\otimes e_2\otimes e_2
   +e_3\otimes e_3\otimes e_3+e_1\otimes e_2\otimes e_3.      \tag{26}
\]

Its slice space in the first factor is

\[
 \operatorname{span}\{E_{11}+E_{23},E_{22},E_{33}\}.         \tag{27}
\]

A matrix
`a(E_11+E_23)+bE_22+cE_33` has rank at least two when `a != 0`
(look at rows `1,2` and columns `1,3`), and when `a=0` it has rank one only
on the two projective directions `E_22,E_33`.  Thus (27) contains only two
rank-one projective points.  On the other hand, every CP-rank-three tensor of
multilinear rank `(3,3,3)` has three independent rank-one matrices in each
slice space: in a three-term CP decomposition, full multilinear rank forces
all three factor families to be independent.  Hence `T` has CP rank at least
four (and the displayed expression gives equality), whereas
`Delta_{6,3}` has CP rank three.  This contradiction proves the lemma.  QED.

This lemma isolates the first genuine finite-versus-border rigidity: the
prism degeneration can approach the target only by leaving every bounded
rank-one parameter chart.  The unresolved general problem is to survive
higher-rank aggregate matrices and additional matching terms.

### The finite obstruction visible in the prism chart

The same example displays exactly what an eventual non-closed-image proof
must detect.  In the sparse diagonal prism chart, let the nine edge weights
be arbitrary finite scalars.  Exact normalization of the three constant
coefficients requires

\[
 w_{14}w_{23}w_{56}=w_{25}w_{13}w_{46}
 =w_{36}w_{12}w_{45}=1.                                      \tag{28}
\]

Every edge weight is then nonzero, so the unique rainbow coefficient

\[
 w_{14}w_{25}w_{36}                                           \tag{29}
\]

cannot vanish.  More explicitly, (29) times the product of the six
horizontal-edge weights equals the product of the three expressions in
(28), hence equals one.  In the degeneration, (29) tends to zero only because
the complementary product tends to infinity.  This is a Laurent/rational
obstruction on an open torus, not a polynomial equation on the output
closure.

## 7. Equality rigidity for rank-one, minimally active support

There is a useful general equality case behind the shorter prism proof.
Suppose `H_S(A)=Delta_{S,q}`, a vertex `p` has exactly `q` active neighbors,
and its active incident matrices have rank one,

\[
 A_{pj}=a_{pj}\otimes b_{pj}.
\]

The star expansion reads

\[
 \Delta_{S,q}=\sum_{j=1}^q a_{pj}\otimes
 (b_{pj}\otimes H_{S\setminus\{p,j\}}).                      \tag{30}
\]

Mode rank `q` makes the `a_pj` a basis.  Contract with its dual basis.  Each
coefficient tensor on the right is then both

\[
 b_{pj}\otimes H_{S\setminus\{p,j\}}
 \quad\text{and}\quad
 \sum_{r=1}^q\lambda_j(e_r)e_r^{\otimes(S\setminus\{p\})}.
\]

The first expression has partition rank one, while the diagonal-rank lemma
says the second has partition rank equal to the number of nonzero
`lambda_j(e_r)`.  Hence each dual vector has support one.  Invertibility
forces these supports to be distinct, so, after a permutation, `a_pj` is a
multiple of `e_j`; equality of the two simple tensors also forces `b_pj` to
be a multiple of the same `e_j` and the deleted hafnian to be a multiple of
`e_j` to the remaining tensor power.

Consequently, if the entire active support is `q`-regular, all its active
rank-one edges are same-color basis tensors and the incident colors form a
proper `q`-edge-coloring.  If there are no additional inactive nonzero edges,
different perfect matchings induce different vertex colorings: at each
vertex its color selects a unique incident edge.  Thus mixed coefficients
cannot cancel.

For `q=3` on a simple graph with at least six vertices, such a support always
has a fourth perfect matching besides its three color classes.  Here is a
self-contained proof.  The union of two color classes is a disjoint union of
alternating even cycles.  If there is more than one cycle, flip just one of
them.  Otherwise it is a Hamilton cycle `C`.  If an edge of the third color
joins opposite parities on `C`, use that edge and match the two remaining
even paths along `C`.  If every third-color chord joins equal parities, the
chords split into a perfect matching of the even positions and one of the
odd positions.  Some even chord and odd chord must interlace.  To see this,
if no oppositely typed chords crossed, parity of the number of opposite-type
endpoints inside any chord would force each matching to pair indices of the
same parity.  Restricting to each parity class and repeating forces matched
indices to be congruent modulo `2^r` for every `r`, impossible in a finite
nonempty set.  Use an interlacing even/odd chord pair; the four gaps between
their endpoints contain even numbers of vertices and can be matched along
`C`.  This gives a new perfect matching (for four vertices it is just the
third color class, which is exactly the exceptional case).

This proves the desired upper bound in the rank-one, 3-regular-support
subcase.  The gap in the full problem is to deduce such minimal activity and
rank-one structure in the presence of higher-rank matrices, inactive-edge
syzygies, and additional perfect matchings.

## 8. Strongest exact conclusions and remaining gap

The proved conclusions are:

1. `q <= n-1` for every exact realization, with the fully general `q <= 3`
   upper bound at `n=4`.
2. The coordinate-sensitive Hall inequalities (9)-(10) for every vertex,
   plus the exhaustive scalar edge-deletion bound (12).
3. The exact two-site differential/exterior identity (17), whose kernel is
   precisely the off-diagonal covectors.
4. Explicit signed cancellation showing that mixed terms and antisymmetric
   edge entries cannot be killed termwise.
5. The finite prism chart cannot realize `Delta_{6,3}` even with arbitrary
   edge matrices.  Three-slice center rigidity and the rectangular support of
   crossed edge products force the three horizontal terms to be monochromatic,
   leaving an uncancellable vertical rainbow term.  In the rank-one subcase,
   the same obstruction appears as grouped CP rank four.
6. For all even `n >= 6`, `Delta_{n,3}` lies in the closure of the very
   restrictive rank-one diagonal matching-tensor image.
7. If the active support is 3-regular, all active matrices are rank one, and
   there are no inactive nonzero edges, equality rigidity reduces the model
   to a proper three-edge-coloring; an alternating-cycle/chord argument then
   supplies a forbidden fourth perfect matching for every `n >= 6`.

The unresolved step is consequently not a polynomial tensor identity.
Arbitrary matrices `A_uv` allow several perfect matchings to contribute to
the same mixed coloring with complex cancellation.  To finish the upper
bound one needs an exact finite-parameter argument that prevents the prism's
`zero times infinity` mechanism after all possible cross-color entries and
cancellations are included.  A sufficient new lemma would be either:

* a justified reduction of every exact `Delta_{n,3}` representation to a
   nonvanishing Laurent chart carrying an invariant such as (28)-(29); or
* an equality/near-equality rigidity theorem for (9)-(12) that forces the
  active tensors into the rank-one diagonal toric stratum.

Neither follows from partition rank or the cap identities alone.  Balanced
`K_{3,3}` and the triangular prism saturate the available rank bounds, and
the border theorem shows why a closed algebraic obstruction cannot bridge
the gap.
