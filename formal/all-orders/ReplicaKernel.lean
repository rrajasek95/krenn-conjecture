import EndpointPDE
import Mathlib.Algebra.MvPolynomial.PDeriv

/-!
# The literal finite two-replica kernel

Tensor components are finite scalar polynomials in the four mean coordinates
`x,y,u,v`.  The scalar kernel is constructed by a bilinear contraction of two
copies; its matrix entries are literal partial derivatives, followed by setting
the auxiliary `u,v` columns to zero.  Source boundary identities and scalar
kernel covariance remain explicit inputs until the physical-source bridge.
-/

set_option autoImplicit false
set_option relaxedAutoImplicit false

namespace KrennAllOrders.ReplicaKernel

open MvPolynomial
open scoped BigOperators Matrix
open KrennAllOrders.ReplicaCovariance
open KrennAllOrders.GramInvariants
open KrennAllOrders.EndpointPDE

noncomputable section Substitution

variable {K σ τ : Type*} [CommRing K] [Fintype σ]

/-- A finite polynomial chain rule for an arbitrary polynomial substitution. -/
theorem pderiv_substitution (f : σ → MvPolynomial τ K)
    (p : MvPolynomial σ K) (j : τ) :
    pderiv j (eval₂Hom C f p) =
      ∑ i : σ, eval₂Hom C f (pderiv i p) * pderiv j (f i) := by
  classical
  induction p using MvPolynomial.induction_on with
  | C a => simp
  | add p q hp hq =>
    simp only [map_add, hp, hq, add_mul, Finset.sum_add_distrib]
  | mul_X p n hp =>
    simp only [map_mul, pderiv_mul, hp, eval₂Hom_X', map_add,
      pderiv_X, Pi.single_apply, Finset.sum_add_distrib, add_mul,
      Finset.sum_mul]
    simp only [apply_ite, map_one, map_zero, mul_one, mul_zero, ite_mul, zero_mul]
    rw [Finset.sum_ite_eq]
    simp only [Finset.mem_univ, ite_true]
    congr 1
    apply Finset.sum_congr rfl
    intro i _
    ring

end Substitution

noncomputable section Construction

variable {K ι : Type*} [Field K] [Fintype ι]

abbrev MeanPolynomial (K : Type*) [CommRing K] := MvPolynomial (Fin 4) K
abbrev ReplicaPolynomial (K : Type*) [CommRing K] := MvPolynomial (Fin 4 × Fin 2) K
abbrev CartesianPolynomial (K : Type*) [CommRing K] := MvPolynomial (Fin 4) K

/-- Copy a four-mean polynomial into one of the two replica rows. -/
def meanCopy (i : Fin 2) : MeanPolynomial K →+* ReplicaPolynomial K :=
  eval₂Hom C (fun j => X (j, i))

/-- Set the two auxiliary columns to zero while keeping the `x,y` columns. -/
def zeroAuxiliary : ReplicaPolynomial K →+* CartesianPolynomial K :=
  eval₂Hom C (fun ji => (![parameterP (K := K) ji.2,
    parameterQ (K := K) ji.2, 0, 0] : Fin 4 → CartesianPolynomial K) ji.1)

/-- The literal binary mean substitution in one replica row. -/
def binaryMean (i : Fin 2) : MeanPolynomial K →+* CartesianPolynomial K :=
  eval₂Hom C ![parameterP (K := K) i, parameterQ (K := K) i, 0, 0]

theorem zeroAuxiliary_meanCopy (i : Fin 2) (p : MeanPolynomial K) :
    zeroAuxiliary (meanCopy i p) = binaryMean i p := by
  have hh : zeroAuxiliary.comp (meanCopy (K := K) i) = binaryMean i := by
    apply MvPolynomial.ringHom_ext
    · intro a
      simp [zeroAuxiliary, meanCopy, binaryMean]
    · intro j
      simp [zeroAuxiliary, meanCopy, binaryMean]
  exact DFunLike.congr_fun hh p

/-- A scalar bilinear contraction with literal finite coefficient weights. -/
def contraction {σ : Type*} (κ : ι → ι → K)
    (A B : ι → MvPolynomial σ K) : MvPolynomial σ K :=
  ∑ s : ι, ∑ t : ι, C (κ s t) * A s * B t

/-- The scalar two-replica kernel of the actual tensor polynomial `E`. -/
def kernel (κ : ι → ι → K) (E : ι → MeanPolynomial K) : ReplicaPolynomial K :=
  contraction κ (fun s => meanCopy 0 (E s)) (fun s => meanCopy 1 (E s))

/-- The zero-auxiliary scalar kernel. -/
def scalarKernel (κ : ι → ι → K) (E : ι → MeanPolynomial K) :
    CartesianPolynomial K := zeroAuxiliary (kernel κ E)

/-- Literal mixed auxiliary-column partial derivatives of the scalar kernel. -/
def kernelMatrix (κ : ι → ι → K) (E : ι → MeanPolynomial K) :
    Matrix (Fin 2) (Fin 2) (CartesianPolynomial K) :=
  fun i j => zeroAuxiliary (pderiv (2, i) (pderiv (3, j) (kernel κ E)))

/-- The corrected matrix used by the supported-edge argument. -/
def correctedMatrix (κ : ι → ι → K) (E : ι → MeanPolynomial K) (e : K) :
    Matrix (Fin 2) (Fin 2) (CartesianPolynomial K) :=
  kernelMatrix κ E + (C e * scalarKernel κ E) • 1

theorem pderiv_meanCopy (r : Fin 4) (k i : Fin 2) (p : MeanPolynomial K) :
    pderiv (r, k) (meanCopy i p) =
      if k = i then meanCopy i (pderiv r p) else 0 := by
  classical
  rw [meanCopy, pderiv_substitution]
  simp only [pderiv_X, Pi.single_apply, Prod.mk.injEq]
  by_cases hi : k = i
  · subst k
    simp [and_true, eq_comm]
  · simp [hi, Ne.symm hi]

theorem pderiv_contraction {σ : Type*} (κ : ι → ι → K)
    (A B : ι → MvPolynomial σ K) (j : σ) :
    pderiv j (contraction κ A B) =
      contraction κ (fun s => pderiv j (A s)) B +
        contraction κ A (fun s => pderiv j (B s)) := by
  simp only [contraction, map_sum, pderiv_mul, pderiv_C, zero_mul, zero_add,
    Finset.sum_add_distrib]

theorem map_contraction {σ τ : Type*} (f : MvPolynomial σ K →+* MvPolynomial τ K)
    (hf : ∀ a, f (C a) = C a) (κ : ι → ι → K)
    (A B : ι → MvPolynomial σ K) :
    f (contraction κ A B) = contraction κ (fun s => f (A s)) (fun s => f (B s)) := by
  simp only [contraction, map_sum, map_mul, hf]

@[simp] theorem contraction_zero_left {σ : Type*} (κ : ι → ι → K)
    (B : ι → MvPolynomial σ K) : contraction κ (fun _ => 0) B = 0 := by
  simp [contraction]

@[simp] theorem contraction_zero_right {σ : Type*} (κ : ι → ι → K)
    (A : ι → MvPolynomial σ K) : contraction κ A (fun _ => 0) = 0 := by
  simp [contraction]

@[simp] theorem zeroAuxiliary_C (a : K) :
    zeroAuxiliary (C a) = (C a : CartesianPolynomial K) := by
  simp [zeroAuxiliary]

/-- An off-diagonal matrix entry is the contraction of one `u` derivative and
one `v` derivative in different replica rows. -/
theorem kernelMatrix_zero_one (κ : ι → ι → K) (E : ι → MeanPolynomial K) :
    kernelMatrix κ E 0 1 = contraction κ
      (fun s => binaryMean 0 (pderiv 2 (E s)))
      (fun s => binaryMean 1 (pderiv 3 (E s))) := by
  unfold kernelMatrix kernel
  simp only [pderiv_contraction, pderiv_meanCopy, ite_true,
    show (1 : Fin 2) ≠ 0 by decide, show (0 : Fin 2) ≠ 1 by decide, ite_false,
    contraction_zero_left, contraction_zero_right, zero_add, add_zero]
  rw [map_contraction zeroAuxiliary zeroAuxiliary_C]
  simp only [zeroAuxiliary_meanCopy]

/-- The diagonal `11` entry differentiates the second tensor twice. -/
theorem kernelMatrix_one_one (κ : ι → ι → K) (E : ι → MeanPolynomial K) :
    kernelMatrix κ E 1 1 = contraction κ
      (fun s => binaryMean 0 (E s))
      (fun s => binaryMean 1 (pderiv 2 (pderiv 3 (E s)))) := by
  unfold kernelMatrix kernel
  simp only [pderiv_contraction, pderiv_meanCopy, ite_true,
    show (1 : Fin 2) ≠ 0 by decide, ite_false, contraction_zero_left, zero_add]
  rw [map_contraction zeroAuxiliary zeroAuxiliary_C]
  simp only [zeroAuxiliary_meanCopy]

theorem scalarKernel_eq (κ : ι → ι → K) (E : ι → MeanPolynomial K) :
    scalarKernel κ E = contraction κ (fun s => binaryMean 0 (E s))
      (fun s => binaryMean 1 (E s)) := by
  simp only [scalarKernel, kernel, contraction, map_sum, map_mul,
    zeroAuxiliary_meanCopy]
  simp [zeroAuxiliary]

theorem contraction_add_left {σ : Type*} (κ : ι → ι → K)
    (A B D : ι → MvPolynomial σ K) :
    contraction κ (fun s => A s + B s) D =
      contraction κ A D + contraction κ B D := by
  simp [contraction, add_mul, mul_add, Finset.sum_add_distrib]

theorem contraction_add_right {σ : Type*} (κ : ι → ι → K)
    (A B D : ι → MvPolynomial σ K) :
    contraction κ A (fun s => B s + D s) =
      contraction κ A B + contraction κ A D := by
  simp [contraction, mul_add, Finset.sum_add_distrib]

theorem contraction_mul_left {σ : Type*} (κ : ι → ι → K)
    (A B : ι → MvPolynomial σ K) (c : MvPolynomial σ K) :
    contraction κ (fun s => c * A s) B = c * contraction κ A B := by
  simp only [contraction, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro s _
  apply Finset.sum_congr rfl
  intro t _
  ring

theorem contraction_mul_right {σ : Type*} (κ : ι → ι → K)
    (A B : ι → MvPolynomial σ K) (c : MvPolynomial σ K) :
    contraction κ A (fun s => c * B s) = c * contraction κ A B := by
  simp only [contraction, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro s _
  apply Finset.sum_congr rfl
  intro t _
  ring

theorem correctedMatrix_zero_one (κ : ι → ι → K)
    (E : ι → MeanPolynomial K) (e : K) :
    correctedMatrix κ E e 0 1 = kernelMatrix κ E 0 1 := by
  simp [correctedMatrix]

theorem correctedMatrix_one_one (κ : ι → ι → K)
    (E : ι → MeanPolynomial K) (e : K) :
    correctedMatrix κ E e 1 1 = contraction κ
      (fun s => binaryMean 0 (E s))
      (fun s => binaryMean 1 (pderiv 2 (pderiv 3 (E s)) + C e * E s)) := by
  simp only [correctedMatrix, Matrix.add_apply, Matrix.smul_apply,
    Matrix.one_apply_eq, smul_eq_mul, mul_one, kernelMatrix_one_one,
    scalarKernel_eq, map_add, map_mul]
  have hc : binaryMean (K := K) 1 (C e) = C e := by simp [binaryMean]
  rw [hc, contraction_add_right, contraction_mul_right]

end Construction

noncomputable section Covariance

variable {K : Type*} [Field K]

/-- Simultaneously rotate every one of the four mean columns. -/
def replicaFrameAssignment (O : Matrix (Fin 2) (Fin 2) K)
    (ji : Fin 4 × Fin 2) : ReplicaPolynomial K :=
  ∑ k : Fin 2, C (O ji.2 k) * X (ji.1, k)

def replicaFramePullback (O : Matrix (Fin 2) (Fin 2) K) :
    ReplicaPolynomial K →+* ReplicaPolynomial K :=
  eval₂Hom C (replicaFrameAssignment O)

/-- Scalar orthogonal invariance of the constructed two-replica kernel. -/
def KernelInvariant (g : ReplicaPolynomial K) : Prop :=
  ∀ O : Matrix (Fin 2) (Fin 2) K, Oᵀ * O = 1 → replicaFramePullback O g = g

/-- Mixed `u,v` column derivatives of any scalar replica polynomial. -/
def auxiliaryMatrix (g : ReplicaPolynomial K) :
    Matrix (Fin 2) (Fin 2) (CartesianPolynomial K) :=
  fun i j => zeroAuxiliary (pderiv (2, i) (pderiv (3, j) g))

/-- Entrywise pullback of a Cartesian matrix. -/
def matrixFramePullback (O : Matrix (Fin 2) (Fin 2) K)
    (M : Matrix (Fin 2) (Fin 2) (CartesianPolynomial K)) :
    Matrix (Fin 2) (Fin 2) (CartesianPolynomial K) :=
  fun i j => framePullback O (M i j)

theorem pderiv_replicaFrameAssignment (O : Matrix (Fin 2) (Fin 2) K)
    (r s : Fin 4) (k i : Fin 2) :
    pderiv (r, k) (replicaFrameAssignment O (s, i)) =
      if s = r then C (O i k) else 0 := by
  classical
  by_cases hs : s = r
  · subst s
    fin_cases k <;>
      simp [replicaFrameAssignment, Fin.sum_univ_two, pderiv_X]
  · simp [replicaFrameAssignment, pderiv_X, Prod.mk.injEq, hs]

/-- The transpose factors in the differentiated scalar covariance are proved
by the finite polynomial chain rule. -/
theorem pderiv_replicaFramePullback (O : Matrix (Fin 2) (Fin 2) K)
    (r : Fin 4) (k : Fin 2) (g : ReplicaPolynomial K) :
    pderiv (r, k) (replicaFramePullback O g) =
      ∑ i : Fin 2, C (O i k) * replicaFramePullback O (pderiv (r, i) g) := by
  classical
  rw [replicaFramePullback, pderiv_substitution]
  simp only [Fintype.sum_prod_type, pderiv_replicaFrameAssignment]
  rw [Finset.sum_comm]
  simp only [mul_ite, mul_zero, Finset.sum_ite_eq', Finset.mem_univ, ite_true]
  apply Finset.sum_congr rfl
  intro i _
  rw [mul_comm]

/-- Setting auxiliary columns to zero commutes with a simultaneous rotation. -/
theorem zeroAuxiliary_replicaFramePullback (O : Matrix (Fin 2) (Fin 2) K)
    (g : ReplicaPolynomial K) :
    zeroAuxiliary (replicaFramePullback O g) =
      framePullback O (zeroAuxiliary g) := by
  have hh : zeroAuxiliary.comp (replicaFramePullback (K := K) O) =
      (framePullback O).comp zeroAuxiliary := by
    apply MvPolynomial.ringHom_ext
    · intro a
      simp [zeroAuxiliary, replicaFramePullback, framePullback]
    · intro ji
      rcases ji with ⟨r, i⟩
      fin_cases r <;> fin_cases i <;>
        simp [zeroAuxiliary, replicaFramePullback, replicaFrameAssignment,
          framePullback, parameterP, parameterQ, columnAssignment,
          Matrix.mulVec, dotProduct, Fin.sum_univ_two]
  exact DFunLike.congr_fun hh g

/-- Literal differentiation of scalar covariance gives the matrix's
orthogonal conjugation law, with both transpose factors. -/
theorem auxiliaryMatrix_framePullback (O : Matrix (Fin 2) (Fin 2) K)
    (g : ReplicaPolynomial K) :
    auxiliaryMatrix (replicaFramePullback O g) =
      (O.map (C : K →+* CartesianPolynomial K))ᵀ *
        matrixFramePullback O (auxiliaryMatrix g) *
        O.map (C : K →+* CartesianPolynomial K) := by
  apply Matrix.ext
  intro i j
  simp only [auxiliaryMatrix, pderiv_replicaFramePullback, map_sum,
    pderiv_mul, pderiv_C, zero_mul, zero_add, map_mul,
    zeroAuxiliary_C, zeroAuxiliary_replicaFramePullback]
  simp only [matrixFramePullback, auxiliaryMatrix, Matrix.mul_apply, Matrix.transpose_apply, Matrix.map_apply,
    Fin.sum_univ_two]
  ring

/-- Scalar kernel invariance proves the required matrix covariance; it is not
postulated as an extra matrix hypothesis. -/
theorem auxiliaryMatrix_covariant {g : ReplicaPolynomial K}
    (hg : KernelInvariant g) : OrthogonalCovariant (auxiliaryMatrix g) := by
  intro O P Q ho
  have hm := auxiliaryMatrix_framePullback O g
  rw [hg O ho] at hm
  have hoo : O * Oᵀ = 1 := mul_eq_one_comm.mp ho
  have hooC : O.map (C : K →+* CartesianPolynomial K) * (O.map (C : K →+* CartesianPolynomial K))ᵀ = 1 := by
    apply Matrix.ext
    intro i j
    have hij := congrArg (fun A : Matrix (Fin 2) (Fin 2) K => (C (A i j) : CartesianPolynomial K)) hoo
    simpa [Matrix.mul_apply, Matrix.transpose_apply, Matrix.map_apply,
      Matrix.one_apply, apply_ite, Fin.sum_univ_two] using hij
  have hconj : O.map (C : K →+* CartesianPolynomial K) * auxiliaryMatrix g * (O.map (C : K →+* CartesianPolynomial K))ᵀ =
      matrixFramePullback O (auxiliaryMatrix g) := by
    conv_lhs => rw [hm]
    simp only [Matrix.mul_assoc, hooC, Matrix.mul_one]
    rw [← Matrix.mul_assoc, hooC, Matrix.one_mul]
  apply Matrix.ext
  intro i j
  have hij := congrArg (fun A : Matrix (Fin 2) (Fin 2) (CartesianPolynomial K) =>
      MvPolynomial.eval (columnAssignment P Q) (A i j)) hconj.symm
  have hP : (![columnAssignment P Q 0, columnAssignment P Q 1] : Fin 2 → K) = P := by
    funext k
    fin_cases k <;> rfl
  have hQ : (![columnAssignment P Q 2, columnAssignment P Q 3] : Fin 2 → K) = Q := by
    funext k
    fin_cases k <;> rfl
  simpa [matrixFramePullback, evalAtColumns, eval_framePullback, hP, hQ,
    Matrix.mul_apply, Matrix.transpose_apply, Matrix.map_apply, Fin.sum_univ_two] using hij

/-- The restricted scalar kernel is itself an orthogonal invariant. -/
theorem zeroAuxiliary_invariant {g : ReplicaPolynomial K}
    (hg : KernelInvariant g) : OrthogonalInvariant (zeroAuxiliary g) := by
  intro O ho
  rw [← zeroAuxiliary_replicaFramePullback, hg O ho]

theorem evalAtColumns_add
    (M N : Matrix (Fin 2) (Fin 2) (CartesianPolynomial K)) (P Q : Fin 2 → K) :
    evalAtColumns (M + N) P Q = evalAtColumns M P Q + evalAtColumns N P Q := by
  apply Matrix.ext
  intro i j
  simp [evalAtColumns]

theorem evalAtColumns_scalar (f : CartesianPolynomial K) (P Q : Fin 2 → K) :
    evalAtColumns (f • (1 : Matrix (Fin 2) (Fin 2) (CartesianPolynomial K))) P Q =
      MvPolynomial.eval (columnAssignment P Q) f • (1 : Matrix (Fin 2) (Fin 2) K) := by
  apply Matrix.ext
  intro i j
  by_cases hij : i = j
  · simp [evalAtColumns, hij]
  · simp [evalAtColumns, hij]

/-- Adding an invariant scalar multiple of the identity preserves covariance. -/
theorem covariant_add_scalar
    {M : Matrix (Fin 2) (Fin 2) (CartesianPolynomial K)} {f : CartesianPolynomial K}
    (hm : OrthogonalCovariant M) (hf : OrthogonalInvariant f) :
    OrthogonalCovariant (M + f • 1) := by
  intro O P Q ho
  have hoo : O * Oᵀ = 1 := mul_eq_one_comm.mp ho
  have hP : (![columnAssignment P Q 0, columnAssignment P Q 1] : Fin 2 → K) = P := by
    funext k
    fin_cases k <;> rfl
  have hQ : (![columnAssignment P Q 2, columnAssignment P Q 3] : Fin 2 → K) = Q := by
    funext k
    fin_cases k <;> rfl
  have hfeval := congrArg (MvPolynomial.eval (columnAssignment P Q)) (hf O ho)
  rw [eval_framePullback, hP, hQ] at hfeval
  rw [evalAtColumns_add, evalAtColumns_scalar, hm O P Q ho,
    evalAtColumns_add, evalAtColumns_scalar, hfeval]
  simp only [Matrix.mul_add, Matrix.add_mul, Matrix.mul_smul, Matrix.smul_mul,
    Matrix.mul_one, hoo]

variable {ι : Type*} [Fintype ι]

/-- Covariance of the actual corrected kernel matrix follows from invariance
of the actual contracted scalar kernel. -/
theorem correctedMatrix_covariant {κ : ι → ι → K} {E : ι → MeanPolynomial K} {e : K}
    (hg : KernelInvariant (kernel κ E)) : OrthogonalCovariant (correctedMatrix κ E e) := by
  apply covariant_add_scalar (auxiliaryMatrix_covariant hg)
  intro O ho
  have hf := zeroAuxiliary_invariant hg O ho
  change framePullback O (scalarKernel κ E) = scalarKernel κ E at hf
  change framePullback O (C e * scalarKernel κ E) = C e * scalarKernel κ E
  rw [map_mul, hf]
  simp [framePullback]

end Covariance

noncomputable section SourceBoundaries

variable {K ι : Type*} [Field K] [Fintype ι]

def meanXAxis : MeanPolynomial K →+* MeanPolynomial K :=
  eval₂Hom C ![X 0, 0, 0, 0]

def meanYAxis : MeanPolynomial K →+* MeanPolynomial K :=
  eval₂Hom C ![0, X 1, 0, 0]

def meanBinaryProjection : MeanPolynomial K →+* MeanPolynomial K :=
  eval₂Hom C ![X 0, X 1, 0, 0]

/-- Set a single mean variable to zero. -/
def zeroVariable (i : Fin 4) : MeanPolynomial K →+* MeanPolynomial K :=
  eval₂Hom C (fun j => if j = i then 0 else X j)

/-- Exact polynomial remainder divisibility for restriction to an axis. -/
theorem X_dvd_sub_zeroVariable (i : Fin 4) (p : MeanPolynomial K) :
    X i ∣ p - zeroVariable i p := by
  classical
  induction p using MvPolynomial.induction_on with
  | C a => simp [zeroVariable]
  | add p q hp hq =>
    rw [map_add]
    convert dvd_add hp hq using 1; ring
  | mul_X p j hp =>
    rw [map_mul]
    by_cases hij : j = i
    · subst j
      simp [zeroVariable]
    · have hh := dvd_mul_of_dvd_left hp (X j)
      simpa [zeroVariable, hij, sub_mul] using hh

theorem X_dvd_of_zeroVariable_eq_zero (i : Fin 4) {p : MeanPolynomial K}
    (h : zeroVariable i p = 0) : X i ∣ p := by
  simpa only [h, sub_zero] using X_dvd_sub_zeroVariable i p

theorem zeroVariable_binaryProjection_zero (p : MeanPolynomial K) :
    zeroVariable 0 (meanBinaryProjection p) = meanYAxis p := by
  have hh : (zeroVariable (K := K) 0).comp meanBinaryProjection = meanYAxis := by
    apply MvPolynomial.ringHom_ext
    · intro a
      simp [zeroVariable, meanBinaryProjection, meanYAxis]
    · intro j
      fin_cases j <;> simp [zeroVariable, meanBinaryProjection, meanYAxis]
  exact DFunLike.congr_fun hh p

theorem zeroVariable_binaryProjection_one (p : MeanPolynomial K) :
    zeroVariable 1 (meanBinaryProjection p) = meanXAxis p := by
  have hh : (zeroVariable (K := K) 1).comp meanBinaryProjection = meanXAxis := by
    apply MvPolynomial.ringHom_ext
    · intro a
      simp [zeroVariable, meanBinaryProjection, meanXAxis]
    · intro j
      fin_cases j <;> simp [zeroVariable, meanBinaryProjection, meanXAxis]
  exact DFunLike.congr_fun hh p

theorem binaryMean_binaryProjection (i : Fin 2) (p : MeanPolynomial K) :
    binaryMean i (meanBinaryProjection p) = binaryMean i p := by
  have hh : (binaryMean (K := K) i).comp meanBinaryProjection = binaryMean i := by
    apply MvPolynomial.ringHom_ext
    · intro a
      simp [binaryMean, meanBinaryProjection]
    · intro j
      fin_cases j <;> simp [binaryMean, meanBinaryProjection]
  exact DFunLike.congr_fun hh p

theorem parameterP_dvd_binaryMean (i : Fin 2) {p : MeanPolynomial K}
    (h : meanYAxis p = 0) : parameterP i ∣ binaryMean i p := by
  have hz : zeroVariable 0 (meanBinaryProjection p) = 0 := by
    rw [zeroVariable_binaryProjection_zero, h]
  have hd := map_dvd (binaryMean (K := K) i) (X_dvd_of_zeroVariable_eq_zero 0 hz)
  rw [binaryMean_binaryProjection] at hd
  simpa [binaryMean] using hd

theorem parameterQ_dvd_binaryMean (i : Fin 2) {p : MeanPolynomial K}
    (h : meanXAxis p = 0) : parameterQ i ∣ binaryMean i p := by
  have hz : zeroVariable 1 (meanBinaryProjection p) = 0 := by
    rw [zeroVariable_binaryProjection_one, h]
  have hd := map_dvd (binaryMean (K := K) i) (X_dvd_of_zeroVariable_eq_zero 1 hz)
  rw [binaryMean_binaryProjection] at hd
  simpa [binaryMean] using hd

theorem mul_dvd_contraction {σ : Type*} (κ : ι → ι → K)
    (A B : ι → MvPolynomial σ K) {p q : MvPolynomial σ K}
    (hA : ∀ s, p ∣ A s) (hB : ∀ s, q ∣ B s) : p * q ∣ contraction κ A B := by
  unfold contraction
  apply Finset.dvd_sum
  intro s _
  apply Finset.dvd_sum
  intro t _
  simpa [mul_assoc, mul_comm, mul_left_comm] using
    dvd_mul_of_dvd_right (mul_dvd_mul (hA s) (hB t)) (C (κ s t))

theorem kernelMatrix_one_zero (κ : ι → ι → K) (E : ι → MeanPolynomial K) :
    kernelMatrix κ E 1 0 = contraction κ
      (fun s => binaryMean 0 (pderiv 3 (E s)))
      (fun s => binaryMean 1 (pderiv 2 (E s))) := by
  unfold kernelMatrix kernel
  simp only [pderiv_contraction, pderiv_meanCopy, ite_true,
    show (0 : Fin 2) ≠ 1 by decide, show (1 : Fin 2) ≠ 0 by decide, ite_false,
    contraction_zero_left, contraction_zero_right, zero_add, add_zero]
  rw [map_contraction zeroAuxiliary zeroAuxiliary_C]
  simp only [zeroAuxiliary_meanCopy]

/-- Off-diagonal divisibility is derived from the two source-axis vanishing
identities, not assumed as a property of the constructed matrix. -/
theorem correctedMatrix_offDiagonal_divisibility
    (κ : ι → ι → K) (E : ι → MeanPolynomial K) (e : K)
    (hu : ∀ s, meanYAxis (pderiv 2 (E s)) = 0)
    (hv : ∀ s, meanXAxis (pderiv 3 (E s)) = 0) :
    parameterP (K := K) 0 * parameterQ (K := K) 1 ∣ correctedMatrix κ E e 0 1 ∧
      parameterP (K := K) 1 * parameterQ (K := K) 0 ∣ correctedMatrix κ E e 1 0 := by
  constructor
  · rw [correctedMatrix_zero_one, kernelMatrix_zero_one]
    exact mul_dvd_contraction κ _ _
      (fun s => parameterP_dvd_binaryMean 0 (hu s))
      (fun s => parameterQ_dvd_binaryMean 1 (hv s))
  · have hentry : correctedMatrix κ E e 1 0 = kernelMatrix κ E 1 0 := by
      simp [correctedMatrix]
    rw [hentry, kernelMatrix_one_zero, mul_comm]
    exact mul_dvd_contraction κ _ _
      (fun s => parameterQ_dvd_binaryMean 0 (hv s))
      (fun s => parameterP_dvd_binaryMean 1 (hu s))

/-- Differentiate the full first-row mean polynomial before restricting the
`Q₀` coordinate. -/
theorem pderiv_binaryMean_zero (p : MeanPolynomial K) :
    pderiv 2 (binaryMean 0 p) = binaryMean 0 (pderiv 1 p) := by
  induction p using MvPolynomial.induction_on with
  | C a => simp [binaryMean]
  | add p q hp hq => simp only [map_add, hp, hq]
  | mul_X p j hp =>
    simp only [map_mul, pderiv_mul, map_add, hp]
    fin_cases j <;> simp [binaryMean, parameterP, parameterQ, pderiv_X]

/-- The second-row mean tensor is independent of the first-row `Q₀` parameter. -/
theorem pderiv_binaryMean_one (p : MeanPolynomial K) :
    pderiv 2 (binaryMean 1 p) = 0 := by
  induction p using MvPolynomial.induction_on with
  | C a => simp [binaryMean]
  | add p q hp hq => simp only [map_add, hp, hq, add_zero]
  | mul_X p j hp =>
    simp only [map_mul, pderiv_mul, hp, zero_mul, zero_add]
    fin_cases j <;> simp [binaryMean, parameterP, parameterQ, pderiv_X]

theorem axisRestriction_binaryMean_zero_Xaxis (p : MeanPolynomial K) :
    axisRestriction (binaryMean 0 (meanXAxis p)) = axisRestriction (binaryMean 0 p) := by
  have hh : (axisRestriction (K := K)).comp ((binaryMean 0).comp meanXAxis) =
      axisRestriction.comp (binaryMean 0) := by
    apply MvPolynomial.ringHom_ext
    · intro a
      simp [axisRestriction, binaryMean, meanXAxis]
    · intro j
      fin_cases j <;> simp [axisRestriction, binaryMean, meanXAxis, parameterP, parameterQ]
  exact DFunLike.congr_fun hh p

/-- A scalar contraction of actual tensor coefficients. -/
def scalarContraction (κ : ι → ι → K) (A B : ι → K) : K :=
  ∑ s : ι, ∑ t : ι, κ s t * A s * B t

theorem eval_contraction {σ : Type*} (κ : ι → ι → K)
    (A B : ι → MvPolynomial σ K) (z : σ → K) :
    MvPolynomial.eval z (contraction κ A B) =
      scalarContraction κ (fun s => MvPolynomial.eval z (A s))
        (fun s => MvPolynomial.eval z (B s)) := by
  simp [contraction, scalarContraction]

theorem eval_zero_binaryMean (i : Fin 2) (p : MeanPolynomial K) :
    MvPolynomial.eval (0 : Fin 4 → K) (binaryMean i p) =
      MvPolynomial.eval (0 : Fin 4 → K) p := by
  change MvPolynomial.eval (0 : Fin 4 → K) (eval₂ C _ p) = _
  rw [← MvPolynomial.eval_assoc]
  have hh : MvPolynomial.eval (0 : Fin 4 → K) ∘
      ![parameterP (K := K) i, parameterQ (K := K) i, 0, 0] =
      (0 : Fin 4 → K) := by
    funext j
    fin_cases j <;> fin_cases i <;> simp [parameterP, parameterQ]
  rw [hh]

/-- The origin is computed from the literal tensor coefficients, rather than
postulated as an additional matrix property. -/
theorem correctedMatrix_origin (κ : ι → ι → K)
    (E : ι → MeanPolynomial K) (e : K) :
    MvPolynomial.eval (0 : Fin 4 → K) (correctedMatrix κ E e 1 1) =
      scalarContraction κ (fun s => MvPolynomial.eval (0 : Fin 4 → K) (E s))
        (fun s => MvPolynomial.eval (0 : Fin 4 → K)
          (pderiv 2 (pderiv 3 (E s)) + C e * E s)) := by
  rw [correctedMatrix_one_one, eval_contraction]
  simp only [eval_zero_binaryMean]

@[simp] theorem binaryMean_C (i : Fin 2) (a : K) :
    binaryMean i (C a) = (C a : CartesianPolynomial K) := by simp [binaryMean]

@[simp] theorem binaryMean_X (i : Fin 2) (j : Fin 4) :
    binaryMean i (X j) =
      (![parameterP i, parameterQ i, 0, 0] j : CartesianPolynomial K) := by
  simp [binaryMean]

/-- Transport an original `x`-axis mean identity to the Cartesian `Q₀=0`
axis.  This is restriction of a full polynomial identity. -/
theorem axis_drift_of_mean_identity (p rhs : MeanPolynomial K) (d : K)
    (h : meanXAxis (pderiv 1 p + C d * X 0 * p) = rhs) :
    axisRestriction (binaryMean 0 (pderiv 1 p) + C d * X 0 * binaryMean 0 p) =
      axisRestriction (binaryMean 0 rhs) := by
  have hh := congrArg (fun a : MeanPolynomial K => axisRestriction (binaryMean 0 a)) h
  rw [axisRestriction_binaryMean_zero_Xaxis] at hh
  simpa only [map_add, map_mul, binaryMean_C, binaryMean_X, parameterP,
    Matrix.cons_val_zero] using hh

/-- The full normal derivative of a contraction, before any axis restriction.
Only the right tensor's actual parameter independence is used. -/
theorem drift_contraction (κ : ι → ι → K)
    (A B : ι → CartesianPolynomial K) (c : CartesianPolynomial K)
    (hB : ∀ s, pderiv 2 (B s) = 0) :
    pderiv 2 (contraction κ A B) + c * contraction κ A B =
      contraction κ (fun s => pderiv 2 (A s) + c * A s) B := by
  rw [pderiv_contraction]
  simp only [hB, contraction_zero_right, add_zero]
  rw [contraction_add_left, contraction_mul_left]

/-- The off-diagonal Cartesian boundary follows from the original mixed
`yu` source boundary.  The retained kernel is not assumed to inherit a new
source identity. -/
theorem correctedMatrix_offDiagonalBoundary (κ : ι → ι → K)
    (E : ι → MeanPolynomial K) (d e : K)
    (hsource : ∀ s, meanXAxis
      (pderiv 1 (pderiv 2 (E s)) + C d * X 0 * pderiv 2 (E s)) = 0) :
    MatrixOffDiagonalBoundary (correctedMatrix κ E e) d := by
  unfold MatrixOffDiagonalBoundary
  rw [correctedMatrix_zero_one, kernelMatrix_zero_one]
  rw [drift_contraction κ _ _ (C d * X 0)
    (fun s => pderiv_binaryMean_one (pderiv 3 (E s)))]
  rw [map_contraction axisRestriction axisRestriction_C]
  have hh : ∀ s, axisRestriction
      (pderiv 2 (binaryMean 0 (pderiv 2 (E s))) +
        C d * X 0 * binaryMean 0 (pderiv 2 (E s))) = 0 := by
    intro s
    rw [pderiv_binaryMean_zero]
    simpa only [map_zero] using axis_drift_of_mean_identity (pderiv 2 (E s)) 0 d
      (hsource s)
  simp only [hh, contraction_zero_left]

/-- The scalar Cartesian boundary follows from the original pure-`B` row
identity and the pure-`H` cap of the unchanged second-row tensor. -/
theorem correctedMatrix_scalarBoundary (κ : ι → ι → K)
    (E : ι → MeanPolynomial K) (b : ι → K) (d e β η : K)
    (hsource : ∀ s, meanXAxis (pderiv 1 (E s) + C d * X 0 * E s) =
      X 0 * C β * C (b s))
    (hcap : contraction κ (fun s => C (b s))
      (fun s => binaryMean 1 (pderiv 2 (pderiv 3 (E s)) + C e * E s)) = C η) :
    MatrixScalarBoundary (correctedMatrix κ E e) d (β * η) := by
  unfold MatrixScalarBoundary
  rw [correctedMatrix_one_one]
  rw [drift_contraction κ _ _ (C d * X 0)
    (fun s => pderiv_binaryMean_one
      (pderiv 2 (pderiv 3 (E s)) + C e * E s))]
  rw [map_sub, map_contraction axisRestriction axisRestriction_C]
  have hh : ∀ s, axisRestriction
      (pderiv 2 (binaryMean 0 (E s)) + C d * X 0 * binaryMean 0 (E s)) =
      X 0 * C β * C (b s) := by
    intro s
    rw [pderiv_binaryMean_zero]
    have hs := axis_drift_of_mean_identity (E s) (X 0 * C β * C (b s)) d (hsource s)
    simpa only [map_mul, binaryMean_X, binaryMean_C, parameterP,
      Matrix.cons_val_zero, axisRestriction_X, axisRestriction_C] using hs
  simp only [hh]
  rw [contraction_mul_left]
  have hcapAxis := congrArg axisRestriction hcap
  rw [map_contraction axisRestriction axisRestriction_C] at hcapAxis
  simp only [axisRestriction_C] at hcapAxis
  rw [hcapAxis]
  simp only [map_mul, axisRestriction_C, axisRestriction_X, Matrix.cons_val_zero]
  ring

variable [IsAlgClosed K] [CharZero K]

/-- The actual finite tensor kernel supplies covariance, off-diagonal
divisibility, and both Cartesian boundary equations to the checked endpoint
module.  The remaining inputs are explicit original-source tensor identities.
-/
theorem endpoint_of_tensor_kernel
    (κ : ι → ι → K) (E : ι → MeanPolynomial K) (b : ι → K) {d e β η α : K}
    (hd : d ≠ 0) (hη : η ≠ 0)
    (hcov : KernelInvariant (kernel κ E))
    (hu : ∀ s, meanYAxis (pderiv 2 (E s)) = 0)
    (hv : ∀ s, meanXAxis (pderiv 3 (E s)) = 0)
    (hmixed : ∀ s, meanXAxis
      (pderiv 1 (pderiv 2 (E s)) + C d * X 0 * pderiv 2 (E s)) = 0)
    (hsource : ∀ s, meanXAxis (pderiv 1 (E s) + C d * X 0 * E s) =
      X 0 * C β * C (b s))
    (hcap : contraction κ (fun s => C (b s))
      (fun s => binaryMean 1 (pderiv 2 (pderiv 3 (E s)) + C e * E s)) = C η)
    (horigin : scalarContraction κ
      (fun s => MvPolynomial.eval (0 : Fin 4 → K) (E s))
      (fun s => MvPolynomial.eval (0 : Fin 4 → K)
        (pderiv 2 (pderiv 3 (E s)) + C e * E s)) = η * α) : β = d * α := by
  obtain ⟨h₀₁, h₁₀⟩ := correctedMatrix_offDiagonal_divisibility κ E e hu hv
  exact endpoint_of_covariant_matrix_boundaries hd hη (correctedMatrix_covariant hcov)
    h₀₁ h₁₀ (correctedMatrix_offDiagonalBoundary κ E d e hmixed)
    (correctedMatrix_scalarBoundary κ E b d e β η hsource hcap)
    ((correctedMatrix_origin κ E e).trans horigin)

end SourceBoundaries

end KrennAllOrders.ReplicaKernel
