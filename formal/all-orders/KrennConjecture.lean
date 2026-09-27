/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import PhysicalClosure
import WholeBinaryResponse
import EndpointCovariance
import BinarySourceInterface
import DiagonalSource
import Mathlib.Analysis.Complex.Polynomial.Basic

/-!
# Assembly of the all-orders ternary equation-system contradiction

The physical source is the canonical weighted matching equation system.
The final contradiction is assembled from proved original-source response,
diagonalisation, and endpoint identities; auxiliary rotation parameters are
fixed explicitly in the complex field.
-/

namespace KrennAllOrders.KrennConjecture

open MatchingModel SiteAlgebra RootResponse

/-- Every even order in the conjecture's range has the exact retained-core
form used by the physical covariance and omission modules. -/
theorem exists_retained_size {N : ℕ} (hN : 6 ≤ N) (heven : Even N) :
    ∃ k : ℕ, N = 2 * (k + 2) := by
  obtain ⟨m, hm⟩ := heven
  refine ⟨m - 2, ?_⟩
  omega

/-- The rotation parameter used in the physical whole-response theorem is
the concrete scalar `sqrt(2)/2`, with its exact norm-one identity proved. -/
theorem complex_rotation_normalization :
    WholeBinaryResponse.halfRotation * WholeBinaryResponse.halfRotation +
      WholeBinaryResponse.halfRotation * WholeBinaryResponse.halfRotation = 1 :=
  WholeBinaryResponse.halfRotation_normalized

/-- Once the original source has diagonal colour blocks, every supported edge
has its exact actual hafnian cofactor product equal to the pure target one.
No retained-source or endpoint response identity is assumed. -/
theorem supported_endpoint_of_diagonal_eqSystem (m : ℕ)
    (W : WeightsN (2 * (m + 1)) 3 ℂ) (hW : EqSystemN (2 * (m + 1)) 3 W)
    (hdiag : EndpointSource.DiagonalSource W) (b : Fin 3)
    (p q : V (2 * (m + 1))) (hd : edgeMatrix W (p, b) (q, b) ≠ 0) :
    edgeMatrix W (p, b) (q, b) * pureCofactor W b p q = 1 := by
  have hpq : p ≠ q := by
    intro hpq
    subst q
    exact hd (edgeMatrix_same_site W p b b)
  obtain ⟨h, hhb, _⟩ := WholeBinaryResponse.exists_third_colour b b
  exact EndpointCovariance.supported_endpoint_from_original_binary_responses m W hW
    hdiag p q hpq b h hhb.symm
    (BinarySourceInterface.originalHigherZeroOnPalette m W hW p b h)
    (BinarySourceInterface.originalHigherZeroOnPalette m W hW q b h) hd

/-- The original complex ternary equation system has no solution at any even
order at least six. All response, diagonal, endpoint, and graph identities
used here are proved from that original equation system. -/
theorem not_eqSystemN_three {N : ℕ} (hN : 6 ≤ N) (heven : Even N)
    (W : WeightsN N 3 ℂ) : ¬ EqSystemN N 3 W := by
  obtain ⟨k, hsize⟩ := exists_retained_size hN heven
  subst N
  intro hW
  have hdiag := DiagonalSource.diagonal_of_eqSystem k W hW
  exact PhysicalClosure.not_eqSystemN_of_diagonal_and_endpoint hN heven W hdiag
    (fun i p q hd =>
      supported_endpoint_of_diagonal_eqSystem (k + 1) W hW hdiag i p q hd) hW

/-- Existential form of the unconditional ternary nonexistence theorem. -/
theorem not_exists_eqSystemN_three {N : ℕ} (hN : 6 ≤ N) (heven : Even N) :
    ¬ ∃ W : WeightsN N 3 ℂ, EqSystemN N 3 W := by
  rintro ⟨W, hW⟩
  exact not_eqSystemN_three hN heven W hW

end KrennAllOrders.KrennConjecture
