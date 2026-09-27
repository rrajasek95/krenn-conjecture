/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import RootResponse
import SupportMatching

/-!
# Exact remaining physical obligations for the ternary conjecture

The cofactor in this statement is the literal deleted-pair matching amplitude
defined in `RootResponse`. Row expansion, degree one, forced noncancellation,
and the combinatorial obstruction are proved imports. Only diagonalisation
and the supported endpoint identity remain explicit premises here.
-/

namespace KrennAllOrders.PhysicalClosure

open MatchingModel SiteAlgebra RootResponse SupportMatching

variable {K : Type*} [Field K] [CharZero K]

theorem not_eqSystemN_of_diagonal_and_endpoint {N : ℕ} (hN : 6 ≤ N) (heven : Even N)
    (W : WeightsN N 3 K)
    (hdiagonal : ∀ v u i j, i ≠ j → edgeMatrix W (v, i) (u, j) = 0)
    (hendpoint : ∀ i p q, edgeMatrix W (p, i) (q, i) ≠ 0 →
      edgeMatrix W (p, i) (q, i) * pureCofactor W i p q = 1) : ¬ EqSystemN N 3 W := by
  intro hEq
  obtain ⟨m, hm⟩ := heven
  have hmpos : 0 < m := by omega
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hmpos)
  have hsize : N = 2 * (k + 1) := by omega
  clear hm
  subst N
  apply not_eqSystemN_three_of_endpoint_identities (by omega) W (pureCofactor W)
    hdiagonal ?_ hendpoint hEq
  intro i p
  exact pureCofactor_rowSum_eq_one k W hEq p i

end KrennAllOrders.PhysicalClosure
