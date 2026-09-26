# Ten vertices are excluded by the uniform cofactor identities

**Status.** NEW proposed research proof, 2026-09-20, by `/root`.
Complete independent audit is pending. The proof composes new all-order
identities, including the independently reviewed degree bound and two
new scalar/component results whose frozen sources are linked below.
It uses no graph census, finite algebraic certificate, or assumption
of generic or positive weights. The general conjecture remains open.

## 1. Hypothetical source and exact inputs

Assume an ordinary complex ternary source on a set V of TEN vertices,
with local spaces exactly C^3 and fixed target bases a,b,c, satisfies

    A^[5]=tau_a a^V+tau_b b^V+tau_c c^V,
    tau_a tau_b tau_c != 0.                                (1)

The physical algebra is commutative and square-zero at each site;
Q^[j]=Q^j/j!. A whole equality retains every mixed color coefficient.

The reviewed [global edge theorem](../unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-GLOBAL-EDGE-MONOCHROMATICITY-AND-COFACTOR-INVERSE.md)
makes every original edge diagonal in these bases. Let M_h be its
symmetric zero-diagonal scalar h adjacency, and let

    C_h[u,v]=haf(M_h[V without {u,v}]) for u!=v,
    C_h[u,u]=0.

Then haf(M_h)=tau_h!=0 and M_h C_h=tau_h I. In particular all these
matrices are invertible. Every color word has the exact coefficient

    product_h haf(M_h[S_h]),                               (2)

where V is the ordered disjoint union of its color classes S_h.
Haf(empty)=1, and odd-order hafnians are zero. Products in (2) retain
all cancellations inside the matching sums.

The remaining inputs are these precise results.

* The reviewed [neighborhood and degree theorem](../unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-CLOSED-NEIGHBORHOOD-ISOTROPY-AND-COLOR-DEGREE-BOUND.md)
  gives 1<=deg_(G_h)(v)<=3. For k!=h it also gives C_k[u,v]=0
  whenever u and v are h-adjacent or share an h neighbor.
* The reviewed [scalar degree theorem](../unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-SCALAR-PENCIL-STAR-INVARIANCE-AND-DEGREE-STRUCTURE.md)
  says degree two is impossible and every degree-one vertex belongs
  to an isolated matching edge. Thus every color component is an
  isolated edge or a connected cubic graph.
* The frozen [scalar triangle theorem](CUBIC-SCALAR-TRIANGLE-EXCLUSION-NEW-SOURCE.md)
  excludes every triangle whose three vertices have scalar degree
  three, under the actual identity MC=haf(M)I!=0. Consequently every
  cubic color component here is triangle-free.
* The reviewed [balanced binary cofactor theorem](../unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-BIPARTITE-TWO-ACTIVE-RECTANGULAR-COFACTOR-NONVANISHING.md)
  gives nonzero whole binary cofactors after every opposite-shore
  deletion from an actual balanced binary source with both targets
  nonzero. Individual pure cofactor coefficients may vanish.
* The frozen [crown-plus-edge theorem](BIPARTITE-COLOR-COMPONENT-BOUNDARY-AND-CROWN-EXCLUSION.md)
  excludes a color graph K_(r,r) with one perfect matching removed,
  together with one isolated edge on the remaining two vertices,
  for every r>=3. We need only r=4. Its proof uses the actual
  cofactor inverse identities, neighborhood zeros, scalar degree
  lemmas, and original mixed coefficients. It is independent of
  the present ten-vertex conclusion.

No minimum counterexample premise is used. The conclusion is for
every source satisfying (1), not just a support-minimal representative.

## 2. A common five-dimensional isotropic coordinate set is impossible

We give the argument explicitly. Suppose S subset V has |S|=5 and

    C_b[S,S]=C_c[S,S]=0,                                   (3)

relabeling the colors if needed. Put T=V without S, also of size five.
In the ordering S,T, either of these invertible cofactor matrices has
block form [[0,Z],[Z^T,H]], with Z square and invertible. Indeed a
kernel vector of Z^T would give a full kernel vector supported on S.
Its inverse has zero T,T block. Therefore

    M_b[T,T]=M_c[T,T]=0.                                  (4)

Project the original whole source to the b/c planes. Every T vertex
must match to S, and the equal shore sizes force every matching to
use only crossing edges. The crossing-only quadratic B is an ACTUAL
balanced binary source with top tau_b b^V+tau_c c^V.

For every s in S,t in T, its whole binary cofactor F_st after deleting
s,t is nonzero by the reviewed theorem. The same occupancy argument
on the remaining four-plus-four vertices shows that F_st equals the
b/c projection of the FULL original cofactor off s,t.

Slice the original source to a at s,t and b/c everywhere else. Since
only two vertices carry a, diagonality forces their direct a edge.
The exact whole slice is M_a[s,t] F_st, and (1) makes it zero.
As F_st!=0, every M_a[s,t]=0. Hence M_a splits over S,T and

    tau_a=haf(M_a[S]) haf(M_a[T])=0,                       (5)

since each shore has ODD size five. This contradicts (1).

The same argument works at any n=2m>=6 with m odd: a coordinate set
of size m cannot be totally isotropic for both other cofactor forms.
It does not require S to be independent or to be a neighborhood.
At even m the last parity contradiction is unavailable.

## 3. Every color square graph has clique number at most four

The square graph G_h^2 joins distinct vertices whose G_h-distance is
one or two. If L is a clique of G_h^2, neighborhood zeros give

    C_k[L,L]=0                  for each k!=h.            (6)

The diagonal is zero by definition. Since C_k is a nondegenerate
bilinear form on a ten-dimensional space, an isotropic coordinate
subspace has dimension at most five. Thus |L|<=5. Equality is
impossible by Section 2, so

    omega(G_h^2)<=4.                                      (7)

In particular G_h has NO five-cycle: any two vertices of a five-cycle
are at distance at most two along that cycle, so they form a clique
of size five in G_h^2. The cycle need not be induced for this argument.

## 4. A cubic component of size at most ten must now be bipartite

We include the short graph argument to avoid a classification or census.
Let H be any connected cubic component of a color graph, with q<=10
vertices. It has no triangle by the scalar theorem and no five-cycle
by Section 3. If it is not bipartite, choose a shortest odd cycle C
of length g. Then g>=7.

EVERY vertex of H has at most two neighbors on C. For a vertex on C,
a chord of C would split it into two shorter cycles, one odd, which
contradicts minimality. It therefore has exactly its two cycle neighbors.
For a vertex x outside C, suppose three neighbors occur on C. In
cyclic order they cut C into three positive-length arcs. None has
length one, since that would make a triangle through x. Their total
length g is odd, so at least one arc has odd length. The other two
have length at least two, so that odd arc has length at most g-4.
Together with its two incident edges at x it makes an odd cycle of
length at most g-2, again contradicting minimality. This proves the
neighbor bound, including possible chords elsewhere in the graph.

Count ordered incidences from the g cycle vertices to all vertices
of H. Cubicity gives exactly 3g incidences. Counting by their other
endpoint and using the preceding bound gives at most 2q. Thus

    3g <= 2q <= 20,                                      (8)

contrary to g>=7. Hence H is bipartite.

This incidence argument is uniform: a triangle-free cubic nonbipartite
graph with shortest odd cycle length g has at least 3g/2 vertices.
Here its concrete size bound is sufficient; no graph list is used.

## 5. Every possible bipartite cubic component is excluded

A cubic bipartite component has equal shore sizes r,r by counting
its edges. Simplicity gives r>=3. Since its order is at most ten,
the only possibilities are r=3,4,5.

If r=3, the component is K_(3,3). Every pair of its six vertices
has distance at most two, contrary to (7).

If r=4, each vertex misses exactly one vertex of the opposite shore.
These missing pairs constitute a perfect matching, so the component
is exactly the crown K_(4,4) minus a perfect matching. The two remaining
vertices of V must form one isolated h edge: all components have degree
one or three and are disjoint, and a simple graph on two vertices
cannot have degree three. The crown-plus-edge theorem excludes this
case for arbitrary nonzero weights.

If r=5, the component spans V. Two vertices on the same shore have
three neighbors each in a shore of size five; their neighbor sets
must intersect. Consequently either shore is a five-vertex clique
in G_h^2, again contradicting (7).

All possible cubic components are excluded. Every color graph is
therefore a perfect matching on V, with all matching weights nonzero.

## 6. The remaining three matching colors contradict odd shore parity

Take the union of the b and c perfect matchings. Each component is an
alternating even cycle, or a single edge shared by the two matchings.
Equivalently one may keep the two colored copies of a shared edge and
view it as an alternating cycle of length two. Each component admits
a bipartition with equal shore sizes, so their union has a bipartition

    V=U disjoint_union T,       |U|=|T|=5.

Both scalar matrices M_b,M_c are bipartite on these same shores.
Their inverses are supported on their respective matching edges
(with reciprocal weights), so their actual cofactor matrices satisfy

    C_b[U,U]=C_c[U,U]=0.

Section 2 gives the contradiction. No assertion that the union cycle
is connected is needed. No unweighted matching classification, older
physical-degree theorem, or six/eight-site induction input is used.

**Conclusion.** No actual ordinary complex ternary source satisfying
(1) exists on ten vertices, subject to the stated independently
reviewable inputs. This is a proposed research proof pending complete
independent audit, not a formal registry promotion or an all-order
resolution. Its all-order mechanisms leave larger weighted diagonal
sources to be excluded separately.
