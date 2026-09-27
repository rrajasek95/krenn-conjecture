# Complete Lean formalization of the Krenn–Gu equation-system conjecture

The full complex nonexistence statement is proved for every even `N ≥ 6`
and every `D ≥ 3`, using the exact upstream weighted matching definitions:

```lean
∀ N D : ℕ, N ≥ 6 → Even N → D ≥ 3 →
  ¬ ∃ W : MonochromaticQuantumGraph.WeightsN N D ℂ,
    MonochromaticQuantumGraph.EqSystemN N D W
```

The final declaration is
[`UpstreamFullProof.eqSystem_no_solution_ge6_ge3`](../upstream-adapter/FullProof.lean).
The same file proves the `True ↔ ...` wrapper corresponding to the upstream
question's affirmative answer. There are no remaining reflection, response,
rotation, diagonalisation, cofactor, or endpoint hypotheses.

The local theorem
[`KrennConjecture.not_eqSystemN_three`](KrennConjecture.lean)
proves the ternary contradiction at every even order at least six. The
[literal adapter](../upstream-adapter/UpstreamAdapter.lean) identifies local
and upstream weights, matching recursion, and equation systems. The proved
upstream palette-restriction API then supplies every `D ≥ 3`.

## Proof chain

| Step | Checked modules |
|---|---|
| Original matching sum equals coefficients of the divided quadratic in the physical-site algebra | [MatchingModel](MatchingModel.lean), [SiteAlgebra](SiteAlgebra.lean), [RootResponse](RootResponse.lean) |
| Actual finite Wick moments, shifted means, and replica covariance | [WickCovariance](WickCovariance.lean), [WickCoefficientBridge](WickCoefficientBridge.lean), [WickRootBridge](WickRootBridge.lean), [WickShiftedBridge](WickShiftedBridge.lean), [WickReplicaBridge](WickReplicaBridge.lean) |
| Physical determinant reflection and receiving-word identities | [ReflectionResponses](ReflectionResponses.lean), [ReflectionTensorBridge](ReflectionTensorBridge.lean), [WickPhysicalBridge](WickPhysicalBridge.lean), [PhysicalReflection](PhysicalReflection.lean) |
| Complete binary higher-response vanishing, including terminal degree | [OddResponseVanishing](OddResponseVanishing.lean), [ResponseFactor](ResponseFactor.lean), [FiniteResponseRigidity](FiniteResponseRigidity.lean), [OddRotation](OddRotation.lean), [WholeBinaryResponse](WholeBinaryResponse.lean) |
| Actual shifted binary pairings and full orthogonal covariance | [BinaryPairing](BinaryPairing.lean), [WickPairing](WickPairing.lean), [WickFinitePairing](WickFinitePairing.lean), [WickFiniteOrthogonal](WickFiniteOrthogonal.lean), [WickEvenResponse](WickEvenResponse.lean) |
| Literal retained tensor and finite omission source equation | [EvenResponse](EvenResponse.lean), [OmittedResponse](OmittedResponse.lean), [PhysicalMeanWick](PhysicalMeanWick.lean), [RetainedMeanWick](RetainedMeanWick.lean), [RetainedBinary](RetainedBinary.lean), [OmissionTensor](OmissionTensor.lean) |
| Pure even-response constancy and original-source diagonalisation | [OmissionRotation](OmissionRotation.lean), [PairingDerivative](PairingDerivative.lean), [OmissionCancellation](OmissionCancellation.lean), [OmissionConstancy](OmissionConstancy.lean), [OmissionDegree](OmissionDegree.lean), [CofactorResponse](CofactorResponse.lean), [CofactorDiagonal](CofactorDiagonal.lean), [DiagonalSource](DiagonalSource.lean) |
| Polynomial invariant ring and endpoint differential equations | [ReplicaCovariance](ReplicaCovariance.lean), [GramInvariants](GramInvariants.lean), [ReplicaKernel](ReplicaKernel.lean), [EndpointPDE](EndpointPDE.lean), [PolynomialODE](PolynomialODE.lean) |
| All endpoint inputs derived from the original source | [PhysicalEndpoint](PhysicalEndpoint.lean), [EndpointSource](EndpointSource.lean), [EndpointCovariance](EndpointCovariance.lean), [BinarySourceInterface](BinarySourceInterface.lean) |
| Unique colour support and the unconditional three-matching obstruction | [EndpointDegree](EndpointDegree.lean), [SupportMatching](SupportMatching.lean), [ForcedMatchingSum](ForcedMatchingSum.lean), [ThreeMatching](ThreeMatching.lean), [CycleCoordinates](CycleCoordinates.lean), [MatchingTransport](MatchingTransport.lean), [ChordObstruction](ChordObstruction.lean), [ThreeMatchingObstruction](ThreeMatchingObstruction.lean) |
| Final contradiction and exact upstream theorem | [PhysicalClosure](PhysicalClosure.lean), [KrennConjecture](KrennConjecture.lean), [FullProof](../upstream-adapter/FullProof.lean) |

The response theorem concerns receiving words using at most two colours;
all departure-row parameters remain arbitrary. That scope suffices for every
omission and endpoint step. Polynomial cancellation takes place before
parameter evaluation, so zero parameter values are included. The proof uses
arbitrary complex aggregate endpoint-colour weights and assumes no positivity,
genericity, or inherited source condition on deleted graphs.

## Verification

The integrated package builds with warnings treated as errors. The
[axiom report](axioms.txt) lists only `propext`, `Classical.choice`, and
`Quot.sound`. No proof hole, custom axiom, or native-evaluation axiom occurs
in the final proof dependencies.

[Verification metadata](verification.json) records the exact toolchain,
source hashes, and every audited declaration. The count includes definitions
with proof fields and is not a count of theorems. The
[upstream verification](../upstream-adapter/verification.json) separately
checks the literal adapter and the exact final declarations.

## Reproduce

Install Lean through `elan`, then run from this directory:

```sh
lake exe cache get
python3 verify.py
```

Use the [upstream verification instructions](../upstream-adapter/README.md)
to check the full `N,D` theorem against the pinned formal-conjectures definitions.

The toolchain is Lean 4.33.1. The manifest pins mathlib revision
`0df444a360eaa60ab8c11dca51a86af692955474` (tag `v4.33.1`).

## Upstream contribution and written proof

[PR #6627](https://github.com/google-deepmind/formal-conjectures/pull/6627)
contains the short palette-restriction API and records the external full proof.
Formal Conjectures is a statement repository; the complete checked proof is
in this external project.

The [cited research PDF](../../proofs/krenn-gu-all-orders-paper.pdf) explains
the mathematical argument. The [formalization workplan](WORKPLAN.md) records
module ownership and the completion requirements.
