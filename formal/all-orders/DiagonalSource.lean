/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import OmissionConstancy
import BinarySourceInterface

/-! # Global diagonal reduction of the original complex weighted source

The only hypothesis is the original graph equation system. The whole binary
response theorem supplies the finite source identity, actual replica rotation
forces pure even-response constancy, and degree extraction/polarization gives
the cofactor matrix identities for the original weights.
-/

namespace KrennAllOrders.DiagonalSource

open MatchingModel SiteAlgebra

/-- Every complex ternary source on at least four even vertices has zero
aggregate weights between distinct endpoint colours. -/
theorem diagonal_of_eqSystem (k : ℕ) (W : WeightsN (2 * (k + 2)) 3 ℂ)
    (hW : EqSystemN (2 * (k + 2)) 3 W) :
    ∀ p q i h, i ≠ h → edgeMatrix W (p, i) (q, h) = 0 := by
  apply CofactorResponse.source_diagonal_of_omission_vanishing k W hW
  intro p q hpq i h
  obtain ⟨j, hjh⟩ := exists_ne h
  apply OmissionDegree.omitted_two_row_zero_of_pure_even_constancy k W p q i h
  intro a
  exact OmissionConstancy.pure_even_constancy (k + 1) W hW p q hpq h j hjh.symm
    BinarySourceInterface.normTwo BinarySourceInterface.normTwo_sq
    (fun w r hpos hr => BinarySourceInterface.omitted_higher_zero
      (k + 1) W hW p q h j w r hpos hr) a

end KrennAllOrders.DiagonalSource
