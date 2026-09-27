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
| Matching-tensor source reconstruction | Recover source information under the stated response and direction hypotheses; distinguish single-copy from multiple-copy information. | [Matching tensors and copies](../../notes/matching-tensor-recovery-and-multiple-copies-2026-09-26.md), [two-direction reconstruction](../../notes/two-direction-source-reconstruction-2026-09-26.md) |
| Two observed Gaussian cross moments | Generically recover both mean rows and all cross-site covariance blocks at five sites of local dimension at least four, up to product-one site scalings. | [Theorem and proof](../../notes/two-observation-source-reconstruction-2026-09-27.md), [reconstruction](../../computations/matching-tensor-recovery-2026-09-26/pair_observation.py), [independent matrix audit](../../computations/matching-tensor-recovery-2026-09-26/audit_pair_observation.py) |
| Calibrated response spans at all odd orders | Retaining actual output coefficients removes the covariance ambiguity in the all-orders span theorems; one calibrated output suffices from order seven once the span is known. | [Theorem, calibration thresholds, and fifth-order involution](../../notes/calibrated-source-reconstruction-all-orders-2026-09-27.md), [exact replay](../../computations/matching-tensor-recovery-2026-09-26/calibrated_span.py) |
| One observed Gaussian cross moment | At local dimensions at least three, generically recover the full source from one seven-site tensor; classify the two five-site possibilities and recover a shared source from two five-site tensors. | [Written proofs and scope](../../notes/one-direction-source-reconstruction-2026-09-27.md), [reconstruction](../../computations/matching-tensor-recovery-2026-09-26/single_source.py), [independent matrix audit](../../computations/matching-tensor-recovery-2026-09-26/audit_single_source.py) |
| Mean directions from one tensor at every odd order | Generically identify every local mean line for all odd orders at least five, using a two-site attachment induction; also covers generic unknown response coefficients. | [Written proof and limits](../../notes/mean-direction-recovery-all-orders-2026-09-27.md), [symbolic and exact checks](../../computations/matching-tensor-recovery-2026-09-26/mean_direction_induction.py) |
| Covariance recovery from a restricted exterior kernel | Replace full-kernel completion by a map with cubically many columns; an exact nine-site rank certificate gives full generic source recovery from one nine-site tensor. | [Criterion and nine-site theorem](../../notes/single-output-covariance-low-degree-2026-09-27.md), [rank-certificate replay](../../computations/matching-tensor-recovery-2026-09-26/three_outside_certificate.py) |

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
the graph is not complete. These use spans of outputs; measurement-noise
stability remains open. Their reproduction commands are in the linked notes.

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
[restricted-kernel theorem](../../notes/single-output-covariance-low-degree-2026-09-27.md)
then recovers the covariance directly at nine sites. Its replay certifies
the required rank, while the written argument proves global uniqueness;
it is not a full blind reconstruction implementation. Full single-output
source recovery at arbitrary odd orders at least eleven remains open.

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
23 rate and design packages without numerical optimization dependencies.
