/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import Mathlib.Algebra.MvPolynomial.Basic
import Mathlib.Algebra.MvPolynomial.Eval
import Mathlib.Data.Fin.Basic
import Mathlib.Data.List.Pairwise
import Mathlib.RingTheory.MvPolynomial.WeightedHomogeneous

/-!
# The weighted endpoint-colour matching polynomial

The graph definitions and matching recursion below mirror
`FormalConjectures.Paper.MonochromaticQuantumGraph` at upstream commit
`e2c4441f9545b85790aebcfaa445e194fcab9d5b`. They are kept in a separate
namespace so this Mathlib-only package does not depend on the conjectures package.
A literal adapter to that upstream namespace is a separate obligation.

Variables are pairs `(vertex, colour)`. On a list without repeated vertices,
the matching polynomial is multilinear at each site, so it represents the
same-site-zero algebra used in Section 2 of the manuscript. No symmetry of
endpoint colours or edge weights is imposed. The ordered matching recursion
uses precisely the edge orientation used upstream.
-/

namespace KrennAllOrders.MatchingModel

open scoped BigOperators

abbrev V (N : ℕ) := Fin N

/-- Mirrored upstream edge labels; `u < v` is enforced by the ordered enumeration. -/
structure EdgeN (N D : ℕ) where
  u : V N
  v : V N
  i : Fin D
  j : Fin D
deriving DecidableEq

abbrev WeightsN (N D : ℕ) (α : Type*) := EdgeN N D → α

def mkEdge {N D : ℕ} (u v : V N) (i j : Fin D) : EdgeN N D :=
  ⟨u, v, i, j⟩

def vertices : (N : ℕ) → List (V N)
  | 0 => []
  | N + 1 => (0 : Fin (N + 1)) :: (vertices N).map Fin.succ

def pmSumListAux {α : Type*} [Semiring α] {N D : ℕ}
    (W : WeightsN N D α) (ι : V N → Fin D) : ℕ → List (V N) → α
  | 0, _ => 1
  | 1, _ => 0
  | _ + 2, [] => 1
  | _ + 2, [_] => 0
  | n + 2, v :: vs =>
      (vs.map fun u => W (mkEdge v u (ι v) (ι u)) *
        pmSumListAux W ι n (vs.erase u)).sum

def pmSumList {α : Type*} [Semiring α] {N D : ℕ}
    (W : WeightsN N D α) (ι : V N → Fin D) (L : List (V N)) : α :=
  pmSumListAux W ι L.length L

def pmSumN {α : Type*} [Semiring α] (N D : ℕ)
    (W : WeightsN N D α) (ι : V N → Fin D) : α :=
  pmSumList W ι (vertices N)

def allEqualList {N D : ℕ} (ι : V N → Fin D) (L : List (V N)) : Prop :=
  List.IsChain (fun v w => ι v = ι w) L

def allEqual {N D : ℕ} (ι : V N → Fin D) : Prop :=
  allEqualList ι (vertices N)

instance {N D : ℕ} (ι : V N → Fin D) (L : List (V N)) :
    Decidable (allEqualList ι L) := by
  letI : DecidableRel (fun v w : V N => ι v = ι w) := fun v w => inferInstance
  unfold allEqualList
  infer_instance

instance {N D : ℕ} (ι : V N → Fin D) : Decidable (allEqual ι) := by
  unfold allEqual
  infer_instance

def EqSystemN {α : Type*} [Semiring α] (N D : ℕ) (W : WeightsN N D α) : Prop :=
  ∀ ι : V N → Fin D, pmSumN N D W ι = if allEqual ι then 1 else 0

abbrev SiteVariable (N D : ℕ) := V N × Fin D
abbrev MatchingPolynomial (N D : ℕ) (α : Type*) [CommSemiring α] :=
  MvPolynomial (SiteVariable N D) α

variable {α : Type*} [CommSemiring α] {N D : ℕ}

/-- Sum the arbitrary endpoint-colour weights of one oriented edge. -/
noncomputable def edgePolynomial (W : WeightsN N D α) (v u : V N) :
    MatchingPolynomial N D α :=
  ∑ i : Fin D, ∑ j : Fin D,
    MvPolynomial.C (W (mkEdge v u i j)) *
      MvPolynomial.X (v, i) * MvPolynomial.X (u, j)

/-- The polynomial uses exactly the upstream matching recursion, including its fuel boundaries. -/
noncomputable def matchingPolynomialAux (W : WeightsN N D α) :
    ℕ → List (V N) → MatchingPolynomial N D α
  | 0, _ => 1
  | 1, _ => 0
  | _ + 2, [] => 1
  | _ + 2, [_] => 0
  | n + 2, v :: vs =>
      (vs.map fun u => edgePolynomial W v u *
        matchingPolynomialAux W n (vs.erase u)).sum

noncomputable def matchingPolynomialList (W : WeightsN N D α) (L : List (V N)) :
    MatchingPolynomial N D α := matchingPolynomialAux W L.length L

noncomputable def matchingPolynomialN (W : WeightsN N D α) :
    MatchingPolynomial N D α := matchingPolynomialList W (vertices N)

/-- Set the selected variable at each vertex to one and all other local colours to zero. -/
noncomputable def selector (ι : V N → Fin D) : SiteVariable N D → α :=
  fun z => if z.2 = ι z.1 then 1 else 0

@[simp]
theorem eval_edgePolynomial (W : WeightsN N D α) (ι : V N → Fin D) (v u : V N) :
    MvPolynomial.eval (selector ι) (edgePolynomial W v u) =
      W (mkEdge v u (ι v) (ι u)) := by
  classical
  simp [edgePolynomial, selector, MvPolynomial.eval_mul]

/-- Selector evaluation commutes with the exact matching recursion.
This statement alone is not yet the coefficient bridge. -/
theorem eval_matchingPolynomialAux (W : WeightsN N D α) (ι : V N → Fin D) :
    ∀ (n : ℕ) (L : List (V N)),
      MvPolynomial.eval (selector ι) (matchingPolynomialAux W n L) =
        pmSumListAux W ι n L
  | 0, _ => by simp [matchingPolynomialAux, pmSumListAux]
  | 1, _ => by simp [matchingPolynomialAux, pmSumListAux]
  | _ + 2, [] => by simp [matchingPolynomialAux, pmSumListAux]
  | _ + 2, [_] => by simp [matchingPolynomialAux, pmSumListAux]
  | n + 2, v :: u :: L => by
    simp only [matchingPolynomialAux, pmSumListAux]
    rw [map_list_sum]
    congr 1
    simp only [List.map_map]
    apply List.map_congr_left
    intro r _
    simp only [Function.comp_apply]
    rw [map_mul, eval_edgePolynomial, eval_matchingPolynomialAux W ι n]

theorem eval_matchingPolynomialN (W : WeightsN N D α) (ι : V N → Fin D) :
    MvPolynomial.eval (selector ι) (matchingPolynomialN W) = pmSumN N D W ι :=
  eval_matchingPolynomialAux W ι _ _

@[simp]
theorem matchingPolynomialList_nil (W : WeightsN N D α) :
    matchingPolynomialList W [] = 1 := rfl

@[simp]
theorem matchingPolynomialList_singleton (W : WeightsN N D α) (v : V N) :
    matchingPolynomialList W [v] = 0 := rfl

/-- Exponent of the word selected by `ι` on a vertex list. -/
noncomputable def wordExponent (ι : V N → Fin D) : List (V N) → SiteVariable N D →₀ ℕ
  | [] => 0
  | v :: L => Finsupp.single (v, ι v) 1 + wordExponent ι L

/-- A word has no variable of a colour other than its chosen local colour. -/
theorem wordExponent_wrong_color (ι : V N → Fin D) (L : List (V N))
    (v : V N) (i : Fin D) (hi : i ≠ ι v) : wordExponent ι L (v, i) = 0 := by
  induction L with
  | nil => simp [wordExponent]
  | cons u L ih =>
    have h : (u, ι u) ≠ (v, i) := by
      intro h
      have huv : u = v := congrArg Prod.fst h
      have hui : ι u = i := congrArg Prod.snd h
      exact hi (by simpa [huv] using hui.symm)
    simp [wordExponent, h, ih]

/-- Removing a listed vertex removes exactly its selected variable. -/
theorem wordExponent_erase (ι : V N → Fin D) (L : List (V N)) (u : V N)
    (hu : u ∈ L) :
    wordExponent ι L = Finsupp.single (u, ι u) 1 + wordExponent ι (L.erase u) := by
  induction L with
  | nil => simp at hu
  | cons v L ih =>
    by_cases hv : v = u
    · subst v
      simp [wordExponent]
    · have huL : u ∈ L := by simpa [Ne.symm hv] using hu
      rw [List.erase_cons_tail (by simpa using hv)]
      simp only [wordExponent]
      rw [ih huL]
      ac_rfl

private theorem coeff_X_mul_zero (P : MatchingPolynomial N D α)
    (m : SiteVariable N D →₀ ℕ) (z : SiteVariable N D) (hz : m z = 0) :
    MvPolynomial.coeff m (MvPolynomial.X z * P) = 0 := by
  classical
  simp [MvPolynomial.coeff_X_mul', Finsupp.mem_support_iff, hz]

/-- Only the two selected endpoint colours can contribute to a word coefficient. -/
theorem coeff_edgePolynomial_mul (W : WeightsN N D α) (ι : V N → Fin D)
    (L : List (V N)) (v u : V N) (P : MatchingPolynomial N D α) :
    MvPolynomial.coeff (wordExponent ι L) (edgePolynomial W v u * P) =
      W (mkEdge v u (ι v) (ι u)) *
        MvPolynomial.coeff (wordExponent ι L)
          (MvPolynomial.X (v, ι v) * MvPolynomial.X (u, ι u) * P) := by
  classical
  simp only [edgePolynomial, Finset.sum_mul, MvPolynomial.coeff_sum]
  rw [Finset.sum_eq_single (ι v)]
  · rw [Finset.sum_eq_single (ι u)]
    · rw [mul_assoc, mul_assoc, MvPolynomial.coeff_C_mul, mul_assoc]
    · intro j _ hj
      rw [show MvPolynomial.C (W (mkEdge v u (ι v) j)) *
          MvPolynomial.X (v, ι v) * MvPolynomial.X (u, j) * P =
          MvPolynomial.X (u, j) *
            (MvPolynomial.C (W (mkEdge v u (ι v) j)) * MvPolynomial.X (v, ι v) * P)
          by ring]
      exact coeff_X_mul_zero _ _ _ (wordExponent_wrong_color ι L u j hj)
    · simp
  · intro i _ hi
    apply Finset.sum_eq_zero
    intro j _
    rw [show MvPolynomial.C (W (mkEdge v u i j)) *
        MvPolynomial.X (v, i) * MvPolynomial.X (u, j) * P =
        MvPolynomial.X (v, i) *
          (MvPolynomial.C (W (mkEdge v u i j)) * MvPolynomial.X (u, j) * P)
        by ring]
    exact coeff_X_mul_zero _ _ _ (wordExponent_wrong_color ι L v i hi)
  · simp

/-- The coefficient of a complete selected word is the recursive matching sum.
The list-length hypothesis handles the exact empty/terminal fuel conventions. -/
theorem coeff_matchingPolynomialAux (W : WeightsN N D α) (ι : V N → Fin D) :
    ∀ (n : ℕ) (L : List (V N)), L.length = n →
      MvPolynomial.coeff (wordExponent ι L) (matchingPolynomialAux W n L) =
        pmSumListAux W ι n L
  | 0, L, h => by
    cases L with
    | nil => simp [wordExponent, matchingPolynomialAux, pmSumListAux]
    | cons v L => simp at h
  | 1, L, _ => by simp [matchingPolynomialAux, pmSumListAux]
  | _ + 2, [], h => by simp at h
  | _ + 2, [_], h => by simp at h
  | n + 2, v :: u :: L, h => by
    simp only [matchingPolynomialAux, pmSumListAux]
    rw [← MvPolynomial.coeffAddMonoidHom_apply]
    rw [map_list_sum]
    congr 1
    simp only [List.map_map]
    apply List.map_congr_left
    intro r hr
    simp only [Function.comp_apply, MvPolynomial.coeffAddMonoidHom_apply]
    rw [coeff_edgePolynomial_mul]
    have hw : wordExponent ι (v :: u :: L) =
        Finsupp.single (v, ι v) 1 + Finsupp.single (r, ι r) 1 +
          wordExponent ι ((u :: L).erase r) := by
      rw [wordExponent, wordExponent_erase ι (u :: L) r hr]
      ac_rfl
    rw [hw, mul_assoc, add_assoc, MvPolynomial.coeff_X_mul,
      MvPolynomial.coeff_X_mul]
    rw [coeff_matchingPolynomialAux W ι n ((u :: L).erase r)]
    rw [List.length_erase_of_mem hr]
    simp only [List.length_cons] at h ⊢
    omega

theorem coeff_matchingPolynomialList (W : WeightsN N D α) (ι : V N → Fin D)
    (L : List (V N)) :
    MvPolynomial.coeff (wordExponent ι L) (matchingPolynomialList W L) =
      pmSumList W ι L :=
  coeff_matchingPolynomialAux W ι L.length L rfl

theorem coeff_matchingPolynomialN (W : WeightsN N D α) (ι : V N → Fin D) :
    MvPolynomial.coeff (wordExponent ι (vertices N)) (matchingPolynomialN W) =
      pmSumN N D W ι :=
  coeff_matchingPolynomialList W ι _

theorem coeff_matchingPolynomialList_eq_selector (W : WeightsN N D α)
    (ι : V N → Fin D) (L : List (V N)) :
    MvPolynomial.coeff (wordExponent ι L) (matchingPolynomialList W L) =
      MvPolynomial.eval (selector ι) (matchingPolynomialList W L) :=
  (coeff_matchingPolynomialList W ι L).trans
    (eval_matchingPolynomialAux W ι L.length L).symm

/-- Give every local colour at a vertex the same independent site weight. -/
noncomputable def siteWeight (z : SiteVariable N D) : V N →₀ ℕ :=
  Finsupp.single z.1 1

/-- The prescribed multidegree, counting each occurrence of a listed site. -/
noncomputable def siteProfile : List (V N) → V N →₀ ℕ
  | [] => 0
  | v :: L => Finsupp.single v 1 + siteProfile L

/-- The abstract site weight is the sum of the exponents of its local colours. -/
theorem siteWeight_apply (m : SiteVariable N D →₀ ℕ) (v : V N) :
    Finsupp.weight siteWeight m v = ∑ i : Fin D, m (v, i) := by
  classical
  simp [Finsupp.weight_eq_sum, siteWeight, Fintype.sum_prod_type, Finsupp.single_apply]

theorem siteProfile_erase (L : List (V N)) (u : V N) (hu : u ∈ L) :
    siteProfile L = Finsupp.single u 1 + siteProfile (L.erase u) := by
  induction L with
  | nil => simp at hu
  | cons v L ih =>
    by_cases hv : v = u
    · subst v
      simp [siteProfile]
    · have huL : u ∈ L := by simpa [Ne.symm hv] using hu
      rw [List.erase_cons_tail (by simpa using hv)]
      simp only [siteProfile]
      rw [ih huL]
      ac_rfl

theorem siteProfile_apply (L : List (V N)) (v : V N) :
    siteProfile L v = L.count v := by
  induction L with
  | nil => simp [siteProfile]
  | cons u L ih =>
    simp [siteProfile, List.count_cons, ih, Finsupp.single_apply, add_comm]

theorem siteProfile_nodup (L : List (V N)) (hL : L.Nodup) (v : V N) :
    siteProfile L v = if v ∈ L then 1 else 0 := by
  rw [siteProfile_apply, hL.count]

private theorem weighted_list_sum (L : List (MatchingPolynomial N D α))
    (s : V N →₀ ℕ)
    (h : ∀ P ∈ L, MvPolynomial.IsWeightedHomogeneous siteWeight P s) :
    MvPolynomial.IsWeightedHomogeneous siteWeight L.sum s := by
  induction L with
  | nil => exact MvPolynomial.isWeightedHomogeneous_zero α siteWeight s
  | cons P L ih =>
    exact (h P (by simp)).add (ih fun Q hQ => h Q (by simp [hQ]))

theorem edgePolynomial_siteHomogeneous (W : WeightsN N D α) (v u : V N) :
    MvPolynomial.IsWeightedHomogeneous siteWeight (edgePolynomial W v u)
      (Finsupp.single v 1 + Finsupp.single u 1) := by
  classical
  unfold edgePolynomial
  apply MvPolynomial.IsWeightedHomogeneous.sum
  intro i _
  apply MvPolynomial.IsWeightedHomogeneous.sum
  intro j _
  simpa only [siteWeight, zero_add] using
    ((MvPolynomial.isWeightedHomogeneous_C siteWeight (W (mkEdge v u i j))).mul
      (MvPolynomial.isWeightedHomogeneous_X α siteWeight (v, i))).mul
        (MvPolynomial.isWeightedHomogeneous_X α siteWeight (u, j))

/-- Every monomial has precisely the prescribed degree at each site.
For nodup lists this proves the required site multilinearity. -/
theorem matchingPolynomialAux_siteHomogeneous (W : WeightsN N D α) :
    ∀ (n : ℕ) (L : List (V N)), L.length = n →
      MvPolynomial.IsWeightedHomogeneous siteWeight (matchingPolynomialAux W n L)
        (siteProfile L)
  | 0, L, h => by
    cases L with
    | nil => exact MvPolynomial.isWeightedHomogeneous_one α siteWeight
    | cons v L => simp at h
  | 1, L, _ => MvPolynomial.isWeightedHomogeneous_zero α siteWeight (siteProfile L)
  | _ + 2, [], h => by simp at h
  | _ + 2, [_], h => by simp at h
  | n + 2, v :: u :: L, h => by
    simp only [matchingPolynomialAux]
    apply weighted_list_sum
    intro P hP
    obtain ⟨r, hr, rfl⟩ := List.mem_map.mp hP
    have hlen : ((u :: L).erase r).length = n := by
      rw [List.length_erase_of_mem hr]
      simp only [List.length_cons] at h ⊢
      omega
    have hs := (edgePolynomial_siteHomogeneous W v r).mul
      (matchingPolynomialAux_siteHomogeneous W n ((u :: L).erase r) hlen)
    have hp : siteProfile (v :: u :: L) =
        (Finsupp.single v 1 + Finsupp.single r 1) +
          siteProfile ((u :: L).erase r) := by
      rw [siteProfile, siteProfile_erase (u :: L) r hr]
      ac_rfl
    rw [hp]
    exact hs

theorem matchingPolynomialList_siteHomogeneous (W : WeightsN N D α) (L : List (V N)) :
    MvPolynomial.IsWeightedHomogeneous siteWeight (matchingPolynomialList W L)
      (siteProfile L) :=
  matchingPolynomialAux_siteHomogeneous W L.length L rfl

@[simp]
theorem vertices_eq_finRange (n : ℕ) : vertices n = List.finRange n := by
  induction n with
  | zero => rfl
  | succ n ih => rw [vertices, ih, List.finRange_succ]

theorem vertices_nodup (n : ℕ) : (vertices n).Nodup := by
  rw [vertices_eq_finRange]
  exact (List.pairwise_lt_finRange n).imp fun h => ne_of_lt h

theorem vertices_pairwise_lt (n : ℕ) :
    (vertices n).Pairwise (fun v u => v < u) := by
  rw [vertices_eq_finRange]
  exact List.pairwise_lt_finRange n

@[simp]
theorem mem_vertices (v : V N) : v ∈ vertices N := by simp

theorem matchingPolynomialN_siteHomogeneous (W : WeightsN N D α) :
    MvPolynomial.IsWeightedHomogeneous siteWeight (matchingPolynomialN W)
      (siteProfile (vertices N)) :=
  matchingPolynomialList_siteHomogeneous W _

/-- Thus every occurring monomial has degree exactly one at every site. -/
theorem matchingPolynomialN_siteDegree (W : WeightsN N D α)
    (m : SiteVariable N D →₀ ℕ)
    (hm : MvPolynomial.coeff m (matchingPolynomialN W) ≠ 0) (v : V N) :
    Finsupp.weight siteWeight m v = 1 := by
  rw [matchingPolynomialN_siteHomogeneous W hm]
  rw [siteProfile_nodup _ (vertices_nodup N)]
  simp

/-- There is exactly one selected colour at each site of every occurring monomial. -/
theorem matchingPolynomialN_localDegree (W : WeightsN N D α)
    (m : SiteVariable N D →₀ ℕ)
    (hm : MvPolynomial.coeff m (matchingPolynomialN W) ≠ 0) (v : V N) :
    (∑ i : Fin D, m (v, i)) = 1 := by
  rw [← siteWeight_apply]
  exact matchingPolynomialN_siteDegree W m hm v

/-- The exact upstream equation system is equivalent to the corresponding full word coefficients. -/
theorem eqSystemN_iff_coefficients (W : WeightsN N D α) :
    EqSystemN N D W ↔ ∀ ι : V N → Fin D,
      MvPolynomial.coeff (wordExponent ι (vertices N)) (matchingPolynomialN W) =
        if allEqual ι then 1 else 0 := by
  simp only [EqSystemN, coeff_matchingPolynomialN]

/-- Parallel edges of the same endpoint colours aggregate linearly in the edge factor. -/
theorem edgePolynomial_add (W W' : WeightsN N D α) (v u : V N) :
    edgePolynomial (fun e => W e + W' e) v u =
      edgePolynomial W v u + edgePolynomial W' v u := by
  classical
  simp [edgePolynomial, map_add, add_mul, Finset.sum_add_distrib]

/-- Reversing an edge swaps both its vertices and its endpoint colours. -/
def reverseEdge (e : EdgeN N D) : EdgeN N D := ⟨e.v, e.u, e.j, e.i⟩

theorem edgePolynomial_reverse (W : WeightsN N D α) (v u : V N) :
    edgePolynomial (fun e => W (reverseEdge e)) v u = edgePolynomial W u v := by
  classical
  unfold edgePolynomial
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  simp only [mkEdge, reverseEdge]
  ring

/-- Weights on reversed/noncanonical edge labels do not affect the ordered matching sum. -/
theorem pmSumListAux_congr_ordered (W W' : WeightsN N D α) (ι : V N → Fin D)
    (hW : ∀ v u : V N, v < u → ∀ i j, W (mkEdge v u i j) = W' (mkEdge v u i j)) :
    ∀ (n : ℕ) (L : List (V N)), L.Pairwise (fun v u => v < u) →
      pmSumListAux W ι n L = pmSumListAux W' ι n L
  | 0, _, _ => rfl
  | 1, _, _ => rfl
  | _ + 2, [], _ => rfl
  | _ + 2, [_], _ => rfl
  | n + 2, v :: u :: L, hL => by
    simp only [pmSumListAux]
    congr 1
    apply List.map_congr_left
    intro r hr
    rw [hW v r (List.rel_of_pairwise_cons hL hr)]
    rw [pmSumListAux_congr_ordered W W' ι hW n ((u :: L).erase r)
      (List.Pairwise.erase r (List.pairwise_cons.mp hL).2)]

theorem pmSumN_congr_ordered (W W' : WeightsN N D α) (ι : V N → Fin D)
    (hW : ∀ v u : V N, v < u → ∀ i j, W (mkEdge v u i j) = W' (mkEdge v u i j)) :
    pmSumN N D W ι = pmSumN N D W' ι :=
  pmSumListAux_congr_ordered W W' ι hW _ _ (vertices_pairwise_lt N)

end KrennAllOrders.MatchingModel
