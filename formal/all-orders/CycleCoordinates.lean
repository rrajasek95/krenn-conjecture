/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import ThreeMatching
import Mathlib.Combinatorics.SimpleGraph.CycleGraph
import Mathlib.Combinatorics.SimpleGraph.Hamiltonian

/-! # Cyclic coordinates for the final matching obstruction -/

namespace KrennAllOrders.ThreeMatching

variable {V C : Type*} [Fintype V]

/-- A spanning cycle gives bijective cyclic coordinates, preserving each cycle edge. -/
theorem exists_cycle_equiv_of_spanning {G : SimpleGraph V}
    (hcard : 2 < Fintype.card V) {p : V} (walk : G.Walk p p)
    (hcycle : walk.IsCycle) (hspan : ∀ v, v ∈ walk.support) :
    ∃ e : Fin (Fintype.card V) ≃ V, ∀ i j,
      (SimpleGraph.cycleGraph (Fintype.card V)).Adj i j → G.Adj (e i) (e j) := by
  classical
  have htail : walk.tail.IsHamiltonian := by
    apply hcycle.isPath_tail.isHamiltonian_of_mem
    intro v
    by_cases hv : v = p
    · subst v
      exact walk.tail.end_mem_support
    · have hmem := hspan v
      rw [← SimpleGraph.Walk.cons_support_tail hcycle.not_nil] at hmem
      exact (List.mem_cons.mp hmem).resolve_left hv
  have hh : walk.IsHamiltonianCycle := ⟨hcycle, htail⟩
  obtain ⟨copy⟩ := (SimpleGraph.cycleGraph_isContained_iff hcard).mpr
    ⟨p, walk, hcycle, hh.length_eq⟩
  have hbij : Function.Bijective copy := by
    exact ⟨copy.injective, copy.injective.surjective_of_finite
      (Fintype.equivFin V).symm⟩
  exact ⟨Equiv.ofBijective copy hbij, fun _ _ h => copy.toHom.map_rel h⟩

/-- The no-mixed-matching assumption provides the cyclic coordinates used in the chord proof. -/
theorem exists_cycle_equiv_of_no_mixed (colours : C → Matching V)
    (hcard : 2 < Fintype.card V) (hno : ¬ HasMixedMatching colours)
    {a b : C} (hab : a ≠ b) (p : V) :
    ∃ e : Fin (Fintype.card V) ≃ V, ∀ i j,
      (SimpleGraph.cycleGraph (Fintype.card V)).Adj i j →
        (pairGraph colours a b).Adj (e i) (e j) := by
  obtain ⟨walk, hcycle, hspan⟩ := exists_spanning_cycle_of_no_mixed colours hcard hno hab p
  exact exists_cycle_equiv_of_spanning hcard walk hcycle hspan

end KrennAllOrders.ThreeMatching
