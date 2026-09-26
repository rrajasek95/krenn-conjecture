/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import Mathlib.Algebra.BigOperators.Field

/-!
# Supported endpoint identities force degree one

This is the finite-sum step in Section 5 of the all-orders two-replica proof.
The endpoint identities and the matching expansion are explicit hypotheses.
This file does not assume or assert the Krenn–Gu conjecture.
-/

namespace KrennAllOrders

open scoped BigOperators

variable {K ι : Type*} [Field K] [CharZero K] [Fintype ι]

open scoped Classical in
/-- If a row expansion has nonzero value `β` and each supported term equals
`β`, then the row has exactly one supported entry. -/
theorem card_support_eq_one_of_endpoint_identities
    (w cofactor : ι → K) (β : K) (hβ : β ≠ 0)
    (hexpand : ∑ q, w q * cofactor q = β)
    (hendpoint : ∀ q, w q ≠ 0 → w q * cofactor q = β) :
    (Finset.univ.filter fun q => w q ≠ 0).card = 1 := by
  classical
  let s := Finset.univ.filter fun q => w q ≠ 0
  have hsum : (s.card : K) * β = β := by
    calc
      (s.card : K) * β = ∑ _q ∈ s, β := by simp
      _ = ∑ q, w q * cofactor q := by
        rw [Finset.sum_filter]
        apply Finset.sum_congr rfl
        intro q _
        by_cases hq : w q = 0
        · simp [hq]
        · simp [hq, hendpoint q hq]
      _ = β := hexpand
  have hcard : (s.card : K) = 1 :=
    mul_right_cancel₀ hβ (by simpa using hsum)
  exact Nat.cast_injective (R := K) (by simpa using hcard)

/-- The same endpoint hypotheses give a unique supported neighbor. -/
theorem exists_unique_support_of_endpoint_identities
    (w cofactor : ι → K) (β : K) (hβ : β ≠ 0)
    (hexpand : ∑ q, w q * cofactor q = β)
    (hendpoint : ∀ q, w q ≠ 0 → w q * cofactor q = β) :
    ∃! q, w q ≠ 0 := by
  classical
  obtain ⟨q, hq⟩ := Finset.card_eq_one.mp
    (card_support_eq_one_of_endpoint_identities w cofactor β hβ hexpand hendpoint)
  refine ⟨q, ?_, ?_⟩
  · have hmem : q ∈ Finset.univ.filter (fun r => w r ≠ 0) := by
      rw [hq]
      exact Finset.mem_singleton_self q
    exact (Finset.mem_filter.mp hmem).2
  · intro r hr
    have hmem : r ∈ Finset.univ.filter (fun r => w r ≠ 0) :=
      Finset.mem_filter.mpr ⟨Finset.mem_univ r, hr⟩
    rw [hq] at hmem
    exact Finset.mem_singleton.mp hmem

end KrennAllOrders
