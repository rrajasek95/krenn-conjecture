# Statements submitted for repository certification

This package uses “certification” in the sense of the repository baseline:
an exact proof artifact and an independent mathematical audit. It is not a
Lean proof, a claim of human peer review, or a proof at every number of sites.
The final admission status is recorded in the supersession ledger.

## The model and the scope

There are an even number of sites, $n=2m\ge4$. At each site there are
three fixed basis vectors $a,b,c$. Multiplication is commutative, and any
product using the same site twice is zero. A quadratic source $A$ is a sum
of edges between distinct sites; each edge can have arbitrary complex
coefficients for its nine ordered endpoint-color pairs. Parallel contributions
to the same cell are combined into their total coefficient.

Write $A^{[m]}=A^m/m!$. Expanding it sums the weights of all perfect matchings,
with each matching counted once. The hypothesis throughout is the **whole** equality

$$
A^{[m]}=\tau_a a^V+\tau_b b^V+\tau_c c^V,
\qquad \tau_a\tau_b\tau_c\ne0.
$$

Thus all mixed color words have total amplitude zero, after possible complex
cancellation. There is no positivity, genericity, density, sparsity, or
minimum-counterexample assumption. Unequal nonzero pure amplitudes are allowed.

## GD: global diagonal reduction

Every edge coefficient with different colors at its two endpoints is zero
in the **original fixed target bases**. For each color $h$, let $M_h$ be
the symmetric zero-diagonal matrix of its remaining edge weights. Define

$$
C_h[u,v]=\operatorname{haf}(M_h[V\setminus\{u,v\}])\quad(u\ne v),
\qquad C_h[u,u]=0.
$$

Then $M_hC_h=\tau_h I$, so $C_h=\tau_h M_h^{-1}$. Here a hafnian is the
sum of products over perfect matchings, with the empty hafnian equal to one.
These are the actual deletion cofactors of $M_h$, not separately assigned matrices.

The remaining existence problem is exactly

$$
\operatorname{haf}(M_h)=\tau_h\ne0,\qquad
\prod_h\operatorname{haf}(M_h[S_h])=0
$$

for every nonconstant color partition $V=S_a\sqcup S_b\sqcup S_c$.
Odd-sized hafnians are zero. Cancellation inside each hafnian remains allowed.

Proof: [GD §§1–6](sources/GD.md), with the chain CF, BM, HP, EV below.
Independent review: [original audit](audits/GD.md) and the
[current-text foundation reconstruction](audits/FOUNDATION.md), which pins
all six foundation texts by their current SHA-256 values.

## Degree restrictions

For $n=2m\ge6$, each site's degree in each individual color obeys

$$
1\le \deg_h(v)\le m-2.
$$

A degree-one vertex belongs to an isolated edge, and degree two is impossible.
Also, if two vertices are adjacent or have a common neighbor in color $h$,
their cofactor in either other color is zero. At four sites the strict degree
bound does not apply; the familiar three colored matchings on $K_4$ remain valid.

Proof: [NB §§1–4](sources/NB.md), [SD §5 only](sources/SD.md).
Independent audits: [NB](audits/NB.md), [SD](audits/SD.md).
The leaf and degree-two lemmas need only the actual scalar identity
$MC=\operatorname{haf}(M)I\ne0$. The strict upper bound needs the full source.

## Eight sites: a complete finite conclusion

**There is no source satisfying the stated whole equation on eight sites.**

The degree bound gives degree at most two in every color. The scalar lemma
excludes degree two, so each color consists of a perfect matching with all
weights nonzero. If two colors share an edge $e$, the word using the first
color on $e$ and the second elsewhere has a unique matching contribution:
the first edge times all remaining edges of the second matching. Its weight
is nonzero, contradicting the whole equation. Thus the three matchings are
pairwise edge-disjoint.

Relabel vertices to make the first matching $01,23,45,67$. There are exactly
$7\cdot5\cdot3\cdot1=105$ perfect matchings on the eight labeled vertices.
[matching8.json](matching8.json) supplies an extra matching in the union for
every ordered pair of second and third matchings disjoint from the first and
from each other. The checker regenerates all 105 matchings by the exhaustive
least-vertex recurrence and checks every eligible ordered pair; it uses no
graph-isomorphism library or unverified symmetry reduction. Fixing the first
matching is justified by relabeling any perfect matching's four edges.

Color each vertex by the color of its edge in the extra matching. This word
is mixed: a pure matching would be one of the original three. At every vertex
there is only one incident edge of the selected color, so the word has exactly
one compatible matching. The checker also verifies uniqueness by inspecting
all 105 matchings. Its coefficient is a product of nonzero edge weights and
cannot cancel. This is the contradiction.

The generator independently enumerates four-edge subsets of the 28 possible
edges and keeps those covering every vertex. The verifier does not import it.
The analogous extra-matching statement fails at four sites, as the included
boundary control confirms. This finite certificate proves only the terminal
matching lemma; the arbitrary-weight reduction uses GD, NB, and SD.

## Ten sites: an analytic conclusion

**There is no source satisfying the stated whole equation on ten sites.**

The complete proof is [H10 §§1–6](sources/H10.md), with an
[independent full audit](audits/H10.md) of the surviving exact
[frozen source](sources/H10-frozen.md). Its steps are:

1. Every color component is an isolated edge or a cubic graph.
2. Five vertices cannot form a common isotropic coordinate subspace for
   both other cofactor matrices: inversion gives an actual balanced binary
   source, BC forces the remaining color to have no edges across the cut,
   and its odd five-site shores cannot have a perfect matching.
3. A cubic color component has no triangles (TR) or five-cycles (step 2).
   A shortest longer odd cycle would have length $g\ge7$. Every cycle
   vertex has one neighbor outside it; every outside vertex has at most
   two neighbors on it. Thus $3g\le2q\le20$, impossible for a component
   of $q\le10$ vertices. Every cubic component is therefore bipartite.
4. Its equal shores have size 3, 4, or 5. Size 3 and size 5 violate the
   cofactor isotropy constraints. Size 4 is a crown graph together with
   an isolated edge, excluded by CR. Thus all three colors are matchings.
5. Two matchings have a common balanced bipartition into five and five
   vertices, including when some edges coincide. Their cofactor matrices
   vanish on each shore, contradicting step 2.

This proof uses no graph census or SAT solver. The included bounded triangle
and crown checks verify identities and essential hypotheses, not the entire
ten-site theorem. In particular, the scalar crown-plus-edge control satisfies
$MC=15I$; its exclusion requires the other two colors.

## Dependency inventory

Only the stated sections are admitted. Copying a whole historical file does
not promote its other corollaries. Empty dependency lists below mean those
scoped sections prove their identities directly by finite algebra.

| ID | Admitted proof scope | Inputs | Independent review |
|---|---|---|---|
| CF | [§§1–3: common pure-response factors](sources/CF.md) | None | [CF](audits/CF.md), [foundation](audits/FOUNDATION.md) |
| BM | [§§1–3: binary mixed-response vanishing](sources/BM.md) | None | [BM](audits/BM.md), [foundation](audits/FOUNDATION.md) |
| HP | [§§1–4: higher pure/binary vanishing](sources/HP.md) | CF, BM | [HP](audits/HP.md), [foundation](audits/FOUNDATION.md) |
| EV | [§§1–3 and the source application (14) in §5 only](sources/EV.md) | HP | [EV](audits/EV.md), [foundation](audits/FOUNDATION.md) |
| GD | [§§1–6: diagonal reduction and actual inverses](sources/GD.md) | EV | [GD](audits/GD.md), [foundation](audits/FOUNDATION.md) |
| RV | [§1: retained-vacuum four-row identity](sources/RV.md) | None | [RV](audits/RV.md), [BC §2](audits/BC.md) |
| BC | [§§1–3 and balanced-source corollary in §4 only](sources/BC.md) | RV | [BC](audits/BC.md) |
| NB | [§§1–4: neighborhood zeros and strict degree bound](sources/NB.md) | GD, HP, BC | [NB](audits/NB.md) |
| SD | [§5 only: scalar leaves and degree two](sources/SD.md) | None | [SD](audits/SD.md) |
| TR | [§§1–4: cubic-triangle theorem only; excludes degree-at-least-four corollary](sources/TR.md) | None | [TR](audits/TR.md) |
| CR | [§§3,5: complementary nullity and crown plus edge](sources/CR.md) | GD, NB, SD | [CR](audits/CR.md) |
| H10 | [§§1–6: ten-site impossibility](sources/H10.md) | GD, NB, SD, TR, BC, CR | [H10](audits/H10.md) |

The EV scope excludes the contextual whole-pair-cofactor nonvanishing claim
and other §5 consequences; GD needs only (14). BC excludes the later kernel
discussion. TR excludes its separate degree-at-least-four corollary, which
would additionally use SD. These exclusions concern admitted scope, not
changes to the historical proof texts.

HP requires all three target functions to be active and their joint image to
have rank at least two. The original three rows at a root of a full source
have rank three, supplying this premise. Higher responses on words using all
three colors need not vanish. BC asserts whole binary cofactor nonvanishing,
not nonvanishing of each of its pure coefficients. Those distinctions are
preserved throughout this package.

The same eight- and ten-site exclusions apply to sources with more than three
nonzero diagonal target terms: project locally onto any three designated
target coordinates. This preserves an ordinary quadratic source and the
three nonzero target amplitudes. Global diagonality is stated here for the
ternary model; no additional conclusion about arbitrary unused coordinates
is registered.

The six-site theorem was already certified in the older spine. General
even orders $n\ge12$ remain open under the results admitted here. No claim
is made to close SP-CLEAN-BRIDGE or to justify universal descent.
