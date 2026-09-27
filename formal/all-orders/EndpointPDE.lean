import GramInvariants
import PolynomialODE

/-!
# Coordinate boundary equations imply the finite endpoint identity

This module proves the chain rule, axis cancellation, and finite polynomial ODE
steps in the supported-edge argument.  The two coordinate boundary identities
remain explicit premises; their construction from the physical matching source
belongs to the source/replica modules.

The Cartesian variables are `(P₀,P₁,Q₀,Q₁)`, and the Gram variables are
`(σ,τ,c)`.  In particular, this file never assumes a Gram-coordinate ODE.
-/

set_option autoImplicit false
set_option relaxedAutoImplicit false

namespace KrennAllOrders.EndpointPDE

open MvPolynomial
open KrennAllOrders.GramInvariants

noncomputable section ChainRule

variable {K : Type*} [Field K]

/-- Restrict the Gram substitution to the axis `Q₀=0`. -/
theorem axisRestriction_gramMap (p : MvPolynomial (Fin 3) K) :
    axisRestriction (gramMap p) = axisGramMap p :=
  DFunLike.congr_fun axisRestriction_comp_gramMap p

/-- Gram substitution takes the Cartesian origin to the Gram origin. -/
theorem eval_zero_gramMap (p : MvPolynomial (Fin 3) K) :
    MvPolynomial.eval (0 : Fin 4 → K) (gramMap p) =
      MvPolynomial.eval (0 : Fin 3 → K) p := by
  change MvPolynomial.eval (0 : Fin 4 → K) (MvPolynomial.eval₂ C _ p) = _
  rw [← MvPolynomial.eval_assoc]
  have hassign : MvPolynomial.eval (0 : Fin 4 → K) ∘
      ![KrennAllOrders.ReplicaCovariance.dot₂
          (KrennAllOrders.ReplicaCovariance.parameterP (K := K))
          (KrennAllOrders.ReplicaCovariance.parameterP (K := K)),
        KrennAllOrders.ReplicaCovariance.dot₂
          (KrennAllOrders.ReplicaCovariance.parameterQ (K := K))
          (KrennAllOrders.ReplicaCovariance.parameterQ (K := K)),
        KrennAllOrders.ReplicaCovariance.dot₂
          (KrennAllOrders.ReplicaCovariance.parameterP (K := K))
          (KrennAllOrders.ReplicaCovariance.parameterQ (K := K))] =
      (0 : Fin 3 → K) := by
    funext i
    fin_cases i <;>
      simp [KrennAllOrders.ReplicaCovariance.dot₂,
        KrennAllOrders.ReplicaCovariance.parameterP,
        KrennAllOrders.ReplicaCovariance.parameterQ]
  rw [hassign]

@[simp] theorem axisRestriction_C (a : K) :
    axisRestriction (C a) = (C a : MvPolynomial (Fin 3) K) := by
  simp [axisRestriction]

@[simp] theorem axisRestriction_X (i : Fin 4) :
    axisRestriction (X i) = (![X 0, X 1, 0, X 2] i : MvPolynomial (Fin 3) K) := by
  simp [axisRestriction]

@[simp] theorem axisGramMap_C (a : K) :
    axisGramMap (C a) = (C a : MvPolynomial (Fin 3) K) := by
  simp [axisGramMap]

/-- Exact normal chain rule on the `Q₀=0` axis: the `τ` contribution vanishes,
and the `c` contribution is multiplied by `P₀`. -/
theorem axisRestriction_pderiv_gramMap (p : MvPolynomial (Fin 3) K) :
    axisRestriction (pderiv 2 (gramMap p)) =
      X 0 * axisGramMap (pderiv 2 p) := by
  induction p using MvPolynomial.induction_on with
  | C a => simp [gramMap, axisGramMap, axisRestriction]
  | add p q hp hq => simp [hp, hq, mul_add]
  | mul_X p j hp =>
    simp only [map_mul, pderiv_mul, map_add, hp, axisRestriction_gramMap]
    fin_cases j <;>
      simp [gramMap, axisGramMap, axisRestriction,
        KrennAllOrders.ReplicaCovariance.dot₂,
        KrennAllOrders.ReplicaCovariance.parameterP,
        KrennAllOrders.ReplicaCovariance.parameterQ, pderiv_X]
    all_goals ring

/-- The exact axis chain rule for the off-diagonal entry `P₀ Q₁ b(σ,τ,c)`. -/
theorem axisRestriction_offDiagonal_derivative (b : MvPolynomial (Fin 3) K) :
    axisRestriction (pderiv 2 (X 0 * X 3 * gramMap b)) =
      X 0 ^ 2 * X 2 * axisGramMap (pderiv 2 b) := by
  simp only [pderiv_mul, pderiv_X, Pi.single_apply]
  simp only [show (0 : Fin 4) ≠ 2 by decide, show (3 : Fin 4) ≠ 2 by decide,
    ite_false, zero_mul, mul_zero, add_zero, zero_add]
  rw [map_mul, map_mul, axisRestriction_pderiv_gramMap]
  simp only [axisRestriction_X, Matrix.cons_val_zero, Matrix.cons_val_three]
  dsimp [Matrix.vecHead, Matrix.vecTail]
  ring

end ChainRule

noncomputable section Univariate

variable {K : Type*} [Field K]

/-- Treat `c` as the univariate variable, with the two other Gram variables
in the coefficient ring.  This is an actual algebra equivalence. -/
def cPolynomialEquiv : MvPolynomial (Fin 3) K ≃ₐ[K]
    Polynomial (MvPolynomial (Fin 2) K) :=
  (renameEquiv K (Equiv.swap (0 : Fin 3) 2)).trans (finSuccEquiv K 2)

theorem cPolynomialEquiv_C (a : K) :
    cPolynomialEquiv (C a) = Polynomial.C (C a) := by
  simp [cPolynomialEquiv, renameEquiv_apply, finSuccEquiv_apply]

theorem cPolynomialEquiv_X (j : Fin 3) :
    cPolynomialEquiv (X j) =
      (![Polynomial.C (X 1), Polynomial.C (X 0), Polynomial.X] j :
        Polynomial (MvPolynomial (Fin 2) K)) := by
  fin_cases j <;>
    simp [cPolynomialEquiv, renameEquiv_apply, finSuccEquiv_apply, Equiv.swap_apply_def]
  all_goals rfl

/-- The `c` partial derivative becomes the ordinary polynomial derivative. -/
theorem cPolynomialEquiv_pderiv (p : MvPolynomial (Fin 3) K) :
    cPolynomialEquiv (pderiv 2 p) =
      Polynomial.derivative (cPolynomialEquiv p) := by
  induction p using MvPolynomial.induction_on with
  | C a => simp [cPolynomialEquiv_C]
  | add p q hp hq => simp [hp, hq]
  | mul_X p j hp =>
    simp only [pderiv_mul, map_add, map_mul, hp, Polynomial.derivative_mul,
      cPolynomialEquiv_X]
    fin_cases j <;> simp [pderiv_X]

/-- A finite Gram polynomial satisfying the homogeneous `c` ODE is zero.
The coefficient ring is genuinely `K[σ,τ]`. -/
theorem eq_zero_of_c_ode {b : MvPolynomial (Fin 3) K} {d : K}
    (hd : d ≠ 0) (h : pderiv 2 b + C d * b = 0) : b = 0 := by
  apply cPolynomialEquiv.injective
  rw [map_zero]
  apply KrennAllOrders.eq_zero_of_derivative_add_C_mul_eq_zero (C_ne_zero.mpr hd)
  simpa only [map_add, map_mul, cPolynomialEquiv_C, cPolynomialEquiv_pderiv,
    map_zero] using congrArg cPolynomialEquiv h

/-- A finite Gram polynomial satisfying the inhomogeneous `c` ODE is the
constant `k/d`, independent of all three Gram variables. -/
theorem eq_C_div_of_c_ode {a : MvPolynomial (Fin 3) K} {d k : K}
    (hd : d ≠ 0) (h : pderiv 2 a + C d * a = C k) : a = C (k / d) := by
  apply cPolynomialEquiv.injective
  rw [cPolynomialEquiv_C]
  apply KrennAllOrders.eq_C_of_derivative_add_C_mul_eq_C_mul (C_ne_zero.mpr hd)
  have hdk : d * (k / d) = k := by field_simp
  have h' := congrArg cPolynomialEquiv h
  simp only [map_add, map_mul, cPolynomialEquiv_C, cPolynomialEquiv_pderiv] at h'
  simpa only [← Polynomial.C_mul, ← map_mul, hdk] using h'

end Univariate

noncomputable section Boundary

variable {K : Type*} [Field K] [IsAlgClosed K]

/-- The explicit coordinate boundary equation for the off-diagonal coefficient.
It is an equation of finite polynomials on the `Q₀=0` axis. -/
def OffDiagonalBoundary (b : MvPolynomial (Fin 3) K) (d : K) : Prop :=
  axisRestriction (pderiv 2 (X 0 * X 3 * gramMap b) +
    C d * X 0 * (X 0 * X 3 * gramMap b)) = 0

/-- The coordinate boundary equation for the scalar coefficient once the
off-diagonal coefficient has vanished. -/
def ScalarBoundary (a : MvPolynomial (Fin 3) K) (d k : K) : Prop :=
  axisRestriction (pderiv 2 (gramMap a) + C d * X 0 * gramMap a -
    C k * X 0) = 0

/-- Chain rule, integral-domain cancellation, and injectivity of the axis Gram
map turn the off-diagonal coordinate boundary into the actual `c` ODE. -/
theorem c_ode_of_offDiagonalBoundary {b : MvPolynomial (Fin 3) K} {d : K}
    (h : OffDiagonalBoundary b d) : pderiv 2 b + C d * b = 0 := by
  have hp : X 0 ^ 2 * X 2 * axisGramMap (pderiv 2 b + C d * b) = 0 := by
    have h' := h
    unfold OffDiagonalBoundary at h'
    rw [map_add, axisRestriction_offDiagonal_derivative] at h'
    simp only [map_mul, axisRestriction_C, axisRestriction_X,
      axisRestriction_gramMap, Matrix.cons_val_zero, Matrix.cons_val_three] at h'
    dsimp [Matrix.vecHead, Matrix.vecTail] at h'
    simp only [map_add, map_mul, axisGramMap_C]
    convert h' using 1; ring
  have hz : axisGramMap (pderiv 2 b + C d * b) = 0 :=
    (mul_eq_zero.mp hp).resolve_left (mul_ne_zero (pow_ne_zero _ (X_ne_zero 0))
      (X_ne_zero 2))
  exact axisGramMap_injective (hz.trans (map_zero axisGramMap).symm)

/-- The off-diagonal coefficient vanishes for a supported nonzero endpoint. -/
theorem offDiagonal_eq_zero {b : MvPolynomial (Fin 3) K} {d : K}
    (hd : d ≠ 0) (h : OffDiagonalBoundary b d) : b = 0 :=
  eq_zero_of_c_ode hd (c_ode_of_offDiagonalBoundary h)

/-- The scalar coordinate boundary yields the inhomogeneous Gram ODE. -/
theorem c_ode_of_scalarBoundary {a : MvPolynomial (Fin 3) K} {d k : K}
    (h : ScalarBoundary a d k) : pderiv 2 a + C d * a = C k := by
  have hp : X 0 * axisGramMap (pderiv 2 a + C d * a - C k) = 0 := by
    have h' := h
    unfold ScalarBoundary at h'
    rw [map_sub, map_add, axisRestriction_pderiv_gramMap] at h'
    simp only [map_mul, axisRestriction_C, axisRestriction_X,
      axisRestriction_gramMap, Matrix.cons_val_zero] at h'
    simp only [map_sub, map_add, map_mul, axisGramMap_C]
    convert h' using 1; ring
  have hz : axisGramMap (pderiv 2 a + C d * a - C k) = 0 :=
    (mul_eq_zero.mp hp).resolve_left (X_ne_zero 0)
  exact sub_eq_zero.mp (axisGramMap_injective
    (hz.trans (map_zero axisGramMap).symm))

/-- The coordinate boundary equation forces the scalar coefficient to be a
constant in every Gram variable. -/
theorem scalar_eq_constant {a : MvPolynomial (Fin 3) K} {d k : K}
    (hd : d ≠ 0) (h : ScalarBoundary a d k) : a = C (k / d) :=
  eq_C_div_of_c_ode hd (c_ode_of_scalarBoundary h)

/-- Supported-edge endpoint identity, derived from the explicit coordinate
boundary equation and the value at the origin. -/
theorem endpoint_of_scalarBoundary {a : MvPolynomial (Fin 3) K} {d β η α : K}
    (hd : d ≠ 0) (hη : η ≠ 0) (h : ScalarBoundary a d (β * η))
    (hzero : MvPolynomial.eval (0 : Fin 3 → K) a = η * α) : β = d * α := by
  have ha := scalar_eq_constant hd h
  have hconst : β * η / d = η * α := by simpa [ha] using hzero
  apply mul_right_cancel₀ hη
  have hprod := (div_eq_iff hd).mp hconst
  simpa [mul_assoc, mul_comm, mul_left_comm] using hprod

end Boundary

noncomputable section MatrixEndpoint

open KrennAllOrders.ReplicaCovariance
open scoped Matrix

variable {K : Type*} [Field K] [IsAlgClosed K] [CharZero K]

/-- The first source boundary identity, expressed directly for a matrix entry
before choosing its unique normal-form coefficients. -/
def MatrixOffDiagonalBoundary
    (T : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) (d : K) : Prop :=
  axisRestriction (pderiv 2 (T 0 1) + C d * X 0 * T 0 1) = 0

/-- The second source boundary identity, expressed directly for a diagonal
matrix entry.  No Gram-coordinate derivative is assumed. -/
def MatrixScalarBoundary
    (T : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)) (d k : K) : Prop :=
  axisRestriction (pderiv 2 (T 1 1) + C d * X 0 * T 1 1 - C k * X 0) = 0

omit [IsAlgClosed K] [CharZero K] in
/-- The off-diagonal coordinate identity transfers to the normal-form
coefficient by an exact entry computation. -/
theorem offDiagonalBoundary_of_matrix_normal_form
    {T : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    {a b : MvPolynomial (Fin 3) K} {d : K}
    (ht : T = gramMap a • 1 + gramMap b • Matrix.vecMulVec parameterP parameterQ)
    (h : MatrixOffDiagonalBoundary T d) : OffDiagonalBoundary b d := by
  have hentry : T 0 1 = X 0 * X 3 * gramMap b := by
    rw [ht]
    simp [Matrix.vecMulVec, parameterP, parameterQ]
    ring
  simpa only [MatrixOffDiagonalBoundary, hentry, OffDiagonalBoundary] using h

omit [IsAlgClosed K] [CharZero K] in
/-- With the off-diagonal coefficient eliminated, the second coordinate
boundary is exactly the scalar coefficient boundary. -/
theorem scalarBoundary_of_matrix_normal_form
    {T : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)}
    {a b : MvPolynomial (Fin 3) K} {d k : K}
    (ht : T = gramMap a • 1 + gramMap b • Matrix.vecMulVec parameterP parameterQ)
    (hb : b = 0) (h : MatrixScalarBoundary T d k) : ScalarBoundary a d k := by
  have hentry : T 1 1 = gramMap a := by simp [ht, hb]
  simpa only [MatrixScalarBoundary, hentry, ScalarBoundary] using h

/-- The complete algebraic endpoint step.  Covariance and off-diagonal
divisibility produce the Gram normal form; the two Cartesian boundary
identities force its homogeneous coefficient to vanish and its scalar
coefficient to be constant.  Physical-source identities are explicit premises.
-/
theorem endpoint_of_covariant_matrix_boundaries
    {T : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin 4) K)} {d β η α : K}
    (hd : d ≠ 0) (hη : η ≠ 0)
    (hcov : OrthogonalCovariant T)
    (h₀₁ : parameterP (K := K) 0 * parameterQ (K := K) 1 ∣ T 0 1)
    (h₁₀ : parameterP (K := K) 1 * parameterQ (K := K) 0 ∣ T 1 0)
    (hoff : MatrixOffDiagonalBoundary T d)
    (hscalar : MatrixScalarBoundary T d (β * η))
    (horigin : MvPolynomial.eval (0 : Fin 4 → K) (T 1 1) = η * α) :
    β = d * α := by
  obtain ⟨a, b, ht⟩ := orthogonal_covariant_gram_normal_form hcov h₀₁ h₁₀
  have hb : b = 0 := offDiagonal_eq_zero hd
    (offDiagonalBoundary_of_matrix_normal_form ht hoff)
  apply endpoint_of_scalarBoundary hd hη
    (scalarBoundary_of_matrix_normal_form ht hb hscalar)
  have hentry : T 1 1 = gramMap a := by simp [ht, hb]
  rw [hentry] at horigin
  simpa only [eval_zero_gramMap] using horigin

end MatrixEndpoint

end KrennAllOrders.EndpointPDE
