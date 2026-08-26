/-
UNAUDITED — lane L1, 2026-08-20, pinned krenn-conjecture HEAD f9a3bd6.
Scratch: lives inside a throwaway formal-conjectures clone. Not a PR.
-/
import N8Diagonal.Product

/-!
# From the equation system to hafnian facts

The interface between the registry's `EqSystemNZ` and the hafnian world: the
two families of facts that everything downstream consumes, and the B2 witness
of Lemma 3.4 of `proofs/eight-site-diagonal-obstruction.md`.

The solve site is the **least** vertex, so the Laplace expansion used for B2 is
the head expansion `haf_cons`. That choice is free: the refutation is unchanged
at `z = 0` (measured, `encoder/disentangle.py`, 20/20 orbits still UNSAT).
-/

namespace MonochromaticQuantumGraph

open scoped BigOperators

variable {α : Type} [CommSemiring α] {N D : Nat} {W : WeightsN N D α}

/-- A constant word is constant. -/
theorem allEqual_const (c : Fin D) : allEqual (fun _ : V N => c) := by
  unfold allEqual allEqualList
  induction (vertices N) with
  | nil => simp
  | cons a t iht => cases t with
    | nil => simp
    | cons b s => simp_all

/-- The colour classes of a constant word: everything, or nothing. -/
theorem filter_const (c d : Fin D) (L : List (V N)) :
    L.filter (fun x => decide ((fun _ : V N => c) x = d)) = if c = d then L else [] := by
  by_cases h : c = d
  · simp [h]
  · simp [h]

/-- **H1.** Every monochromatic amplitude is a single hafnian, hence nonzero. -/
theorem haf_vertices_ne_zero (hW : IsDiagonal W) (hEq : EqSystemNZ N D W) (c : Fin D) :
    haf W c (vertices N) ≠ 0 := by
  have h0 := hEq.1 (fun _ => c) (allEqual_const c)
  rw [pmSumN_diagonal hW] at h0
  rw [Finset.prod_eq_single c] at h0
  · simpa [filter_const] using h0
  · intro d _ hd; simp [Ne.symm hd]
  · intro h; exact absurd (Finset.mem_univ c) h

/-- **H2.** Every mixed amplitude is a product of hafnians, hence that product vanishes. -/
theorem prod_haf_eq_zero (hW : IsDiagonal W) (hEq : EqSystemNZ N D W)
    (ι : V N → Fin D) (h : ¬ allEqual ι) :
    ∏ c : Fin D, haf W c ((vertices N).filter (fun x => decide (ι x = c))) = 0 :=
  (pmSumN_diagonal hW ι).symm.trans (hEq.2 ι h)

/-- A nonzero list sum has a nonzero summand. -/
private theorem exists_ne_zero_of_sum_ne_zero {β : Type} [AddCommMonoid β]
    {l : List β} (h : l.sum ≠ 0) : ∃ x ∈ l, x ≠ 0 := by
  by_contra hc
  push_neg at hc
  exact h (List.sum_eq_zero hc)

/-- **B2, per colour** (Lemma 3.4). Laplace at the least site: some site `y` has both a
nonzero edge to the solve site and a nonzero cofactor. -/
theorem exists_b2 [NoZeroDivisors α] (hW : IsDiagonal W) (hEq : EqSystemNZ N D W) (c : Fin D)
    (z u₀ : V N) (rest : List (V N)) (hv : vertices N = z :: u₀ :: rest) :
    ∃ y ∈ u₀ :: rest,
      W (mkEdge z y c c) ≠ 0 ∧ haf W c ((u₀ :: rest).erase y) ≠ 0 := by
  have hne := haf_vertices_ne_zero hW hEq c
  rw [hv, haf_cons W c z u₀ rest] at hne
  obtain ⟨x, hx, hx0⟩ := exists_ne_zero_of_sum_ne_zero hne
  obtain ⟨y, hy, rfl⟩ := List.mem_map.1 hx
  exact ⟨y, hy, mul_ne_zero_iff.1 hx0⟩

end MonochromaticQuantumGraph
