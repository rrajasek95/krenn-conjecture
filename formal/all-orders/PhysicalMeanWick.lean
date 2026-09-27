/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import WickPhysicalBridge
import WickEvenResponse
import WickFinitePairing
import PhysicalEndpoint

/-! # Shifted moments of literal original source rows -/

namespace KrennAllOrders.PhysicalMeanWick

open scoped BigOperators
open MvPolynomial MatchingModel SiteAlgebra RootResponse
open WickCovariance WickPhysicalBridge WickRootBridge

variable {K τ : Type*} [Field K] [CharZero K] [Fintype τ] {N D : ℕ}

/-- Any finite linear family of the original endpoint-colour rows. -/
noncomputable def meanRow (W : WeightsN N D K) (z : τ → SiteVariable N D)
    (a : τ → K) : MatchingPolynomial N D K :=
  ∑ j, C (a j) * rowPolynomial (edgeMatrix W) (z j)

/-- The same family as a mean functional for the actual source covariance. -/
noncomputable def meanFunctional (W : WeightsN N D K) (z : τ → SiteVariable N D)
    (a : τ → K) : PhysicalSpace N D K →ₗ[K] K :=
  ∑ j, a j • physicalCovariance W (physicalBasis (z j))

omit [CharZero K] in
theorem meanFunctional_basis (W : WeightsN N D K) (z : τ → SiteVariable N D)
    (a : τ → K) (t : SiteVariable N D) :
    meanFunctional W z a (physicalBasis t) = ∑ j, a j * edgeMatrix W (z j) t := by
  simp [meanFunctional, physicalCovariance_basis]

omit [CharZero K] in
theorem selectedRestriction_meanRow (W : WeightsN N D K)
    (S : Finset (V N)) (ι : V N → Fin D) (z : τ → SiteVariable N D) (a : τ → K) :
    selectedRestriction S ι (meanRow W z a) =
      linearPolynomial (fun v : ↥S => meanFunctional W z a
        (physicalBasis (selectedInput S ι v))) := by
  classical
  simp only [meanRow, map_sum, map_mul]
  have hrow : ∀ j, selectedRestriction S ι (rowPolynomial (edgeMatrix W) (z j)) =
      linearPolynomial (fun v : ↥S => edgeMatrix W (z j) (selectedInput S ι v)) :=
    fun j => killCompl_linearPolynomial _ _ _
  simp only [selectedRestriction, MvPolynomial.killCompl_C] at hrow ⊢
  simp_rw [hrow]
  simp only [linearPolynomial, meanFunctional_basis, map_sum, map_mul, Finset.sum_mul,
    Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro v _
  apply Finset.sum_congr rfl
  intro j _
  ring

omit [CharZero K] in
/-- Literal quadratic word restriction is the covariance used by the moments. -/
theorem selectedRestriction_sourceQuadratic (W : WeightsN N D K)
    (S : Finset (V N)) (ι : V N → Fin D) :
    selectedRestriction S ι (sourceQuadratic W) =
      WickCoefficientBridge.symmetricQuadratic (fun u v : ↥S =>
        physicalCovariance W (physicalBasis (selectedInput S ι u))
          (physicalBasis (selectedInput S ι v))) := by
  change MvPolynomial.killCompl (selectedInput_injective S ι)
    (WickCoefficientBridge.symmetricQuadratic (edgeMatrix W)) = _
  rw [killCompl_symmetricQuadratic]
  simp only [physicalCovariance_basis]

/-- The finite shifted Wick moment equals the actual original even-response
coefficient on any selected physical receiving word. -/
theorem shiftedMoment_even_selected (W : WeightsN N D K)
    (S : Finset (V N)) (ι : V N → Fin D) (z : τ → SiteVariable N D) (a : τ → K)
    (m : ℕ) (hS : S.card = 2 * m) :
    shiftedMoment (physicalCovariance W) (meanFunctional W z a)
      (fun v : ↥S => physicalBasis (selectedInput S ι v)) =
      coeff (∑ v ∈ S, Finsupp.single (v, ι v) 1)
        (EvenResponse.evenResponse (K := K) m (sourceQuadratic W) (meanRow W z a)) := by
  rw [WickEvenResponse.shiftedMoment_eq_evenResponse _ _ _ m (by simpa using hS)]
  rw [← selectedRestriction_sourceQuadratic, ← selectedRestriction_meanRow]
  have he := EvenResponse.map_evenResponse (K := K) (selectedRestriction S ι).toRingHom
    (fun c => by simp [selectedRestriction]) m (sourceQuadratic W) (meanRow W z a)
  change selectedRestriction S ι (EvenResponse.evenResponse (K := K) m
    (sourceQuadratic W) (meanRow W z a)) = _ at he
  calc
    _ = coeff (WickCoefficientBridge.topExponent (↥S))
        (selectedRestriction S ι (EvenResponse.evenResponse (K := K) m
          (sourceQuadratic W) (meanRow W z a))) := congrArg _ he.symm
    _ = _ := coeff_selectedRestriction S ι _

/-- The physical mean family is linear in the original scalar parameters. -/
noncomputable def meanFunctionalLinear (W : WeightsN N D K) (z : τ → SiteVariable N D) :
    (τ → K) →ₗ[K] (PhysicalSpace N D K →ₗ[K] K) where
  toFun := meanFunctional W z
  map_add' := by
    intro a b
    simp [meanFunctional, add_smul, Finset.sum_add_distrib]
  map_smul' := by
    intro t a
    simp [meanFunctional, mul_smul, Finset.smul_sum]

end KrennAllOrders.PhysicalMeanWick
