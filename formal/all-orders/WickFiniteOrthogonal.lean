import WickFinitePairing

/-! # Arbitrary finite-site orthogonal covariance of actual response pairings -/

namespace KrennAllOrders.WickFiniteOrthogonal

open scoped Classical
open WickFinitePairing

variable {K E ι : Type*} [Field K] [CharZero K]
  [AddCommGroup E] [Module K E] [Fintype ι]

/-- Every covariance-preserving two-replica matrix contributes its determinant
once per retained physical site. -/
theorem response_pairing_linear (B : E →ₗ[K] E →ₗ[K] K)
    (μ ν : E →ₗ[K] K) (u v : ι → E) (a b c d : K)
    (h1 : a * a + c * c = 1) (h2 : b * b + d * d = 1)
    (h12 : a * b + c * d = 0) :
    BinaryPairing.pairing (responseTensor B (a • μ + c • ν) u v)
      (responseTensor B (b • μ + d • ν) u v) =
      (a * d - b * c) ^ Fintype.card ι *
        BinaryPairing.pairing (responseTensor B μ u v) (responseTensor B ν u v) := by
  let e := (Fintype.equivFin ι).symm
  have h := WickPairing.contractedShifted_linear B μ ν
    (fun i => u (e i)) (fun i => v (e i)) a b c d h1 h2 h12
  simp only [WickPairing.contractedShifted_eq_pairing] at h
  have hr (ξ : E →ₗ[K] K) :
      WickPairing.responseTensor B ξ (fun i => u (e i)) (fun i => v (e i)) =
        fun w => responseTensor B ξ u v (wordEquiv e w) := by
    funext w
    exact responseTensor_reindex B ξ u v e w
  simp only [hr, pairing_reindex] at h
  exact h

/-- On an even retained set the determinant factor is one for every orthogonal
matrix, including the reflection component. -/
theorem response_pairing_orthogonal_even (B : E →ₗ[K] E →ₗ[K] K)
    (μ ν : E →ₗ[K] K) (u v : ι → E) (a b c d : K)
    (h1 : a * a + c * c = 1) (h2 : b * b + d * d = 1)
    (h12 : a * b + c * d = 0) (heven : Even (Fintype.card ι)) :
    BinaryPairing.pairing (responseTensor B (a • μ + c • ν) u v)
      (responseTensor B (b • μ + d • ν) u v) =
      BinaryPairing.pairing (responseTensor B μ u v) (responseTensor B ν u v) := by
  have hdet : (a * d - b * c) ^ 2 = 1 := by
    calc
      _ = (a * a + c * c) * (b * b + d * d) - (a * b + c * d) ^ 2 := by ring
      _ = 1 := by rw [h1, h2, h12]; ring
  have hpow : (a * d - b * c) ^ Fintype.card ι = 1 := by
    obtain ⟨k, hk⟩ := heven
    rw [hk, ← two_mul, pow_mul, hdet, one_pow]
  rw [response_pairing_linear B μ ν u v a b c d h1 h2 h12, hpow, one_mul]

end KrennAllOrders.WickFiniteOrthogonal
