/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import RetainedMeanWick
import OmissionTensor
import OmissionCancellation

/-! # Actual rotation and constancy of the omitted response tensor -/

namespace KrennAllOrders.OmissionRotation

open scoped BigOperators
open MvPolynomial MatchingModel SiteAlgebra RootResponse CofactorResponse
open PhysicalEndpoint RetainedBinary WickCovariance WickPhysicalBridge PhysicalMeanWick
open RetainedMeanWick OmissionTensor BinaryPairing FiniteResponseRigidity

variable {K : Type*} [Field K] [CharZero K] {N D : ℕ}

/-- The scalar-zero response, as a constant parameter tensor. -/
noncomputable def constantTensor {ι : Type*}
    (E : BinaryPairing.Tensor ι (ReplicaKernel.MeanPolynomial K)) :
    BinaryPairing.Tensor ι (ReplicaKernel.MeanPolynomial K) :=
  fun w => C (eval (fun _ => 0) (E w))

omit [CharZero K] in
theorem eval_scaleVariables (s : K) (P : ReplicaKernel.MeanPolynomial K) (a : Fin 4 → K) :
    eval a (scaleVariables s P) = eval (fun i => s * a i) P := by
  change eval₂ (RingHom.id K) a (eval₂ C (fun i => C s * X i) P) = _
  rw [← eval₂_assoc]
  congr 1
  funext i
  simp

/-- The actual retained coefficient tensor satisfies norm-two mean rotation. -/
theorem coefficientTensor_rotation (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D)
    (z : Fin 4 → SiteVariable (2 * (m + 1)) D) (s : K) (hs : s * s = 2) :
    pairing (coefficientTensor m W p q b h z) (coefficientTensor m W p q b h z) =
      pairing (constantTensor (coefficientTensor m W p q b h z))
        (fun w => scaleVariables s (coefficientTensor m W p q b h z w)) := by
  classical
  apply MvPolynomial.funext
  intro a
  simp only [PairingDerivative.map_pairing, constantTensor, eval_C, eval_scaleVariables]
  have hE : (fun w => eval a (coefficientTensor m W p q b h z w)) =
      WickFinitePairing.responseTensor (physicalCovariance W) (meanFunctional W z a)
        (fun v : RetainedSites p q => physicalBasis (v.val, b))
        (fun v : RetainedSites p q => physicalBasis (v.val, h)) := by
    funext w
    exact eval_coefficientTensor m W p q hpq b h z w a
  have hF : (fun w => eval (fun _ => 0) (coefficientTensor m W p q b h z w)) =
      WickFinitePairing.responseTensor (physicalCovariance W) 0
        (fun v : RetainedSites p q => physicalBasis (v.val, b))
        (fun v : RetainedSites p q => physicalBasis (v.val, h)) := by
    funext w
    rw [eval_coefficientTensor m W p q hpq]
    simp [meanFunctional]
  have hEs : (fun w => eval (fun i => s * a i) (coefficientTensor m W p q b h z w)) =
      WickFinitePairing.responseTensor (physicalCovariance W) (s • meanFunctional W z a)
        (fun v : RetainedSites p q => physicalBasis (v.val, b))
        (fun v : RetainedSites p q => physicalBasis (v.val, h)) := by
    funext w
    rw [eval_coefficientTensor m W p q hpq]
    congr 2
    exact (meanFunctionalLinear W z).map_smul s a
  rw [hE, hF, hEs]
  exact WickFinitePairing.response_pairing_diagonal _ _ _ _ s hs

/-- The original three root-colour rows and one omitted-root direction. -/
def omissionPoints (p q : V N) (h : Fin 3) : Fin 4 → SiteVariable N 3 :=
  ![(p, 0), (p, 1), (p, 2), (q, h)]

omit [CharZero K] in
theorem coefficientTensor_omission (m : ℕ) (W : WeightsN N 3 K)
    (p q : V N) (b h : Fin 3) :
    coefficientTensor m W p q b h (omissionPoints p q h) =
      OmissionTensor.responseTensor m W p q b h := by
  have hrows : (fun j => coreRow W p q (omissionPoints p q h j)) = omissionRows W p q h := by
    funext j
    fin_cases j <;> simp [omissionPoints, omissionRows]
  funext w
  simp only [coefficientTensor, OmissionTensor.responseTensor, hrows]

/-- Norm-two rotation of the literal omitted source tensor. -/
theorem omitted_tensor_rotation (m : ℕ) (W : WeightsN (2 * (m + 1)) 3 K)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin 3) (s : K) (hs : s * s = 2) :
    pairing (OmissionTensor.responseTensor m W p q b h)
      (OmissionTensor.responseTensor m W p q b h) =
      pairing (constantTensor (OmissionTensor.responseTensor m W p q b h))
        (fun w => scaleVariables s (OmissionTensor.responseTensor m W p q b h w)) := by
  simpa only [coefficientTensor_omission] using
    coefficientTensor_rotation m W p q hpq b h (omissionPoints p q h) s hs

end KrennAllOrders.OmissionRotation
