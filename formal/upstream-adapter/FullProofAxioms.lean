import FullProof

/-! # Axiom and exact-statement audit of the upstream all-orders theorem -/

#print axioms KrennAllOrders.UpstreamFullProof.no_solution_three
#print axioms KrennAllOrders.UpstreamFullProof.eqSystem_no_solution_ge6_ge3
#print axioms KrennAllOrders.UpstreamFullProof.answer_true_eqSystem_no_solution_ge6_ge3

example : ∀ N D : ℕ, N ≥ 6 → Even N → D ≥ 3 →
    ¬∃ W : MonochromaticQuantumGraph.WeightsN N D ℂ,
      MonochromaticQuantumGraph.EqSystemN N D W :=
  KrennAllOrders.UpstreamFullProof.eqSystem_no_solution_ge6_ge3
