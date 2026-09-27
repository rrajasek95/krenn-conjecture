/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import SiteAlgebra
import ForcedMatchingSum
import EndpointDegree

/-!
# From supported endpoint identities to the exact weighted contradiction

Symmetric, loop-free weights with one supported neighbour at each vertex give
an actual partner involution. Applying this to each diagonal colour block
connects the endpoint identities to the checked matching obstruction.
-/

namespace KrennAllOrders.SupportMatching

open MatchingModel SiteAlgebra ThreeMatching ForcedMatchingSum
open scoped BigOperators

variable {K V : Type*} [CommRing K] [IsDomain K]

/-- Extract the unique supported partner from a symmetric loop-free row system. -/
noncomputable def matchingOfUniqueSupport (S : V → V → K)
    (hsym : ∀ v u, S v u = S u v) (hdiag : ∀ v, S v v = 0)
    (hunique : ∀ v, ∃! u, S v u ≠ 0) : Matching V where
  partner v := (hunique v).choose
  partner_partner v := by
    apply Eq.symm
    apply (hunique ((hunique v).choose)).choose_spec.2
    rw [hsym]
    exact (hunique v).choose_spec.1
  partner_ne_self v := by
    intro h
    have hn := (hunique v).choose_spec.1
    rw [h, hdiag] at hn
    exact hn rfl

omit [IsDomain K] in
theorem matchingOfUniqueSupport_partner_iff (S : V → V → K)
    (hsym : ∀ v u, S v u = S u v) (hdiag : ∀ v, S v v = 0)
    (hunique : ∀ v, ∃! u, S v u ≠ 0) (v u : V) :
    (matchingOfUniqueSupport S hsym hdiag hunique).partner v = u ↔ S v u ≠ 0 := by
  constructor
  · intro h
    rw [← h]
    exact (hunique v).choose_spec.1
  · intro h
    exact ((hunique v).choose_spec.2 u h).symm

variable {N D : ℕ}

/-- The monochromatic block of the source's canonical symmetric edge matrix. -/
noncomputable def monochromaticWeight (W : WeightsN N D K) (i : Fin D)
    (v u : Fin N) : K := edgeMatrix W (v, i) (u, i)

noncomputable def colourMatchings (W : WeightsN N D K)
    (hunique : ∀ i v, ∃! u, monochromaticWeight W i v u ≠ 0) :
    Fin D → Matching (Fin N) := fun i =>
  matchingOfUniqueSupport (monochromaticWeight W i)
    (fun v u => edgeMatrix_symm W (v, i) (u, i))
    (fun v => edgeMatrix_same_site W v i i) (hunique i)

omit [IsDomain K] in
/-- Diagonal endpoint-colour blocks and one supported neighbour per colour
are precisely the partner-support hypotheses used by the weighted recursion. -/
theorem hasMatchingSupport_of_diagonal_unique (W : WeightsN N D K)
    (hdiagonal : ∀ v u i j, i ≠ j → edgeMatrix W (v, i) (u, j) = 0)
    (hunique : ∀ i v, ∃! u, monochromaticWeight W i v u ≠ 0) :
    HasMatchingSupport W (colourMatchings W hunique) := by
  intro v u hvu i j
  by_cases hij : i = j
  · subst j
    simp only [true_and]
    rw [show (colourMatchings W hunique i).partner v = u ↔
      monochromaticWeight W i v u ≠ 0 from
      matchingOfUniqueSupport_partner_iff _ _ _ _ v u]
    rw [monochromaticWeight, edgeMatrix_ordered W v u hvu]
  · have hw : W (mkEdge v u i j) = 0 := by
      rw [← edgeMatrix_ordered W v u hvu]
      exact hdiagonal v u i j hij
    simp only [hw, ne_eq, not_true_eq_false, hij, false_and]

theorem not_eqSystemN_three_of_diagonal_unique (hN : 4 < N)
    (W : WeightsN N 3 K)
    (hdiagonal : ∀ v u i j, i ≠ j → edgeMatrix W (v, i) (u, j) = 0)
    (hunique : ∀ i v, ∃! u, monochromaticWeight W i v u ≠ 0) :
    ¬ EqSystemN N 3 W :=
  not_eqSystemN_three_of_matching_support hN W (colourMatchings W hunique)
    (hasMatchingSupport_of_diagonal_unique W hdiagonal hunique)

/-- Row expansion and the supported endpoint identity close the exact weighted
equation system after diagonalisation. The three remaining physical hypotheses
are written explicitly in terms of the original edge weights. -/
theorem not_eqSystemN_three_of_endpoint_identities
    {F : Type*} [Field F] [CharZero F] (hN : 4 < N) (W : WeightsN N 3 F)
    (cofactor : Fin 3 → Fin N → Fin N → F)
    (hdiagonal : ∀ v u i j, i ≠ j → edgeMatrix W (v, i) (u, j) = 0)
    (hexpand : ∀ i p, ∑ q, monochromaticWeight W i p q * cofactor i p q = 1)
    (hendpoint : ∀ i p q, monochromaticWeight W i p q ≠ 0 →
      monochromaticWeight W i p q * cofactor i p q = 1) : ¬ EqSystemN N 3 W := by
  apply not_eqSystemN_three_of_diagonal_unique hN W hdiagonal
  intro i p
  exact exists_unique_support_of_endpoint_identities
    (monochromaticWeight W i p) (cofactor i p) 1 one_ne_zero (hexpand i p) (hendpoint i p)

end KrennAllOrders.SupportMatching
