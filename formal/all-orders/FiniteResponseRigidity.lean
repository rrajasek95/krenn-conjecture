/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import Mathlib.Algebra.Polynomial.Degree.Lemmas
import Mathlib.Algebra.MvPolynomial.Funext

/-!
# Finite response rigidity under a replica rotation

The scalar factor in the odd-response argument satisfies
`g(s L)^2 = g(L)` for a nonzero scalar `s`, and `g(0) = 1`.
A finite polynomial with these properties is identically one. The derivation
of this functional equation from the physical source is a separate obligation.
-/

namespace KrennAllOrders.FiniteResponseRigidity

variable {K σ : Type*} [CommRing K] [IsDomain K]

theorem polynomial_eq_one_of_rescaling_square (p : Polynomial K) (s : K)
    (hs : s ≠ 0) (hzero : p.eval 0 = 1)
    (h : (p.comp (Polynomial.C s * Polynomial.X)) ^ 2 = p) : p = 1 := by
  have hd := congrArg Polynomial.natDegree h
  rw [Polynomial.natDegree_pow, Polynomial.natDegree_comp,
    Polynomial.natDegree_C_mul_X s hs, mul_one] at hd
  have hp : p = Polynomial.C (p.coeff 0) :=
    Polynomial.eq_C_of_natDegree_eq_zero (by omega)
  have hc : p.coeff 0 = 1 := by
    rw [Polynomial.coeff_zero_eq_eval_zero]
    exact hzero
  simpa only [hc, Polynomial.C_1] using hp

/-- Evaluate a multivariate polynomial on the formal line through a vector. -/
noncomputable def lineMap (x : σ → K) : MvPolynomial σ K →+* Polynomial K :=
  MvPolynomial.eval₂Hom Polynomial.C (fun i => Polynomial.C (x i) * Polynomial.X)

/-- Simultaneous scalar substitution in all variables. -/
noncomputable def scaleVariables (s : K) : MvPolynomial σ K →+* MvPolynomial σ K :=
  MvPolynomial.eval₂Hom MvPolynomial.C (fun i => MvPolynomial.C s * MvPolynomial.X i)

omit [IsDomain K] in
theorem lineMap_scaleVariables (x : σ → K) (s : K) (g : MvPolynomial σ K) :
    lineMap x (scaleVariables s g) =
      (lineMap x g).comp (Polynomial.C s * Polynomial.X) := by
  have hhom : (lineMap x).comp (scaleVariables s) =
      (Polynomial.compRingHom (Polynomial.C s * Polynomial.X)).comp (lineMap x) := by
    ext <;> simp [lineMap, scaleVariables, mul_left_comm]
  exact RingHom.congr_fun hhom g

omit [IsDomain K] in
theorem eval_lineMap (x : σ → K) (t : K) (g : MvPolynomial σ K) :
    (lineMap x g).eval t = MvPolynomial.eval (fun i => x i * t) g := by
  have hhom : (Polynomial.evalRingHom t).comp (lineMap x) =
      MvPolynomial.eval (fun i => x i * t) := by
    ext <;> simp [lineMap]
  exact RingHom.congr_fun hhom g

/-- Every vector is a specialization of its formal line, so the univariate
degree argument proves the full multivariate identity. -/
theorem eq_one_of_rescaling_square [Infinite K] (g : MvPolynomial σ K) (s : K)
    (hs : s ≠ 0) (hzero : MvPolynomial.eval (fun _ => 0) g = 1)
    (h : (scaleVariables s g) ^ 2 = g) : g = 1 := by
  apply MvPolynomial.funext
  intro x
  have hline : lineMap x g = 1 := by
    apply polynomial_eq_one_of_rescaling_square _ s hs
    · simpa only [eval_lineMap, mul_zero] using hzero
    · have hh := congrArg (lineMap x) h
      simpa only [map_pow, lineMap_scaleVariables] using hh
  have hx := congrArg (Polynomial.eval 1) hline
  simpa only [eval_lineMap, mul_one, Polynomial.eval_one, map_one] using hx

end KrennAllOrders.FiniteResponseRigidity
