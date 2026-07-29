# Isotropic square jets force doubled target-axis centres

## 1. Outcome

Retain the live corank-two normal form

\[
 S_i=P_i\Delta,
 \qquad P_iHP_j^{\mathsf T}=(\beta_i+\beta_j)q_{ij},    \tag{1}
\]

and the polarized cap identity

\[
 {q^{r-1}\over(r-1)!}p(v)^2+(v^{\mathsf T}Bv)Q
       =\sum_{c=0}^2{v_c^2\over d_c}X_c,               \tag{2}
\]

where `p(v)` has local factor `P_i v`, `B=A_pq Delta^{-1}` is symmetric,
and `X_c=bigotimes_(i in W)e_c^(i)`.  Suppose the live component is proper,
so its
rank-three boundary contains a literal zero-star site `y` with `P_y=0`.

The diagonal values impose a finite pattern theorem which is stronger than
the annihilator target-cover statement.  On every irreducible component
`C` of the isotropic locus `v^T Bv=0`, and for every target coordinate
which is not identically zero on `C`, there are at least two distinct
outside sites `z` for which

\[
              0\ne P_z(\widehat C)\subseteq\mathbb C e_c.           \tag{3}
\]

Here `widehat C` is the vector subspace represented by `C` when `C` is a
projective line.  For an irreducible conic, or for `B=0`, condition (3)
means instead `0!=im P_z subseteq C e_c`, because the component spans the
whole three-space.

Every site in (3) is singular, lies outside the live component, and is a
literal zero-cross witness for colour `c` for every re-deleted live edge.
In particular the diagonal identities rule out all raw minimum covers made
from one rank-two site covering two axes, two rank-one sites covering two
axes, a rank-two plus a rank-one site covering three axes, or three
rank-one sites covering three axes.

The sharp surviving minima are:

| direct quadratic | isotropic components | forced centre pattern | minimum sites |
|---|---|---|---:|
| `B=0` | all of `P^2` | two rank-one sites of image `C e_c` for every `c` | 6 |
| `rank B=3` | one irreducible conic | the same six rank-one coordinate-image sites | 6 |
| `B=lambda E_cc` | the double line `v_c=0` | two centres for each of the other two colours | 4 |
| rank one, noncoordinate | one noncoordinate line | two centres for all three colours | 6 |
| rank two, both factors coordinate | two coordinate lines | four paired centres | 4 |
| rank two, at most one factor coordinate | two lines | the component requirements need at least six sites | 6 |

This is a value theorem, not a witness count: it follows from the first two
graded pieces of the square response.  It explains exactly how the new
coordinate-free diagonal lemma meets the equality-five witness boundary.
All cases with a six-site minimum are incompatible with a five-site witness
union.  The two four-site patterns can occupy four members of that union,
with the fifth witness left over, and their restricted isotropic cap
equations have exact rational cofactor models.  Thus those two patterns,
not the old one-site target covers, are the genuine finite residual.

## 2. A site-dependent second-order filtration

Fix `v` and put

\[
 L_i(v)=\begin{cases}
          \mathbb C P_iv,&P_iv\ne0,\\
          0,&P_iv=0.
        \end{cases}                                      \tag{4}
\]

Let `F_v^k` be the sum of tensor subspaces in which at least `k` sites
carry their factor in `L_i(v)`.  Since the two marked factors in `p(v)^2`
occupy distinct sites,

\[
                         p(v)^2{q^{r-1}\over(r-1)!}\in F_v^2.       \tag{5}
\]

On an isotropic direction, (2) therefore gives

\[
                         \sum_c{v_c^2\over d_c}X_c\in F_v^2.       \tag{6}
\]

Let `C` be an irreducible component of the isotropic locus.  Call `i` a
`(C,c)`-centre if, for general `[v] in C`,

\[
                              0\ne P_iv\in\mathbb C e_c.            \tag{7}
\]

For a general point of `C`, every accidental equation
`P_iv in C e_c` which is not identically true on `C` is avoided.  Choose a
complement to every nonzero line (4).  The tensor product is then graded by
the subset of sites at which the line factor is used.  If `a_c` is the
number of `(C,c)`-centres, the least-degree component of `X_c` has degree
exactly `a_c` and is nonzero.

Now use the literal zero boundary site `y`.  Since `L_y(v)=0`, its factor
in every least-degree component remains the unprojected vector `e_c`.
Hence least-degree components belonging to different colours are linearly
independent after flattening at `y`.  Components with different centre
subsets already lie in different direct summands.  If the smallest `a_c`
among the colours active on `C` were zero or one, the corresponding
least-degree part of the left side of (6) could not cancel, contradicting
membership in `F_v^2`.  Therefore

\[
                  \boxed{a_c\ge2\quad
                    \text{for every colour active on }C.}          \tag{8}
\]

This proves the doubled-centre theorem.

If `C=P(K)` is a projective line, (7) is precisely
`0!=P_iK subseteq C e_c`, which implies `rank P_i<=2`.  If `C` spans
`P^2`, its image under a linear map can be a fixed projective point only
when `im P_i=C e_c`.  An invertible live `P_i` satisfies neither
condition, so all centres lie outside `U`.

## 3. Zero-cross and dead-edge geometry

Let `K_c` be the alternating three-by-three form with kernel `C e_c`.
At a line-component centre, either `rank P_i=1`, or `im P_i` is a plane
containing `e_c`.  In both cases

\[
                              P_i^{\mathsf T}K_cP_i=0.               \tag{9}
\]

For a live pair `a,b`, equation (1) expresses both low-rank blocks to `i`
as nonzero scalar multiples of `P_aHP_i^T` and `P_bHP_i^T`.  Thus

\[
 q_{ai}K_cq_{bi}^{\mathsf T}=0,                         \tag{10}
\]

so every centre is a literal colour-`c` zero-cross witness for every live
edge.  A rank-one coordinate-image centre satisfies (9) for all three
colours.

The dead relation edges add an exact but limited restriction.  Such an
edge `ij` obeys

\[
                    P_iHP_j^{\mathsf T}=0,
       \qquad \operatorname {rank}P_i+\operatorname {rank}P_j\le3. \tag{11}
\]

Consequently two rank-two centres can never be joined by a dead relation
edge.  A rank-two/rank-one dead pair is possible only when their row plane
and row line are exactly `H`-orthogonal, and two rank-one centres are dead
exactly when their row lines are `H`-orthogonal.  These alternatives do not
collapse the four-centre minima below; Section 6 gives rational models.

## 4. Classification of the minimum patterns

If `B=0`, every direction is isotropic and all three coordinates are
active.  A centre valid on all of `P^2` has
`im P_i=C e_c`; (8) gives two distinct sites for each colour, hence six
rank-one sites.  The same argument applies when `rank B=3`: its irreducible
conic spans `P^2` and every coordinate is active.

If `rank B=1`, write `B=uu^T` up to a scalar.  Its isotropic component is
the projective line `P(u^perp)`.  When `u` is a coordinate vector, say
`B=lambda E_cc`, the coordinate `v_c` vanishes identically and the other
two are active.  Equation (8) gives two distinct centres for each of those
two colours, hence four sites.  One site cannot serve both colours because
the nonzero line `P_i(u^perp)` cannot lie on two distinct coordinate axes.
For noncoordinate `u`, all three colours are active and six centres are
required.

If `rank B=2`, over `C` write

\[
                         v^{\mathsf T}Bv=\ell_+(v)\ell_-(v).         \tag{12}
\]

Each factor gives a two-dimensional isotropic plane `K_+` or `K_-`.  On a
noncoordinate plane all three colours are active; on `v_c=0` exactly the
other two are active.  A single site can be a centre for at most one colour
on each component.  It can pair a `(+ ,c)` requirement with a `(-,d)`
requirement as follows:

* if `c=d`, its whole image lies on `C e_c` and it has rank one;
* if `c!=d`, it kills `K_+ intersection K_-` and can have rank two with
  image `span(e_c,e_d)`.

If both components are coordinate planes, each contributes four centre
incidences and they can be paired on four sites.  If at least one component
is noncoordinate, that component alone needs six distinct sites; all
requirements from the other component can overlap those six, but the
minimum cannot fall below six.  This proves the table in Section 1.

## 5. The remaining contracted cap equations

Let `C=P(K)` be a line component and let `A` be its centre set.  At every
other site choose, when possible,

\[
                    \eta_i\in\operatorname {Ann}(P_iK).             \tag{13}
\]

Contract those sites and leave `A` open.  For `x,z in K`, both marked
factors are forced onto `A`.  Since the restriction of `B` to the totally
isotropic plane `K` is zero, the surviving equation is

\[
 p_A(x)p_A(z)R_A
   =\sum_{c\ \mathrm{active\ on}\ K}
       {x_cz_c\over d_c}\tau_c X_{c,A},                \tag{14}
\]

where `R_A` is the contracted common cofactor and

\[
                         \tau_c=\prod_{i\notin A}\eta_i(e_c).       \tag{15}
\]

Thus the finite centre pattern is an honest smaller bilinear cap problem,
not only an incidence shadow.  Both active target values can be retained
exactly when the covectors in (13) can be chosen nonzero on both axes.  If
one cannot, then some noncentre plane `P_iK` contains that target axis;
this is the precise additional alignment escape left by the contraction.

For `B=lambda E_cc`, take active colours `d,e`.  The following normalized
minimum four-centre instance on `d_1,d_2,e_1,e_2` has

\[
 p_d=e_d^{(d_1)}+e_d^{(d_2)},
 \qquad p_e=e_e^{(e_1)}+e_e^{(e_2)}.                   \tag{16}
\]

The restricted equations (14) are consistent.  With `tau_d=tau_e=1`
and `d_d=d_e=1`, put

\[
 R_A={1\over2}e_d^{(e_1)}e_d^{(e_2)}
          +{1\over2}e_e^{(d_1)}e_e^{(d_2)}.             \tag{17}
\]

Then

\[
 p_d^2R_A=X_{d,A},\qquad p_e^2R_A=X_{e,A},
 \qquad p_dp_eR_A=0.                                   \tag{18}
\]

The two-coordinate-factor rank-two pattern has the same exact model on
each isotropic component separately.  The contractions (13) for its two
different planes need not agree, so comparing the resulting cofactors as
though they were one tensor would be invalid.  Equations (14)--(18) show
why the four-centre patterns survive the present diagonal jet.  They do
not, however, lift to the actual common power in the normalized rational
models of Section 6: the one-hole hafnian recurrence proving this is in
[`four-centre-common-power-one-hole-obstruction.md`](four-centre-common-power-one-hole-obstruction.md).

For `B=0`, taking `K=V` in (13) is impossible at every live site because
`Ann(P_iV)=0` there.  An irreducible rank-three conic likewise has no one
linear subspace `K` whose annihilators produce a centre-only contraction.
Thus their forced six-centre patterns do not automatically become isolated
six-site cap equations; the unavoidable live factors are the exact
remaining obstruction.

## 6. Exact rational structural models

The centre requirements, zero-cross equations, dead-edge normal form, and
zero boundary are mutually compatible.  Take

\[
 H=\begin{pmatrix}0&1&2\\1&0&3\\2&3&0\end{pmatrix},
 \qquad \Delta=\operatorname {diag}(2,3,5).             \tag{19}
\]

Use three live sites with `P=I`, four centre sites, and one zero boundary
site `y`.  Give every nonzero-`P` site `beta=1`, give `y` `beta=-1`, put

\[
 q_{ij}={1\over2}P_iHP_j^{\mathsf T}                   \tag{20}
\]

between nonzero sites, and put an invertible copy of `H` on every desired
edge from `y`.  Then (1) holds exactly, the rank-three graph is connected
and nonbipartite, and every edge leaving the live component in that graph
ends at the literal zero site.

For `B=E_00`, take two copies of each matrix

\[
                         P_1=\operatorname {diag}(1,1,0),
       \qquad           P_2=\operatorname {diag}(1,0,1).            \tag{21}
\]

On `K=span(e_1,e_2)`, these map respectively onto `C e_1` and `C e_2`.
For the rank-two quadratic `v_0v_1`, take two copies of

\[
                         P_{10}=\operatorname {diag}(1,1,0)
\]

and two copies of

\[
                         P_2=\operatorname {diag}(0,0,1).           \tag{22}
\]

The first matrix pairs the `(v_0=0,1)` and `(v_1=0,0)` requirements; the
second pairs the colour-two requirement on both components.  These are
exact rational local counterconfigurations to any attempt to eliminate the
four-site patterns using only (1), (3), (9)--(11), or the five-witness
incidence shadow.  They are not asserted to satisfy the uncontracted cap
equation; the surviving equations are precisely (14).

For every six-centre row of the table, one equally takes two copies of

\[
                              P_c=e_ce_c^{\mathsf T}
                    \qquad(c=0,1,2).                    \tag{23}
\]

Each is a rank-one centre for its indicated colour on every isotropic
component, is triple zero-cross, and fits the same relation-block
construction (20).  Hence dead-edge orthogonality and the zero cut alone
also do not exclude the six-centre pattern at larger orders.

## 7. Exact audit

[`verify_live_isotropic_second_jet_cover_patterns.py`](../computations/verify_live_isotropic_second_jet_cover_patterns.py)
checks (8) as a graded-support statement, enumerates the component-incidence
minima in the table, verifies every rank, anchor, zero-cross, dead-edge, and
relation block in (19)--(22), and verifies the four-site cofactor identity
(18) over the rationals.
