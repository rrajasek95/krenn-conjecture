# GHZ fidelity and production rate

[All subprojects](../README.md) · [Illustrated rate guide](../../explainers/RATE-FOLLOWUPS.md)

The exact Krenn–Gu theorem forbids a nonzero perfect GHZ output in the
stated setting. This project asks how much rate is lost when the output is
only approximately GHZ.

**Status:** written proofs with exact supporting checks; independent audit
pending. The unrestricted six-site square-root rate law remains open.

## The question

For a source on $n=2m$ sites, let $H$ be its matching-amplitude output and
$S$ the sum of the squared absolute values of its edge entries. We use the
scale-invariant rate $R=\lVert H\rVert^2/S^m$. At six sites, $F$ is fidelity
with the three-color GHZ target.

The target is a constant $C$, independent of the complex source, such that
$R\le C\sqrt{1-F}$ near $F=1$. Here “unrestricted” permits arbitrary complex
colored edge entries. The normalization is mathematical; translating it
into a laboratory count rate requires a physical source model.

## Results and proof packages

| Result | What it establishes | Read and reproduce |
| --- | --- | --- |
| Explicit unrestricted rate bound | A six-site exponent of $1/15$; the diagonal model has exponent $1/5$. | [Rate follow-ups](../../explainers/RATE-FOLLOWUPS.md), [proof](../../notes/rate-sharpness-followup-2026-09-26.md), [replay](../../computations/rate-sharpness-followup-2026-09-26/README.md) |
| Square-root laws in controlled settings | A cancellation hypothesis gives exponent $1/2$. The prism also has a full complex neighborhood bound and an optimal leading coefficient. | [Design guide](../../explainers/RATE-DESIGN-FRONTIER.md), [prism proof](../../notes/prism-optimal-rate-2026-09-26.md), [replay](../../computations/rate-design-frontier-2026-09-26/README.md) |
| Regular two-triangle limits | Full-rank triangle responses lead to a fidelity gap or a local square-root bound. | [Boundary guide](../../explainers/BOUNDARY-STRUCTURE.md), [classification](../../notes/regular-triangle-rate-classification-2026-09-26.md), [replay](../../computations/boundary-structure-2026-09-26/README.md) |
| Reduction to balanced sources | Site scaling preserves output and improves rate. A sharp response identity excludes complete derivative collapse at a balanced six-site limit. | [Balancing guide](../../explainers/SITE-BALANCING.md), [proof](../../notes/site-balancing-rate-reduction-2026-09-26.md), [replay](../../computations/site-balancing-2026-09-26/README.md) |
| Classification of triangle rank loss | Triangle ranks are 7, 8, or 9; the two-triangle derivative has rank at least 49. A separate balanced, full-support example has rank 25. | [Frontier guide](../../explainers/BALANCED-FRONTIER.md), [proof](../../notes/triangle-response-rank-classification-2026-09-27.md), [replay](../../computations/balanced-frontier-2026-09-27/README.md) |
| Higher-order identities at full-support single-color limits | An analytic path with leading GHZ output starts at parameter order at least $m+2$ on $2m$ sites, hence at least five on six sites. | [Proof and quantitative remainder bound](../../notes/full-support-single-color-jets-2026-09-27.md), [replay](../../computations/full-support-jets-2026-09-27/README.md) |

The last result concerns powers of an analytic path parameter. It does not
give a uniform fifth-power bound in distance, or establish the square-root law.

## What remains

Balancing narrows the possible zero-output limits:

~~~mermaid
flowchart TD
    A["Balanced six-site zero-output limit"] --> B{"Support has a perfect matching?"}
    B -->|No| C["Two triangles"]
    C --> D{"Both responses have full rank?"}
    D -->|Yes| E["Fidelity gap or local square-root law"]
    D -->|No| F["Open: compare higher-order error with signal"]
    B -->|Yes| G["Open: matching terms cancel"]
    G --> H["Full-support single-color identities constrain initial orders"]
~~~

At six sites write $H=\lambda\Delta+E$, where $\Delta$ is the sum of the
three monochromatic words and $E$ is orthogonal to it. After normalizing
$S=1$, the missing estimate is $\lVert E\rVert\ge c|\lambda|^3$, uniformly
through the remaining singular limits. A large response in some direction
does not yet control the GHZ direction.

Earlier higher-order analyses are preserved in the
[critical-cone](../../computations/critical-cone-2026-09-26/README.md),
[higher-jet](../../computations/higher-order-2026-09-26/README.md), and
[extension-obstruction](../../computations/critical-extension-search-2026-09-26/README.md)
packages. The [project-wide replay](../README.md#reproduce-the-follow-up-checks)
checks these together with the current results.
