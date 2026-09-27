/-
Copyright (c) 2026 Rishi. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/

import ChordObstruction
import CycleCoordinates
import MatchingTransport

/-!
# The three-perfect-matching obstruction

On more than four vertices, any family containing three labelled perfect
matchings admits a perfect matching with a nonconstant receiving colour word.
Shared physical edges are allowed: the no-mixed-matching assumption first
excludes them, and then the alternating-cycle and chord constructions apply.
-/

namespace KrennAllOrders.ThreeMatching

variable {V C : Type*} [Fintype V]

/-- Three distinct colour labels always admit a mixed perfect matching once the
vertex set has more than four vertices. Evenness follows from any one matching. -/
theorem hasMixedMatching_of_three_colours (colours : C → Matching V)
    (hcard : 4 < Fintype.card V) {a b c : C}
    (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c) :
    HasMixedMatching colours := by
  classical
  by_contra hno
  have htwo : 2 < Fintype.card V := by omega
  have hdisjoint := colour_partner_injective_of_no_mixed colours htwo hno
  obtain ⟨p⟩ := Fintype.card_pos_iff.mp (show 0 < Fintype.card V by omega)
  obtain ⟨n, hsize⟩ : ∃ n : ℕ, Fintype.card V = n + 2 :=
    ⟨Fintype.card V - 2, by omega⟩
  have heven : (n + 2) % 2 = 0 := by
    simpa only [hsize, Nat.even_iff] using (colours a).even_card
  have hbig : 4 < n + 2 := by omega
  obtain ⟨e, he⟩ : ∃ e : Fin (n + 2) ≃ V, ∀ i j,
      (SimpleGraph.cycleGraph (n + 2)).Adj i j →
        (pairGraph colours a b).Adj (e i) (e j) := by
    have hequiv := exists_cycle_equiv_of_no_mixed colours htwo hno hab p
    rw [hsize] at hequiv
    exact hequiv
  let H := (colours c).map e.symm
  obtain ⟨M, hcover, ⟨u, hu⟩, ⟨v, hv⟩⟩ :=
    Chord.exists_hybrid_matching H heven hbig
  let N := M.map e
  have hH (i : Fin (n + 2)) : e (H.partner i) = (colours c).partner (e i) := by
    simp only [H, Matching.map, Equiv.symm_symm, Equiv.apply_symm_apply]
  have hcoverN : ∀ w, ∃ k, N.partner w = (colours k).partner w := by
    intro w
    obtain ⟨i, rfl⟩ := e.surjective w
    change (∃ k, (M.map e).partner (e i) = (colours k).partner (e i))
    rw [Matching.map_partner]
    rcases hcover i with hi | hi
    · exact ⟨c, (congrArg e hi).trans (hH i)⟩
    · have hedge := he i (M.partner i) hi
      change (colours a).partner (e i) = e (M.partner i) ∨
        (colours b).partner (e i) = e (M.partner i) at hedge
      rcases hedge with ha | hb
      · exact ⟨a, ha.symm⟩
      · exact ⟨b, hb.symm⟩
  have hc : N.partner (e u) = (colours c).partner (e u) := by
    change (M.map e).partner (e u) = _
    rw [Matching.map_partner, hu, hH]
  have hedge := he v (M.partner v) hv
  change (colours a).partner (e v) = e (M.partner v) ∨
    (colours b).partner (e v) = e (M.partner v) at hedge
  rcases hedge with ha | hb
  · have hNa : N.partner (e v) = (colours a).partner (e v) := by
      exact (Matching.map_partner M e v).trans ha.symm
    exact hno (hasMixedMatching_of_partner_cover colours N hdisjoint hcoverN hac.symm hc hNa)
  · have hNb : N.partner (e v) = (colours b).partner (e v) := by
      exact (Matching.map_partner M e v).trans hb.symm
    exact hno (hasMixedMatching_of_partner_cover colours N hdisjoint hcoverN hbc.symm hc hNb)

/-- The usual three-colour form of the obstruction. -/
theorem hasMixedMatching_three (colours : Fin 3 → Matching V)
    (hcard : 4 < Fintype.card V) : HasMixedMatching colours :=
  hasMixedMatching_of_three_colours colours hcard
    (a := 0) (b := 1) (c := 2) (by decide) (by decide) (by decide)

/-- A family with no mixed perfect matching on more than four vertices has at most
two colour labels. The statement needs no finite enumeration of the colour type. -/
theorem colour_eq_of_no_mixed (colours : C → Matching V)
    (hcard : 4 < Fintype.card V) (hno : ¬HasMixedMatching colours)
    {a b : C} (hab : a ≠ b) (c : C) : c = a ∨ c = b := by
  by_contra h
  have hca : c ≠ a := fun hca => h (Or.inl hca)
  have hcb : c ≠ b := fun hcb => h (Or.inr hcb)
  exact hno (hasMixedMatching_of_three_colours colours hcard hab hca.symm hcb.symm)

end KrennAllOrders.ThreeMatching
