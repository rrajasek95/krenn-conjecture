import WickReplicaBridge
import ReflectionResponses
import ReflectionTensorBridge
import BinaryPairing

/-!
# Actual finite Wick response pairing and replica rotation

The kernel is the actual shifted moment of the full product of local alternating
determinants. Its rotation law follows from the constructed moment and literal
covariance invariance, not from a supplied response-kernel axiom.
-/

namespace KrennAllOrders.WickPairing

open scoped BigOperators Classical
open WickCovariance WickCoefficientBridge WickShiftedBridge WickReplicaBridge
open ReflectionResponses ReflectionTensorBridge

variable {K E : Type*} [Field K] [CharZero K] [AddCommGroup E] [Module K E]

/-- A receiving tensor obtained from the actual finite shifted moments. -/
noncomputable def responseTensor {n : ℕ} (B : E →ₗ[K] E →ₗ[K] K)
    (μ : E →ₗ[K] K) (u v : Fin n → E) : BinaryPairing.Tensor (Fin n) K :=
  fun w => shiftedMoment B μ (fun i => if w i then v i else u i)

/-- No auxiliary slots remain after the local determinant contraction. -/
abbrev NoAux := Fin 0 ⊕ Fin 0

def noAuxValues : NoAux → E × E := Sum.elim Fin.elim0 Fin.elim0

/-- Literal determinant contraction against the actual independent shifted
replica moment. -/
noncomputable def contractedShifted {n : ℕ} (B : E →ₗ[K] E →ₗ[K] K)
    (μ ν : E →ₗ[K] K) (u v : Fin n → E) : K :=
  contractSites n (shiftedMoment (replicaCovariance B) (replicaMean μ ν))
    replicaLeft replicaRight u v noAuxValues

omit [CharZero K] in
theorem replicaMean_comp_linear (μ ν : E →ₗ[K] K) (a b c d : K) :
    (replicaMean μ ν).comp (replicaLinear a b c d) =
      replicaMean (a • μ + c • ν) (b • μ + d • ν) := by
  apply LinearMap.ext
  intro x
  simp only [LinearMap.comp_apply, replicaMean_apply, replicaLinear_apply,
    map_add, map_smul, LinearMap.add_apply, LinearMap.smul_apply, smul_eq_mul]
  ring

/-- Every covariance-preserving replica coordinate change acts by its literal
determinant at each physical site on the actual shifted response contraction. -/
theorem contractedShifted_linear {n : ℕ} (B : E →ₗ[K] E →ₗ[K] K)
    (μ ν : E →ₗ[K] K) (u v : Fin n → E) (a b c d : K)
    (h1 : a * a + c * c = 1) (h2 : b * b + d * d = 1)
    (h12 : a * b + c * d = 0) :
    contractedShifted B (a • μ + c • ν) (b • μ + d • ν) u v =
      (a * d - b * c) ^ n * contractedShifted B μ ν u v := by
  let T := replicaLinear (E := E) a b c d
  let f := shiftedMoment (ι := PairSlots n NoAux) (replicaCovariance B) (replicaMean μ ν)
  have hf : SlotSymmetric f := fun τ z => shiftedMoment_permute _ _ τ z
  have hcov : ∀ x y, replicaCovariance B (T x) (T y) = replicaCovariance B x y :=
    replicaLinear_covariance B a b c d
      (by simpa only [pow_two] using h1) (by simpa only [pow_two] using h2) h12
  have hm : shiftedMoment (ι := PairSlots n NoAux) (replicaCovariance B)
      (replicaMean (a • μ + c • ν) (b • μ + d • ν)) =
      f.compLinearMap (fun _ => T) := by
    ext z
    rw [MultilinearMap.compLinearMap_apply]
    change _ = shiftedMoment (replicaCovariance B) (replicaMean μ ν) (fun i => T (z i))
    rw [shiftedMoment_invariant _ _ T hcov, replicaMean_comp_linear]
  unfold contractedShifted
  rw [hm, contractSites_compLinearMap, replicaLinear_comp_left, replicaLinear_comp_right,
    contractSites_determinant n f hf]
  simp only [MultilinearMap.compLinearMap_apply, smul_apply, smul_eq_mul]
  congr 1
  congr 1
  funext i
  cases i with
  | inl i => exact Fin.elim0 i
  | inr i => exact Fin.elim0 i

/-- The determinant is one for an actual SO(2) replica rotation. -/
theorem contractedShifted_rotation {n : ℕ} (B : E →ₗ[K] E →ₗ[K] K)
    (μ ν : E →ₗ[K] K) (u v : Fin n → E) (a b : K) (hab : a * a + b * b = 1) :
    contractedShifted B (a • μ - b • ν) (b • μ + a • ν) u v =
      contractedShifted B μ ν u v := by
  have h := contractedShifted_linear B μ ν u v a b (-b) a
    (by simpa only [neg_mul_neg] using hab) (by rw [add_comm]; exact hab) (by ring)
  have hdet : a * a - b * (-b) = 1 := by
    simpa only [mul_neg, sub_neg_eq_add] using hab
  have hc : a • μ + (-b) • ν = a • μ - b • ν := by module
  simpa only [hc, hdet, one_pow, one_mul] using h

/-- The diagonal two-replica response is rotated to a centered first replica
and a mean enlarged by a scalar whose square is two. -/
theorem contractedShifted_diagonal {n : ℕ} (B : E →ₗ[K] E →ₗ[K] K)
    (μ : E →ₗ[K] K) (u v : Fin n → E) (s : K) (hs : s * s = 2) :
    contractedShifted B μ μ u v = contractedShifted B 0 (s • μ) u v := by
  have hab : (s / 2) * (s / 2) + (s / 2) * (s / 2) = 1 := by
    field_simp
    linear_combination 2 * hs
  have h := contractedShifted_rotation B μ μ u v (s / 2) (s / 2) hab
  rw [sub_self, ← add_smul, show s / 2 + s / 2 = s by ring] at h
  exact h.symm

/-- Empty auxiliary slots contribute no extra response data. -/
theorem shiftedMoment_sum_fin_zero {n : ℕ} (B : E →ₗ[K] E →ₗ[K] K)
    (μ : E →ₗ[K] K) (v : Fin n → E) :
    shiftedMoment B μ (Sum.elim v (Fin.elim0 : Fin 0 → E)) = shiftedMoment B μ v := by
  have hfun : Sum.elim v (Fin.elim0 : Fin 0 → E) =
      fun i => v (Equiv.sumEmpty (Fin n) (Fin 0) i) := by
    funext i
    cases i with
    | inl i => rfl
    | inr i => exact Fin.elim0 i
  rw [hfun, shiftedMoment_relabel]

/-- The literal determinant contraction equals exactly the signed complement
pairing of the two actual shifted receiving tensors. Every Boolean receiving
word is included by the generic contraction expansion. -/
theorem contractedShifted_eq_pairing {n : ℕ} (B : E →ₗ[K] E →ₗ[K] K)
    (μ ν : E →ₗ[K] K) (u v : Fin n → E) :
    contractedShifted B μ ν u v =
      BinaryPairing.pairing (responseTensor B μ u v) (responseTensor B ν u v) := by
  rw [contractedShifted, contractSites_expansion, BinaryPairing.pairing]
  convert! (Fintype.sum_equiv (wordsEquiv n)
    (fun w => wordSign (R := K) n w •
      shiftedMoment (replicaCovariance B) (replicaMean μ ν)
        (wordInputs n replicaLeft replicaRight u v w noAuxValues))
    (fun w => BinaryPairing.sign w * responseTensor B μ u v w *
      responseTensor B ν u v (BinaryPairing.complement w)) ?_) using 1
  · congr 1
    ext w
    simp
  intro w
  have hz : noAuxValues (E := E) =
      Sum.elim (fun i : Fin 0 => (Fin.elim0 i, (0 : E)))
        (fun j : Fin 0 => ((0 : E), Fin.elim0 j)) := by
    funext i
    cases i with
    | inl i => exact Fin.elim0 i
    | inr i => exact Fin.elim0 i
  rw [hz, wordInputs_eq_split, shiftedMoment_relabel _ _ (splitSlotsEquiv n)]
  simp only [splitReplicaInputs]
  rw [shiftedMoment_independent_replicas B μ ν
    (Sum.elim (leftWord n u v w) Fin.elim0) (Sum.elim (rightWord n u v w) Fin.elim0),
    shiftedMoment_sum_fin_zero, shiftedMoment_sum_fin_zero, wordSign_eq_sign, smul_eq_mul]
  have hr : rightWord n u v w =
      fun i => if BinaryPairing.complement (wordsEquiv n w) i then v i else u i := by
    funext i
    cases h : wordsEquiv n w i <;> simp [rightWord, BinaryPairing.complement, h]
  rw [hr]
  change BinaryPairing.sign (wordsEquiv n w) *
      (responseTensor B μ u v (wordsEquiv n w) *
        responseTensor B ν u v (BinaryPairing.complement (wordsEquiv n w))) = _
  ring

/-- Universal independent-mean rotation identity for actual finite responses. -/
theorem response_pairing_rotation {n : ℕ} (B : E →ₗ[K] E →ₗ[K] K)
    (μ ν : E →ₗ[K] K) (u v : Fin n → E) (a b : K) (hab : a * a + b * b = 1) :
    BinaryPairing.pairing (responseTensor B (a • μ - b • ν) u v)
      (responseTensor B (b • μ + a • ν) u v) =
      BinaryPairing.pairing (responseTensor B μ u v) (responseTensor B ν u v) := by
  simp only [← contractedShifted_eq_pairing]
  exact contractedShifted_rotation B μ ν u v a b hab

/-- The norm-two mean rotation is a theorem of the actual response pairing. -/
theorem response_pairing_diagonal {n : ℕ} (B : E →ₗ[K] E →ₗ[K] K)
    (μ : E →ₗ[K] K) (u v : Fin n → E) (s : K) (hs : s * s = 2) :
    BinaryPairing.pairing (responseTensor B μ u v) (responseTensor B μ u v) =
      BinaryPairing.pairing (responseTensor B 0 u v) (responseTensor B (s • μ) u v) := by
  simp only [← contractedShifted_eq_pairing]
  exact contractedShifted_diagonal B μ u v s hs

/-- Scalar-line specialization used to differentiate the actual finite identity.
The scalar parameter is arbitrary; no formal response-covariance hypothesis is
passed to this theorem. -/
theorem response_pairing_diagonal_line {n : ℕ} (B : E →ₗ[K] E →ₗ[K] K)
    (μ ν : E →ₗ[K] K) (u v : Fin n → E) (s : K) (hs : s * s = 2) (t : K) :
    BinaryPairing.pairing (responseTensor B (μ + t • ν) u v)
      (responseTensor B (μ + t • ν) u v) =
      BinaryPairing.pairing (responseTensor B 0 u v)
        (responseTensor B (s • (μ + t • ν)) u v) :=
  response_pairing_diagonal B (μ + t • ν) u v s hs

end KrennAllOrders.WickPairing
