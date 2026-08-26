/-
UNAUDITED (lane L1 staging), 2026-08-20.
Part of `formal/n8-diagonal`; see that directory's README.md.
-/
import N8Diagonal.Symm

/-!
# Endpoint symmetry may be assumed without loss of generality

`Symm.lean` buys general-position Laplace expansion (`haf_expand`, which the A3
clause family needs) from an endpoint-symmetry hypothesis `IsSymm W`. The
registry's `WeightsN` carries no such hypothesis, so this file discharges it.

The observation is that `pmSumList` on a strictly sorted list only ever reads
edge labels with `e.u < e.v`: the recursion always pairs the head — the least
remaining site — with a later one, and `List.erase` preserves sortedness. So
replacing `W` by its symmetrisation changes no value that `pmSumN` can see.
-/

namespace MonochromaticQuantumGraph

variable {α : Type} [CommSemiring α] {N D : Nat}

/-- Reflect every edge label into canonical endpoint order. -/
def symmetrize (W : WeightsN N D α) : WeightsN N D α :=
  fun e => if e.u < e.v then W e else W ⟨e.v, e.u, e.j, e.i⟩

theorem symmetrize_of_lt {W : WeightsN N D α} {u v : V N} {i j : Fin D} (h : u < v) :
    symmetrize W (mkEdge u v i j) = W (mkEdge u v i j) := by
  simp [symmetrize, mkEdge, h]

theorem isSymm_symmetrize (W : WeightsN N D α) : IsSymm (symmetrize W) := by
  rintro ⟨u, v, i, j⟩ huv
  rcases lt_trichotomy u v with h | h | h
  · have h' : ¬ v < u := not_lt_of_gt h
    simp [symmetrize, h, h']
  · exact absurd h huv
  · have h' : ¬ u < v := not_lt_of_gt h
    simp [symmetrize, h, h']

theorem isDiagonal_symmetrize {W : WeightsN N D α} (hW : IsDiagonal W) :
    IsDiagonal (symmetrize W) := by
  rintro ⟨u, v, i, j⟩ hij
  by_cases h : u < v
  · simpa [symmetrize, h] using hW ⟨u, v, i, j⟩ hij
  · simpa [symmetrize, h] using hW ⟨v, u, j, i⟩ (Ne.symm hij)

/-- On a strictly sorted list the matching sum reads only canonically oriented
labels, so symmetrising changes nothing. -/
theorem pmSumList_symmetrize (W : WeightsN N D α) (ι : V N → Fin D) :
    ∀ (n : Nat) (L : List (V N)), L.length = n → L.Pairwise (· < ·) →
      pmSumList (symmetrize W) ι L = pmSumList W ι L := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro L hL hsorted
    match L with
    | [] => rfl
    | v :: m =>
      have hn : n = m.length + 1 := by rw [← hL]; simp
      have hlt : ∀ u ∈ m, v < u := fun u hu => List.rel_of_pairwise_cons hsorted hu
      have hm : m.Pairwise (· < ·) := hsorted.of_cons
      rw [pmSumList_cons' (symmetrize W) ι v m, pmSumList_cons' W ι v m]
      refine congrArg List.sum (List.map_congr_left fun u hu => ?_)
      have hue : (m.erase u).Pairwise (· < ·) := List.Pairwise.sublist List.erase_sublist hm
      have hlen : (m.erase u).length < n := by
        have h1 := List.length_erase_of_mem hu
        have h2 : 1 ≤ m.length := List.length_pos_of_mem hu
        omega
      rw [symmetrize_of_lt (hlt u hu), ih _ hlen (m.erase u) rfl hue]

/-- The canonical vertex list is strictly increasing. -/
theorem vertices_sorted : ∀ N : Nat, (vertices N).Pairwise (· < ·)
  | 0 => by simp [vertices]
  | N + 1 => by
      rw [vertices]
      refine List.pairwise_cons.mpr ⟨?_, ?_⟩
      · intro b hb
        obtain ⟨x, _, rfl⟩ := List.mem_map.mp hb
        exact Fin.succ_pos x
      · exact List.pairwise_map.mpr
          ((vertices_sorted N).imp (fun h => Fin.succ_lt_succ_iff.mpr h))

theorem pmSumN_symmetrize (W : WeightsN N D α) (ι : V N → Fin D) :
    pmSumN N D (symmetrize W) ι = pmSumN N D W ι :=
  pmSumList_symmetrize W ι _ (vertices N) rfl (vertices_sorted N)

theorem eqSystemNZ_symmetrize {W : WeightsN N D α} (h : EqSystemNZ N D W) :
    EqSystemNZ N D (symmetrize W) := by
  refine ⟨fun ι hι => ?_, fun ι hι => ?_⟩
  · rw [pmSumN_symmetrize]; exact h.1 ι hι
  · rw [pmSumN_symmetrize]; exact h.2 ι hι

/-- **The WLOG step.** A counterexample may be taken endpoint-symmetric. -/
theorem exists_symm_of_exists {W : WeightsN N D α}
    (hW : IsDiagonal W) (hEq : EqSystemNZ N D W) :
    ∃ W' : WeightsN N D α, IsDiagonal W' ∧ IsSymm W' ∧ EqSystemNZ N D W' :=
  ⟨symmetrize W, isDiagonal_symmetrize hW, isSymm_symmetrize W, eqSystemNZ_symmetrize hEq⟩

end MonochromaticQuantumGraph
