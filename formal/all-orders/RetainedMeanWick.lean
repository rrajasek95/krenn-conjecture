/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import PhysicalMeanWick
import RetainedBinary

/-! # The physical even tensor on the twice-deleted core -/

namespace KrennAllOrders.RetainedMeanWick

open scoped BigOperators
open MvPolynomial MatchingModel SiteAlgebra RootResponse CofactorResponse
open PhysicalEndpoint RetainedBinary WickCovariance WickPhysicalBridge PhysicalMeanWick

variable {K τ : Type*} [Field K] [CharZero K] [Fintype τ] {N D : ℕ}

/-- Every original row restricted to the two-root-deleted core. -/
noncomputable def coreRow (W : WeightsN N D K) (p q : V N) (z : SiteVariable N D) :
    PhysicalPolynomial N D K := eraseSite q (eraseSite p (rowPolynomial (edgeMatrix W) z))

omit [CharZero K] in
@[simp] theorem coreRow_left (W : WeightsN N D K) (p q : V N) (i : Fin D) :
    coreRow W p q (p, i) = retainedRow W p q i := by
  rw [coreRow, eraseSite_rowPolynomial]
  rfl

omit [CharZero K] in
@[simp] theorem coreRow_right (W : WeightsN N D K) (p q : V N) (i : Fin D) :
    coreRow W p q (q, i) = retainedRow W q p i := by
  rw [coreRow, eraseSite_commute, eraseSite_rowPolynomial]
  rfl

omit [CharZero K] in
theorem erased_meanRow (W : WeightsN N D K) (p q : V N)
    (z : τ → SiteVariable N D) (a : τ → K) :
    eraseSite q (eraseSite p (PhysicalMeanWick.meanRow W z a)) =
      ∑ j, C (a j) * coreRow W p q (z j) := by
  simp only [PhysicalMeanWick.meanRow, map_sum, map_mul, eraseSite_C, coreRow]

omit [CharZero K] in
/-- On a selected retained word, the exact full source coefficient is unchanged
by deleting both omitted roots from its quadratic and every row. -/
theorem coeff_evenResponse_core (m : ℕ) (W : WeightsN N D K) (p q : V N)
    (ι : V N → Fin D) (z : τ → SiteVariable N D) (a : τ → K) :
    coeff (wordExponent ι (retainedVertices p q))
      (EvenResponse.evenResponse (K := K) m (sourceQuadratic W) (PhysicalMeanWick.meanRow W z a)) =
    coeff (wordExponent ι (retainedVertices p q))
      (EvenResponse.evenResponse (K := K) m (retainedQuadratic W p q)
        (∑ j, C (a j) * coreRow W p q (z j))) := by
  have hp : p ∉ retainedVertices p q := by simp [mem_retainedVertices]
  have hq : q ∉ retainedVertices p q := by simp [mem_retainedVertices]
  rw [← coeff_word_eraseSite p _ ι _ hp, ← coeff_word_eraseSite q _ ι _ hq]
  rw [EvenResponse.map_evenResponse (eraseSite p) (fun _ => eraseSite_C p _),
    EvenResponse.map_evenResponse (eraseSite q) (fun _ => eraseSite_C q _), erased_meanRow]
  rfl

/-- Actual shifted moments on the physical subtype of retained sites are the
literal finite even-response coefficients used by both omission and endpoint. -/
theorem shiftedMoment_retained_even (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (ι : V (2 * (m + 1)) → Fin D)
    (z : τ → SiteVariable (2 * (m + 1)) D) (a : τ → K) :
    shiftedMoment (physicalCovariance W) (meanFunctional W z a)
      (fun v : RetainedSites p q => physicalBasis (v.val, ι v.val)) =
      coeff (wordExponent ι (retainedVertices p q))
        (EvenResponse.evenResponse (K := K) m (retainedQuadratic W p q)
          (∑ j, C (a j) * coreRow W p q (z j))) := by
  let L := retainedVertices p q
  let vals : ↥L.toFinset → PhysicalSpace (2 * (m + 1)) D K :=
    fun v => physicalBasis (selectedInput L.toFinset ι v)
  have hv : (fun v : RetainedSites p q => physicalBasis (v.val, ι v.val)) =
      fun v => vals (retainedListEquiv p q v) := rfl
  rw [hv, WickReplicaBridge.shiftedMoment_relabel _ _ (retainedListEquiv p q)]
  have hcard : L.toFinset.card = 2 * m := by
    rw [List.toFinset_card_of_nodup (retainedVertices_nodup p q), retainedVertices_length p q hpq]
    omega
  rw [shiftedMoment_even_selected W L.toFinset ι z a m hcard,
    ← wordExponent_eq_finset_sum ι L (retainedVertices_nodup p q)]
  exact coeff_evenResponse_core m W p q ι z a

/-- A literal retained binary tensor with four formal mean parameters. -/
noncomputable def coefficientTensor (m : ℕ) (W : WeightsN N D K)
    (p q : V N) (b h : Fin D) (z : Fin 4 → SiteVariable N D) :
    BinaryPairing.Tensor (RetainedSites p q) (ReplicaKernel.MeanPolynomial K) :=
  fun w => receivingPolynomial (wordExponent (receivingWord p q b h w) (retainedVertices p q))
    (physicalEvenResponse m (retainedQuadratic W p q) (fun j => coreRow W p q (z j)))

/-- Exact evaluation of the physical tensor as the finite shifted Wick tensor,
with covariance built from the original edge weights. -/
theorem eval_coefficientTensor (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D)
    (z : Fin 4 → SiteVariable (2 * (m + 1)) D)
    (w : RetainedSites p q → Bool) (a : Fin 4 → K) :
    eval a (coefficientTensor m W p q b h z w) =
      WickFinitePairing.responseTensor (physicalCovariance W) (meanFunctional W z a)
        (fun v : RetainedSites p q => physicalBasis (v.val, b))
        (fun v : RetainedSites p q => physicalBasis (v.val, h)) w := by
  rw [coefficientTensor, eval_receivingPolynomial, eval_physicalEvenResponse,
    ← shiftedMoment_retained_even m W p q hpq _ z a]
  unfold WickFinitePairing.responseTensor
  congr 1
  funext v
  rw [receivingWord_at_retained]
  cases w v <;> rfl

end KrennAllOrders.RetainedMeanWick
