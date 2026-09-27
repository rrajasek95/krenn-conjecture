# Why the GHZ signal starts so slowly near a full-support single-color zero

[All explainers](README.md) · [GHZ project](../research/ghz-rates/README.md) ·
[Written proof](../notes/full-support-ghz-onset-2026-09-27.md) ·
[Exact replay](../computations/full-support-ghz-onset-2026-09-27/README.md)

We now have a uniform fifth-power onset bound at every six-site
full-support single-color zero. Every nearby source direction is
included, even when edge matrices lose rank.

**Evidence:** written proof with exact supporting checks; independent
audit pending. The unrestricted square-root rate law remains open.

**Subsequent result:** the [star fidelity certificate](GHZ-STAR-FIDELITY-GAP.md)
now excludes every such zero as a high-fidelity limit, giving the stronger
local bound $\varepsilon\ge c|\lambda|$. This guide preserves the onset
argument and its reusable response geometry.

## What the statement means

Start with a source $A_0$ that uses only one color, $a$.
“Full support” means every pair of sites has a nonzero ground
amplitude. Despite that, its six-site output is zero because the
matching terms cancel.

Now perturb the source and compare its output with the GHZ target:

$$
H(A)=\lambda(a^6+b^6+c^6)+E.
$$

Here $\lambda$ is the desired signal amplitude, $\varepsilon=\|E\|$
measures the output error, and $\delta=\|A-A_0\|$ measures how far
the source has moved. The theorem says

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5.}
$$

The constants depend on the fixed ground source, but not on the
direction of the perturbation. If the error is much smaller than
the signal, the signal cannot grow faster than a constant times
the fifth power of source distance.

The result includes the single-cell directions that earlier
response tests could not control. It imposes no matrix-rank
condition and no requirement that several edges stay comparably large.

## How the graph organizes the proof

Delete an edge's two endpoints and add the matching amplitudes
on the other four sites. The result is its **ground cofactor**.
A nonzero cofactor forces the binary part of that edge to be
small, of order $\delta^2$, when the output is close to GHZ.
Such edges are called anchors.

The ground equations make the weighted sum of cofactor edges
at every vertex zero. A minimal nonempty pattern of these edges
must be one of four shapes:

~~~mermaid
flowchart TD
    A["Ground cofactor equations"] --> B["Four possible minimal anchor patterns"]
    B --> C["Four-cycle"]
    B --> D["Six-cycle"]
    B --> E["Two triangles meeting at a vertex"]
    B --> F["Two triangles joined by a bridge"]
    C --> G["Project away a large outside edge"]
    D --> H["Response equations produce a controlled four-cycle"]
    E --> I["Four small arms leave one removable product"]
    F --> J["Rescale a four-cycle and control its attachments"]
    G --> K["Uniform fifth-power onset"]
    H --> K
    I --> K
    J --> K
~~~

An elementary incidence-matrix argument proves this list.
An independent exact check also covers all 32,768 labelled
six-vertex graphs. The final two arguments are explained below.

## A projection removes the last large term in the four-cycle case

Suppose four anchored edges form a cycle on sites $2,3,4,5$.
Their binary blocks are small. The two other edges within those
four sites can initially be larger:

~~~mermaid
flowchart LR
    A["2"] --- C["4"]
    A --- D["5"]
    B["3"] --- C
    B --- D
    A ==>|"U: possibly large"| B
    C -.->|"V"| D
~~~

The four ordinary lines are anchors. Choose $U$ to be the larger
of the two remaining blocks. The quartet output equation forces
$V$ to be small, unless the error is already large enough to
prove the desired bound.

An exact rearrangement writes the full output as a product
containing $U$, plus terms that are already small. Project the
two-site output at $2,3$ perpendicular to $U$. This removes the
whole large product.

Crucially, this projection cannot remove the whole GHZ target.
At least half of its binary squared norm remains. The surviving
output is bounded by

$$
(\text{source size})\times(\delta^2)^2
\le\delta^5.
$$

The edge between the other two sites may vanish completely;
the argument does not divide by it.

## A balanced four-cycle has no hidden attachment direction

For the bridge configuration, the proof first separates easy
small-edge cases. In the remaining case, positive scaling factors
at the six sites expose a nearly flat four-cycle.
Their product is one, so every six-site matching amplitude is
unchanged: each matching uses every site exactly once.

A representative balanced cycle has scalar weights

~~~mermaid
flowchart LR
    A["0"] ---|"1"| B["1"]
    A ---|"1"| D["3"]
    B ---|"1"| C["2"]
    C ---|"-1"| D
~~~

Its two matching products cancel. All four edge norms are one.
Let $X$ collect the attachments from a new outside site to this
core, and let $M X$ collect the quartet responses they produce.
The exact identity is

$$
\boxed{\|M X\|^2=2\|X\|^2.}
$$

It holds for colored edge matrices in any finite local dimensions,
with the stated balanced flat-cycle hypotheses.
Every attachment is visible to the response, with the same
norm factor. A nearby core retains a uniform lower bound.

The proof then scales each original output equation by its
correct site factor. Terms involving the unknown attachments
have a small coefficient and can be moved to the left side of
the inequality. Both outside attachment collections become
small. The matching expansion gives the fifth-power bound.

## What this completes, and what it does not

The full-support single-color onset problem now has no remaining
critical directions. The earlier stars, triangles, rank-one
edges, and ground-cofactor cases are all covered.

For the unrestricted square-root rate law, the missing comparison
is still

$$
\varepsilon\ge c|\lambda|^3
$$

after source normalization at the remaining relevant limits.
The onset theorem by itself bounds the signal using source distance.
The subsequent [star certificate](GHZ-STAR-FIDELITY-GAP.md) supplies
a stronger direct error bound near every full-support single-color zero
and excludes this entire class. Other zero-output limits that pass
the new support test remain relevant.
