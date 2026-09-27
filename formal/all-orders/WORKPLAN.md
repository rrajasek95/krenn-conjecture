# Full-proof formalization completion record

The mathematical formalization is complete. The local theorem
`KrennAllOrders.KrennConjecture.not_eqSystemN_three` proves ternary
nonexistence from the original complex matching equations. The external
`KrennAllOrders.UpstreamFullProof.eqSystem_no_solution_ge6_ge3` proves the
exact upstream statement for every even `N ≥ 6` and every `D ≥ 3`.

## Parallel responsibilities

| Owner | Delivered work |
|---|---|
| `audit_det_bridge` | Matching model, physical-site quotient, root responses, actual determinant reflection, selected physical coefficient bridges, final local assembly, and exact upstream theorem. |
| `routing_author` | Complete three-matching obstruction, finite and shifted Wick moments, independent replicas, actual response rotations, whole binary-response vanishing, and independent final statement audit. |
| `global_bridge` | Matrix covariance, full invariant-ring theorem, endpoint kernel and differential equations, every original-source endpoint input, actual omission constancy, and independent diagonal-reduction audit. |
| Root | Upstream adapter and reproducible integration, source/cofactor identities, finite response/omission algebra, polarization, actual retained tensor and rotation, diagonalisation, final verification, and publication. |

## Exact target

```lean
∀ N D : ℕ, N ≥ 6 → Even N → D ≥ 3 →
  ¬ ∃ W : MonochromaticQuantumGraph.WeightsN N D ℂ,
    MonochromaticQuantumGraph.EqSystemN N D W
```

The upstream definitions and palette API are pinned at
`e2c4441f9545b85790aebcfaa445e194fcab9d5b`. Their equality with the local
model is proved through the matching recursion. The full proof does not
invoke any upstream conjecture whose proof is a placeholder.

## Verification requirements

- Strict compilation with Lean 4.33.1 and warnings treated as errors.
- Axiom checks of every delivered theorem and proof-bearing definition.
- Only `propext`, `Classical.choice`, and `Quot.sound` in final dependencies.
- No proof holes, custom axioms, or native-evaluation proofs.
- Exact upstream statement, preserving arbitrary complex aggregate weights.
- Binary-only receiving-response scope sufficient for all final applications.
- Polynomial cancellation before evaluation, including zero parameters.

The generated `verification.json` and `axioms.txt` files in each formal
package are the executable verification record. The final external proof
link in the upstream PR must use a fixed commit and point to its exact declaration.
