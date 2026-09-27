/-
Copyright (c) 2026 Rishi. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/

import WickCovariance
import SiteAlgebra
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Logic.Equiv.Fin.Basic
import Mathlib.Algebra.MvPolynomial.Equiv
import Mathlib.RingTheory.MvPolynomial.Homogeneous
import Mathlib.Tactic.LinearCombination

/-! # Actual squarefree coefficients of finite Wick pairing sums -/

namespace KrennAllOrders.WickCoefficientBridge

open scoped BigOperators Classical
open WickCovariance

variable {R ι : Type*} [CommRing R] [Fintype ι] [DecidableEq ι]

/-- One occurrence of every labelled variable. -/
noncomputable def topExponent (ι : Type*) [Fintype ι] : ι →₀ ℕ :=
  ∑ i, Finsupp.single i 1

@[simp]
theorem topExponent_apply (i : ι) : topExponent ι i = 1 := by
  simp [topExponent, Finsupp.single_apply]

@[simp]
theorem topExponent_degree : (topExponent ι).degree = Fintype.card ι := by
  simp [Finsupp.degree_eq_sum]

/-- The exponent recorded by a list of choices, one choice for each input label. -/
noncomputable def choiceExponent (f : ι → ι) : ι →₀ ℕ :=
  ∑ i, Finsupp.single (f i) 1

theorem choiceExponent_eq_top_iff (f : ι → ι) :
    choiceExponent f = topExponent ι ↔ Function.Bijective f := by
  constructor
  · intro h
    apply Function.Surjective.bijective_of_finite
    intro j
    by_contra hj
    have hn : ∀ i, f i ≠ j := by simpa only [not_exists] using hj
    have hc := congrArg (fun d : ι →₀ ℕ => d j) h
    simp [choiceExponent, hn] at hc
  · intro h
    exact h.sum_comp (fun i => Finsupp.single i 1)

omit [DecidableEq ι] in
/-- A product of labelled variables records precisely its occurrence exponents. -/
theorem prod_X_choice (f : ι → ι) :
    (∏ i, (MvPolynomial.X (f i) : MvPolynomial ι R)) =
      MvPolynomial.monomial (choiceExponent f) 1 := by
  simpa only [choiceExponent, MvPolynomial.X] using
    (MvPolynomial.monomial_sum_one (R := R) Finset.univ
      (fun i => Finsupp.single (f i) 1)).symm

/-- Squarefree top extraction keeps exactly the bijective assignments. -/
theorem coeff_top_prod_X_choice (f : ι → ι) :
    MvPolynomial.coeff (topExponent ι) (∏ i, (MvPolynomial.X (f i) : MvPolynomial ι R)) =
      if Function.Bijective f then 1 else 0 := by
  rw [prod_X_choice]
  simp only [MvPolynomial.coeff_monomial, choiceExponent_eq_top_iff]

/-- A bijective self-map is exactly a permutation; this reindexing keeps all
weights, rather than identifying them only up to support. -/
noncomputable def bijectiveEquivPerm :
    {f : ι → ι // Function.Bijective f} ≃ Equiv.Perm ι where
  toFun f := Equiv.ofBijective f.1 f.2
  invFun σ := ⟨σ, σ.bijective⟩
  left_inv f := by rfl
  right_inv σ := by ext i; rfl

theorem sum_bijective_eq_sum_perm (w : (ι → ι) → R) :
    (∑ f : ι → ι, if Function.Bijective f then w f else 0) =
      ∑ σ : Equiv.Perm ι, w σ := by
  classical
  rw [← Finset.sum_filter]
  rw [Finset.sum_subtype (p := Function.Bijective) _
    (fun _ => by simp only [Finset.mem_filter, Finset.mem_univ, true_and])]
  exact Fintype.sum_equiv bijectiveEquivPerm _ _ (fun _ => rfl)

/-- Exact extraction for an arbitrary weighted assignment sum. This is the finite
coefficient identity underlying the Wick pairing normalization. -/
theorem coeff_top_weighted_choices (w : (ι → ι) → R) :
    MvPolynomial.coeff (topExponent ι)
      (∑ f : ι → ι, MvPolynomial.C (w f) * ∏ i, MvPolynomial.X (f i)) =
      ∑ σ : Equiv.Perm ι, w σ := by
  simp only [MvPolynomial.coeff_sum, MvPolynomial.coeff_C_mul, coeff_top_prod_X_choice]
  simp only [mul_ite, mul_one, mul_zero]
  exact sum_bijective_eq_sum_perm w

/-- The oriented quadratic sum, before division by two. Same-label entries are
retained; squarefree coefficient extraction itself discards their repeats. -/
noncomputable def rawQuadratic (S : ι → ι → R) : MvPolynomial ι R :=
  ∑ i, ∑ j, MvPolynomial.C (S i j) * MvPolynomial.X i * MvPolynomial.X j

omit [DecidableEq ι] in
theorem rawQuadratic_eq_pairAssignments (S : ι → ι → R) :
    rawQuadratic S = ∑ f : Fin 2 → ι,
      MvPolynomial.C (S (f 0) (f 1)) * ∏ j : Fin 2, MvPolynomial.X (f j) := by
  unfold rawQuadratic
  calc
    _ = ∑ p : ι × ι, MvPolynomial.C (S p.1 p.2) *
        MvPolynomial.X p.1 * MvPolynomial.X p.2 := (Fintype.sum_prod_type _).symm
    _ = _ := by
      symm
      apply Fintype.sum_equiv (finTwoArrowEquiv ι)
      intro f
      simp [Fin.prod_univ_two, mul_assoc]

omit [DecidableEq ι] in
/-- Every term in the literal covariance quadratic has degree two. -/
theorem rawQuadratic_isHomogeneous (S : ι → ι → R) :
    (rawQuadratic S).IsHomogeneous 2 := by
  apply MvPolynomial.IsHomogeneous.sum
  intro i _
  apply MvPolynomial.IsHomogeneous.sum
  intro j _
  exact (MvPolynomial.isHomogeneous_C_mul_X (S i j) i).mul
    (MvPolynomial.isHomogeneous_X _ j)

omit [DecidableEq ι] in
/-- Expanding the actual quadratic power produces every labelled assignment,
with the literal product of its covariance entries. -/
theorem rawQuadratic_pow_assignments (S : ι → ι → R) (m : ℕ) :
    rawQuadratic S ^ m = ∑ f : Slots m → ι,
      MvPolynomial.C (∏ i : Fin m, S (f ⟨i, 0⟩) (f ⟨i, 1⟩)) *
        ∏ j : Slots m, MvPolynomial.X (f j) := by
  calc
    rawQuadratic S ^ m = ∏ _i : Fin m, rawQuadratic S := by simp
    _ = ∏ _i : Fin m, ∑ f : Fin 2 → ι,
        MvPolynomial.C (S (f 0) (f 1)) * ∏ j : Fin 2, MvPolynomial.X (f j) := by
      rw [rawQuadratic_eq_pairAssignments]
    _ = ∑ f : Fin m → Fin 2 → ι, ∏ i : Fin m,
        (MvPolynomial.C (S (f i 0) (f i 1)) * ∏ j : Fin 2, MvPolynomial.X (f i j)) :=
      Fintype.prod_sum _
    _ = _ := by
      apply Fintype.sum_equiv (Equiv.piCurry (fun (_i : Fin m) (_j : Fin 2) => ι)).symm
      intro f
      simp only [Equiv.piCurry_symm_apply, Finset.prod_mul_distrib, ← map_prod,
        Fintype.prod_sigma, Sigma.uncurry]

/-- The all-distinct coefficient of the actual quadratic power is the full
permutation pairing sum, before its `2^m m!` normalization. -/
theorem coeff_top_rawQuadratic_pow (m : ℕ) (S : Slots m → Slots m → R) :
    MvPolynomial.coeff (topExponent (Slots m)) (rawQuadratic S ^ m) =
      ∑ σ : Equiv.Perm (Slots m), ∏ i : Fin m, S (σ ⟨i, 0⟩) (σ ⟨i, 1⟩) := by
  rw [rawQuadratic_pow_assignments]
  exact coeff_top_weighted_choices (R := R) (ι := Slots m)
    (fun f => ∏ i : Fin m, S (f ⟨i, 0⟩) (f ⟨i, 1⟩))

section SplitCoefficients

variable {κ : Type*}

omit [Fintype ι] [DecidableEq ι] in
/-- Currying disjoint polynomial alphabets preserves the literal two coefficient
extractions. -/
theorem coeff_sumRingEquiv (P : MvPolynomial (ι ⊕ κ) R)
    (d : ι →₀ ℕ) (e : κ →₀ ℕ) :
    MvPolynomial.coeff e (MvPolynomial.coeff d (MvPolynomial.sumRingEquiv R ι κ P)) =
      MvPolynomial.coeff (Finsupp.sumElim d e) P := by
  simp [MvPolynomial.sumRingEquiv, MvPolynomial.coeff,
    AddMonoidAlgebra.curryRingEquiv, AddMonoidAlgebra.curryAddEquiv]

omit [Fintype ι] [DecidableEq ι] in
theorem sumRingEquiv_rename_left (P : MvPolynomial ι R) :
    MvPolynomial.sumRingEquiv R ι κ (MvPolynomial.rename Sum.inl P) =
      MvPolynomial.map MvPolynomial.C P := by
  induction P using MvPolynomial.induction_on with
  | C r => simp
  | add P Q hP hQ => simp [map_add, hP, hQ]
  | mul_X P i hP => simp [map_mul, hP]

omit [Fintype ι] [DecidableEq ι] in
theorem sumRingEquiv_rename_right (P : MvPolynomial κ R) :
    MvPolynomial.sumRingEquiv R ι κ (MvPolynomial.rename Sum.inr P) =
      MvPolynomial.C P := by
  induction P using MvPolynomial.induction_on with
  | C r => simp
  | add P Q hP hQ => simp [map_add, hP, hQ]
  | mul_X P i hP => simp [map_mul, hP]

omit [Fintype ι] [DecidableEq ι] in
/-- Coefficients of independent replicas factor exactly for arbitrary
polynomials on their disjoint label sets. -/
theorem coeff_rename_mul_rename (P : MvPolynomial ι R) (Q : MvPolynomial κ R)
    (d : ι →₀ ℕ) (e : κ →₀ ℕ) :
    MvPolynomial.coeff (Finsupp.sumElim d e)
      (MvPolynomial.rename Sum.inl P * MvPolynomial.rename Sum.inr Q) =
        MvPolynomial.coeff d P * MvPolynomial.coeff e Q := by
  rw [← coeff_sumRingEquiv, map_mul, sumRingEquiv_rename_left, sumRingEquiv_rename_right]
  rw [mul_comm (MvPolynomial.map MvPolynomial.C P), MvPolynomial.coeff_C_mul,
    MvPolynomial.coeff_map, mul_comm Q, MvPolynomial.coeff_C_mul]

variable [Fintype κ] [DecidableEq κ]

@[simp]
theorem topExponent_sumElim :
    Finsupp.sumElim (topExponent ι) (topExponent κ) = topExponent (ι ⊕ κ) := by
  ext i
  cases i <;> simp

/-- In particular the full squarefree top coefficient factors across replicas. -/
theorem coeff_top_rename_mul_rename (P : MvPolynomial ι R) (Q : MvPolynomial κ R) :
    MvPolynomial.coeff (topExponent (ι ⊕ κ))
      (MvPolynomial.rename Sum.inl P * MvPolynomial.rename Sum.inr Q) =
        MvPolynomial.coeff (topExponent ι) P * MvPolynomial.coeff (topExponent κ) Q := by
  rw [← topExponent_sumElim, coeff_rename_mul_rename]

/-- Binomial splitting retains the exact power and factorial bookkeeping of the
two independent polynomial alphabets. -/
theorem coeff_top_sum_rename_pow (P : MvPolynomial ι R) (Q : MvPolynomial κ R) (n : ℕ) :
    MvPolynomial.coeff (topExponent (ι ⊕ κ))
      ((MvPolynomial.rename Sum.inl P + MvPolynomial.rename Sum.inr Q) ^ n) =
      ∑ k ∈ Finset.range (n + 1), (n.choose k : R) *
        MvPolynomial.coeff (topExponent ι) (P ^ k) *
        MvPolynomial.coeff (topExponent κ) (Q ^ (n - k)) := by
  rw [add_pow, MvPolynomial.coeff_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [show (↑(n.choose k) : MvPolynomial (ι ⊕ κ) R) =
      MvPolynomial.C (n.choose k : R) by simp]
  rw [mul_comm ((_ ^ k) * (_ ^ (n - k))), MvPolynomial.coeff_C_mul,
    ← map_pow, ← map_pow, coeff_top_rename_mul_rename]
  ring

end SplitCoefficients

/-- Homogeneity discards every quadratic power except the one with the required
number of labelled slots. -/
theorem coeff_top_pow_eq_zero (P : MvPolynomial ι R) (hP : P.IsHomogeneous 2)
    {m k : ℕ} (hcard : Fintype.card ι = 2 * m) (hne : k ≠ m) :
    MvPolynomial.coeff (topExponent ι) (P ^ k) = 0 := by
  apply (hP.pow k).coeff_eq_zero
  rw [topExponent_degree, hcard]
  omega

/-- An odd number of labelled slots cannot be filled by quadratic factors. -/
theorem coeff_top_pow_eq_zero_of_odd (P : MvPolynomial ι R)
    (hP : P.IsHomogeneous 2) (hodd : ¬Even (Fintype.card ι)) (k : ℕ) :
    MvPolynomial.coeff (topExponent ι) (P ^ k) = 0 := by
  apply (hP.pow k).coeff_eq_zero
  rw [topExponent_degree]
  intro h
  apply hodd
  exact ⟨k, by omega⟩

section Relabelling

variable {κ : Type*} [Fintype κ] [DecidableEq κ]

theorem topExponent_mapDomain (e : ι ≃ κ) :
    (topExponent ι).mapDomain e = topExponent κ := by
  ext j
  rw [Finsupp.mapDomain_equiv_apply]
  simp

theorem coeff_top_rename_equiv (e : ι ≃ κ) (P : MvPolynomial ι R) :
    MvPolynomial.coeff (topExponent κ) (MvPolynomial.rename e P) =
      MvPolynomial.coeff (topExponent ι) P := by
  rw [← topExponent_mapDomain e, MvPolynomial.coeff_rename_mapDomain e e.injective]

omit [DecidableEq ι] [DecidableEq κ] in
theorem rawQuadratic_rename_equiv (e : ι ≃ κ) (S : κ → κ → R) :
    MvPolynomial.rename e (rawQuadratic (fun i j => S (e i) (e j))) = rawQuadratic S := by
  simp only [rawQuadratic, map_sum, map_mul, MvPolynomial.rename_C, MvPolynomial.rename_X]
  apply Fintype.sum_equiv e
  intro i
  apply Fintype.sum_equiv e
  intro j
  rfl

/-- The covariance of independent finite variable families has zero off-block
entries, while each within-family covariance is kept literally. -/
def blockCovariance (S : ι → ι → R) (T : κ → κ → R) : (ι ⊕ κ) → (ι ⊕ κ) → R
  | .inl i, .inl j => S i j
  | .inr i, .inr j => T i j
  | _, _ => 0

omit [DecidableEq ι] [DecidableEq κ] in
theorem rawQuadratic_blockCovariance (S : ι → ι → R) (T : κ → κ → R) :
    rawQuadratic (blockCovariance S T) =
      MvPolynomial.rename Sum.inl (rawQuadratic S) +
        MvPolynomial.rename Sum.inr (rawQuadratic T) := by
  simp [rawQuadratic, blockCovariance, Fintype.sum_sum_type, map_sum, map_mul]

end Relabelling

section Field

variable {K E : Type*} [Field K] [AddCommGroup E] [Module K E]

/-- The literal symmetric quadratic on the finite label set. -/
noncomputable def symmetricQuadratic (S : ι → ι → K) : MvPolynomial ι K :=
  MvPolynomial.C ((2 : K)⁻¹) * rawQuadratic S

/-- Exact divided power of the labelled symmetric quadratic. -/
noncomputable def dividedQuadratic (S : ι → ι → K) (m : ℕ) : MvPolynomial ι K :=
  MvPolynomial.C ((m.factorial : K)⁻¹) * symmetricQuadratic S ^ m

omit [DecidableEq ι] in
theorem symmetricQuadratic_isHomogeneous (S : ι → ι → K) :
    (symmetricQuadratic S).IsHomogeneous 2 :=
  (rawQuadratic_isHomogeneous S).C_mul _

omit [DecidableEq ι] in
theorem dividedQuadratic_rename_equiv {κ : Type*} [Fintype κ] [DecidableEq κ]
    (e : ι ≃ κ) (S : κ → κ → K) (m : ℕ) :
    MvPolynomial.rename e (dividedQuadratic (fun i j => S (e i) (e j)) m) =
      dividedQuadratic S m := by
  simp only [dividedQuadratic, symmetricQuadratic, map_mul, map_pow,
    MvPolynomial.rename_C, rawQuadratic_rename_equiv]

/-- The coefficient bridge has the same normalization as the finite Wick sum. -/
theorem coeff_top_dividedQuadratic (m : ℕ) (S : Slots m → Slots m → K) :
    MvPolynomial.coeff (topExponent (Slots m)) (dividedQuadratic S m) =
      ((2 : K) ^ m * (m.factorial : K))⁻¹ *
        ∑ σ : Equiv.Perm (Slots m), ∏ i : Fin m, S (σ ⟨i, 0⟩) (σ ⟨i, 1⟩) := by
  rw [dividedQuadratic, symmetricQuadratic, mul_pow, ← map_pow,
    MvPolynomial.coeff_C_mul, MvPolynomial.coeff_C_mul, coeff_top_rawQuadratic_pow]
  simp only [mul_inv_rev, inv_pow, mul_assoc]

/-- The constructed Wick moment equals the actual squarefree coefficient of the
divided covariance quadratic. This is an equality of coefficient constructions,
not an added covariance axiom. -/
theorem wickMoment_eq_coeff_dividedQuadratic (B : E →ₗ[K] E →ₗ[K] K)
    (m : ℕ) (v : Slots m → E) :
    wickMoment B m v = MvPolynomial.coeff (topExponent (Slots m))
      (dividedQuadratic (fun i j => B (v i) (v j)) m) := by
  rw [wickMoment_apply, coeff_top_dividedQuadratic]

/-- The same bridge on an arbitrary even finite label set. No preferred
enumeration or coordinate order remains in the coefficient expression. -/
theorem centeredMoment_eq_coeff_dividedQuadratic (B : E →ₗ[K] E →ₗ[K] K)
    (h : Even (Fintype.card ι)) (v : ι → E) :
    centeredMoment B v = MvPolynomial.coeff (topExponent ι)
      (dividedQuadratic (fun i j => B (v i) (v j)) (Fintype.card ι / 2)) := by
  rw [centeredMoment_of_even B h, wickMoment_eq_coeff_dividedQuadratic]
  rw [← coeff_top_rename_equiv (evenSlotsEquiv h)]
  exact congrArg (MvPolynomial.coeff (topExponent ι))
    (dividedQuadratic_rename_equiv (evenSlotsEquiv h)
      (fun i j => B (v i) (v j)) (Fintype.card ι / 2))

variable [CharZero K]

/-- Independent replicas factor at the actual divided quadratic top coefficient.
The proof keeps the entire binomial expansion and discards other powers only by
the homogeneous degree at each separate replica. -/
theorem coeff_top_divided_sum_factorization {κ : Type*} [Fintype κ] [DecidableEq κ]
    (P : MvPolynomial ι K) (Q : MvPolynomial κ K)
    (hP : P.IsHomogeneous 2) (_hQ : Q.IsHomogeneous 2) (m n : ℕ)
    (hm : Fintype.card ι = 2 * m) (_hn : Fintype.card κ = 2 * n) :
    MvPolynomial.coeff (topExponent (ι ⊕ κ))
      (MvPolynomial.C (((m + n).factorial : K)⁻¹) *
        (MvPolynomial.rename Sum.inl P + MvPolynomial.rename Sum.inr Q) ^ (m + n)) =
      MvPolynomial.coeff (topExponent ι) (MvPolynomial.C ((m.factorial : K)⁻¹) * P ^ m) *
        MvPolynomial.coeff (topExponent κ) (MvPolynomial.C ((n.factorial : K)⁻¹) * Q ^ n) := by
  rw [MvPolynomial.coeff_C_mul, coeff_top_sum_rename_pow]
  have hsum : (∑ k ∈ Finset.range (m + n + 1), ((m + n).choose k : K) *
      MvPolynomial.coeff (topExponent ι) (P ^ k) *
      MvPolynomial.coeff (topExponent κ) (Q ^ (m + n - k))) =
      ((m + n).choose m : K) * MvPolynomial.coeff (topExponent ι) (P ^ m) *
        MvPolynomial.coeff (topExponent κ) (Q ^ n) := by
    rw [Finset.sum_eq_single m]
    · simp only [Nat.add_sub_cancel_left]
    · intro k _ hkm
      rw [coeff_top_pow_eq_zero P hP hm hkm, mul_zero, zero_mul]
    · intro h
      exact False.elim (h (Finset.mem_range.mpr (by omega)))
  rw [hsum, MvPolynomial.coeff_C_mul, MvPolynomial.coeff_C_mul]
  have hfac : ((m + n).choose m : K) * (m.factorial : K) * (n.factorial : K) =
      ((m + n).factorial : K) := by
    exact_mod_cast (by simpa only [Nat.add_sub_cancel_left] using
      (Nat.choose_mul_factorial_mul_factorial (show m ≤ m + n by omega)))
  have hm0 : (m.factorial : K) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero m)
  have hn0 : (n.factorial : K) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero n)
  have hmn0 : ((m + n).factorial : K) ≠ 0 :=
    Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero (m + n))
  field_simp
  linear_combination (MvPolynomial.coeff (topExponent ι) (P ^ m) *
    MvPolynomial.coeff (topExponent κ) (Q ^ n)) * hfac

omit [CharZero K] [DecidableEq ι] in
theorem symmetricQuadratic_blockCovariance {κ : Type*} [Fintype κ] [DecidableEq κ]
    (S : ι → ι → K) (T : κ → κ → K) :
    symmetricQuadratic (blockCovariance S T) =
      MvPolynomial.rename Sum.inl (symmetricQuadratic S) +
        MvPolynomial.rename Sum.inr (symmetricQuadratic T) := by
  simp only [symmetricQuadratic, rawQuadratic_blockCovariance, map_mul,
    MvPolynomial.rename_C, mul_add]

/-- Exact factorization for the divided covariance quadratic of two independent
even replicas, with the ordinary binomial multiplicity fully canceled. -/
theorem coeff_top_divided_blockCovariance {κ : Type*} [Fintype κ] [DecidableEq κ]
    (S : ι → ι → K) (T : κ → κ → K) (m n : ℕ)
    (hm : Fintype.card ι = 2 * m) (hn : Fintype.card κ = 2 * n) :
    MvPolynomial.coeff (topExponent (ι ⊕ κ)) (dividedQuadratic (blockCovariance S T) (m + n)) =
      MvPolynomial.coeff (topExponent ι) (dividedQuadratic S m) *
        MvPolynomial.coeff (topExponent κ) (dividedQuadratic T n) := by
  simp only [dividedQuadratic, symmetricQuadratic_blockCovariance]
  exact coeff_top_divided_sum_factorization _ _ (symmetricQuadratic_isHomogeneous S)
    (symmetricQuadratic_isHomogeneous T) m n hm hn

omit [CharZero K] in
/-- In the odd case the independent covariance has zero squarefree coefficient,
including when the total number of slots across both replicas is even. -/
theorem coeff_top_divided_blockCovariance_of_odd {κ : Type*}
    [Fintype κ] [DecidableEq κ] (S : ι → ι → K) (T : κ → κ → K)
    (hodd : ¬Even (Fintype.card ι)) (m : ℕ) :
    MvPolynomial.coeff (topExponent (ι ⊕ κ))
      (dividedQuadratic (blockCovariance S T) m) = 0 := by
  rw [dividedQuadratic, symmetricQuadratic_blockCovariance,
    MvPolynomial.coeff_C_mul, coeff_top_sum_rename_pow]
  simp only [coeff_top_pow_eq_zero_of_odd _ (symmetricQuadratic_isHomogeneous S) hodd,
    mul_zero, zero_mul, Finset.sum_const_zero]

omit [CharZero K] in
/-- Relabelling the actual centered moment by an arbitrary equivalence does not
change it; this follows from the literal coefficient bridge. -/
theorem centeredMoment_relabel {κ : Type*} [Fintype κ] [DecidableEq κ]
    (B : E →ₗ[K] E →ₗ[K] K) (e : ι ≃ κ) (v : κ → E) :
    centeredMoment B (fun i => v (e i)) = centeredMoment B v := by
  have hc := Fintype.card_congr e
  by_cases h : Even (Fintype.card ι)
  · have hk : Even (Fintype.card κ) := hc ▸ h
    rw [centeredMoment_eq_coeff_dividedQuadratic B h,
      centeredMoment_eq_coeff_dividedQuadratic B hk]
    rw [← coeff_top_rename_equiv e]
    rw [dividedQuadratic_rename_equiv e (fun i j => B (v i) (v j)), hc]
  · have hk : ¬Even (Fintype.card κ) := by simpa only [hc] using h
    simp only [centeredMoment_of_not_even _ h, centeredMoment_of_not_even _ hk]

/-- Independent replicas factor as actual finite Wick moments, for arbitrary
finite arities. In particular the odd/odd case is zero for a proved coefficient
reason, not an assumed independence axiom. -/
theorem centeredMoment_independent_replicas {κ : Type*} [Fintype κ] [DecidableEq κ]
    (B : E →ₗ[K] E →ₗ[K] K) (v : ι → E) (w : κ → E) :
    centeredMoment (replicaCovariance B)
      (Sum.elim (fun i => (v i, (0 : E))) (fun j => ((0 : E), w j))) =
      centeredMoment B v * centeredMoment B w := by
  have hcov : (fun i j => replicaCovariance B
      (Sum.elim (fun i => (v i, (0 : E))) (fun j => ((0 : E), w j)) i)
      (Sum.elim (fun i => (v i, (0 : E))) (fun j => ((0 : E), w j)) j)) =
      blockCovariance (fun i j => B (v i) (v j)) (fun i j => B (w i) (w j)) := by
    funext i j
    cases i <;> cases j <;> simp [blockCovariance]
  by_cases hi : Even (Fintype.card ι)
  · by_cases hk : Even (Fintype.card κ)
    · have hi' : Fintype.card ι = 2 * (Fintype.card ι / 2) := by
        obtain ⟨m, hm⟩ := hi
        omega
      have hk' : Fintype.card κ = 2 * (Fintype.card κ / 2) := by
        obtain ⟨m, hm⟩ := hk
        omega
      have hsum : Even (Fintype.card (ι ⊕ κ)) := by
        rw [Fintype.card_sum]
        exact hi.add hk
      have hhalf : Fintype.card (ι ⊕ κ) / 2 =
          Fintype.card ι / 2 + Fintype.card κ / 2 := by
        rw [Fintype.card_sum]
        omega
      rw [centeredMoment_eq_coeff_dividedQuadratic _ hsum, hcov, hhalf,
        coeff_top_divided_blockCovariance _ _ _ _ hi' hk',
        centeredMoment_eq_coeff_dividedQuadratic B hi,
        centeredMoment_eq_coeff_dividedQuadratic B hk]
    · have hs : ¬Even (Fintype.card (ι ⊕ κ)) := by
        simp only [Fintype.card_sum]
        intro h
        exact hk ((Nat.even_add.mp h).mp hi)
      simp only [centeredMoment_of_not_even _ hs,
        centeredMoment_of_not_even _ hk, mul_zero]
  · by_cases hs : Even (Fintype.card (ι ⊕ κ))
    · rw [centeredMoment_eq_coeff_dividedQuadratic _ hs, hcov,
        coeff_top_divided_blockCovariance_of_odd _ _ hi,
        centeredMoment_of_not_even _ hi, zero_mul]
    · simp only [centeredMoment_of_not_even _ hs,
        centeredMoment_of_not_even _ hi, zero_mul]

end Field

end KrennAllOrders.WickCoefficientBridge
