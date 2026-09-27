/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import EndpointSource
import RetainedMeanWick
import WickFinitePairing
import WickFiniteOrthogonal

/-! # Covariance of the actual finite endpoint kernel -/

namespace KrennAllOrders.EndpointCovariance

open scoped BigOperators Matrix
open MvPolynomial MatchingModel SiteAlgebra RootResponse CofactorResponse PhysicalEndpoint
open EndpointSource RetainedBinary WickCovariance WickPhysicalBridge PhysicalMeanWick

variable {K : Type*} [Field K] [CharZero K] {N D : ℕ}

/-- The four original endpoint-colour rows, with exactly the same order as
the constructed parameter response. -/
def endpointPoints (p q : V N) (b h : Fin D) : Fin 4 → SiteVariable N D :=
  ![(p, b), (q, b), (p, h), (q, h)]

omit [CharZero K] in
theorem coreRow_endpointPoints (W : WeightsN N D K) (p q : V N) (b h : Fin D)
    (j : Fin 4) :
    RetainedMeanWick.coreRow W p q (endpointPoints p q b h j) =
      endpointRows W p q b h j := by
  fin_cases j <;> simp [endpointPoints, endpointRows]

omit [CharZero K] in
theorem eval_meanCopy (i : Fin 2) (P : ReplicaKernel.MeanPolynomial K)
    (a : Fin 4 × Fin 2 → K) :
    eval a (ReplicaKernel.meanCopy i P) = eval (fun j => a (j, i)) P := by
  change eval₂ (RingHom.id K) a (eval₂ C _ P) = _
  rw [← eval₂_assoc]
  simp only [eval₂_X]
  rfl

omit [CharZero K] in
theorem eval_endpointKernel (m : ℕ) (W : WeightsN N D K) (p q : V N) (b h : Fin D)
    (a : Fin 4 × Fin 2 → K) :
    eval a (ReplicaKernel.kernel (binaryKernel (K := K) p q) (endpointTensor m W p q b h)) =
      BinaryPairing.pairing
        (fun w => eval (fun j => a (j, 0)) (endpointTensor m W p q b h w))
        (fun w => eval (fun j => a (j, 1)) (endpointTensor m W p q b h w)) := by
  rw [ReplicaKernel.kernel, ReplicaKernel.eval_contraction,
    scalarContraction_eq_binaryPairing]
  simp only [eval_meanCopy]

omit [CharZero K] in
theorem eval_replicaFramePullback (O : Matrix (Fin 2) (Fin 2) K)
    (P : ReplicaKernel.ReplicaPolynomial K) (a : Fin 4 × Fin 2 → K) :
    eval a (ReplicaKernel.replicaFramePullback O P) =
      eval (fun ji => ∑ k : Fin 2, O ji.2 k * a (ji.1, k)) P := by
  change eval₂ (RingHom.id K) a (eval₂ C _ P) = _
  rw [← eval₂_assoc]
  congr 1
  funext ji
  simp [ReplicaKernel.replicaFrameAssignment]

/-- The parameter response is identified with actual finite Wick moments on
the retained physical sites, without a retained-source hypothesis. -/
theorem eval_endpointTensor_eq_responseTensor (m : ℕ)
    (W : WeightsN (2 * (m + 1)) D K)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (a : Fin 4 → K)
    (w : RetainedSites p q → Bool) :
    eval a (endpointTensor m W p q b h w) =
      WickFinitePairing.responseTensor (physicalCovariance W)
        (meanFunctional W (endpointPoints p q b h) a)
        (fun v : RetainedSites p q => physicalBasis (v.val, b))
        (fun v : RetainedSites p q => physicalBasis (v.val, h)) w := by
  rw [endpointTensor, eval_endpointResponse]
  have hm := RetainedMeanWick.shiftedMoment_retained_even m W p q hpq
    (receivingWord p q b h w) (endpointPoints p q b h) a
  simp only [coreRow_endpointPoints] at hm
  rw [← hm]
  unfold WickFinitePairing.responseTensor
  congr 1
  funext v
  rw [receivingWord_at_retained]
  cases w v <;> rfl

omit [CharZero K] in
theorem meanFunctional_pair_transform (W : WeightsN N D K)
    (z : Fin 4 → SiteVariable N D) (a b : Fin 4 → K) (s t : K) :
    meanFunctional W z (fun j => s * a j + t * b j) =
      s • meanFunctional W z a + t • meanFunctional W z b := by
  change meanFunctionalLinear W z (s • a + t • b) = _
  rw [map_add, map_smul, map_smul]
  rfl

/-- Every actual finite endpoint kernel is invariant under the complete
orthogonal group. The determinant sign cancels on the even retained set;
the reflection component is included. -/
theorem endpoint_kernel_invariant (m : ℕ)
    (W : WeightsN (2 * (m + 1)) D K)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) :
    ReplicaKernel.KernelInvariant
      (ReplicaKernel.kernel (binaryKernel (K := K) p q) (endpointTensor m W p q b h)) := by
  intro O hO
  apply MvPolynomial.funext
  intro a
  rw [eval_replicaFramePullback, eval_endpointKernel, eval_endpointKernel]
  have ht (v : Fin 4 → K) :
      (fun w : RetainedSites p q → Bool => eval v (endpointTensor m W p q b h w)) =
        WickFinitePairing.responseTensor (physicalCovariance W)
          (meanFunctional W (endpointPoints p q b h) v)
          (fun r : RetainedSites p q => physicalBasis (r.val, b))
          (fun r : RetainedSites p q => physicalBasis (r.val, h)) := by
    funext w
    exact eval_endpointTensor_eq_responseTensor m W p q hpq b h v w
  rw [ht, ht, ht, ht]
  simp only [Fin.sum_univ_two]
  rw [meanFunctional_pair_transform, meanFunctional_pair_transform]
  have hoo : O * Oᵀ = 1 := mul_eq_one_comm.mp hO
  have h₀ : O 0 0 * O 0 0 + O 0 1 * O 0 1 = 1 := by
    have hh := congrArg (fun M : Matrix (Fin 2) (Fin 2) K => M 0 0) hoo
    simpa only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.one_apply,
      Fin.sum_univ_two, if_true] using hh
  have h₁ : O 1 0 * O 1 0 + O 1 1 * O 1 1 = 1 := by
    have hh := congrArg (fun M : Matrix (Fin 2) (Fin 2) K => M 1 1) hoo
    simpa only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.one_apply,
      Fin.sum_univ_two, if_true] using hh
  have h₀₁ : O 0 0 * O 1 0 + O 0 1 * O 1 1 = 0 := by
    have hh := congrArg (fun M : Matrix (Fin 2) (Fin 2) K => M 0 1) hoo
    simpa only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.one_apply,
      Fin.sum_univ_two, if_neg (by decide : (0 : Fin 2) ≠ 1)] using hh
  have heven : Even (Fintype.card (RetainedSites p q)) := by
    rw [card_retainedSites p q hpq]
    exact ⟨m, by omega⟩
  exact WickFiniteOrthogonal.response_pairing_orthogonal_even (physicalCovariance W)
    (meanFunctional W (endpointPoints p q b h) (fun j => a (j, 0)))
    (meanFunctional W (endpointPoints p q b h) (fun j => a (j, 1)))
    (fun r : RetainedSites p q => physicalBasis (r.val, b))
    (fun r : RetainedSites p q => physicalBasis (r.val, h))
    (O 0 0) (O 1 0) (O 0 1) (O 1 1) h₀ h₁ h₀₁ heven

variable [IsAlgClosed K]

/-- The literal graph-model endpoint identity, after actual diagonalization
and vanishing of the original binary higher responses. No replica covariance
or endpoint differential equation remains as a hypothesis. -/
theorem supported_endpoint_from_original_binary_responses (m : ℕ)
    (W : WeightsN (2 * (m + 1)) D K) (hW : EqSystemN (2 * (m + 1)) D W)
    (hdiag : DiagonalSource W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (hp : OriginalHigherZeroOnPalette m W p b h)
    (hq : OriginalHigherZeroOnPalette m W q b h)
    (hd : edgeMatrix W (p, b) (q, b) ≠ 0) :
    edgeMatrix W (p, b) (q, b) * RootResponse.pureCofactor W b p q = 1 := by
  exact endpoint_of_original_source m W hW hdiag p q hpq b h hbh hp hq hd
    (endpoint_kernel_invariant m W p q hpq b h)

end KrennAllOrders.EndpointCovariance
