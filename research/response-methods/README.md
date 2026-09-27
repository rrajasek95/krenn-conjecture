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
| Positive site scaling | Preserve the entire output while reducing source strength; reduce both global rate problems to balanced sources. | [Illustrated guide](../../explainers/SITE-BALANCING.md), [proof](../../notes/site-balancing-rate-reduction-2026-09-26.md), [replay](../../computations/site-balancing-2026-09-26/README.md) |
| Four-site response norm identity | A sharp balanced six-site bound, a quantitative measure of imbalance, and an exclusion of complete derivative collapse. | [Proof](../../notes/balanced-four-site-response-bound-2026-09-26.md), [replay](../../computations/site-balancing-2026-09-26/README.md) |
| Polynomial rate certificates and arc tests | Verify an exact algebraic certificate or a proposed violating path; turn a rate claim into a checkable identity. | [Proof](../../notes/integral-rate-certificates-2026-09-26.md), [replay](../../computations/method-utility-2026-09-26/README.md) |
| Paired-hafnian stability estimates | Quantitative control in the paired-hafnian setting under the stated hypotheses. | [Proof](../../notes/paired-hafnian-application-2026-09-26.md), [replay](../../computations/rate-sharpness-followup-2026-09-26/README.md) |
| Full-support higher-order identities | Relate higher GHZ coefficients to lower mixed coefficients; restrict when a leading GHZ output can appear. | [Proof](../../notes/full-support-single-color-jets-2026-09-27.md), [replay](../../computations/full-support-jets-2026-09-27/README.md) |
| Matching-tensor source reconstruction | Recover source information under the stated response and direction hypotheses; distinguish single-copy from multiple-copy information. | [Matching tensors and copies](../../notes/matching-tensor-recovery-and-multiple-copies-2026-09-26.md), [two-direction reconstruction](../../notes/two-direction-source-reconstruction-2026-09-26.md) |

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
18 rate and design packages without numerical optimization dependencies.
