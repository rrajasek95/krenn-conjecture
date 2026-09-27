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
| Critical directions and local distance bounds | Classify every support of the first non-ground critical direction at the rank-25 example. Smooth core and star families give a uniform fifth-power source-distance estimate; dense five-site directions give a sixth-power estimate. | [Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md), [support classification](../../notes/rank25-critical-directions-2026-09-27.md), [distance bounds](../../notes/ghz-critical-direction-normal-form-2026-09-27.md), [replay](../../computations/flat-core-rigidity-2026-09-27/README.md) |
| All flat supports and stars through matrix rank loss | Every full-support single-color zero has only star or at-most-four-site first critical directions. A bound using arm norms extends the fifth-power estimate to spanning stars of any matrix rank. | [All-size support theorem](../../notes/four-site-flat-support-classification-2026-09-27.md), [rank-independent bound](../../notes/rank-free-star-response-bound-2026-09-27.md), [replay](../../computations/flat-support-structure-2026-09-27/README.md) |
| Onset through the loss of one star arm | Four non-ground arms bounded below relative to the non-ground source norm suffice for a uniform fifth-power distance estimate. A complete four-arm kernel classification identifies the hidden directions and a sharp square-root response obstruction. | [Kernel geometry](../../notes/four-arm-star-response-2026-09-27.md), [GHZ distance theorem](../../notes/four-arm-ghz-distance-bound-2026-09-27.md), [replay](../../computations/four-arm-ghz-boundary-2026-09-27/README.md) |
| Onset at every non-star four-site core | Control the two outside sites without resolving internal singularities. Only a cube-root core can hide an attachment, and a ground-cofactor constraint removes that kernel. The fifth-power estimate is uniform away from triangles and stars with at most three arms. | [Attachment theorem and GHZ application](../../notes/four-core-attachment-ghz-bound-2026-09-27.md), [replay](../../computations/four-core-attachments-2026-09-27/README.md) |
| Onset at every full triangle through rank loss | Pairwise attachment control and a local GHZ projection extend the fifth-power estimate to all triangles. The combined estimate is uniform away from stars with at most three arms. | [Triangle theorem](../../notes/triangle-attachment-ghz-bound-2026-09-27.md), [replay](../../computations/triangle-ghz-onset-2026-09-27/README.md) |
| Three comparable arms suffice for onset | A weighted extension estimate handles every three-arm pattern, including zero center cofactor rows. The fifth-power estimate is now uniform away from stars with at most two arms. | [Three-arm theorem and reusable extension lemma](../../notes/three-arm-ghz-distance-bound-2026-09-27.md), [replay](../../computations/three-arm-ghz-onset-2026-09-27/README.md) |
| Two uniformly invertible arms suffice for onset | A singular-value estimate and ground cofactors give fifth-power onset. One invertible arm also suffices when its endpoint cofactor rows meet the stated condition. | [Two-arm theorem and kernel classification](../../notes/two-invertible-arm-ghz-bound-2026-09-27.md), [replay](../../computations/two-arm-ghz-onset-2026-09-27/README.md) |
| Two-arm onset beyond invertibility | An injective attachment map suffices, uniformly away from rank loss. This removes the endpoint-cofactor condition for one invertible arm and covers rank-one arms with different center lines. At shared-center pairs, an explicit residual bound isolates the closing-edge contribution. | [Rescaled-triangle proof and residual estimate](../../notes/transverse-two-arm-ghz-onset-2026-09-27.md), [replay](../../computations/transverse-two-arm-ghz-2026-09-27/README.md) |
| Two comparable arms suffice at every matrix rank | Retaining individual outside-arm sizes and using two ground-selected anchors closes the shared-center rank-one case. The fifth-power onset estimate is now uniform away from single-edge directions. | [Two-anchor theorem and corollary](../../notes/coherent-two-arm-ghz-onset-2026-09-27.md), [replay](../../computations/coherent-two-arm-ghz-2026-09-27/README.md) |
| A single uniformly invertible edge suffices for onset | A bilinear response lemma and a sharp determinant-tangent projection handle the decay of every other edge. The combined estimate is uniform away from single rank-one edge directions. | [Single-edge theorem and projection gap](../../notes/single-invertible-edge-ghz-onset-2026-09-27.md), [replay](../../computations/single-invertible-edge-ghz-2026-09-27/README.md) |
| A same-color edge component suffices for onset | A binary adjugate identity gives a sharp quadratic response certificate without matrix-rank assumptions. The combined estimate is uniform away from thirty projective directions, each supported on one different-color cell. | [Identity, norm certificate, and onset theorem](../../notes/binary-adjugate-ghz-onset-2026-09-27.md), [replay](../../computations/binary-adjugate-ghz-2026-09-27/README.md) |
| Ground-cofactor tests through single-edge rank loss | A common anchored neighbor or an outside anchored four-cycle suffices at every matrix rank. This covers both zero endpoint cofactor rows and reduces the thirty candidates according to the ground source; the exact sparse fixture leaves sixteen. | [Balanced-response proof and cofactor criteria](../../notes/balanced-response-ghz-onset-2026-09-27.md), [replay](../../computations/balanced-response-ghz-2026-09-27/README.md) |
| Two anchor configurations contain the remaining full-support onset problem | Four anchored arms or a six-cycle of anchors settles every nearby source direction. An exhaustive cofactor-graph classification leaves only a four-cycle with isolated sites, its complete-four-vertex extension, or two triangles joined by a bridge. At most sixteen projective directions remain, and both residual anchor configurations have exact ground examples. | [Classification and analytic rules](../../notes/cofactor-graph-ghz-frontier-2026-09-27.md), [complete graph replay](../../computations/cofactor-graph-frontier-2026-09-27/README.md) |

The earlier higher-order identities concern an analytic path parameter.
The new distance bounds are uniform under their stated family or arm-size
hypotheses. None establishes the unrestricted square-root law.

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
    H --> I["Every such limit: first critical support uses at most four sites or is a star"]
    I --> J["Fifth-power onset: arm, edge, and ground-cofactor criteria"]
    I --> K["Remaining onset: different-color cells in two anchor configurations"]
    J --> L["Still open: error-versus-signal estimate"]
    K --> L
~~~

At six sites write $H=\lambda\Delta+E$, where $\Delta$ is the sum of the
three monochromatic words and $E$ is orthogonal to it. After normalizing
$S=1$, the missing estimate is $\lVert E\rVert\ge c|\lambda|^3$, uniformly
through the remaining singular limits. A large response in some direction
does not yet control the GHZ direction.

At a full-support single-color zero, the
[latest classification](../../notes/cofactor-graph-ghz-frontier-2026-09-27.md)
leaves at most sixteen projective directions. All are pure different-color
single cells in two remaining anchor configurations: an edge from a
four-cycle to an isolated cofactor vertex, or an edge between the
non-bridge vertices of two triangles joined by a bridge.
An anchored edge has nonzero ground hafnian cofactor.
The complete-four-vertex cofactor case is covered by the same
remaining four-cycle problem.
All other cofactor graphs already give fifth-power onset in every
nearby source direction. With exactly one zero cofactor row, no onset
directions remain; with no zero rows, at most eight remain.
The error-versus-signal bound remains open even in the families whose
onset is now controlled.

Earlier higher-order analyses are preserved in the
[critical-cone](../../computations/critical-cone-2026-09-26/README.md),
[higher-jet](../../computations/higher-order-2026-09-26/README.md), and
[extension-obstruction](../../computations/critical-extension-search-2026-09-26/README.md)
packages. The [project-wide replay](../README.md#reproduce-the-follow-up-checks)
checks these together with the current results.
