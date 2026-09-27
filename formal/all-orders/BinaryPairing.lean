/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Fintype.Pi
import Mathlib.Algebra.Module.Pi
import Mathlib.Algebra.Ring.Parity
import Mathlib.LinearAlgebra.BilinearMap
import Mathlib.Tactic.Ring

/-! # The finite binary alternating pairing on receiving tensors -/

namespace KrennAllOrders.BinaryPairing

open scoped BigOperators Classical

variable {ι R : Type*} [Fintype ι] [CommRing R]

abbrev Tensor (ι R : Type*) := (ι → Bool) → R

def complement (w : ι → Bool) : ι → Bool := fun i => !(w i)

omit [Fintype ι] in
@[simp] theorem complement_complement (w : ι → Bool) : complement (complement w) = w := by
  funext i
  exact Bool.not_not (w i)

def complementEquiv : (ι → Bool) ≃ (ι → Bool) where
  toFun := complement
  invFun := complement
  left_inv := complement_complement
  right_inv := complement_complement

def sign (w : ι → Bool) : R := ∏ i, if w i then (-1 : R) else 1

noncomputable def pairing (P Q : Tensor ι R) : R :=
  ∑ w : ι → Bool, sign w * P w * Q (complement w)

@[simp] theorem sign_false : sign (fun _ : ι => false) = (1 : R) := by simp [sign]

@[simp] theorem sign_true : sign (fun _ : ι => true) = (-1 : R) ^ Fintype.card ι := by
  simp [sign]

theorem sign_complement (w : ι → Bool) :
    sign (complement w) = (-1 : R) ^ Fintype.card ι * sign w := by
  have heach (i : ι) : (if complement w i then (-1 : R) else 1) =
      (-1 : R) * (if w i then -1 else 1) := by
    cases h : w i <;> simp [complement, h]
  simp only [sign, heach, Finset.prod_mul_distrib, Finset.prod_const, Finset.card_univ]

/-- Swapping tensors contributes one minus sign for each physical site. -/
theorem pairing_swap (P Q : Tensor ι R) :
    pairing Q P = (-1 : R) ^ Fintype.card ι * pairing P Q := by
  rw [pairing, ← Equiv.sum_comp (complementEquiv (ι := ι))]
  change (∑ w : ι → Bool, sign (complement w) * Q (complement w) *
    P (complement (complement w))) = _
  simp only [sign_complement, complement_complement]
  rw [pairing, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro w _
  ring

theorem pairing_add_left (P Q U : Tensor ι R) :
    pairing (P + Q) U = pairing P U + pairing Q U := by
  simp only [pairing, Pi.add_apply, mul_add, add_mul, Finset.sum_add_distrib]

theorem pairing_add_right (P Q U : Tensor ι R) :
    pairing P (Q + U) = pairing P Q + pairing P U := by
  simp only [pairing, Pi.add_apply, mul_add, Finset.sum_add_distrib]

theorem pairing_smul_left (c : R) (P Q : Tensor ι R) :
    pairing (c • P) Q = c * pairing P Q := by
  simp only [pairing, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro w _
  ring

theorem pairing_smul_right (c : R) (P Q : Tensor ι R) :
    pairing P (c • Q) = c * pairing P Q := by
  simp only [pairing, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro w _
  ring

/-- A pure receiving tensor, with value one on the constant word and zero elsewhere. -/
noncomputable def pure (b : Bool) : Tensor ι R := fun w => if w = (fun _ => b) then 1 else 0

theorem pairing_pure_left (b : Bool) (P : Tensor ι R) :
    pairing (pure b) P = sign (fun _ : ι => b) * P (fun _ => !b) := by
  classical
  simp only [pairing, pure]
  rw [Finset.sum_eq_single (fun _ : ι => b)]
  · simp only [ite_true, mul_one]
    rfl
  · intro w _ hw
    simp [hw]
  · simp

theorem pairing_pure_false (P : Tensor ι R) : pairing (pure false) P = P (fun _ => true) := by
  rw [pairing_pure_left]
  simp

theorem pairing_pure_true (P : Tensor ι R) :
    pairing (pure true) P = (-1 : R) ^ Fintype.card ι * P (fun _ => false) := by
  rw [pairing_pure_left]
  simp

omit [Fintype ι] in
theorem complement_eq_constant_iff (w : ι → Bool) (b : Bool) :
    complement w = (fun _ => b) ↔ w = (fun _ => !b) := by
  have h : complement (fun _ : ι => !b) = (fun _ => b) := by
    funext i
    exact Bool.not_not b
  constructor
  · intro hw
    exact (complementEquiv (ι := ι)).injective (hw.trans h.symm)
  · intro hw
    rw [hw, h]

theorem pairing_pure_right (P : Tensor ι R) (b : Bool) :
    pairing P (pure b) = sign (fun _ : ι => !b) * P (fun _ => !b) := by
  classical
  simp only [pairing, pure, complement_eq_constant_iff]
  rw [Finset.sum_eq_single (fun _ : ι => !b)]
  · simp
  · intro w _ hw
    simp [hw]
  · simp

theorem pairing_right_pure_true (P : Tensor ι R) :
    pairing P (pure true) = P (fun _ => false) := by
  rw [pairing_pure_right]
  simp

theorem pairing_right_pure_false (P : Tensor ι R) :
    pairing P (pure false) = (-1 : R) ^ Fintype.card ι * P (fun _ => true) := by
  rw [pairing_pure_right]
  simp

/-- The literal finite sum is bilinear, allowing tensor coefficients in any
commutative ring, including the row-parameter polynomial ring. -/
noncomputable def bilinearPairing : Tensor ι R →ₗ[R] Tensor ι R →ₗ[R] R where
  toFun P := {
    toFun := pairing P
    map_add' Q U := pairing_add_right P Q U
    map_smul' c Q := pairing_smul_right c P Q }
  map_add' P Q := by
    ext U
    exact pairing_add_left P Q U
  map_smul' c P := by
    ext Q
    exact pairing_smul_left c P Q

/-- On the two pure receiving words the contraction is a two-by-two form,
with the sign determined by the number of physical sites. -/
theorem pairing_pure_combinations [Nonempty ι] (a b c d : R) :
    pairing (a • pure false + b • pure true : Tensor ι R)
      (c • pure false + d • pure true) = a * d + (-1 : R) ^ Fintype.card ι * b * c := by
  rw [pairing_add_left, pairing_smul_left, pairing_smul_left,
    pairing_pure_false, pairing_pure_true]
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  simp only [pure, funext_iff, Bool.false_eq_true, Bool.true_eq_false,
    forall_const, ite_false, ite_true, mul_zero, mul_one, zero_add, add_zero]
  ring

theorem pairing_pure_combinations_odd [Nonempty ι] (hodd : Odd (Fintype.card ι))
    (a b c d : R) :
    pairing (a • pure false + b • pure true : Tensor ι R)
      (c • pure false + d • pure true) = a * d - b * c := by
  rw [pairing_pure_combinations, hodd.neg_one_pow]
  ring

theorem pairing_symmetric_of_even (heven : Even (Fintype.card ι)) (P Q : Tensor ι R) :
    pairing P Q = pairing Q P := by
  rw [pairing_swap, heven.neg_one_pow, one_mul]

end KrennAllOrders.BinaryPairing
