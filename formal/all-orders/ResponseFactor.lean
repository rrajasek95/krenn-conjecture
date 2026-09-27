/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import Mathlib.Algebra.MvPolynomial.Division
import Mathlib.Algebra.MvPolynomial.NoZeroDivisors

/-!
# The common scalar factor in the odd-response argument

For the actual three-row family at a source root, the three linear responses
are independent coordinate variables after rescaling by their nonzero pure
amplitudes. Reflection gives cross-multiplication identities for the pure
higher responses. This file proves their common-factor consequence for any
family with two distinct coordinates. The reflection identities themselves
remain hypotheses until the physical Wick construction is instantiated.
-/

namespace KrennAllOrders.ResponseFactor

variable {K σ : Type*} [CommRing K] [IsDomain K]

/-- Coordinatewise proportional polynomial responses share a polynomial factor;
division by a coordinate does not introduce rational functions. -/
theorem exists_common_factor (H : σ → MvPolynomial σ K)
    {a b : σ} (hab : a ≠ b)
    (hcross : ∀ i j, MvPolynomial.X i * H j = MvPolynomial.X j * H i) :
    ∃ q : MvPolynomial σ K, ∀ i, H i = MvPolynomial.X i * q := by
  have hd : MvPolynomial.X a ∣ MvPolynomial.X b * H a := by
    rw [← hcross a b]
    exact dvd_mul_right _ _
  have hda : MvPolynomial.X a ∣ H a :=
    (MvPolynomial.X_dvd_mul_iff.mp hd).resolve_left (by simpa using hab)
  obtain ⟨q, hq⟩ := hda
  refine ⟨q, fun i => ?_⟩
  apply mul_left_cancel₀ (MvPolynomial.X_ne_zero (R := K) a)
  calc
    MvPolynomial.X a * H i = MvPolynomial.X i * H a := hcross a i
    _ = MvPolynomial.X a * (MvPolynomial.X i * q) := by rw [hq]; ring

theorem common_factor_unique (H : σ → MvPolynomial σ K) {a : σ}
    {q r : MvPolynomial σ K}
    (hq : H a = MvPolynomial.X a * q) (hr : H a = MvPolynomial.X a * r) : q = r :=
  mul_left_cancel₀ (MvPolynomial.X_ne_zero a) (hq.symm.trans hr)

/-- The one surviving complementary pure word forces a mixed response to vanish. -/
theorem mixed_response_eq_zero {H f : MvPolynomial σ K}
    (hf : f ≠ 0) (hreflection : f * H = 0) : H = 0 :=
  (mul_eq_zero.mp hreflection).resolve_left hf

end KrennAllOrders.ResponseFactor
