# The good-pair response fork and exact overlap flatness

## 1. Outcome

There is a canonical object which puts the two surviving good-pair escapes
in one diagram.  It is a **response fork**, rather than an ordinary chain
complex:

\[
 \widehat K_q\ \xleftarrow{\ \delta_q\ }\ \mathfrak t_W
       \ \xrightarrow{\ B_3(q)\ }\ \mathbb C^{E_3(q)}.             \tag{1}
\]

Its left cohomology is exactly the extra source-Hessian kernel (E1), and
its right cohomology is exactly the bipartite/isolated defect space (E2):

\[
 H^-(q):=\operatorname {coker}\delta_q\simeq E_q,
 \qquad
 H^+(q):=\ker B_3(q)=D_q.                                  \tag{2}
\]

For every physical off-diagonal pair response, exactly one of the following
happens:

* its class is a distinguished nonzero E1 class; or
* it has a vertex-weight primitive, and every such primitive belongs to
  the E2 defect space.

This unification retains zero blocks, endpoint order, arbitrary complex
cancellation, and the scalar direct entry.  It also exposes the exact
overlap law.  If a response in the chart deleting `r,u` has primitive
`alpha`, then its coordinate at a third vertex `v`, together with the
blocks incident to `v`, gives a first-order transition equation.  A
near-perfect-matching gauge identity makes the complete target-zero triple
row cancel **before multiplication or passage modulo an annihilator**.
Thus boundary responses are flat in the strongest literal sense.

What does not follow is a chart-to-chart parallel transport map.  Canonical
restrictions give linear relations on overlaps, but the restriction maps
need not be isomorphisms, the full transition equation does not output the
primitive of the adjacent chart, and active E1 classes need not integrate.
Consequently the currently available local data do not prove the proposed
global dichotomy “rank-at-most-two colour subbundle or active clean cap.”
Section 8 states the missing synchronization/factorization gate precisely.

## 2. Coordinate-free local construction

Work in the site-square-zero algebra

\[
 \mathcal R(S)=\bigotimes_{i\in S}(\mathbb C\oplus V_i),
 \qquad V_iV_i=0,
\]

and write \(\mathcal R_k(S)\) for its site-degree-`k` part.  Delete an
**oriented** good pair `(r,u)` from an exact ternary source on
`|B|=2m`, put

\[
 W=B\setminus\{r,u\},\qquad |W|=2t,\qquad t=m-1,
\]

and let \(q\in\mathcal R_2(W)\) be the internal quadratic.  Put

\[
 Q_q=q^{[t]},\qquad
 H_q:\mathcal R_2(W)\longrightarrow\mathcal R_{2t}(W),
 \quad H_q(Z)=Zq^{[t-1]}.                                \tag{3}
\]

The site-scaling Lie algebra is the intrinsically indexed space

\[
                  \mathfrak t_W=\bigoplus_{i\in W}\mathbb C\epsilon_i.
\]

For \(\alpha\in\mathfrak t_W\), define the infinitesimal vertex scaling
\(\Gamma_q(\alpha)=Z^\alpha\) blockwise by

\[
                    (Z^\alpha)_{ij}=(\alpha_i+\alpha_j)q_{ij}.       \tag{4}
\]

Every perfect matching uses every site once, so

\[
              H_q(Z^\alpha)=\left(\sum_{i\in W}\alpha_i\right)Q_q. \tag{5}
\]

This identity remains true when \(Q_q=0\), when some or all blocks vanish,
and without any rank hypothesis.

Define the augmented response-cycle space

\[
 \widehat K_q=
 \{(Z,\lambda)\in\mathcal R_2(W)\oplus\mathbb C:
                         H_q(Z)=\lambda Q_q\},                       \tag{6}
\]

and the left arrow of (1) by

\[
 \delta_q(\alpha)=
       \left(Z^\alpha,\sum_{i\in W}\alpha_i\right).                 \tag{7}
\]

For the right arrow, let `G_3(q)` have vertex set `W` and edge `ij`
exactly when the endpoint-ordered block \(q_{ij}\in V_i\otimes V_j\)
has rank three.  Zero blocks and rank-one or rank-two blocks are not edges.
Its signless incidence map is

\[
 B_3(q):\mathfrak t_W\longrightarrow\mathbb C^{E_3(q)},
 \qquad (B_3(q)\alpha)_{ij}=\alpha_i+\alpha_j.                      \tag{8}
\]

No basis inside any \(V_i\) is used in (3)--(8).  Changing endpoint order
transposes a block and therefore preserves its rank.

## 3. The two cohomologies and the physical response dichotomy

Recall the usual extra-Hessian quotient

\[
 E_q=\ker H_q\Big/
       \{Z^\alpha:\sum_i\alpha_i=0\}.                              \tag{9}
\]

**Theorem 3.1 (response-fork cohomology).**  The assignments in (2) are
canonical.  Moreover,

\[
 \dim H^+(q)=
 \#\{\text{nontrivial bipartite components of }G_3(q)\}
       +\#\{\text{isolated vertices of }G_3(q)\}.                  \tag{10}
\]

**Proof.**  Equation (5) first proves that `delta_q` lands in
`widehat K_q`.  Given `(Z,lambda)` in (6), choose any
\(\beta\in\mathfrak t_W\) with \(\sum_i\beta_i=\lambda\) and set

\[
 \Phi([(Z,\lambda)])=[Z-Z^\beta]\in E_q.                           \tag{11}
\]

The numerator is in `ker H_q` by (5).  Two choices of `beta` differ by a
zero-sum gauge; changing `(Z,lambda)` by `delta_q(alpha)` has the same
effect.  Conversely, `Z in ker H_q` maps to the class of `(Z,0)`.
If (11) is zero, then `Z-Z^beta=Z^gamma` for a zero-sum `gamma`, whence
`(Z,lambda)=delta_q(beta+gamma)`.  This proves the first isomorphism,
including the case `Q_q=0`.

On a connected component of `G_3(q)`, equation `B_3 alpha=0` says that
the weights alternate across edges.  A nontrivial bipartite component has
one shore-sign parameter, a nonbipartite component has none because an odd
cycle changes its sign, and an isolated vertex has one free parameter.
Components are independent, proving (10).  \(\square\)

Now orient the deleted stars at `r` and `u`.  Thus `p_c` is the colour-`c`
row at `r`, `s_d` the colour-`d` row at `u`, and
\(a^{ru}_{cd}\) is the `(c,d)` entry of the direct block in that order.
The exact pair equation in divided powers is

\[
 a^{ru}_{cd}Q_q+H_q(p_cs_d)=\delta_{cd}X_c^W.                       \tag{12}
\]

For `c != d`, define the augmented physical response

\[
                   R^{ru}_{cd}=(p_cs_d,-a^{ru}_{cd})\in\widehat K_q. \tag{13}
\]

Under (11), its left class is the customary distinguished class

\[
 \left[p_cs_d+{a^{ru}_{cd}\over t}q\right]\in E_q;                 \tag{14}
\]

indeed one may take every coordinate of `beta` equal to
`-a^(ru)_(cd)/(2t)`.

**Theorem 3.2 (one-response E1/E2 dichotomy).**  If the class of (13) is
zero, then every primitive

\[
                   R^{ru}_{cd}=\delta_q(\alpha)                     \tag{15}
\]

satisfies

\[
                     B_3(q)\alpha=0,
 \qquad              \sum_i\alpha_i=-a^{ru}_{cd}.                  \tag{16}
\]

Thus a gauge-rigid chart, for which `E_q=0`, sends all six off-diagonal
responses to E2 primitives.  A primitive is unique whenever `delta_q` is
injective.  In the gauge-rigid charts used in the good-pair analysis,
pair-complement activity makes the nonzero-block graph connected and
nonbipartite, so the vertex-gauge map is injective and the primitive is
indeed unique.

**Proof.**  On a rank-three edge `ij`, the physical block of `p_c s_d` is

\[
 p_{c,i}\otimes s_{d,j}+s_{d,i}\otimes p_{c,j},                     \tag{17}
\]

of matrix rank at most two.  The same block in `Z^alpha` is
`(alpha_i+alpha_j)q_ij`, which has rank three unless its scalar is zero.
Equality (15), block by block, therefore gives
`alpha_i+alpha_j=0`.  The scalar coordinate of (15) gives the second
identity in (16).  Zero blocks never enter this comparison and no sum of
different physical blocks is separated.  \(\square\)

There is a direct cap interpretation.  The canonical unnormalized pair
cap is

\[
                 \mathcal P^{cd}_{ru}=t p_cs_d+a^{ru}_{cd}q.       \tag{16a}
\]

If (15) holds, then

\[
 \mathcal P^{cd}_{ru}=Z_q^\theta,
 \qquad
 \theta=t\alpha+{a^{ru}_{cd}\over2}{\bf1},
 \qquad \sum_i\theta_i=0.                                      \tag{16b}
\]

Thus on the E2 side the canonical off-diagonal cap is literally a
zero-sum Hessian gauge, while on the E1 side its quotient class is
`t[R^(ru)_(cd)]` and is nonzero.  This identifies the pair-cap class, but
it does **not** construct an active cap covector or prove the nonlinear
source-form cap equation.

## 4. Why an ordinary three-term complex is not the right object

The two actual response maps in (1) have the same domain and point in
opposite directions in the zigzag.  Making `delta_q` and `B_3(q)`
consecutive differentials would require a vanishing composition which is
false in general.

For an explicit guard, take four sites, put

\[
 q_{01}=I_3,\qquad q_{02}=e_0\otimes e_0,
\]

and let every other block be zero.  Then `G_3(q)` consists of the edge
`01` and two isolated vertices.  The vector

\[
                         \zeta=(1,-1,0,0)                           \tag{18}
\]

lies in `ker B_3(q)` and has sum zero, but

\[
                    (Z^\zeta)_{02}=e_0\otimes e_0\ne0.              \tag{19}
\]

Hence `delta_q(zeta) != 0`: an E2 vector can be a nonzero boundary on the
E1 side.  In particular, the inclusion
`D_q -> mathfrak t_W` followed by `delta_q` is not a differential.

One can formally package (2) into the split three-term complex

\[
 \mathfrak t_W\xrightarrow{(\delta_q,0)}
       \widehat K_q\oplus\mathfrak t_W
   \xrightarrow{(0,B_3(q))}\mathbb C^{E_3(q)},                    \tag{20}
\]

whose middle cohomology is `E_q direct-sum D_q`.  But (20) inserts a
zero coupling by hand and contains no transition or holonomy information.
The fork (1), with its physical distinguished elements (13), is therefore
the minimal non-artificial unified object.  Dualizing one arrow is also
possible, but it replaces one of the desired spaces by its dual cokernel.

## 5. Canonical overlap restrictions

Fix a fan centre `r`, put `U=B\setminus{r}`, and let `F subset U` be a
set of good fan neighbours.  For `u in F`, write

\[
 W_u=U\setminus\{u\},\qquad q_u=Q|_{W_u}.
\]

For distinct `u,v in F`, their common odd complement is

\[
 K_{uv}=U\setminus\{u,v\},\qquad q_{uv}=Q|_{K_{uv}}.                \tag{21}
\]

On an arbitrary site set `S`, define the two common reservoirs

\[
 \mathscr Q(S)=\mathcal R_2(S)/\Gamma_{q_S}(\mathfrak t_S),
 \qquad
 \mathscr D(S)=\ker B_3(q_S).                                      \tag{22}
\]

There are canonical restriction maps

\[
 \begin{aligned}
 \rho^-_{u,uv}:H^-(q_u)&\longrightarrow\mathscr Q(K_{uv}),
 &[(Z,\lambda)]&\longmapsto[Z|_{K_{uv}}],\\
 \rho^+_{u,uv}:H^+(q_u)&\longrightarrow\mathscr D(K_{uv}),
 &\alpha&\longmapsto\alpha|_{K_{uv}}.                             \tag{23}
 \end{aligned}
\]

For the first map, changing a representative by `delta_(q_u)(alpha)`
changes its restriction by the full gauge
`Gamma_(q_uv)(alpha|K_uv)`.  Equivalently, in the presentation (9), the
restrictions of zero-sum gauges on `W_u` are exactly all gauges on
`K_uv`: extend `gamma in mathfrak t_(K_uv)` by the coordinate
`-sum gamma` at `v`.  The second map is valid because `G_3(q_uv)` is the
induced subgraph of `G_3(q_u)`.  Thus zero, low-rank, and rank-three blocks
all behave correctly under deletion.

The two arrows into a common reservoir define a canonical **transition
relation**

\[
 \mathcal T^\pm_{uv}=
 \{(x_u,x_v):\rho^\pm_{u,uv}(x_u)=\rho^\pm_{v,uv}(x_v)\}.            \tag{24}
\]

It is generally a relation, not the graph of a linear map: either
restriction can have a kernel or acquire new degrees of freedom after a
vertex becomes isolated.  Restrictions commute under every further
deletion.

For local families \(x_u^\pm\), define their structural curvature
by

\[
 \kappa^\pm_{uv}=ho^\pm_{u,uv}(x_u^\pm)
                         -\rho^\pm_{v,uv}(x_v^\pm).                 \tag{25}
\]

On three fan charts `u,v,w`, restriction to
`L=U\setminus\{u,v,w}` gives the exact Bianchi identity

\[
 \kappa^\pm_{uv}|_L+\kappa^\pm_{vw}|_L
                         +\kappa^\pm_{wu}|_L=0.                    \tag{26}
\]

This is a genuine coordinate-free flatness law, although at this point it
is the telescoping law of the restriction system rather than a new source
equation.

The positive reservoir has an exact descent property.  If `|F|>=3` and
`alpha^(u) in mathscr D(W_u)` have zero pairwise curvature, then there is
a unique

\[
                    \alpha\in\mathscr D(U),
 \qquad             \alpha|_{W_u}=\alpha^{(u)}.                    \tag{27}
\]

Indeed, the common coordinates define `alpha_i`; every rank-three edge
`ij` of `q_U` lies in some `W_u` with `u notin {i,j}`, where its signless
constraint holds.  Consequently

\[
                         \Gamma_{q_U}(\alpha)                       \tag{28}
\]

is a global blockwise-rank-at-most-two quadratic: it vanishes on every
rank-three block, and is a scalar multiple of a rank-at-most-two block on
every other edge.  This is the rigorous part of the proposed low-rank
gluing alternative.  It is a low-rank **block section**; a common physical
two-factor colour subbundle does not follow from (27)--(28).

There is also a useful sufficient negative-descent statement.  Suppose the
gauge maps `Gamma_(q_S)` are injective on every pair and triple overlap of
the deletion cover.  Then pairwise-flat classes in `mathscr Q(W_u)` glue
to a unique class in `mathscr Q(U)`.  To see this, choose representatives
`Z_u` and the unique transition weights `alpha_uv` with

\[
       Z_u-Z_v=\Gamma_{q_{uv}}(\alpha_{uv}).                         \tag{29}
\]

Injectivity on triple overlaps turns telescoping of the left side into the
ordinary cocycle equation for the `alpha_uv`.  Site by site, that scalar
cocycle on a simplex is a coboundary, so
`alpha_uv=beta_u-beta_v`.  Replacing `Z_u` by
`Z_u-Gamma(beta_u)` makes the representatives literally agree.  Since
`|F|>=3`, every block of `U` occurs in some chart and they glue.  The same
argument proves uniqueness modulo one global gauge.

Local pair-chart gauge rigidity does **not** imply this extra injectivity
after two or three more deletions.  When it fails, (29) is defined only
modulo `ker Gamma` and its triple coboundary is a kernel-valued obstruction.
Also, the map from augmented left cohomology to (22) can forget a scalar
direction when `Q_q=0`.  These are real descent obstructions, not choices
of coordinates.

## 6. The exact source transition law

The abstract curvature (25) does not yet use the blocks incident to the
third deleted vertex.  Those blocks give a stronger, literal identity.
Fix distinct `r,u,v`, put

\[
 K=B\setminus\{r,u,v\},\qquad |K|=2t-1,
\]

and decompose the chart deleting `r,u`, with `v` still internal, as

\[
 \begin{aligned}
 q_u&=q+\sum_e x_{v,e}T_e,\\
 p_c&=P_c+\sum_e a^{rv}_{ce}x_{v,e},\\
 s_d&=S_d+\sum_e a^{uv}_{de}x_{v,e}.                   \tag{30}
 \end{aligned}
\]

Every displayed direct coefficient respects the written endpoint order.
In particular, `a^(uv)_(de)` is the coefficient at colour `d` on `u` and
colour `e` on `v`; reversing the block transposes the indices.

Suppose `c != d` and the full response (13) is a boundary with primitive
\(\alpha\in\mathfrak t_{K\cup\{v\}}\).  Put
\(\beta=\alpha|_K\) and \(h=\alpha_v\).  Comparing separately the blocks
inside `K`, the blocks incident to `v`, and the scalar coordinate gives

\[
 \boxed{\begin{aligned}
 P_cS_d&=Z_q^\beta,\\
 a^{uv}_{de}P_c+a^{rv}_{ce}S_d
     &=\nabla_{\beta,h}T_e,
       \qquad (\nabla_{\beta,h}T_e)_i=(\beta_i+h)T_{e,i},\\
 a^{ru}_{cd}&=-\sum_{i\in K}\beta_i-h.
 \end{aligned}}                                                        \tag{31}
\]

This is the canonical transition law carried by the **actual source
variables**.  It needs the primitive on the full even chart, including its
`v` coordinate; a primitive restricted only to the odd common complement
does not contain enough information.

The cancellation mechanism is the following odd-site gauge identity.

**Lemma 6.1 (near-perfect gauge identity).**  For every
`beta in mathfrak t_K` and every linear element `T` on the odd set `K`,

\[
 Z_q^\beta Tq^{[t-2]}
   =\left(\left(\sum_{i\in K}\beta_i\right)T
                    -\beta\mathbin\cdot T\right)q^{[t-1]},          \tag{32}
\]

where `(beta dot T)_i=beta_i T_i`.

**Proof.**  Fix the site `i` supplied by `T` and a perfect matching of
`K\setminus{i}` supplied by `q^[t-1]`.  On the left, distinguish in turn
each matching edge as the `Z^beta` edge.  The sum of its endpoint weights
over all matching edges is `sum_K beta-beta_i`, exactly the coefficient on
the right.  This proof is coefficientwise in every endpoint colour and
uses no nonvanishing hypothesis.  \(\square\)

The target-zero triple row for colours `(c,d,e)` is

\[
 \begin{aligned}
 \Omega^{ruv}_{cde}:={}&
 (a^{ru}_{cd}T_e+a^{rv}_{ce}S_d+a^{uv}_{de}P_c)q^{[t-1]}\\
 &\quad+P_cS_dT_eq^{[t-2]}=0,\qquad(c\ne d).             \tag{33}
 \end{aligned}
\]

Substituting (31)--(32), the coefficient multiplying `q^[t-1]` is

\[
 \begin{aligned}
 &-\left(\sum\beta+h\right)T_e
   +\nabla_{\beta,h}T_e
   +\left(\sum\beta\right)T_e-\beta\mathbin\cdot T_e=0.            \tag{34}
 \end{aligned}
\]

Thus (33) is flat before multiplication: it is not merely zero modulo
`Ann(q^[t-1])`.  If the primitive is changed by `kappa in ker delta_(q_u)`,
the `v`-incident block of `Z^kappa=0` says
`nabla_(kappa|K,kappa_v)T_e=0`, so (31) is independent of the ambiguity.

The same argument with a different off-diagonal pair covers every triple
colouring which is not constant.  For example, when `c=d != e`, use the
chart deleting `r,v`.  Hence, if all relevant off-diagonal responses in
the three pair charts are boundaries, all 24 target-zero rows in the
27-row triple packet are exact flatness identities.  The three constant
colour rows retain their normalized targets and are not cohomological
flatness equations.

This is the primitive, gauge-potential version of the power-free canonical
cap connection in
[`overlapping-pair-cap-bianchi-connection.md`](overlapping-pair-cap-bianchi-connection.md).
That connection compares the cap quadratics from two charts universally;
(31) says exactly how one gauge-trivial cap lifts through the third vertex.
It therefore refines the E2 boundary branch of that identity rather than
supplying a second independent overlap equation.

## 7. Ann(q), common-restriction countermodels, and failure of transport

The common-restriction model in
[`defect-coefficient-rank-and-two-defect-sparsity.md`](defect-coefficient-rank-and-two-defect-sparsity.md)
does not contradict the transition law (31).  It retains `P,S,T,q` on `K` but omits the
`v` coordinate of the primitive and the `v`-incident equality in (31).
Its two arbitrary defect vectors therefore need not synchronize, and its
displayed residual `-6` is precisely evidence that the missing transition
law is not satisfied.  Common restrictions alone are strictly weaker than
one full even-chart boundary.

Conversely, if an argument knows only that a quadratic difference vanishes
after multiplication by a power of `q`, its representative is defined
modulo the corresponding annihilator.  The block identity in (31) can then
change by an annihilator representative even though the contracted response
does not.  This is the exact issue guarded in
[`centered-rank-one-overlap-packet-independent-audit.md`](centered-rank-one-overlap-packet-independent-audit.md):
quadratic representatives cannot be compared before multiplying by `q`.
The fork avoids that error only on the boundary branch, where (15) is a
literal equality in `R_2`, not a congruence.

There is still no map sending `alpha^(ru)_(cd)` to an
`alpha^(rv)_(ce)`.  Equation (31) sends the first primitive and the third
star to a linear combination of the first two stars; it does not solve for
the adjacent primitive, and division by a star form or a direct entry is
not legitimate.  The restriction maps (23) may also gain or lose isolated
vertices and bipartite components.  Thus zero triple residual does not by
itself identify the two E2 fibres.

On the E1 side, an extra Hessian class is only an infinitesimal response.
The exact Hamilton example in
[`source-hessian-nonintegrability-countermodel.md`](source-hessian-nonintegrability-countermodel.md)
has an extra class which is obstructed at second order.  Therefore an E1
class cannot be promoted to a global deformation, subbundle, or clean cap
without additional ternary/four-cut input.

## 8. The remaining global gate

The response fork proves the strongest unconditional local alternative:

\[
 \boxed{\text{nonzero distinguished E1 class}\quad\text{or}\quad
        \text{an E2 primitive satisfying the exact transition law (31).}} \tag{35}
\]

To turn (35) into the desired global dichotomy, one still needs the
following two assertions, neither of which follows from the current pair
or overlap identities.

1. **Synchronization-or-cap.**  In a good fan, select enough physical
   off-diagonal responses so that either their E2 primitives have zero
   curvature in (25), or a nonzero transition mismatch produces an active
   source-form dressed cap with all required normalization factors
   nonzero.  The full source law available for this step is (31), not
   equality of common restrictions.  The three constant-colour rows must
   be used to obtain activity; the 24 flat target-zero rows cannot do it.
2. **Low-rank factorization.**  If the primitives synchronize, positive
   descent gives the global blockwise-rank-at-most-two section (28).  One
   must still prove that the selected physical products factor through one
   common rank-at-most-two colour subbundle, rather than merely giving
   unrelated rank-at-most-two blocks.

A negative-side alternative additionally requires extracting a clean cap
directly from a nonzero distinguished E1 response, using complete ternary
or four-cut equations.  Integration of the Hessian class is unavailable.
In particular, (16b) does not bridge to an **active** solution of the
source-form cap equation: it places the E2 cap in the gauge-zero class, and
the remaining three normalized diagonal rows are exactly the data needed
to establish cap activity.

These are precise obstructions to global holonomy, not a failure of the
local unification.  Any continuation which simply declares overlap
restrictions equal, divides by a star, ignores the primitive's deleted
coordinate, or compares representatives modulo `Ann(q)` will bypass one of
the exact countermodels above.

## 9. Audit

The dependency-free checker
[`verify_good_pair_response_fork_and_overlap_flatness.py`](../computations/verify_good_pair_response_fork_and_overlap_flatness.py)
audits, over the integers:

* the even-site gauge identity (5);
* the odd-site identity (32) and the cancellation (34);
* the signless-incidence nullity formula for every graph on at most five
  vertices;
* the non-complex example (18)--(19); and
* the zero-sum extension used in the negative restriction map.

These checks are deliberately small matching ledgers, not an exhaustive
source search.  The substantive statements above are the coefficientwise
proofs.
