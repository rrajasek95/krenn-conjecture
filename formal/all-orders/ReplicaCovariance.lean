import Mathlib.Algebra.MvPolynomial.Eval
import Mathlib.Algebra.MvPolynomial.Funext
import Mathlib.FieldTheory.IsAlgClosed.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.FieldSimp

/-!
# The algebraic two-replica matrix step

This file formalizes an algebraic part of the finite two-replica argument.  The
physical-source tensor identities and their orthogonal covariance are not
assumed implicitly: callers must supply the two explicit wedge identities and
the two off-diagonal divisibilities.  Over independent polynomial parameters,
these hypotheses force a polynomial scalar-plus-outer-product normal form.
-/

set_option autoImplicit false
set_option relaxedAutoImplicit false

namespace KrennAllOrders.ReplicaCovariance

open scoped Matrix

section Domain

variable {R : Type*} [CommRing R] [IsDomain R]

/-- The alternating pairing on two-dimensional column vectors. -/
def cross₂ (v w : Fin 2 → R) : R := v 0 * w 1 - v 1 * w 0

/-- The ordinary bilinear pairing on two-dimensional column vectors. -/
def dot₂ (v w : Fin 2 → R) : R := v 0 * w 0 + v 1 * w 1

/-- Entrywise version of the polynomial normal-form argument.  No division is
used.  In the intended polynomial application the three nonzero factors are
nonzero polynomials, rather than assumptions on an individual parameter point. -/
theorem normal_form_entries
    {p₀ p₁ q₀ q₁ m₀₀ m₀₁ m₁₀ m₁₁ b b' : R}
    (hp : p₀ * p₁ ≠ 0) (hq : q₀ * q₁ ≠ 0)
    (hc : p₀ * q₀ + p₁ * q₁ ≠ 0)
    (h₀₁ : m₀₁ = p₀ * q₁ * b) (h₁₀ : m₁₀ = p₁ * q₀ * b')
    (hP : p₀ ^ 2 * m₁₀ + p₀ * p₁ * (m₁₁ - m₀₀) - p₁ ^ 2 * m₀₁ = 0)
    (hQ : q₀ ^ 2 * m₀₁ + q₀ * q₁ * (m₁₁ - m₀₀) - q₁ ^ 2 * m₁₀ = 0) :
    b = b' ∧ ∃ a : R,
      m₀₀ = a + b * p₀ * q₀ ∧ m₀₁ = b * p₀ * q₁ ∧
      m₁₀ = b * p₁ * q₀ ∧ m₁₁ = a + b * p₁ * q₁ := by
  have hP' : p₀ * p₁ *
      ((m₁₁ - m₀₀) - (p₁ * q₁ * b - p₀ * q₀ * b')) = 0 := by
    calc
      _ = p₀ ^ 2 * m₁₀ + p₀ * p₁ * (m₁₁ - m₀₀) - p₁ ^ 2 * m₀₁ := by
        rw [h₀₁, h₁₀]
        ring
      _ = 0 := hP
  have hQ' : q₀ * q₁ *
      ((m₁₁ - m₀₀) - (p₁ * q₁ * b' - p₀ * q₀ * b)) = 0 := by
    calc
      _ = q₀ ^ 2 * m₀₁ + q₀ * q₁ * (m₁₁ - m₀₀) - q₁ ^ 2 * m₁₀ := by
        rw [h₀₁, h₁₀]
        ring
      _ = 0 := hQ
  have hdP : m₁₁ - m₀₀ = p₁ * q₁ * b - p₀ * q₀ * b' :=
    sub_eq_zero.mp ((mul_eq_zero.mp hP').resolve_left hp)
  have hdQ : m₁₁ - m₀₀ = p₁ * q₁ * b' - p₀ * q₀ * b :=
    sub_eq_zero.mp ((mul_eq_zero.mp hQ').resolve_left hq)
  have hbb : (p₀ * q₀ + p₁ * q₁) * (b - b') = 0 := by
    calc
      _ = (p₁ * q₁ * b - p₀ * q₀ * b') -
          (p₁ * q₁ * b' - p₀ * q₀ * b) := by ring
      _ = 0 := by rw [← hdP, ← hdQ]; ring
  have hb : b = b' := sub_eq_zero.mp ((mul_eq_zero.mp hbb).resolve_left hc)
  refine ⟨hb, m₀₀ - b * p₀ * q₀, ?_, ?_, ?_, ?_⟩
  · ring
  · rw [h₀₁]
    ring
  · rw [h₁₀, ← hb]
    ring
  · calc
      m₁₁ = m₀₀ + (m₁₁ - m₀₀) := by ring
      _ = (m₀₀ - b * p₀ * q₀) + b * p₁ * q₁ := by rw [hdP, ← hb]; ring

/-- A matrix-facing form of `normal_form_entries`.  Wedge vanishing expresses
that `P` and `Q` are respectively right and left eigenvector directions, without
introducing rational eigenvalue functions. -/
theorem normal_form_of_wedges_and_divisibility
    {M : Matrix (Fin 2) (Fin 2) R} {P Q : Fin 2 → R} {b b' : R}
    (hp : P 0 * P 1 ≠ 0) (hq : Q 0 * Q 1 ≠ 0) (hc : dot₂ P Q ≠ 0)
    (h₀₁ : M 0 1 = P 0 * Q 1 * b) (h₁₀ : M 1 0 = P 1 * Q 0 * b')
    (hP : cross₂ P (M *ᵥ P) = 0) (hQ : cross₂ Q (Mᵀ *ᵥ Q) = 0) :
    b = b' ∧ ∃ a : R, M = a • (1 : Matrix (Fin 2) (Fin 2) R) +
      b • Matrix.vecMulVec P Q := by
  have hP' : P 0 ^ 2 * M 1 0 + P 0 * P 1 * (M 1 1 - M 0 0) -
      P 1 ^ 2 * M 0 1 = 0 := by
    calc
      _ = cross₂ P (M *ᵥ P) := by
        simp [cross₂, Matrix.mulVec, dotProduct, Fin.sum_univ_two]
        ring
      _ = 0 := hP
  have hQ' : Q 0 ^ 2 * M 0 1 + Q 0 * Q 1 * (M 1 1 - M 0 0) -
      Q 1 ^ 2 * M 1 0 = 0 := by
    calc
      _ = cross₂ Q (Mᵀ *ᵥ Q) := by
        simp [cross₂, Matrix.mulVec, dotProduct, Fin.sum_univ_two]
        ring
      _ = 0 := hQ
  obtain ⟨hb, a, h₀₀, h₀₁', h₁₀', h₁₁⟩ :=
    normal_form_entries hp hq hc h₀₁ h₁₀ hP' hQ'
  refine ⟨hb, a, ?_⟩
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.vecMulVec, h₀₀, h₀₁', h₁₀', h₁₁, mul_assoc]

/-- Exact eigenvector equations imply the wedge hypotheses used above. -/
theorem normal_form_of_eigenvectors_and_divisibility
    {M : Matrix (Fin 2) (Fin 2) R} {P Q : Fin 2 → R} {b b' lval rval : R}
    (hp : P 0 * P 1 ≠ 0) (hq : Q 0 * Q 1 ≠ 0) (hc : dot₂ P Q ≠ 0)
    (h₀₁ : M 0 1 = P 0 * Q 1 * b) (h₁₀ : M 1 0 = P 1 * Q 0 * b')
    (hP : M *ᵥ P = lval • P) (hQ : Mᵀ *ᵥ Q = rval • Q) :
    b = b' ∧ ∃ a : R, M = a • (1 : Matrix (Fin 2) (Fin 2) R) +
      b • Matrix.vecMulVec P Q := by
  apply normal_form_of_wedges_and_divisibility hp hq hc h₀₁ h₁₀
  · rw [hP]
    simp [cross₂]
    ring
  · rw [hQ]
    simp [cross₂]
    ring

/-- The scalar and outer-product coefficients are unique wherever the indicated
outer-product entry is nonzero. -/
theorem scalar_outer_coefficients_unique
    {P Q : Fin 2 → R} {a b a' b' : R} (hpq : P 0 * Q 1 ≠ 0)
    (h : a • (1 : Matrix (Fin 2) (Fin 2) R) + b • Matrix.vecMulVec P Q =
      a' • (1 : Matrix (Fin 2) (Fin 2) R) + b' • Matrix.vecMulVec P Q) :
    a = a' ∧ b = b' := by
  have h₀₁ := congrArg (fun M : Matrix (Fin 2) (Fin 2) R => M 0 1) h
  have hb : b = b' := by
    apply mul_right_cancel₀ hpq
    simpa [Matrix.vecMulVec] using h₀₁
  have h₀₀ := congrArg (fun M : Matrix (Fin 2) (Fin 2) R => M 0 0) h
  have ha : a = a' := by
    apply add_right_cancel (b := b * (P 0 * Q 0))
    simpa [Matrix.vecMulVec, ← hb] using h₀₀
  exact ⟨ha, hb⟩

end Domain

section AdaptedFrames

variable {K : Type*} [Field K]

/-- An orthogonal frame whose first coordinate annihilates `P`, when
`s² = P·P`. -/
def adaptedFrame (P : Fin 2 → K) (s : K) : Matrix (Fin 2) (Fin 2) K :=
  !![P 1 / s, -(P 0 / s); P 0 / s, P 1 / s]

theorem adaptedFrame_orthogonal {P : Fin 2 → K} {s : K}
    (hs : s ≠ 0) (hsq : s ^ 2 = dot₂ P P) :
    (adaptedFrame P s)ᵀ * adaptedFrame P s = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [adaptedFrame, Matrix.mul_apply, Fin.sum_univ_two, dot₂] at * <;>
    field_simp
  all_goals
    try rw [hsq]
    ring

theorem adaptedFrame_first_coordinate {P : Fin 2 → K} {s : K} :
    (adaptedFrame P s *ᵥ P) 0 = 0 := by
  simp [adaptedFrame, Matrix.mulVec, dotProduct, Fin.sum_univ_two]
  ring

/-- A transverse zero in an adapted frame forces the right wedge identity.
This is the precise finite-dimensional covariance-to-eigenvector step. -/
theorem cross₂_eq_zero_of_adapted_frame
    {M N : Matrix (Fin 2) (Fin 2) K} {P : Fin 2 → K} {s : K}
    (hs : s ≠ 0)
    (hcov : N = adaptedFrame P s * M * (adaptedFrame P s)ᵀ)
    (hzero : N 0 1 = 0) : cross₂ P (M *ᵥ P) = 0 := by
  have hentry := congrArg (fun A : Matrix (Fin 2) (Fin 2) K => A 0 1) hcov
  rw [hzero] at hentry
  have hscaled : cross₂ P (M *ᵥ P) = -s ^ 2 *
      (adaptedFrame P s * M * (adaptedFrame P s)ᵀ) 0 1 := by
    simp [cross₂, Matrix.mulVec, Matrix.vecMul, dotProduct, Matrix.mul_apply, adaptedFrame,
      Fin.sum_univ_two]
    field_simp
    ring
  rw [hscaled, ← hentry]
  ring

end AdaptedFrames

noncomputable section IndependentParameters

variable {K : Type*} [CommRing K] [IsDomain K]

/-- The first independent polynomial parameter column. -/
def parameterP : Fin 2 → MvPolynomial (Fin 4) K :=
  ![MvPolynomial.X 0, MvPolynomial.X 1]

/-- The second independent polynomial parameter column. -/
def parameterQ : Fin 2 → MvPolynomial (Fin 4) K :=
  ![MvPolynomial.X 2, MvPolynomial.X 3]

theorem parameterP_product_ne_zero :
    parameterP (K := K) 0 * parameterP (K := K) 1 ≠ 0 := by
  exact mul_ne_zero (MvPolynomial.X_ne_zero 0) (MvPolynomial.X_ne_zero 1)

theorem parameterQ_product_ne_zero :
    parameterQ (K := K) 0 * parameterQ (K := K) 1 ≠ 0 := by
  exact mul_ne_zero (MvPolynomial.X_ne_zero 2) (MvPolynomial.X_ne_zero 3)

/-- The Gram cross-coordinate is a nonzero polynomial.  Evaluating at
`P = Q = (1,0)` proves this without any generic-point convention. -/
theorem parameter_dot_ne_zero :
    dot₂ (parameterP (K := K)) (parameterQ (K := K)) ≠ 0 := by
  intro h
  have heval := congrArg (MvPolynomial.eval (![1, 0, 1, 0] : Fin 4 → K)) h
  simp [dot₂, parameterP, parameterQ, MvPolynomial.eval_add,
    MvPolynomial.eval_mul, MvPolynomial.eval_X] at heval

/-- The first parameter norm is also a nonzero polynomial; isotropic parameter
points do not make the polynomial itself zero. -/
theorem parameterP_norm_ne_zero :
    dot₂ (parameterP (K := K)) (parameterP (K := K)) ≠ 0 := by
  intro h
  have heval := congrArg (MvPolynomial.eval (![1, 0, 0, 0] : Fin 4 → K)) h
  simp [dot₂, parameterP, MvPolynomial.eval_add,
    MvPolynomial.eval_mul, MvPolynomial.eval_X] at heval

theorem parameterQ_norm_ne_zero :
    dot₂ (parameterQ (K := K)) (parameterQ (K := K)) ≠ 0 := by
  intro h
  have heval := congrArg (MvPolynomial.eval (![0, 0, 1, 0] : Fin 4 → K)) h
  simp [dot₂, parameterQ, MvPolynomial.eval_add,
    MvPolynomial.eval_mul, MvPolynomial.eval_X] at heval

/-- Polynomial extension of the generic matrix normal form.  Only the two
wedge identities and off-diagonal divisibilities are hypotheses; all generic
nonzero factors are proved from the independent indeterminates. -/
theorem polynomial_normal_form
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    (h₀₁ : parameterP (K := K) 0 * parameterQ (K := K) 1 ∣ M 0 1)
    (h₁₀ : parameterP (K := K) 1 * parameterQ (K := K) 0 ∣ M 1 0)
    (hP : cross₂ (parameterP (K := K)) (M *ᵥ parameterP (K := K)) = 0)
    (hQ : cross₂ (parameterQ (K := K)) (Mᵀ *ᵥ parameterQ (K := K)) = 0) :
    ∃ a b : MvPolynomial (Fin 4) K,
      M = a • (1 : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) +
        b • Matrix.vecMulVec (parameterP (K := K)) (parameterQ (K := K)) := by
  obtain ⟨b, hb⟩ := h₀₁
  obtain ⟨b', hb'⟩ := h₁₀
  obtain ⟨_, a, ha⟩ := normal_form_of_wedges_and_divisibility
    parameterP_product_ne_zero parameterQ_product_ne_zero parameter_dot_ne_zero
    hb hb' hP hQ
  exact ⟨a, b, ha⟩

/-- Independent indeterminates make the polynomial coefficients unique. -/
theorem polynomial_normal_form_unique
    {a b a' b' : MvPolynomial (Fin 4) K}
    (h : a • (1 : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) +
        b • Matrix.vecMulVec (parameterP (K := K)) (parameterQ (K := K)) =
      a' • (1 : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) +
        b' • Matrix.vecMulVec (parameterP (K := K)) (parameterQ (K := K))) :
    a = a' ∧ b = b' := by
  exact scalar_outer_coefficients_unique
    (mul_ne_zero (MvPolynomial.X_ne_zero 0) (MvPolynomial.X_ne_zero 3)) h

end IndependentParameters

noncomputable section PolynomialCovariance

variable {K : Type*} [Field K]

/-- Evaluation assignment corresponding to a pair of two-dimensional columns. -/
def columnAssignment (P Q : Fin 2 → K) : Fin 4 → K :=
  ![P 0, P 1, Q 0, Q 1]

/-- Evaluate every entry of the polynomial matrix at two parameter columns. -/
def evalAtColumns (M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K))
    (P Q : Fin 2 → K) : Matrix (Fin 2) (Fin 2) K :=
  fun i j => MvPolynomial.eval (columnAssignment P Q) (M i j)

omit [Field K] in
theorem columnAssignment_recover (z : Fin 4 → K) :
    columnAssignment ![z 0, z 1] ![z 2, z 3] = z := by
  ext i
  fin_cases i <;> rfl

/-- Evaluation commutes with the right wedge expression. -/
theorem eval_right_wedge
    (M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) (z : Fin 4 → K) :
    MvPolynomial.eval z (cross₂ (parameterP (K := K))
      (M *ᵥ parameterP (K := K))) =
      cross₂ ![z 0, z 1] (evalAtColumns M ![z 0, z 1] ![z 2, z 3] *ᵥ ![z 0, z 1]) := by
  simp [cross₂, parameterP, Matrix.mulVec, dotProduct, Fin.sum_univ_two,
    evalAtColumns, columnAssignment_recover, map_sub, map_add, map_mul,
    MvPolynomial.eval_X]

/-- Evaluation commutes with the left wedge expression. -/
theorem eval_left_wedge
    (M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) (z : Fin 4 → K) :
    MvPolynomial.eval z (cross₂ (parameterQ (K := K))
      (Mᵀ *ᵥ parameterQ (K := K))) =
      cross₂ ![z 2, z 3] ((evalAtColumns M ![z 0, z 1] ![z 2, z 3])ᵀ *ᵥ ![z 2, z 3]) := by
  simp [cross₂, parameterQ, Matrix.mulVec, dotProduct, Fin.sum_univ_two,
    evalAtColumns, columnAssignment_recover, map_sub, map_add, map_mul,
    MvPolynomial.eval_X]

/-- The concrete orthogonal covariance required by the replica matrix step.
This property is a hypothesis, not a formalization of the physical tensor
construction producing the matrix. -/
def OrthogonalCovariant
    (M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) : Prop :=
  ∀ (O : Matrix (Fin 2) (Fin 2) K) (P Q : Fin 2 → K), Oᵀ * O = 1 →
    evalAtColumns M (O *ᵥ P) (O *ᵥ Q) = O * evalAtColumns M P Q * Oᵀ

theorem evalAtColumns_transverse_right_zero
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    (h₀₁ : parameterP (K := K) 0 * parameterQ (K := K) 1 ∣ M 0 1)
    {P Q : Fin 2 → K} (hp : P 0 = 0) : evalAtColumns M P Q 0 1 = 0 := by
  obtain ⟨b, hb⟩ := h₀₁
  simp [evalAtColumns, hb, parameterP, parameterQ, columnAssignment, hp,
    MvPolynomial.eval_mul, MvPolynomial.eval_X]

theorem evalAtColumns_transverse_left_zero
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    (h₁₀ : parameterP (K := K) 1 * parameterQ (K := K) 0 ∣ M 1 0)
    {P Q : Fin 2 → K} (hq : Q 0 = 0) : evalAtColumns M P Q 1 0 = 0 := by
  obtain ⟨b, hb⟩ := h₁₀
  simp [evalAtColumns, hb, parameterP, parameterQ, columnAssignment, hq,
    MvPolynomial.eval_mul, MvPolynomial.eval_X]

variable [IsAlgClosed K]

theorem evaluated_right_wedge_zero
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    (hcov : OrthogonalCovariant M)
    (h₀₁ : parameterP (K := K) 0 * parameterQ (K := K) 1 ∣ M 0 1)
    {P Q : Fin 2 → K} (hnorm : dot₂ P P ≠ 0) :
    cross₂ P (evalAtColumns M P Q *ᵥ P) = 0 := by
  obtain ⟨s, hsq⟩ := IsAlgClosed.exists_pow_nat_eq (dot₂ P P) zero_lt_two
  have hs : s ≠ 0 := by
    intro hs
    apply hnorm
    rw [← hsq, hs]
    simp
  apply cross₂_eq_zero_of_adapted_frame hs
    (hcov (adaptedFrame P s) P Q (adaptedFrame_orthogonal hs hsq))
  exact evalAtColumns_transverse_right_zero h₀₁ adaptedFrame_first_coordinate

theorem evaluated_left_wedge_zero
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    (hcov : OrthogonalCovariant M)
    (h₁₀ : parameterP (K := K) 1 * parameterQ (K := K) 0 ∣ M 1 0)
    {P Q : Fin 2 → K} (hnorm : dot₂ Q Q ≠ 0) :
    cross₂ Q ((evalAtColumns M P Q)ᵀ *ᵥ Q) = 0 := by
  obtain ⟨s, hsq⟩ := IsAlgClosed.exists_pow_nat_eq (dot₂ Q Q) zero_lt_two
  have hs : s ≠ 0 := by
    intro hs
    apply hnorm
    rw [← hsq, hs]
    simp
  have hrot := hcov (adaptedFrame Q s) P Q (adaptedFrame_orthogonal hs hsq)
  have ht : (evalAtColumns M (adaptedFrame Q s *ᵥ P)
      (adaptedFrame Q s *ᵥ Q))ᵀ =
      adaptedFrame Q s * (evalAtColumns M P Q)ᵀ * (adaptedFrame Q s)ᵀ := by
    rw [hrot]
    simp [Matrix.transpose_mul, Matrix.mul_assoc]
  apply cross₂_eq_zero_of_adapted_frame hs ht
  exact evalAtColumns_transverse_left_zero h₁₀ adaptedFrame_first_coordinate

/-- Orthogonal covariance and right off-diagonal divisibility imply the right
wedge as an identity of polynomials, including isotropic parameter values. -/
theorem polynomial_right_wedge_zero
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    (hcov : OrthogonalCovariant M)
    (h₀₁ : parameterP (K := K) 0 * parameterQ (K := K) 1 ∣ M 0 1) :
    cross₂ (parameterP (K := K)) (M *ᵥ parameterP (K := K)) = 0 := by
  have hprod : dot₂ (parameterP (K := K)) (parameterP (K := K)) *
      cross₂ (parameterP (K := K)) (M *ᵥ parameterP (K := K)) = 0 := by
    apply MvPolynomial.funext
    intro z
    rw [map_zero, map_mul, eval_right_wedge]
    have hnormeval : MvPolynomial.eval z
        (dot₂ (parameterP (K := K)) (parameterP (K := K))) =
        dot₂ ![z 0, z 1] ![z 0, z 1] := by
      simp [dot₂, parameterP, map_add, map_mul, MvPolynomial.eval_X]
    rw [hnormeval]
    by_cases hn : dot₂ ![z 0, z 1] ![z 0, z 1] = 0
    · rw [hn, zero_mul]
    · rw [evaluated_right_wedge_zero hcov h₀₁ hn, mul_zero]
  exact (mul_eq_zero.mp hprod).resolve_left parameterP_norm_ne_zero

/-- The corresponding left polynomial wedge identity. -/
theorem polynomial_left_wedge_zero
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    (hcov : OrthogonalCovariant M)
    (h₁₀ : parameterP (K := K) 1 * parameterQ (K := K) 0 ∣ M 1 0) :
    cross₂ (parameterQ (K := K)) (Mᵀ *ᵥ parameterQ (K := K)) = 0 := by
  have hprod : dot₂ (parameterQ (K := K)) (parameterQ (K := K)) *
      cross₂ (parameterQ (K := K)) (Mᵀ *ᵥ parameterQ (K := K)) = 0 := by
    apply MvPolynomial.funext
    intro z
    rw [map_zero, map_mul, eval_left_wedge]
    have hnormeval : MvPolynomial.eval z
        (dot₂ (parameterQ (K := K)) (parameterQ (K := K))) =
        dot₂ ![z 2, z 3] ![z 2, z 3] := by
      simp [dot₂, parameterQ, map_add, map_mul, MvPolynomial.eval_X]
    rw [hnormeval]
    by_cases hn : dot₂ ![z 2, z 3] ![z 2, z 3] = 0
    · rw [hn, zero_mul]
    · rw [evaluated_left_wedge_zero hcov h₁₀ hn, mul_zero]
  exact (mul_eq_zero.mp hprod).resolve_left parameterQ_norm_ne_zero

/-- The complete algebraic covariance-to-normal-form step.  A concrete
orthogonally covariant polynomial matrix with the two indicated transverse
divisibilities is a polynomial scalar matrix plus a polynomial outer product.
No generic-point, nonisotropic-point, or rational-function hypothesis remains. -/
theorem polynomial_normal_form_of_covariance
    {M : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    (hcov : OrthogonalCovariant M)
    (h₀₁ : parameterP (K := K) 0 * parameterQ (K := K) 1 ∣ M 0 1)
    (h₁₀ : parameterP (K := K) 1 * parameterQ (K := K) 0 ∣ M 1 0) :
    ∃ a b : MvPolynomial (Fin 4) K,
      M = a • (1 : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) +
        b • Matrix.vecMulVec (parameterP (K := K)) (parameterQ (K := K)) := by
  exact polynomial_normal_form h₀₁ h₁₀
    (polynomial_right_wedge_zero hcov h₀₁) (polynomial_left_wedge_zero hcov h₁₀)

end PolynomialCovariance

end KrennAllOrders.ReplicaCovariance
