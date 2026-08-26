/-
UNAUDITED — lane L1, 2026-08-20, pinned krenn-conjecture HEAD f9a3bd6.
Scratch: lives inside a throwaway formal-conjectures clone. Not a PR.
-/
import N8Diagonal.Defs

/-!
# Hafnians and the product formula for diagonal weightings

The one lemma diagonality buys: for a diagonal `W`, the perfect-matching sum of
a word factors as a product over colour classes of hafnians. This is equation
(2) of `proofs/eight-site-diagonal-obstruction.md`, and everything downstream
of it is bookkeeping.

`haf` needs no new recursion: `pmSumList W ι L` with `ι` constant at `c` is
already the hafnian of the colour-`c` weight function on `L`.
-/

namespace MonochromaticQuantumGraph

open scoped BigOperators

variable {α : Type} [Semiring α] {N D : Nat}

/-- The hafnian of the colour-`c` weight function on the sites `L`. -/
def haf (W : WeightsN N D α) (c : Fin D) (L : List (V N)) : α :=
  pmSumList W (fun _ => c) L

@[simp] theorem haf_nil (W : WeightsN N D α) (c : Fin D) : haf W c [] = 1 := rfl

@[simp] theorem haf_singleton (W : WeightsN N D α) (c : Fin D) (v : V N) :
    haf W c [v] = 0 := rfl

/-- One Laplace step for the fuelled recursion, with the fuel discharged. -/
theorem pmSumList_cons (W : WeightsN N D α) (ι : V N → Fin D)
    (v u₀ : V N) (vs : List (V N)) :
    pmSumList W ι (v :: u₀ :: vs) =
      ((u₀ :: vs).map (fun u =>
        W (mkEdge v u (ι v) (ι u)) * pmSumList W ι ((u₀ :: vs).erase u))).sum := by
  have h : pmSumList W ι (v :: u₀ :: vs) =
      ((u₀ :: vs).map (fun u =>
        W (mkEdge v u (ι v) (ι u)) *
          pmSumListAux W ι vs.length ((u₀ :: vs).erase u))).sum := rfl
  rw [h]
  refine congrArg List.sum (List.map_congr_left ?_)
  intro u hu
  refine congrArg _ ?_
  have hlen : ((u₀ :: vs).erase u).length = vs.length := by
    rw [List.length_erase_of_mem hu]
    simp
  unfold pmSumList
  rw [hlen]

/-- The Laplace step in uniform form: no side condition on the tail.

The empty-tail case is `haf W c [v] = 0` on the left and an empty sum on the right, so the
awkward `v :: u₀ :: vs` shape of `pmSumList_cons` is not needed downstream. -/
theorem pmSumList_cons' (W : WeightsN N D α) (ι : V N → Fin D) (v : V N) (m : List (V N)) :
    pmSumList W ι (v :: m) =
      (m.map (fun u => W (mkEdge v u (ι v) (ι u)) * pmSumList W ι (m.erase u))).sum := by
  cases m with
  | nil => rfl
  | cons u₀ vs => exact pmSumList_cons W ι v u₀ vs

/-- Laplace expansion of a hafnian at the head site, uniform form. -/
theorem haf_cons' (W : WeightsN N D α) (c : Fin D) (v : V N) (m : List (V N)) :
    haf W c (v :: m) =
      (m.map (fun u => W (mkEdge v u c c) * haf W c (m.erase u))).sum :=
  pmSumList_cons' W (fun _ => c) v m

/-- Laplace expansion of a hafnian at the head site. -/
theorem haf_cons (W : WeightsN N D α) (c : Fin D) (v u₀ : V N) (vs : List (V N)) :
    haf W c (v :: u₀ :: vs) =
      ((u₀ :: vs).map (fun u =>
        W (mkEdge v u c c) * haf W c ((u₀ :: vs).erase u))).sum :=
  pmSumList_cons W (fun _ => c) v u₀ vs

end MonochromaticQuantumGraph
