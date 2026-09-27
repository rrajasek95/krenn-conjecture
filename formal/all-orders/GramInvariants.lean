import ReplicaCovariance
import Mathlib.Algebra.MvPolynomial.PDeriv
import Mathlib.Tactic.Ring

/-!
# Scalar invariants and Gram coordinates for the two-replica matrix

This module keeps the algebraic invariant step separate from the construction
of the physical-source replica kernel.  The relevant covariance and polynomial
normal-form identities are explicit hypotheses.
-/

set_option autoImplicit false
set_option relaxedAutoImplicit false

namespace KrennAllOrders.GramInvariants

open KrennAllOrders.ReplicaCovariance
open scoped Matrix

section MatrixAlgebra

variable {R : Type*} [CommRing R] [IsDomain R]

/-- Scalar-plus-outer-product coefficients are unique for any two nonzero
columns.  This removes a coordinate-specific nonzero-entry condition. -/
theorem scalar_outer_unique_of_nonzero
    {P Q : Fin 2 → R} {a b a' b' : R} (hp : P ≠ 0) (hq : Q ≠ 0)
    (h : a • (1 : Matrix (Fin 2) (Fin 2) R) + b • Matrix.vecMulVec P Q =
      a' • (1 : Matrix (Fin 2) (Fin 2) R) + b' • Matrix.vecMulVec P Q) :
    a = a' ∧ b = b' := by
  have h₀₀ := congrArg (fun M : Matrix (Fin 2) (Fin 2) R => M 0 0) h
  have h₀₁ := congrArg (fun M : Matrix (Fin 2) (Fin 2) R => M 0 1) h
  have h₁₁ := congrArg (fun M : Matrix (Fin 2) (Fin 2) R => M 1 1) h
  change a * 1 + b * (P 0 * Q 0) = a' * 1 + b' * (P 0 * Q 0) at h₀₀
  change a * 0 + b * (P 0 * Q 1) = a' * 0 + b' * (P 0 * Q 1) at h₀₁
  change a * 1 + b * (P 1 * Q 1) = a' * 1 + b' * (P 1 * Q 1) at h₁₁
  simp only [mul_one] at h₀₀ h₁₁
  simp only [mul_zero, zero_add] at h₀₁
  have hd₀₀ : a - a' = -(b - b') * (P 0 * Q 0) := by
    linear_combination h₀₀
  have hd₁₁ : a - a' = -(b - b') * (P 1 * Q 1) := by
    linear_combination h₁₁
  have hd₀₁ : (b - b') * (P 0 * Q 1) = 0 := by
    linear_combination h₀₁
  have ha : a = a' := by
    apply sub_eq_zero.mp
    have hs : (a - a') ^ 2 = 0 := by
      calc
        _ = (-(b - b') * (P 0 * Q 0)) * (-(b - b') * (P 1 * Q 1)) := by
          exact (pow_two (a - a')).trans (congrArg₂ (· * ·) hd₀₀ hd₁₁)
        _ = ((b - b') * (P 0 * Q 1)) * ((b - b') * (P 1 * Q 0)) := by ring
        _ = 0 := by rw [hd₀₁, zero_mul]
    have hs' : (a - a') * (a - a') = 0 := by simpa [pow_two] using hs
    exact (mul_eq_zero.mp hs').elim id id
  obtain ⟨i, hi⟩ := Function.ne_iff.mp hp
  obtain ⟨j, hj⟩ := Function.ne_iff.mp hq
  have hij := congrArg (fun M : Matrix (Fin 2) (Fin 2) R => M i j) h
  have hb : b = b' := by
    apply mul_right_cancel₀ (mul_ne_zero hi hj)
    simpa [Matrix.vecMulVec, ← ha] using hij
  exact ⟨ha, hb⟩

omit [IsDomain R] in
/-- Orthogonal conjugation back to the original frame restores a normal form. -/
theorem conjugate_scalar_outer
    {O : Matrix (Fin 2) (Fin 2) R} (ho : Oᵀ * O = 1)
    (P Q : Fin 2 → R) (a b : R) :
    Oᵀ * (a • (1 : Matrix (Fin 2) (Fin 2) R) +
      b • Matrix.vecMulVec (O *ᵥ P) (O *ᵥ Q)) * O =
      a • (1 : Matrix (Fin 2) (Fin 2) R) + b • Matrix.vecMulVec P Q := by
  simp only [Matrix.mul_add, Matrix.add_mul, Matrix.mul_smul, Matrix.smul_mul,
    Matrix.mul_one, Matrix.mul_vecMulVec, Matrix.vecMulVec_mul,
    ← Matrix.mulVec_transpose, Matrix.mulVec_mulVec, ho, Matrix.one_mulVec]

end MatrixAlgebra

noncomputable section ScalarCovariance

variable {K : Type*} [Field K]

/-- Pull a scalar polynomial back along the simultaneous change of frame. -/
def framePullback (O : Matrix (Fin 2) (Fin 2) K) :
    MvPolynomial (Fin 4) K →+* MvPolynomial (Fin 4) K :=
  MvPolynomial.eval₂Hom MvPolynomial.C
    (columnAssignment ((O.map MvPolynomial.C) *ᵥ parameterP (K := K))
      ((O.map MvPolynomial.C) *ᵥ parameterQ (K := K)))

/-- A scalar polynomial invariant under every orthogonal change of frame. -/
def OrthogonalInvariant (p : MvPolynomial (Fin 4) K) : Prop :=
  ∀ O : Matrix (Fin 2) (Fin 2) K, Oᵀ * O = 1 → framePullback O p = p

theorem eval_framePullback (O : Matrix (Fin 2) (Fin 2) K)
    (p : MvPolynomial (Fin 4) K) (z : Fin 4 → K) :
    MvPolynomial.eval z (framePullback O p) =
      MvPolynomial.eval (columnAssignment (O *ᵥ ![z 0, z 1])
        (O *ᵥ ![z 2, z 3])) p := by
  change MvPolynomial.eval z (MvPolynomial.eval₂ MvPolynomial.C _ p) = _
  rw [← MvPolynomial.eval_assoc]
  have hassign : MvPolynomial.eval z ∘
      columnAssignment ((O.map MvPolynomial.C) *ᵥ parameterP (K := K))
        ((O.map MvPolynomial.C) *ᵥ parameterQ (K := K)) =
      columnAssignment (O *ᵥ ![z 0, z 1]) (O *ᵥ ![z 2, z 3]) := by
    ext i
    fin_cases i <;>
      simp [columnAssignment, parameterP, parameterQ, Matrix.mulVec, dotProduct,
        Fin.sum_univ_two, map_add, map_mul, MvPolynomial.eval_C, MvPolynomial.eval_X]
  rw [hassign]

theorem eval_normal_form
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    {a b : MvPolynomial (Fin 4) K}
    (hm : M = a • (1 : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) +
      b • Matrix.vecMulVec (parameterP (K := K)) (parameterQ (K := K)))
    (P Q : Fin 2 → K) :
    evalAtColumns M P Q =
      MvPolynomial.eval (columnAssignment P Q) a • (1 : Matrix (Fin 2) (Fin 2) K) +
      MvPolynomial.eval (columnAssignment P Q) b • Matrix.vecMulVec P Q := by
  rw [hm]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [evalAtColumns, columnAssignment, parameterP, parameterQ, Matrix.vecMulVec,
      map_add, map_mul, MvPolynomial.eval_X]

/-- Covariance identifies normal-form coefficients at any nonzero pair of
columns.  The polynomial extension below also covers zero columns. -/
theorem evaluated_coefficients_invariant
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    {a b : MvPolynomial (Fin 4) K} (hcov : OrthogonalCovariant M)
    (hm : M = a • (1 : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) +
      b • Matrix.vecMulVec (parameterP (K := K)) (parameterQ (K := K)))
    {O : Matrix (Fin 2) (Fin 2) K} (ho : Oᵀ * O = 1)
    {P Q : Fin 2 → K} (hp : P ≠ 0) (hq : Q ≠ 0) :
    MvPolynomial.eval (columnAssignment (O *ᵥ P) (O *ᵥ Q)) a =
        MvPolynomial.eval (columnAssignment P Q) a ∧
      MvPolynomial.eval (columnAssignment (O *ᵥ P) (O *ᵥ Q)) b =
        MvPolynomial.eval (columnAssignment P Q) b := by
  have hforms :
      MvPolynomial.eval (columnAssignment (O *ᵥ P) (O *ᵥ Q)) a •
          (1 : Matrix (Fin 2) (Fin 2) K) +
        MvPolynomial.eval (columnAssignment (O *ᵥ P) (O *ᵥ Q)) b •
          Matrix.vecMulVec P Q =
      MvPolynomial.eval (columnAssignment P Q) a • (1 : Matrix (Fin 2) (Fin 2) K) +
        MvPolynomial.eval (columnAssignment P Q) b • Matrix.vecMulVec P Q := by
    calc
      _ = Oᵀ * evalAtColumns M (O *ᵥ P) (O *ᵥ Q) * O := by
        rw [eval_normal_form hm, conjugate_scalar_outer ho]
      _ = Oᵀ * (O * evalAtColumns M P Q * Oᵀ) * O := by rw [hcov O P Q ho]
      _ = (Oᵀ * O) * evalAtColumns M P Q * (Oᵀ * O) := by
        simp only [Matrix.mul_assoc]
      _ = evalAtColumns M P Q := by rw [ho]; simp
      _ = _ := eval_normal_form hm P Q
  exact scalar_outer_unique_of_nonzero hp hq hforms

variable [Infinite K]

/-- The coefficients of an orthogonally covariant polynomial normal form are
themselves scalar orthogonal invariants, as polynomial identities. -/
theorem normal_form_coefficients_invariant
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    {a b : MvPolynomial (Fin 4) K} (hcov : OrthogonalCovariant M)
    (hm : M = a • (1 : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) +
      b • Matrix.vecMulVec (parameterP (K := K)) (parameterQ (K := K))) :
    OrthogonalInvariant a ∧ OrthogonalInvariant b := by
  have hext (p : MvPolynomial (Fin 4) K)
      (hp : ∀ (O : Matrix (Fin 2) (Fin 2) K), Oᵀ * O = 1 →
        ∀ (P Q : Fin 2 → K), P ≠ 0 → Q ≠ 0 →
          MvPolynomial.eval (columnAssignment (O *ᵥ P) (O *ᵥ Q)) p =
            MvPolynomial.eval (columnAssignment P Q) p) : OrthogonalInvariant p := by
    intro O ho
    have hprod :
        (dot₂ (parameterP (K := K)) (parameterP (K := K)) *
          dot₂ (parameterQ (K := K)) (parameterQ (K := K))) *
          (framePullback O p - p) = 0 := by
      apply MvPolynomial.funext
      intro z
      simp only [map_mul, map_sub, map_zero, eval_framePullback]
      have hrecover : MvPolynomial.eval z p =
          MvPolynomial.eval (columnAssignment ![z 0, z 1] ![z 2, z 3]) p := by
        rw [columnAssignment_recover]
      rw [hrecover]
      have hevalP : MvPolynomial.eval z
          (dot₂ (parameterP (K := K)) (parameterP (K := K))) =
          dot₂ ![z 0, z 1] ![z 0, z 1] := by
        simp [dot₂, parameterP, map_add, map_mul, MvPolynomial.eval_X]
      have hevalQ : MvPolynomial.eval z
          (dot₂ (parameterQ (K := K)) (parameterQ (K := K))) =
          dot₂ ![z 2, z 3] ![z 2, z 3] := by
        simp [dot₂, parameterQ, map_add, map_mul, MvPolynomial.eval_X]
      rw [hevalP, hevalQ]
      by_cases hP : dot₂ ![z 0, z 1] ![z 0, z 1] = 0
      · rw [hP, zero_mul, zero_mul]
      by_cases hQ : dot₂ ![z 2, z 3] ![z 2, z 3] = 0
      · rw [hQ, mul_zero, zero_mul]
      have hp' : (![z 0, z 1] : Fin 2 → K) ≠ 0 := by
        intro hz
        apply hP
        rw [hz]
        simp [dot₂]
      have hq' : (![z 2, z 3] : Fin 2 → K) ≠ 0 := by
        intro hz
        apply hQ
        rw [hz]
        simp [dot₂]
      rw [hp O ho _ _ hp' hq', sub_self, mul_zero]
    exact sub_eq_zero.mp ((mul_eq_zero.mp hprod).resolve_left
      (mul_ne_zero parameterP_norm_ne_zero parameterQ_norm_ne_zero))
  constructor
  · apply hext a
    intro O ho P Q hp hq
    exact (evaluated_coefficients_invariant hcov hm ho hp hq).1
  · apply hext b
    intro O ho P Q hp hq
    exact (evaluated_coefficients_invariant hcov hm ho hp hq).2

end ScalarCovariance

noncomputable section GramMaps

variable {K : Type*} [CommRing K]

/-- The polynomial substitution `(σ,τ,c) ↦ (P·P,Q·Q,P·Q)`. -/
def gramMap : MvPolynomial (Fin 3) K →+* MvPolynomial (Fin 4) K :=
  MvPolynomial.eval₂Hom MvPolynomial.C
    ![dot₂ (parameterP (K := K)) (parameterP (K := K)),
      dot₂ (parameterQ (K := K)) (parameterQ (K := K)),
      dot₂ (parameterP (K := K)) (parameterQ (K := K))]

/-- Gram substitution on the axis `Q₀=0`: `(σ,τ,c) ↦ (A²+B²,V²,BV)`. -/
def axisGramMap : MvPolynomial (Fin 3) K →+* MvPolynomial (Fin 3) K :=
  MvPolynomial.eval₂Hom MvPolynomial.C
    ![MvPolynomial.X 0 ^ 2 + MvPolynomial.X 1 ^ 2,
      MvPolynomial.X 2 ^ 2, MvPolynomial.X 1 * MvPolynomial.X 2]

/-- Restrict the original four parameter coordinates to `Q₀=0`. -/
def axisRestriction : MvPolynomial (Fin 4) K →+* MvPolynomial (Fin 3) K :=
  MvPolynomial.eval₂Hom MvPolynomial.C
    ![MvPolynomial.X 0, MvPolynomial.X 1, 0, MvPolynomial.X 2]

theorem axisRestriction_comp_gramMap :
    (axisRestriction (K := K)).comp gramMap = axisGramMap := by
  apply MvPolynomial.ringHom_ext
  · intro r
    simp [axisRestriction, gramMap, axisGramMap]
  · intro i
    fin_cases i <;>
      simp [axisRestriction, gramMap, axisGramMap, dot₂, parameterP, parameterQ, pow_two]

theorem eval_axisGramMap (p : MvPolynomial (Fin 3) K) (z : Fin 3 → K) :
    MvPolynomial.eval z (axisGramMap p) =
      MvPolynomial.eval ![z 0 ^ 2 + z 1 ^ 2, z 2 ^ 2, z 1 * z 2] p := by
  change MvPolynomial.eval z (MvPolynomial.eval₂ MvPolynomial.C _ p) = _
  rw [← MvPolynomial.eval_assoc]
  have hassign : MvPolynomial.eval z ∘
      (![MvPolynomial.X 0 ^ 2 + MvPolynomial.X 1 ^ 2,
        MvPolynomial.X 2 ^ 2, MvPolynomial.X 1 * MvPolynomial.X 2] :
          Fin 3 → MvPolynomial (Fin 3) K) =
      ![z 0 ^ 2 + z 1 ^ 2, z 2 ^ 2, z 1 * z 2] := by
    ext i
    fin_cases i <;> simp [map_add, map_mul, map_pow, MvPolynomial.eval_X]
  rw [hassign]

end GramMaps

noncomputable section GramInjectivity

variable {K : Type*} [Field K] [IsAlgClosed K]

/-- Every Gram-coordinate point with nonzero `τ` has a preimage on the axis.
This elementary square-root construction replaces an informal Jacobian or
generic-coordinate argument. -/
theorem exists_axis_gram_preimage (z : Fin 3 → K) (hτ : z 1 ≠ 0) :
    ∃ w : Fin 3 → K,
      ![w 0 ^ 2 + w 1 ^ 2, w 2 ^ 2, w 1 * w 2] = z := by
  obtain ⟨v, hv⟩ := IsAlgClosed.exists_pow_nat_eq (z 1) zero_lt_two
  have hv0 : v ≠ 0 := by
    intro h
    apply hτ
    rw [← hv, h]
    simp
  obtain ⟨a, ha⟩ := IsAlgClosed.exists_pow_nat_eq (z 0 - (z 2 / v) ^ 2) zero_lt_two
  refine ⟨![a, z 2 / v, v], ?_⟩
  ext i
  fin_cases i
  · change a ^ 2 + (z 2 / v) ^ 2 = z 0
    rw [ha]
    ring
  · exact hv
  · change (z 2 / v) * v = z 2
    simp [hv0]

/-- The axis Gram substitution is injective.  Its use in the PDE step therefore
does not discard a polynomial equation in `(σ,τ,c)`. -/
theorem axisGramMap_injective : Function.Injective (axisGramMap (K := K)) := by
  have hker (p : MvPolynomial (Fin 3) K) (hp : axisGramMap p = 0) : p = 0 := by
    have hprod : MvPolynomial.X 1 * p = 0 := by
      apply MvPolynomial.funext
      intro z
      rw [map_zero, map_mul, MvPolynomial.eval_X]
      by_cases hz : z 1 = 0
      · rw [hz, zero_mul]
      obtain ⟨w, hw⟩ := exists_axis_gram_preimage z hz
      have heval := congrArg (MvPolynomial.eval w) hp
      rw [eval_axisGramMap, hw, map_zero] at heval
      rw [heval, mul_zero]
    exact (mul_eq_zero.mp hprod).resolve_left (MvPolynomial.X_ne_zero 1)
  intro p q hpq
  apply sub_eq_zero.mp
  apply hker
  rw [map_sub, hpq, sub_self]

/-- The full Gram-coordinate substitution is injective as well. -/
theorem gramMap_injective : Function.Injective (gramMap (K := K)) := by
  intro p q hpq
  apply axisGramMap_injective
  have hcomp := congrArg (fun f : MvPolynomial (Fin 3) K →+*
      MvPolynomial (Fin 3) K => f p) (axisRestriction_comp_gramMap (K := K))
  have hcomp' := congrArg (fun f : MvPolynomial (Fin 3) K →+*
      MvPolynomial (Fin 3) K => f q) (axisRestriction_comp_gramMap (K := K))
  change axisRestriction (gramMap p) = axisGramMap p at hcomp
  change axisRestriction (gramMap q) = axisGramMap q at hcomp'
  rw [← hcomp, ← hcomp', hpq]

end GramInjectivity

section PowerSums

variable {A B : Type*} [CommRing A] [CommRing B]

/-- A denominator-free form of the two-variable symmetric-power recurrence. -/
theorem power_sum_mem_range (φ : A →+* B) {s t : B}
    (hs : s + t ∈ φ.range) (hp : s * t ∈ φ.range) (n : ℕ) :
    s ^ n + t ^ n ∈ φ.range := by
  induction n using Nat.twoStepInduction with
  | zero => simpa using φ.range.add_mem φ.range.one_mem φ.range.one_mem
  | one => simpa using hs
  | more n hn hn' =>
    have hm : (s + t) * (s ^ (n + 1) + t ^ (n + 1)) -
        (s * t) * (s ^ n + t ^ n) ∈ φ.range :=
      φ.range.sub_mem (φ.range.mul_mem hs hn') (φ.range.mul_mem hp hn)
    have heq : (s + t) * (s ^ (n + 1) + t ^ (n + 1)) -
        (s * t) * (s ^ n + t ^ n) = s ^ (n + 2) + t ^ (n + 2) := by
      rw [pow_succ, pow_succ, show n + 2 = (n + 1) + 1 by omega,
        pow_succ, pow_succ, pow_succ, pow_succ]
      ring
    rw [heq] at hm
    exact hm

end PowerSums

noncomputable section LightConeMonomials

variable {K : Type*} [CommRing K]

/-- The Gram generators in light-cone coordinates, with the third coordinate
scaled by two: `(p₊p₋,q₊q₋,p₊q₋+p₋q₊)`. -/
def lightGramMap : MvPolynomial (Fin 3) K →+* MvPolynomial (Fin 4) K :=
  MvPolynomial.eval₂Hom MvPolynomial.C
    ![MvPolynomial.X 0 * MvPolynomial.X 1,
      MvPolynomial.X 2 * MvPolynomial.X 3,
      MvPolynomial.X 0 * MvPolynomial.X 3 + MvPolynomial.X 1 * MvPolynomial.X 2]

/-- Reflection exchanges the two light-cone coordinates of each column. -/
def lightReflection : MvPolynomial (Fin 4) K →+* MvPolynomial (Fin 4) K :=
  MvPolynomial.eval₂Hom MvPolynomial.C
    ![MvPolynomial.X 1, MvPolynomial.X 0, MvPolynomial.X 3, MvPolynomial.X 2]

/-- A diagonal light-cone scaling; the inverse is supplied as a coefficient. -/
def lightScaling (r s : K) : MvPolynomial (Fin 4) K →+* MvPolynomial (Fin 4) K :=
  MvPolynomial.eval₂Hom MvPolynomial.C
    ![MvPolynomial.C r * MvPolynomial.X 0, MvPolynomial.C s * MvPolynomial.X 1,
      MvPolynomial.C r * MvPolynomial.X 2, MvPolynomial.C s * MvPolynomial.X 3]

@[simp] theorem lightScaling_C (r s a : K) :
    lightScaling r s (MvPolynomial.C a) = MvPolynomial.C a := by
  simp [lightScaling]

@[simp] theorem lightScaling_X (r s : K) (i : Fin 4) :
    lightScaling r s (MvPolynomial.X i) =
      (![MvPolynomial.C r * MvPolynomial.X 0, MvPolynomial.C s * MvPolynomial.X 1,
        MvPolynomial.C r * MvPolynomial.X 2, MvPolynomial.C s * MvPolynomial.X 3] i :
          MvPolynomial (Fin 4) K) := by
  simp [lightScaling]

@[simp] theorem lightReflection_C (a : K) :
    lightReflection (MvPolynomial.C a) = MvPolynomial.C a := by
  simp [lightReflection]

@[simp] theorem lightReflection_X (i : Fin 4) :
    lightReflection (MvPolynomial.X i) =
      (![MvPolynomial.X 1, MvPolynomial.X 0, MvPolynomial.X 3, MvPolynomial.X 2] i :
        MvPolynomial (Fin 4) K) := by
  simp [lightReflection]

private theorem monomial_four (d : Fin 4 →₀ ℕ) (a : K) :
    MvPolynomial.monomial d a = MvPolynomial.C a *
      (MvPolynomial.X 0 ^ d 0 * MvPolynomial.X 1 ^ d 1 *
        MvPolynomial.X 2 ^ d 2 * MvPolynomial.X 3 ^ d 3) := by
  have hd : Finsupp.indicator Finset.univ (fun i _ => d i) = d := by
    ext i
    simp
  have hm := MvPolynomial.prod_X_pow (R := K) d Finset.univ
  rw [hd] at hm
  calc
    _ = MvPolynomial.C a * MvPolynomial.monomial d 1 := by
      rw [MvPolynomial.C_mul_monomial, mul_one]
    _ = _ := by
      rw [← hm]
      congr 1
      simp [Fin.prod_univ_succ, mul_assoc]

theorem lightScaling_monomial (r s : K) (d : Fin 4 →₀ ℕ) (a : K) :
    lightScaling r s (MvPolynomial.monomial d a) =
      MvPolynomial.monomial d (a * r ^ (d 0 + d 2) * s ^ (d 1 + d 3)) := by
  rw [monomial_four, monomial_four]
  simp only [map_mul, map_pow, lightScaling_C, lightScaling_X]
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.cons_val_two, Matrix.cons_val_three]
  dsimp [Matrix.vecHead, Matrix.vecTail]
  simp only [pow_add, mul_pow]
  ring

/-- Coefficientwise diagonal action on light-cone monomials. -/
theorem coeff_lightScaling (r s : K) (p : MvPolynomial (Fin 4) K) (d : Fin 4 →₀ ℕ) :
    MvPolynomial.coeff d (lightScaling r s p) =
      MvPolynomial.coeff d p * r ^ (d 0 + d 2) * s ^ (d 1 + d 3) := by
  have hs := congrArg (lightScaling r s) (MvPolynomial.as_sum p)
  rw [map_sum] at hs
  rw [hs, MvPolynomial.coeff_sum]
  simp only [lightScaling_monomial, MvPolynomial.coeff_monomial]
  rw [Finset.sum_eq_single d]
  · simp
  · intro b hb hbd
    simp [hbd]
  · intro hd
    have hcoeff : MvPolynomial.coeff d p = 0 :=
      (MvPolynomial.notMem_support_iff).mp hd
    simp [hcoeff]

private theorem light_generator_mem (i : Fin 3) :
    (![MvPolynomial.X 0 * MvPolynomial.X 1,
      MvPolynomial.X 2 * MvPolynomial.X 3,
      MvPolynomial.X 0 * MvPolynomial.X 3 + MvPolynomial.X 1 * MvPolynomial.X 2] i :
        MvPolynomial (Fin 4) K) ∈ (lightGramMap (K := K)).range := by
  refine ⟨MvPolynomial.X i, ?_⟩
  simp [lightGramMap]

private theorem light_power_sum_mem (n : ℕ) :
    ((MvPolynomial.X 0 * MvPolynomial.X 3) ^ n +
      (MvPolynomial.X 1 * MvPolynomial.X 2) ^ n : MvPolynomial (Fin 4) K) ∈
      (lightGramMap (K := K)).range := by
  apply power_sum_mem_range
  · exact light_generator_mem 2
  · have h : ((MvPolynomial.X 0 * MvPolynomial.X 1) *
        (MvPolynomial.X 2 * MvPolynomial.X 3) : MvPolynomial (Fin 4) K) ∈
        (lightGramMap (K := K)).range := (lightGramMap (K := K)).range.mul_mem
      (light_generator_mem 0) (light_generator_mem 1)
    convert h using 1
    ring

/-- Every balanced light-cone monomial, symmetrized by reflection, belongs to
the Gram-coordinate polynomial ring. -/
theorem balanced_monomial_symmetrization_mem (d : Fin 4 →₀ ℕ) (a : K)
    (hd : d 0 + d 2 = d 1 + d 3) :
    MvPolynomial.monomial d a + lightReflection (MvPolynomial.monomial d a) ∈
      (lightGramMap (K := K)).range := by
  have hC : (MvPolynomial.C a : MvPolynomial (Fin 4) K) ∈
      (lightGramMap (K := K)).range := ⟨MvPolynomial.C a, by simp [lightGramMap]⟩
  have hA : (MvPolynomial.X 0 * MvPolynomial.X 1 : MvPolynomial (Fin 4) K) ∈
      (lightGramMap (K := K)).range := light_generator_mem 0
  have hB : (MvPolynomial.X 2 * MvPolynomial.X 3 : MvPolynomial (Fin 4) K) ∈
      (lightGramMap (K := K)).range := light_generator_mem 1
  by_cases h : d 1 ≤ d 0
  · have h₀ : d 0 = d 1 + (d 0 - d 1) := by omega
    have h₃ : d 3 = d 2 + (d 0 - d 1) := by omega
    have heq : MvPolynomial.monomial d a = MvPolynomial.C a *
        (MvPolynomial.X 0 * MvPolynomial.X 1) ^ d 1 *
        (MvPolynomial.X 2 * MvPolynomial.X 3) ^ d 2 *
        (MvPolynomial.X 0 * MvPolynomial.X 3) ^ (d 0 - d 1) := by
      conv_lhs => rw [monomial_four, h₀, h₃]
      simp only [pow_add, mul_pow]
      ring
    rw [heq]
    simp only [map_mul, map_pow, lightReflection_C, lightReflection_X]
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one,
      Matrix.cons_val_two, Matrix.cons_val_three]
    dsimp [Matrix.vecHead, Matrix.vecTail]
    have hm := (lightGramMap (K := K)).range.mul_mem
      ((lightGramMap (K := K)).range.mul_mem
        ((lightGramMap (K := K)).range.mul_mem hC
          ((lightGramMap (K := K)).range.pow_mem hA (d 1)))
        ((lightGramMap (K := K)).range.pow_mem hB (d 2)))
      (light_power_sum_mem (d 0 - d 1))
    convert hm using 1
    ring
  · have h₁ : d 1 = d 0 + (d 1 - d 0) := by omega
    have h₂ : d 2 = d 3 + (d 1 - d 0) := by omega
    have heq : MvPolynomial.monomial d a = MvPolynomial.C a *
        (MvPolynomial.X 0 * MvPolynomial.X 1) ^ d 0 *
        (MvPolynomial.X 2 * MvPolynomial.X 3) ^ d 3 *
        (MvPolynomial.X 1 * MvPolynomial.X 2) ^ (d 1 - d 0) := by
      conv_lhs => rw [monomial_four, h₁, h₂]
      simp only [pow_add, mul_pow]
      ring
    rw [heq]
    simp only [map_mul, map_pow, lightReflection_C, lightReflection_X]
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one,
      Matrix.cons_val_two, Matrix.cons_val_three]
    dsimp [Matrix.vecHead, Matrix.vecTail]
    have hm := (lightGramMap (K := K)).range.mul_mem
      ((lightGramMap (K := K)).range.mul_mem
        ((lightGramMap (K := K)).range.mul_mem hC
          ((lightGramMap (K := K)).range.pow_mem hA (d 0)))
        ((lightGramMap (K := K)).range.pow_mem hB (d 3)))
      (light_power_sum_mem (d 1 - d 0))
    convert hm using 1
    ring

end LightConeMonomials

noncomputable section LightConeRepresentation

variable {K : Type*} [Field K] [CharZero K]

/-- In characteristic zero, invariance under just the light-cone scaling by
`2` already forces every nonzero monomial to have weight zero. -/
theorem balanced_of_lightScaling_two
    (p : MvPolynomial (Fin 4) K) (hscale : lightScaling 2 (2 : K)⁻¹ p = p) :
    ∀ d ∈ p.support, d 0 + d 2 = d 1 + d 3 := by
  intro d hd
  have hc : MvPolynomial.coeff d p ≠ 0 := MvPolynomial.mem_support_iff.mp hd
  have hcoeff := congrArg (MvPolynomial.coeff d) hscale
  rw [coeff_lightScaling] at hcoeff
  have hpow : (2 : K) ^ (d 0 + d 2) = (2 : K) ^ (d 1 + d 3) := by
    have hprod : (2 : K) ^ (d 0 + d 2) * ((2 : K)⁻¹) ^ (d 1 + d 3) = 1 := by
      apply mul_left_cancel₀ hc
      simpa [mul_assoc] using hcoeff
    have hm := congrArg (fun a : K => a * (2 : K) ^ (d 1 + d 3)) hprod
    simpa [mul_assoc, ← mul_pow, two_ne_zero] using hm
  have hnat : (2 : ℕ) ^ (d 0 + d 2) = (2 : ℕ) ^ (d 1 + d 3) := by
    apply Nat.cast_injective (R := K)
    simpa using hpow
  exact Nat.pow_right_injective (by decide : 2 ≤ (2 : ℕ)) hnat

/-- Weight-zero light-cone polynomials fixed by reflection are polynomials in
the three light-cone Gram generators.  The proof is a finite monomial argument,
not an assumed invariant-ring theorem. -/
theorem light_gram_representation_of_balanced_reflection
    (p : MvPolynomial (Fin 4) K)
    (hbalance : ∀ d ∈ p.support, d 0 + d 2 = d 1 + d 3)
    (hreflection : lightReflection p = p) :
    ∃ g : MvPolynomial (Fin 3) K, lightGramMap g = p := by
  have hsum : ∑ d ∈ p.support, MvPolynomial.monomial d (MvPolynomial.coeff d p) = p :=
    MvPolynomial.support_sum_monomial_coeff p
  have hsumsym : p + lightReflection p =
      ∑ d ∈ p.support, (MvPolynomial.monomial d (MvPolynomial.coeff d p) +
        lightReflection (MvPolynomial.monomial d (MvPolynomial.coeff d p))) := by
    rw [Finset.sum_add_distrib, ← map_sum, hsum]
  have hsym : p + lightReflection p ∈ (lightGramMap (K := K)).range := by
    rw [hsumsym]
    apply (lightGramMap (K := K)).range.sum_mem
    intro d hd
    exact balanced_monomial_symmetrization_mem d _ (hbalance d hd)
  have hhalf : (MvPolynomial.C ((2 : K)⁻¹) : MvPolynomial (Fin 4) K) ∈
      (lightGramMap (K := K)).range :=
    ⟨MvPolynomial.C ((2 : K)⁻¹), by simp [lightGramMap]⟩
  have hp := (lightGramMap (K := K)).range.mul_mem hhalf hsym
  have heq : MvPolynomial.C ((2 : K)⁻¹) * (p + lightReflection p) = p := by
    rw [hreflection]
    calc
      _ = (MvPolynomial.C ((2 : K)⁻¹) * MvPolynomial.C (2 : K)) * p := by
        simp only [map_ofNat]
        ring
      _ = p := by rw [← map_mul, inv_mul_cancel₀ (two_ne_zero : (2 : K) ≠ 0), map_one, one_mul]
  rw [heq] at hp
  exact hp

end LightConeRepresentation

noncomputable section LightConeCoordinates

variable {K : Type*} [Field K] [CharZero K]

/-- Cartesian coordinates reconstructed from the light-cone columns. -/
def cartesianOfLight (i : K) (z : Fin 4 → K) : Fin 4 → K :=
  ![(z 0 + z 1) / 2, (-i / 2) * (z 0 - z 1),
    (z 2 + z 3) / 2, (-i / 2) * (z 2 - z 3)]

/-- Light-cone coordinates associated to Cartesian columns. -/
def lightOfCartesian (i : K) (z : Fin 4 → K) : Fin 4 → K :=
  ![z 0 + i * z 1, z 0 - i * z 1, z 2 + i * z 3, z 2 - i * z 3]

def toLightCone (i : K) : MvPolynomial (Fin 4) K →+* MvPolynomial (Fin 4) K :=
  MvPolynomial.eval₂Hom MvPolynomial.C
    ![MvPolynomial.C ((2 : K)⁻¹) * (MvPolynomial.X 0 + MvPolynomial.X 1),
      MvPolynomial.C (-i / 2) * (MvPolynomial.X 0 - MvPolynomial.X 1),
      MvPolynomial.C ((2 : K)⁻¹) * (MvPolynomial.X 2 + MvPolynomial.X 3),
      MvPolynomial.C (-i / 2) * (MvPolynomial.X 2 - MvPolynomial.X 3)]

def fromLightCone (i : K) : MvPolynomial (Fin 4) K →+* MvPolynomial (Fin 4) K :=
  MvPolynomial.eval₂Hom MvPolynomial.C
    ![MvPolynomial.X 0 + MvPolynomial.C i * MvPolynomial.X 1,
      MvPolynomial.X 0 - MvPolynomial.C i * MvPolynomial.X 1,
      MvPolynomial.X 2 + MvPolynomial.C i * MvPolynomial.X 3,
      MvPolynomial.X 2 - MvPolynomial.C i * MvPolynomial.X 3]

omit [CharZero K] in
theorem eval_toLightCone (i : K) (p : MvPolynomial (Fin 4) K) (z : Fin 4 → K) :
    MvPolynomial.eval z (toLightCone i p) = MvPolynomial.eval (cartesianOfLight i z) p := by
  change MvPolynomial.eval z (MvPolynomial.eval₂ MvPolynomial.C _ p) = _
  rw [← MvPolynomial.eval_assoc]
  have hassign : MvPolynomial.eval z ∘
      (![MvPolynomial.C ((2 : K)⁻¹) * (MvPolynomial.X 0 + MvPolynomial.X 1),
        MvPolynomial.C (-i / 2) * (MvPolynomial.X 0 - MvPolynomial.X 1),
        MvPolynomial.C ((2 : K)⁻¹) * (MvPolynomial.X 2 + MvPolynomial.X 3),
        MvPolynomial.C (-i / 2) * (MvPolynomial.X 2 - MvPolynomial.X 3)] :
          Fin 4 → MvPolynomial (Fin 4) K) = cartesianOfLight i z := by
    ext j
    fin_cases j <;> simp [cartesianOfLight, map_add, map_sub, map_mul,
      MvPolynomial.eval_C, MvPolynomial.eval_X, div_eq_mul_inv, mul_comm]
  rw [hassign]

omit [CharZero K] in
theorem eval_fromLightCone (i : K) (p : MvPolynomial (Fin 4) K) (z : Fin 4 → K) :
    MvPolynomial.eval z (fromLightCone i p) = MvPolynomial.eval (lightOfCartesian i z) p := by
  change MvPolynomial.eval z (MvPolynomial.eval₂ MvPolynomial.C _ p) = _
  rw [← MvPolynomial.eval_assoc]
  have hassign : MvPolynomial.eval z ∘
      (![MvPolynomial.X 0 + MvPolynomial.C i * MvPolynomial.X 1,
        MvPolynomial.X 0 - MvPolynomial.C i * MvPolynomial.X 1,
        MvPolynomial.X 2 + MvPolynomial.C i * MvPolynomial.X 3,
        MvPolynomial.X 2 - MvPolynomial.C i * MvPolynomial.X 3] :
          Fin 4 → MvPolynomial (Fin 4) K) = lightOfCartesian i z := by
    ext j
    fin_cases j <;> simp [lightOfCartesian, map_add, map_sub, map_mul,
      MvPolynomial.eval_C, MvPolynomial.eval_X]
  rw [hassign]

theorem cartesian_light_inverse {i : K} (hi : i ^ 2 = -1) (z : Fin 4 → K) :
    cartesianOfLight i (lightOfCartesian i z) = z := by
  ext j
  fin_cases j <;> simp [cartesianOfLight, lightOfCartesian] <;> field_simp
  all_goals
    ring_nf
    simp [hi]

variable [Infinite K]

theorem fromLightCone_toLightCone {i : K} (hi : i ^ 2 = -1)
    (p : MvPolynomial (Fin 4) K) : fromLightCone i (toLightCone i p) = p := by
  apply MvPolynomial.funext
  intro z
  rw [eval_fromLightCone, eval_toLightCone, cartesian_light_inverse hi]

/-- One explicit orthogonal matrix implementing light-cone scaling by `2`. -/
def scalingFrame (i : K) : Matrix (Fin 2) (Fin 2) K :=
  !![5 / 4, 3 * i / 4; -(3 * i / 4), 5 / 4]

omit [Infinite K] in
theorem scalingFrame_orthogonal {i : K} (hi : i ^ 2 = -1) :
    (scalingFrame i)ᵀ * scalingFrame i = 1 := by
  ext j k
  fin_cases j <;> fin_cases k <;>
    simp [scalingFrame, Matrix.mul_apply, Fin.sum_univ_two] <;> field_simp
  all_goals
    ring_nf <;> norm_num [hi]

omit [CharZero K] [Infinite K] in
theorem eval_lightScaling (r s : K) (p : MvPolynomial (Fin 4) K) (z : Fin 4 → K) :
    MvPolynomial.eval z (lightScaling r s p) =
      MvPolynomial.eval ![r * z 0, s * z 1, r * z 2, s * z 3] p := by
  change MvPolynomial.eval z (MvPolynomial.eval₂ MvPolynomial.C _ p) = _
  rw [← MvPolynomial.eval_assoc]
  have hassign : MvPolynomial.eval z ∘
      (![MvPolynomial.C r * MvPolynomial.X 0, MvPolynomial.C s * MvPolynomial.X 1,
        MvPolynomial.C r * MvPolynomial.X 2, MvPolynomial.C s * MvPolynomial.X 3] :
          Fin 4 → MvPolynomial (Fin 4) K) = ![r * z 0, s * z 1, r * z 2, s * z 3] := by
    ext j
    fin_cases j <;> simp [map_mul, MvPolynomial.eval_C, MvPolynomial.eval_X]
  rw [hassign]

omit [CharZero K] [Infinite K] in
theorem eval_lightReflection (p : MvPolynomial (Fin 4) K) (z : Fin 4 → K) :
    MvPolynomial.eval z (lightReflection p) = MvPolynomial.eval ![z 1, z 0, z 3, z 2] p := by
  change MvPolynomial.eval z (MvPolynomial.eval₂ MvPolynomial.C _ p) = _
  rw [← MvPolynomial.eval_assoc]
  have hassign : MvPolynomial.eval z ∘
      (![MvPolynomial.X 1, MvPolynomial.X 0, MvPolynomial.X 3, MvPolynomial.X 2] :
          Fin 4 → MvPolynomial (Fin 4) K) = ![z 1, z 0, z 3, z 2] := by
    ext j
    fin_cases j <;> simp [MvPolynomial.eval_X]
  rw [hassign]

omit [Infinite K] in
theorem cartesian_scalingFrame {i : K} (hi : i ^ 2 = -1) (z : Fin 4 → K) :
    cartesianOfLight i ![2 * z 0, (2 : K)⁻¹ * z 1, 2 * z 2, (2 : K)⁻¹ * z 3] =
      columnAssignment (scalingFrame i *ᵥ ![(cartesianOfLight i z) 0, (cartesianOfLight i z) 1])
        (scalingFrame i *ᵥ ![(cartesianOfLight i z) 2, (cartesianOfLight i z) 3]) := by
  ext j
  fin_cases j <;>
    simp [cartesianOfLight, scalingFrame, columnAssignment, Matrix.mulVec,
      dotProduct, Fin.sum_univ_two] <;> field_simp
  all_goals
    ring_nf <;> (norm_num [hi]; ring)

/-- Reflection of both light-cone columns is an ordinary Cartesian reflection. -/
def reflectionFrame : Matrix (Fin 2) (Fin 2) K := !![1, 0; 0, -1]

omit [CharZero K] [Infinite K] in
theorem reflectionFrame_orthogonal :
    (reflectionFrame (K := K))ᵀ * reflectionFrame = 1 := by
  ext j k
  fin_cases j <;> fin_cases k <;>
    simp [reflectionFrame, Matrix.mul_apply, Fin.sum_univ_two]

omit [CharZero K] [Infinite K] in
theorem cartesian_reflectionFrame (i : K) (z : Fin 4 → K) :
    cartesianOfLight i ![z 1, z 0, z 3, z 2] =
      columnAssignment (reflectionFrame *ᵥ ![(cartesianOfLight i z) 0, (cartesianOfLight i z) 1])
        (reflectionFrame *ᵥ ![(cartesianOfLight i z) 2, (cartesianOfLight i z) 3]) := by
  ext j
  fin_cases j <;>
    simp [cartesianOfLight, reflectionFrame, columnAssignment, Matrix.mulVec,
      dotProduct, Fin.sum_univ_two] <;> ring

theorem lightScaling_toLightCone {i : K} (hi : i ^ 2 = -1)
    (p : MvPolynomial (Fin 4) K) :
    lightScaling 2 (2 : K)⁻¹ (toLightCone i p) =
      toLightCone i (framePullback (scalingFrame i) p) := by
  apply MvPolynomial.funext
  intro z
  rw [eval_lightScaling, eval_toLightCone, eval_toLightCone, eval_framePullback,
    cartesian_scalingFrame hi]

omit [CharZero K] in
theorem lightReflection_toLightCone (i : K) (p : MvPolynomial (Fin 4) K) :
    lightReflection (toLightCone i p) = toLightCone i (framePullback reflectionFrame p) := by
  apply MvPolynomial.funext
  intro z
  rw [eval_lightReflection, eval_toLightCone, eval_toLightCone, eval_framePullback,
    cartesian_reflectionFrame]

/-- Orthogonal invariance supplies the two proven light-cone representation
conditions: weight zero and reflection symmetry. -/
theorem light_gram_representation_of_orthogonalInvariant
    {i : K} (hi : i ^ 2 = -1) (p : MvPolynomial (Fin 4) K)
    (hp : OrthogonalInvariant p) :
    ∃ g : MvPolynomial (Fin 3) K, lightGramMap g = toLightCone i p := by
  apply light_gram_representation_of_balanced_reflection
  · apply balanced_of_lightScaling_two
    rw [lightScaling_toLightCone hi, hp _ (scalingFrame_orthogonal hi)]
  · rw [lightReflection_toLightCone, hp _ reflectionFrame_orthogonal]

/-- Correct the factor of two in the third light-cone Gram generator. -/
def doubleThird : MvPolynomial (Fin 3) K →+* MvPolynomial (Fin 3) K :=
  MvPolynomial.eval₂Hom MvPolynomial.C
    ![MvPolynomial.X 0, MvPolynomial.X 1, 2 * MvPolynomial.X 2]

omit [CharZero K] in
theorem fromLightCone_comp_lightGramMap {i : K} (hi : i ^ 2 = -1) :
    (fromLightCone i).comp lightGramMap = (gramMap (K := K)).comp doubleThird := by
  apply MvPolynomial.ringHom_ext
  · intro a
    simp [fromLightCone, lightGramMap, gramMap, doubleThird]
  · intro j
    apply MvPolynomial.funext
    intro z
    change MvPolynomial.eval z (fromLightCone i (lightGramMap (MvPolynomial.X j))) =
      MvPolynomial.eval z (gramMap (doubleThird (MvPolynomial.X j)))
    rw [eval_fromLightCone]
    fin_cases j <;>
      simp [lightGramMap, gramMap, doubleThird, lightOfCartesian, dot₂,
        parameterP, parameterQ, map_add, map_mul, MvPolynomial.eval_X]
    all_goals
      ring_nf; norm_num [hi]

variable [IsAlgClosed K]

/-- The two-column orthogonal invariant-ring theorem used by the manuscript:
every invariant scalar polynomial is a polynomial in `σ=P·P`, `τ=Q·Q`, and
`c=P·Q`.  The light-cone balance and reflection arguments are proved above. -/
theorem gram_representation_of_orthogonalInvariant
    (p : MvPolynomial (Fin 4) K) (hp : OrthogonalInvariant p) :
    ∃ g : MvPolynomial (Fin 3) K, gramMap g = p := by
  obtain ⟨i, hi⟩ := IsAlgClosed.exists_pow_nat_eq (-1 : K) zero_lt_two
  obtain ⟨g, hg⟩ := light_gram_representation_of_orthogonalInvariant hi p hp
  refine ⟨doubleThird g, ?_⟩
  have hcomp := congrArg (fun f : MvPolynomial (Fin 3) K →+*
      MvPolynomial (Fin 4) K => f g) (fromLightCone_comp_lightGramMap hi)
  change fromLightCone i (lightGramMap g) = gramMap (doubleThird g) at hcomp
  rw [← hcomp, hg, fromLightCone_toLightCone hi]

/-- The normal-form coefficients of the covariant replica matrix admit genuine
Gram-coordinate polynomial representatives.  The source-kernel hypotheses are
still explicit; no physical covariance theorem is assumed by the formalization. -/
theorem normal_form_coefficients_gram_representation
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    {a b : MvPolynomial (Fin 4) K} (hcov : OrthogonalCovariant M)
    (hm : M = a • (1 : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) +
      b • Matrix.vecMulVec (parameterP (K := K)) (parameterQ (K := K))) :
    ∃ A B : MvPolynomial (Fin 3) K, gramMap A = a ∧ gramMap B = b := by
  obtain ⟨ha, hb⟩ := normal_form_coefficients_invariant hcov hm
  obtain ⟨A, hA⟩ := gram_representation_of_orthogonalInvariant a ha
  obtain ⟨B, hB⟩ := gram_representation_of_orthogonalInvariant b hb
  exact ⟨A, B, hA, hB⟩

/-- The full covariance/divisibility step, now expressed by actual
Gram-coordinate polynomials rather than unspecified invariant coefficients. -/
theorem orthogonal_covariant_gram_normal_form
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    (hcov : OrthogonalCovariant M)
    (h₀₁ : parameterP (K := K) 0 * parameterQ (K := K) 1 ∣ M 0 1)
    (h₁₀ : parameterP (K := K) 1 * parameterQ (K := K) 0 ∣ M 1 0) :
    ∃ A B : MvPolynomial (Fin 3) K,
      M = gramMap A • (1 : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) +
        gramMap B • Matrix.vecMulVec (parameterP (K := K)) (parameterQ (K := K)) := by
  obtain ⟨a, b, hm⟩ := polynomial_normal_form_of_covariance hcov h₀₁ h₁₀
  obtain ⟨A, B, hA, hB⟩ := normal_form_coefficients_gram_representation hcov hm
  exact ⟨A, B, by simpa [hA, hB] using hm⟩

/-- Both Gram-coordinate representatives in the normal form are unique. -/
theorem orthogonal_covariant_gram_normal_form_unique
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    (hcov : OrthogonalCovariant M)
    (h₀₁ : parameterP (K := K) 0 * parameterQ (K := K) 1 ∣ M 0 1)
    (h₁₀ : parameterP (K := K) 1 * parameterQ (K := K) 0 ∣ M 1 0) :
    ∃! AB : MvPolynomial (Fin 3) K × MvPolynomial (Fin 3) K,
      M = gramMap AB.1 • (1 : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) +
        gramMap AB.2 • Matrix.vecMulVec (parameterP (K := K)) (parameterQ (K := K)) := by
  obtain ⟨A, B, hm⟩ := orthogonal_covariant_gram_normal_form hcov h₀₁ h₁₀
  refine ⟨(A, B), hm, ?_⟩
  intro AB hAB
  obtain ⟨hA, hB⟩ := polynomial_normal_form_unique (hAB.symm.trans hm)
  exact Prod.ext (gramMap_injective hA) (gramMap_injective hB)

end LightConeCoordinates

end KrennAllOrders.GramInvariants
