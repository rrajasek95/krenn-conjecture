/-
Copyright (c) 2026 Rishi. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/

import Mathlib.LinearAlgebra.Multilinear.Basic
import Mathlib.LinearAlgebra.Multilinear.Curry
import Mathlib.LinearAlgebra.BilinearMap
import Mathlib.Data.Fintype.Perm
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Logic.Equiv.Sum
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Ring

/-!
# Finite Wick pairing moments and covariance-preserving substitutions

The moment is constructed explicitly, not postulated: for `2m` labelled slots,
sum the products of `m` covariance pairs over all permutations and divide by
`2^m m!`. Each unoriented pairing is thereby counted once for symmetric
covariance. This file proves genuine multilinearity and linear-substitution
naturality from that construction, then specializes to two-replica rotations.

The later identification with physical-site divided quadratic coefficients is
an additional bridge; it is not an assumption of these theorems.
-/

namespace KrennAllOrders.WickCovariance

open scoped BigOperators Classical

variable {R E F : Type*} [Field R]
  [AddCommGroup E] [Module R E] [AddCommGroup F] [Module R F]

/-- Two labelled slots for each of `m` reference pairs. -/
abbrev Slots (m : ℕ) := (_i : Fin m) × Fin 2

/-- One covariance pair, viewed as a genuine two-variable multilinear map. -/
def covariancePair (B : E →ₗ[R] E →ₗ[R] R) :
    MultilinearMap R (fun _ : Fin 2 => E) R where
  toFun v := B (v 0) (v 1)
  map_update_add' v i x y := by
    fin_cases i <;> simp
  map_update_smul' v i c x := by
    fin_cases i <;> simp

@[simp]
theorem covariancePair_apply (B : E →ₗ[R] E →ₗ[R] R) (v : Fin 2 → E) :
    covariancePair B v = B (v 0) (v 1) := rfl

/-- The product attached to one reference pairing of the labelled slots. -/
def pairingProduct (B : E →ₗ[R] E →ₗ[R] R) (m : ℕ) :
    MultilinearMap R (fun _ : Slots m => E) R :=
  (MultilinearMap.mkPiAlgebra R (Fin m) R).compMultilinearMap fun _ => covariancePair B

@[simp]
theorem pairingProduct_apply (B : E →ₗ[R] E →ₗ[R] R) (m : ℕ) (v : Slots m → E) :
    pairingProduct B m v = ∏ i : Fin m, B (v ⟨i, 0⟩) (v ⟨i, 1⟩) := rfl

/-- The finite Wick moment. The denominator is `2^m m!`, not `(2m)!`. -/
noncomputable def wickMoment (B : E →ₗ[R] E →ₗ[R] R) (m : ℕ) :
    MultilinearMap R (fun _ : Slots m => E) R :=
  ((2 : R) ^ m * (m.factorial : R))⁻¹ •
    ∑ σ : Equiv.Perm (Slots m), (pairingProduct B m).domDomCongr σ

/-- The literal, finite covariance-pairing formula. -/
theorem wickMoment_apply (B : E →ₗ[R] E →ₗ[R] R) (m : ℕ) (v : Slots m → E) :
    wickMoment B m v = ((2 : R) ^ m * (m.factorial : R))⁻¹ *
      ∑ σ : Equiv.Perm (Slots m), ∏ i : Fin m,
        B (v (σ ⟨i, 0⟩)) (v (σ ⟨i, 1⟩)) := by
  simp [wickMoment, MultilinearMap.domDomCongr_apply]

/-- The empty pairing has weight one. -/
@[simp]
theorem wickMoment_zero (B : E →ₗ[R] E →ₗ[R] R) (v : Slots 0 → E) :
    wickMoment B 0 v = 1 := by
  simp [wickMoment_apply]

/-- Relabelling the input slots leaves the complete pairing sum unchanged. -/
theorem wickMoment_permute (B : E →ₗ[R] E →ₗ[R] R) (m : ℕ)
    (τ : Equiv.Perm (Slots m)) (v : Slots m → E) :
    wickMoment B m (fun i => v (τ i)) = wickMoment B m v := by
  simp only [wickMoment_apply]
  congr 1
  exact Fintype.sum_equiv (Equiv.mulLeft τ) _ _ (fun _ => rfl)

/-- On a repeated input, the formula records the exact permutation normalization. -/
theorem wickMoment_const (B : E →ₗ[R] E →ₗ[R] R) (m : ℕ) (x : E) :
    wickMoment B m (fun _ => x) =
      ((2 : R) ^ m * (m.factorial : R))⁻¹ *
        ((2 * m).factorial : R) * B x x ^ m := by
  simp only [wickMoment_apply, Finset.prod_const, Finset.card_univ, Fintype.card_fin,
    Finset.sum_const, nsmul_eq_mul, Fintype.card_perm, Fintype.card_sigma,
    Finset.sum_const, Nat.cast_id]
  rw [Nat.mul_comm m 2]
  ring

theorem slots_one_cases (i : Slots 1) : i = ⟨0, 0⟩ ∨ i = ⟨0, 1⟩ := by
  rcases i with ⟨i, j⟩
  fin_cases i
  fin_cases j <;> simp

/-- At order two the normalized sum is exactly the given symmetric covariance. -/
@[simp]
theorem wickMoment_one [CharZero R] (B : E →ₗ[R] E →ₗ[R] R)
    (hB : ∀ x y, B x y = B y x) (v : Slots 1 → E) :
    wickMoment B 1 v = B (v ⟨0, 0⟩) (v ⟨0, 1⟩) := by
  have hne : (⟨0, 0⟩ : Slots 1) ≠ ⟨0, 1⟩ := by decide
  have hterm (σ : Equiv.Perm (Slots 1)) :
      (∏ i : Fin 1, B (v (σ ⟨i, 0⟩)) (v (σ ⟨i, 1⟩))) =
        B (v ⟨0, 0⟩) (v ⟨0, 1⟩) := by
    rw [Fintype.prod_unique]
    change B (v (σ ⟨0, 0⟩)) (v (σ ⟨0, 1⟩)) = _
    rcases slots_one_cases (σ ⟨0, 0⟩) with h0 | h0
    · have h1 : σ ⟨0, 1⟩ = ⟨0, 1⟩ := by
        rcases slots_one_cases (σ ⟨0, 1⟩) with h1 | h1
        · exact False.elim (hne (σ.injective (h0.trans h1.symm)))
        · exact h1
      rw [h0, h1]
    · have h1 : σ ⟨0, 1⟩ = ⟨0, 0⟩ := by
        rcases slots_one_cases (σ ⟨0, 1⟩) with h1 | h1
        · exact h1
        · exact False.elim (hne (σ.injective (h0.trans h1.symm)))
      rw [h0, h1, hB]
  rw [wickMoment_apply]
  simp_rw [hterm]
  norm_num [Fintype.card_perm, Slots, nsmul_eq_mul]
  ring

/-- Every slot is linear; this is obtained from the constructed multilinear map. -/
theorem wickMoment_update_add (B : E →ₗ[R] E →ₗ[R] R) (m : ℕ)
    (v : Slots m → E) (i : Slots m) (x y : E) :
    wickMoment B m (Function.update v i (x + y)) =
      wickMoment B m (Function.update v i x) + wickMoment B m (Function.update v i y) :=
  (wickMoment B m).map_update_add v i x y

theorem wickMoment_update_smul (B : E →ₗ[R] E →ₗ[R] R) (m : ℕ)
    (v : Slots m → E) (i : Slots m) (c : R) (x : E) :
    wickMoment B m (Function.update v i (c • x)) =
      c * wickMoment B m (Function.update v i x) :=
  (wickMoment B m).map_update_smul v i c x

/-- Linear coordinate substitution expands into the full finite sum of pairing
moments, with one coefficient from every input slot. -/
theorem wickMoment_linear_expansion {ι : Type*} [Fintype ι]
    (B : E →ₗ[R] E →ₗ[R] R) (m : ℕ)
    (a : Slots m → ι → R) (v : ι → E) :
    wickMoment B m (fun i => ∑ j, a i j • v j) =
      ∑ choices : Slots m → ι,
        (∏ i, a i (choices i)) * wickMoment B m (fun i => v (choices i)) := by
  classical
  rw [(wickMoment B m).map_sum]
  apply Finset.sum_congr rfl
  intro choices _
  exact (wickMoment B m).map_smul_univ (fun i => a i (choices i)) _

/-- Naturality is proved from the actual pairing formula: pull back the covariance
or apply the same linear map to every input slot. -/
theorem wickMoment_naturality (B : F →ₗ[R] F →ₗ[R] R) (T : E →ₗ[R] F)
    (m : ℕ) (v : Slots m → E) :
    wickMoment (B.compl₁₂ T T) m v = wickMoment B m (fun i => T (v i)) := by
  simp only [wickMoment_apply, LinearMap.compl₁₂_apply]

/-- Any covariance-preserving linear map preserves every finite Wick moment. -/
theorem wickMoment_invariant (B : E →ₗ[R] E →ₗ[R] R) (T : E →ₗ[R] E)
    (hT : ∀ x y, B (T x) (T y) = B x y) (m : ℕ) (v : Slots m → E) :
    wickMoment B m (fun i => T (v i)) = wickMoment B m v := by
  simp only [wickMoment_apply, hT]

section ArbitrarySlots

variable {ι : Type*} [Fintype ι]

/-- For an even finite family, identify its labels with the reference paired slots.
The complete pairing sum is permutation invariant, so this choice carries no
mathematical restriction on the labels. -/
noncomputable def evenSlotsEquiv (h : Even (Fintype.card ι)) :
    Slots (Fintype.card ι / 2) ≃ ι :=
  Fintype.equivOfCardEq (by
    simp only [Slots, Fintype.card_sigma, Fintype.card_fin, Finset.sum_const,
      Finset.card_univ, smul_eq_mul]
    obtain ⟨k, hk⟩ := h
    omega)

/-- A centered moment on any finite set of labels; odd moments are exactly zero. -/
noncomputable def centeredMoment (B : E →ₗ[R] E →ₗ[R] R) :
    MultilinearMap R (fun _ : ι => E) R :=
  if h : Even (Fintype.card ι) then
    (wickMoment B (Fintype.card ι / 2)).domDomCongr (evenSlotsEquiv h)
  else 0

theorem centeredMoment_of_even (B : E →ₗ[R] E →ₗ[R] R)
    (h : Even (Fintype.card ι)) (v : ι → E) :
    centeredMoment B v = wickMoment B (Fintype.card ι / 2)
      (fun i => v (evenSlotsEquiv h i)) := by
  simp only [centeredMoment, dif_pos h, MultilinearMap.domDomCongr_apply]

@[simp]
theorem centeredMoment_of_not_even (B : E →ₗ[R] E →ₗ[R] R)
    (h : ¬Even (Fintype.card ι)) (v : ι → E) : centeredMoment B v = 0 := by
  simp [centeredMoment, h]

/-- Naturality holds for all arities, including the odd zero moments. -/
theorem centeredMoment_naturality (B : F →ₗ[R] F →ₗ[R] R) (T : E →ₗ[R] F)
    (v : ι → E) :
    centeredMoment (B.compl₁₂ T T) v = centeredMoment B (fun i => T (v i)) := by
  by_cases h : Even (Fintype.card ι)
  · simp only [centeredMoment_of_even _ h]
    exact wickMoment_naturality B T _ _
  · simp only [centeredMoment_of_not_even _ h]

/-- The arbitrary-label centered moment is symmetric in all its slots. -/
theorem centeredMoment_permute (B : E →ₗ[R] E →ₗ[R] R)
    (τ : Equiv.Perm ι) (v : ι → E) :
    centeredMoment B (fun i => v (τ i)) = centeredMoment B v := by
  by_cases h : Even (Fintype.card ι)
  · simp only [centeredMoment_of_even _ h]
    let e := evenSlotsEquiv (ι := ι) h
    have hw := wickMoment_permute B (Fintype.card ι / 2)
      ((e.trans τ).trans e.symm) (fun i => v (e i))
    simpa only [Equiv.trans_apply, Equiv.apply_symm_apply] using hw
  · simp only [centeredMoment_of_not_even _ h]

/-- The product of the deterministic means on a finite set of labels. -/
def meanProduct (μ : E →ₗ[R] R) : MultilinearMap R (fun _ : ι => E) R :=
  (MultilinearMap.mkPiAlgebra R ι R).compLinearMap fun _ => μ

@[simp]
theorem meanProduct_apply (μ : E →ₗ[R] R) (v : ι → E) :
    meanProduct μ v = ∏ i, μ (v i) := rfl

/-- The contribution with exactly the labels in `s` replaced by deterministic
means; its complement is evaluated by the actual centered pairing sum. -/
noncomputable def shiftedTerm (B : E →ₗ[R] E →ₗ[R] R) (μ : E →ₗ[R] R)
    (s : Finset ι) : MultilinearMap R (fun _ : ι => E) R := by
  classical
  exact ((meanProduct (ι := {i // i ∈ s}) μ).smulRight
    (centeredMoment (ι := {i // i ∉ s}) B)).uncurrySum.domDomCongr
      (Equiv.sumCompl fun i => i ∈ s)

theorem shiftedTerm_apply (B : E →ₗ[R] E →ₗ[R] R) (μ : E →ₗ[R] R)
    (s : Finset ι) (v : ι → E) :
    shiftedTerm B μ s v = (∏ i : {i // i ∈ s}, μ (v i)) *
      centeredMoment B (fun i : {i // i ∉ s} => v i) := rfl

/-- The complete finite shifted Wick moment, expanding every choice of mean or
centered variable. It is a multilinear map by construction. -/
noncomputable def shiftedMoment (B : E →ₗ[R] E →ₗ[R] R) (μ : E →ₗ[R] R) :
    MultilinearMap R (fun _ : ι => E) R :=
  ∑ s : Finset ι, shiftedTerm B μ s

theorem shiftedMoment_apply (B : E →ₗ[R] E →ₗ[R] R) (μ : E →ₗ[R] R) (v : ι → E) :
    shiftedMoment B μ v = ∑ s : Finset ι,
      (∏ i : {i // i ∈ s}, μ (v i)) *
        centeredMoment B (fun i : {i // i ∉ s} => v i) := by
  simp [shiftedMoment, shiftedTerm_apply]

/-- The complete shifted moment, including all mean terms, obeys the full linear
coordinate-substitution expansion. -/
theorem shiftedMoment_linear_expansion {κ : Type*} [Fintype κ]
    (B : E →ₗ[R] E →ₗ[R] R) (μ : E →ₗ[R] R)
    (a : ι → κ → R) (v : κ → E) :
    shiftedMoment B μ (fun i => ∑ j, a i j • v j) =
      ∑ choices : ι → κ,
        (∏ i, a i (choices i)) * shiftedMoment B μ (fun i => v (choices i)) := by
  rw [(shiftedMoment B μ).map_sum]
  apply Finset.sum_congr rfl
  intro choices _
  exact (shiftedMoment B μ).map_smul_univ (fun i => a i (choices i)) _

/-- The shifted finite pairing construction commutes with linear substitution;
both the covariance and the mean are pulled back literally. -/
theorem shiftedMoment_naturality (B : F →ₗ[R] F →ₗ[R] R) (μ : F →ₗ[R] R)
    (T : E →ₗ[R] F) (v : ι → E) :
    shiftedMoment (B.compl₁₂ T T) (μ.comp T) v =
      shiftedMoment B μ (fun i => T (v i)) := by
  simp only [shiftedMoment_apply, LinearMap.comp_apply, centeredMoment_naturality]

/-- Covariance-preserving substitution changes only the deterministic mean in
the complete shifted moment. -/
theorem shiftedMoment_invariant (B : E →ₗ[R] E →ₗ[R] R) (μ : E →ₗ[R] R)
    (T : E →ₗ[R] E) (hT : ∀ x y, B (T x) (T y) = B x y) (v : ι → E) :
    shiftedMoment B μ (fun i => T (v i)) = shiftedMoment B (μ.comp T) v := by
  have hB : B.compl₁₂ T T = B := by
    ext x y
    exact hT x y
  rw [← shiftedMoment_naturality, hB]

end ArbitrarySlots

/-- Two independent replicas have the direct-sum covariance. -/
def replicaCovariance (B : E →ₗ[R] E →ₗ[R] R) :
    (E × E) →ₗ[R] (E × E) →ₗ[R] R :=
  B.compl₁₂ (LinearMap.fst R E E) (LinearMap.fst R E E) +
    B.compl₁₂ (LinearMap.snd R E E) (LinearMap.snd R E E)

@[simp]
theorem replicaCovariance_apply (B : E →ₗ[R] E →ₗ[R] R) (x y : E × E) :
    replicaCovariance B x y = B x.1 y.1 + B x.2 y.2 := rfl

/-- A general linear change of the two replica coordinates. -/
def replicaLinear (a b c d : R) : (E × E) →ₗ[R] (E × E) :=
  (a • LinearMap.fst R E E + b • LinearMap.snd R E E).prod
    (c • LinearMap.fst R E E + d • LinearMap.snd R E E)

@[simp]
theorem replicaLinear_apply (a b c d : R) (x : E × E) :
    replicaLinear a b c d x = (a • x.1 + b • x.2, c • x.1 + d • x.2) := rfl

/-- Every algebraically orthogonal two-by-two change preserves covariance,
including determinant-minus-one reflections. -/
theorem replicaLinear_covariance (B : E →ₗ[R] E →ₗ[R] R) (a b c d : R)
    (hfirst : a ^ 2 + c ^ 2 = 1) (hsecond : b ^ 2 + d ^ 2 = 1)
    (hcross : a * b + c * d = 0) (x y : E × E) :
    replicaCovariance B (replicaLinear a b c d x) (replicaLinear a b c d y) =
      replicaCovariance B x y := by
  simp only [replicaCovariance_apply, replicaLinear_apply, map_add, map_smul,
    LinearMap.add_apply, LinearMap.smul_apply, smul_eq_mul]
  calc
    _ = (a ^ 2 + c ^ 2) * B x.1 y.1 + (b ^ 2 + d ^ 2) * B x.2 y.2 +
        (a * b + c * d) * (B x.1 y.2 + B x.2 y.1) := by ring
    _ = _ := by rw [hfirst, hsecond, hcross]; ring

/-- The local alternating product used to pair the two receiving replicas. -/
def alternatingProduct (μ ν : E →ₗ[R] R) (x : E × E) : R :=
  μ x.1 * ν x.2 - ν x.1 * μ x.2

/-- The local alternating product changes by the literal determinant. -/
theorem alternatingProduct_replicaLinear (μ ν : E →ₗ[R] R)
    (a b c d : R) (x : E × E) :
    alternatingProduct μ ν (replicaLinear a b c d x) =
      (a * d - b * c) * alternatingProduct μ ν x := by
  simp only [alternatingProduct, replicaLinear_apply, map_add, map_smul, smul_eq_mul]
  ring

/-- The literal two-replica rotation, with no analytic or probabilistic hypothesis. -/
def replicaRotation (a b : R) : (E × E) →ₗ[R] (E × E) :=
  (a • LinearMap.fst R E E + b • LinearMap.snd R E E).prod
    ((-b) • LinearMap.fst R E E + a • LinearMap.snd R E E)

@[simp]
theorem replicaRotation_apply (a b : R) (x : E × E) :
    replicaRotation a b x = (a • x.1 + b • x.2, (-b) • x.1 + a • x.2) := rfl

/-- Algebraic orthogonality preserves the replica covariance. -/
theorem replicaRotation_covariance (B : E →ₗ[R] E →ₗ[R] R) (a b : R)
    (h : a ^ 2 + b ^ 2 = 1) (x y : E × E) :
    replicaCovariance B (replicaRotation a b x) (replicaRotation a b y) =
      replicaCovariance B x y := by
  simp only [replicaCovariance_apply, replicaRotation_apply, map_add, map_smul,
    LinearMap.add_apply, LinearMap.smul_apply, smul_eq_mul]
  calc
    _ = (a ^ 2 + b ^ 2) * (B x.1 y.1 + B x.2 y.2) := by ring
    _ = _ := by rw [h, one_mul]

/-- The two-replica orthogonal invariance used in the finite reflection argument,
derived from pairing moments rather than assumed as a formal Gaussian axiom. -/
theorem wickMoment_replicaRotation (B : E →ₗ[R] E →ₗ[R] R) (a b : R)
    (h : a ^ 2 + b ^ 2 = 1) (m : ℕ) (v : Slots m → E × E) :
    wickMoment (replicaCovariance B) m (fun i => replicaRotation a b (v i)) =
      wickMoment (replicaCovariance B) m v :=
  wickMoment_invariant _ _ (replicaRotation_covariance B a b h) m v

/-- The same replica invariance for the complete finite expansion with means. -/
theorem shiftedMoment_replicaRotation {ι : Type*} [Fintype ι]
    (B : E →ₗ[R] E →ₗ[R] R) (μ : (E × E) →ₗ[R] R) (a b : R)
    (h : a ^ 2 + b ^ 2 = 1) (v : ι → E × E) :
    shiftedMoment (replicaCovariance B) μ (fun i => replicaRotation a b (v i)) =
      shiftedMoment (replicaCovariance B) (μ.comp (replicaRotation a b)) v :=
  shiftedMoment_invariant _ μ _ (replicaRotation_covariance B a b h) v

/-- Orthogonal reflections obey the same finite substitution law for all moments. -/
theorem shiftedMoment_replicaLinear {ι : Type*} [Fintype ι]
    (B : E →ₗ[R] E →ₗ[R] R) (μ : (E × E) →ₗ[R] R) (a b c d : R)
    (hfirst : a ^ 2 + c ^ 2 = 1) (hsecond : b ^ 2 + d ^ 2 = 1)
    (hcross : a * b + c * d = 0) (v : ι → E × E) :
    shiftedMoment (replicaCovariance B) μ (fun i => replicaLinear a b c d (v i)) =
      shiftedMoment (replicaCovariance B) (μ.comp (replicaLinear a b c d)) v :=
  shiftedMoment_invariant _ μ _ (replicaLinear_covariance B a b c d hfirst hsecond hcross) v

end KrennAllOrders.WickCovariance
