# The remaining full-support onset problem has two anchor configurations

September 27, 2026. **Written proof and exact exhaustive graph certificate;
independent audit pending.** The unrestricted square-root rate law remains open.

[Replay](../computations/cofactor-graph-frontier-2026-09-27/README.md) ·
[Illustrated guide](../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../research/ghz-rates/README.md)

## 1. The ground-cofactor graph determines the remaining shapes

Let $A_0$ be a six-site source using only ground color $a$, with
all ground entries $D_{ij}$ nonzero and $\operatorname{haf}D=0$.
For a nearby ternary source put

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\quad
\varepsilon=\|E\|,\quad \delta=\|A-A_0\|,\quad
d=\delta^2,\quad t=\|T\|\le\delta,
$$

where $T$ is its binary non-ground part.
The **cofactor graph** $\Gamma_D$ contains edge $ij$ exactly when
$c_{ij}=\operatorname{haf}D[V\setminus\{i,j\}]\ne0$.
Such an edge is anchored: its binary block is $O(\varepsilon+d)$.

**Theorem.** Unless $\Gamma_D$ has one of the following three forms,
every source in a neighborhood of $A_0$ obeys

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5.}
\tag{1}
$$

| Exceptional cofactor graph | Remaining candidate edges | Projective directions |
| --- | --- | --- |
| A four-cycle and two isolated vertices | Between an isolated vertex and a cycle vertex | 16 |
| A complete four-vertex graph and two isolated vertices | Between an isolated vertex and an active vertex | 16 |
| Two triangles joined by one bridge | Between non-bridge vertices in different triangles | 8 |

For an exceptional graph, (1) is uniform when $T=0$ or the normalized
direction stays a fixed positive distance from a pure $bc$ or $cb$
cell on one of the displayed edges. Each such complex coordinate
line counts as one projective direction.

Consequently, **at most sixteen directions remain at any fixed
full-support single-color ground zero**. If at most one cofactor
row is zero, at most eight remain; with exactly one zero row,
none remain. This concerns onset, not the rate-law error exponent.

The complete four-vertex graph contains a four-cycle. Thus it would
suffice to prove the missing onset estimate in just **two anchor
configurations**, up to relabelling and interchange of $b,c$:

1. A four-cycle of ground anchors, with the substantial binary
   edge joining one cycle vertex to one of the two other sites.
2. Two anchored triangles joined by an anchored bridge, with the
   substantial binary edge joining non-bridge vertices across
   the two triangles.

The first problem allows additional anchors between the four active
vertices; proving only the case where both cycle diagonals have
zero cofactors would not, by itself, settle the complete-four case.

These are families with continuous ground coefficients and arbitrary
perturbations, not two isolated numerical examples. The displayed
directions are not counterexamples; they are where the present tests stop.

## 2. Two additional analytic rules

As in the [balanced-response proof](balanced-response-ghz-onset-2026-09-27.md),
the cases $T=0$, $\varepsilon>td$, or $t=O(d)$ follow from
$|\lambda|\le\varepsilon+15t^3$. Otherwise

$$
\varepsilon\le td,\qquad f:=\|\mathcal F_4(T)\|\le Ctd,
$$

and every anchored block is $O(d)$.

**Four small arms.** If some vertex $r$ has four incident binary
blocks of size $O(d)$, then (1) holds. Let $rj$ be its only
possibly larger edge. The matching expansion at $r$ is

$$
H_6(T)=T_{rj}\mathcal F_{V\setminus\{r,j\}}(T)
+\sum_{k\ne r,j}T_{rk}\mathcal F_{V\setminus\{r,k\}}(T).
$$

If $T_{rj}\ne0$, project the two-site space at $r,j$ perpendicular
to that block viewed as a vector. This removes the first term.
The other four terms have total norm $O(df)=O(td^2)$.
A projection perpendicular to one core vector retains at least
squared binary GHZ norm one. If the exceptional block is zero,
the unprojected estimate suffices. This proves (1).
In particular, **any cofactor vertex of degree at least four
gives the onset estimate for every nearby source**.

**Propagation from two anchors.** Fix a substantial block
$G=T_{ij}$ with $\|G\|\ge\eta t$. For two outside sites $r,s$,
the quartet response is

$$
F_{ijrs}=G T_{rs}+T_{ir}T_{js}+T_{is}T_{jr}.
\tag{2}
$$

If $ir,is$ are anchored, both products after the first contain
an $O(d)$ factor, and hence $\|T_{rs}\|=O(d)$. The same holds
if $jr,js$ are anchored. Thus the controlled outside edges include

$$
\Gamma_D[L]\ \cup\
\binom{N_{\Gamma_D}(i)\cap L}{2}\ \cup\
\binom{N_{\Gamma_D}(j)\cap L}{2},\qquad
L=V\setminus\{i,j\}.
\tag{3}
$$

If this enlarged outside graph contains a four-cycle, (1) follows.
The four-cycle proof in sections 5--6 of the balanced-response note
requires only that its four blocks be $O(d)$; it does not otherwise
use their nonzero ground cofactors. Equation (2) supplies exactly
the same hypotheses for the added edges. No matrix-rank condition
is imposed on $G$.

The previous common-anchored-neighbor criterion remains available.
An anchored substantial edge itself gives $t=O(d)$.

## 3. A six-cycle of anchors settles every source direction

Suppose $\Gamma_D$ contains a cycle through all six vertices.
Choose a largest binary block, so $\|G\|\ge t/\sqrt{15}$.
If its endpoints are adjacent on that cycle, it is anchored.
If their cycle distance is two, they have a common anchored
neighbor. Both cases are already covered.

For opposite endpoints, label them $0,1$ and write the anchored
cycle as

$$
0-2-3-1-4-5-0.
$$

The anchors at 0 make $25$ small by (2), and those at 1 make
$34$ small. Together with anchored edges $23,45$, these give
the outside four-cycle $2-3-4-5-2$. The propagated four-cycle
criterion applies. These are all pairs of vertices on the cycle,
so (1) holds for every nearby source.

## 4. Which graphs can be cofactor graphs?

The hafnian expansion at every vertex gives

$$
\sum_{j\ne i}D_{ij}c_{ij}=0.
\tag{4}
$$

Set $w_{ij}=D_{ij}c_{ij}$ on $\Gamma_D$. Every displayed edge
weight is nonzero. Thus the graph admits nonzero complex edge
weights whose sum at every vertex is zero.
The graph is nonempty by the
[ground cofactor fact](ghz-critical-direction-normal-form-2026-09-27.md).
Equation (4) is a necessary condition; the graph test does not
assume every graph passing it is realized by a ground source.

Let $B_\Gamma$ be the unsigned vertex-edge incidence matrix,
with two entries equal to one in each edge column.
If $b(\Gamma)$ counts bipartite connected components, including
isolated vertices, then over $\mathbb C$

$$
\operatorname{rank}B_\Gamma=6-b(\Gamma).
\tag{5}
$$

Indeed, the left-kernel equations are $z_i+z_j=0$ on every edge.
A connected bipartite component permits one alternating constant;
an odd cycle forces that constant to zero.

An edge coordinate can be nonzero in $\ker B_\Gamma$ exactly
when deleting that column leaves the rank unchanged.
Over the infinite field $\mathbb C$, finitely many proper
coordinate hyperplanes cannot cover the kernel. Therefore
there is a kernel vector nonzero on **every** edge precisely when

$$
b(\Gamma-e)=b(\Gamma)\quad\hbox{for every edge }e.
\tag{6}
$$

This makes admissibility an exact finite graph test.

There is an independent description. Any minimal nonempty support
of such weights is one of:

- an even cycle;
- two odd cycles meeting at one vertex;
- two odd cycles joined by a path.

Here is a proof sufficient for six vertices. Minimal support is
connected and has no vertex of degree one. Its incidence kernel
is one-dimensional: otherwise a linear combination of two kernel
vectors can cancel one edge without cancelling them all.
In the bipartite case (5) gives as many edges as vertices, so it
is an even cycle. In the non-bipartite case there is one more
edge than vertex. Following paths through vertices of degree two
leaves either two cycles meeting at a vertex, two cycles joined
by a path, or three paths between two vertices. The last form
contains a proper even cycle because two of the three path
lengths have the same parity. Minimality excludes it.
Both remaining cycles must be odd, or one even cycle would
already be a proper admissible support.

On at most six vertices the list is consequently just a four-cycle,
a six-cycle, two triangles meeting at a vertex, or two triangles
joined by one edge. Every edge of an admissible graph is in a
minimal support of this kind. To see this, minimize support among
kernel vectors whose selected edge is nonzero; any smaller
kernel support omitting that edge could be subtracted to reduce it
further. Conversely, if these supports cover all edges, a generic
linear combination of their nonzero weight vectors is nonzero
on every edge.

## 5. Complete finite classification

The replay exhausts all $2^{15}=32{,}768$ labelled simple graphs
on six vertices. It checks (6) against the independent union of
all 285 labelled minimal supports, each with an explicit integer
kernel vector:

| Minimal support | Labelled instances |
| --- | ---: |
| Four-cycle | 45 |
| Six-cycle | 60 |
| Two triangles meeting at one vertex | 90 |
| Two triangles joined by one edge | 90 |

There are 10,099 nonempty admissible supports. After removing
graphs with a vertex of degree at least four or a six-cycle,
the exact list is:

| Remaining graph type | Labelled instances |
| --- | ---: |
| Four-cycle and two isolated vertices | 45 |
| Complete four-vertex graph and two isolated vertices | 15 |
| Complete bipartite graph with parts of size two and three, plus one isolated vertex | 60 |
| Two triangles joined by one edge | 90 |

The bipartite type is also fully controlled. Edges among its five
active vertices are anchored or have a common anchored neighbor.
For an edge from the isolated site to a vertex in the part of
size three, its outside graph already contains a four-cycle.
For an edge to a vertex in the part of size two, rule (3) adds
the triangle on its three neighbors; the other vertex in the
part of size two is connected to all three, yielding an outside
four-cycle again.

The classifier then applies the substantial-edge tests to every
edge of every remaining graph. The only unhandled pairs are
exactly those in the theorem's table.
For the three exceptional types, the previous two-arm, invertible-edge,
and same-color criteria leave only the stated different-color
single-cell directions. The compactness argument in the
[adjugate proof](binary-adjugate-ghz-onset-2026-09-27.md) gives
uniformity away from them.

This is a complete finite classification of the necessary graph
condition, not a random search over ground coefficients.
The analytic implications use sections 2--3 and the earlier
written response proofs. Independent audit of the combined chain
is still pending.

## 6. Both residual anchor configurations occur

The existing exact ground fixture has cofactor graph
$02,03,12,13$, a four-cycle with isolated vertices 4 and 5.
Its eight isolate-to-cycle edges give sixteen projective directions.
Thus the universal upper count sixteen is attained by the present
tests at a genuine full-support ground zero.

The bridge configuration also has a full-support **real** ground
example. Take internal ground edges on triangles $\{0,1,2\}$ and
$\{3,4,5\}$ all equal to one. Set their cross-edge matrix to

$$
B=\begin{pmatrix}
a&h&h\\ h&e&e\\h&e&e
\end{pmatrix},\quad
2h^4+5h^2-1=0,\quad h>0,\quad
a=h^{-1}-3h,\quad e=-\frac1{2h}.
\tag{7}
$$

The positive root obeys $0<h^2<1/4$, so every entry is nonzero.
Put $s=h^{-1}-h>0$. The internal cofactors are

$$
c_{01}=c_{02}=c_{34}=c_{35}=-s,\qquad c_{12}=c_{45}=s.
$$

Among cross edges, only
$c_{03}=1+1/(2h^2)$ is nonzero.
For example $1+2he=0$ and
$1+ae+h^2=(2h^4+5h^2-1)/(2h^2)=0$
give all eight other cross-cofactor cancellations.
The expansion at vertex 1 gives $\operatorname{haf}D=-s+s=0$.
The cofactor graph is precisely the two triangles joined by $03$.
The four pairs $14,15,24,25$ remain, giving eight projective directions.

The replay verifies (7) and every matching/cofactor identity exactly
in the quotient by $2h^4+5h^2-1$, using rational arithmetic.
The inequalities above identify the intended real root and show
that the source has full support.

## 7. What is still missing

Two anchor configurations now contain the entire remaining
full-support single-color **onset** problem. Neither has yet
been controlled near its pure different-color edge directions.
Even completing (1) in those families would not establish the
error-versus-signal inequality $\varepsilon\ge c|\lambda|^3$.
Other zero-output boundary types also remain relevant to the
unrestricted rate law. The W-state global optimum is a separate
open target.
