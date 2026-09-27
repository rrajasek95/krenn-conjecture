/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import EvenResponse
import CofactorResponse
import OddResponseVanishing

/-! # From actual higher responses to omitted source coefficients -/

namespace KrennAllOrders.OmittedResponse

open scoped BigOperators
open MatchingModel SiteAlgebra RootResponse CofactorResponse

variable {K : Type*} [Field K] [CharZero K] {N D : ℕ}

omit [CharZero K] in
/-- The finite shifted odd response uses the same raw normalization as the
actual higher-response tower, followed by its mean factorial. -/
theorem oddResponse_term (k r : ℕ) (Q L : MatchingPolynomial N D K) :
    EvenResponse.dividedPower (K := K) L (2 * r + 1) *
      EvenResponse.dividedPower (K := K) Q (k - r) =
    MvPolynomial.C (((2 * r + 1).factorial : K)⁻¹) *
      (MvPolynomial.C (((k - r).factorial : K)⁻¹) * L ^ (2 * r + 1) * Q ^ (k - r)) := by
  simp only [EvenResponse.dividedPower, Algebra.algebraMap_self, RingHom.id_apply]
  ring

omit [CharZero K] in
/-- A literal selected coefficient of the finite odd response reduces to its
linear term when all its actual higher coefficients vanish. -/
theorem coeff_oddResponse_eq_linear_of_higher_zero
    (k : ℕ) (Q L : MatchingPolynomial N D K) (m : SiteVariable N D →₀ ℕ)
    (hzero : ∀ r, 0 < r → r ≤ k →
      MvPolynomial.coeff m
        (MvPolynomial.C (((k - r).factorial : K)⁻¹) * L ^ (2 * r + 1) * Q ^ (k - r)) = 0) :
    MvPolynomial.coeff m (EvenResponse.oddResponse (K := K) k Q L) =
      MvPolynomial.coeff m (MvPolynomial.C ((k.factorial : K)⁻¹) * L * Q ^ k) := by
  classical
  simp only [EvenResponse.oddResponse, MvPolynomial.coeff_sum, oddResponse_term,
    MvPolynomial.coeff_C_mul]
  rw [Finset.sum_eq_single 0]
  · simp
  · intro r hr hr0
    rw [hzero r (Nat.pos_of_ne_zero hr0) (by have := Finset.mem_range.mp hr; omega), mul_zero]
  · simp

omit [CharZero K] in
/-- Vanishing of the actual parameter response polynomial supplies precisely
the raw receiving coefficient needed by the finite omission calculation. -/
theorem raw_coefficient_zero_of_response_zero (W : WeightsN N D K)
    (p : V N) (k r : ℕ) (hr : r ≤ k) (ι : V N → Fin D) (a : Fin D → K)
    (hz : OddResponseVanishing.oddResponsePolynomial W p k r ι = 0) :
    MvPolynomial.coeff (wordExponent ι ((vertices N).erase p))
      (MvPolynomial.C (((k - r).factorial : K)⁻¹) *
        OddResponseVanishing.rowAt W p a ^ (2 * r + 1) *
        deletedQuadratic W p ^ (k - r)) = 0 := by
  have h := congrArg (MvPolynomial.eval a) hz
  rw [OddResponseVanishing.eval_oddResponsePolynomial] at h
  simpa only [OddResponseVanishing.oddResponse, if_pos hr,
    OddResponseVanishing.retainedCoefficient_project, map_zero] using h

/-- Full finite response coefficients are determined by the original pure
linear response after the actual higher-response polynomials vanish. -/
theorem coeff_source_oddResponse (k : ℕ) (W : WeightsN (2 * (k + 1)) D K)
    (hW : EqSystemN (2 * (k + 1)) D W) (p : V (2 * (k + 1)))
    (ι : V (2 * (k + 1)) → Fin D) (a : Fin D → K)
    (hzero : ∀ r, 0 < r → r ≤ k →
      OddResponseVanishing.oddResponsePolynomial W p k r ι = 0) :
    MvPolynomial.coeff (wordExponent ι ((vertices (2 * (k + 1))).erase p))
      (EvenResponse.oddResponse (K := K) k (deletedQuadratic W p)
        (OddResponseVanishing.rowAt W p a)) =
      ∑ i : Fin D, a i * MvPolynomial.coeff
        (wordExponent ι ((vertices (2 * (k + 1))).erase p)) (pureRootWord p i) := by
  classical
  rw [coeff_oddResponse_eq_linear_of_higher_zero k _ _ _
    (fun r hp hr => raw_coefficient_zero_of_response_zero W p k r hr ι a (hzero r hp hr))]
  have h := OddResponseVanishing.oddResponse_zero k W hW p a
  have hc := congrArg (OddResponseVanishing.retainedCoefficient p ι) h
  change _ = _ at hc
  rw [show OddResponseVanishing.oddResponse W p k 0 a =
      project (MvPolynomial.C ((k.factorial : K)⁻¹) *
        OddResponseVanishing.rowAt W p a * deletedQuadratic W p ^ k) by
      simp [OddResponseVanishing.oddResponse]] at hc
  rw [OddResponseVanishing.retainedCoefficient_project] at hc
  rw [hc]
  change (OddResponseVanishing.retainedCoefficientHom p ι)
    (∑ i, OddResponseVanishing.siteScalar (a i) * project (pureRootWord p i)) = _
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro i _
  exact (OddResponseVanishing.retainedCoefficient_scalar_mul p ι (a i) _).trans
    (congrArg (a i * ·) (OddResponseVanishing.retainedCoefficient_project p ι _))

/-- Coefficients after literal root extraction are the original coefficients
with that root's receiving colour restored. -/
theorem coeff_rootExtract (P : MatchingPolynomial N D K)
    (q : V N) (ι : V N → Fin D) (L : List (V N)) (hq : q ∉ L) :
    MvPolynomial.coeff (wordExponent ι L) (rootExtract q (ι q) P) =
      MvPolynomial.coeff (wordExponent ι (q :: L)) P := by
  rw [rootExtract, coeff_word_eraseSite q _ ι L hq]
  exact (coeff_root_pderiv P ι q L hq).symm

/-- On the twice-deleted core, root extraction restores precisely the original
retained receiving word, independently of the ordered enumeration. -/
theorem coeff_retained_rootExtract (P : MatchingPolynomial N D K)
    (p q : V N) (hpq : p ≠ q) (ι : V N → Fin D) :
    MvPolynomial.coeff (wordExponent ι (retainedVertices p q))
      (rootExtract q (ι q) P) =
      MvPolynomial.coeff (wordExponent ι ((vertices N).erase p)) P := by
  have hq : q ∉ retainedVertices p q := by simp [mem_retainedVertices]
  rw [coeff_rootExtract P q ι _ hq]
  congr 1
  rw [wordExponent, wordExponent_erase ι _ q
    ((List.mem_erase_of_ne hpq.symm).mpr (mem_vertices q))]
  rfl

/-- The exact finite even omission source equation, expressed as receiving
coefficients of the original source rather than a presumed tensor identity. -/
theorem coeff_omitted_source (k : ℕ) (W : WeightsN (2 * (k + 1)) D K)
    (hW : EqSystemN (2 * (k + 1)) D W)
    (p q : V (2 * (k + 1))) (hpq : p ≠ q)
    (ι : V (2 * (k + 1)) → Fin D) (a : Fin D → K)
    (hzero : ∀ r, 0 < r → r ≤ k →
      OddResponseVanishing.oddResponsePolynomial W p k r ι = 0) :
    MvPolynomial.coeff (wordExponent ι (retainedVertices p q))
      (rootExtract q (ι q) (OddResponseVanishing.rowAt W p a) *
        EvenResponse.evenResponse (K := K) k
          (eraseSite q (deletedQuadratic W p))
          (eraseSite q (OddResponseVanishing.rowAt W p a)) +
       rootExtract q (ι q) (deletedQuadratic W p) *
        EvenResponse.lowerOddResponse (K := K) k
          (eraseSite q (deletedQuadratic W p))
          (eraseSite q (OddResponseVanishing.rowAt W p a))) =
      ∑ i : Fin D, a i * MvPolynomial.coeff
        (wordExponent ι ((vertices (2 * (k + 1))).erase p)) (pureRootWord p i) := by
  rw [← EvenResponse.rootExtract_oddResponse, coeff_retained_rootExtract _ p q hpq ι]
  exact coeff_source_oddResponse k W hW p ι a hzero

end KrennAllOrders.OmittedResponse
