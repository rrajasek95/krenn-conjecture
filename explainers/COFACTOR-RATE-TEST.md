# A square-root test that survives response rank loss

[All explainers](README.md) · [GHZ project](../research/ghz-rates/README.md) ·
[Proof](../notes/cofactor-square-root-rate-2026-09-28.md) ·
[Exact replay](../computations/cofactor-square-root-rate-2026-09-28/README.md)

We can now prove a local square-root rate bound at every balanced
single-color six-site zero, including singular sources.
The same argument improves the unrestricted six-site exponent from
$1/15$ to $1/14$. The universal square-root target remains open.

**Evidence:** written proof with exact supporting checks; independent
audit pending. These results are separate from the Lean-verified exact theorem.

## What the square-root question asks

Write the matching output as

$$
H=\lambda\Delta+E.
$$

Here $\Delta$ is the sum of the three same-color GHZ words, $\lambda$
is their average amplitude, and $E$ is the remaining error. After
normalizing source strength, the desired estimate is

$$
\|E\|\ge c|\lambda|^3.
$$

It says that error cannot disappear arbitrarily fast relative to the
signal. Using the definitions of fidelity and rate converts this into
$R\le C\sqrt{1-F}/F^{3/2}$.

A local theorem permits the constant to depend on a fixed limiting
source. The universal theorem needs one constant covering every source.

## Multiply an edge matrix by its matching cofactors

For a same-color source, collect its edge weights in a symmetric
six-by-six matrix $D$. Its diagonal is zero.

For each pair of sites, remove those sites and add the three matching
products on the four remaining sites. Put this number in a second
matrix $C$, again with zero diagonal. These numbers are the matching
cofactors.

~~~mermaid
flowchart LR
    A["Scalar edge matrix D"] --> B["Delete each pair of sites"]
    B --> C["Four-site matching sums form C"]
    A --> E["Compute D C"]
    C --> E
    E --> F{"Nonzero at the zero-output source?"}
    F -->|"Yes"| G["Local square-root bound"]
    F -->|"No"| H["Test is inconclusive"]
~~~

**If $DC\ne0$ at a zero-output source, the square-root bound holds
throughout a neighborhood**, including arbitrary complex, colored
perturbations. There is an analogous test using nine matrix products
for general three-color sources.

The full theorem also gives a numerical certificate at each source,
but its constants are very conservative.

## An example the regular-response theorem missed

Take two separate triangles, with all six edges of one color and weight one:

~~~mermaid
flowchart LR
    A["0"] ---|"1"| B["1"]
    B ---|"1"| C["2"]
    C ---|"1"| A
    D["3"] ---|"1"| E["4"]
    E ---|"1"| F["5"]
    F ---|"1"| D
~~~

There is no perfect matching on all six sites, so the output is zero.
Each triangle response has rank seven, below the rank-nine condition
in the earlier theorem.

Nevertheless,

$$
DC=
\begin{pmatrix}
0&2\mathbf1\\
2\mathbf1&0
\end{pmatrix}\ne0,
$$

where each block is three-by-three and $\mathbf1$ is the all-ones block.
The new test therefore proves a local square-root bound.

A second exact example is a signed source on the octahedral graph.
Its matching terms cancel, and it passes the previous star support
test, but $DC\ne0$ again. The proof and replay give its twelve weights.

## Why this covers every balanced single-color limit

There are two cases. If the support has no perfect matching, balance
forces exactly the two triangles just discussed. Their matrix product
is nonzero even when the six nonzero weights have arbitrary complex phases.

If the support has a perfect matching, scale its three weights to one.
Twelve complex edge weights remain free. An exact algebraic certificate
shows that the entries of $DC$ cannot all vanish: their polynomial
combinations would otherwise imply $1=0$.

The saved certificate has 244 steps. Each step adds polynomial
multiples of earlier expressions, and the final expression is exactly
one. The checker replays these steps using rational arithmetic; it
does not rely on a numerical solver's report of failure.

~~~mermaid
flowchart TD
    A["Balanced single-color source"] --> B{"Perfect matching in its support?"}
    B -->|"Yes"| C["Polynomial certificate forces D C nonzero"]
    B -->|"No"| D["Two triangles force D C nonzero"]
    C --> E["Local square-root law"]
    D --> E
~~~

This covers every scalar source-matrix rank. The uniform constant
near the normalized balanced single-color zero set follows from
compactness; we do not yet have a useful numerical value for it.

## Why the polynomial estimate improves

The proof uses an auxiliary polynomial $g$ and the residual

$$
g(s/\sqrt2)^2-g(s).
$$

The previous estimate allowed the coefficients of $g$ to become large
as the physical signal vanished. It compensated by shrinking the
auxiliary variable range, which weakened the final rate bound.

The new observation is that a small residual already bounds the
coefficients of $g$. A polynomial's square has quadratic growth in
its coefficient size; the other terms have only linear growth.
Once that size is bounded, one fixed rescaling works.

~~~mermaid
flowchart TD
    A["Small polynomial residual"] --> B["Uniform bound on polynomial coefficients"]
    B --> C["Fixed auxiliary rescaling"]
    C --> D["Stronger cubic-response estimate"]
    D --> E["Nonzero cofactor product gives local square-root law"]
    D --> F["Sharper diagonal reduction gives global exponent 1/14"]
~~~

This improves an estimate within the existing proof method. It does
not assume that a singular response matrix becomes invertible.

## What remains

Any sequence beating every square-root constant must approach a
balanced zero-output source where **all nine matrix–cofactor products
vanish**. All higher odd binary responses must vanish there too.

The new certificate rules out every balanced single-color limit as
a source of square-root violations. Remaining candidates involve
more than one target color, and no individual color's support may
contain a perfect matching.

The test can be inconclusive at a source where the square-root law
still holds: the familiar prism is an example. We must still analyze
the remaining common zeros of these equations. The new global
exponent $1/14$ is stronger than $1/15$, but remains well short of $1/2$.
