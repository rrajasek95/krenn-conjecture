/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import PhysicalEndpoint
import BinaryPairing

/-! # Binary receiving tensors on an actual twice-deleted physical core -/

namespace KrennAllOrders.RetainedBinary

open scoped BigOperators
open MvPolynomial MatchingModel SiteAlgebra RootResponse CofactorResponse PhysicalEndpoint

variable {K : Type*} [Field K] [CharZero K] {N D : ℕ}

/-- The physical sites retaining neither distinguished root. -/
abbrev RetainedSites (p q : V N) := {v : V N // v ≠ p ∧ v ≠ q}

/-- Extend a binary receiving word by the omitted root's receiving colour. -/
noncomputable def receivingWord (p q : V N) (b h : Fin D)
    (w : RetainedSites p q → Bool) : V N → Fin D :=
  fun v => if hv : v ≠ p ∧ v ≠ q then if w ⟨v, hv⟩ then h else b else h

omit [CharZero K] in
@[simp] theorem receivingWord_at_q (p q : V N) (b h : Fin D)
    (w : RetainedSites p q → Bool) : receivingWord p q b h w q = h := by
  simp [receivingWord]

@[simp] theorem receivingWord_at_retained (p q : V N) (b h : Fin D)
    (w : RetainedSites p q → Bool) (v : RetainedSites p q) :
    receivingWord p q b h w v = if w v then h else b := by
  simp only [receivingWord, dif_pos v.property]

@[simp] theorem receivingWord_true (p q : V N) (b h : Fin D) :
    receivingWord p q b h (fun _ => true) = fun _ => h := by
  funext v
  simp [receivingWord]

omit [CharZero K] in
/-- The literal pure retained word is exactly the pure binary tensor. -/
theorem coeff_pureRetainedWord (p q : V N) (b h : Fin D) (hbh : b ≠ h)
    (w : RetainedSites p q → Bool) :
    coeff (wordExponent (receivingWord p q b h w) (retainedVertices p q))
      (pureRetainedWord (K := K) p q h) =
      BinaryPairing.pure true w := by
  classical
  unfold pureRetainedWord BinaryPairing.pure
  rw [coeff_monomial]
  by_cases hw : w = (fun _ => true)
  · simp [hw]
  · rw [if_neg hw]
    apply if_neg
    intro heq
    apply hw
    funext v
    by_contra hv
    have hfalse : w v = false := Bool.eq_false_of_not_eq_true hv
    have hmem : v.val ∈ retainedVertices p q := (mem_retainedVertices p q v.val).mpr v.property
    have hcolor : h ≠ receivingWord p q b h w v.val := by
      rw [receivingWord_at_retained, hfalse]
      exact hbh.symm
    have hc := congrArg (fun n : SiteVariable N D →₀ ℕ => n (v.val, h)) heq
    rw [wordExponent_selected, (retainedVertices_nodup p q).count, if_pos hmem,
      wordExponent_wrong_color _ _ v.val h hcolor] at hc
    exact Nat.one_ne_zero hc

/-- The subtype tensor has exactly the physical vertices of the retained list. -/
noncomputable def retainedListEquiv (p q : V N) :
    RetainedSites p q ≃ ↥(retainedVertices p q).toFinset where
  toFun v := ⟨v.val, List.mem_toFinset.mpr ((mem_retainedVertices p q v.val).mpr v.property)⟩
  invFun v := ⟨v.val, (mem_retainedVertices p q v.val).mp (List.mem_toFinset.mp v.property)⟩
  left_inv _ := rfl
  right_inv _ := rfl

theorem card_retainedSites (p q : V N) (hpq : p ≠ q) :
    Fintype.card (RetainedSites p q) = N - 2 := by
  rw [Fintype.card_congr (retainedListEquiv p q), Fintype.card_coe,
    List.toFinset_card_of_nodup (retainedVertices_nodup p q), retainedVertices_length p q hpq]

theorem even_card_retainedSites (k : ℕ) (p q : V (2 * (k + 2))) (hpq : p ≠ q) :
    Even (Fintype.card (RetainedSites p q)) := by
  rw [card_retainedSites p q hpq]
  exact ⟨k + 1, by omega⟩

/-- Receiving exponents depend only on the colours of the listed sites. -/
theorem wordExponent_congr_on_list (ι κ : V N → Fin D) (L : List (V N))
    (h : ∀ v ∈ L, ι v = κ v) : wordExponent ι L = wordExponent κ L := by
  induction L with
  | nil => rfl
  | cons v L ih =>
    simp only [wordExponent, h v (by simp), ih (fun u hu => h u (by simp [hu]))]

omit [CharZero K] in
/-- The other pure retained word is the pure false receiving tensor. -/
theorem coeff_pureRetainedWord_false (p q : V N) (b h : Fin D) (hbh : b ≠ h)
    (w : RetainedSites p q → Bool) :
    coeff (wordExponent (receivingWord p q b h w) (retainedVertices p q))
      (pureRetainedWord (K := K) p q b) = BinaryPairing.pure false w := by
  classical
  unfold pureRetainedWord BinaryPairing.pure
  rw [coeff_monomial]
  by_cases hw : w = (fun _ => false)
  · rw [if_pos hw]
    apply if_pos
    apply wordExponent_congr_on_list
    intro v hv
    have hpq := (mem_retainedVertices p q v).mp hv
    simp [receivingWord, hpq, hw]
  · rw [if_neg hw]
    apply if_neg
    intro heq
    apply hw
    funext v
    by_contra hv
    have htrue : w v = true := Bool.eq_true_of_not_eq_false hv
    have hmem : v.val ∈ retainedVertices p q := (mem_retainedVertices p q v.val).mpr v.property
    have hcolor : b ≠ receivingWord p q b h w v.val := by
      rw [receivingWord_at_retained, htrue]
      exact hbh
    have hc := congrArg (fun n : SiteVariable N D →₀ ℕ => n (v.val, b)) heq
    rw [wordExponent_selected, (retainedVertices_nodup p q).count, if_pos hmem,
      wordExponent_wrong_color _ _ v.val b hcolor] at hc
    exact Nat.one_ne_zero hc

end KrennAllOrders.RetainedBinary
