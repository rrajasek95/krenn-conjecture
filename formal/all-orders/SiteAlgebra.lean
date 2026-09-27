/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import MatchingModel
import Mathlib.Algebra.MvPolynomial.PDeriv
import Mathlib.Algebra.MvPolynomial.CommRing
import Mathlib.RingTheory.Ideal.Quotient.Defs
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/-!
# Physical sites and the divided matching power

This file connects the held matching-polynomial model to the physical-site
algebra of Section 2: every product of two local colours at one vertex is zero.
The graph weights remain arbitrary and the canonical endpoint orientation is
inherited from `MatchingModel`. No Wick or divided-power identity is assumed.
-/

namespace KrennAllOrders.SiteAlgebra

open scoped BigOperators
open MatchingModel

variable {R : Type*} {N D : ℕ}

section Ring

variable [CommRing R]

/-- All forbidden two-variable products at a common physical site. -/
def siteRelations (N D : ℕ) (R : Type*) [CommRing R] :
    Set (MatchingPolynomial N D R) :=
  {P | ∃ (v : V N) (i j : Fin D),
    P = MvPolynomial.X (v, i) * MvPolynomial.X (v, j)}

/-- The ideal imposing the physical-site product rule. -/
noncomputable def siteIdeal (N D : ℕ) (R : Type*) [CommRing R] :
    Ideal (MatchingPolynomial N D R) := Ideal.span (siteRelations N D R)

abbrev SiteRing (N D : ℕ) (R : Type*) [CommRing R] :=
  MatchingPolynomial N D R ⧸ siteIdeal N D R

noncomputable def project : MatchingPolynomial N D R →+* SiteRing N D R :=
  Ideal.Quotient.mk (siteIdeal N D R)

noncomputable def siteX (v : V N) (i : Fin D) : SiteRing N D R :=
  project (MvPolynomial.X (v, i))

/-- The defining physical-site identity, including the square of one colour. -/
@[simp]
theorem siteX_mul_same (v : V N) (i j : Fin D) :
    siteX (R := R) v i * siteX v j = 0 := by
  rw [siteX, siteX, ← map_mul]
  apply Ideal.Quotient.eq_zero_iff_mem.mpr
  exact Ideal.subset_span ⟨v, i, j, rfl⟩

@[simp]
theorem siteX_sq (v : V N) (i : Fin D) : (siteX (R := R) v i) ^ 2 = 0 := by
  rw [pow_two, siteX_mul_same]

/-- Canonical symmetric matrix of edge weights. Reversing vertices reverses endpoint colours. -/
noncomputable def edgeMatrix (W : WeightsN N D R)
    (z t : SiteVariable N D) : R :=
  if z.1 < t.1 then W (mkEdge z.1 t.1 z.2 t.2)
  else if t.1 < z.1 then W (mkEdge t.1 z.1 t.2 z.2) else 0

theorem edgeMatrix_symm (W : WeightsN N D R) (z t : SiteVariable N D) :
    edgeMatrix W z t = edgeMatrix W t z := by
  unfold edgeMatrix
  rcases lt_trichotomy z.1 t.1 with h | h | h
  · simp [h, not_lt_of_gt h]
  · simp [h]
  · simp [h, not_lt_of_gt h]

@[simp]
theorem edgeMatrix_same_site (W : WeightsN N D R) (v : V N) (i j : Fin D) :
    edgeMatrix W (v, i) (v, j) = 0 := by simp [edgeMatrix]

theorem edgeMatrix_ordered (W : WeightsN N D R) (v u : V N) (hvu : v < u)
    (i j : Fin D) : edgeMatrix W (v, i) (u, j) = W (mkEdge v u i j) := by
  simp [edgeMatrix, hvu]

end Ring

section Field

variable [Field R] [CharZero R]

/-- A symmetric quadratic, with the factor one-half removing the two orientations. -/
noncomputable def symmetricQuadratic (S : SiteVariable N D → SiteVariable N D → R) :
    MatchingPolynomial N D R :=
  MvPolynomial.C ((2 : R)⁻¹) *
    ∑ z : SiteVariable N D, ∑ t : SiteVariable N D,
      MvPolynomial.C (S z t) * MvPolynomial.X z * MvPolynomial.X t

noncomputable def rowPolynomial (S : SiteVariable N D → SiteVariable N D → R)
    (z : SiteVariable N D) : MatchingPolynomial N D R :=
  ∑ t : SiteVariable N D, MvPolynomial.C (S z t) * MvPolynomial.X t

/-- Formal differentiation extracts the actual incident row of a symmetric quadratic. -/
theorem pderiv_symmetricQuadratic
    (S : SiteVariable N D → SiteVariable N D → R)
    (hS : ∀ z t, S z t = S t z) (z : SiteVariable N D) :
    MvPolynomial.pderiv z (symmetricQuadratic S) = rowPolynomial S z := by
  classical
  have hterm (a b : SiteVariable N D) :
      MvPolynomial.pderiv z
        (MvPolynomial.C (S a b) * MvPolynomial.X a * MvPolynomial.X b) =
      (if a = z then MvPolynomial.C (S a b) * MvPolynomial.X b else 0) +
        (if b = z then MvPolynomial.C (S a b) * MvPolynomial.X a else 0) := by
    by_cases ha : a = z <;> by_cases hb : b = z <;> simp [ha, hb] <;> ring
  have hfirst :
      (∑ a : SiteVariable N D, ∑ b : SiteVariable N D,
        if a = z then MvPolynomial.C (S a b) * MvPolynomial.X b else 0) =
      rowPolynomial S z := by
    rw [Finset.sum_comm]
    simp [rowPolynomial]
  have hsecond :
      (∑ a : SiteVariable N D, ∑ b : SiteVariable N D,
        if b = z then MvPolynomial.C (S a b) * MvPolynomial.X a else 0) =
      rowPolynomial S z := by simp [rowPolynomial, hS]
  have hgrad : MvPolynomial.pderiv z
      (∑ a : SiteVariable N D, ∑ b : SiteVariable N D,
        MvPolynomial.C (S a b) * MvPolynomial.X a * MvPolynomial.X b) =
      rowPolynomial S z + rowPolynomial S z := by
    simp_rw [map_sum, hterm, Finset.sum_add_distrib]
    rw [hfirst, hsecond]
  rw [symmetricQuadratic, MvPolynomial.pderiv_C_mul, hgrad]
  have htwo : (2 : R) ≠ 0 := by norm_num
  have hC : MvPolynomial.C ((2 : R)⁻¹) * MvPolynomial.C (2 : R) =
      (1 : MatchingPolynomial N D R) := by
    rw [← map_mul, inv_mul_cancel₀ htwo, map_one]
  calc
    MvPolynomial.C ((2 : R)⁻¹) *
        (rowPolynomial S z + rowPolynomial S z) =
      (MvPolynomial.C ((2 : R)⁻¹) * MvPolynomial.C (2 : R)) * rowPolynomial S z := by
        simp only [map_ofNat]
        ring
    _ = rowPolynomial S z := by rw [hC, one_mul]

/-- The actual edge quadratic used by the graph model. -/
noncomputable def sourceQuadratic (W : WeightsN N D R) : MatchingPolynomial N D R :=
  symmetricQuadratic (edgeMatrix W)

theorem pderiv_sourceQuadratic (W : WeightsN N D R) (z : SiteVariable N D) :
    MvPolynomial.pderiv z (sourceQuadratic W) = rowPolynomial (edgeMatrix W) z :=
  pderiv_symmetricQuadratic _ (edgeMatrix_symm W) z

/-- A selected word contains no variable at a site omitted from its list. -/
theorem wordExponent_not_mem (ι : V N → Fin D) (L : List (V N))
    (v : V N) (hv : v ∉ L) (i : Fin D) : wordExponent ι L (v, i) = 0 := by
  induction L with
  | nil => simp [wordExponent]
  | cons u L ih =>
    have hvu : v ≠ u := by
      intro h
      exact hv (List.mem_cons.mpr (Or.inl h))
    have hvL : v ∉ L := by
      intro h
      exact hv (List.mem_cons.mpr (Or.inr h))
    have hpair : (u, ι u) ≠ (v, i) := by
      intro h
      exact hvu (congrArg Prod.fst h).symm
    simp [wordExponent, hpair, ih hvL]

omit [CharZero R] in
/-- Multiplying by a row extracts its possible partners in a nodup selected word. -/
theorem coeff_rowPolynomial_mul
    (S : SiteVariable N D → SiteVariable N D → R) (z : SiteVariable N D)
    (ι : V N → Fin D) (L : List (V N)) (hL : L.Nodup)
    (P : MatchingPolynomial N D R) :
    MvPolynomial.coeff (wordExponent ι L) (rowPolynomial S z * P) =
      (L.map fun u => S z (u, ι u) *
        MvPolynomial.coeff (wordExponent ι (L.erase u)) P).sum := by
  classical
  simp only [rowPolynomial, Finset.sum_mul, MvPolynomial.coeff_sum,
    Fintype.sum_prod_type, mul_assoc, MvPolynomial.coeff_C_mul]
  have hcolor (u : V N) :
      (∑ i : Fin D, S z (u, i) * MvPolynomial.coeff (wordExponent ι L)
        (MvPolynomial.X (u, i) * P)) =
      S z (u, ι u) * MvPolynomial.coeff (wordExponent ι L)
        (MvPolynomial.X (u, ι u) * P) := by
    apply Finset.sum_eq_single (ι u)
    · intro i _ hi
      simp [MvPolynomial.coeff_X_mul', Finsupp.mem_support_iff,
        wordExponent_wrong_color ι L u i hi]
    · simp
  simp_rw [hcolor]
  let f := fun u : V N => S z (u, ι u) * MvPolynomial.coeff (wordExponent ι L)
    (MvPolynomial.X (u, ι u) * P)
  change (∑ u, f u) = _
  calc
    (∑ u, f u) = ∑ u ∈ L.toFinset, f u := by
      symm
      apply Finset.sum_subset (Finset.subset_univ _)
      intro u _ hu
      have huL : u ∉ L := by simpa using hu
      simp [f, MvPolynomial.coeff_X_mul', Finsupp.mem_support_iff,
        wordExponent_not_mem ι L u huL (ι u)]
    _ = ∑ u ∈ L.toFinset, S z (u, ι u) *
        MvPolynomial.coeff (wordExponent ι (L.erase u)) P := by
      apply Finset.sum_congr rfl
      intro u hu
      have huL : u ∈ L := List.mem_toFinset.mp hu
      simp only [f]
      rw [wordExponent_erase ι L u huL, MvPolynomial.coeff_X_mul]
    _ = _ := List.sum_toFinset _ hL

/-- Since a root occurs exactly once, its coefficient is extracted without a factorial. -/
theorem coeff_root_pderiv (P : MatchingPolynomial N D R) (ι : V N → Fin D)
    (v : V N) (L : List (V N)) (hv : v ∉ L) :
    MvPolynomial.coeff (wordExponent ι (v :: L)) P =
      MvPolynomial.coeff (wordExponent ι L) (MvPolynomial.pderiv (v, ι v) P) := by
  rw [MvPolynomial.coeff_pderiv, wordExponent_not_mem ι L v hv (ι v)]
  simp [wordExponent, add_comm]

/-- Exact root extraction from a quadratic power; the remaining quadratic is unchanged. -/
theorem coeff_sourceQuadratic_pow_succ (W : WeightsN N D R) (ι : V N → Fin D)
    (k : ℕ) (v : V N) (L : List (V N)) (hv : v ∉ L) (hL : L.Nodup) :
    MvPolynomial.coeff (wordExponent ι (v :: L)) (sourceQuadratic W ^ (k + 1)) =
      (k + 1 : R) * (L.map fun u => edgeMatrix W (v, ι v) (u, ι u) *
        MvPolynomial.coeff (wordExponent ι (L.erase u)) (sourceQuadratic W ^ k)).sum := by
  rw [coeff_root_pderiv _ ι v L hv, MvPolynomial.pderiv_pow,
    pderiv_sourceQuadratic]
  simp only [Nat.add_sub_cancel]
  rw [show (↑(k + 1) : MatchingPolynomial N D R) * sourceQuadratic W ^ k *
      rowPolynomial (edgeMatrix W) (v, ι v) =
      MvPolynomial.C (k + 1 : R) *
        (rowPolynomial (edgeMatrix W) (v, ι v) * sourceQuadratic W ^ k) by
      simp only [Nat.cast_add, Nat.cast_one, map_add, map_natCast, map_one]
      ring]
  rw [MvPolynomial.coeff_C_mul, coeff_rowPolynomial_mul _ _ ι L hL]

/-- The exact factorial matching coefficient, with the canonical edge orientation.
The empty matching is included, and the quadratic is unchanged throughout the recursion. -/
theorem coeff_sourceQuadratic_pow (W : WeightsN N D R) (ι : V N → Fin D) :
    ∀ (k : ℕ) (L : List (V N)), L.length = 2 * k →
      L.Pairwise (fun v u => v < u) →
      MvPolynomial.coeff (wordExponent ι L) (sourceQuadratic W ^ k) =
        (k.factorial : R) * pmSumListAux W ι (2 * k) L := by
  intro k
  induction k with
  | zero =>
    intro L hlen _
    have hL : L = [] := by simpa using hlen
    subst L
    simp [wordExponent, pmSumListAux]
  | succ k ih =>
    intro L hlen hord
    cases L with
    | nil => simp at hlen
    | cons v vs =>
      have hn : (v :: vs).Nodup := hord.imp (fun h => ne_of_lt h)
      have hv : v ∉ vs := (List.nodup_cons.mp hn).1
      have hvs : vs.Nodup := (List.nodup_cons.mp hn).2
      rw [coeff_sourceQuadratic_pow_succ W ι k v vs hv hvs]
      have hterm :
          (vs.map fun u => edgeMatrix W (v, ι v) (u, ι u) *
            MvPolynomial.coeff (wordExponent ι (vs.erase u))
              (sourceQuadratic W ^ k)).sum =
          (k.factorial : R) *
            (vs.map fun u => W (mkEdge v u (ι v) (ι u)) *
              pmSumListAux W ι (2 * k) (vs.erase u)).sum := by
        rw [← List.sum_map_mul_left]
        congr 1
        apply List.map_congr_left
        intro u hu
        have helen : (vs.erase u).length = 2 * k := by
          rw [List.length_erase_of_mem hu]
          simp only [List.length_cons] at hlen
          omega
        rw [edgeMatrix_ordered W v u (List.rel_of_pairwise_cons hord hu),
          ih (vs.erase u) helen (List.Pairwise.erase u (List.pairwise_cons.mp hord).2)]
        ring
      rw [hterm]
      have htwo : 2 * (k + 1) = 2 * k + 2 := by omega
      cases vs with
      | nil => simp only [List.length_cons, List.length_nil] at hlen; omega
      | cons u us =>
        rw [htwo, Nat.factorial_succ, Nat.cast_mul]
        simp only [pmSumListAux, Nat.cast_add, Nat.cast_one]
        ring

/-- Full-site coefficients of the ordinary quadratic power are exactly factorial matching sums. -/
theorem coeff_sourceQuadratic_pow_full (k : ℕ)
    (W : WeightsN (2 * k) D R) (ι : V (2 * k) → Fin D) :
    MvPolynomial.coeff (wordExponent ι (vertices (2 * k)))
      (sourceQuadratic W ^ k) = (k.factorial : R) * pmSumN (2 * k) D W ι := by
  simpa [pmSumN, pmSumList] using
    coeff_sourceQuadratic_pow W ι k (vertices (2 * k))
      (by simp) (vertices_pairwise_lt _)

/-- The divided power is defined in the ordinary ring; its physical projection is separate. -/
noncomputable def dividedSourcePower (W : WeightsN N D R) (k : ℕ) :
    MatchingPolynomial N D R :=
  MvPolynomial.C ((k.factorial : R)⁻¹) * sourceQuadratic W ^ k

/-- The quadratic divided top power has the literal recursive matching coefficients. -/
theorem coeff_dividedSourcePower_full (k : ℕ)
    (W : WeightsN (2 * k) D R) (ι : V (2 * k) → Fin D) :
    MvPolynomial.coeff (wordExponent ι (vertices (2 * k)))
      (dividedSourcePower W k) = pmSumN (2 * k) D W ι := by
  rw [dividedSourcePower, MvPolynomial.coeff_C_mul, coeff_sourceQuadratic_pow_full]
  have hf : (k.factorial : R) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero k)
  rw [← mul_assoc, inv_mul_cancel₀ hf, one_mul]

end Field

section QuotientCoefficients

variable [CommRing R]

/-- The selected colour exponent is the number of occurrences of its site. -/
theorem wordExponent_selected (ι : V N → Fin D) (L : List (V N)) (v : V N) :
    wordExponent ι L (v, ι v) = L.count v := by
  induction L with
  | nil => simp [wordExponent]
  | cons u L ih =>
    by_cases h : u = v
    · subst u
      simp [wordExponent, ih, add_comm]
    · have hp : (u, ι u) ≠ (v, ι v) := by
        intro hp
        exact h (congrArg Prod.fst hp)
      simp [wordExponent, hp, h, ih]

/-- The degree at a physical vertex counts all its endpoint colours together. -/
noncomputable def siteDegree (m : SiteVariable N D →₀ ℕ) (v : V N) : ℕ :=
  ∑ i : Fin D, m (v, i)

/-- Ordinary monomial degree, grouped by physical vertices. -/
noncomputable def exponentDegree (m : SiteVariable N D →₀ ℕ) : ℕ :=
  ∑ v : V N, siteDegree m v

theorem weight_one_eq_exponentDegree (m : SiteVariable N D →₀ ℕ) :
    Finsupp.weight (fun _ : SiteVariable N D => (1 : ℕ)) m = exponentDegree m := by
  simp [Finsupp.weight_eq_sum, exponentDegree, siteDegree, Fintype.sum_prod_type]

/-- A doubled physical-site degree contains two (possibly equal) local variables. -/
theorem exists_same_site_pair_le (m : SiteVariable N D →₀ ℕ) (v : V N)
    (h : 2 ≤ siteDegree m v) :
    ∃ i j : Fin D, Finsupp.single (v, i) 1 + Finsupp.single (v, j) 1 ≤ m := by
  classical
  obtain ⟨i, _, hi⟩ := Finset.sum_pos_iff.mp (show 0 < ∑ i : Fin D, m (v, i) by
    change 0 < siteDegree m v
    omega)
  have hile : Finsupp.single (v, i) 1 ≤ m := Finsupp.single_le_iff.mpr hi
  let t := m - Finsupp.single (v, i) 1
  have ht : t + Finsupp.single (v, i) 1 = m := tsub_add_cancel_of_le hile
  have hd : siteDegree t v + 1 = siteDegree m v := by
    rw [← ht]
    simp [siteDegree, Finset.sum_add_distrib, Finsupp.single_apply]
  obtain ⟨j, _, hj⟩ := Finset.sum_pos_iff.mp (show 0 < ∑ j : Fin D, t (v, j) by
    change 0 < siteDegree t v
    omega)
  refine ⟨i, j, ?_⟩
  have hjle : Finsupp.single (v, j) 1 ≤ t := Finsupp.single_le_iff.mpr hj
  calc
    Finsupp.single (v, i) 1 + Finsupp.single (v, j) 1 ≤
        Finsupp.single (v, i) 1 + t := add_le_add le_rfl hjle
    _ = m := by rw [add_comm, ht]

/-- Every monomial with a doubled physical site is zero in the quotient. -/
theorem monomial_mem_siteIdeal_of_doubled (m : SiteVariable N D →₀ ℕ) (a : R)
    (v : V N) (h : 2 ≤ siteDegree m v) :
    MvPolynomial.monomial m a ∈ siteIdeal N D R := by
  classical
  obtain ⟨i, j, hij⟩ := exists_same_site_pair_le m v h
  have hgen : (MvPolynomial.monomial
      (Finsupp.single (v, i) 1 + Finsupp.single (v, j) 1) (1 : R)) ∈ siteIdeal N D R := by
    have heq : (MvPolynomial.X (v, i) * MvPolynomial.X (v, j) :
        MatchingPolynomial N D R) = MvPolynomial.monomial
          (Finsupp.single (v, i) 1 + Finsupp.single (v, j) 1) 1 := by
      simp [MvPolynomial.X, MvPolynomial.monomial_mul]
    rw [← heq]
    exact Ideal.subset_span ⟨v, i, j, rfl⟩
  have heq := add_tsub_cancel_of_le hij
  rw [← heq]
  simpa only [MvPolynomial.monomial_mul, one_mul] using
    (siteIdeal N D R).mul_mem_right
      (MvPolynomial.monomial (m - (Finsupp.single (v, i) 1 + Finsupp.single (v, j) 1)) a)
      hgen

/-- A squarefree-site monomial of full degree chooses one colour at each vertex. -/
theorem exists_word_of_full_squarefree (m : SiteVariable N D →₀ ℕ)
    (hs : ∀ v, siteDegree m v ≤ 1) (hd : exponentDegree m = N) :
    ∃ ι : V N → Fin D, m = wordExponent ι (vertices N) := by
  classical
  have hone : ∀ v, siteDegree m v = 1 := by
    have hh : ∀ v ∈ Finset.univ, siteDegree m v = 1 :=
      (Finset.sum_eq_sum_iff_of_le (fun v (_ : v ∈ Finset.univ) => hs v)).mp
        (by simpa [exponentDegree] using hd)
    exact fun v => hh v (Finset.mem_univ v)
  have hex (v : V N) : ∃ i : Fin D, 0 < m (v, i) := by
    obtain ⟨i, _, hi⟩ := Finset.sum_pos_iff.mp (show 0 < ∑ i : Fin D, m (v, i) by
      change 0 < siteDegree m v
      rw [hone v]
      norm_num)
    exact ⟨i, hi⟩
  choose ι hι using hex
  refine ⟨ι, ?_⟩
  ext z
  rcases z with ⟨v, i⟩
  have hchosen : m (v, ι v) = 1 := by
    have hle := Finset.single_le_sum (fun j (_ : j ∈ Finset.univ) => Nat.zero_le (m (v, j)))
      (Finset.mem_univ (ι v))
    change m (v, ι v) ≤ siteDegree m v at hle
    rw [hone v] at hle
    exact Nat.le_antisymm hle (hι v)
  by_cases hi : i = ι v
  · subst i
    rw [wordExponent_selected, (vertices_nodup N).count]
    simp only [mem_vertices, if_true]
    exact hchosen
  · have herase : ∑ j ∈ Finset.univ.erase (ι v), m (v, j) = 0 := by
      have hh := Finset.sum_erase_add Finset.univ (fun j => m (v, j)) (Finset.mem_univ (ι v))
      rw [hchosen] at hh
      change (∑ j ∈ Finset.univ.erase (ι v), m (v, j)) + 1 = siteDegree m v at hh
      rw [hone v] at hh
      omega
    have hle := Finset.single_le_sum (fun j (_ : j ∈ Finset.univ.erase (ι v)) =>
      Nat.zero_le (m (v, j))) (Finset.mem_erase.mpr ⟨hi, Finset.mem_univ i⟩)
    rw [herase] at hle
    rw [wordExponent_wrong_color ι (vertices N) v i hi]
    exact Nat.eq_zero_of_le_zero hle

/-- Full-degree physical-site tensors are determined by their receiving-word coefficients. -/
theorem project_eq_of_full_coefficients (P Q : MatchingPolynomial N D R)
    (hP : MvPolynomial.IsWeightedHomogeneous (fun _ : SiteVariable N D => (1 : ℕ)) P N)
    (hQ : MvPolynomial.IsWeightedHomogeneous (fun _ : SiteVariable N D => (1 : ℕ)) Q N)
    (hc : ∀ ι : V N → Fin D,
      MvPolynomial.coeff (wordExponent ι (vertices N)) P =
        MvPolynomial.coeff (wordExponent ι (vertices N)) Q) : project P = project Q := by
  apply sub_eq_zero.mp
  rw [← map_sub project]
  apply Ideal.Quotient.eq_zero_iff_mem.mpr
  rw [MvPolynomial.as_sum (P - Q)]
  apply Ideal.sum_mem
  intro m hm
  by_cases hdouble : ∃ v, 2 ≤ siteDegree m v
  · obtain ⟨v, hv⟩ := hdouble
    exact monomial_mem_siteIdeal_of_doubled m _ v hv
  · have hs : ∀ v, siteDegree m v ≤ 1 := by
      intro v
      by_contra hv
      apply hdouble
      exact ⟨v, by omega⟩
    have hd : exponentDegree m = N := by
      rw [← weight_one_eq_exponentDegree]
      exact (hP.sub hQ) (MvPolynomial.mem_support_iff.mp hm)
    obtain ⟨ι, rfl⟩ := exists_word_of_full_squarefree m hs hd
    rw [MvPolynomial.coeff_sub, hc ι, sub_self, MvPolynomial.monomial_zero]
    exact (siteIdeal N D R).zero_mem

theorem wordExponent_selected_le_one (ι : V N → Fin D) (L : List (V N))
    (hL : L.Nodup) (v : V N) : wordExponent ι L (v, ι v) ≤ 1 := by
  rw [wordExponent_selected, hL.count]
  split_ifs <;> omega

/-- Every forbidden common-site product has zero coefficient at a nodup receiving word,
even after arbitrary polynomial multiplication. -/
theorem coeff_siteRelation_mul (ι : V N → Fin D) (L : List (V N)) (hL : L.Nodup)
    (v : V N) (i j : Fin D) (P : MatchingPolynomial N D R) :
    MvPolynomial.coeff (wordExponent ι L)
      ((MvPolynomial.X (v, i) * MvPolynomial.X (v, j)) * P) = 0 := by
  classical
  have hnot : ¬ (Finsupp.single (v, i) 1 + Finsupp.single (v, j) 1 ≤
      wordExponent ι L) := by
    intro h
    by_cases hi : i = ι v
    · by_cases hj : j = ι v
      · have hc := h (v, ι v)
        have hb := wordExponent_selected_le_one ι L hL v
        simp [hi, hj] at hc
        omega
      · have hc := h (v, j)
        simp [wordExponent_wrong_color ι L v j hj] at hc
    · have hc := h (v, i)
      simp [wordExponent_wrong_color ι L v i hi] at hc
  have hmono : (MvPolynomial.X (v, i) * MvPolynomial.X (v, j) :
      MatchingPolynomial N D R) =
      MvPolynomial.monomial (Finsupp.single (v, i) 1 + Finsupp.single (v, j) 1) 1 := by
    simp [MvPolynomial.X, MvPolynomial.monomial_mul]
  rw [hmono, MvPolynomial.coeff_monomial_mul', if_neg hnot]

/-- Nondoubled receiving-word coefficients annihilate the entire site ideal. -/
theorem coeff_siteIdeal_zero (ι : V N → Fin D) (L : List (V N)) (hL : L.Nodup)
    (P : MatchingPolynomial N D R) (hP : P ∈ siteIdeal N D R) :
    MvPolynomial.coeff (wordExponent ι L) P = 0 := by
  classical
  have hall : ∀ Q ∈ siteIdeal N D R, ∀ A : MatchingPolynomial N D R,
      MvPolynomial.coeff (wordExponent ι L) (Q * A) = 0 := by
    intro Q hQ
    induction hQ using Submodule.span_induction with
    | mem Q hQ =>
      rcases hQ with ⟨v, i, j, rfl⟩
      exact fun A => coeff_siteRelation_mul ι L hL v i j A
    | zero => intro A; simp
    | add Q Q' _ _ ih ih' =>
      intro A
      simp [add_mul, ih A, ih' A]
    | smul A Q _ ih =>
      intro A'
      simpa only [smul_eq_mul, mul_assoc, mul_left_comm A Q] using ih (A * A')
  simpa using hall P hP 1

/-- Thus the selected coefficient is intrinsic to the physical-site quotient. -/
theorem coeff_eq_of_project_eq (ι : V N → Fin D) (L : List (V N)) (hL : L.Nodup)
    (P Q : MatchingPolynomial N D R) (h : project P = project Q) :
    MvPolynomial.coeff (wordExponent ι L) P =
      MvPolynomial.coeff (wordExponent ι L) Q := by
  have hmem : P - Q ∈ siteIdeal N D R :=
    (Ideal.Quotient.mk_eq_mk_iff_sub_mem P Q).mp h
  have hc := coeff_siteIdeal_zero ι L hL (P - Q) hmem
  rw [MvPolynomial.coeff_sub] at hc
  exact sub_eq_zero.mp hc

/-- Full-site coefficients on the actual quotient, independent of representative. -/
noncomputable def siteCoefficient (ι : V N → Fin D) : SiteRing N D R → R :=
  fun q => MvPolynomial.coeff (wordExponent ι (vertices N)) (Quotient.out q)

@[simp]
theorem siteCoefficient_project (ι : V N → Fin D) (P : MatchingPolynomial N D R) :
    siteCoefficient ι (project P) =
      MvPolynomial.coeff (wordExponent ι (vertices N)) P := by
  apply coeff_eq_of_project_eq ι (vertices N) (vertices_nodup N)
  exact Ideal.Quotient.mk_out (project P)

/-- Coefficient extraction is additive on the physical-site algebra. -/
noncomputable def siteCoefficientHom (ι : V N → Fin D) : SiteRing N D R →+ R where
  toFun := siteCoefficient ι
  map_zero' := by
    rw [← map_zero project, siteCoefficient_project]
    exact MvPolynomial.coeff_zero _
  map_add' := by
    intro q r
    obtain ⟨P, rfl⟩ := Ideal.Quotient.mk_surjective q
    obtain ⟨Q, rfl⟩ := Ideal.Quotient.mk_surjective r
    change siteCoefficient ι (project P + project Q) =
      siteCoefficient ι (project P) + siteCoefficient ι (project Q)
    calc
      siteCoefficient ι (project P + project Q) = siteCoefficient ι (project (P + Q)) :=
        congrArg (siteCoefficient ι) (map_add project P Q).symm
      _ = _ := by rw [siteCoefficient_project, MvPolynomial.coeff_add,
        siteCoefficient_project, siteCoefficient_project]

@[simp]
theorem siteCoefficient_project_mul_C (ι : V N → Fin D)
    (a : R) (q : SiteRing N D R) :
    siteCoefficient ι (project (MvPolynomial.C a) * q) = a * siteCoefficient ι q := by
  obtain ⟨P, rfl⟩ := Ideal.Quotient.mk_surjective q
  change siteCoefficient ι (project (MvPolynomial.C a) * project P) =
    a * siteCoefficient ι (project P)
  calc
    siteCoefficient ι (project (MvPolynomial.C a) * project P) =
        siteCoefficient ι (project (MvPolynomial.C a * P)) :=
      congrArg (siteCoefficient ι) (map_mul project (MvPolynomial.C a) P).symm
    _ = _ := by rw [siteCoefficient_project, MvPolynomial.coeff_C_mul,
      siteCoefficient_project]

end QuotientCoefficients

section DividedPhysicalCoefficients

variable [Field R] [CharZero R]

omit [CharZero R] in
/-- The edge quadratic is homogeneous of ordinary degree two. -/
theorem sourceQuadratic_totalHomogeneous (W : WeightsN N D R) :
    MvPolynomial.IsWeightedHomogeneous (fun _ : SiteVariable N D => (1 : ℕ))
      (sourceQuadratic W) 2 := by
  classical
  unfold sourceQuadratic symmetricQuadratic
  apply MvPolynomial.IsWeightedHomogeneous.C_mul
  apply MvPolynomial.IsWeightedHomogeneous.sum
  intro z _
  apply MvPolynomial.IsWeightedHomogeneous.sum
  intro t _
  simpa using
    ((MvPolynomial.isWeightedHomogeneous_C (fun _ : SiteVariable N D => (1 : ℕ))
      (edgeMatrix W z t)).mul
      (MvPolynomial.isWeightedHomogeneous_X R (fun _ : SiteVariable N D => (1 : ℕ)) z)).mul
      (MvPolynomial.isWeightedHomogeneous_X R (fun _ : SiteVariable N D => (1 : ℕ)) t)

omit [CharZero R] in
/-- The actual full matching tensor is homogeneous of full ordinary site degree. -/
theorem matchingPolynomialN_totalHomogeneous (W : WeightsN N D R) :
    MvPolynomial.IsWeightedHomogeneous (fun _ : SiteVariable N D => (1 : ℕ))
      (matchingPolynomialN W) N := by
  intro m hm
  rw [weight_one_eq_exponentDegree]
  unfold exponentDegree siteDegree
  have hs := matchingPolynomialN_siteHomogeneous W hm
  have hv (v : V N) : (∑ i : Fin D, m (v, i)) = 1 := by
    rw [← siteWeight_apply, hs, siteProfile_nodup _ (vertices_nodup N)]
    simp
  simp_rw [hv]
  simp

/-- The whole quadratic top power, not merely one coefficient, is factorial times
the full matching tensor in the physical-site algebra. -/
theorem project_sourceQuadratic_pow_full (k : ℕ) (W : WeightsN (2 * k) D R) :
    project (sourceQuadratic W ^ k) =
      project (MvPolynomial.C (k.factorial : R) * matchingPolynomialN W) := by
  apply project_eq_of_full_coefficients
  · simpa [nsmul_eq_mul, Nat.mul_comm] using (sourceQuadratic_totalHomogeneous W).pow k
  · exact (matchingPolynomialN_totalHomogeneous W).C_mul _
  · intro ι
    rw [coeff_sourceQuadratic_pow_full, MvPolynomial.coeff_C_mul,
      coeff_matchingPolynomialN]

/-- The physical divided top power is exactly the full matching tensor. -/
theorem project_dividedSourcePower_full (k : ℕ) (W : WeightsN (2 * k) D R) :
    project (dividedSourcePower W k) = project (matchingPolynomialN W) := by
  apply project_eq_of_full_coefficients
  · unfold dividedSourcePower
    simpa [nsmul_eq_mul, Nat.mul_comm] using
      ((sourceQuadratic_totalHomogeneous W).pow k).C_mul ((k.factorial : R)⁻¹)
  · exact matchingPolynomialN_totalHomogeneous W
  · intro ι
    rw [coeff_dividedSourcePower_full, coeff_matchingPolynomialN]

/-- The divided top power in the same-site-zero algebra has precisely the graph's
recursive matching amplitudes; this uses the proved ordinary-power coefficient identity. -/
theorem siteCoefficient_dividedSourcePower (k : ℕ)
    (W : WeightsN (2 * k) D R) (ι : V (2 * k) → Fin D) :
    siteCoefficient ι (project (dividedSourcePower W k)) = pmSumN (2 * k) D W ι := by
  rw [siteCoefficient_project, coeff_dividedSourcePower_full]

end DividedPhysicalCoefficients

end KrennAllOrders.SiteAlgebra
