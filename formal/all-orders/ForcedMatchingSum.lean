/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import MatchingModel
import ThreeMatchingObstruction
import Mathlib.Data.List.Chain

/-!
# The weighted contradiction once each colour has a unique partner

This file applies the actual recursive matching sum to a forced partner
matching. Each recursion has precisely one nonzero term; its weight cannot
cancel. The support hypotheses are explicit until supplied by the physical
diagonal and endpoint identities.
-/

namespace KrennAllOrders.ForcedMatchingSum

open MatchingModel ThreeMatching

variable {K : Type*} [CommRing K] [IsDomain K] {N D : ℕ}

private theorem closed_after_pair (M : Matching (Fin N)) (v : Fin N)
    (L : List (Fin N)) (hv : v ∉ L) (hn : L.Nodup)
    (hclosed : ∀ x ∈ v :: L, M.partner x ∈ v :: L) :
    ∀ x ∈ L.erase (M.partner v), M.partner x ∈ L.erase (M.partner v) := by
  intro x hx
  have hmem : x ∈ L ∧ x ≠ M.partner v := by
    simpa [hn.erase_eq_filter] using hx
  have hxv : x ≠ v := by intro h; exact hv (h ▸ hmem.1)
  have hpxv : M.partner x ≠ v := by
    intro h
    exact hmem.2 (M.partner_injective (h.trans (M.partner_partner v).symm))
  have hpxp : M.partner x ≠ M.partner v := fun h => hxv (M.partner_injective h)
  have hpL : M.partner x ∈ L :=
    (List.mem_cons.mp (hclosed x (List.mem_cons.mpr (Or.inr hmem.1)))).resolve_left hpxv
  simpa [hn.erase_eq_filter] using And.intro hpL hpxp

/-- An ordered, partner-closed list has a nonzero matching sum when its only
supported edges are those of the given partner involution. -/
theorem pmSumListAux_ne_zero_of_forced (W : WeightsN N D K) (word : Fin N → Fin D)
    (M : Matching (Fin N))
    (hweight : ∀ v u, v < u →
      (W (mkEdge v u (word v) (word u)) ≠ 0 ↔ M.partner v = u)) :
    ∀ (n : ℕ) (L : List (Fin N)), L.length = n → L.Nodup →
      L.Pairwise (· < ·) → (∀ x ∈ L, M.partner x ∈ L) →
      pmSumListAux W word n L ≠ 0
  | 0, [], _, _, _, _ => by simp [pmSumListAux]
  | 0, _ :: _, hlen, _, _, _ => by simp at hlen
  | 1, [], hlen, _, _, _ => by simp at hlen
  | 1, [v], _, _, _, hclosed => by
    have h := hclosed v (by simp)
    simp only [List.mem_singleton] at h
    exact False.elim (M.partner_ne_self v h)
  | 1, _ :: _ :: _, hlen, _, _, _ => by simp at hlen
  | n + 2, [], hlen, _, _, _ => by simp at hlen
  | n + 2, [v], hlen, _, _, _ => by simp at hlen
  | n + 2, v :: u :: L, hlen, hnodup, hsorted, hclosed => by
    classical
    let tail := u :: L
    have ht : tail.Nodup := (List.nodup_cons.mp hnodup).2
    have hv : v ∉ tail := (List.nodup_cons.mp hnodup).1
    have horder : ∀ x ∈ tail, v < x := (List.pairwise_cons.mp hsorted).1
    have htorder : tail.Pairwise (· < ·) := (List.pairwise_cons.mp hsorted).2
    have hp : M.partner v ∈ tail :=
      (List.mem_cons.mp (hclosed v (by simp))).resolve_left (M.partner_ne_self v)
    have hlen' : (tail.erase (M.partner v)).length = n := by
      rw [List.length_erase_of_mem hp]
      change (u :: L).length - 1 = n
      simp only [List.length_cons] at hlen ⊢
      omega
    have hrec := pmSumListAux_ne_zero_of_forced W word M hweight n
      (tail.erase (M.partner v)) hlen' (ht.erase _) (htorder.erase _)
      (closed_after_pair M v tail hv ht hclosed)
    have hsum :
        (tail.map fun x => W (mkEdge v x (word v) (word x)) *
          pmSumListAux W word n (tail.erase x)).sum =
        W (mkEdge v (M.partner v) (word v) (word (M.partner v))) *
          pmSumListAux W word n (tail.erase (M.partner v)) := by
      rw [← List.sum_toFinset _ ht]
      apply Finset.sum_eq_single (M.partner v)
      · intro x hx hne
        have hxL : x ∈ tail := List.mem_toFinset.mp hx
        have hw : W (mkEdge v x (word v) (word x)) = 0 := by
          by_contra h
          exact hne ((hweight v x (horder x hxL)).mp h).symm
        rw [hw, zero_mul]
      · intro h
        exact False.elim (h (List.mem_toFinset.mpr hp))
    change (tail.map fun x => W (mkEdge v x (word v) (word x)) *
      pmSumListAux W word n (tail.erase x)).sum ≠ 0
    rw [hsum]
    exact mul_ne_zero ((hweight v (M.partner v) (horder _ hp)).mpr rfl) hrec

theorem pmSumN_ne_zero_of_forced (W : WeightsN N D K) (word : Fin N → Fin D)
    (M : Matching (Fin N))
    (hweight : ∀ v u, v < u →
      (W (mkEdge v u (word v) (word u)) ≠ 0 ↔ M.partner v = u)) :
    pmSumN N D W word ≠ 0 := by
  apply pmSumListAux_ne_zero_of_forced W word M hweight
    (vertices N).length (vertices N) rfl (vertices_nodup N) (vertices_pairwise_lt N)
  intro x _
  exact mem_vertices (M.partner x)

/-- The upstream-style chain predicate really forces any two listed colours to agree. -/
theorem allEqualList_eq (word : Fin N → Fin D) (L : List (Fin N))
    (h : allEqualList word L) {v w : Fin N} (hv : v ∈ L) (hw : w ∈ L) :
    word v = word w := by
  let : Trans (fun x y : Fin N => word x = word y)
      (fun x y : Fin N => word x = word y) (fun x y : Fin N => word x = word y) :=
    ⟨fun h₁ h₂ => h₁.trans h₂⟩
  cases L with
  | nil => simp at hv
  | cons a L =>
    have hchain : (a :: L).IsChain (fun x y => word x = word y) := h
    have ha : ∀ x ∈ a :: L, word a = word x := by
      intro x hx
      rcases List.mem_cons.mp hx with rfl | hx
      · rfl
      · exact hchain.rel_cons hx
    exact (ha v hv).symm.trans (ha w hw)

theorem not_allEqual_of_distinct (word : Fin N → Fin D) {v w : Fin N}
    (hne : word v ≠ word w) : ¬ allEqual word := by
  intro h
  exact hne (allEqualList_eq word (vertices N) h (mem_vertices v) (mem_vertices w))

/-- The physical support pattern obtained from diagonalisation and degree one.
It is expressed only on ordered edges, exactly as the upstream model uses them. -/
def HasMatchingSupport (W : WeightsN N D K) (colours : Fin D → Matching (Fin N)) : Prop :=
  ∀ v u, v < u → ∀ i j,
    (W (mkEdge v u i j) ≠ 0 ↔ i = j ∧ (colours i).partner v = u)

/-- A realized receiving word has one nonzero contribution when each colour
has exactly the support of its partner matching. -/
theorem pmSumN_ne_zero_of_realizes (W : WeightsN N D K)
    (colours : Fin D → Matching (Fin N)) (hsupport : HasMatchingSupport W colours)
    (M : Matching (Fin N)) (word : Fin N → Fin D) (hreal : Realizes colours word M) :
    pmSumN N D W word ≠ 0 := by
  apply pmSumN_ne_zero_of_forced W word M
  intro v u hvu
  rw [hsupport v u hvu]
  constructor
  · rintro ⟨_, hp⟩
    exact (hreal v).1.trans hp
  · intro hp
    refine ⟨?_, (hreal v).1.symm.trans hp⟩
    simpa only [hp] using (hreal v).2.symm

/-- The exact weighted equation system excludes any mixed matching after
the supported partner pattern has been established. -/
theorem no_mixed_of_eqSystem_and_support (W : WeightsN N D K)
    (colours : Fin D → Matching (Fin N)) (hsupport : HasMatchingSupport W colours)
    (hEq : EqSystemN N D W) : ¬ HasMixedMatching colours := by
  rintro ⟨M, word, hreal, v, w, hne⟩
  have hnonzero := pmSumN_ne_zero_of_realizes W colours hsupport M word hreal
  have hzero := hEq word
  rw [if_neg (not_allEqual_of_distinct word hne)] at hzero
  exact hnonzero hzero

/-- The complete ternary contradiction, conditional only on deriving the
diagonal unique-partner support pattern from the physical source. -/
theorem not_eqSystemN_three_of_matching_support (hN : 4 < N)
    (W : WeightsN N 3 K) (colours : Fin 3 → Matching (Fin N))
    (hsupport : HasMatchingSupport W colours) : ¬ EqSystemN N 3 W := by
  intro hEq
  exact no_mixed_of_eqSystem_and_support W colours hsupport hEq
    (hasMixedMatching_three colours (by simpa only [Fintype.card_fin] using hN))

end KrennAllOrders.ForcedMatchingSum
