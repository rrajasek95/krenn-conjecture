# The non-clean pair-catalecticant branch and a connected zero-block theorem

## 1. Outcome

There is an exact structural obstruction in the non-clean branch of the
nine pair caps.  Suppose the internal Hessian is gauge-rigid and the three
pure targets have quadratic lifts supported on a physical graph `G` which
also supports `q`.  Then every one of the nine polarized star products is
supported on `G`.  On the complementary graph `F`, all product blocks
vanish.

If the vertices reached by at least one of the two deleted stars induce a
connected subgraph of `F`, the cap equations are impossible.  The reason
is entirely site-graded: mutually annihilating site subspaces are either
all pure toward one deleted endpoint, or form a one-dimensional alternating
family on a bipartite graph.  In the first case the cap/output flattening
has rank at most one; in the second it has rank at most two.  The ternary
diagonal target has rank three.

Consequently a hypothetical solution in this chart must make the
two-star-active subgraph of `F` disconnected.  In particular, if `F` is
`k`-vertex-connected, at least `k` internal sites are simultaneously
invisible to both deleted stars.  This is a precise sparse-star escape,
not an abstract level-algebra artifact.

An exact six-site core shows why the hoped-for stronger bridge to clean
exposure cannot follow from Hessian data alone.  It is maximally
gauge-rigid, every active cell has nonzero cofactor, all three pure targets
have supported one-cell lifts, no pair cofactor has ternary rank, and yet
there is no clean exposed edge.  The factorized nine-cap equations are
therefore essential.  The connected zero-block theorem uses exactly that
factorization and forces at least two two-star-inactive sites in this
boundary core.

## 2. Pair-cap and gauge notation

Let `W` have `N=2r` sites and put

\[
 \mathcal R_W=\bigotimes_{i\in W}(\mathbb C\oplus V_i),
 \qquad V_iV_i=0.
\]

For an internal quadratic `q`, define

\[
 Q={q^r\over r!},\qquad
 \mathcal H_q(Z)={Zq^{r-1}\over(r-1)!}.                  \tag{1}
\]

The normalized two-deletion equations are

\[
 \boxed{\quad
 \mathcal H_q(p_cs_d)+a_{cd}Q=\delta_{cd}X_c,
 \qquad 0\le c,d\le2.
 \quad}                                                   \tag{2}
\]

The unavoidable gauge kernel is

\[
 \mathcal G_q=
 \left\{Z^\alpha:(Z^\alpha)_{ij}=(\alpha_i+\alpha_j)q_{ij},
                         \ \sum_i\alpha_i=0\right\}.     \tag{3}
\]

Call `q` gauge-rigid when `ker H_q=G_q`.

## 3. Supported lifts force zero product blocks

Let `G` be a graph on `W`.  A quadratic is **supported on `G`** if all its
blocks outside `G` vanish.

**Lemma 3.1 (supported-product lemma).**  Suppose `q` is gauge-rigid and
supported on `G`.  Suppose there are quadratics `T_c`, also supported on
`G`, such that

\[
                         \mathcal H_q(T_c)=X_c.           \tag{4}
\]

Then every solution of (2) satisfies

\[
                         p_cs_d\text{ is supported on }G
                         \quad(0\le c,d\le2).             \tag{5}
\]

**Proof.**  Since `H_q(q)=rQ`, equations (2) give

\[
 p_cs_d+{a_{cd}\over r}q-\delta_{cd}T_c\in\ker H_q
                                                    =\mathcal G_q. \tag{6}
\]

Every term other than `p_cs_d` in (6) is supported on `G`; gauge vectors
are supported wherever `q` is.  Therefore `p_cs_d` is supported on `G`.
`QED`

This is the point at which the actual common power `q^(r-1)` enters.  A
general abstract quotient algebra need not identify its kernel with the
physical vertex gauges and gives no common support conclusion.

## 4. Mutually annihilating site subspaces

Package the two star families at a site-coordinate label `(i,alpha)` as

\[
 P_{i\alpha}=(p_{0,i,\alpha},p_{1,i,\alpha},p_{2,i,\alpha})^t,
 \qquad
 S_{i\alpha}=(s_{0,i,\alpha},s_{1,i,\alpha},s_{2,i,\alpha})^t,
\]

and put

\[
 x_{i\alpha}=(P_{i\alpha},S_{i\alpha}),\qquad
 U_i=\operatorname {span}\{x_{i0},x_{i1},x_{i2}\}
       \subseteq\mathbb C^3\oplus\mathbb C^3.            \tag{7}
\]

As before, define

\[
 \Phi((P,S),(P',S'))=PS'^t+P'S^t.                       \tag{8}
\]

The whole `(i,j)` block of all nine products vanishes exactly when

\[
                         \Phi(U_i,U_j)=0.                 \tag{9}
\]

We use the zero-pair classification from
`n8-clean-nearperfect-paircap-obstruction.md`: two nonzero points with
zero `Phi` are either pure of the same endpoint type, or are mixed
antipodes `(P,S)` and a scalar multiple of `(P,-S)`.

**Lemma 4.1 (connected zero-block classification).**  Let `F` be a
connected graph and suppose `U_i ne 0` at every vertex and (9) holds on
every edge of `F`.  Exactly one of the following occurs.

1. Every `U_i` is contained in `C^3 direct-sum 0`.
2. Every `U_i` is contained in `0 direct-sum C^3`.
3. The graph `F` is bipartite, every `U_i` is one-dimensional, and there
   is a mixed point `x=(P,S)` such that the site lines are `Cx` on one
   shore and `C(P,-S)` on the other.

**Proof.**  If some `U_i` contains a nonzero pure point, its zero relation
with a neighboring nonzero subspace forces that entire neighbor to be pure
of the same type.  Pairing back with a nonzero point of the neighbor forces
all of `U_i` to have that type.  Connectedness propagates the conclusion
to every site.

Otherwise choose a mixed `x in U_i`.  The zero-pair classification forces
every nonzero point of a neighboring `U_j` onto the single antipodal line
`C(P,-S)`.  Pairing a generator of that line back against `U_i` forces
`U_i=Cx`.  Propagation makes every site one-dimensional and alternates the
two lines along every edge.  A consistent alternation exists precisely
when `F` is bipartite. `QED`

## 5. Connected forbidden-block theorem

Call a site **two-star-active** if `U_i ne 0`.  This means that at least
one of the two deleted vertices has a nonzero matrix to that internal
site.

**Theorem 5.1 (connected forbidden blocks).**  Suppose the nine equations
(2) hold and there is a graph `F` such that every product block
`(p_cs_d)_{ij}` vanishes for `ij in F`.  If the subgraph of `F` induced by
the two-star-active sites is connected, then (2) is impossible.

**Proof.**  In either pure case of Lemma 4.1, one complete star family
vanishes, so all products `p_cs_d` vanish.  The left side of (2), viewed in

\[
 \operatorname {Mat}_{3\times3}\otimes(\mathcal R_W)_N,
\]

then has matrix/output flattening rank at most one, from `A tensor Q`.

In the mixed case write the active-site lines, after absorbing local
scalars, as `(P,S)` and `(P,-S)` on the two shores.  There are linear
elements `u,v in (R_W)_1` such that

\[
                         p_c=P_cu,\qquad s_d=S_dv.        \tag{10}
\]

Consequently all nine products package as the single decomposable tensor

\[
                         (PS^t)\otimes uv.                \tag{11}
\]

After applying `H_q` and adding the direct term, the left side of (2) has
matrix/output flattening rank at most two.  But the right side is

\[
                         \sum_{c=0}^2E_{cc}\otimes X_c,  \tag{12}
\]

which has rank three because both triples are linearly independent.  This
is a contradiction.  Sites outside the active set contribute zero to
`u,v` and do not change the argument. `QED`

Combining Lemma 3.1 and Theorem 5.1 gives the promised exact dichotomy.

**Corollary 5.2 (inactive-site cut).**  Under the hypotheses of Lemma 3.1,
let `F` be the complement of `G`.  In any solution of the nine caps, the
subgraph of `F` induced by the two-star-active sites is disconnected.  If
`F` is `k`-vertex-connected, at least `k` internal sites are simultaneously
invisible to both deleted stars.

The last statement follows because deleting fewer than `k` inactive sites
leaves the active induced graph connected.

## 6. The exhaustive pair trichotomy

The preceding theorem can be applied without guessing a graph of target
lifts.  Let `G(q)` be the physical support graph of `q`, and let
`R_2(G(q))` be the quadratic cells on its edges.

**Theorem 6.1 (pair-catalecticant trichotomy).**  Fix two deleted vertices
of a putative source and use (1)--(2).  At least one of the following
holds.

1. **Extra Hessian kernel:** `ker H_q` properly contains `G_q`.
2. **External pure lift:** for some colour `c`,
   \[
                  X_c\notin H_q(R_2(G(q))).              \tag{13}
   \]
3. **Invisible complement cut:** if `A` is the set of internal sites
   adjacent to at least one deleted vertex, the complement of `G(q)`
   induced on `A` is disconnected.

**Proof.**  If the first two alternatives fail, `q` is gauge-rigid and
each `X_c` has a lift supported on `G(q)`.  Lemma 3.1 makes every product
`p_cs_d` supported on `G(q)`.  The two-star-active set is exactly `A`, so
Theorem 5.1 forces the third alternative. `QED`

The external-lift branch has a concrete interpretation.  In the diagonal
`(c,c)` cap, the direct term is supported on `G(q)`.  If (13) holds, the
product `p_cs_c` must use a block on an absent internal edge whose
catalecticant class is nonzero modulo the internal-support image.  Thus an
absent chord is completed by the two deleted stars and carries an active
cofactor class.  Clean exposure is a particularly rigid instance of this
branch, but (13) alone does not isolate a single coefficient row.

The trichotomy is uniform and can be imposed for every deleted pair.  It
also identifies why it does not yet prove order descent:

* extra Hessian directions need not integrate to an exact deformation
  (`source-hessian-nonintegrability-countermodel.md`);
* an external lift can be a multi-edge Koszul bridge rather than a clean
  cell; and
* disconnectedness of a **complement** graph is a dense join in the
  support graph, not a small support separator.

The last limitation persists even after applying the conclusion to every
pair and recording component parity, as Section 8 shows.

## 7. A maximally rigid non-clean boundary core

On sites `0,...,5`, let `q` consist of the following nine unit cells:

\[
\begin{array}{c|c}
0&(04;00),(12;00),(35;00)\\
1&(01;11),(25;11),(34;11)\\
2&(02;22),(13;22),(45;22).
\end{array}                                               \tag{14}
\]

The three rows are perfect matchings.  Exact expansion gives

\[
 Q(q)=X_0+X_1+X_2+e_0\otimes e_2\otimes e_1\otimes
                         e_2\otimes e_0\otimes e_1.       \tag{15}
\]

Nevertheless all three pure tensors have supported one-cell Hessian
lifts:

\[
 \mathcal H_q(E_{12}^{00})=X_0,\qquad
 \mathcal H_q(E_{01}^{11})=X_1,\qquad
 \mathcal H_q(E_{02}^{22})=X_2.                          \tag{16}
\]

The map `H_q:R_2 -> R_6` has rank `130`.  Its domain has dimension `135`,
and the five independent vertex gauges are always in its kernel, so

\[
                         \ker H_q=G_q.                   \tag{17}
\]

Every one of the nine active cells has a nonzero cofactor.  On the other
hand, no absent physical edge is cleanly exposed for any colour.  Thus
gauge rigidity, active cofactors, and simultaneous pure target membership
do not force the clean hypothesis of the preceding sparse theorem.

There is also no immediate pair-deletion descent: every four-site
cofactor of (14) has local flattening rank at most two, whereas
`Delta_(4,3)` has local rank three.  In particular none is locally
equivalent to the smaller ternary target.

Let `G` be the nine-edge physical support in (14).  Its complement is the
six-cycle

\[
                         03,32,24,41,15,50.               \tag{18}
\]

Equations (16)--(17) put this core under Corollary 5.2.  The cycle is
two-vertex-connected.  Hence any hypothetical completion of this `q` to
all nine pair caps would have at least two internal sites with both deleted
stars identically zero.  This is new information supplied by the
factorized products; none of the Hessian facts (15)--(17) alone sees it.

## 8. Extra kernel plus external lift need not become clean

The intersection of alternatives 1 and 2 in Theorem 6.1 has its own exact
boundary.  On six sites take the following thirteen unit cells:

\[
\begin{split}
 &(34;22),(45;22),(04;00),(13;00),(23;11),(02;11),(01;22),\\
 &(35;11),(13;11),(04;11),(14;00),(25;00),(34;00).
\end{split}                                               \tag{19}
\]

Its Hessian has rank `125`, so this is genuinely in the extra-kernel
branch.  All three pure tensors are nevertheless in the full Hessian
image.  More precisely,

\[
 H_q(E_{03}^{00})=X_0,\qquad
 H_q(E_{14}^{11})=X_1,\qquad
 H_q(E_{23}^{22})=X_2.                                  \tag{20}
\]

The physical edge `03` is absent from the support of `q`.
The Hessian image of cells on supported physical edges has rank `85`, and
adjoining `X_0` raises it to `86`.  Thus `X_0` is a genuine external pure
lift, even though its displayed preimage is a single cell.

Still, `(03,0)` is not cleanly exposed in the sense of Section 3, and no
other absent edge-colour pair is clean.  The pure target
row is singleton, but other rows in the same nine-cell edge block have
competing columns.  Every active `q`-cell has nonzero cofactor.

This gives a precise negative audit:

\[
 \text{external pure lift, even by one cell}
 \quad\not\Longrightarrow\quad
 \text{clean exposed edge}.                              \tag{21}
\]

The example is not a nine-cap solution.  It shows that any proof of the
implication in (21) must use the factorized products together with control
of the extra Hessian kernel; target membership and cofactor activity do not
suffice.

## 9. Global separator and parity do not follow

There is a sharp eight-vertex support countermodel to a graph-only global
use of alternative 3 in Theorem 6.1.  Partition the vertices as

\[
 A=\{0,1,2\},\qquad B=\{3,4,5\},\qquad C=\{6,7\},        \tag{22}
\]

and take the complete tripartite support graph `K_(3,3,2)`.  Its complement
has three components of parities odd, odd, and even.  The support graph is
5-vertex-connected and matching-covered.

For every deleted pair `p,q`, let `D_pq` be the internal sites adjacent to
at least one of them.  Direct inspection of the three parts gives

\[
 \overline{G-p-q}[D_{pq}]\ \text{disconnected}            \tag{23}
\]

for all 28 pairs.  If the endpoints lie in different parts, all remaining
sites are active and at least two complement parts survive.  If they lie
in the same three-vertex part, its one remaining vertex is inactive while
the other two parts remain as two complement components.  If they are the
two vertices of `C`, the two three-vertex components remain.  Hence the
global disconnected-complement conclusion supplies neither a small vertex
cut of the support nor an order reduction.

This boundary also survives the currently available entry-minimal support
data.  The graph has the following three edge-disjoint perfect matchings:

\[
\begin{aligned}
 M_0&=03|16|25|47,\\
 M_1&=07|15|23|46,\\
 M_2&=06|13|24|57.
\end{aligned}                                             \tag{24}
\]

Put the singleton cell `(r,r)` on `M_r` and `(0,0)` on every remaining
edge.  Then every vertex has an active coordinate anchor of every colour.
All coefficients are positive and every edge has a complementary perfect
matching, so every edge cofactor is nonzero.  The scalar-cell contribution
atoms at each star are linearly independent: their ranks are five at the
six vertices in the two three-vertex parts and six at the last two
vertices.  Finally, enumeration of all 36 perfect matchings shows that the
graph has no nontrivial tight odd cut.

This array is not asserted to realize the ternary target.  It is an exact
countermodel to the implication

\[
 \text{alternative 3 for every pair + component parity + anchors/activity}
 \Longrightarrow \text{a support separator or smaller realization}. \tag{25}
\]

Coefficient-level compatibility among the pair quotients is still needed.

## 10. Exact audit

Run

```text
uv run python computations/verify_nonclean_pair_catalecticant_bridge.py
```

The script constructs all `729 by 135` Hessian coefficients over the
integers, certifies rank `130` modulo `1000003`, verifies the five gauge
directions and the three lifts (16), expands (15), checks absence of every
clean exposed edge, and computes all local flattening ranks of all fifteen
four-site cofactors.  It verifies the ranks, four singleton lifts, supported
image gap, active cofactors, and absence of clean blocks in (19)--(21).  It
also audits (22)--(24): 5-connectivity, all 28
deleted-pair complement decompositions, three anchor matchings, active
cofactors, local star independence, all 36 perfect matchings, and absence
of tight odd cuts.
