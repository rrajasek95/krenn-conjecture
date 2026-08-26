/-
UNAUDITED — lane L1, 2026-08-20, pinned krenn-conjecture HEAD f9a3bd6.
Scratch: lives inside a throwaway formal-conjectures clone. Not a PR.
-/
import N8Diagonal.Haf

/-!
# The product formula

Equation (2) of `proofs/eight-site-diagonal-obstruction.md`: for a diagonal
weighting the perfect-matching sum of a word is the product over colours of the
hafnians of its colour classes. This is the whole structural content of
diagonality, and `IsDiagonal` is used nowhere else in the development.
-/

namespace MonochromaticQuantumGraph

open scoped BigOperators

variable {α : Type} {N D : Nat}

/-- Vanishing summands may be dropped from a mapped sum. -/
private theorem sum_map_filter {β : Type} [AddCommMonoid β]
    (l : List (V N)) (p : V N → Bool) (f : V N → β)
    (h : ∀ u ∈ l, p u = false → f u = 0) :
    (l.map f).sum = ((l.filter p).map f).sum := by
  induction l with
  | nil => simp
  | cons a t iht =>
    have iht' := iht (fun u hu hp => h u (List.mem_cons_of_mem _ hu) hp)
    rw [List.filter_cons]
    by_cases hp : p a = true
    · rw [if_pos hp, List.map_cons, List.sum_cons, List.map_cons, List.sum_cons, iht']
    · rw [if_neg hp, List.map_cons, List.sum_cons,
        h a (by simp) (by simpa using hp), zero_add, iht']

/-- A constant right factor comes out of a mapped sum. -/
private theorem sum_map_mul_right {β : Type} [NonUnitalNonAssocSemiring β]
    (l : List (V N)) (f : V N → β) (r : β) :
    (l.map (fun u => f u * r)).sum = (l.map f).sum * r := by
  induction l with
  | nil => simp
  | cons a t iht => simp [iht, add_mul]

variable [CommSemiring α]

/-- **The product formula.** For a diagonal weighting, the perfect-matching sum of a
word is the product over colours of the hafnians of its colour classes.

This is equation (2) of the source proof, and the only place `IsDiagonal` is used. -/
theorem pmSumList_diagonal {W : WeightsN N D α} (hW : IsDiagonal W) :
    ∀ (n : Nat) (L : List (V N)), L.length = n → ∀ (ι : V N → Fin D),
      pmSumList W ι L
        = ∏ c : Fin D, haf W c (L.filter (fun x => decide (ι x = c))) := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro L hL ι
    match L with
    | [] =>
      rw [show pmSumList W ι ([] : List (V N)) = 1 from rfl]
      simp
    | [v] =>
      refine (Finset.prod_eq_zero (Finset.mem_univ (ι v)) ?_).symm
      simp
    | v :: u₀ :: vs =>
      have hn : n = vs.length + 2 := by rw [← hL]; simp
      -- Step 1: Laplace at the head, then drop the off-colour summands (diagonality).
      rw [pmSumList_cons W ι v u₀ vs,
        sum_map_filter (u₀ :: vs) (fun x => decide (ι x = ι v)) _ ?vanish]
      case vanish =>
        intro u _ hu
        have hne : ι v ≠ ι u := by intro h; simp [h] at hu
        rw [hW (mkEdge v u (ι v) (ι u)) hne, zero_mul]
      -- Facts about the surviving sites.
      have hmem : ∀ u ∈ (u₀ :: vs).filter (fun x => decide (ι x = ι v)),
          u ∈ (u₀ :: vs) ∧ ι u = ι v := by
        intro u hu
        exact ⟨List.mem_of_mem_filter hu, by simpa using List.of_mem_filter hu⟩
      -- Step 2: the induction hypothesis on each erased tail.
      rw [List.map_congr_left (l := (u₀ :: vs).filter (fun x => decide (ι x = ι v)))
        (g := fun u => W (mkEdge v u (ι v) (ι v)) *
          ∏ c : Fin D, haf W c (((u₀ :: vs).erase u).filter (fun x => decide (ι x = c))))
        ?useIH]
      case useIH =>
        intro u hu
        obtain ⟨hut, huc⟩ := hmem u hu
        have hlen : ((u₀ :: vs).erase u).length = vs.length := by
          rw [List.length_erase_of_mem hut]; simp
        rw [ih vs.length (by omega) _ hlen ι, huc]
      -- Step 3: split off the head colour on the right.
      rw [← Finset.mul_prod_erase Finset.univ _ (Finset.mem_univ (ι v))]
      -- Step 4: split off the head colour inside each summand, and identify the
      -- other-colour classes with those of the whole word.
      rw [List.map_congr_left (l := (u₀ :: vs).filter (fun x => decide (ι x = ι v)))
        (g := fun u => (W (mkEdge v u (ι v) (ι v)) *
            haf W (ι v) (((u₀ :: vs).filter (fun x => decide (ι x = ι v))).erase u)) *
          ∏ c ∈ Finset.univ.erase (ι v),
            haf W c ((v :: u₀ :: vs).filter (fun x => decide (ι x = c)))) ?split]
      case split =>
        intro u hu
        obtain ⟨hut, huc⟩ := hmem u hu
        rw [← Finset.mul_prod_erase Finset.univ _ (Finset.mem_univ (ι v)), ← mul_assoc]
        congr 1
        · rw [List.erase_filter]
        · refine Finset.prod_congr rfl fun c hc => ?_
          have hcc : c ≠ ι v := Finset.ne_of_mem_erase hc
          have hnm : u ∉ (u₀ :: vs).filter (fun x => decide (ι x = c)) := by
            intro hm
            have huc' : ι u = c := by simpa using List.of_mem_filter hm
            exact hcc ((huc.symm.trans huc').symm)
          have hvc : ¬ ((fun x => decide (ι x = c)) v = true) := by
            simp only [decide_eq_true_eq]
            exact fun h => hcc h.symm
          rw [List.filter_cons_of_neg (p := fun x => decide (ι x = c)) (a := v) hvc,
            ← List.erase_filter, List.erase_of_not_mem hnm]
      -- Step 5: pull the constant other-colour product out of the sum.
      rw [sum_map_mul_right]
      congr 1
      -- Step 6: what is left is the Laplace expansion of the head colour class.
      rw [List.filter_cons_of_pos (p := fun x => decide (ι x = ι v)) (a := v)
        (l := u₀ :: vs) (by simp)]
      match hcl : (u₀ :: vs).filter (fun x => decide (ι x = ι v)) with
      | [] => simp
      | w :: ws => rw [haf_cons W (ι v) v w ws]

/-- The product formula on the canonical vertex list of `K_N`. -/
theorem pmSumN_diagonal {W : WeightsN N D α} (hW : IsDiagonal W) (ι : V N → Fin D) :
    pmSumN N D W ι
      = ∏ c : Fin D, haf W c ((vertices N).filter (fun x => decide (ι x = c))) :=
  pmSumList_diagonal hW _ (vertices N) rfl ι

end MonochromaticQuantumGraph
