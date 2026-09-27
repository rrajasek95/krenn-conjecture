# Site balancing reduces the global rate problem

September 26, 2026. **Written proof with exact supporting checks; independent
audit pending.** This result is separate from the Lean-verified exact theorem.

[Replay](../computations/site-balancing-2026-09-26/README.md) ·
[Response bound](balanced-four-site-response-bound-2026-09-26.md) ·
[Illustrated guide](../explainers/SITE-BALANCING.md)

## 1. Definitions and the normalization theorem

Let there be $n=2m$ sites and a finite color palette. Write $A_{ij}$ for
the complex matrix of source entries on edge $ij$, with

$$
 w_{ij}=\|A_{ij}\|_F^2,\qquad
 S=\sum_{i<j}w_{ij},\qquad d_i=\sum_{j\ne i}w_{ij}.
$$

The matching tensor $H(A)$ sums the products of source entries over perfect
matchings, for each output color word. Its degree in $A$ is $m$. Call a
source **balanced** when $d_i=2S/n$ at every site. For nonzero output, the
normalized rate is $R(A)=\|H(A)\|^2/S^m$.

**Theorem.** If the support graph of $A$ contains a perfect matching, delete
every edge block that belongs to no supported perfect matching. The resulting
source has a finite positive site scaling

$$
 B_{ij}=g_i g_j A_{ij},\qquad g_i>0,\qquad \prod_i g_i=1,
$$

where the displayed $A_{ij}$ denotes the retained blocks, such that

$$
 H(B)=H(A_{\rm original}),\qquad S(B)\le S(A_{\rm original}),\qquad
 d_i(B)=2S(B)/n.
$$

It minimizes source strength within the positive scaling orbit of the pruned
source. Consequently it preserves every output fidelity and cannot decrease
normalized rate. Every nonzero-output source satisfies the support hypothesis.
The theorem also applies when output cancels to zero despite a supported
perfect matching.

**Proof.** An edge in no supported perfect matching occurs in no nonzero
matching term. Deleting its entire block therefore preserves $H$. Every
remaining edge belongs to a perfect matching composed entirely of remaining
edges. Positive scaling preserves every matching product: it contributes
exactly the factor $\prod_i g_i=1$.

Put $g_i=e^{x_i}$, $\sum_i x_i=0$. After pruning, minimize the convex function

$$
                 S(x)=\sum_{ij}w_{ij}e^{2(x_i+x_j)}.                 \tag{1}
$$

Take a minimizing sequence whose values are bounded above. All scaled block
norms are bounded above. For any retained edge choose a supported perfect
matching containing it. The product of the block norms along that matching
is invariant and strictly positive. The upper bounds on the other factors
give a positive lower bound on the chosen block norm. Thus every retained
edge sum $x_i+x_j$ stays bounded above and below.

Pass to a subsequence of these finitely many edge sums. The image of the
linear map

$$
 \{x:\sum_i x_i=0\}\longrightarrow\mathbb R^{E},\qquad
 x\longmapsto(x_i+x_j)_{ij\in E}
$$

is a closed linear subspace. Its limiting point therefore comes from a finite
$x_*$, which attains the minimum in (1). This argument does not require
the site variables themselves to be bounded; bipartite components can have
scaling stabilizers.

At a constrained minimum, $\partial_iS=2d_i$ has the same value for every
$i$. Since $\sum_i d_i=2S$, this is precisely balance. Conversely, starting
from a balanced source, $e^t\ge1+t$ gives

$$
 S(x)\ge S+2\sum_i d_i x_i=S.
$$

Thus balance is sufficient as well as necessary for a minimum in the scaling
orbit. Pruning and minimization each weakly decrease the norm. This proves
the theorem. ∎

This is a diagonal scaling argument. Classical matrix scaling provides
related support and attainment results; see
[Sinkhorn and Knopp (1967)](https://msp.org/pjm/1967/21-2/pjm-v21-n2-p14-s.pdf).
The proof above establishes the specific symmetric, product-one statement
needed here directly. We make no priority claim for this normalization.

## 2. Why this is a global proof reduction

At six sites and three target colors, let

$$
 \Delta=a^6+b^6+c^6,\quad
 \lambda=\frac{H_{a^6}+H_{b^6}+H_{c^6}}3,\quad
 E=H-\lambda\Delta,\quad \varepsilon=\|E\|.
$$

The desired homogeneous sharp-rate estimate is

$$
                      |\lambda|^3\le C S^3\varepsilon.           \tag{2}
$$

It suffices to prove (2) for balanced sources with $S=1$, with a constant
uniform over that set. Indeed, for any nonzero-output source, the theorem
produces balanced $B$ with exactly the same $H,\lambda,\varepsilon$ and
$S_B\le S_A$. Applying the normalized estimate to $B/\sqrt{S_B}$, whose
output is $H(B)/S_B^{3/2}$, yields

$$
                |\lambda|^3\le C S_B^3\varepsilon
                             \le C S_A^3\varepsilon.
$$

Zero output satisfies (2) automatically. Conversely, a global estimate
certainly holds on balanced sources. Thus this is an equivalent restricted
proof obligation, not merely a heuristic choice of examples.

For clarity, with $F=3|\lambda|^2/\|H\|^2>0$, (2) implies

$$
 R\le 3\sqrt3 C\frac{\sqrt{1-F}}{F^{3/2}}.
$$

Replacing a source by its balanced representative improves rate at fixed
fidelity. Therefore any violation of a proposed fidelity--rate upper bound
also has a balanced representative violating it.

The normalized balanced set is compact. A sequence in it with $F\to1$
has a convergent subsequence. The limit has zero output, since otherwise it
would be a nonzero exact GHZ source, excluded by the exact Krenn--Gu theorem.
Its site strengths remain $1/3$. The
[sharp response bound](balanced-four-site-response-bound-2026-09-26.md)
shows that its entire first derivative cannot vanish.

In particular, the earlier five-site critical core with an isolated sixth
site cannot be this balanced limit. This does not rule out curved GHZ
approaches to that unbalanced core. Instead it shows that such an approach,
if relevant to a global rate counterexample, has a more efficient balanced
representation whose limiting derivative is nonzero. **Partial rank loss
and cancellation in the target direction remain open.**

## 3. Which balanced supports have no perfect matching?

**Proposition.** At six sites, a balanced nonzero source whose support has no
perfect matching consists of exactly two disconnected triangles. Each of
the six nonzero edge blocks has squared norm $S/6$.

**Proof.** The positive edge weights $x_{ij}=3w_{ij}/S$ satisfy
$\sum_{j\ne i}x_{ij}=1$. They give a fractional perfect matching on the
support. The polytope of such nonnegative weights is nonempty and compact,
so it has an extreme point.

Here is the elementary structure of an extreme point. Its positive-support
incidence columns must be linearly independent: a nontrivial dependence
would allow small positive and negative perturbations preserving all vertex
degrees. A leaf forces its incident edge to have weight one, and hence its
neighbor to have no other positive edge. Thus a component containing a leaf
is a single edge. A remaining connected component has minimum degree two.
Column independence gives at most as many edges as vertices, whereas minimum
degree two gives the reverse inequality. It is therefore a cycle. An even
cycle permits an alternating perturbation and is not extreme; an odd cycle
has all weights $1/2$.

On six vertices, a cover by edges and odd cycles is either three edges or
two triangles. The first would give a perfect matching. Therefore the
original support contains two disjoint triangles. Any edge between them,
together with the opposite edge in each triangle, would give a perfect
matching. There are consequently no other support edges. The three degree
equations in each triangle force all its edge weights to be $S/6$. ∎

This uses the classical extreme-point description of fractional matching
polytopes; see [Behrend, *Fractional Perfect b-Matching Polytopes. I: General
Theory*](https://arxiv.org/abs/1301.7356). The argument above supplies the needed
special case. The replay enumerates all $2^{15}=32,768$ labeled supports:
24,823 contain a perfect matching, and precisely ten contain a fractional
perfect matching without an ordinary one, the ten pairs of triangles.
Enumeration is supporting evidence, not the proof of the extreme-point fact.

Thus balanced zero-output limits have two support possibilities:

- Two equal-strength triangles. The prior regular-triangle theorem covers
  the full-rank cases; rank-deficient triangle responses remain relevant.
- Support containing a perfect matching. Zero output then requires algebraic
  cancellation among supported matching terms or their color components.

The response bound prevents total derivative collapse in both cases.

## 4. Consequence for W-state design

The normalization theorem preserves any output tensor, including $W_n$,
for every even $n$. Global W-rate optimization can therefore be restricted
to pruned balanced sources. It introduces no assumption of a scalar core or
a prescribed number of unrestricted roots.

The known six-site rate-$1/65$ design already satisfies the condition. Its
ten core edges have sole entry $aa=\sqrt{26}$; each of the five edges to
the root has entries $ba=5,ab=1$. Every edge block has squared norm (26),
so $S=390$ and every site has incident strength $130=S/3$.

Balance is a necessary normalization for an optimal design, not a sufficient
optimality criterion. The all-even two-root theorem and the unrestricted
six-site local optimum remain the proved W results; the global unrestricted
optimum is still open.
