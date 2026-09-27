import WickCoefficientBridge
import Mathlib.Algebra.MvPolynomial.Coeff

/-!
# Repeated isotropic root slots give the literal source response

The coefficient expansion retains every auxiliary root slot. Pairings between
two auxiliary slots have zero covariance; the remaining pairings give exactly
the raw row power, with no factorial left on that row power.
-/

namespace KrennAllOrders.WickRootBridge

open scoped BigOperators Classical
open WickCovariance WickCoefficientBridge

variable {R ι : Type*} [CommRing R] [Fintype ι] [DecidableEq ι]

/-- The literal row linear form on the finite retained label set. -/
noncomputable def linearPolynomial (μ : ι → R) : MvPolynomial ι R :=
  ∑ i, MvPolynomial.C (μ i) * MvPolynomial.X i

omit [DecidableEq ι] in
theorem linearPolynomial_isHomogeneous (μ : ι → R) :
    (linearPolynomial μ).IsHomogeneous 1 := by
  apply MvPolynomial.IsHomogeneous.sum
  intro i _
  exact MvPolynomial.isHomogeneous_C_mul_X _ _

theorem topExponent_multinomial : (topExponent ι).multinomial = (Fintype.card ι).factorial := by
  rw [Finsupp.multinomial_eq_of_support_subset (Finset.subset_univ _)]
  simp [Nat.multinomial]

/-- Each order of the distinct auxiliary labels contributes once. -/
theorem coeff_top_sum_X_pow (k : ℕ) :
    MvPolynomial.coeff (topExponent ι) ((∑ i : ι, MvPolynomial.X i : MvPolynomial ι R) ^ k) =
      if Fintype.card ι = k then ((Fintype.card ι).factorial : R) else 0 := by
  rw [MvPolynomial.coeff_sum_X_pow_of_fintype, topExponent_multinomial]
  have hd : (topExponent ι).sum (fun _ m => m) = Fintype.card ι :=
    topExponent_degree (ι := ι)
  rw [hd]
  split_ifs <;> simp

/-- Covariance with any number of copies of one isotropic auxiliary root. -/
def auxiliaryCovariance {κ : Type*} (S : ι → ι → R) (μ : ι → R) :
    (ι ⊕ κ) → (ι ⊕ κ) → R
  | .inl i, .inl j => S i j
  | .inl i, .inr _ => μ i
  | .inr _, .inl j => μ j
  | .inr _, .inr _ => 0

omit [DecidableEq ι] in
theorem rawQuadratic_auxiliaryCovariance {κ : Type*} [Fintype κ]
    (S : ι → ι → R) (μ : ι → R) :
    rawQuadratic (auxiliaryCovariance (κ := κ) S μ) =
      MvPolynomial.rename Sum.inl (rawQuadratic S) +
        2 * (MvPolynomial.rename Sum.inl (linearPolynomial μ) *
          MvPolynomial.rename Sum.inr (∑ i : κ, MvPolynomial.X i)) := by
  have hmul : MvPolynomial.rename Sum.inl (linearPolynomial μ) *
      MvPolynomial.rename Sum.inr (∑ i : κ, MvPolynomial.X i) =
      ∑ i : ι, ∑ j : κ,
        MvPolynomial.C (μ i) * MvPolynomial.X (Sum.inl i) * MvPolynomial.X (Sum.inr j) := by
    simp only [linearPolynomial, map_sum, map_mul, MvPolynomial.rename_C,
      MvPolynomial.rename_X, Finset.sum_mul, Finset.mul_sum]
    exact Finset.sum_comm
  rw [hmul]
  simp only [rawQuadratic, auxiliaryCovariance, Fintype.sum_sum_type,
    MvPolynomial.C_0, zero_mul, Finset.sum_const_zero, add_zero,
    map_sum, map_mul, MvPolynomial.rename_C, MvPolynomial.rename_X,
    Finset.sum_add_distrib]
  rw [Finset.sum_comm (f := fun j : κ => fun i : ι =>
    MvPolynomial.C (μ i) * MvPolynomial.X (Sum.inr j) * MvPolynomial.X (Sum.inl i))]
  have hcross : (∑ i : ι, ∑ j : κ,
      MvPolynomial.C (μ i) * MvPolynomial.X (Sum.inr j) * MvPolynomial.X (Sum.inl i)) =
      ∑ i : ι, ∑ j : κ,
      MvPolynomial.C (μ i) * MvPolynomial.X (Sum.inl i) * MvPolynomial.X (Sum.inr j) := by
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro j _
    ring
  rw [hcross]
  ring

section Field

variable {K : Type*} [Field K] [CharZero K]

omit [DecidableEq ι] in
/-- The two cross orientations cancel the symmetric quadratic's factor one half. -/
theorem symmetricQuadratic_auxiliaryCovariance {κ : Type*} [Fintype κ]
    (S : ι → ι → K) (μ : ι → K) :
    symmetricQuadratic (auxiliaryCovariance (κ := κ) S μ) =
      MvPolynomial.rename Sum.inl (symmetricQuadratic S) +
        MvPolynomial.rename Sum.inl (linearPolynomial μ) *
          MvPolynomial.rename Sum.inr (∑ i : κ, MvPolynomial.X i) := by
  rw [symmetricQuadratic, rawQuadratic_auxiliaryCovariance]
  simp only [symmetricQuadratic, map_mul, MvPolynomial.rename_C, mul_add]
  have htwo : (MvPolynomial.C ((2 : K)⁻¹) : MvPolynomial (ι ⊕ κ) K) * 2 = 1 := by
    rw [show (2 : MvPolynomial (ι ⊕ κ) K) = MvPolynomial.C (2 : K) from
        (map_ofNat MvPolynomial.C 2).symm,
      ← map_mul, inv_mul_cancel₀ (by norm_num : (2 : K) ≠ 0), map_one]
  linear_combination (MvPolynomial.rename Sum.inl (linearPolynomial μ) *
    MvPolynomial.rename Sum.inr (∑ i : κ, MvPolynomial.X i)) * htwo

/-- Adding distinct isotropic root labels extracts a raw row power. The binomial
coefficient and auxiliary-slot factorial cancel against the total divided power. -/
theorem coeff_top_auxiliary_root {κ : Type*} [Fintype κ] [DecidableEq κ]
    (Q L : MvPolynomial ι K) (k d : ℕ) (hd : Fintype.card κ = d) :
    MvPolynomial.coeff (topExponent (ι ⊕ κ))
      (MvPolynomial.C (((k + d).factorial : K)⁻¹) *
        (MvPolynomial.rename Sum.inl Q +
          MvPolynomial.rename Sum.inl L *
            MvPolynomial.rename Sum.inr (∑ i : κ, MvPolynomial.X i)) ^ (k + d)) =
      MvPolynomial.coeff (topExponent ι)
        (MvPolynomial.C ((k.factorial : K)⁻¹) * L ^ d * Q ^ k) := by
  rw [MvPolynomial.coeff_C_mul, add_comm (MvPolynomial.rename Sum.inl Q), add_pow,
    MvPolynomial.coeff_sum]
  have hterm : ∀ j : ℕ,
      MvPolynomial.coeff (topExponent (ι ⊕ κ))
        (((MvPolynomial.rename Sum.inl L *
            MvPolynomial.rename Sum.inr (∑ i : κ, MvPolynomial.X i)) ^ j *
          (MvPolynomial.rename Sum.inl Q) ^ (k + d - j)) *
          ((k + d).choose j : MvPolynomial (ι ⊕ κ) K)) =
        ((k + d).choose j : K) *
          MvPolynomial.coeff (topExponent ι) (L ^ j * Q ^ (k + d - j)) *
            (if d = j then (d.factorial : K) else 0) := by
    intro j
    rw [show ((k + d).choose j : MvPolynomial (ι ⊕ κ) K) =
        MvPolynomial.C ((k + d).choose j : K) by simp]
    rw [mul_comm (_ * _), MvPolynomial.coeff_C_mul]
    have hpoly : ((MvPolynomial.rename Sum.inl L *
        MvPolynomial.rename Sum.inr (∑ i : κ, MvPolynomial.X i)) ^ j *
        (MvPolynomial.rename Sum.inl Q) ^ (k + d - j)) =
        MvPolynomial.rename Sum.inl (L ^ j * Q ^ (k + d - j)) *
          MvPolynomial.rename Sum.inr ((∑ i : κ, MvPolynomial.X i) ^ j) := by
      simp only [mul_pow, map_mul, map_pow]
      ring
    rw [hpoly, coeff_top_rename_mul_rename, coeff_top_sum_X_pow, hd]
    ring
  simp_rw [hterm]
  rw [Finset.sum_eq_single d]
  · simp only [Nat.add_sub_cancel_right, eq_self, ↓reduceIte]
    rw [mul_assoc (MvPolynomial.C _) (L ^ d), MvPolynomial.coeff_C_mul]
    have hfac : ((k + d).choose d : K) * (d.factorial : K) * (k.factorial : K) =
        ((k + d).factorial : K) := by
      exact_mod_cast (by simpa only [Nat.add_sub_cancel_right] using
        (Nat.choose_mul_factorial_mul_factorial (show d ≤ k + d by omega)))
    have hk0 : (k.factorial : K) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero k)
    have hkd0 : ((k + d).factorial : K) ≠ 0 :=
      Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero (k + d))
    field_simp
    linear_combination MvPolynomial.coeff (topExponent ι) (L ^ d * Q ^ k) * hfac
  · intro j _ hj
    rw [if_neg (Ne.symm hj), mul_zero]
  · intro h
    exact False.elim (h (Finset.mem_range.mpr (by omega)))

/-- Literal Wick-to-response bridge with repeated isotropic root slots. The
retained family has `2*k+d` slots and the auxiliary family has `d` slots. Its
moment is precisely the raw root-row power times the divided retained quadratic.
The statement also covers the terminal case `k=0`. -/
theorem centeredMoment_isotropic_roots {κ E : Type*}
    [Fintype κ] [DecidableEq κ] [AddCommGroup E] [Module K E]
    (B : E →ₗ[K] E →ₗ[K] K) (v : ι → E) (g : E)
    (k d : ℕ) (hi : Fintype.card ι = 2 * k + d) (hd : Fintype.card κ = d)
    (hgg : B g g = 0) (hcross : ∀ i, B (v i) g = B g (v i)) :
    centeredMoment B (Sum.elim v (fun _ : κ => g)) =
      MvPolynomial.coeff (topExponent ι)
        (MvPolynomial.C ((k.factorial : K)⁻¹) *
          linearPolynomial (fun i => B g (v i)) ^ d *
            symmetricQuadratic (fun i j => B (v i) (v j)) ^ k) := by
  have heven : Even (Fintype.card (ι ⊕ κ)) := by
    refine ⟨k + d, ?_⟩
    simp only [Fintype.card_sum, hi, hd]
    omega
  have hhalf : Fintype.card (ι ⊕ κ) / 2 = k + d := by
    simp only [Fintype.card_sum, hi, hd]
    omega
  have hcov : (fun i j => B (Sum.elim v (fun _ : κ => g) i)
      (Sum.elim v (fun _ : κ => g) j)) =
      auxiliaryCovariance (fun i j => B (v i) (v j)) (fun i => B g (v i)) := by
    funext i j
    cases i <;> cases j <;> simp [auxiliaryCovariance, hgg, hcross]
  rw [centeredMoment_eq_coeff_dividedQuadratic _ heven, hcov, hhalf,
    dividedQuadratic, symmetricQuadratic_auxiliaryCovariance,
    coeff_top_auxiliary_root _ _ k d hd]

end Field

end KrennAllOrders.WickRootBridge
