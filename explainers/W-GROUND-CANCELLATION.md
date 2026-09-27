# When cancelling ground matchings still cannot improve a W source

September 27, 2026. Written proofs with exact supporting checks; independent
audit pending.

[W project and open target](../research/w-state-design/README.md) ·
[All guides](README.md) ·
[Exact replay](../computations/w-ground-cancellation-2026-09-27/README.md)

A W output has exactly one excited site. Its all-ground output must be zero.
Earlier we proved the known optimum whenever the ground graph has no perfect
matching. Two new results cover families where ground perfect matchings
exist but cancel.

## 1. Adding cancelling ground edges to the optimal core

Start with an odd complete core whose ground edges all have the same weight
$w$. Join the remaining site to its core sites with arbitrary complex ground
weights $z_i$. At six sites the picture is:

~~~mermaid
graph TD
    R["Remaining site 0"]
    subgraph CORE["Five-site core: every internal ground edge has weight w"]
        A["1"] --- B["2"]
        B --- C["3"]
        C --- D["4"]
        D --- E["5"]
        E --- A
        A --- C
        A --- D
        B --- D
        B --- E
        C --- E
    end
    R ---|"z₁"| A
    R ---|"z₂"| B
    R ---|"z₃"| C
    R ---|"z₄"| D
    R ---|"z₅"| E
~~~

Choose the partner of site 0 first. The four remaining core sites can be
matched in three ways, each of weight $w^2$. The ground output is therefore

$$
3w^2(z_1+z_2+z_3+z_4+z_5).
$$

It vanishes exactly when the five added weights sum to zero. All fifteen
ground edges can be nonzero, so this is actual cancellation between
supported matchings.

Could these extra ground edges make the desired W output cheaper? We can
now answer this for **every even site count at least six**: they cannot.
The known rate remains optimal in this class, and any nonzero added ground
strength gives a strict loss.

The argument allows arbitrary additional colored entries on every edge.
Fixing the ground core does not fix the rest of the design.

## 2. Why the extra responses do not pay for their cost

For each excited site, the possible incident excitation entries form a
linear response row. Its coefficients are matching sums on the remaining
sites. A larger row can produce a given W amplitude with less source
strength, by Cauchy–Schwarz.

~~~mermaid
flowchart LR
    A["Add cancelling ground edges"] --> B["Some excitation responses become larger"]
    A --> C["Ground source strength increases"]
    B --> D["Exact response-row formulas"]
    C --> D
    D --> E["At n ≥ 6, the strength cost always wins in this core family"]
~~~

At six sites, let $x$ be added ground strength divided by core ground
strength. The bound is

$$
R\le\frac1{65}\,
\frac{13(3+4x)}{(1+x)^2(39+2x)}.
$$

At $x=0$ this is $1/65$, attained by the known design. The factor decreases
strictly as $x$ grows. For example, at $x=1$ the upper bound is $7/820$,
about $55.5\%$ of the known optimum.

The [all-even proof](../notes/w-state-coherent-odd-core-2026-09-27.md)
computes the response rows, sums their minimum strength requirements, and
proves this monotonicity. Four sites behave differently: the corresponding
response relaxation can improve, but its unwanted outputs remain to be
cancelled. The theorem explicitly starts at six sites.

## 3. A second family is uniformly below the optimum

Take four sites in a cycle, with common complex ground weight $s$. One
additional site joins all four with weight $u$; another joins them with
alternating weights $v,-v,v,-v$. Leave the edge between the two additional
sites and the two cycle diagonals absent.

The ground graph is an octahedron when all three parameters are nonzero.
Its ground matching terms cancel for every complex choice of $s,u,v$.

For this family, allowing every colored completion still gives

$$
R<\frac{2}{135}=\frac{26}{27}\,\frac1{65}.
$$

The proof reduces the rate bound to positivity of one quartic polynomial.
Its coefficients in two interval bases are all positive, and its remaining
tail also has positive coefficients. The
[exact proof](../notes/w-state-octahedral-ground-gap-2026-09-27.md)
lists those coefficients, so no numerical minimizer is needed.

This family contains the earlier example where isolating a ground site by
local shears increases source strength. That normalization failure is real,
but this separate bound excludes the family from improving the optimum.

## 4. The remaining problem

~~~mermaid
flowchart TD
    A["Ground perfect matchings cancel"] --> B{"Ground-core structure"}
    B --> C["Uniform odd core plus arbitrary root couplings"]
    C --> D["Known optimum proved for every even n ≥ 6"]
    B --> E["Six-site octahedral family"]
    E --> F["Strict rate gap below 1/65"]
    B --> G["Other, nonuniform ground cores"]
    G --> H["Unrestricted optimization remains open"]
~~~

Ground cancellation alone does not guarantee an advantage. In these two
families we can quantify its cost. The remaining task is to control
nonuniform ground cores beyond these formulas, or find an exact design
that beats the proposed optimum.
