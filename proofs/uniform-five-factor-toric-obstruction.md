# A uniform toric obstruction for the balanced five-factor model

## 1. Result

The balanced Boolean support in Proposition 4.1 of
`notes/torus-polystable-fiber.md` is not merely an artefact of six vertices.
It survives every support and moment-map test at every even order.  On its
natural all-rank-one stratum, however, the mixed coefficient equations are
uniformly inconsistent.

Let `B` have even cardinality `n >= 6`.  Let

\[
                         P,P',Q_0,Q_1,Q_2                 \tag{1}
\]

be pairwise edge-disjoint perfect matchings.  Assume that `P union P'` is a
Hamilton cycle `C`, and that some edge `xy` of `Q_0` joins the two
bipartition classes of `C`.  Put a full-support nonzero rank-one tensor on
each edge of `P union P'`, a nonzero multiple of `e_i tensor e_i` on every
edge of `Q_i`, and zero on every other underlying pair.  Then the resulting
matching tensor is not

\[
                         \Delta_{n,3}=\sum_{i=0}^2e_i^{\otimes n}. \tag{2}
\]

The proof below is a Laurent, or localized source-ideal, certificate.  It
uses only mixed coefficient equations and nonvanishing of the displayed
source coordinates.  In particular it permits arbitrary nonzero complex
rank-one factors and arbitrary nonzero anchor weights.

## 2. Clean colorings can vary one port at a time

Call a coloring `c:B -> {0,1,2}` **clean** if no edge of `Q_i` has both
endpoints colored `i`, for any `i`.  Thus a clean coloring disables every
anchor edge.

**Lemma 2.1 (clean Hamming pairs).**  For every vertex `v` and every
`a in {1,2}`, there are two clean mixed colorings `c,c'` which agree away
from `v` and satisfy

\[
                         c(v)=0,\qquad c'(v)=a.             \tag{3}
\]

**Proof.**  Let `b` be the third color, so `{0,a,b}={0,1,2}`.  We construct
a set `S subset B minus {v}` with the following properties:

1. `S union {v}` is independent in the matching `Q_0`;
2. every `Q_b`-edge other than the edge incident with `v` has exactly one
   endpoint in `S`.

The union `Q_0 union Q_b` is a disjoint union of alternating even cycles.
On a component not containing `v`, choose every other vertex so that each
`Q_b`-edge has one chosen endpoint and no `Q_0`-edge has two.  On the
component containing `v`, delete the `Q_b`-edge incident with `v`.  What
remains is an alternating path.  Starting after the `Q_0`-neighbor of `v`,
choose the even-indexed vertices along this path.  This chooses one endpoint
of every remaining `Q_b`-edge, chooses no two endpoints of a `Q_0`-edge,
and does not choose the `Q_0`-neighbor of `v`.  The required `S` follows.

Color every vertex of `S` by `0`, every vertex outside `S union {v}` by
`b`, and color `v` first by `0` and then by `a`.  The zero-colored vertices
are `Q_0`-independent in both colorings.  Only `v` can have color `a`, and
every `Q_b`-edge has a non-`b` endpoint.  Hence both colorings are clean.
They are mixed because the `Q_b`-neighbor of `v` lies outside
`S union {v}` and has color `b`.  This proves the lemma. `QED`

## 3. The two Hamilton-cycle monomials cancel identically

For each full-support rank-one edge `uv` write its endpoint factors as

\[
 A_{uv}=p_{uv}^{(u)}\otimes p_{uv}^{(v)},
 \qquad p_{uv}^{(u)}(r),p_{uv}^{(v)}(r)\ne0\quad(r=0,1,2). \tag{4}
\]

Let `m_P(c)` and `m_{P'}(c)` be the matching monomials of `P` and `P'` in
the coefficient indexed by `c`.  Their ratio factors vertex by vertex:

\[
 \frac{m_P(c)}{m_{P'}(c)}=\prod_{v\in B}\rho_v(c(v)),       \tag{5}
\]

where `rho_v(r)` is the quotient of the local rank-one factor on the
`P`-edge at `v` by that on the `P'`-edge at `v`.  Every `rho_v(r)` is
nonzero.

For a clean coloring, the only usable underlying edges are those of `C`.
An even Hamilton cycle has exactly its two alternating perfect matchings,
namely `P` and `P'`.  A clean coloring is mixed, so (2) would give

\[
                         m_P(c)+m_{P'}(c)=0.                \tag{6}
\]

Apply (6) to the two clean colorings in Lemma 2.1.  They differ only at
`v`; division by the nonzero monomials in (5) gives

\[
                         \rho_v(0)=\rho_v(a).               \tag{7}
\]

This holds for every `v` and `a=1,2`.  Hence the ratio (5) is independent of
the coloring.  Since it equals `-1` on every clean coloring, we obtain

\[
                         m_P(d)+m_{P'}(d)=0                 \tag{8}
\]

for **every** coloring `d`, constant or mixed.

This is the essential source-ideal step.  Boolean support sees only the two
terms in (6); the collection of neighboring fibers forces their Laurent
ratio to be the constant `-1` on the entire coloring cube.

## 4. One activated chord gives the contradiction

Choose a vertex `w` outside `{x,y}`.  Lemma 2.1 supplies a clean coloring
having `w` colored `1`.  Change only the colors at `x,y` to `0`.  Call the
result `d`.  Because `xy` is their common `Q_0`-edge, this activates exactly
the one anchor edge `xy`: all other `Q_0`-edges remain disabled, and changing
a color to zero cannot activate a `Q_1`- or `Q_2`-edge.  The coloring is
still mixed because `d(w)=1`.

The endpoints `x,y` lie in opposite bipartition classes of the Hamilton
cycle.  Deleting them from `C` leaves two even paths, each with a unique
perfect matching.  Therefore `C union {xy}` has exactly three perfect
matchings: `P`, `P'`, and

\[
              H=\{xy\}\mathbin\cup
                 \text{(the unique matchings of the two paths)}. \tag{9}
\]

All factors in the monomial `m_H(d)` are nonzero.  The mixed coefficient at
`d`, using (8), is consequently

\[
 H_n(A)_d=m_P(d)+m_{P'}(d)+m_H(d)=m_H(d)\ne0,              \tag{10}
\]

contrary to (2).  This proves the result.

## 5. The countermodel from the torus note satisfies the hypotheses

For completeness, use the standard cyclic one-factorization on
`B=Z/(n-1) union {infinity}`.  Its round `r` is

\[
 F_r=\{\{\infty,r\}\}\mathbin\cup
     \{\{r+k,r-k\}:1\le k<n/2\}.                           \tag{11}
\]

Take

\[
 P=F_0,\quad P'=F_1,\quad Q_i=F_{i+2}.                    \tag{12}
\]

The first two rounds form the Hamilton cycle beginning

\[
 \infty,0,2,-2,4,-4,6,-6,\ldots,1,\infty.                 \tag{13}
\]

Successive edges alternate between `F_0` and `F_1`; the displayed residues
are modulo `n-1`, and they exhaust all residues because `n-1` is odd.  The
edge `{0,4}` belongs to `F_2=Q_0`, and its endpoints occur at positions one
and four in (13), hence in opposite bipartition classes.  The theorem
applies for every even `n>=6`.

If the full rank-one factors on `P union P'` are chosen to be all-ones
vectors and the anchors have unit weight, this source is already at a
Kempf--Ness critical point for the target-stabilizing torus: every port
`(v,i)` has squared incidence `3+3+1=7`.  It is also strictly support
balanced and every coloring supports at least `P` and `P'`.  Thus neither
ordinary balance, squared-norm balance, anchors, nor the no-singleton rule
detects the contradiction.  Equations (5)--(10) show precisely what is
missing: a localized binomial compatibility relation across several mixed
coefficient fibers.

The discovery audit `computations/analyze_five_factor_countermodel.py`
checks the cyclic construction, the full local-character rank, and an exact
three-matching witness for the first four even orders.  The proof above is
uniform and does not depend on that finite audit.

## 6. A robust-clean-coloring lemma

There is a stronger version which removes the rank-one assumption on the
Hamilton cycle.  Let

\[
                         D=Q_0\cup Q_1\cup Q_2.             \tag{14}
\]

Regard the proper edge color `i` on `Q_i` as a choice available at each
vertex.  A coloring `c` selects at `v` the unique incident `Q_(c(v))` edge.
It is clean exactly when no edge of `D` is selected by both endpoints.

**Lemma 6.1 (robust clean extension).**  Let `U subset B`.  If every
component of `D-U` contains a cycle, then one can color `B-U` so that every
assignment of colors to `U` extends it to a clean coloring, provided `U` is
independent in `D`.

**Proof.**  In every component of `D-U`, choose a spanning unicyclic
subgraph.  Direct its unique cycle cyclically and direct every remaining
tree edge toward the cycle.  Color a vertex of `B-U` by the label of its
outgoing edge.  Thus every background vertex selects an edge wholly inside
`B-U`, and no such edge is selected at both ends: off the cycle a vertex
selects its parent while its parent selects onward, and on the cycle all
selections have one cyclic direction.  A boundary edge is never selected by
its background endpoint.  Vertices of `U` may therefore select arbitrary
incident edges without a mutual selection across the boundary; independence
of `U` prevents a mutual selection inside `U`. `QED`

Suppose now that `D` is 3-vertex-connected, `n>=8`, and the Hamilton cycle
`C=P union P'` is edge-disjoint from `D`.  For one vertex `v`, the graph
`D-v` is connected and has

\[
 |E(D-v)|=3n/2-3\ \ge\ n-1=|V(D-v)|,                       \tag{15}
\]

so it contains a cycle.  For the endpoints `u,v` of any edge of `C`, the
vertices are nonadjacent in `D`; hence `D-{u,v}` is connected and

\[
 |E(D-\{u,v\})|=3n/2-6\ \ge\ n-2=|V(D-\{u,v\})|.           \tag{16}
\]

It too contains a cycle.  Lemma 6.1 consequently supplies both of the
following:

* a clean background away from any one vertex which remains clean for all
  three colors at that vertex;
* a clean background away from the endpoints of any cycle edge which
  remains clean for all nine ordered color pairs at those endpoints.

Every coloring just constructed is mixed.  Indeed, for a proposed constant
color `i`, the background endpoint of the `Q_i`-edge from a deleted vertex
does not select that boundary edge and therefore does not have color `i`.

## 7. Arbitrary full matrices on the Hamilton cycle

**Theorem 7.1 (robust five-factor obstruction).**  Assume `n>=8`, that
`D=Q_0 union Q_1 union Q_2` is 3-vertex-connected, and that
`C=P union P'` is an edge-disjoint Hamilton cycle.  Put an arbitrary matrix
with all nine entries nonzero on every edge of `C`, a nonzero multiple of
`e_i tensor e_i` on every edge of `Q_i`, and zero elsewhere.  Then its
matching tensor is not `Delta_(n,3)`.

**Proof.**  All matching monomials of `P` and `P'` are nonzero.  Define the
Laurent ratio

\[
                         R(c)=m_P(c)/m_{P'}(c).              \tag{17}
\]

For every clean coloring the only usable graph is `C`, whose only perfect
matchings are `P,P'`.  Since the robust clean colorings above are mixed, the
mixed equations give `R(c)=-1` on all of them.

Fix a cycle edge `e=uv` and use a robust background away from `u,v`.  For
colors `a,a',b,b'`, all four corners are clean, so their `R`-values are
`-1`.  Taking their multiplicative rectangle gives

\[
 1=\frac{R(a,b)R(a',b')}{R(a,b')R(a',b)}
  =\left(
    \frac{A_e(a,b)A_e(a',b')}{A_e(a,b')A_e(a',b)}
    \right)^{\sigma_e},                                    \tag{18}
\]

where `sigma_e=1` for `e in P` and `sigma_e=-1` for `e in P'`.  Every other
cycle-edge factor cancels: an edge adjacent to `e` depends on only one of
the two varied colors, and all other factors are fixed.  Equation (18), for
all choices of colors, says that every `2 by 2` minor of `A_e` vanishes.
Since its entries are nonzero, `A_e` has rank one.  This holds on every edge
of `C`.

We are now in the setting of Sections 3--4.  Alternatively, use the robust
one-vertex backgrounds directly: the rank-one factorization of (17) and the
three equal values `R=-1` force each local factor `rho_v` to be independent
of its color.  Thus

\[
                         m_P(c)+m_{P'}(c)=0                 \tag{19}
\]

for every coloring `c`.

Because `D` is connected, some edge of `D` crosses the two bipartition
classes of `C`; otherwise those classes disconnect `D`.  Relabel the three
colors so that such an edge `xy` belongs to `Q_0`.  Choose `w` outside
`{x,y}` and a robust clean coloring with `w` colored `1`, then change only
`x,y` to color zero.  Exactly the anchor edge `xy` becomes usable.  As in
Section 4, `C union {xy}` has precisely `P,P'` and one further perfect
matching `H`, and the mixed coefficient is, by (19), the nonzero monomial
`m_H`.  This is a contradiction. `QED`

## 8. Such robust balanced countermodels exist at every order

For every even `n>=8`, take for `D` the Möbius ladder on `Z/n`: its rim is
the cycle with edges `{j,j+1}`, and its rungs are `{j,j+n/2}`.  The rungs
form one perfect matching and the alternating rim edges form two more, so
`D` is 3-edge-colorable.  It is 3-vertex-connected.  Indeed, deleting two
vertices cuts the rim into at most two paths; if both are nonempty, some
antipodal rung joins them (a nonempty proper cyclic interval cannot be
invariant under translation by `n/2`).

The complement of `D` has minimum degree `n-4>=n/2`.  Dirac's theorem gives
a Hamilton cycle `C` in that complement.  Split its alternating edges into
`P,P'`, and use the three edge-color classes of `D` as `Q_0,Q_1,Q_2`.
These are five pairwise edge-disjoint perfect matchings satisfying Theorem
7.1.  At `n=6`, take `C=C_6` and let `D` be its triangular-prism complement;
the full-matrix chart is the exact saturated obstruction already proved in
`proofs/saturated-rank-graph-obstruction.md`.

Thus the balanced Boolean countermodel can be chosen, uniformly in every
even order, so that its **entire arbitrary full-matrix chart** is excluded
by clean-fiber Laurent relations.  This still does not prove the conjecture:
a hypothetical closed-orbit point need not have support equal to five
factors, need not contain two universal full-support matchings, and may have
extra edges whose monomials enter the clean fibers.  The sharply reduced
remaining issue for this route is therefore not balance but extraction of a
robust five-factor subchart while controlling all additional matching terms.

## 9. Why a target-torus support face cannot remove the extra terms

The most tempting extraction argument is unavailable for an exact reason.

**Lemma 9.1 (target-torus faces are fiber-saturated).**  Let `S` be a source
coordinate support, and let `h_(v,i)` have zero sum over `v` for each color.
Give a supported coordinate `(uv;i,j)` the target-torus weight

\[
                         \omega(uv;i,j)=h_{u,i}+h_{v,j}.    \tag{20}
\]

Assume every supported coordinate has nonnegative weight, so that the
one-parameter limit at zero is finite.  Fix a coloring `c`.  If one supported
perfect-matching monomial in the `c`-fiber survives the limit, then every
supported perfect-matching monomial in that fiber survives.

**Proof.**  For every perfect matching `M` compatible with `c`, its total
weight is

\[
 \sum_{uv\in M}\omega(uv;c(u),c(v))
     =\sum_{v\in B}h_{v,c(v)},                              \tag{21}
\]

which is independent of `M`.  A surviving monomial uses only weight-zero
coordinates, so (21) is zero.  Every other supported monomial has the same
zero total weight.  Since all of its coordinate weights are nonnegative,
each of them is zero, and that monomial survives as well. `QED`

In particular, a target-stabilizing one-parameter subgroup can never retain
`P,P'` in one of the clean fibers while deleting its extra cancellation
mates.  For a constant-color fiber of an exact point, at least one monomial
must survive in any exact finite limit, so the whole supported constant fiber
survives.  At the closed-orbit representative of Theorem 3.1 in the torus
note, strict balance already rules out any nontrivial nonnegative deletion
direction; Lemma 9.1 is the stronger fiberwise reason that even a putative
face tailored to the five-factor core cannot work.

The prism border scaling does not evade the lemma.  It has both positive and
negative source-coordinate weights, so its source escapes to infinity and
has no affine support-deleting limit.  It can make a mixed *output*
coefficient tend to zero only because the whole coefficient is one torus
weight, exactly as (21) says.

Consequently entry-minimality, closed-orbit balance, or a
Hilbert--Mumford face cannot bridge the arbitrary-extra-edge gap.  What would
bridge it is one of two genuinely new inputs:

1. a structural theorem producing the required clean fibers with no extra
   supported matchings already present; or
2. a non-torus localized ideal identity which eliminates all extra terms
   before applying the rectangles.

This is a strict reduction rather than a reformulation: Theorem 7.1 supplies
the full contradiction after either input, while Lemma 9.1 proves that the
most natural minimization mechanism cannot supply it.

## 10. A balanced exact-support countermodel to binomial extraction

Even the existence of a binomial clean fiber cannot be inferred from the
known support and moment-map conditions.  For every even `n>=8`, choose six
pairwise edge-disjoint perfect matchings

\[
                         P_0,P_1,P_2,Q_0,Q_1,Q_2           \tag{22}
\]

from a one-factorization of `K_n`.  Put `I+J` on every edge of the three
`P`-matchings, put `e_i e_i^T` on `Q_i`, and put zero elsewhere.  Then:

* every vertex has a same-color coordinate anchor for each color;
* every coloring has at least the three supported monomials `P_0,P_1,P_2`;
* every full matrix is invertible;
* assigning weight one to supported cells gives incidence
  `3+3+3+1=10` at every port; and
* using actual squared magnitudes gives incidence
  `6+6+6+1=19` at every port.

Thus this point is both strictly support-balanced and already
squared-magnitude balanced, while **no** coefficient fiber is binomial.
This is an exact finite support construction, not a claim that its
coefficients equal the target.  It proves that anchors, full-rank witnesses,
closed-orbit balance, Kempf--Ness balance, and the no-singleton rule do not
force the local hypothesis needed by the rectangle argument.  Lemma 9.1
also shows that a finite target-torus face retaining two of the universal
monomials must retain the third.  Hence controlling extra matching terms
requires the algebraic coefficient equations in an essentially non-Boolean,
non-Hilbert--Mumford way.
