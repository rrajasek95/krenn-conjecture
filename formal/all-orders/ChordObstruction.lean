/-
Copyright (c) 2026 Rishi. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/

import ThreeMatching
import Mathlib.Combinatorics.SimpleGraph.CycleGraph

/-!
# Filling the intervals between matching chords

These constructions use the cyclic order on `Fin (n + 2)`. They build actual
partner involutions using prescribed chords at selected vertices and cycle
edges elsewhere.
-/

set_option autoImplicit false

namespace KrennAllOrders.ThreeMatching

open scoped Classical

namespace Chord

variable {n : ℕ}

theorem next_val (i : Fin (n + 2)) :
    (i + 1).val = if i.val + 1 < n + 2 then i.val + 1 else 0 := by
  rw [Fin.val_add_one]
  split_ifs with h h' h'
  · have hi := congrArg Fin.val h
    simp only [Fin.val_last] at hi
    omega
  · rfl
  · rfl
  · have hi : i = Fin.last (n + 1) := by
      apply Fin.ext
      simp only [Fin.val_last]
      omega
    exact False.elim (h hi)

theorem prev_val (i : Fin (n + 2)) :
    (i - 1).val = if i.val = 0 then n + 1 else i.val - 1 := by
  by_cases hi : i = 0
  · subst i
    simp
  · rw [Fin.val_sub_one_of_ne_zero hi, if_neg]
    exact fun h => hi (Fin.ext h)

theorem next_adj (i : Fin (n + 2)) :
    (SimpleGraph.cycleGraph (n + 2)).Adj i (i + 1) := by
  rw [← SimpleGraph.mem_neighborSet, SimpleGraph.cycleGraph_neighborSet]
  exact Set.mem_insert_of_mem _ (Set.mem_singleton _)

theorem prev_adj (i : Fin (n + 2)) :
    (SimpleGraph.cycleGraph (n + 2)).Adj i (i - 1) := by
  rw [← SimpleGraph.mem_neighborSet, SimpleGraph.cycleGraph_neighborSet]
  exact Set.mem_insert _ _

/-- Fill non-chord vertices by a coherent choice of cyclic successor or predecessor. -/
noncomputable def fill (H : Matching (Fin (n + 2))) (hole forward : Fin (n + 2) → Prop)
    (hclosed : ∀ i, hole i → hole (H.partner i))
    (hnext : ∀ i, ¬hole i → forward i → ¬hole (i + 1) ∧ ¬forward (i + 1))
    (hprev : ∀ i, ¬hole i → ¬forward i → ¬hole (i - 1) ∧ forward (i - 1)) :
    Matching (Fin (n + 2)) where
  partner i := if hole i then H.partner i else if forward i then i + 1 else i - 1
  partner_partner i := by
    by_cases hi : hole i
    · simp only [if_pos hi, if_pos (hclosed i hi), H.partner_partner]
    · by_cases hf : forward i
      · obtain ⟨hn, hnf⟩ := hnext i hi hf
        simp only [if_neg hi, if_pos hf, if_neg hn, if_neg hnf, add_sub_cancel_right]
      · obtain ⟨hp, hpf⟩ := hprev i hi hf
        simp only [if_neg hi, if_neg hf, if_neg hp, if_pos hpf, sub_add_cancel]
  partner_ne_self i := by
    by_cases hi : hole i
    · simpa only [if_pos hi] using H.partner_ne_self i
    · by_cases hf : forward i
      · simp only [if_neg hi, if_pos hf]
        intro h
        have ha := next_adj i
        rw [h] at ha
        exact (SimpleGraph.cycleGraph (n + 2)).irrefl ha
      · simp only [if_neg hi, if_neg hf]
        intro h
        have ha := prev_adj i
        rw [h] at ha
        exact (SimpleGraph.cycleGraph (n + 2)).irrefl ha

theorem fill_at_hole (H : Matching (Fin (n + 2))) (hole forward : Fin (n + 2) → Prop)
    (hclosed hnext hprev) {i : Fin (n + 2)} (hi : hole i) :
    (fill H hole forward hclosed hnext hprev).partner i = H.partner i := by
  simp only [fill, if_pos hi]

theorem fill_off_hole (H : Matching (Fin (n + 2))) (hole forward : Fin (n + 2) → Prop)
    (hclosed hnext hprev) {i : Fin (n + 2)} (hi : ¬hole i) :
    (SimpleGraph.cycleGraph (n + 2)).Adj i
      ((fill H hole forward hclosed hnext hprev).partner i) := by
  simp only [fill, if_neg hi]
  split_ifs
  · exact next_adj i
  · exact prev_adj i

/-- The two endpoints reserved for a single chord. -/
def twoHoles (a b i : Fin (n + 2)) : Prop := i = a ∨ i = b

/-- Alternating adjacent-pair directions on the two arcs between opposite-parity holes. -/
def twoForward (a b i : Fin (n + 2)) : Prop :=
  (i.val % 2 = a.val % 2) ↔ (i.val < a.val ∨ b.val < i.val)

theorem two_next {a b : Fin (n + 2)} (hab : a.val < b.val)
    (hparity : a.val % 2 ≠ b.val % 2) (heven : (n + 2) % 2 = 0)
    (i : Fin (n + 2)) (hi : ¬twoHoles a b i) (hf : twoForward a b i) :
    ¬twoHoles a b (i + 1) ∧ ¬twoForward a b (i + 1) := by
  simp only [twoHoles, twoForward, Fin.ext_iff] at hi hf ⊢
  rw [next_val]
  split_ifs <;> omega

theorem two_prev {a b : Fin (n + 2)} (hab : a.val < b.val)
    (hparity : a.val % 2 ≠ b.val % 2) (heven : (n + 2) % 2 = 0)
    (i : Fin (n + 2)) (hi : ¬twoHoles a b i) (hf : ¬twoForward a b i) :
    ¬twoHoles a b (i - 1) ∧ twoForward a b (i - 1) := by
  simp only [twoHoles, twoForward, Fin.ext_iff] at hi hf ⊢
  rw [prev_val]
  split_ifs <;> omega

theorem two_closed (H : Matching (Fin (n + 2))) {a b : Fin (n + 2)}
    (hab : H.partner a = b) (i : Fin (n + 2)) (hi : twoHoles a b i) :
    twoHoles a b (H.partner i) := by
  rcases hi with rfl | rfl
  · exact Or.inr hab
  · exact Or.inl (by rw [← hab, H.partner_partner])

/-- Reserve one opposite-parity chord and pair all remaining vertices along the cycle. -/
noncomputable def fillTwo (H : Matching (Fin (n + 2))) {a b : Fin (n + 2)}
    (hab : a.val < b.val) (hH : H.partner a = b)
    (hparity : a.val % 2 ≠ b.val % 2) (heven : (n + 2) % 2 = 0) :
    Matching (Fin (n + 2)) :=
  fill H (twoHoles a b) (twoForward a b) (two_closed H hH)
    (two_next hab hparity heven) (two_prev hab hparity heven)

/-- The endpoints reserved for two interlacing chords. -/
def fourHoles (a b c d i : Fin (n + 2)) : Prop := i = a ∨ i = b ∨ i = c ∨ i = d

/-- Alternating pair directions on the four arcs between cyclically alternating holes. -/
def fourForward (a b c d i : Fin (n + 2)) : Prop :=
  (i.val % 2 = a.val % 2) ↔
    (i.val < a.val ∨ (b.val < i.val ∧ i.val < c.val) ∨ d.val < i.val)

theorem four_next {a b c d : Fin (n + 2)}
    (hab : a.val < b.val) (hbc : b.val < c.val) (hcd : c.val < d.val)
    (hac : a.val % 2 = c.val % 2) (hbd : b.val % 2 = d.val % 2)
    (hparity : a.val % 2 ≠ b.val % 2) (heven : (n + 2) % 2 = 0)
    (i : Fin (n + 2)) (hi : ¬fourHoles a b c d i) (hf : fourForward a b c d i) :
    ¬fourHoles a b c d (i + 1) ∧ ¬fourForward a b c d (i + 1) := by
  simp only [fourHoles, fourForward, Fin.ext_iff] at hi hf ⊢
  rw [next_val]
  split_ifs <;> omega

theorem four_prev {a b c d : Fin (n + 2)}
    (hab : a.val < b.val) (hbc : b.val < c.val) (hcd : c.val < d.val)
    (hac : a.val % 2 = c.val % 2) (hbd : b.val % 2 = d.val % 2)
    (hparity : a.val % 2 ≠ b.val % 2) (heven : (n + 2) % 2 = 0)
    (i : Fin (n + 2)) (hi : ¬fourHoles a b c d i) (hf : ¬fourForward a b c d i) :
    ¬fourHoles a b c d (i - 1) ∧ fourForward a b c d (i - 1) := by
  simp only [fourHoles, fourForward, Fin.ext_iff] at hi hf ⊢
  rw [prev_val]
  split_ifs <;> omega

theorem four_closed (H : Matching (Fin (n + 2))) {a b c d : Fin (n + 2)}
    (hac : H.partner a = c) (hbd : H.partner b = d)
    (i : Fin (n + 2)) (hi : fourHoles a b c d i) :
    fourHoles a b c d (H.partner i) := by
  rcases hi with rfl | rfl | rfl | rfl
  · exact Or.inr (Or.inr (Or.inl hac))
  · exact Or.inr (Or.inr (Or.inr hbd))
  · exact Or.inl (by rw [← hac, H.partner_partner])
  · exact Or.inr (Or.inl (by rw [← hbd, H.partner_partner]))

/-- Reserve two interlacing chords and pair the four remaining arcs along the cycle. -/
noncomputable def fillFour (H : Matching (Fin (n + 2))) {a b c d : Fin (n + 2)}
    (hab : a.val < b.val) (hbc : b.val < c.val) (hcd : c.val < d.val)
    (hHac : H.partner a = c) (hHbd : H.partner b = d)
    (hac : a.val % 2 = c.val % 2) (hbd : b.val % 2 = d.val % 2)
    (hparity : a.val % 2 ≠ b.val % 2) (heven : (n + 2) % 2 = 0) :
    Matching (Fin (n + 2)) :=
  fill H (fourHoles a b c d) (fourForward a b c d) (four_closed H hHac hHbd)
    (four_next hab hbc hcd hac hbd hparity heven)
    (four_prev hab hbc hcd hac hbd hparity heven)

/-- A parity-preserving matching has two interlacing chords of opposite endpoint parities.

Choose a chord of minimum positive linear span. The partner of the next vertex
cannot lie strictly inside that span, so it gives the interlacing chord. -/
theorem exists_interlacing_of_parity_preserving (H : Matching (Fin (n + 2)))
    (hparity : ∀ i, (H.partner i).val % 2 = i.val % 2) :
    ∃ a b c d : Fin (n + 2),
      a.val < b.val ∧ b.val < c.val ∧ c.val < d.val ∧
      H.partner a = c ∧ H.partner b = d ∧
      a.val % 2 = c.val % 2 ∧ b.val % 2 = d.val % 2 ∧ a.val % 2 ≠ b.val % 2 := by
  have hzero : 0 < (H.partner 0).val := by
    have hne := H.partner_ne_self 0
    have hv : (H.partner 0).val ≠ 0 := fun h => hne (Fin.ext h)
    omega
  have hex : ∃ k : ℕ, ∃ a b : Fin (n + 2),
      H.partner a = b ∧ a.val < b.val ∧ b.val - a.val = k :=
    ⟨(H.partner 0).val, 0, H.partner 0, rfl, hzero, Nat.sub_zero _⟩
  obtain ⟨a, b, hHab, hab, hgap⟩ := Nat.find_spec hex
  have hmin : ∀ i j : Fin (n + 2), H.partner i = j → i.val < j.val →
      Nat.find hex ≤ j.val - i.val := by
    intro i j hij hlt
    exact Nat.find_min' hex ⟨i, j, hij, hlt, rfl⟩
  have hbp : b.val % 2 = a.val % 2 := by simpa only [hHab] using hparity a
  let c : Fin (n + 2) := ⟨a.val + 1, by omega⟩
  let d := H.partner c
  have hcv : c.val = a.val + 1 := rfl
  have hac : a.val < c.val := by omega
  have hcb : c.val < b.val := by omega
  have hdp : d.val % 2 = c.val % 2 := hparity c
  have hHdc : H.partner d = c := H.partner_partner c
  have hdc : d ≠ c := H.partner_ne_self c
  have hout : d.val < a.val ∨ b.val < d.val := by
    by_contra hout
    have hinside : a.val < d.val ∧ d.val < b.val := by omega
    by_cases hcd : c.val < d.val
    · have hm := hmin c d rfl hcd
      omega
    · have hdc' : d.val < c.val := by
        have hneq : d.val ≠ c.val := fun h => hdc (Fin.ext h)
        omega
      have hm := hmin d c hHdc hdc'
      omega
  rcases hout with hda | hbd
  · refine ⟨d, a, c, b, hda, hac, hcb, hHdc, hHab, hdp, hbp.symm, ?_⟩
    omega
  · refine ⟨a, c, b, d, hac, hcb, hbd, hHab, rfl, hbp.symm, hdp.symm, ?_⟩
    omega

/-- More than four vertices leave a vertex outside any four reserved endpoints. -/
theorem exists_outside_four (hbig : 4 < n + 2) (a b c d : Fin (n + 2)) :
    ∃ i, ¬fourHoles a b c d i := by
  have hcard : ({a, b, c, d} : Finset (Fin (n + 2))).card <
      (Finset.univ : Finset (Fin (n + 2))).card := by
    have hle := (Finset.card_le_four : ({a, b, c, d} : Finset (Fin (n + 2))).card ≤ 4)
    simpa only [Finset.card_univ, Fintype.card_fin] using lt_of_le_of_lt hle hbig
  obtain ⟨i, _, hi⟩ := Finset.exists_mem_notMem_of_card_lt_card hcard
  exact ⟨i, by simpa only [fourHoles, Finset.mem_insert, Finset.mem_singleton] using hi⟩

/-- A one-chord completion has an original-matching edge and an unreserved cycle edge. -/
theorem exists_hybrid_of_opposite_parity (H : Matching (Fin (n + 2)))
    (heven : (n + 2) % 2 = 0) (hbig : 4 < n + 2) {a b : Fin (n + 2)}
    (hab : a.val < b.val) (hH : H.partner a = b)
    (hparity : a.val % 2 ≠ b.val % 2) :
    ∃ M : Matching (Fin (n + 2)),
      (∀ i, M.partner i = H.partner i ∨
        (SimpleGraph.cycleGraph (n + 2)).Adj i (M.partner i)) ∧
      (∃ i, M.partner i = H.partner i) ∧
      (∃ i, (SimpleGraph.cycleGraph (n + 2)).Adj i (M.partner i)) := by
  let M := fillTwo H hab hH hparity heven
  have hhole (i) (hi : twoHoles a b i) : M.partner i = H.partner i :=
    fill_at_hole H _ _ _ _ _ hi
  have hout (i) (hi : ¬twoHoles a b i) :
      (SimpleGraph.cycleGraph (n + 2)).Adj i (M.partner i) :=
    fill_off_hole H _ _ _ _ _ hi
  refine ⟨M, ?_, ⟨a, hhole a (Or.inl rfl)⟩, ?_⟩
  · intro i
    by_cases hi : twoHoles a b i
    · exact Or.inl (hhole i hi)
    · exact Or.inr (hout i hi)
  · obtain ⟨i, hi⟩ := exists_outside_four hbig a b a b
    exact ⟨i, hout i (fun h => hi (h.elim Or.inl (fun hb => Or.inr (Or.inl hb))))⟩

/-- A two-chord completion has an original-matching edge and an unreserved cycle edge. -/
theorem exists_hybrid_of_interlacing (H : Matching (Fin (n + 2)))
    (heven : (n + 2) % 2 = 0) (hbig : 4 < n + 2) {a b c d : Fin (n + 2)}
    (hab : a.val < b.val) (hbc : b.val < c.val) (hcd : c.val < d.val)
    (hHac : H.partner a = c) (hHbd : H.partner b = d)
    (hac : a.val % 2 = c.val % 2) (hbd : b.val % 2 = d.val % 2)
    (hparity : a.val % 2 ≠ b.val % 2) :
    ∃ M : Matching (Fin (n + 2)),
      (∀ i, M.partner i = H.partner i ∨
        (SimpleGraph.cycleGraph (n + 2)).Adj i (M.partner i)) ∧
      (∃ i, M.partner i = H.partner i) ∧
      (∃ i, (SimpleGraph.cycleGraph (n + 2)).Adj i (M.partner i)) := by
  let M := fillFour H hab hbc hcd hHac hHbd hac hbd hparity heven
  have hhole (i) (hi : fourHoles a b c d i) : M.partner i = H.partner i :=
    fill_at_hole H _ _ _ _ _ hi
  have hout (i) (hi : ¬fourHoles a b c d i) :
      (SimpleGraph.cycleGraph (n + 2)).Adj i (M.partner i) :=
    fill_off_hole H _ _ _ _ _ hi
  refine ⟨M, ?_, ⟨a, hhole a (Or.inl rfl)⟩, ?_⟩
  · intro i
    by_cases hi : fourHoles a b c d i
    · exact Or.inl (hhole i hi)
    · exact Or.inr (hout i hi)
  · obtain ⟨i, hi⟩ := exists_outside_four hbig a b c d
    exact ⟨i, hout i hi⟩

/-- On an even cycle with more than four vertices, any perfect matching can be
partly retained and completed by cycle edges. The two witness clauses reserve at
least one original edge and at least one cycle edge. -/
theorem exists_hybrid_matching (H : Matching (Fin (n + 2)))
    (heven : (n + 2) % 2 = 0) (hbig : 4 < n + 2) :
    ∃ M : Matching (Fin (n + 2)),
      (∀ i, M.partner i = H.partner i ∨
        (SimpleGraph.cycleGraph (n + 2)).Adj i (M.partner i)) ∧
      (∃ i, M.partner i = H.partner i) ∧
      (∃ i, (SimpleGraph.cycleGraph (n + 2)).Adj i (M.partner i)) := by
  by_cases hp : ∀ i, (H.partner i).val % 2 = i.val % 2
  · obtain ⟨a, b, c, d, hab, hbc, hcd, hHac, hHbd, hac, hbd, hparity⟩ :=
      exists_interlacing_of_parity_preserving H hp
    exact exists_hybrid_of_interlacing H heven hbig hab hbc hcd hHac hHbd hac hbd hparity
  · push Not at hp
    obtain ⟨a, hparity⟩ := hp
    let b := H.partner a
    have hne : a.val ≠ b.val := fun h => (H.partner_ne_self a) (Fin.ext h.symm)
    by_cases hab : a.val < b.val
    · exact exists_hybrid_of_opposite_parity H heven hbig hab rfl (Ne.symm hparity)
    · have hba : b.val < a.val := by omega
      exact exists_hybrid_of_opposite_parity H heven hbig hba
        (H.partner_partner a) hparity

end Chord

end KrennAllOrders.ThreeMatching
