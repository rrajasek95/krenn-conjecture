/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import WholeBinaryResponse
import EndpointSource

/-! # Original binary response consequences of the complex source equations -/

namespace KrennAllOrders.BinarySourceInterface

open MatchingModel SiteAlgebra RootResponse RetainedBinary

/-- The endpoint's palette-scoped source input follows from the graph equations. -/
theorem originalHigherZeroOnPalette (m : ℕ)
    (W : WeightsN (2 * (m + 1)) 3 ℂ) (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p : V (2 * (m + 1))) (b h : Fin 3) :
    EndpointSource.OriginalHigherZeroOnPalette m W p b h := by
  intro ι hι r hpos hr
  apply WholeBinaryResponse.whole_binary_response_zero m r hr hpos W hW p ι
  exact ⟨b, h, fun v _ => hι v⟩

/-- Extending a retained binary word at omitted roots preserves its palette. -/
theorem receivingWord_onPalette {N D : ℕ} (p q : V N) (b h : Fin D)
    (w : RetainedSites p q → Bool) : EndpointSource.OnPalette (receivingWord p q b h w) b h := by
  intro v
  unfold receivingWord
  split_ifs <;> simp

/-- The exact higher-response input to the omitted tensor, with no response
hypothesis left beyond the original equation system. -/
theorem omitted_higher_zero (m : ℕ)
    (W : WeightsN (2 * (m + 1)) 3 ℂ) (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p q : V (2 * (m + 1))) (b h : Fin 3) (w : RetainedSites p q → Bool)
    (r : ℕ) (hpos : 0 < r) (hr : r ≤ m) :
    OddResponseVanishing.oddResponsePolynomial W p m r (receivingWord p q b h w) = 0 :=
  originalHigherZeroOnPalette m W hW p b h _ (receivingWord_onPalette p q b h w) r hpos hr

/-- A concrete square-root-of-two scale from the checked normalized rotation. -/
noncomputable def normTwo : ℂ := 2 * WholeBinaryResponse.halfRotation

theorem normTwo_sq : normTwo * normTwo = 2 := by
  have h := WholeBinaryResponse.halfRotation_normalized
  unfold normTwo
  linear_combination 2 * h

end KrennAllOrders.BinarySourceInterface
