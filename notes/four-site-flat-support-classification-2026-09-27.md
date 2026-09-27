# All support graphs with vanishing four-site matching tensors

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** No Lean verification or literature-priority claim is made.

[Replay](../computations/flat-support-structure-2026-09-27/README.md) ·
[Rank-independent star bound](rank-free-star-response-bound-2026-09-27.md) ·
[Five-clique classification](flat-four-response-five-clique-2026-09-27.md)

## 1. Classification

Let $A$ be a complex colored source on any number of sites, with any
finite palette. Its support has edge $ij$ when the block $A_{ij}$ is
nonzero. A site is active if it meets an edge.

**Theorem.** Every source with $\mathcal F_4(A)=0$ belongs to at least
one of these three classes:

1. A source on at most four active sites, whose four-site matching
   tensor vanishes when there are four active sites.
2. A star, with arbitrary colored blocks on its arms and all other
   edges zero.
3. An isolated complete five-site core of the form
   $A_{ij}=c_{ij}v_iv_j^{\mathsf T}$, where $v_i\ne0$ and the scalar
   coefficients are the cube-root pattern:

$$
c_{01}=c_{23}=1,\quad c_{02}=c_{13}=\omega,\quad
c_{03}=c_{12}=\omega^2,\quad c_{i4}=1\ (i<4).
$$

Conversely all three stated classes have $\mathcal F_4=0$.
The classes overlap for small stars. The first class retains the
four-site tensor equation; the theorem does not classify all solutions
of that equation into matrix normal forms.

In particular, a non-star flat source has at most five active sites.
If it has five, its support is complete and every edge block has rank
one with a common local direction at each site.
For real sources, the third class is impossible.

## 2. Reduce the support question to scalar weights

For each site choose a local linear functional. Applying their tensor
product sends each block to a scalar and preserves every four-site
vanishing equation.

These functionals can preserve every nonzero edge: each edge value is
a nonzero polynomial in the functional coordinates. The product over
all support edges is a nonzero polynomial over $\mathbb C$, so some
choice makes all of them nonzero simultaneously.
The projected scalar source therefore has exactly the original graph.

It suffices to classify scalar support graphs. Once the graph is a
five-clique, the prior colored five-clique theorem supplies the stated
matrix structure and isolation.

## 3. A vertex of degree at least three contains all active sites in its closed neighborhood

Work with scalar weights. Let $c$ have distinct neighbors $i,j,k$,
with nonzero weights $g_i,g_j,g_k$, and let $v$ be a nonneighbor of $c$.
Put $h_l=A_{lv}$ for neighbors $l$ of $c$.
The quartet equations on $c,i,j,v$ give

$$
g_i h_j+g_j h_i=0.
$$

The three equations for pairs among $i,j,k$ imply
$2g_i g_j h_k=0$, by multiplying and subtracting as in the
three-leaf identity. Thus $h_k=0$, and then all $h_l=0$.
For any other nonneighbor $w$, the quartet $c,i,v,w$ now gives
$g_iA_{vw}=0$. Therefore $v$ is isolated.

Every active site consequently lies in $\{c\}\cup N(c)$.
This argument needs only three nonzero arms, and uses the full
four-site equations, including those outside the star.

## 4. Classify by maximum degree

If two distinct connected components each contain an edge, their four
endpoints have a unique nonzero matching product, which cannot vanish.
There is at most one component with edges.

If the maximum degree is at most two, this component is a path or a
cycle. A path or cycle on at least five vertices contains four
consecutive vertices with exactly one perfect matching. This is
impossible. Hence there are at most four active sites.

If the maximum degree is three, section 3 confines all active sites
to a set of four.

If the maximum degree is four, section 3 confines all active sites
to the center and its four neighbors. Rescale the four neighbor sites
so their scalar star arms equal one. The four equations containing
the center say that every triangle of leaf-edge weights sums to zero.
Their solutions are opposite pairs

$$
B_{12}=B_{34}=x,\quad B_{13}=B_{24}=y,\quad
B_{14}=B_{23}=z,\qquad x+y+z=0.
$$

The remaining four-site equation says $x^2+y^2+z^2=0$.
Either all are zero, giving a star, or all are nonzero:
if one were zero, the other two would be negatives and their squares
could not sum to zero. In the nonzero case their ratio is
$1:\omega:\omega^2$, up to relabeling and a common scalar.
The support is the complete five-clique.

If the maximum degree is at least five, section 3 confines all active
sites to that star's vertices. The
[star response bound](rank-free-star-response-bound-2026-09-27.md)
forces every leaf edge to vanish. The source is a star.

This exhausts the possibilities. Applying the support-preserving scalar
projection from section 2, followed by the colored five-clique theorem
in the only five-core case, proves the classification. ∎

## 5. Exact six-site census

The replay checks all $2^{15}=32768$ six-site support graphs.

| Class | Count |
| --- | ---: |
| Rejected by a quartet with exactly one matching | 31954 |
| Rejected by the closed-neighborhood lemma | 390 |
| Rejected by the four-leaf scalar equations or the five-leaf star bound | 76 |
| Realized on at most four active sites | 306 |
| Realized larger stars | 36 |
| Realized complete five-cliques | 6 |

All 348 survivors have explicit scalar examples over $\mathbb Q(\omega)$,
including the empty support. The four-site examples assign matching
products $1,-1$ or $1,\omega,\omega^2$ when cancellation is needed.
The enumeration supports the proof; the general theorem follows from
the all-size argument above.

## 6. Application at every full-support single-color boundary

Let a six-site single-ground-color source $A_0$ have all fifteen ground
entries nonzero and zero output. Along a formal path from $A_0$,
suppose the first two output coefficients vanish. The first non-ground
source coefficient $T$ satisfies $\mathcal F_4(T)=0$ by the earlier
mixed-output identity.

Its support cannot contain a five-clique: for every five-site set,
some internal complementary ground cofactor is nonzero, as proved in
section 5 of the
[GHZ normal-form note](ghz-critical-direction-normal-form-2026-09-27.md).
That edge would produce a nonzero first-order output coefficient.

Thus, **at every full-support single-color zero, the first non-ground
critical direction is a star or uses at most four active sites**.
This extends the shape reduction beyond the special rank-25 example.
The cofactor pattern of that example further restricts its possible
star centers to sites $4$ and $5$.

For spanning stars, the quantitative fifth-power source-distance bound
now survives arbitrary matrix rank loss as long as the five arm norms
remain a fixed fraction of $\|T\|$. Remaining cases include disappearing
arms, four-site cores with singular response, and higher-order
cancellations. The unrestricted square-root rate law is still open.
