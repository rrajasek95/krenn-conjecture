/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import EvenResponse
import BinaryPairing

/-! # Differentiating the finite signed-complement contraction -/

namespace KrennAllOrders.PairingDerivative

open scoped BigOperators
open BinaryPairing

variable {ι R S σ : Type*} [Fintype ι] [CommRing R] [CommRing S]

/-- The alternating sign is preserved under scalar ring maps. -/
theorem map_sign (f : R →+* S) (w : ι → Bool) :
    f (sign w) = sign w := by
  simp only [sign, map_prod]
  apply Finset.prod_congr rfl
  intro i _
  split_ifs <;> simp

/-- Evaluation and scalar extension commute with the actual finite pairing. -/
theorem map_pairing (f : R →+* S) (E F : Tensor ι R) :
    f (pairing E F) = pairing (fun w => f (E w)) (fun w => f (F w)) := by
  simp only [pairing, map_sum, map_mul, map_sign]

/-- The formal derivative of the signed finite contraction is its exact
bilinear product rule. -/
theorem pderiv_pairing (z : σ) (E F : Tensor ι (MvPolynomial σ R)) :
    MvPolynomial.pderiv z (pairing E F) =
      pairing (fun w => MvPolynomial.pderiv z (E w)) F +
      pairing E (fun w => MvPolynomial.pderiv z (F w)) := by
  classical
  have hsign (w : ι → Bool) : (sign w : MvPolynomial σ R) = MvPolynomial.C (sign w : R) :=
    (map_sign MvPolynomial.C w).symm
  simp only [pairing, hsign, map_sum, MvPolynomial.pderiv_mul,
    MvPolynomial.pderiv_C, zero_mul, zero_add, Finset.sum_add_distrib]

/-- On an even number of physical sites the two differentiated terms agree. -/
theorem pderiv_pairing_self_even (heven : Even (Fintype.card ι))
    (z : σ) (E : Tensor ι (MvPolynomial σ R)) :
    MvPolynomial.pderiv z (pairing E E) =
      2 * pairing E (fun w => MvPolynomial.pderiv z (E w)) := by
  rw [pderiv_pairing, pairing_symmetric_of_even heven
    (fun w => MvPolynomial.pderiv z (E w)) E]
  ring

/-- Differentiating the actual norm-two rotation identity gives the normalized
identity used to cancel the direct omitted-root term. -/
theorem differentiated_norm_two_rotation {K : Type*} [Field K] [CharZero K]
    (heven : Even (Fintype.card ι)) (z : σ) (s : K) (hsq : s * s = 2)
    (E F Es V Vs : Tensor ι (MvPolynomial σ K))
    (hE : ∀ w, MvPolynomial.pderiv z (E w) = V w)
    (hF : ∀ w, MvPolynomial.pderiv z (F w) = 0)
    (hEs : ∀ w, MvPolynomial.pderiv z (Es w) = MvPolynomial.C s * Vs w)
    (hrotation : pairing E E = pairing F Es) :
    MvPolynomial.C s * pairing E V = pairing F Vs := by
  have h := congrArg (MvPolynomial.pderiv z) hrotation
  rw [pderiv_pairing_self_even heven, pderiv_pairing] at h
  have he : (fun w => MvPolynomial.pderiv z (E w)) = V := funext hE
  have hf : (fun w => MvPolynomial.pderiv z (F w)) = 0 := funext hF
  have hes : (fun w => MvPolynomial.pderiv z (Es w)) = (MvPolynomial.C s : MvPolynomial σ K) • Vs := by
    funext w
    simpa only [Pi.smul_apply, smul_eq_mul] using hEs w
  rw [he, hf, hes, pairing_smul_right] at h
  have hz : pairing (0 : Tensor ι (MvPolynomial σ K)) Es = 0 := by simp [pairing]
  rw [hz, zero_add] at h
  have hs : s ≠ 0 := by
    intro hs
    simp [hs] at hsq
  have hCs : (MvPolynomial.C s : MvPolynomial σ K) ≠ 0 := MvPolynomial.C_ne_zero.mpr hs
  apply mul_left_cancel₀ hCs
  calc
    MvPolynomial.C s * (MvPolynomial.C s * pairing E V) = 2 * pairing E V := by
      rw [← mul_assoc, ← map_mul, hsq, map_ofNat]
    _ = _ := h

end KrennAllOrders.PairingDerivative
