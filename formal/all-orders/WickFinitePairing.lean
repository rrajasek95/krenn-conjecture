import WickPairing

/-! # Site-enumeration independent actual Wick response pairing

The finite-site adapter preserves the literal signed complement pairing and
therefore transports the proved actual rotation identity to arbitrary finite
retained-site types, including deleted-vertex subtypes.
-/

namespace KrennAllOrders.WickFinitePairing

open scoped BigOperators Classical
open WickCovariance WickReplicaBridge

variable {ι κ K E : Type*} [Fintype ι] [Fintype κ]

/-- Relabel the Boolean receiving words along a site equivalence. -/
def wordEquiv (e : ι ≃ κ) : (ι → Bool) ≃ (κ → Bool) where
  toFun w := fun j => w (e.symm j)
  invFun w := fun i => w (e i)
  left_inv w := by funext i; simp
  right_inv w := by funext i; simp

@[simp] theorem sign_wordEquiv [CommRing K] (e : ι ≃ κ) (w : ι → Bool) :
    BinaryPairing.sign (R := K) (wordEquiv e w) = BinaryPairing.sign w := by
  unfold BinaryPairing.sign
  exact Equiv.prod_comp e.symm (fun i => if w i then (-1 : K) else 1)

omit [Fintype ι] [Fintype κ] in
@[simp] theorem complement_wordEquiv (e : ι ≃ κ) (w : ι → Bool) :
    BinaryPairing.complement (wordEquiv e w) =
      wordEquiv e (BinaryPairing.complement w) := rfl

/-- The actual alternating tensor pairing is independent of site enumeration. -/
theorem pairing_reindex [CommRing K] (e : ι ≃ κ)
    (P Q : BinaryPairing.Tensor κ K) :
    BinaryPairing.pairing (fun w => P (wordEquiv e w))
      (fun w => Q (wordEquiv e w)) = BinaryPairing.pairing P Q := by
  unfold BinaryPairing.pairing
  exact Fintype.sum_equiv (wordEquiv e) _ _ (fun w => by simp)

variable [Field K] [CharZero K] [AddCommGroup E] [Module K E]

/-- Actual finite response on an arbitrary finite retained-site type. -/
noncomputable def responseTensor (B : E →ₗ[K] E →ₗ[K] K)
    (μ : E →ₗ[K] K) (u v : ι → E) : BinaryPairing.Tensor ι K :=
  fun w => shiftedMoment B μ (fun i => if w i then v i else u i)

theorem responseTensor_reindex (B : E →ₗ[K] E →ₗ[K] K)
    (μ : E →ₗ[K] K) (u v : κ → E) (e : ι ≃ κ) (w : ι → Bool) :
    responseTensor B μ (fun i => u (e i)) (fun i => v (e i)) w =
      responseTensor B μ u v (wordEquiv e w) := by
  unfold responseTensor
  have h := shiftedMoment_relabel B μ e
    (fun j => if wordEquiv e w j then v j else u j)
  simpa only [wordEquiv, Equiv.coe_fn_mk, Equiv.symm_apply_apply] using h

/-- Universal independent-mean rotation of actual receiving tensors, on any
finite site type. -/
theorem response_pairing_rotation (B : E →ₗ[K] E →ₗ[K] K)
    (μ ν : E →ₗ[K] K) (u v : ι → E) (a b : K) (hab : a * a + b * b = 1) :
    BinaryPairing.pairing (responseTensor B (a • μ - b • ν) u v)
      (responseTensor B (b • μ + a • ν) u v) =
      BinaryPairing.pairing (responseTensor B μ u v) (responseTensor B ν u v) := by
  let e := (Fintype.equivFin ι).symm
  have h := WickPairing.response_pairing_rotation B μ ν
    (fun i => u (e i)) (fun i => v (e i)) a b hab
  have hr (ξ : E →ₗ[K] K) :
      WickPairing.responseTensor B ξ (fun i => u (e i)) (fun i => v (e i)) =
        fun w => responseTensor B ξ u v (wordEquiv e w) := by
    funext w
    exact responseTensor_reindex B ξ u v e w
  simp only [hr, pairing_reindex] at h
  exact h

/-- The norm-two diagonal identity for an arbitrary finite retained set. -/
theorem response_pairing_diagonal (B : E →ₗ[K] E →ₗ[K] K)
    (μ : E →ₗ[K] K) (u v : ι → E) (s : K) (hs : s * s = 2) :
    BinaryPairing.pairing (responseTensor B μ u v) (responseTensor B μ u v) =
      BinaryPairing.pairing (responseTensor B 0 u v) (responseTensor B (s • μ) u v) := by
  have hab : (s / 2) * (s / 2) + (s / 2) * (s / 2) = 1 := by
    field_simp
    linear_combination 2 * hs
  have h := response_pairing_rotation B μ μ u v (s / 2) (s / 2) hab
  rw [sub_self, ← add_smul, show s / 2 + s / 2 = s by ring] at h
  exact h.symm

/-- Scalar-line form used for the actual even-response differentiated identity. -/
theorem response_pairing_diagonal_line (B : E →ₗ[K] E →ₗ[K] K)
    (μ ν : E →ₗ[K] K) (u v : ι → E) (s : K) (hs : s * s = 2) (t : K) :
    BinaryPairing.pairing (responseTensor B (μ + t • ν) u v)
      (responseTensor B (μ + t • ν) u v) =
      BinaryPairing.pairing (responseTensor B 0 u v)
        (responseTensor B (s • (μ + t • ν)) u v) :=
  response_pairing_diagonal B (μ + t • ν) u v s hs

end KrennAllOrders.WickFinitePairing
