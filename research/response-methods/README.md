# Response identities, certificates, and source reconstruction

[All subprojects](../README.md) · [Illustrated methods guide](../../explainers/METHOD-UTILITY.md)

A matching-output derivative has a concrete meaning: changing one source
entry leaves a smaller matching problem on the other sites. This connects
the exact proof to design optimization, stability estimates, and source
recovery.

**Evidence:** the rate and design tools below have written proofs and exact
supporting checks, with independent audit pending. Source-reconstruction
notes describe their own hypotheses and evidence. These follow-ups are
separate from the Lean-verified exact theorem.

## Tools and applications

| Tool | Useful consequence | Read and reproduce |
| --- | --- | --- |
| Circle averaging at a homogeneous polynomial zero | Convert a polynomial norm bound into a sharp derivative bound on its zero set. For hafnians this yields a universal factor-two W-design guarantee and explicit higher-response losses. | [Lemma and application](../../notes/w-state-universal-factor-two-2026-09-27.md), [illustrated guide](../../explainers/W-GLOBAL-GUARANTEE.md), [replay](../../computations/w-universal-factor-two-2026-09-27/README.md) |
| Equality along the derivative circle and a transverse Hessian | Classify every maximum-response ground source at even sizes from six onward, quantify ground/cofactor overlap, and exclude high-efficiency competitors through a local scalar inequality. | [Proof](../../notes/w-cofactor-rigidity-2026-09-27.md), [replay](../../computations/w-cofactor-rigidity-2026-09-27/README.md) |
| Constrained curvature at a balanced cancellation source | An exact decomposition identifies a second six-site scalar local minimum with 21 positive directions. It excludes another complete-support family and reveals an obstruction to proving global optimality by local descent alone. | [Proof and quadratic forms](../../notes/w-state-balanced-three-plus-three-2026-09-27.md), [replay](../../computations/w-balanced-cancellation-2026-09-27/README.md) |
| Matching counts as orthogonal polynomials | Legendre roots and quadrature weights solve the equal-split response problem. Gegenbauer roots extend the reduction to unequal groups, with a sextic stationary equation at every size and exact interval certificates for whole parameter families. | [Equal-split proof](../../notes/w-state-equal-split-legendre-2026-09-27.md), [general two-group reduction](../../notes/w-state-two-group-reduction-2026-09-27.md), [replay and certificates](../../computations/w-two-group-reduction-2026-09-27/README.md) |
| Response Gram matrices and exact dual certificates | Optimize a fixed core; bound two output requirements at once; account for core uncertainty. | [Proof](../../notes/reusable-response-certificates-2026-09-26.md), [method replay](../../computations/method-utility-2026-09-26/README.md), [fixed-core replay](../../computations/rate-design-frontier-2026-09-26/README.md) |
| Symmetry decompositions and higher-order feasibility constraints | Prove unrestricted local W optimality at every even size; at four sites, higher equations eliminate negative Hessian modes that no feasible path can follow to first order. | [All-even quadratic forms](../../notes/w-state-all-even-local-optimum-2026-09-27.md), [four-site obstruction](../../notes/w-state-four-site-local-obstruction-2026-09-27.md), [replay](../../computations/w-all-even-local-optimum-2026-09-27/README.md) |
| Positive site scaling | Preserve the entire output while reducing source strength; reduce both global rate problems to balanced sources. | [Illustrated guide](../../explainers/SITE-BALANCING.md), [proof](../../notes/site-balancing-rate-reduction-2026-09-26.md), [replay](../../computations/site-balancing-2026-09-26/README.md) |
| Four-site response norm identity | A sharp balanced six-site bound, a quantitative measure of imbalance, and an exclusion of complete derivative collapse. | [Proof](../../notes/balanced-four-site-response-bound-2026-09-26.md), [replay](../../computations/site-balancing-2026-09-26/README.md) |
| Polynomial rate certificates and arc tests | Verify an exact algebraic certificate or a proposed violating path; turn a rate claim into a checkable identity. | [Proof](../../notes/integral-rate-certificates-2026-09-26.md), [replay](../../computations/method-utility-2026-09-26/README.md) |
| Paired-hafnian stability estimates | Quantitative control in the paired-hafnian setting under the stated hypotheses. | [Proof](../../notes/paired-hafnian-application-2026-09-26.md), [replay](../../computations/rate-sharpness-followup-2026-09-26/README.md) |
| Full-support higher-order identities | Relate higher GHZ coefficients to lower mixed coefficients; restrict when a leading GHZ output can appear. | [Proof](../../notes/full-support-single-color-jets-2026-09-27.md), [replay](../../computations/full-support-jets-2026-09-27/README.md) |
| Flat-core rigidity and a sharp star identity | Classify complete five-site cores and invertible binary four-site cores; control distance to smooth critical families; quantify extra leaf-edge strength at invertible stars. | [Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md), [five-core proof](../../notes/flat-four-response-five-clique-2026-09-27.md), [star and binary-core proof](../../notes/star-response-identity-and-binary-flat-cores-2026-09-27.md), [replay](../../computations/flat-core-rigidity-2026-09-27/README.md) |
| Complete flat-support classification and rank-independent star control | Reduce all four-site-flat supports to stars, at most four active sites, or isolated five-cores. Bound extra leaf edges using nonzero arm norms, even when every arm has rank one. | [Support proof](../../notes/four-site-flat-support-classification-2026-09-27.md), [tensor-lifting estimate](../../notes/rank-free-star-response-bound-2026-09-27.md), [replay](../../computations/flat-support-structure-2026-09-27/README.md) |
| Four-arm kernels and additional output constraints | Classify all hidden leaf-response directions and identify a sharp square-root distance obstruction. Mixed GHZ outputs recover a fifth-power onset bound when the fifth arm disappears. | [Response proof](../../notes/four-arm-star-response-2026-09-27.md), [GHZ application](../../notes/four-arm-ghz-distance-bound-2026-09-27.md), [replay](../../computations/four-arm-ghz-boundary-2026-09-27/README.md) |
| Attachment control at singular four-site cores | Classify every hidden extension to a fifth site without an internal normal form. Control the two outside sites to obtain a fifth-power GHZ onset estimate near every non-star four-site core. | [Proof](../../notes/four-core-attachment-ghz-bound-2026-09-27.md), [replay](../../computations/four-core-attachments-2026-09-27/README.md) |
| Pairwise attachment control and a local target projection | A forbidden five-site extension bounds products of attachment sizes. Projecting a shared local factor removes the remaining large output and gives fifth-power GHZ onset through every triangle rank loss. | [Proof](../../notes/triangle-attachment-ghz-bound-2026-09-27.md), [replay](../../computations/triangle-ghz-onset-2026-09-27/README.md) |
| Weighted five-site extension control | Separate rescaling of internal leaf edges and an outside arm converts the flat-support obstruction into a product estimate. A leaf-sensitive mixed-output bound then gives GHZ onset from only three comparable arms. | [General lemma and GHZ theorem](../../notes/three-arm-ghz-distance-bound-2026-09-27.md), [replay](../../computations/three-arm-ghz-onset-2026-09-27/README.md) |
| Singular-value separation of different tensor pairings | A matrix of rank at least two bounds cancellation against a differently paired product. This classifies two-arm attachment kernels and proves GHZ onset with two uniformly invertible arms. | [Estimate, sharpness, and GHZ application](../../notes/two-invertible-arm-ghz-bound-2026-09-27.md), [replay](../../computations/two-arm-ghz-onset-2026-09-27/README.md) |
| Weighted triangle rescaling and complementary response maps | Rescale a weak closing edge without losing the useful output scale. A local projection proves GHZ onset for every uniformly injective two-arm map; a complementary map isolates the closing-edge contribution at shared-center rank-one pairs. | [Proof and projection example](../../notes/transverse-two-arm-ghz-onset-2026-09-27.md), [replay](../../computations/transverse-two-arm-ghz-2026-09-27/README.md) |
| Two controlled attachments and a size dichotomy | Keep each outside-arm size in the complementary response estimate. A large hidden third attachment forces the other center arms to shrink; small hidden attachments permit triangle rescaling. This closes the remaining two-arm onset case. | [Refined estimates and proof](../../notes/coherent-two-arm-ghz-onset-2026-09-27.md), [exact scalar certificates and tensor checks](../../computations/coherent-two-arm-ghz-2026-09-27/README.md) |
| Matching-tensor source reconstruction | Recover source information under the stated response and direction hypotheses; distinguish single-copy from multiple-copy information. | [Matching tensors and copies](../../notes/matching-tensor-recovery-and-multiple-copies-2026-09-26.md), [two-direction reconstruction](../../notes/two-direction-source-reconstruction-2026-09-26.md) |
| Two observed Gaussian cross moments | Generically recover both mean rows and all cross-site covariance blocks at five sites of local dimension at least four, up to product-one site scalings. | [Theorem and proof](../../notes/two-observation-source-reconstruction-2026-09-27.md), [reconstruction](../../computations/matching-tensor-recovery-2026-09-26/pair_observation.py), [independent matrix audit](../../computations/matching-tensor-recovery-2026-09-26/audit_pair_observation.py) |
| Calibrated response spans at all odd orders | Retaining actual output coefficients removes the covariance ambiguity in the all-orders span theorems; one calibrated output suffices from order seven once the span is known. | [Theorem, calibration thresholds, and fifth-order involution](../../notes/calibrated-source-reconstruction-all-orders-2026-09-27.md), [exact replay](../../computations/matching-tensor-recovery-2026-09-26/calibrated_span.py) |
| One observed Gaussian cross moment | At local dimensions at least three, generically recover means and cross-site covariance from one tensor at every odd order at least seven; five sites have exactly two classes, resolved by two shared-source outputs. | [All-orders theorem and shared-source corollary](../../notes/single-cross-moment-all-orders-2026-09-27.md), [five- and seven-site inverse](../../computations/matching-tensor-recovery-2026-09-26/single_source.py) |
| Mean directions from one tensor at every odd order | Generically identify every local mean line for all odd orders at least five, using a two-site attachment induction; also covers generic unknown response coefficients. | [Written proof and limits](../../notes/mean-direction-recovery-all-orders-2026-09-27.md), [symbolic and exact checks](../../computations/matching-tensor-recovery-2026-09-26/mean_direction_induction.py) |
| Mean directions from two commutator kernel conditions | Recover generic mean lines by exact linear algebra at every odd order from three onward; the same criterion identifies generic compression centers beyond matching tensors. Complete the retained nine-site failed-search source. | [All-orders witness, broader theorem, and limits](../../notes/slice-commutator-mean-recovery-2026-09-27.md), [inverse](../../computations/matching-tensor-recovery-2026-09-26/slice_mean_recovery.py), [independent audit](../../computations/matching-tensor-recovery-2026-09-26/verify_slice_mean_recovery.py), [certificate](../../computations/matching-tensor-recovery-2026-09-26/slice-mean-recovery-certificate.json) |
| Observable noisy mean-direction certificates | Use the stacked commutator equations and exact residual checks to constrain the local means of every source in a stated data-error ball, without a nearby source guess. Certified examples cover three, five, and seven sites. | [Finite-error theorem and limits](../../notes/observable-noisy-mean-recovery-2026-09-27.md), [proposal and exact acceptance](../../computations/matching-tensor-recovery-2026-09-26/slice_noise_recovery.py), [replay with separate matrix assembly](../../computations/matching-tensor-recovery-2026-09-26/verify_slice_noise_recovery.py), [certificate](../../computations/matching-tensor-recovery-2026-09-26/slice-noise-recovery-certificate.json) |
| Covariance recovery from a restricted exterior kernel | Replace full-kernel completion by a map with cubically many columns; a two-site induction proves the necessary rank at every odd order at least seven. | [Rigidity criterion](../../notes/single-output-covariance-low-degree-2026-09-27.md), [all-orders rank proof](../../notes/single-cross-moment-all-orders-2026-09-27.md), [exact induction checks](../../computations/matching-tensor-recovery-2026-09-26/covariance_induction.py) |
| Source inverse given the local mean lines | Recover covariance and actual mean scales with quadratically many columns per linear system; exact nine-site examples align four outputs spanning four global mean directions in local dimension three. | [Smaller rank criterion and scope](../../notes/quadratic-size-source-inverse-2026-09-27.md), [inverse and replay](../../computations/matching-tensor-recovery-2026-09-26/restricted_source_inverse.py), [certificate](../../computations/matching-tensor-recovery-2026-09-26/restricted-source-inverse-certificate.json) |
| Blind search and local conditioning | Search for mean lines from the tensor alone, then verify them exactly; complete rational source recovery on seven- and nine-site examples, mean-line recovery at eleven sites, and a retained failed search. | [Proofs, local noise bound, and limits](../../notes/blind-source-search-and-local-conditioning-2026-09-27.md), [search and exact verification](../../computations/matching-tensor-recovery-2026-09-26/blind_mean_search.py), [certificate](../../computations/matching-tensor-recovery-2026-09-26/blind-mean-search-certificate.json) |
| Shared calibration and near-ambiguity | Prove all-orders seventh-order separation and fifth-order local covariance obstructions; shared cubic calibration has a sharp sensitivity formula and a classical tight-frame setting-design criterion. | [Theorems and scope](../../notes/shared-calibration-and-near-ambiguity-2026-09-27.md), [exact replay](../../computations/matching-tensor-recovery-2026-09-26/source_calibration_conditioning.py), [certificate](../../computations/matching-tensor-recovery-2026-09-26/source-calibration-conditioning-certificate.json) |
| Certified full-source initialization | Bound every mean and covariance parameter compatible with noisy full-tensor data, then certify entry into the local correction neighborhood. A seven-site exact example passes at an extremely small error budget; practical thresholds remain open. | [Proof and limitations](../../notes/certified-full-source-initialization-2026-09-27.md), [certificate generator](../../computations/matching-tensor-recovery-2026-09-26/full_source_noise_recovery.py), [exact replay](../../computations/matching-tensor-recovery-2026-09-26/verify_full_source_noise.py), [saved certificate](../../computations/matching-tensor-recovery-2026-09-26/full-source-noise-certificate.json) |
| Certified shared-source alignment and mean spaces | Align independently recovered observations with rigorous scaling-error bounds; enclose all shared means and edges, certify a joint correction ball, and bound the observed mean span. A four-observation seven-site example recovers rank four; a sparse complex ambiguity identifies a necessary boundary. | [Theorems, graph criterion, and limitations](../../notes/certified-shared-source-alignment-2026-09-27.md), [generator](../../computations/matching-tensor-recovery-2026-09-26/shared_source_noise_recovery.py), [exact replay](../../computations/matching-tensor-recovery-2026-09-26/verify_shared_source_noise.py), [certificate](../../computations/matching-tensor-recovery-2026-09-26/shared-source-noise-certificate.json) |
| Full-source local stability | Bound finite errors in all means and edge parameters, prove a local correction iteration converges, and control the observed mean span. Shared covariance information adds even with unknown means. | [Theorems and limits](../../notes/full-source-local-stability-2026-09-27.md), [certificate generator](../../computations/matching-tensor-recovery-2026-09-26/source_local_stability.py), [independent replay](../../computations/matching-tensor-recovery-2026-09-26/verify_source_local_stability.py), [exact witnesses](../../computations/matching-tensor-recovery-2026-09-26/source-local-stability-certificate.json) |
| Products of local scalar measurements | Apply established structured-measurement theory to identify generic sources from `d+1` scalar data, where `d` is the source dimension; certify local source rank and finite noise bounds through eleven sites without constructing full tensors. | [Measurement counts, attribution, and limits](../../notes/product-measurement-source-recovery-2026-09-27.md), [direct scalar computation](../../computations/matching-tensor-recovery-2026-09-26/product_measurements.py), [independent replay](../../computations/matching-tensor-recovery-2026-09-26/verify_product_measurements.py), [certificate](../../computations/matching-tensor-recovery-2026-09-26/product-measurement-certificate.json) |

The matching-tensor reconstruction programs are
[verify.py](../../computations/matching-tensor-recovery-2026-09-26/verify.py),
[multi_copy.py](../../computations/matching-tensor-recovery-2026-09-26/multi_copy.py),
and [two_direction.py](../../computations/matching-tensor-recovery-2026-09-26/two_direction.py).
Their saved certificates sit alongside the programs. Consult the linked
proofs for the exact scope; a response computation alone is not a general
identifiability theorem.

The subsequent [many-direction theorem](../../notes/many-direction-source-reconstruction-2026-09-27.md)
treats three or more independent mean directions. The
[support-graph extension](../../notes/sparse-source-graph-reconstruction-2026-09-27.md)
recovers a generic connected source graph under the stated matching and
local-independence hypotheses, and removes the mean-quadratic ambiguity when
the graph is not complete. These use spans of outputs; their specific
span-based algorithms have no measurement-noise guarantees. The local
joint-source bounds below concern a different estimator. Reproduction
commands are in the linked notes.

The [two-observation result](../../notes/two-observation-source-reconstruction-2026-09-27.md)
uses a three-copy exterior identity to recover the unobserved response
space from two tensors. Their coefficients then determine a covariance
representative by rational operations. Its proof excludes degenerate
alternative mean pairs and is supported by exact reconstruction and an
independent Pfaffian calculation. The pair-matrix rank is established at
five sites; overlapping coordinate projections extend recovery to arbitrary
local dimensions at least four. The later
[one-direction result](../../notes/one-direction-source-reconstruction-2026-09-27.md)
improves the five-site local-dimension requirement to three and recovers
the response space from a single seven-site tensor. It also proves
one-direction covariance rigidity from a supplied span at every odd
order at least five. These are written research results with exact
certificates, separate from the Lean formalization of Krenn–Gu.

The [calibration theorem](../../notes/calibrated-source-reconstruction-all-orders-2026-09-27.md)
upgrades the all-orders span results, including one mean direction, to
recovery of the actual means and covariance blocks. It also proves that
two observations are necessary at five sites.
The [mean-direction induction](../../notes/mean-direction-recovery-all-orders-2026-09-27.md)
now recovers the local mean lines at all odd orders at least five without
assuming span completion. The
[covariance induction](../../notes/single-cross-moment-all-orders-2026-09-27.md)
now completes full generic recovery at every odd order at least seven,
including alignment of any finite family with a shared covariance.
These are written all-orders proofs supported by exact base and deformation
certificates. The earlier exact linear blind inverse implementation covers five
and seven sites. With local mean lines supplied, the
[smaller inverse](../../notes/quadratic-size-source-inverse-2026-09-27.md)
now recovers covariance and mean scales at nine sites, including a shared
source with four observed mean directions. A subsequent
[blind search](../../notes/blind-source-search-and-local-conditioning-2026-09-27.md)
now verifies complete rational sources at seven and nine sites from raw
tensors alone. It supplies local mean-line noise bounds and records a
failed search. The later
[full-source analysis](../../notes/full-source-local-stability-2026-09-27.md)
gives finite local noise bounds for all source parameters and a certified
convergence neighborhood for a separate correction iteration. A later
[slice-commutator algorithm](../../notes/slice-commutator-mean-recovery-2026-09-27.md)
recovers generic mean lines by exact linear algebra at every odd order
from three onward, and completes the retained nine-site failed-search
source. Its all-orders proof uses a fixed nine-dimensional calculation
and tensor powers, and extends to generic compression centers beyond
matching tensors. Combined with covariance recovery, it removes the
nonlinear initialization step for generic exact full-tensor data from
order seven. The later certificate below addresses full-source initialization
with measurement noise under explicit, conservative acceptance conditions.
Inversion from compressed scalar data and nongeneric source classification remain
open. These research results are not part of the Lean formalization of Krenn–Gu.

The subsequent [noisy mean-direction certificate](../../notes/observable-noisy-mean-recovery-2026-09-27.md)
now supplies the mean-line part of initialization from noisy full tensors.
It accounts for solve and vector residuals and covers all matching
representations compatible with a given data-error bound. It uses
established singular-vector perturbation and verified-numerics principles
with the new observable stack. The subsequent
[full-source initializer](../../notes/certified-full-source-initialization-2026-09-27.md)
propagates those errors through covariance recovery and scalar calibration,
then checks that every compatible source lies in the local correction ball.
Its seven-site example uses an error budget of about `3.4e-41`: it closes
the logical single-observation initialization step on the stated open set,
not the problem of useful noise thresholds. The saved numerical proposal
effectively sees rounded clean data; acceptance uses the exact noisy data.
The subsequent [shared-source certificate](../../notes/certified-shared-source-alignment-2026-09-27.md)
now aligns separate recovery gauges, encloses every compatible common covariance
and all observed means, and certifies a joint correction neighborhood. It gives
a rank-four observed mean space from four seven-site tensors, with exact error
and angle bounds. These examples still use noise below double precision.
Useful thresholds and validated floating correction remain open. A graph
criterion separates unique complex scaling alignment from finite ambiguities
on sparse bipartite graphs.

The [calibration-conditioning results](../../notes/shared-calibration-and-near-ambiguity-2026-09-27.md)
give explicit obstructions to uniformly stable covariance recovery and
show how shared observations improve the remaining scale calibration
once the response frame and covariance class are fixed. The full-source
local bounds use the joint forward derivative, without assuming that
intermediate inverse steps are error-free. They also control the span of
observed mean vectors and quantify shared covariance information after
eliminating the unknown means. Their source neighborhoods and noise
thresholds are explicit and conservative; they do not give uniform
global recovery. Recovery of the earlier failed-search input instead uses
the subsequent exact slice algorithm.

The [product-measurement application](../../notes/product-measurement-source-recovery-2026-09-27.md)
separates the number of scalar data from the full tensor's exponential
size. An existing theorem of Gesmundo–Grosdos–Uschmajew gives generic
source identifiability from one more product measurement than the source
dimension. Shared covariance and a known bound on global mean rank reduce
that dimension further. Twice the dimension generically preserves every
distinction between model tensors. Exact local checks cover seven, nine,
and eleven sites; their particular finite probe lists are not certified
globally injective. These counts do not give a sample-complexity bound or
an efficient global reconstruction algorithm. A classical degree bound
also forces exponentially many complex candidates when enumerating all
solutions of a generic square subsystem; this favors using the extra
measurements directly instead of enumerating and filtering every candidate.

With generic unknown response coefficients instead of the calibrated
Gaussian coefficients, [Corollary 10](../../notes/single-cross-moment-all-orders-2026-09-27.md#7-completing-the-theorem-and-shared-source-recovery)
still recovers the complete one-direction response space from a single
tensor at every odd order at least five. Covariance scale and mean-square
addition then remain genuine ambiguities.

## How the projects connect

~~~mermaid
flowchart LR
    A["Matching-output identities"] --> B["Smaller matching responses"]
    B --> C["Gram matrices and exact certificates"]
    B --> D["Site balancing and norm identities"]
    B --> E["Source reconstruction"]
    C --> F["W-state design and fixed-core optimization"]
    D --> F
    D --> G["GHZ boundary and rate analysis"]
    C --> G
~~~

The [GHZ project](../ghz-rates/README.md) and
[W-state project](../w-state-design/README.md) state the unresolved targets.
The [shared replay](../README.md#reproduce-the-follow-up-checks) checks the
34 rate, design, and shared-method packages without numerical optimization dependencies.
