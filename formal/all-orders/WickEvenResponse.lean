import WickShiftedBridge
import EvenResponse

/-!
# Actual shifted Wick moments are the finite even and odd source responses

This file performs only the finite parity reindexing, retaining the endpoint
term. It identifies the concrete Wick construction with the same divided-power
response polynomials used by the source differentiation modules.
-/

namespace KrennAllOrders.WickEvenResponse

open scoped BigOperators Classical
open WickCovariance WickCoefficientBridge WickRootBridge WickShiftedBridge

variable {K E ι : Type*} [Field K] [CharZero K]
  [AddCommGroup E] [Module K E] [Fintype ι]

/-- Exact finite pairing of consecutive indices in a sum. -/
theorem sum_range_pairs {A : Type*} [AddCommMonoid A] (f : ℕ → A) (m : ℕ) :
    (∑ d ∈ Finset.range (2 * m), f d) =
      ∑ r ∈ Finset.range m, (f (2 * r) + f (2 * r + 1)) := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [show 2 * (m + 1) = (2 * m + 1) + 1 by omega,
      Finset.sum_range_succ, Finset.sum_range_succ, ih, Finset.sum_range_succ]
    exact add_assoc _ _ _

omit [CharZero K] in
/-- On an even number of slots all odd mean slices vanish for the actual
centered-complement parity reason. -/
theorem meanSlice_odd_eq_zero (B : E →ₗ[K] E →ₗ[K] K)
    (μ : E →ₗ[K] K) (v : ι → E) (m r : ℕ)
    (hcard : Fintype.card ι = 2 * m) (hr : r < m) :
    meanSlice B μ (2 * r + 1) v = 0 := by
  apply meanSlice_eq_zero_of_odd
  rw [hcard]
  rintro ⟨k, hk⟩
  omega

omit [CharZero K] in
/-- On an odd number of slots all even mean slices vanish, including degree zero. -/
theorem meanSlice_even_eq_zero (B : E →ₗ[K] E →ₗ[K] K)
    (μ : E →ₗ[K] K) (v : ι → E) (m r : ℕ)
    (hcard : Fintype.card ι = 2 * m + 1) (hr : r ≤ m) :
    meanSlice B μ (2 * r) v = 0 := by
  apply meanSlice_eq_zero_of_odd
  rw [hcard]
  rintro ⟨k, hk⟩
  omega

/-- Concrete shifted Wick evaluation on `2m` slots is the literal squarefree
coefficient of the complete finite even response. -/
theorem shiftedMoment_eq_evenResponse (B : E →ₗ[K] E →ₗ[K] K)
    (μ : E →ₗ[K] K) (v : ι → E) (m : ℕ)
    (hcard : Fintype.card ι = 2 * m) :
    shiftedMoment B μ v =
      MvPolynomial.coeff (topExponent ι)
        (EvenResponse.evenResponse (K := K) m
          (symmetricQuadratic (fun i j => B (v i) (v j)))
          (linearPolynomial (fun i => μ (v i)))) := by
  rw [shiftedMoment_eq_sum_meanSlice, hcard, Finset.sum_range_succ, sum_range_pairs]
  have hsum : (∑ r ∈ Finset.range m,
      (meanSlice B μ (2 * r) v + meanSlice B μ (2 * r + 1) v)) =
      ∑ r ∈ Finset.range m, meanSlice B μ (2 * r) v := by
    apply Finset.sum_congr rfl
    intro r hr
    rw [meanSlice_odd_eq_zero B μ v m r hcard (Finset.mem_range.mp hr), add_zero]
  rw [hsum, ← Finset.sum_range_succ]
  simp only [EvenResponse.evenResponse, MvPolynomial.coeff_sum]
  apply Finset.sum_congr rfl
  intro r hr
  have hrm : r ≤ m := by simpa using Finset.mem_range.mp hr
  rw [meanSlice_eq_coeff B μ v (2 * r) (m - r) (by omega)]
  simp only [EvenResponse.dividedPower, dividedQuadratic, Algebra.algebraMap_self,
    RingHom.id_apply]

/-- Concrete shifted Wick evaluation on `2m+1` slots is the literal squarefree
coefficient of the complete finite odd response. -/
theorem shiftedMoment_eq_oddResponse (B : E →ₗ[K] E →ₗ[K] K)
    (μ : E →ₗ[K] K) (v : ι → E) (m : ℕ)
    (hcard : Fintype.card ι = 2 * m + 1) :
    shiftedMoment B μ v =
      MvPolynomial.coeff (topExponent ι)
        (EvenResponse.oddResponse (K := K) m
          (symmetricQuadratic (fun i j => B (v i) (v j)))
          (linearPolynomial (fun i => μ (v i)))) := by
  rw [shiftedMoment_eq_sum_meanSlice, hcard,
    show 2 * m + 1 + 1 = 2 * (m + 1) by omega, sum_range_pairs]
  simp only [EvenResponse.oddResponse, MvPolynomial.coeff_sum]
  apply Finset.sum_congr rfl
  intro r hr
  have hrm : r ≤ m := by simpa using Finset.mem_range.mp hr
  rw [meanSlice_even_eq_zero B μ v m r hcard hrm, zero_add,
    meanSlice_eq_coeff B μ v (2 * r + 1) (m - r) (by omega)]
  simp only [EvenResponse.dividedPower, dividedQuadratic, Algebra.algebraMap_self,
    RingHom.id_apply]

end KrennAllOrders.WickEvenResponse
