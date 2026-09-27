# What the difficult GHZ directions can look like

[All explainers](README.md) · [GHZ project](../research/ghz-rates/README.md) ·
[Proofs and exact replay](../computations/flat-core-rigidity-2026-09-27/README.md)

We can now describe several families of perturbations that initially
hide from the matching output, and measure how close a nearby source is
to those families. At the explicit rank-25 boundary example, we can also
classify all possible support graphs of its first critical direction.

**Evidence:** written proofs with exact supporting checks; independent
audit pending. These are follow-ups to the completed Krenn–Gu proof.
The unrestricted GHZ square-root rate law remains open.

## Start with the smaller matching problem

On four sites, there are three perfect matchings:

$$
12|34,\qquad 13|24,\qquad 14|23.
$$

Each edge carries a matrix of amplitudes for its two endpoint colors.
For a fixed color at each site, multiply the two entries belonging to
each matching and add the three products. Repeating this for every
color choice gives the four-site matching tensor.

Write $\mathcal F_4(A)$ for all these tensors on all four-site subsets.
We call a source **four-site-flat** when every one is zero.
This means the matching terms cancel for every color choice.

Why study this smaller problem? A six-site amplitude is a sum of products
of three edge entries. Differentiating with respect to one entry leaves
the matching tensor on the other four sites. Thus $\mathcal F_4$ records
the first response of the six-site output to edge changes.

~~~mermaid
flowchart LR
    A["Six-site output: products of three edges"] --> B["Vary one edge"]
    B --> C["Four remaining sites: products of two edges"]
    C --> D{"Do all these responses vanish?"}
    D -->|Yes| E["Higher-order terms become essential"]
    D -->|No| F["Some changes are detected to first order"]
~~~

## Three families we can describe precisely

The new theorems do not classify every four-site-flat source. They
classify complete five-site cores, complete invertible binary four-site
cores, and sources containing an invertible spanning star.

| Family | What vanishing forces | Local freedom at six sites, in two colors |
| --- | --- | ---: |
| Complete five-site core | Every edge has rank one; incident edges share a local color direction. The sixth site is isolated. | 10 complex parameters |
| Complete four-site core with invertible two-by-two blocks | All blocks reduce to a fixed identity/antisymmetric pattern by local changes of basis. Both other sites are isolated. | 13 complex parameters |
| Star with five invertible two-by-two arms | Every edge between the leaves is zero. | 20 complex parameters |

“Invertible” means the matrix has no lost color direction. The parameter
counts describe the flat family inside the 60-dimensional space of binary
six-site edge entries; they are separate from the original rank-25 count
for a three-color six-site output derivative.

The five-site pattern uses the complex cube roots of unity:

$$
1+\omega+\omega^2=0.
$$

Its edges among sites $0,1,2,3$ come in opposite pairs with weights
$1,\omega,\omega^2$. The four edges to site $4$ have weight $1$.
These phases cancel every four-site matching sum. The classification
proves that any complete five-site flat core must have this form after
local changes of scale and color direction. There is no corresponding
complete real-weight five-site flat core.

The four-site exception uses

$$
I=\begin{pmatrix}1&0\\0&1\end{pmatrix},
\qquad J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
$$

~~~mermaid
graph LR
    a["0"] ---|"I"| b["1"]
    a ---|"I"| c["2"]
    a ---|"I"| d["3"]
    b ---|"J"| c
    b ---|"-J"| d
    c ---|"J"| d
    e["4: isolated"]
    f["5: isolated"]
~~~

All six core blocks are invertible, yet the four-site output vanishes.
This is why a proof cannot assume that all flat sources use rank-one
edge blocks.

## The star identity gives an explicit measure of error

Take a center joined to $k$ leaves, with identity matrices on its arms,
and $q$ colors at each site. Let $B_{ij}$ be any extra block between
leaves. Orient it by $B_{ji}=B_{ij}^{\mathsf T}$.

The total squared norm of four-site outputs containing the center is
exactly

$$
T_\star=
\underbrace{[q(k-2)-2]\sum_{i<j}\|B_{ij}\|_F^2}_{\text{detects extra edges}}
+\underbrace{\sum_i\left\|\sum_{j\ne i}B_{ij}\right\|_F^2}_{\text{nonnegative correction}}.
$$

For six sites and two colors, the first coefficient is $4$. Therefore
small output response forces small total strength in the extra edges.
No choice of their complex phases can remove that first term.
An antisymmetric triangle attains the coefficient, so it is sharp.

Arbitrary invertible arms can be changed to identities. The resulting
bound includes their largest and smallest singular values, which measure
how much they stretch or compress vectors. This exposes the remaining
difficulty: the estimate deteriorates when an arm loses rank.

## At the rank-25 boundary, only two support shapes survive

The earlier work found a balanced, single-color source with all fifteen
edges present and zero output. Its derivative has rank 25, leaving many
directions undetected at first order.

Consider a path from this source whose first two output orders vanish.
Let $T$ be the first perturbation using only the two other colors.
First-order constraints remove edges $02,03,12,13$ from $T$.
Second-order constraints impose $\mathcal F_4(T)=0$.
Together they force:

~~~mermaid
flowchart TD
    A["First non-ground direction at the rank-25 example"] --> B["Four forbidden edges are zero"]
    B --> C["Every four-site matching tensor vanishes"]
    C --> D["Support uses at most four sites"]
    C --> E["Support is a star centered at 4 or 5"]
    D --> F["All six binary core blocks invertible: classified and locally stable"]
    E --> G["All five arms invertible: explicit star estimate"]
    D --> H["Rank-deficient or sparse cases still require analysis"]
    E --> H
~~~

The proof uses a short cancellation obstruction. If three leaves each
connect to both centers, their pairwise equations would imply a nonzero
product equals zero. Hence at most two such leaves can occur.
If each leaf connects to just one center, all must choose the same one.

The exact replay exhausts the 2048 allowed edge subsets. It excludes
1932 and constructs flat scalar examples on each of the 116 survivors.
The support proof itself allows arbitrary colored blocks.

## From a shape theorem to a quantitative estimate

Near each nondegenerate family, the response controls distance to an
exactly flat source:

$$
\operatorname{dist}(T,\{\mathcal F_4=0\})
\le C\,\frac{\|\mathcal F_4(T)\|}{\|T\|}.
$$

This has practical meaning: a small measured response puts the source
close to a known family, with a stated bound on the discrepancy.
The constant is uniform on compact collections that stay away from
rank loss and disappearing core edges.

For a source $A$ near a full-support single-color zero $A_0$, write

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\quad
\varepsilon=\|E\|,\quad \delta=\|A-A_0\|.
$$

If its non-ground direction is near one of the specified smooth
families, the new estimate gives

$$
|\lambda|\le C_1\varepsilon+C_2\delta^5.
$$

This uses actual source distance. Unlike an order statement for a path
parameter, it is unaffected by describing the same path with a slower
parameter. A separate dense five-site support condition gives a
sixth-power bound and rules out a five-clique as the nonzero first
non-ground jet at these full-support limits.

To finish the universal square-root law, we still need
$\varepsilon\ge c|\lambda|^3$ across every relevant boundary.
The new results identify and control several difficult families, but a
bound involving $\delta$ does not by itself give that error-versus-signal
comparison. Rank-degenerate directions and later cancellations remain
substantive work.
