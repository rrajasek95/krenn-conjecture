/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import RetainedBinary
import PairingDerivative
import OmissionDegree

/-! # The actual binary omission tensor of a ternary source -/

namespace KrennAllOrders.OmissionTensor

open scoped BigOperators
open MvPolynomial MatchingModel SiteAlgebra RootResponse CofactorResponse PhysicalEndpoint RetainedBinary

variable {K : Type*} [Field K] [CharZero K] {N : ℕ}

/-- Three original root rows and the other root's selected directional row. -/
noncomputable def omissionRows (W : WeightsN N 3 K) (p q : V N) (h : Fin 3) :
    Fin 4 → PhysicalPolynomial N 3 K :=
  ![retainedRow W p q 0, retainedRow W p q 1, retainedRow W p q 2, retainedRow W q p h]

/-- The actual mean polynomial for each binary receiving word. -/
noncomputable def responseTensor (m : ℕ) (W : WeightsN N 3 K) (p q : V N) (b h : Fin 3) :
    BinaryPairing.Tensor (RetainedSites p q) (ReplicaKernel.MeanPolynomial K) :=
  fun w => receivingPolynomial (wordExponent (receivingWord p q b h w) (retainedVertices p q))
    (physicalEvenResponse m (retainedQuadratic W p q) (omissionRows W p q h))

/-- Set the auxiliary directional mean to zero while retaining all root rows. -/
noncomputable def directionZero : ReplicaKernel.MeanPolynomial K →+*
    ReplicaKernel.MeanPolynomial K := eval₂Hom C (fun j => if j = 3 then 0 else X j)

omit [CharZero K] in
@[simp] theorem directionZero_C (a : K) : directionZero (C a) = C a := by
  simp [directionZero]

omit [CharZero K] in
@[simp] theorem directionZero_X (j : Fin 4) :
    directionZero (X j : ReplicaKernel.MeanPolynomial K) = if j = 3 then 0 else X j := by
  simp [directionZero]

omit [CharZero K] in
theorem eval_directionZero (P : ReplicaKernel.MeanPolynomial K) (a : Fin 4 → K) :
    eval a (directionZero P) = eval (fun j => if j = 3 then 0 else a j) P := by
  change eval₂ (RingHom.id K) a (eval₂ C (fun j => if j = 3 then 0 else X j) P) = _
  rw [← eval₂_assoc]
  congr 1
  funext j
  by_cases hj : j = 3 <;> simp [hj]

omit [CharZero K] in
theorem omissionRows_castSucc (W : WeightsN N 3 K) (p q : V N) (h i : Fin 3) :
    omissionRows W p q h i.castSucc = retainedRow W p q i := by
  fin_cases i <;> rfl

omit [CharZero K] in
theorem omissionRows_three (W : WeightsN N 3 K) (p q : V N) (h : Fin 3) :
    omissionRows W p q h 3 = retainedRow W q p h := rfl

omit [CharZero K] in
/-- At zero directional parameter the mean is the literal original root row. -/
theorem mean_omissionRows_directionZero (W : WeightsN N 3 K)
    (p q : V N) (h : Fin 3) (a : Fin 4 → K) :
    (∑ j : Fin 4, C (if j = 3 then 0 else a j) * omissionRows W p q h j) =
      eraseSite q (OddResponseVanishing.rowAt W p (fun i => a i.castSucc)) := by
  simp [Fin.sum_univ_succ, omissionRows, OddResponseVanishing.rowAt,
    rootFamilyRow, retainedRow]

omit [CharZero K] in

/-- Evaluation of the omitted tensor is exactly the finite even response of
all three original root rows. -/
theorem eval_directionZero_responseTensor (m : ℕ) (W : WeightsN N 3 K)
    (p q : V N) (b h : Fin 3) (w : RetainedSites p q → Bool) (a : Fin 4 → K) :
    eval a (directionZero (responseTensor m W p q b h w)) =
      coeff (wordExponent (receivingWord p q b h w) (retainedVertices p q))
        (EvenResponse.evenResponse (K := K) m (retainedQuadratic W p q)
          (eraseSite q (OddResponseVanishing.rowAt W p (fun i => a i.castSucc)))) := by
  rw [eval_directionZero, responseTensor, eval_receivingPolynomial,
    eval_physicalEvenResponse, mean_omissionRows_directionZero]

/-- The directional derivative is exactly insertion of the other root row. -/
theorem eval_directionZero_pderiv_responseTensor (m : ℕ) (W : WeightsN N 3 K)
    (p q : V N) (b h : Fin 3) (w : RetainedSites p q → Bool) (a : Fin 4 → K) :
    eval a (directionZero (pderiv 3 (responseTensor m W p q b h w))) =
      coeff (wordExponent (receivingWord p q b h w) (retainedVertices p q))
        (retainedRow W q p h *
          EvenResponse.lowerOddResponse (K := K) m (retainedQuadratic W p q)
            (eraseSite q (OddResponseVanishing.rowAt W p (fun i => a i.castSucc)))) := by
  rw [eval_directionZero, responseTensor, ← receivingPolynomial_pderiv,
    pderiv_physicalEvenResponse, eval_receivingPolynomial]
  simp only [map_mul, eval_C, omissionRows_three]
  rw [EvenResponse.map_lowerOddResponse (eval
    (fun j => C (if j = 3 then 0 else a j))) (fun _ => by simp)]
  simp only [eval_C, meanRow, map_sum, map_mul, eval_X]
  rw [mean_omissionRows_directionZero]

/-- The direct omitted-root edge is the literal linear polynomial in all
three original root-colour parameters. -/
noncomputable def directPolynomial (W : WeightsN N 3 K) (p q : V N) (h : Fin 3) :
    ReplicaKernel.MeanPolynomial K :=
  ∑ i : Fin 3, X i.castSucc * C (edgeMatrix W (p, i) (q, h))

omit [CharZero K] in
theorem eval_directPolynomial (W : WeightsN N 3 K) (p q : V N) (h : Fin 3)
    (a : Fin 4 → K) :
    eval a (directPolynomial W p q h) =
      ∑ i : Fin 3, a i.castSucc * edgeMatrix W (p, i) (q, h) := by
  simp [directPolynomial]

omit [CharZero K] in
theorem rootExtract_rowAt (W : WeightsN N 3 K) (p q : V N) (h : Fin 3)
    (a : Fin 3 → K) :
    rootExtract q h (OddResponseVanishing.rowAt W p a) =
      C (∑ i : Fin 3, a i * edgeMatrix W (p, i) (q, h)) := by
  simp only [OddResponseVanishing.rowAt, rootFamilyRow, rootExtract,
    map_sum, pderiv_C_mul, EvenResponse.pderiv_rowPolynomial,
    map_mul, eraseSite_C]

/-- The original finite odd tower supplies the actual omitted tensor's source
identity. No reflection, covariance, or endpoint identity is assumed here. -/
theorem omitted_source_polynomial (m : ℕ) (W : WeightsN (2 * (m + 1)) 3 K)
    (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin 3) (hbh : b ≠ h)
    (w : RetainedSites p q → Bool)
    (hzero : ∀ r, 0 < r → r ≤ m →
      OddResponseVanishing.oddResponsePolynomial W p m r (receivingWord p q b h w) = 0) :
    directionZero (pderiv 3 (responseTensor m W p q b h w)) =
      X h.castSucc * C (BinaryPairing.pure true w : K) -
        directPolynomial W p q h * directionZero (responseTensor m W p q b h w) := by
  classical
  apply MvPolynomial.funext
  intro a
  rw [eval_directionZero_pderiv_responseTensor]
  simp only [map_sub, map_mul, eval_X, eval_C, eval_directPolynomial,
    eval_directionZero_responseTensor]
  have hs := OmittedResponse.coeff_omitted_source m W hW p q hpq
    (receivingWord p q b h w) (fun i => a i.castSucc) hzero
  rw [receivingWord_at_q, rootExtract_rowAt,
    extractedQuadratic_eq_retainedRow W p q h hpq, coeff_add, coeff_C_mul] at hs
  have hrhs : (∑ i : Fin 3, a i.castSucc *
      coeff (wordExponent (receivingWord p q b h w) ((vertices (2 * (m + 1))).erase p))
        (pureRootWord p i)) = a h.castSucc * (BinaryPairing.pure true w : K) := by
    rw [Finset.sum_eq_single h]
    · rw [coeff_pureRootWord_eq_retained p q hpq _ h (receivingWord_at_q p q b h w),
        coeff_pureRetainedWord p q b h hbh w]
    · intro i _ hi
      rw [coeff_pureRootWord_wrong_color p q hpq _ i
        (by simpa only [receivingWord_at_q] using hi), mul_zero]
    · simp
  rw [hrhs] at hs
  exact eq_sub_of_add_eq' hs

end KrennAllOrders.OmissionTensor
