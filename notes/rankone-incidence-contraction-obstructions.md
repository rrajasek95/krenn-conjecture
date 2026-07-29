# Rank-one incidence contractions and a three-direction obstruction

## 1. Scope and outcome

This note concerns the **simple rank-one aggregate chart**.  Thus every
nonzero aggregate block on a pair `uv` has one factorization

\[
 A_{uv}=x_{u|v}\otimes x_{v|u},\qquad x_{u|v}\in V_u,
 \quad x_{v|u}\in V_v.                                    \tag{1}
\]

Equivalently, this is a local restriction of the perfect-matching
incidence tensor of a simple graph: the column at `u` indexed by the edge
`uv` maps to `x_(u|v)`.  This is strictly narrower than the arbitrary
aggregate problem.  An arbitrary `3 by 3` block is a sum of at most three
rank-one occurrences, so its incidence model is a **multigraph** with
parallel occurrences.  The arguments below which choose one forbidden
symbol for a neighbor use the absence of parallel occurrences and are not
silently asserted for that full model.

Two exact conclusions are proved.

1. Contracting all but one site against annihilators of a fixed incidence
   column gives a rank-one diagonal identity.  In particular, if color `r`
   occurs on a unique incoming coordinate half-edge at a vertex, that edge
   is a mutual same-color coordinate edge.
2. Suppose, more restrictively, that at every site all incident half-edge
   vectors occupy three projective lines.  Use those lines as a local
   incidence basis.  Every nonzero entry of the transition matrix from the
   GHZ basis to that incidence basis then needs a distinct, explicitly
   aligned incident witness.  Hence a generic pair of bases (no common
   projective line) is impossible.  This excludes the natural Fourier
   character construction uniformly at every even order.

Neither result proves that arbitrary rank-one incidence maps use only three
directions.  That monomialization step remains the precise gap between this
note and a uniform rank-one theorem.

## 2. The incidence restriction

Let `G` be a simple graph on an even vertex set `B`, and let

\[
 T_G=\sum_{M\in\operatorname {PM}(G)}
             \bigotimes_{v\in B}f_{v,M(v)},               \tag{2}
\]

where `(f_(v,e):e incident to v)` is the incidence basis at `v`.  Given
linear maps `L_v` with

\[
                         L_vf_{v,uv}=x_{v|u},              \tag{3}
\]

one has

\[
 (\bigotimes_vL_v)T_G
 =\sum_{M\in\operatorname {PM}(G)}
      \bigotimes_{uv\in M}(x_{u|v}\otimes x_{v|u})
 =H_B(A).                                                  \tag{4}
\]

Conversely, (1) defines the maps (3).  Thus an identity

\[
                         H_B(A)=\Delta_{B,3}
 :=\sum_{r=0}^2e_r^{\otimes B}                             \tag{5}
\]

is exactly a local restriction `T_G -> Delta_(B,3)`.  Mode rank in (5)
forces every `L_v` to have rank three.

For comparison, if `A_uv=sum_(k=1)^rho x_(u|v,k) tensor
x_(v|u,k)`, introduce `rho` parallel edge occurrences on `uv`.  Formula
(4) then expands the product of these sums and recovers the arbitrary
aggregate block.  A theorem for every loopless multigraph would therefore
settle the full aggregate problem; the theorems below only claim their
stated simple-graph consequences.

## 3. A one-center annihilator identity

Fix `p in B`.  For `u ne p`, put

\[
                              y_u=x_{u|p}\in V_u.          \tag{6}
\]

Thus `y_u` is the factor at the endpoint opposite `p` on the edge `pu`;
put `y_u=0` if that edge is absent.  Choose independently

\[
                  \alpha_u\in V_u^*,\qquad \alpha_u(y_u)=0.\tag{7}
\]

Contracting every site other than `p` in (5) by these covectors kills every
source matching: the edge incident with `p` is `pu` for some `u`, and its
factor at `u` is killed by (7).  Hence

\[
 \boxed{\quad
   \sum_{r=0}^2\left(\prod_{u\ne p}\alpha_u(e_r)\right)e_r=0.
 \quad}                                                    \tag{8}
\]

The three coordinate components in (8) separate.  For a fixed `r`, if no
nonzero `y_u` were proportional to `e_r`, the plane `y_u^perp` would contain
a covector with nonzero `r`-coordinate for every `u` (also trivially when
`y_u=0`).  Choosing them independently would make the `r`-product in (8)
nonzero.  Therefore:

**Lemma 3.1 (incoming coordinate anchors).**  For every ordered pair
`(p,r)`, some neighbor `u` satisfies

\[
                              x_{u|p}\in\mathbb C^*e_r.    \tag{9}
\]

This is the rank-one specialization of the forced incident-edge theorem,
but the contraction (8) will also give a useful equality case.

## 4. Leaving one hole open

Fix `w ne p` and impose (7) only at `u notin {p,w}`.  A matching in which
`p` is paired with a contracted site is killed.  The only surviving
matchings use `pw`; after deleting that edge their sum is the matching
tensor on `B minus {p,w}`.  Hence

\[
 \boxed{\quad
  \operatorname {diag}(t_0,t_1,t_2)
   =h(\alpha)\,x_{p|w}x_{w|p}^{\mathsf T},\qquad
  t_r=\prod_{u\notin\{p,w\}}\alpha_u(e_r),
 \quad}                                                    \tag{10}
\]

where

\[
 h(\alpha)=\left\langle H_{B\setminus\{p,w\}}(A),
              \bigotimes_{u\notin\{p,w\}}\alpha_u\right\rangle.
                                                                    \tag{11}
\]

This is an identity for every independent choice of annihilators, with no
genericity or termwise-cancellation assumption.  Its right side has matrix
rank at most one.

**Theorem 4.1 (unique anchor becomes mutual).**  Suppose `w` is the unique
site for which `x_(w|p)` is a nonzero multiple of `e_r`.  Then

\[
                 x_{p|w}\in\mathbb C^*e_r,qquad
                 x_{w|p}\in\mathbb C^*e_r.                \tag{12}
\]

Moreover, choices in (7) can be made for which `t_r ne 0`; for every such
choice, `h(alpha) ne 0` and (10) is a nonzero multiple of `E_rr`.

**Proof.**  For every `u notin {p,w}`, the vector `y_u` is not proportional
to `e_r`.  The restriction of the `r`-th coordinate functional to the plane
`y_u^perp` is therefore nonzero.  Choose `alpha_u` in that plane with
`alpha_u(e_r) ne 0`.  Then `t_r ne 0`, so the left side of (10) is nonzero.
Because it equals a rank-one matrix, all its other diagonal entries vanish
and it is exactly `t_rE_rr`.  Equality of two nonzero rank-one matrices
forces both factors on the right of (10) to span the corresponding row and
column lines, proving (12); it also forces `h(alpha) ne0`.  `QED`

In directed language, draw an `r`-arc `u -> p` when
`x_(u|p) in C^*e_r`.  Lemma 3.1 says that every vertex has positive
in-degree in every color.  Theorem 4.1 says that an `r`-arc which is the
unique incoming `r`-arc at its head is automatically a bidirected
same-color coordinate edge.  This conclusion is stronger than the bare
anchor count, but dense configurations may have two or more incoming
anchors of every color.

There is a useful degree consequence.  Let `d(p)` be the degree of `p` in
the nonzero simple support graph, and suppose `d(p)<=5`.  Start with one
incoming coordinate anchor in each of the three colors.  Every color which
is not unique costs at least one additional incident edge.  Hence at most
`d(p)-3` colors can be nonunique, so at least

\[
                              6-d(p)                       \tag{12a}
\]

colors are unique.  Their edges are distinct and Theorem 4.1 makes all of
them mutual same-color coordinate edges.  In particular:

* degree three forces all three incident edges to be mutual coordinate
  edges of distinct colors;
* degree four forces at least two such edges; and
* degree five forces at least one.

Thus a simple rank-one support of maximum degree four contains a spanning
mutual-coordinate subgraph of minimum degree two, and that subgraph contains
a cycle.  This is structural information, not yet a contradiction: the
cycle can have cancellation mates through the remaining edges.

## 5. Three projective incidence directions

Assume now that at each vertex `v` there is a basis

\[
                         f_{v,0},f_{v,1},f_{v,2}           \tag{13}
\]

such that every nonzero incident vector `x_(v|u)` is proportional to one of
these three vectors.  Absorb its nonzero scalar into the edge weight, and
write

\[
                         \ell_v(u)\in\{0,1,2\}            \tag{14}
\]

for the resulting local incidence label.  Rank `L_v=3` means that all three
labels occur at `v`.

Write the target in these local bases.  There are bases
`y_(v,0),y_(v,1),y_(v,2)` (the three local factors in its unique GHZ
decomposition) such that

\[
                 \Delta'=\sum_{r=0}^2\bigotimes_vy_{v,r}.\tag{15}
\]

Let

\[
               Y_v(a,r)=f_{v,a}^*(y_{v,r})                \tag{16}
\]

be the invertible transition matrix.

**Theorem 5.1 (isolated-word alignment).**  Fix a vertex `v`, an incidence
label `a`, and a target component `r` with `Y_v(a,r) ne0`.  Then there is a
neighbor `u` such that

\[
 \ell_v(u)=a,
 \qquad y_{u,r}\in\mathbb C^*f_{u,\ell_u(v)}.             \tag{17}
\]

For fixed `(v,a)`, the witnesses required by different values of `r` are
distinct.  Consequently

\[
           \#\{u:\ell_v(u)=a\}
              \ge \#\{r:Y_v(a,r)\ne0\},
 \qquad n-1\ge \#\operatorname {supp}(Y_v)                \tag{18}
\]

for the complete simple graph (and with `n-1` replaced by the simple
support degree in general).

**Proof.**  Put

\[
                         S=\{u:\ell_v(u)=a\}.             \tag{19}
\]

Every label occurs at `v`, so `S` is a nonempty proper subset of the
neighbors.  For `u in S`, put `d_u=ell_u(v)`.  Consider all incidence-basis
words `c` satisfying

\[
              c_v=a,\qquad c_u\ne d_u\quad(u\in S),       \tag{20}
\]

with the other symbols arbitrary.  No matching has label word `c`: every
edge at `v` whose `v`-label is `a` ends at some `u in S`, but (20) rejects
that edge at its other endpoint.  Since the source coefficient is zero at
every word (20), the same is true of (15).

Let `P_u` be coordinate projection onto
`span{f_(u,b):b ne d_u}` for `u in S`, and the identity outside `S`.  The
simultaneous vanishing just obtained is the tensor identity

\[
  0=\sum_{s=0}^2Y_v(a,s)
       \left(\bigotimes_{u\in S}P_uy_{u,s}\right)
       \otimes
       \left(\bigotimes_{u\notin S\cup\{v\}}y_{u,s}\right). \tag{21}
\]

Choose a vertex `w notin S union {v}`; it exists because `S` is proper.
The three vectors `(y_(w,s))_s` form a basis.  Contracting (21) at `w` by
its dual basis isolates each summand.  For the fixed `r` with
`Y_v(a,r) ne0`, the resulting pure tensor is zero.  Hence
`P_uy_(u,r)=0` for some `u in S`, which is precisely (17).

One neighbor cannot witness two different components, because the
`y_(u,r)` are linearly independent whereas the right side of (17) is one
line.  This proves both inequalities in (18).  `QED`

**Corollary 5.2 (generic three-direction obstruction).**  If

\[
 \{\mathbb Cy_{u,0},\mathbb Cy_{u,1},\mathbb Cy_{u,2}\}
 \cap
 \{\mathbb Cf_{u,0},\mathbb Cf_{u,1},\mathbb Cf_{u,2}\}
 =\varnothing                                             \tag{22}
\]

at every site `u`, then no simple rank-one incidence restriction can equal
the ternary GHZ tensor.

Indeed, every row of every invertible `Y_v` contains a nonzero entry, and
Theorem 5.1 would produce an alignment forbidden by (22).

## 6. Uniform exclusion of the Fourier-character chart

Let `omega` be a primitive cube root of unity and suppose every half-edge
vector, up to a nonzero scalar, is one of

\[
       g_b=(1,\omega^b,\omega^{2b})^{\mathsf T},
       \qquad b\in\mathbb Z/3.                            \tag{23}
\]

The three `g_b` form the Fourier basis, and none is proportional to a target
coordinate vector `e_r`.  Corollary 5.2 therefore excludes this chart for
every even order `n>=4`.

There is also a direct support proof which is useful as an audit.  In the
Fourier basis the target is, up to one nonzero global scalar,

\[
                 Z_n=\sum_{c:\ \sum_vc_v=0}
                              f_{c_1}\otimes\cdots\otimes f_{c_n}.\tag{24}
\]

Give the half-edge at `v` toward `u` its Fourier label `b_(v,u)`.  Fix a
vertex `v` and a desired label `a`.  Let
`S={u:b_(v,u)=a}`.  Since the local map has rank three, `S` is proper.
For each `u in S`, choose `c_u ne b_(u,v)`.  Choose arbitrary values at all
but one of the other vertices, and use the remaining vertex outside `S` to
make `sum c_v=0`, with `c_v=a`.  (Its edge to `v` is already rejected at
the `v` endpoint, so its own value is unrestricted.)  The resulting
zero-sum word has no compatible edge at `v`, and hence no compatible
perfect matching.  Its coefficient in (24) is nevertheless nonzero, the
contradiction.

This proof permits arbitrary nonzero complex half-edge scalars and arbitrary
cancellation among matchings with the same label word.  It uses only that a
nonzero target word needs at least one compatible matching.

## 7. Exact boundary of the result

The obstruction is not a theorem for arbitrary local maps.  A simple
rank-one aggregate source may have four or more projectively different
vectors at a site, so there need not be a three-symbol incidence labeling
(14).  With parallel rank-one occurrences on one underlying pair, even a
three-direction labeling does not give the isolated word (20): different
parallel occurrences can present all three opposite labels at the same
neighbor.  Both escape routes occur before any coefficient cancellation is
examined.

Accordingly the surviving rank-one question is sharp:

> Can the exact GHZ coefficient equations force every simple incidence map
> into three projective directions, or can a fourth local direction support
> finite cancellations which evade Theorems 4.1 and 5.1?

The known tight/free interpolation examples show that arbitrary tensor
supports can use a fourth direction.  They do not satisfy perfect-matching
rectangle completion, so they do not decide this incidence-specific
question.
