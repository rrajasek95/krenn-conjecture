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

- `MatchingModel.lean`: checked matching coefficients and site degrees;
  `audit_det_bridge` is extending this to the physical quotient and divided powers
  in `SiteAlgebra.lean`.
- `ReplicaCovariance.lean`: checked polynomial matrix normal form from explicit
  covariance and divisibility hypotheses; `global_bridge` is proving invariant
  coefficient and Gram-coordinate theorems in `GramInvariants.lean`.
- `ThreeMatching.lean`, `ChordObstruction.lean`, and
  `ThreeMatchingObstruction.lean`: the complete unconditional graph obstruction
  is checked. `routing_author` is now constructing actual finite Wick moments
  and proving their linear covariance in `WickCovariance.lean`.
- Root: checked `CycleCoordinates.lean` and the literal upstream adapter, and
  checked matching transport and finite polynomial response rigidity, and is
  handling reproducible integration and the remaining
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
