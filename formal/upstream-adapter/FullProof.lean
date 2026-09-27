/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import UpstreamAdapter
import KrennConjecture

/-!
# The all-orders theorem for the exact upstream equation system

The matching recursion and weights are identified by `UpstreamAdapter`.
Palette restriction is the upstream API at revision
`e2c4441f9545b85790aebcfaa445e194fcab9d5b`.
-/

namespace KrennAllOrders.UpstreamFullProof

/-- The proved ternary contradiction uses the exact upstream weights and
equation system, with arbitrary complex endpoint-colour weights. -/
theorem no_solution_three {N : ℕ} (hN : 6 ≤ N) (heven : Even N) :
    ¬∃ W : MonochromaticQuantumGraph.WeightsN N 3 ℂ,
      MonochromaticQuantumGraph.EqSystemN N 3 W := by
  rintro ⟨W, hW⟩
  exact KrennConjecture.not_eqSystemN_three hN heven (UpstreamAdapter.toLocalWeights W)
    ((UpstreamAdapter.eqSystemN_iff W).mpr hW)

/-- Exact all-orders Krenn–Gu nonexistence statement over the complex field. -/
theorem eqSystem_no_solution_ge6_ge3 :
    ∀ N D : ℕ, N ≥ 6 → Even N → D ≥ 3 →
      ¬∃ W : MonochromaticQuantumGraph.WeightsN N D ℂ,
        MonochromaticQuantumGraph.EqSystemN N D W :=
  MonochromaticQuantumGraph.no_solution_ge3_of_no_solution_d3
    (fun _ hN heven => no_solution_three hN heven)

/-- Setting the upstream question's answer to `True` gives its exact
propositional wrapper around the proved universal statement. -/
theorem answer_true_eqSystem_no_solution_ge6_ge3 :
    True ↔ ∀ N D : ℕ, N ≥ 6 → Even N → D ≥ 3 →
      ¬∃ W : MonochromaticQuantumGraph.WeightsN N D ℂ,
        MonochromaticQuantumGraph.EqSystemN N D W :=
  ⟨fun _ => eqSystem_no_solution_ge6_ge3, fun _ => trivial⟩

end KrennAllOrders.UpstreamFullProof
