# Exact upstream statement and final closure audit

Date: 2026-09-26. Reviewer: `routing_author`.

**PASS.** The final theorem proves the complex equation-system proposition in
`MonochromaticQuantumGraph.eqSystem_no_solution_ge6_ge3` at upstream revision
`e2c4441f9545b85790aebcfaa445e194fcab9d5b`, with no additional source,
diagonality, response, support, or graph hypothesis. This is an independent
statement-fidelity and final-assembly review; it is not presented as an
independent authorship audit of every mathematical module.

The checked declaration is

```lean
KrennAllOrders.UpstreamFullProof.eqSystem_no_solution_ge6_ge3 :
  ∀ N D : ℕ, N ≥ 6 → Even N → D ≥ 3 →
    ¬ ∃ W : MonochromaticQuantumGraph.WeightsN N D ℂ,
      MonochromaticQuantumGraph.EqSystemN N D W
```

`answer_true_eqSystem_no_solution_ge6_ge3` supplies the corresponding `True ↔`
wrapper. The upstream question is at lines 667–674 of the pinned source; the
original question declaration is not used to prove the new theorem.

## Model and dependency checks

1. **Literal weights and matching sum.** `UpstreamAdapter` preserves all four
   edge coordinates and proves equality of the complete head-pair/erase
   recursion for every fuel and vertex list. Consequently its equivalence of
   `EqSystemN` is proved, not assumed. Complex weights remain arbitrary and
   endpoint colours independent; no positivity, reality, symmetry of the two
   colour labels, genericity, or sparsity is imposed. The canonical symmetric
   edge matrix reverses both endpoint coordinates and their colours, preserving
   the upstream ordered-edge convention. Parallel contributions are represented
   by their aggregate complex edge weights.
2. **Normalization.** The target retains exactly amplitude `1` on every constant
   inherited word and `0` on every nonconstant word. `MatchingModel` identifies
   each word coefficient with the recursive matching sum; `SiteAlgebra` proves
   the divided quadratic coefficient bridge. No additional factorial or change
   of normalization enters the wrapper.
3. **Original responses.** `WholeBinaryResponse` is derived from `EqSystemN`
   alone and includes every positive allowed response degree, including the
   terminal degree. Its receiving words use at most two colours on the retained
   sites; this is the precise scope used by `BinarySourceInterface`, omission,
   and the endpoint proof. No three-colour receiving vanishing or inherited
   retained-core source equation is substituted for it. Formal differentiation
   concerns mean parameters, not a presumed family of source solutions.
4. **Discharged intermediate premises.** `DiagonalSource.diagonal_of_eqSystem`
   derives diagonality from the original equation system. The supported
   endpoint identity is then derived from actual covariance and the two
   original binary response families. `pureCofactor` is the actual deleted-pair
   matching sum. Its endpoint identity and row sum force unique supported
   partners. The intermediate assumptions of `PhysicalClosure` are all supplied
   inside `KrennConjecture.not_eqSystemN_three`.
5. **Graph and noncancellation.** `ThreeMatchingObstruction` handles arbitrary
   three labelled perfect matchings on more than four vertices; shared edges
   are not an extra excluded case. `ForcedMatchingSum` proves a realized colour
   word has a unique nonzero matching contribution under the derived support
   condition, so complex cancellation is not silently replaced by positivity.
6. **Order and palette.** Even `N ≥ 6` is converted exactly to `N = 2 * (k + 2)`.
   The proved upstream colour-restriction API extends ternary nonexistence to
   every `D ≥ 3`. It uses an injective palette restriction and preserves both
   constant and nonconstant words.

## Independent replay

At Lean/mathlib 4.33.1, the reviewer independently reran strict compilation of
`KrennConjecture.lean`, `KrennConjectureAxioms.lean`, `FullProof.lean`, and
`FullProofAxioms.lean` with `-DwarningAsError=true`. The latter contains a direct
type-ascription example for the exact upstream proposition. The adapter was
also independently compiled against the pinned checkout, whose source was
checked unchanged against that revision.

All five local assembly declarations and all three final upstream declarations
pass their axiom reports. The final nonexistence and answer declarations depend
only on `propext`, `Classical.choice`, and `Quot.sound`; they do not depend on
`sorryAx`, custom axioms, or native-computation axioms. The upstream module's
other conjecture stubs and computational examples are not proof dependencies.

## Bound source bytes

Paths below are relative to the repository root, except the final upstream row.

| File | SHA-256 |
| --- | --- |
| `formal/all-orders/MatchingModel.lean` | `9819244f8183902620938cc1f75c68e29091d487447640f13e8a5d6f9f11eba3` |
| `formal/all-orders/WholeBinaryResponse.lean` | `1b87d878535d2a8c7faf4bbda40377a72c54c4cfd0ba1dc6015ca0dec4078276` |
| `formal/all-orders/DiagonalSource.lean` | `ded7730cba43f9164013253767e4c28a036088eccc542d9bc34d925944f4dc5e` |
| `formal/all-orders/EndpointCovariance.lean` | `a7d0b4c254ef442831127fce5ef6b6b2c5212bc077ca563f4aa539d121b3f0da` |
| `formal/all-orders/PhysicalClosure.lean` | `baa2ff78f5da0e44afca2f64d56c22abd880249f89c528258a9d7f97f892a636` |
| `formal/all-orders/KrennConjecture.lean` | `4012e48a03ee56a5f06326cf1b285a4a78939763a7466969d75478374e5fd313` |
| `formal/all-orders/KrennConjectureAxioms.lean` | `d89b9be445ba5e13682375a018244fb75d3aabc472071a70a4bf5c9b8ebc07f5` |
| `formal/upstream-adapter/UpstreamAdapter.lean` | `286e0608edff7c100e0758b25b083988e776d9e332164d1ffdddbfe7240c4a14` |
| `formal/upstream-adapter/FullProof.lean` | `c6c538e156ada6e4c859b9676c8973ded8018ac2a408d3361ce4f9e4e82fbd18` |
| `formal/upstream-adapter/FullProofAxioms.lean` | `62976352f36a8bc2261f9d6f03021e852c3c1f1e1c6214fc9b9fd5e8d9f7bbaa` |
| Upstream `FormalConjectures/Paper/MonochromaticQuantumGraph.lean` | `5d9cef7216c064f7de260c83c5662891820c7ef1c249691b5cf7d071f7036cdb` |

The exact formal conclusion is the normalized complex target for even
`N ≥ 6` and `D ≥ 3`. This audit does not claim a separate formal theorem for
`N = 4`, odd orders, or unequal nonzero pure amplitudes, and does not assert
upstream acceptance or publication. No additional restriction remains inside
the stated upstream target.
