/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import EvenResponse
import OmissionCancellation
import CofactorResponse
import OddResponseVanishing
import Mathlib.Algebra.Polynomial.Roots
import Mathlib.Algebra.CharZero.Infinite

/-! # Extracting and polarizing the quadratic omitted coefficient -/

namespace KrennAllOrders.OmissionDegree

open scoped BigOperators
open MatchingModel SiteAlgebra EvenResponse

variable {K : Type*} [Field K] [CharZero K]

/-- A finite even series which is constant at every scalar has zero quadratic
coefficient. There is no limit or convergence argument. -/
theorem quadratic_coefficient_zero_of_constant_even_series
    (k : ℕ) (c : ℕ → K)
    (hconstant : ∀ t : K, (∑ r ∈ Finset.range (k + 2), c r * t ^ (2 * r)) = c 0) :
    c 1 = 0 := by
  classical
  let P : Polynomial K := ∑ r ∈ Finset.range (k + 2),
    Polynomial.C (c r) * Polynomial.X ^ (2 * r)
  have hP : P = Polynomial.C (c 0) := by
    apply Polynomial.funext
    intro t
    simpa only [P, Polynomial.eval_finsetSum, Polynomial.eval_mul,
      Polynomial.eval_C, Polynomial.eval_pow, Polynomial.eval_X] using hconstant t
  have hc := congrArg (fun p : Polynomial K => p.coeff 2) hP
  simp only [P, Polynomial.finsetSum_coeff, Polynomial.coeff_C_mul_X_pow,
    Polynomial.coeff_C] at hc
  rw [Finset.sum_eq_single 1] at hc
  · simpa using hc
  · intro r _ hr
    simp [hr]
  · simp

omit [CharZero K] in
/-- Scaling a physical row scales its divided powers with the exact degree. -/
theorem dividedPower_C_mul {σ : Type*} (P : MvPolynomial σ K) (a : K) (n : ℕ) :
    dividedPower (K := K) (MvPolynomial.C a * P) n =
      MvPolynomial.C (a ^ n) * dividedPower (K := K) P n := by
  simp only [dividedPower, Algebra.algebraMap_self, RingHom.id_apply,
    mul_pow, map_pow]
  ring

/-- Constancy of the actual finite even response along every scaled row forces
the literal squared-row omission coefficient to vanish. -/
theorem squared_row_coefficient_zero {σ : Type*}
    (k : ℕ) (Q L : MvPolynomial σ K) (m : σ →₀ ℕ)
    (hconstant : ∀ t : K,
      MvPolynomial.coeff m (evenResponse (K := K) (k + 1) Q (MvPolynomial.C t * L)) =
        MvPolynomial.coeff m (dividedPower (K := K) Q (k + 1))) :
    MvPolynomial.coeff m (L ^ 2 * dividedPower (K := K) Q k) = 0 := by
  classical
  let c : ℕ → K := fun r => MvPolynomial.coeff m
    (dividedPower (K := K) L (2 * r) * dividedPower (K := K) Q (k + 1 - r))
  have hc : c 1 = 0 := by
    apply quadratic_coefficient_zero_of_constant_even_series k c
    intro t
    have ht := hconstant t
    simp only [evenResponse, MvPolynomial.coeff_sum, dividedPower_C_mul,
      mul_assoc, MvPolynomial.coeff_C_mul] at ht
    simp only [c, Nat.mul_zero, dividedPower_zero, Nat.sub_zero, one_mul]
    simpa only [Nat.add_assoc, show (1 + 1 : ℕ) = 2 from rfl, mul_comm] using ht
  have hfac : ((2 : ℕ).factorial : K)⁻¹ ≠ 0 := inv_ne_zero (by norm_num)
  apply (mul_eq_zero.mp (show ((2 : ℕ).factorial : K)⁻¹ *
    MvPolynomial.coeff m (L ^ 2 * dividedPower (K := K) Q k) = 0 from ?_)).resolve_left hfac
  simpa only [c, Nat.mul_one, Nat.add_sub_cancel, dividedPower, Algebra.algebraMap_self,
    RingHom.id_apply, mul_assoc, MvPolynomial.coeff_C_mul] using hc

/-- Constancy on a whole linear row family gives the two independent rows
required by the cofactor matrix product. -/
theorem two_row_coefficient_zero {σ E : Type*} [AddCommGroup E] [Module K E]
    (k : ℕ) (Q : MvPolynomial σ K) (L : E →ₗ[K] MvPolynomial σ K)
    (m : σ →₀ ℕ)
    (hconstant : ∀ v, MvPolynomial.coeff m (evenResponse (K := K) (k + 1) Q (L v)) =
      MvPolynomial.coeff m (dividedPower (K := K) Q (k + 1))) (v w : E) :
    MvPolynomial.coeff m (L v * L w * dividedPower (K := K) Q k) = 0 := by
  apply OmissionCancellation.polarized_quadratic_coefficient_eq_zero
    (MvPolynomial.lcoeff K m) L (dividedPower (K := K) Q k) _ v w
  intro u
  apply squared_row_coefficient_zero k Q (L u) m
  intro t
  have ht := hconstant (t • u)
  simpa only [map_smul, MvPolynomial.smul_eq_C_mul] using ht

/-- The original incident-row family restricted to the twice-deleted core,
as a linear map in the original root-colour parameters. -/
noncomputable def omittedRowLinear {N D : ℕ} (W : WeightsN N D K)
    (p q : V N) : (Fin D → K) →ₗ[K] MatchingPolynomial N D K where
  toFun a := RootResponse.eraseSite q (OddResponseVanishing.rowAt W p a)
  map_add' := by
    intro a b
    simp [OddResponseVanishing.rowAt, RootResponse.rootFamilyRow,
      add_mul, Finset.sum_add_distrib]
  map_smul' := by
    intro t a
    simp [OddResponseVanishing.rowAt, RootResponse.rootFamilyRow,
      MvPolynomial.smul_eq_C_mul, mul_assoc, Finset.mul_sum]

omit [CharZero K] in
@[simp]
theorem omittedRowLinear_single {N D : ℕ} (W : WeightsN N D K)
    (p q : V N) (i : Fin D) :
    omittedRowLinear W p q (Pi.single i 1) =
      RootResponse.eraseSite q (rowPolynomial (edgeMatrix W) (p, i)) := by
  classical
  simp [omittedRowLinear, OddResponseVanishing.rowAt, RootResponse.rootFamilyRow,
    Pi.single_apply]

/-- Pure even-response constancy on the actual row family gives exactly the
omitted two-row coefficients in the global diagonal-reduction theorem. -/
theorem omitted_two_row_zero_of_pure_even_constancy {N D : ℕ}
    (k : ℕ) (W : WeightsN N D K) (p q : V N) (i h : Fin D)
    (hconstant : ∀ a : Fin D → K,
      MvPolynomial.coeff (wordExponent (fun _ => h) (CofactorResponse.retainedVertices p q))
        (evenResponse (K := K) (k + 1)
          (RootResponse.eraseSite q (RootResponse.deletedQuadratic W p))
          (omittedRowLinear W p q a)) =
      MvPolynomial.coeff (wordExponent (fun _ => h) (CofactorResponse.retainedVertices p q))
        (dividedPower (K := K)
          (RootResponse.eraseSite q (RootResponse.deletedQuadratic W p)) (k + 1))) :
    MvPolynomial.coeff (wordExponent (fun _ => h) (CofactorResponse.retainedVertices p q))
      (CofactorResponse.omittedTwoRowPolynomial W p q i h k) = 0 := by
  have hz := two_row_coefficient_zero k _ (omittedRowLinear W p q) _ hconstant
    (Pi.single i 1) (Pi.single h 1)
  simpa only [omittedRowLinear_single, CofactorResponse.omittedTwoRowPolynomial,
    dividedPower, Algebra.algebraMap_self, RingHom.id_apply] using hz

end KrennAllOrders.OmissionDegree
