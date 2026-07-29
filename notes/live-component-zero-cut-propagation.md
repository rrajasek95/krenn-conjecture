# Live corank-two blocks form one complete component behind a zero-star cut

## 1. Outcome

Fix a deleted pair `p,q` on the row--column-basis corank-two branch.  Let
`mathscr D subset Z_0` be the four-dimensional relation space of the six
off-diagonal Hessian-kernel classes, and suppose the internal rank-three
graph `G_3(q)` is connected, spanning, and nonbipartite.  The singular
block classification proves that every live rank-three relation edge has
all four endpoint star matrices invertible.

This note gives the exact remaining propagation theorem.  If even one
rank-three edge is live, then there are

* one invertible diagonal matrix `Delta`,
* one invertible symmetric zero-diagonal matrix `H`, and
* scalars `beta_i` at the internal sites

such that, at **every** internal site and pair,

\[
                         S_i=P_i\Delta,                  \tag{1}
\]

and

\[
                  P_iHP_j^{\mathsf T}
                     =(\beta_i+\beta_j)q_{ij}.           \tag{2}
\]

Consequently the set

\[
                         U=\{i:\det P_i\ne0\}           \tag{3}
\]

has at least two vertices and induces a complete graph of live edges.
Every rank-three edge leaving `U` ends at a literal two-star-zero site:

\[
 ij\in G_3(q),\quad i\in U,\quad j\notin U
                  \quad\Longrightarrow\quad P_j=S_j=0. \tag{4}
\]

Thus separate live components do not actually survive.  All invertible
star sites merge into one complete live component, and any residual
connected rank-three graph reaches the singular part only through a
vertex cut on which both deleted stars vanish.

The dead singular edges also have a complete normal form.  After (1), an
edge `ij` is dead exactly when

\[
                              P_iHP_j^{\mathsf T}=0.     \tag{4a}
\]

Equivalently, the colour row spaces of `P_i` and `P_j` are orthogonal for
the nondegenerate form `H`.  Hence

\[
                              \operatorname {rank}P_i+
                              \operatorname {rank}P_j\le3.            \tag{4b}
\]

Apart from a zero endpoint, the only rank pairs are therefore
`(1,1),(1,2),(2,1)`, with arbitrary `H`-orthogonal row spaces of those
dimensions.  This classification is exact, not only necessary.

Connectivity and the hypothesis that every deleted-star row reaches at
least three sites do **not** remove this cut.  Section 6 gives an exact
six-site model satisfying the row--column relation geometry, the actual
off-diagonal common-power kernel equations, dense rows, and a connected
spanning nonbipartite rank-three graph, while its live triangle is
separated by three two-star-zero sites.  What fails is exactly the three
diagonal target equations.

There is one useful full-target closure.  At order eight, re-delete the
two endpoints of a putative live edge.  The mixed one-, two-, and
three-hole identities force at least five of the six outside sites to be
zero-cross witnesses.  The original deleted vertices `p,q` are two
distinct non-witnesses, because all four star matrices at the live edge
are invertible.  This is impossible.  Thus an order-eight corank-two chart
has no live internal relation edge, with no assumption on `A_pq`.

## 2. Setup

Let `W` be the even internal set.  For `c!=d`, write

\[
 K_{cd}=p_cs_d+\lambda_{cd}q,
 \qquad u_{cd}=[K_{cd}]\in E_q,
\]

and assume every two classes in a fixed row or column form a basis of the
two-space `E_q`.  Put

\[
 Z_0=\{M\in\operatorname {Mat}_3:M_{00}=M_{11}=M_{22}=0\},
\]

\[
 f(M)=\sum_{c\ne d}m_{cd}u_{cd},
 \qquad \mathscr D=\ker f.                              \tag{5}
\]

Then `dim mathscr D=4` and

\[
 \mathscr D\cap R_c=\mathscr D\cap C_d=0               \tag{6}
\]

for all directed row and column two-planes.  At an internal site let

\[
 P_i=(p_{0,i}\ p_{1,i}\ p_{2,i}),\qquad
 S_i=(s_{0,i}\ s_{1,i}\ s_{2,i}).                      \tag{7}
\]

The block of the relation represented by `M` is

\[
 \mathcal L_{ij}(M)=P_iMS_j^{\mathsf T}
                       +S_iM^{\mathsf T}P_j^{\mathsf T}.\tag{8}
\]

On a rank-three edge its image on `mathscr D` lies in the invertible line
`C q_ij`.  Call the edge live when this image is nonzero and dead when it
is zero.  The result of
[`singular-relation-block-reduction.md`](singular-relation-block-reduction.md)
will be used in its sharp form:

\[
 \text{every live edge has }P_i,S_i,P_j,S_j\text{ invertible}.       \tag{9}
\]

For `M in mathscr D`, its defining quotient relation says that there are
scalars `alpha_i(M)` of sum zero such that

\[
 \sum_{c\ne d}m_{cd}p_cs_d+\lambda(M)q=Z^{\alpha(M)},
 \qquad
 \lambda(M)=\sum_{c\ne d}m_{cd}\lambda_{cd}.            \tag{10}
\]

On block `ij`, the right side is
`(alpha_i(M)+alpha_j(M))q_ij`.

## 3. The four-plane remembers the diagonal ratio

Choose one live edge `ab`.  Normalize its two left star matrices to the
identity.  The invertible case of the local block classification gives

\[
 P_a=P_b=I,
 \qquad S_a=S_b=\Delta=\operatorname {diag}(d_0,d_1,d_2),
 \qquad d_0d_1d_2\ne0,                                  \tag{11}
\]

and

\[
 \mathscr D=T_\Delta^{-1}(\mathbb C H),
 \qquad T_\Delta(M)=M\Delta+\Delta M^{\mathsf T},        \tag{12}
\]

where `H` is invertible, symmetric, and zero diagonal.  Equality in (12),
not merely inclusion, follows because `rank T_Delta=3`: the preimage of a
line has dimension four.

The diagonal ratio in (11) is intrinsic to `mathscr D` up to a common
scalar.  Indeed, write

\[
 x_{cd}=d_dm_{cd}+d_cm_{dc}\qquad(c<d).                  \tag{13}
\]

Then (12) says that `(x_01,x_02,x_12)` lies on the line of the three
off-diagonal entries of `H`.  All three entries of `H` are nonzero,
because a symmetric zero-diagonal `3 by 3` matrix is invertible exactly
when their product is nonzero.  Hence every functional
`phi in mathscr D^perp` has, on each opposite directed pair,

\[
                         {\phi_{cd}\over\phi_{dc}}
                              ={d_d\over d_c},           \tag{14}
\]

whenever the displayed coordinates are nonzero; for every pair some
`phi` has them nonzero.  Thus the three ratios `d_d/d_c` are recovered
from `mathscr D`.

If another live edge is normalized at its endpoints, its two ratios are
one diagonal matrix `Gamma`.  Applying (14) to the same four-plane gives

\[
                              \Gamma=t\Delta             \tag{15}
\]

for a nonzero scalar `t`.  In particular every live edge has the same
three-dimensional kernel

\[
 \mathscr K:=\ker T_\Delta
       =\{N\Delta^{-1}:N^{\mathsf T}=-N\}
       \subset\mathscr D.                               \tag{16}
\]

## 4. Connectedness turns the common kernel into literal identities

Fix `M in mathscr K`.  Its physical block (8) is zero on every edge of
`G_3(q)`:

* it is zero on a dead edge by definition;
* on a live edge, normalization and (15) identify it with a nonzero
  scalar multiple of `T_Delta(M)=0`.

Equation (10) on a rank-three edge therefore gives

\[
                         \alpha_i(M)+\alpha_j(M)=\lambda(M).          \tag{17}
\]

Connectedness and an odd cycle force every `alpha_i(M)=lambda(M)/2`.
The zero-sum normalization of a vertex gauge, in characteristic zero,
then forces

\[
                         \lambda(M)=0,\qquad \alpha(M)=0.             \tag{18}
\]

Consequently the quadratic relation itself vanishes, on every internal
pair and not merely on `G_3(q)`:

\[
             \sum_{c\ne d}m_{cd}p_cs_d=0
                         \qquad(M\in\mathscr K).         \tag{19}
\]

Take the normalization (11) at the first endpoint `a` and put
`M=N Delta^{-1}` in (19).  On the block `ak`, for an arbitrary internal
site `k`, one obtains

\[
 N(\Delta^{-1}S_k^{\mathsf T}-P_k^{\mathsf T})=0
                   \qquad(N^{\mathsf T}=-N).            \tag{20}
\]

The intersection of the right kernels of all `3 by 3` skew matrices is
zero.  Applying this column by column gives

\[
                              S_k=P_k\Delta              \tag{21}
\]

for every `k`, proving (1).  Notice that this also synchronizes the scalar
in (15) across formerly separate live components.

Choose `M_0 in mathscr D` with `T_Delta(M_0)=H`, and write (10) for this
one relation.  By (21), its block response is

\[
 \mathcal L_{ij}(M_0)=P_iHP_j^{\mathsf T}.              \tag{22}
\]

Set `beta_i=alpha_i(M_0)-lambda(M_0)/2`.  Comparing blocks in (10) gives
the promised global identity

\[
                  P_iHP_j^{\mathsf T}
                     =(\beta_i+\beta_j)q_{ij}.           \tag{23}
\]

No assertion that the `beta_i` sum to zero is needed.

## 5. The complete live component and its boundary

Let `U` be (3).  The original live edge shows `|U|>=2`.  If `i,j in U`,
the left side of (23) is invertible.  Hence `beta_i+beta_j` is nonzero,
`q_ij` is invertible, and

\[
 \mathcal L_{ij}(\mathscr D)
    =\mathbb C P_iHP_j^{\mathsf T}=\mathbb Cq_{ij}.      \tag{24}
\]

Thus `ij` is live.  This proves that `U` is one complete live component.

More generally, (1) and (12) give the whole relation-line image on every
pair:

\[
 \mathcal L_{ij}(\mathscr D)
                  =\mathbb C P_iHP_j^{\mathsf T}.        \tag{24a}
\]

It is dead precisely when the displayed product is zero.  Because `H` is
nondegenerate, this says exactly that
`row(P_i) perp_H row(P_j)`.  Sylvester's rank inequality gives (4b).
Conversely any two such orthogonal row spaces, represented by arbitrary
matrices of the stated ranks, make (24a) zero; (1) then supplies the full
endpoint pairs.  This proves the dead-edge classification in (4a)--(4b).
On a rank-three edge, the factorization (23) also says that the edge is
dead exactly when `beta_i+beta_j=0`.

Now let `ij in G_3(q)` with `i in U` and `j notin U`.  If
`beta_i+beta_j` were nonzero, the two sides of (23) would have ranks less
than three and three, respectively.  Therefore `beta_i+beta_j=0`, and
(23) becomes

\[
                              P_iHP_j^{\mathsf T}=0.
\]

Since `P_iH` is invertible, `P_j=0`; (21) then gives `S_j=0`.  This proves
(4).

In graph language, if `U` is proper, its rank-three vertex boundary is
contained in

\[
                         Z=\{j:P_j=S_j=0\}.              \tag{25}
\]

Every path in `G_3(q)` from `U` to a nonzero singular-star site therefore
passes through `Z`.  Ordinary connectedness permits such a cut and does
not imply that the live subgraph spans.

There is a useful target-level footprint.  The forced incident-edge
theorem says that for every deleted endpoint and every colour `r`, some
incident aggregate block has the form `x e_r^T!=0`.  If the direct block
`A_pq` is invertible, all three anchors from `p` lie at distinct internal
sites.  At such a site

\[
                         P_i=e_r x^{\mathsf T}            \tag{26}
\]

has rank one.  By (1), the same site automatically gives the corresponding
anchor from `q`.  Hence a proper `U` is accompanied by at least three
nonzero rank-one sites and at least one distinct zero boundary site.  In
particular

\[
                         |W\setminus U|\ge4              \tag{27}
\]

when `A_pq` is invertible.  This is compatible with dense rows; it is not
a contradiction at arbitrary order.

The nine pair equations themselves now have the single-star form

\[
 d_d\,\mathcal H_q(p_cp_d)+a_{cd}Q
                       =\delta_{cd}X_c.                 \tag{27a}
\]

Thus the six off-diagonal equations say that the three symmetric products
`p_0p_1,p_0p_2,p_1p_2` all have Hessian response on `C Q`.  If `Q!=0`,
comparison of the two orientations gives

\[
                         {a_{cd}\over d_d}
                           ={a_{dc}\over d_c}\qquad(c\ne d),          \tag{27b}
\]

or equivalently

\[
                         A_{pq}\Delta^{-1}
                              \text{ is symmetric}.       \tag{27c}
\]

The diagonal equations are the remaining nonhomogeneous conditions.  The
countermodel below shows that neither (27a) off diagonal nor (27b), even
together with the complete relation geometry, can replace those three
diagonal equations.

## 6. Sharp connected dense countermodel below the diagonal equations

The zero cut in (25) is genuine at the complete relation/Hessian-kernel
level.  Take six internal sites, split as

\[
                         U=\{0,1,2\},\qquad Z=\{3,4,5\},
\]

and set

\[
 \Delta=\operatorname {diag}(2,3,5),\qquad
 H=\begin{pmatrix}0&1&2\\1&0&3\\2&3&0\end{pmatrix}.   \tag{28}
\]

Put

\[
 P_i=I,\ S_i=\Delta\quad(i\in U),
 \qquad P_z=S_z=0\quad(z\in Z),                         \tag{29}
\]

and define the internal blocks by

\[
 q_{ij}=\begin{cases}
 H/2,&i,j\in U,\\
 H,&|\{i,j\}\cap U|=1,\\
 0,&i,j\in Z.
 \end{cases}                                            \tag{30}
\]

The rank-three graph is the join of a triangle and an independent
three-set.  It is connected, spanning, and nonbipartite.  Every one of the
six star rows in (29) reaches exactly three sites.

Let

\[
 \mathscr D=T_\Delta^{-1}(\mathbb C H).
\]

It has dimension four and satisfies all six avoidance conditions (6).
For `M in mathscr D`, write `T_Delta(M)=tH` and take the vertex-gauge
parameters

\[
                 (\alpha_0,\ldots,\alpha_5)
                         =(t,t,t,-t,-t,-t).              \tag{31}
\]

They sum to zero, and direct block comparison gives

\[
             \sum_{c\ne d}m_{cd}p_cs_d=Z^\alpha.        \tag{32}
\]

Conversely, inspection on an edge inside `U` shows that a combination of
the six off-diagonal products is a vertex gauge only if
`T_Delta(M) in C H`.  Thus `mathscr D` is the **exact** four-dimensional
relation space of these six classes modulo gauges, not merely a selected
subspace.  Row--column avoidance gives the basis property.

Moreover every `p_cs_d` is supported on pairs inside `U`.  After choosing
such a marked pair, the remaining sites consist of one vertex of `U` and
three vertices of `Z`.  Since all `Z-Z` blocks in (30) vanish, they admit
no perfect matching.  Therefore

\[
                         \mathcal H_q(p_cs_d)=0           \tag{33}
\]

for all `c,d`.  In particular the six off-diagonal products are actual
Hessian-kernel vectors and satisfy all six off-diagonal pair equations
with zero direct coefficients.

The three diagonal equations expose the failure exactly.  Their Hessian
terms also vanish by (33), so they would require

\[
                         a_{cc}Q=X_c\qquad(c=0,1,2),     \tag{34}
\]

putting three independent pure tensors on one line.  This is impossible.
The model may also have excess Hessian directions beyond the distinguished
two-space; it is asserted as a sharp countermodel to propagation from
connectivity, density, and the complete off-diagonal relation system, not
as a full target realization.

## 7. The five-witness theorem is uniform in the order

We first record a size point which is obscured by the names of the existing
order-eight notes.

**Lemma 7.1 (uniform five-witness theorem).**  In an exact ternary target
identity of any even order, let `A_ab` be invertible and put

\[
 C_{x,r}^{ab}=A_{ax}K_rA_{bx}^{\mathsf T},\qquad
 \Omega_{ab}=\{x:C_{x,r}^{ab}=0\text{ for some }r\}.    \tag{35}
\]

Provided there are at least five outside sites,

\[
                              |\Omega_{ab}|\ge5.          \tag{36}
\]

**Proof.**  The arguments of
[`n8-minimal-witness-union-obstruction.md`](n8-minimal-witness-union-obstruction.md)
and
[`n8-hard-annihilator-union-four.md`](n8-hard-annihilator-union-four.md)
do not use that the set outside `a,b` has cardinality six; they use only
that all sites outside a proposed three- or four-site witness union can be
contracted by their cross-product covectors.  Here is the exact audit of
that extension.

Work on the irreducible incidence hypersurface

\[
                         g=\alpha^{\mathsf T}A_{ab}\beta=0.           \tag{37}
\]

At a nonwitness site `z`, every coordinate of

\[
 \gamma_z=(\alpha^{\mathsf T}A_{az})
                  \mathbin\times(\beta^{\mathsf T}A_{bz})            \tag{38}
\]

is nonzero in the domain `C[alpha,beta]/(g)`.  Contracting any additional
nonwitness sites by these `gamma_z` therefore does two things only:

1. it kills every matching which sends `a` or `b` to one of those sites;
2. it multiplies each constant target coefficient by a nonzero factor.

If the witness union had three sites, leave those three open and contract
all the others.  The three-hole equation is exactly equation (9) of the
first cited note, with its residual vector now the contraction of a larger
even cofactor.  That vector is still common to the two reversed star
assignments.  The constant word has one source and makes one of its
coordinates nonzero; reversing the assignments gives a nonconstant word
with the same coordinate as its unique source.  This is the same
contradiction, so the union has size at least four.

If the witness union had four sites, the hard-capacity enumeration is
unchanged: every additional site has empty witness mask and hard capacity
zero.  In the nine determinant cases, contract all sites except the same
two holes; the added nonwitness factors are nonzero and are absorbed into
the scalar `t_r`.  In the two independent-monomial cases, they are
likewise absorbed into the two nonzero coefficients.  In the final anchor
rectangle, leave the same four witness sites open and contract every
nonwitness site.  The resulting four-site tensor is still a diagonal with
three nonzero coefficients, and every surviving matching sends `a,b` to
two of the four open sites.  The one-slice anchors and the exact two-hole
anchor-rectangle alternative are therefore literally unchanged.  The
twelve-pattern audit and all three contradictions from the second cited
note apply verbatim.  Thus a four-site union is impossible, proving (36).
`QED`

This uniformization introduces no limiting or generic argument: all
nonzero statements are in the function field of (37), and the extra
contractions are exact matching expansions.

## 8. Re-deleting a live edge

Return to the live corank-two chart and suppose the data come from a full
target identity.  Choose `i,j in U`.  The edge `A_ij=q_ij` is invertible,
so Lemma 7.1 applies.  None of the following outside sites is a witness:

* the original deleted vertices `p,q`, because
  \[
  C_{p,r}^{ij}=P_iK_rP_j^{\mathsf T},\qquad
  C_{q,r}^{ij}=S_iK_rS_j^{\mathsf T};                   \tag{39}
  \]
* any `k in U\setminus\{i,j\}`, because both `q_ik` and `q_jk` are
  invertible.

In every case the cross matrix has rank two.  Hence all five witnesses
forced by Lemma 7.1 lie in the original singular-star complement:

\[
                              \Omega_{ij}\subseteq W\setminus U,
 \qquad                         |W\setminus U|\ge5.       \tag{40}
\]

This is the uniform full-target footprint of a live component.

At order eight, `|W|=6` while `|U|>=2`, so (40) is impossible.  We have
proved:

**Corollary 8.1 (order-eight live-edge closure).**  In an exact
order-eight target identity, a deleted-pair chart satisfying the
row--column-basis corank-two hypotheses and connected spanning
nonbipartite internal rank-three graph has no live internal relation edge.

At larger order, (40) is sharp at the level of witness counts: five
singular sites can carry the five-site hard-incidence patterns classified
in the cited notes.  The complete live set `U` is still separated from
them in `G_3(q)` by literal two-star-zero vertices.  Thus arbitrary-order
closure requires the values in the diagonal equations (27a), not another
count of zero-cross witnesses.

## 9. What the diagonal equations add on a singular direct edge

This section records the exact information which is genuinely new in the
three diagonal equations.  It also rules out a tempting but false shortcut:
the diagonal products do not collapse modulo the off-diagonal products at
the quadratic level.

### 9.1 The internal top power cannot vanish

First, the live branch itself forces

\[
                              Q\ne0.                     \tag{41}
\]

Indeed, suppose `Q=0` and define

\[
 \mathcal B(M)=\sum_{c\ne d}m_{cd}p_cs_d,
 \qquad
 w:Z_0\longrightarrow E_q,\quad M\longmapsto[\mathcal B(M)].       \tag{42}
\]

All six products in (42) lie in `ker mathcal H_q` by the off-diagonal
instances of (27a).  If `M in ker w`, then `mathcal B(M)` is a vertex
gauge.  On the normalized live edge `ab`, its block is
`T_Delta(M)`, while a gauge block is a scalar multiple of `q_ab` and hence
of `H`.  Thus

\[
                              \ker w\subseteq\mathscr D.             \tag{43}
\]

The codomain has dimension two and `dim mathscr D=4`.  Relation (43)
therefore forces `rank w=2` and `ker w=mathscr D`.

On the other hand, `Q=0` and Euler's identity give
`mathcal H_q(q)=0`, so `[q] in E_q`.  This class is nonzero.  If
`q=Z^alpha` were a gauge, then on every edge of `G_3(q)` one would have
`alpha_i+alpha_j=1`.  Connectedness and an odd cycle force all
`alpha_i=1/2`, contradicting the zero-sum gauge normalization.  Since
`w` is onto, choose `M` with `[mathcal B(M)]=[q]`.  Comparing
`mathcal B(M)-q=Z^alpha` on `ab` again gives
`T_Delta(M) in C H`, hence `M in mathscr D=ker w`; this contradicts
`w(M)=[q]!=0`.  This proves (41).

### 9.2 Polarization along the kernel of the direct block

Put

\[
                         B=A_{pq}\Delta^{-1}.            \tag{44}
\]

Because of (41), comparison of the two orientations of every off-diagonal
equation in (27a) proves that `B` is symmetric.  For
`x,z in C^3`, write `p(x)=sum_c x_c p_c`.  Multiplying the `(c,d)`
equation by `x_cz_d/d_d` and summing gives the full polarized identity

\[
 \boxed{
 \mathcal H_q\bigl(p(x)p(z)\bigr)+x^{\mathsf T}Bz\,Q
       =\sum_{c=0}^2{x_cz_c\over d_c}X_c.}               \tag{45}
\]

Suppose now that the direct block is singular and let
`0!=v in K:=ker B`.  Symmetry of `B` turns (45) into

\[
 \boxed{
 \mathcal H_q\bigl(p(v)p(z)\bigr)
       =\sum_{c=0}^2{v_cz_c\over d_c}X_c
       \quad\hbox{for every }z.}                         \tag{46}
\]

In particular, for every coordinate in the support of `v`,

\[
             \mathcal H_q\bigl(p(v)p_c\bigr)
                         ={v_c\over d_c}X_c\ne0.         \tag{47}
\]

This polarized family is strictly stronger than the single square identity
obtained by putting `z=v`.

There is a useful common-centre consequence.  Write `|W|=2r`, put
`t_i=P_iv`, and let `q_{\widehat i}` and `p_{c,\widehat i}` denote the
restrictions obtained by deleting site `i`.  Grouping (47) by the endpoint
occupied by `p(v)` gives the exact slice decomposition

\[
 {v_c\over d_c}X_c
   =\sum_{i\in W}t_i^{(i)}\otimes R_{i,c},
 \qquad
 R_{i,c}={p_{c,\widehat i}q_{\widehat i}^{r-1}
                         \over(r-1)!}.                   \tag{48}
\]

For `v_c!=0`, omit the zero `R_(i,c)` and contract every retained site by
an arbitrary covector annihilating `t_i`.  The right side vanishes.  The
left side is one nonzero pure tensor, so the product of its restricted
coordinate functionals can vanish identically only when one factor does.
Consequently there is a retained site `i_c` with

\[
                         P_{i_c}v\in\mathbb C^*e_c.       \tag{49}
\]

The sites obtained for different coordinates in `supp(v)` are distinct.

The same statement uniformizes over the whole kernel.  If the coordinate
functional `v mapsto v_c` is nonzero on `K`, the dense open set
`{v in K:v_c!=0}` is covered by the finitely many linear conditions

\[
                         P_iv\in\mathbb C e_c
 \qquad(R_{i,c}\ne0).                                   \tag{50}
\]

A vector space over `C` is not a finite union of proper linear subspaces.
After discarding maps which vanish on `K`, some one site therefore obeys

\[
                 0\ne P_i(K)\subseteq\mathbb C e_c,
                 \qquad R_{i,c}\ne0.                    \tag{51}
\]

If `kappa=dim K=3-rank B`, this gives at least `kappa` distinct sites,
and at each selected site

\[
                         \operatorname {rank}P_i\le4-\kappa.        \tag{52}
\]

Thus for `rank B<=1` all these common-centre sites lie outside the live
set `U`; when `B=0` their matrices have rank one.

When `kappa>=2`, these sites are also literal zero-cross witnesses.  In
the original deleted chart,

\[
 C_{i,c}^{pq}=A_{pi}K_cA_{qi}^{\mathsf T}
             =P_i^{\mathsf T}K_cP_i\Delta.              \tag{53}
\]

For a site in (51)--(52), either `rank P_i=1`, or its image is a plane
containing the kernel line `C e_c` of the alternating form `K_c`.
In both cases `P_i^T K_cP_i=0`.

The singular-edge factor witnesses of
[`two-vertex-annihilation-identities.md`](two-vertex-annihilation-identities.md)
sharpen in the same way.  If `rank B=2`, a proportionality
`C_(i,c)^(pq) in C A_pq` becomes, after multiplying by `Delta^-1`, a
matrix which is both skew-symmetric and proportional to the nonzero
symmetric matrix `B`; it must be zero.  If `rank B=1`, write
`B=uu^T` after a scalar rescaling.  The two factor-witness alternatives
become rank-at-most-one skew matrices `u d^T` or `d u^T`, and hence are
again zero.  Therefore the one- and two-hole theorems give the following
literal witness counts:

* for `rank B=2`, every colour has at least two zero-cross witnesses, and
  their union has at least three sites;
* for `rank B=1`, every colour `c` for which `u` is not proportional to
  `e_c` has at least two zero-cross witnesses; if `u` is noncoordinate,
  their union has at least three sites;
* for `B=0`, every colour has at least two zero-cross witnesses, and their
  union has at least three sites.

All these witnesses lie outside `U`, since (53) has rank two when `P_i`
is invertible.  They are compatible with the stronger uncoloured bound
`|W\setminus U|>=5` in (40): one rank-one site can witness all three
colours, so the colourwise counts do not add.

### 9.3 Why local product geometry cannot close the branch

After left-right multiplication by `P_a^{-1},P_b^{-T}` at a live edge
`ab`, the blocks of the six symmetric quadratic products are

\[
 (p_c^2)_{ab}=2E_{cc},qquad
 (p_cp_d)_{ab}=E_{cd}+E_{dc}\quad(c<d).                  \tag{54}
\]

They form a basis of `Sym^2 C^3`.  In particular the six global products
are linearly independent, and the three square classes remain
three-dimensional modulo the span of the three off-diagonal products.
There is therefore no quadratic/local argument which forces the full
product span modulo the off-diagonal part to have dimension at most one.

The target equations point in the opposite direction.  Define

\[
 \overline\Phi:\operatorname {Sym}^2\mathbb C^3
       \longrightarrow (\text{top support})/\mathbb C Q,
 \qquad
 u\mathbin\odot z\longmapsto
       [\mathcal H_q(p(u)p(z))].                         \tag{55}
\]

The off-diagonal three-space lies in `ker overline Phi`, while the diagonal
equations give

\[
                         d_c\overline\Phi(e_c^2)=[X_c].  \tag{56}
\]

Since `X_0,X_1,X_2` are independent and `C Q` has dimension one, their
images in the quotient span a space of dimension at least two.  Hence

\[
                         \operatorname {rank}\overline\Phi\ge2.     \tag{57}
\]

Any arbitrary-order contradiction must therefore show, using the actual
common power `q^(r-1)` and the zero-cut geometry, that this rank is at most
one.  Equations (46)--(53) are the exact surviving constraints supplied by
a singular direct block; witness counts and local product spans alone do
not give that upper bound.

### 9.4 The equality-five incidence boundary really survives the anchors

The sharp case `B=0` shows that (51) cannot be combined with (40) by a
bare count.  Here `K=C^3`, so (51)--(52) give three distinct sites
`z_0,z_1,z_2` with

\[
                         \operatorname {im}P_{z_c}=\mathbb C e_c.   \tag{58}
\]

For a re-deleted live pair, both incident matrices at `z_c` have their
`z_c`-side image on `C e_c`.  Thus `z_c` has the triple zero-cross mask
and its common annihilator plane is `e_c^perp`: it is hard for precisely
colour `c`.

Intersect this requirement with the exact equality-five audit of
[`n8-witness-union-five-stages.md`](n8-witness-union-five-stages.md).
Encode a witness mask by the sum of `2^c` over its colours, so `7` is a
triple site.  Among the thirteen residual mask orbits and their thirty-six
hard assignments, requiring three triple sites hard in the three distinct
colours leaves exactly

\[
 \boxed{
 (0,1,6,7,7,7),\qquad
 (0,3,5,7,7,7),\qquad
 (0,3,7,7,7,7)}.                                      \tag{59}
\]

The respective numbers of surviving labelled hard assignments are
`6,6,12`.  This is an incidence statement, not an assertion that the
three rows extend to a matching tensor.  It proves sharply that even the
largest kernel `B=0`, all three common-centre anchors, and the uniform
five-witness theorem do not force a sixth witness.  Any closure must use
the actual residual cofactor values.

## 10. Exact audit

[`verify_live_component_zero_cut_propagation.py`](../computations/verify_live_component_zero_cut_propagation.py)
checks over the rationals:

1. `dim mathscr D=4`, row--column avoidance, and the three-dimensional
   common kernel in (16);
2. recovery of the opposite-coordinate ratios (14);
3. the two elementary full-rank coefficient maps used in (20) and the
   boundary implication;
4. every block identity in the six-site model (28)--(32);
5. connectedness, spanning, nonbipartiteness, and exact three-site row
   density in that model; and
6. the matching-support vanishing (33), together with an explicit
   nonzero coefficient of `Q`; and
7. the six-dimensional local product span in (54), and the elementary
   alternating-form witness calculations used after (53); and
8. the exact three-orbit equality-five filter in (59).

The checker audits the coordinate algebra.  The gauge, graph, common-power,
and mixed-witness implications are proved above.
