/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import SiteAlgebra
import Mathlib.LinearAlgebra.Matrix.SemiringInverse

/-! # Cofactor identities force diagonal endpoint-colour blocks -/

namespace KrennAllOrders.CofactorDiagonal

open MatchingModel SiteAlgebra
open scoped BigOperators

variable {R V C : Type*} [CommRing R] [Fintype V] [DecidableEq V]

/-- A common right factor with a left inverse cannot annihilate a nonzero
square block. The one-sided inverse is upgraded by finite matrix algebra. -/
theorem block_eq_zero_of_cofactor_identity
    (A B Q : Matrix V V R) (hAQ : A * Q = 1) (hBQ : B * Q = 0) : B = 0 := by
  have hQA : Q * A = 1 := mul_eq_one_comm.mp hAQ
  calc
    B = B * (Q * A) := by rw [hQA, mul_one]
    _ = (B * Q) * A := (mul_assoc B Q A).symm
    _ = 0 := by rw [hBQ, zero_mul]

/-- If the monochromatic and mixed blocks have the stated cofactor products,
every off-diagonal colour block vanishes. -/
theorem offDiagonal_eq_zero (B : C → C → Matrix V V R) (Q : C → Matrix V V R)
    (hdiag : ∀ h, B h h * Q h = 1)
    (hmixed : ∀ i h, i ≠ h → B i h * Q h = 0) {i h : C} (hih : i ≠ h) :
    B i h = 0 :=
  block_eq_zero_of_cofactor_identity (B h h) (B i h) (Q h) (hdiag h) (hmixed i h hih)

variable {N D : ℕ}

/-- The actual ordered-endpoint source represented by its colour blocks. -/
noncomputable def sourceBlock (W : WeightsN N D R) (i h : Fin D) :
    Matrix (Fin N) (Fin N) R := fun p q => edgeMatrix W (p, i) (q, h)

/-- Entrywise pure and mixed cofactor sums give the physical diagonal reduction.
The cofactor sum premises must be supplied by the source response identities. -/
theorem source_diagonal_of_cofactor_sums (W : WeightsN N D R)
    (Q : Fin D → Matrix (Fin N) (Fin N) R)
    (hpure : ∀ h p q, ∑ r, edgeMatrix W (p, h) (r, h) * Q h r q =
      if p = q then 1 else 0)
    (hmixed : ∀ i h, i ≠ h → ∀ p q,
      ∑ r, edgeMatrix W (p, i) (r, h) * Q h r q = 0) :
    ∀ p q i h, i ≠ h → edgeMatrix W (p, i) (q, h) = 0 := by
  have hd : ∀ h, sourceBlock W h h * Q h = 1 := by
    intro h
    ext p q
    exact hpure h p q
  have hm : ∀ i h, i ≠ h → sourceBlock W i h * Q h = 0 := by
    intro i h hih
    ext p q
    exact hmixed i h hih p q
  intro p q i h hih
  exact congrFun (congrFun (offDiagonal_eq_zero (sourceBlock W) Q hd hm hih) p) q

end KrennAllOrders.CofactorDiagonal
