# Full-proof formalization assignments

Assigned September 26, 2026. These are implementation tasks, not claims that
the corresponding parts of the conjecture have been formalized.

| Owner | Module | First concrete milestone | Full responsibility |
|---|---|---|---|
| `audit_det_bridge` | `MatchingModel.lean` | Relate a polynomial matching representation to the actual recursive matching sum, with a precise distinction between selector evaluation and coefficients. | Matching model, site variables, and the graph-to-algebra bridge. |
| `global_bridge` | `ReplicaCovariance.lean` | Prove a polynomial 2-by-2 matrix normal form from the relevant divisibility and eigenvector identities. | Two-replica kernel algebra and covariance reduction. |
| `routing_author` | `ThreeMatching.lean` | Formalize matching uniqueness and a valid matching-switch construction using concrete graph definitions. | The final three-matching obstruction and its connection to colour support. |
| Root agent | Package integration and upstream adapter | Identify the local model with the exact upstream definitions and maintain a single reproducible build and axiom report. | Assemble the complete theorem, coordinate remaining reflection/response identities, and prepare the full-proof link. |

Each implementation agent owns its named module and a corresponding axiom
check file. Package manifests, shared documentation, integration files, and
upstream changes are coordinated by the root agent.

## Integrated milestones and current work

- `MatchingModel.lean` and `SiteAlgebra.lean`: checked the complete physical
  quotient/divided-power bridge. `RootResponse.lean` derives the actual root
  response and arbitrary-root cofactor expansion. `audit_det_bridge` is
  working on the whole higher-response tower in `OddResponseVanishing.lean`.
- `ReplicaCovariance.lean` and `GramInvariants.lean`: checked polynomial normal
  form, full invariant-ring representation, and injective axis restriction.
  `EndpointPDE.lean` derives the Gram differential equations from Cartesian
  boundaries and proves the endpoint consequence. `global_bridge` is
  constructing the literal tensor kernel in `ReplicaKernel.lean`.
- `ThreeMatching.lean`, `ChordObstruction.lean`, and
  `ThreeMatchingObstruction.lean`: the complete unconditional graph obstruction
  is checked. `WickCovariance.lean` also constructs and proves covariance for
  actual finite pairing moments. `routing_author` is connecting them to the
  physical quadratic coefficients in `WickCoefficientBridge.lean`.
- Root: checked `CycleCoordinates.lean` and the literal upstream adapter, and
  checked matching transport, finite response rigidity, common response
  factors, cofactor matrix cancellation, binary tensor pairing, omission
  cancellation, and the exact final weighted contradiction. Root is deriving
  actual cofactor sums from retained coefficients in `CofactorResponse.lean`,
  and handling reproducible integration and the remaining
  physical-source chain. New in-progress files are excluded from default
  build targets until they are accepted.

## Exact target

Using the upstream `MonochromaticQuantumGraph` definitions, the required
mathematical conclusion is:

```lean
∀ N D : ℕ, N ≥ 6 → Even N → D ≥ 3 →
  ¬ ∃ W : WeightsN N D ℂ, EqSystemN N D W
```

The existing palette-restriction API reduces this to the case `D = 3`.
The upstream definitions and that API are pinned at
`e2c4441f9545b85790aebcfaa445e194fcab9d5b` in the formal-conjectures fork.
Any mirrored local definitions need a proved adapter; matching names or
informal equivalence alone are not sufficient.

## Acceptance of each milestone

- Compile with Lean 4.33.1 and warnings treated as errors.
- Inspect `#print axioms` for every delivered theorem.
- Use no `sorry`, custom axioms, placeholder definitions, or native-evaluation
  proofs.
- State hypotheses explicitly and record which have actually been derived
  from the graph equation system.
- Preserve the distinction between aggregate weights and individual parallel
  edges, and between a general matrix lemma and its physical-source instance.

The full result is complete only after the exact target follows with no
unproved bridge assumptions. Its PR link must point to that declaration at a
fixed commit. The [remaining-work ledger](README.md#remaining-formalization)
continues to describe outstanding obligations until checked implementations
are integrated.
