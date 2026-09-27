import WickCoefficientBridge
import WickRootBridge
import Mathlib.Algebra.MvPolynomial.Coeff

/-!
# Shifted finite Wick moments and literal source coefficients

The mean expansion is related to the actual squarefree coefficients, including
the inverse factorials. No Gaussian evaluation or reflection identity is assumed.
-/

namespace KrennAllOrders.WickShiftedBridge

open scoped BigOperators Classical
open WickCovariance WickCoefficientBridge WickRootBridge

variable {R ι : Type*} [CommRing R] [Fintype ι] [DecidableEq ι]

/-- The squarefree exponent of one subset of the finite label set. -/
noncomputable def subsetExponent (s : Finset ι) : ι →₀ ℕ :=
  ∑ i ∈ s, Finsupp.single i 1

omit [Fintype ι] in
@[simp]
theorem subsetExponent_apply (s : Finset ι) (i : ι) :
    subsetExponent s i = if i ∈ s then 1 else 0 := by
  simp [subsetExponent, Finsupp.single_apply, Finset.sum_ite_eq']

omit [Fintype ι] in
@[simp]
theorem subsetExponent_support (s : Finset ι) : (subsetExponent s).support = s := by
  ext i
  simp

theorem subsetExponent_sum_compl (s : Finset ι) :
    subsetExponent s + subsetExponent sᶜ = topExponent ι := by
  ext i
  by_cases hi : i ∈ s <;> simp [hi]

omit [Fintype ι] in
theorem subsetExponent_injective : Function.Injective (subsetExponent (ι := ι)) := by
  intro s t h
  simpa using congrArg Finsupp.support h

theorem subsetExponent_degree (s : Finset ι) : (subsetExponent s).degree = s.card := by
  rw [Finsupp.degree_eq_sum]
  simp [Finset.sum_const]

/-- Every split of the full squarefree exponent is uniquely a subset and its
complement. This is the exact convolution indexing for the mean expansion. -/
theorem antidiagonal_top_eq :
    Finset.antidiagonal (topExponent ι) =
      Finset.univ.image (fun s : Finset ι => (subsetExponent s, subsetExponent sᶜ)) := by
  ext ⟨a, b⟩
  simp only [Finset.mem_antidiagonal, Finset.mem_image, Finset.mem_univ, true_and,
    Prod.mk.injEq]
  constructor
  · intro h
    refine ⟨a.support, ?_, ?_⟩
    · ext i
      have hi := congrArg (fun f : ι →₀ ℕ => f i) h
      simp only [Finsupp.add_apply, topExponent_apply] at hi
      by_cases ha : a i = 0
      · simp [ha]
      · simp [ha]
        omega
    · ext i
      have hi := congrArg (fun f : ι →₀ ℕ => f i) h
      simp only [Finsupp.add_apply, topExponent_apply] at hi
      by_cases ha : a i = 0
      · simp [ha]
        omega
      · simp [ha]
        omega
  · rintro ⟨s, rfl, rfl⟩
    exact subsetExponent_sum_compl s

/-- Complete coefficient convolution over all mean subsets. -/
theorem coeff_top_mul (P Q : MvPolynomial ι R) :
    MvPolynomial.coeff (topExponent ι) (P * Q) =
      ∑ s : Finset ι, MvPolynomial.coeff (subsetExponent s) P *
        MvPolynomial.coeff (subsetExponent sᶜ) Q := by
  rw [MvPolynomial.coeff_mul, antidiagonal_top_eq, Finset.sum_image]
  intro s _ t _ h
  exact subsetExponent_injective (congrArg Prod.fst h)

omit [Fintype ι] in
/-- Subset exponents are exactly renamed full exponents on subtype labels. -/
theorem subsetExponent_mapDomain (s : Finset ι) :
    (topExponent {i // i ∈ s}).mapDomain Subtype.val = subsetExponent s := by
  ext i
  by_cases hi : i ∈ s
  · rw [show i = (⟨i, hi⟩ : {i // i ∈ s}).val from rfl,
      Finsupp.mapDomain_apply Subtype.val_injective]
    simp [hi]
  · rw [Finsupp.mapDomain_of_notMem_range]
    · simp [hi]
    · simpa using hi

omit [Fintype ι] in
/-- Restricting variables to a subset preserves precisely its squarefree
coefficient; the discarded variables are set to zero. -/
theorem coeff_subset_eq_restrict (s : Finset ι) (P : MvPolynomial ι R) :
    MvPolynomial.coeff (subsetExponent s) P =
      MvPolynomial.coeff (topExponent {i // i ∈ s})
        (MvPolynomial.killCompl (Subtype.val_injective (p := fun i => i ∈ s)) P) := by
  rw [MvPolynomial.coeff_killCompl, subsetExponent_mapDomain]

omit [Fintype ι] in
theorem subsetExponent_multinomial (s : Finset ι) :
    (subsetExponent s).multinomial = s.card.factorial := by
  rw [Finsupp.multinomial_eq, subsetExponent_support]
  have hp : (∏ i ∈ s, (subsetExponent s i).factorial) = 1 := by
    apply Finset.prod_eq_one
    intro i hi
    simp [hi]
  simp only [Nat.multinomial, hp, Nat.div_one]
  congr 1
  simp

/-- The multinomial coefficient of the row power on a squarefree subset. -/
theorem coeff_subset_linearPolynomial_pow (μ : ι → R) (s : Finset ι) (d : ℕ) :
    MvPolynomial.coeff (subsetExponent s) (linearPolynomial μ ^ d) =
      if s.card = d then (s.card.factorial : R) * ∏ i ∈ s, μ i else 0 := by
  have hlin : linearPolynomial μ = ∑ i : ι, μ i • (MvPolynomial.X i : MvPolynomial ι R) := by
    simp only [linearPolynomial, MvPolynomial.smul_eq_C_mul]
  rw [hlin, MvPolynomial.coeff_linearCombination_X_pow_of_fintype,
    subsetExponent_multinomial]
  have hdeg : (subsetExponent s).sum (fun _ m => m) = s.card := subsetExponent_degree s
  rw [hdeg]
  split_ifs
  · simp [Finsupp.prod]
  · rfl

omit [Fintype ι] [DecidableEq ι] in
theorem restrict_X_of_mem (s : Finset ι) (i : ι) (hi : i ∈ s) :
    MvPolynomial.killCompl (Subtype.val_injective (p := fun i => i ∈ s))
      (MvPolynomial.X i : MvPolynomial ι R) = MvPolynomial.X (⟨i, hi⟩ : {i // i ∈ s}) := by
  have hrename : (MvPolynomial.X i : MvPolynomial ι R) =
      MvPolynomial.rename Subtype.val (MvPolynomial.X (⟨i, hi⟩ : {i // i ∈ s})) := by simp
  rw [hrename, MvPolynomial.killCompl_rename_app]

omit [Fintype ι] [DecidableEq ι] in
theorem restrict_X_of_not_mem (s : Finset ι) (i : ι) (hi : i ∉ s) :
    MvPolynomial.killCompl (Subtype.val_injective (p := fun i => i ∈ s))
      (MvPolynomial.X i : MvPolynomial ι R) = 0 := by
  apply MvPolynomial.killCompl_monomial_eq_zero_of_notMem_range (a := i)
  · simp
  · simpa using hi

theorem sum_restrict_support {A : Type*} [AddCommMonoid A]
    (s : Finset ι) (f : ι → A) (hz : ∀ i, i ∉ s → f i = 0) :
    (∑ i : ι, f i) = ∑ i : {i // i ∈ s}, f i := by
  rw [← Fintype.sum_subtype_add_sum_subtype (fun i => i ∈ s) f]
  rw [show (∑ i : {i // i ∉ s}, f i) = 0 from
    Finset.sum_eq_zero (fun i _ => hz i i.property), add_zero]
  congr!

/-- Retaining a subset of variables retains exactly the induced quadratic. -/
theorem restrict_rawQuadratic (s : Finset ι) (S : ι → ι → R) :
    MvPolynomial.killCompl (Subtype.val_injective (p := fun i => i ∈ s)) (rawQuadratic S) =
      rawQuadratic (fun i j : {i // i ∈ s} => S i j) := by
  simp only [rawQuadratic, map_sum, map_mul, MvPolynomial.killCompl_C]
  rw [sum_restrict_support s _ (by
    intro i hi
    simp only [restrict_X_of_not_mem s i hi, mul_zero, zero_mul, Finset.sum_const_zero])]
  apply Finset.sum_congr rfl
  intro i _
  rw [sum_restrict_support s _ (by
    intro j hj
    simp only [restrict_X_of_not_mem s j hj, mul_zero])]
  apply Finset.sum_congr rfl
  intro j _
  rw [restrict_X_of_mem s i i.property, restrict_X_of_mem s j j.property]

section Field

variable {K E : Type*} [Field K] [CharZero K] [AddCommGroup E] [Module K E]

omit [CharZero K] in
theorem restrict_dividedQuadratic (s : Finset ι) (S : ι → ι → K) (k : ℕ) :
    MvPolynomial.killCompl (Subtype.val_injective (p := fun i => i ∈ s)) (dividedQuadratic S k) =
      dividedQuadratic (fun i j : {i // i ∈ s} => S i j) k := by
  simp only [dividedQuadratic, symmetricQuadratic, map_mul, map_pow,
    MvPolynomial.killCompl_C, restrict_rawQuadratic]

omit [CharZero K] in
/-- A subset coefficient of the literal divided quadratic is its centered Wick
moment when the subset has the required number of slots. -/
theorem coeff_subset_dividedQuadratic (B : E →ₗ[K] E →ₗ[K] K) (v : ι → E)
    (s : Finset ι) (k : ℕ) (hk : s.card = 2 * k) :
    MvPolynomial.coeff (subsetExponent s) (dividedQuadratic (fun i j => B (v i) (v j)) k) =
      centeredMoment B (fun i : {i // i ∈ s} => v i) := by
  have hc : Fintype.card {i // i ∈ s} = 2 * k := by simpa using hk
  have heven : Even (Fintype.card {i // i ∈ s}) := ⟨k, by omega⟩
  rw [coeff_subset_eq_restrict, restrict_dividedQuadratic,
    centeredMoment_eq_coeff_dividedQuadratic _ heven]
  rw [hc, Nat.mul_div_right k (by omega : 0 < 2)]

omit [CharZero K] in
/-- A wrong-size subset coefficient of the divided quadratic is zero. -/
theorem coeff_subset_dividedQuadratic_of_ne (S : ι → ι → K)
    (s : Finset ι) (k : ℕ) (hk : s.card ≠ 2 * k) :
    MvPolynomial.coeff (subsetExponent s) (dividedQuadratic S k) = 0 := by
  apply ((symmetricQuadratic_isHomogeneous S).pow k).C_mul _ |>.coeff_eq_zero
  rw [subsetExponent_degree]
  omega

/-- The part of the actual shifted moment using exactly `d` deterministic means. -/
noncomputable def meanSlice (B : E →ₗ[K] E →ₗ[K] K) (μ : E →ₗ[K] K)
    (d : ℕ) (v : ι → E) : K :=
  ∑ s : Finset ι, if s.card = d then shiftedTerm B μ s v else 0

omit [DecidableEq ι] in
/-- Every fixed mean-degree of the actual shifted Wick construction equals the
corresponding literal divided row/quadratic coefficient. -/
theorem meanSlice_eq_coeff (B : E →ₗ[K] E →ₗ[K] K) (μ : E →ₗ[K] K)
    (v : ι → E) (d k : ℕ) (hcard : Fintype.card ι = d + 2 * k) :
    meanSlice B μ d v =
      MvPolynomial.coeff (topExponent ι)
        (MvPolynomial.C ((d.factorial : K)⁻¹) *
          linearPolynomial (fun i => μ (v i)) ^ d *
            dividedQuadratic (fun i j => B (v i) (v j)) k) := by
  classical
  rw [meanSlice, mul_assoc, MvPolynomial.coeff_C_mul, coeff_top_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro s _
  rw [coeff_subset_linearPolynomial_pow]
  by_cases hs : s.card = d
  · rw [if_pos hs, if_pos hs]
    have hcompl : sᶜ.card = 2 * k := by
      rw [Finset.card_compl, hs, hcard]
      omega
    rw [coeff_subset_dividedQuadratic B v sᶜ k hcompl, shiftedTerm_apply]
    rw [← Finset.prod_subtype (p := fun i => i ∈ s) s (fun _ => Iff.rfl)
      (fun i => μ (v i))]
    simp only [hs]
    have hd0 : (d.factorial : K) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero d)
    field_simp
    congr 1
    exact centeredMoment_relabel B
      (Equiv.subtypeEquivRight (fun i : ι => (Finset.mem_compl (s := s) (a := i)).symm))
      (fun i : {i // i ∈ sᶜ} => v i)
  · rw [if_neg hs, if_neg hs]
    simp

omit [DecidableEq ι] [CharZero K] in
/-- The finite shifted moment is the sum of all its mean-degree slices. -/
theorem shiftedMoment_eq_sum_meanSlice (B : E →ₗ[K] E →ₗ[K] K)
    (μ : E →ₗ[K] K) (v : ι → E) :
    shiftedMoment B μ v = ∑ d ∈ Finset.range (Fintype.card ι + 1), meanSlice B μ d v := by
  simp only [shiftedMoment_apply, meanSlice, shiftedTerm_apply]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro s _
  rw [Finset.sum_eq_single s.card]
  · simp
  · intro d _ hd
    rw [if_neg (Ne.symm hd)]
  · intro h
    exact False.elim (h (Finset.mem_range.mpr (by have := Finset.card_le_univ s; omega)))

omit [CharZero K] [DecidableEq ι] in
/-- Parity is inherited from the actual centered complement, at every mean degree. -/
theorem meanSlice_eq_zero_of_odd (B : E →ₗ[K] E →ₗ[K] K) (μ : E →ₗ[K] K)
    (v : ι → E) (d : ℕ) (hodd : ¬Even (Fintype.card ι - d)) :
    meanSlice B μ d v = 0 := by
  classical
  apply Finset.sum_eq_zero
  intro s _
  split_ifs with hs
  · rw [shiftedTerm_apply]
    have hc : Fintype.card {i // i ∉ s} = Fintype.card ι - d := by
      simpa only [Finset.mem_compl, Fintype.card_coe, Finset.card_compl, hs] using
        (show Fintype.card {i // i ∈ sᶜ} = sᶜ.card from Fintype.card_coe sᶜ)
    rw [centeredMoment_of_not_even B (by simpa only [hc] using hodd), mul_zero]
  · rfl

omit [DecidableEq ι] in
/-- Full finite generating-function bridge, with every original mean degree and
its exact divided normalization retained. The expression is finite, including
the terminal pure-mean term. -/
theorem shiftedMoment_eq_coeff_sum (B : E →ₗ[K] E →ₗ[K] K)
    (μ : E →ₗ[K] K) (v : ι → E) :
    shiftedMoment B μ v =
      ∑ d ∈ Finset.range (Fintype.card ι + 1),
        if Even (Fintype.card ι - d) then
          MvPolynomial.coeff (topExponent ι)
            (MvPolynomial.C ((d.factorial : K)⁻¹) *
              linearPolynomial (fun i => μ (v i)) ^ d *
                dividedQuadratic (fun i j => B (v i) (v j)) ((Fintype.card ι - d) / 2))
        else 0 := by
  rw [shiftedMoment_eq_sum_meanSlice]
  apply Finset.sum_congr rfl
  intro d hd
  by_cases heven : Even (Fintype.card ι - d)
  · rw [if_pos heven]
    apply meanSlice_eq_coeff
    have hdn : d ≤ Fintype.card ι := by simpa using Finset.mem_range.mp hd
    obtain ⟨k, hk⟩ := heven
    omega
  · rw [if_neg heven, meanSlice_eq_zero_of_odd B μ v d heven]

end Field

end KrennAllOrders.WickShiftedBridge
