/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import BinaryPairing
import Mathlib.Algebra.Algebra.Basic
import Mathlib.Algebra.Field.Basic
import Mathlib.Tactic.LinearCombination

/-!
# Cancelling the direct term in the even-omission identity

This is the finite bilinear algebra after differentiating the actual replica
rotation identity. Both rotation identities and both source response formulas
are explicit premises; their physical-source derivation is a separate step.
-/

namespace KrennAllOrders.OmissionCancellation

variable {R M : Type*} [CommRing R] [IsDomain R]
  [AddCommGroup M] [Module R M]

/-- The direct root coefficient cancels using the undifferentiated rotation
identity, leaving equality of the retained pure coefficients. -/
theorem pairing_eq_of_response_and_rotation
    (B : M →ₗ[R] M →ₗ[R] R) (E F Es V Vs H : M) (s f d : R)
    (hs : s ≠ 0) (hf : f ≠ 0)
    (hV : V = f • H - d • E)
    (hVs : Vs = (s * f) • H - (s * d) • Es)
    (hrotation : B E E = B F Es)
    (hderivative : s * B E V = B F Vs) : B E H = B F H := by
  rw [hV, hVs] at hderivative
  simp only [map_sub, map_smul, smul_eq_mul] at hderivative
  rw [← hrotation] at hderivative
  apply mul_left_cancel₀ (mul_ne_zero hs hf)
  linear_combination hderivative

/-- The binary contraction with the pure true word extracts the pure false
coefficient, so the generic cancellation has the exact omission conclusion. -/
theorem pure_coefficient_eq_of_response_and_rotation
    {ι : Type*} [Fintype ι] (E F Es V Vs : BinaryPairing.Tensor ι R) (s f d : R)
    (hs : s ≠ 0) (hf : f ≠ 0)
    (hV : V = f • BinaryPairing.pure true - d • E)
    (hVs : Vs = (s * f) • BinaryPairing.pure true - (s * d) • Es)
    (hrotation : BinaryPairing.pairing E E = BinaryPairing.pairing F Es)
    (hderivative : s * BinaryPairing.pairing E V = BinaryPairing.pairing F Vs) :
    E (fun _ => false) = F (fun _ => false) := by
  have h := pairing_eq_of_response_and_rotation BinaryPairing.bilinearPairing
    E F Es V Vs (BinaryPairing.pure true) s f d hs hf hV hVs hrotation hderivative
  change BinaryPairing.pairing E (BinaryPairing.pure true) =
    BinaryPairing.pairing F (BinaryPairing.pure true) at h
  simpa only [BinaryPairing.pairing_right_pure_true] using h

/-- The quadratic omission coefficient polarizes to two independently chosen
rows. Characteristic zero is used only to cancel the factor two. -/
theorem polarized_quadratic_coefficient_eq_zero
    {K A E : Type*} [Field K] [CharZero K] [CommRing A] [Algebra K A]
    [AddCommGroup E] [Module K E]
    (C : A →ₗ[K] K) (L : E →ₗ[K] A) (Q : A)
    (hzero : ∀ v, C ((L v) ^ 2 * Q) = 0) (v w : E) :
    C (L v * L w * Q) = 0 := by
  have hexpand : L (v + w) ^ 2 * Q =
      L v ^ 2 * Q + L w ^ 2 * Q + (2 : K) • (L v * L w * Q) := by
    rw [map_add]
    simp only [Algebra.smul_def, map_ofNat]
    ring
  have h := hzero (v + w)
  rw [hexpand, map_add, map_add, map_smul, hzero v, hzero w] at h
  simp only [zero_add, smul_eq_mul] at h
  exact (mul_eq_zero.mp h).resolve_left (by norm_num)

end KrennAllOrders.OmissionCancellation
