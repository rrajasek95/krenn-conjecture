# Spanning E2 responses evacuate every visible block

## 1. Outcome

The inactive-edge gap left by
[`synchronized-e2-factorization-and-inactive-edge-boundary.md`](synchronized-e2-factorization-and-inactive-edge-boundary.md)
has a coordinate-free multiresponse reduction.

Let `q` be the internal quadratic of a gauge-rigid good-pair chart, let

\[
                         D=\ker B_3(q),                              \tag{1}
\]

and suppose synchronized E2 primitives spanning `D` have responses through
the same sitewise planes `L_i`, `dim L_i<=2`.  Then every source block
visible to at least one defect already lies in those planes.  The only
uncontrolled pairs form the **universal inactive core**

\[
 K(D)=\{ij:\alpha_i+\alpha_j=0\text{ for every }\alpha\in D\}.    \tag{2}
\]

It has an exact component-free description:

* all vertices in nonbipartite rank-three components form one clique;
* each bipartite rank-three component contributes the complete bipartite
  graph between its two shores; and
* isolated rank-three vertices have no incident core pair.

The physical equations sharpen this.  Fix one selected response
`p_a s_b`, `a!=b`, whose dense factorization defines
`L_i=span{p_(a,i),s_(b,i)}`.  If `p_a` reaches at least two sites, then
either one physical deleted-star row reaches at most one site, or **all six
physical rows lie in the planes**.  In the latter branch the three exact
diagonal identities force three vertex sets, each saturable by a matching
of `K(D)`, to cover the whole chart.

Consequently, in this nonsparse multiresponse branch:

1. `G_3(q)` has no isolated vertex;
2. every nontrivial bipartite component with shore orders `r,s` satisfies
   `r<=3s` and `s<=3r`; and
3. a component `K_(1,k)` has `k<=3`.  At equality, its three leaf planes
   are the three distinct target coordinate planes, and exact target
   contraction forces a different coordinate anchor through each of the
   three rank-three blocks.

This is not yet the full synchronization-or-cap theorem.  Balanced
bipartite cores and the clique made from nonbipartite components can have
a three-matching saturation cover, so the diagonal equations do not force
their transverse blocks into `L`.  The exact remaining boundary is now
smaller: exclude those cores (or export a clean cap), and exclude the
anchored ternary claw at the rank-three-degree-three equality.  No graph
case enumeration is used below.

## 2. Defect visibility and the universal core

Let `W` be the even internal site set and work in

\[
 {\cal R}(W)=\bigotimes_{i\in W}(\mathbb C\oplus V_i),
 \qquad V_iV_i=0.                                             \tag{3}
\]

Write `G_3(q)` for the graph of rank-three blocks.  Its signless incidence
kernel is

\[
 D=\{\alpha\in\mathbb C^W:\alpha_i+\alpha_j=0
                                  \ (ij\in E(G_3(q)))\}.          \tag{4}
\]

For subspaces `L_i subset V_i`, put

\[
 {\cal L}_1=\bigoplus_iL_i,
 \qquad
 {\cal L}_2=\bigoplus_{i<j}L_i\otimes L_j.                       \tag{5}
\]

The gauge response is

\[
             \Gamma_q(\alpha)_{ij}=(\alpha_i+\alpha_j)q_{ij}.    \tag{6}
\]

**Lemma 2.1 (multiresponse evacuation).**  Suppose vectors
`alpha^(1),...,alpha^(d)` span `D` and

\[
                       \Gamma_q(\alpha^{(h)})\in{\cal L}_2
                       \qquad(1\le h\le d).                       \tag{7}
\]

Then

\[
                   ij\notin K(D)\quad\Longrightarrow\quad
                   q_{ij}\in L_i\otimes L_j.                     \tag{8}
\]

**Proof.**  By linearity, (7) holds for every `alpha in D`.  If
`ij notin K(D)`, choose `alpha` with `alpha_i+alpha_j!=0`.  The `ij`
block of (7), divided by that nonzero scalar, is (8).  No block entry or
minor is divided by.  \(\square\)

The promised description of (2) is equally direct.

**Lemma 2.2 (core classification).**  Let `N` be the union of the vertex
sets of all nonbipartite components of `G_3(q)`.  For every nontrivial
bipartite component `C`, choose shores `C^+,C^-`.  Then

\[
 K(D)=\binom N2\ \mathbin{\dot\cup}
             \bigdotcup_{C\ \mathrm{bipartite}} C^+\times C^-.  \tag{9}
\]

In particular, no pair incident with an isolated vertex lies in `K(D)`.

**Proof.**  A vector in `D` is zero on every nonbipartite component, is
`t_C` on one shore and `-t_C` on the other shore of a bipartite component,
and has one free coordinate at every isolated vertex.  All these parameters
are independent.  A pair evaluation `alpha_i+alpha_j` therefore vanishes
identically exactly in the two cases displayed in (9).  \(\square\)

Thus the uncontrolled graph is not the inactive graph of one chosen
primitive.  It is the intersection of the inactive graphs of the whole
defect space.  Passing from one response to a spanning family removes all
cross-component pairs and all same-shore pairs at once.

## 3. Literal physical products capture the six star rows

We first record the small linear fact which makes physical provenance
matter.

**Lemma 3.1 (a planar factor captures its partner).**  Let
`x in cal L_1` reach at least two sites.  If `xy in cal L_2`, then
`y in cal L_1`.

**Proof.**  Fix a site `j` and choose `i!=j` with `x_i!=0`.  Apply the
quotient `V_j -> V_j/L_j` to the `ij` block

\[
                         x_i\otimes y_j+y_i\otimes x_j.            \tag{10}
\]

The second summand dies because `x_j in L_j`, while the whole block dies
because it lies in `L_i tensor L_j`.  Hence
`x_i tensor (y_j mod L_j)=0`, so `y_j in L_j`.  This works for every
`j`.  \(\square\)

Now assume the exact pair equations on `|W|=2t` sites:

\[
 a_{cd}q^{[t]}+p_cs_dq^{[t-1]}=\delta_{cd}X_c^W,
 \qquad 0\le c,d\le2.                                           \tag{11}
\]

Gauge rigidity implies that for every `c!=d` there is
`alpha^(cd) in D` with

\[
                         p_cs_d=\Gamma_q(\alpha^{cd}).             \tag{12}
\]

Indeed, the mixed equation and
`q q^[t-1]=t q^[t]` first put
`p_cs_d+(a_cd/t)q` in the zero-sum gauge kernel; subtracting the constant
gauge gives (12), with `sum alpha^(cd)=-a_cd`.  Rank three of `q_ij`
and rank at most two of the product block then put the primitive in (4).

**Theorem 3.2 (physical-row capture or one-site sparsity).**  Assume the
hypotheses of Lemma 2.1 and the exact gauge-rigid equations (11).  Choose
`a!=b`, let `h` be the third colour, and suppose

\[
 p_a\in{\cal L}_1,qquad s_b\in{\cal L}_1,qquad
 |\operatorname {supp}_s(p_a)|\ge2.                              \tag{13}
\]

Then either one of `s_b,p_h,s_h` has site support at most one, or

\[
                         p_0,p_1,p_2,s_0,s_1,s_2
                                      \in{\cal L}_1.              \tag{14}
\]

In particular, (13) holds for the planes produced by a dense synchronized
factorization `Gamma_q(alpha)=p_a s_b`.

**Proof.**  Equations (7), (12), and spanning of `D` put every mixed
product `p_c s_d`, `c!=d`, in `cal L_2`.  Apply Lemma 3.1 successively:

1. `p_a s_b` and `p_a s_h` put `s_b,s_h` in `cal L_1`;
2. if `s_b` reaches two sites, `p_h s_b` puts `p_h` in `cal L_1`;
3. if `p_h` reaches two sites, `p_h s_a` puts `s_a` in `cal L_1`; and
4. if `s_h` reaches two sites, `p_b s_h` puts `p_b` in `cal L_1`.

If one of the three stated support conditions fails, the sparse
alternative holds.  Otherwise these four steps give all six rows in
(14).  \(\square\)

There is also a useful zero-propagation statement for the selected
factor.  On every rank-three edge its block is zero.  If `P_i,S_i` are
nonzero around an odd cycle, simple-tensor uniqueness gives
`S_i=lambda_iP_i` with `lambda_i=-lambda_j` across each edge, which is
impossible around that cycle.  Hence

\[
 \{i:P_i=0\text{ or }S_i=0\}
       \quad\hbox{meets every odd cycle of }G_3(q).                 \tag{15}
\]

In particular, if both selected rows are nonzero at every rank-three
vertex, all rank-three components are bipartite and the clique term in
(9) disappears.

## 4. Exact diagonal contraction gives a saturation cover

Assume the nonsparse conclusion (14).  Define the target-transverse sets

\[
             M_c=\{i\in W:e_c^{(i)}\notin L_i\},
             \qquad c=0,1,2.                                    \tag{16}
\]

A set of vertices is **saturable** in a graph if some matching is incident
with every vertex of the set; the matching may also use vertices outside
the set.

**Theorem 4.1 (ternary inactive-core cover).**  Each `M_c` is saturable
by a matching of `K(D)`, and

\[
                              W=M_0\cup M_1\cup M_2.               \tag{17}
\]

**Proof.**  For `i in M_c`, apply `V_i -> V_i/L_i` to the diagonal
identity in (11), and apply the identity at all other sites.  Its right
side remains a nonzero pure tensor by the definition of `M_c`.

Expand the nonzero left side into its direct-edge and two-star matching
layers.  In the two-star layer, neither star row can occupy a site of
`M_c`, because all six rows lie in `cal L_1`.  Thus in either layer every
site of `M_c` is covered by a `q`-edge.  If such an edge were outside
`K(D)`, Lemma 2.1 would put its block in `L_i tensor L_j`, and the quotient
at its endpoint in `M_c` would kill the term.  Since the projected sum is
nonzero, at least one surviving matching term exists.  Its `q`-edges
incident with `M_c` are core edges and form a matching saturating `M_c`.

At each site the three target vectors are independent while `dim L_i<=2`.
At least one target vector is absent from `L_i`, which is exactly (17).
\(\square\)

This argument uses the normalized coefficient one in every diagonal row.
It never selects a term from a zero coefficient: a term is selected only
after the projected tensor is known to be nonzero.

## 5. Component consequences and the sharp claw

The saturation-cover number of the graph in (9) is elementary.  A subset
meeting the two shores of `K_(r,s)` in `x,y` vertices is saturable exactly
when

\[
                              x\le s,qquad y\le r.                 \tag{18}
\]

Necessity follows because the selected vertices need distinct opposite
mates.  For sufficiency, use `k` selected-to-selected edges, where
`k=max(0,x+y-r,x+y-s)`, and match the remaining selected vertices to
unselected opposite-shore vertices.  The bounds in (18), together with
`x<=r,y<=s`, give `k<=min(x,y)`, so this construction is valid.
Consequently

\[
 \operatorname {satcov}(K_{r,s})
       =\left\lceil{\max(r,s)\over\min(r,s)}\right\rceil.          \tag{19}
\]

A clique of even order has saturation-cover number one; a clique of odd
order at least three has number two.  Saturation-cover number of a disjoint
union is the maximum of the component numbers.  An isolated vertex has
infinite saturation-cover number.

Combining (9), (17), and (19) proves the three consequences stated in
Section 1.  Explicitly, if `C^+,C^-` have orders `r,s`, then

\[
 r\le\sum_{c=0}^2|M_c\cap C^+|\le3s,
 \qquad
 s\le\sum_{c=0}^2|M_c\cap C^-|\le3r.                            \tag{20}
\]

There is a rigid equality case which is useful for the next cap step.

**Corollary 5.1 (anchored ternary claw).**  Suppose a bipartite
rank-three component has shores `{v}` and
`{u_0,u_1,u_2}`.  In the nonsparse branch, after relabelling the leaves,

\[
                     L_{u_c}=\operatorname {span}
                   \{e_d^{(u_c)}:d\ne c\}.                       \tag{21}
\]

Let `pi_(u_c):V_(u_c)->V_(u_c)/L_(u_c)`.  Then

\[
 (\operatorname{id}\otimes\pi_{u_c})(q_{v u_c})
       \in \mathbb C^*e_c^{(v)}\otimes\pi_{u_c}(e_c^{(u_c)}).
                                                                        \tag{22}
\]

**Proof.**  A saturable subset of the three-leaf shore contains at most
one leaf.  Three such sets cover all three leaves only if their leaf parts
are three distinct singletons.  This proves (21), since each leaf plane
contains the other two independent target axes and omits the assigned one.

Project the colour-`c` diagonal equation only at `u_c`.  Every physical
star row is killed if it occupies that leaf.  Every `q`-block from `u_c`
to a vertex other than `v` is outside `K(D)`, hence lies in the two planes
and is also killed.  Therefore every surviving term uses the one block
`q_(v u_c)`.  Since the quotient at `u_c` is one-dimensional, the entire
projected left side has its `v`-factor in the line obtained from that
block.  The projected right side is nonzero and has `v`-factor
`e_c^(v)`.  This proves the nonzero line identity (22).  \(\square\)

Thus a one-versus-many component either has rank-three degree at most two,
or is the single sharply described degree-three claw.  The latter is not
an anonymous graph exception: its three transverse rank-three columns are
the three target coordinate anchors at the centre.

## 6. Exact remaining gate

The multiresponse theorem closes the broad “all inactive edges are
uncontrolled” gap.  Only `K(D)` survives, and its ability to carry the
diagonal targets is measured exactly by

\[
                         \operatorname {satcov}(K(D))\le3.         \tag{23}
\]

Hence any independent source theorem proving
`satcov(K(D))>=4` closes the nonsparse synchronized branch immediately.
Equivalently, it is enough to exclude the bipartite cores whose shore ratio
is at most three, the nonbipartite clique core, and the anchored claw (22),
or to turn one of them into an active clean cap.  A one-response argument
cannot obtain this:
it sees one inactive graph rather than the intersection (2).

There is one important quantifier boundary.  The
[`defect-coefficient rank theorem`](defect-coefficient-rank-and-two-defect-sparsity.md)
already proves that, on a **single dense defect-three chart**, its six
physical off-diagonal primitives span `D`.  What is not yet known is that
three independent directions can be synchronized through the fan and made
to factor through the **same** global planes `L_i`.  The earlier dense
factorization theorem supplies those planes for one synchronized direction.
Thus “spans `D` inside one common synchronized subbundle” remains a
conditional hypothesis here, rather than an established property of every
dense defect-three fan chart.

The lightweight checker
[`verify_multiresponse_inactive_core_evacuation.py`](../computations/verify_multiresponse_inactive_core_evacuation.py)
audits the core formula from exact signless kernels, the saturation
criterion and cover number, the `K_(1,3)` equality pattern, and the three
coordinate quotient anchors.  The general statements are the linear and
matching arguments above, not finite graph enumeration.
