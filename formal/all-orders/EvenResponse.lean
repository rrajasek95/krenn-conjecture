/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import RootResponse
import Mathlib.Tactic.FieldSimp

/-! # Finite Gaussian response polynomials and their omission formulas -/

namespace KrennAllOrders.EvenResponse

open MatchingModel SiteAlgebra

open scoped BigOperators

variable {K A σ : Type*} [Field K] [CharZero K] [CommRing A] [Algebra K A]

/-- Divided powers use inverses in the scalar field, so the coefficient algebra
may itself be a parameter polynomial ring or a physical-site quotient. -/
noncomputable def dividedPower (P : MvPolynomial σ A) (n : ℕ) : MvPolynomial σ A :=
  MvPolynomial.C (algebraMap K A ((n.factorial : K)⁻¹)) * P ^ n

omit [CharZero K] in
@[simp] theorem dividedPower_zero (P : MvPolynomial σ A) :
    dividedPower (K := K) P 0 = 1 := by simp [dividedPower]

theorem factorial_inverse_succ (n : ℕ) :
    (((n + 1).factorial : K)⁻¹) * (n + 1 : K) = (n.factorial : K)⁻¹ := by
  have hn : (n + 1 : K) ≠ 0 := Nat.cast_add_one_ne_zero n
  have hf : (n.factorial : K) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero n)
  rw [Nat.factorial_succ, Nat.cast_mul, Nat.cast_add, Nat.cast_one]
  field_simp

theorem pderiv_dividedPower_succ (P : MvPolynomial σ A) (z : σ) (n : ℕ) :
    MvPolynomial.pderiv z (dividedPower (K := K) P (n + 1)) =
      dividedPower (K := K) P n * MvPolynomial.pderiv z P := by
  have hscalar : algebraMap K A (((n + 1).factorial : K)⁻¹) * (n + 1 : A) =
      algebraMap K A ((n.factorial : K)⁻¹) := by
    simpa only [map_mul, map_add, map_natCast, map_one] using
      congrArg (algebraMap K A) (factorial_inverse_succ (K := K) n)
  simp only [dividedPower, MvPolynomial.pderiv_C_mul, Derivation.leibniz_pow,
    Nat.add_sub_cancel, smul_eq_mul]
  have hC : MvPolynomial.C (algebraMap K A (((n + 1).factorial : K)⁻¹)) *
      MvPolynomial.C (n + 1 : A) =
      (MvPolynomial.C (algebraMap K A ((n.factorial : K)⁻¹)) : MvPolynomial σ A) := by
    rw [← map_mul, hscalar]
  calc
    _ = (MvPolynomial.C (algebraMap K A (((n + 1).factorial : K)⁻¹)) *
      MvPolynomial.C (n + 1 : A)) * P ^ n * MvPolynomial.pderiv z P := by
        simp only [map_add, map_natCast, map_one]
        ring
    _ = _ := by rw [hC]

/-- The finite odd shifted response on `2m+1` retained sites. -/
noncomputable def oddResponse (m : ℕ) (Q L : MvPolynomial σ A) : MvPolynomial σ A :=
  ∑ r ∈ Finset.range (m + 1),
    dividedPower (K := K) L (2 * r + 1) * dividedPower (K := K) Q (m - r)

/-- The finite even shifted response on `2m` retained sites. -/
noncomputable def evenResponse (m : ℕ) (Q L : MvPolynomial σ A) : MvPolynomial σ A :=
  ∑ r ∈ Finset.range (m + 1),
    dividedPower (K := K) L (2 * r) * dividedPower (K := K) Q (m - r)

/-- The odd response one site below `evenResponse`, with an empty sum at zero. -/
noncomputable def lowerOddResponse (m : ℕ) (Q L : MvPolynomial σ A) : MvPolynomial σ A :=
  ∑ r ∈ Finset.range m,
    dividedPower (K := K) L (2 * r + 1) * dividedPower (K := K) Q (m - 1 - r)

omit [CharZero K] in
theorem lowerOddResponse_succ (m : ℕ) (Q L : MvPolynomial σ A) :
    lowerOddResponse (K := K) (m + 1) Q L = oddResponse (K := K) m Q L := by
  simp only [lowerOddResponse, oddResponse, Nat.add_sub_cancel]

/-- Differentiating the finite odd response gives exactly its two even-core
contributions, including the terminal divided power. -/
theorem pderiv_oddResponse (m : ℕ) (Q L : MvPolynomial σ A) (z : σ) :
    MvPolynomial.pderiv z (oddResponse (K := K) m Q L) =
      MvPolynomial.pderiv z L * evenResponse (K := K) m Q L +
      MvPolynomial.pderiv z Q * lowerOddResponse (K := K) m Q L := by
  classical
  unfold oddResponse
  simp only [map_sum, MvPolynomial.pderiv_mul, pderiv_dividedPower_succ,
    Finset.sum_add_distrib]
  congr 1
  · simp only [evenResponse, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro r _
    ring
  · rw [Finset.sum_range_succ]
    simp only [Nat.sub_self, dividedPower_zero, MvPolynomial.pderiv_one, mul_zero, add_zero]
    simp only [lowerOddResponse, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro r hr
    have hrm : r < m := Finset.mem_range.mp hr
    have hpow : m - r = (m - 1 - r) + 1 := by omega
    rw [hpow, pderiv_dividedPower_succ]
    ring

/-- Mean differentiation of the finite even response is its lower odd response. -/
theorem pderiv_evenResponse_of_pderiv_quadratic_zero
    (m : ℕ) (Q L : MvPolynomial σ A) (z : σ)
    (hQ : MvPolynomial.pderiv z Q = 0) :
    MvPolynomial.pderiv z (evenResponse (K := K) m Q L) =
      MvPolynomial.pderiv z L * lowerOddResponse (K := K) m Q L := by
  classical
  have hDQ : ∀ n, MvPolynomial.pderiv z (dividedPower (K := K) Q n) = 0 := by
    intro n
    cases n with
    | zero => simp
    | succ n => rw [pderiv_dividedPower_succ, hQ, mul_zero]
  unfold evenResponse
  simp only [map_sum, MvPolynomial.pderiv_mul, hDQ, mul_zero, add_zero]
  rw [Finset.sum_range_succ']
  simp only [Nat.mul_zero, dividedPower_zero, MvPolynomial.pderiv_one, zero_mul, add_zero]
  simp only [lowerOddResponse, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro r _
  have heven : 2 * (r + 1) = (2 * r + 1) + 1 := by omega
  have hsub : m - (r + 1) = m - 1 - r := by omega
  rw [heven, pderiv_dividedPower_succ, hsub]
  ring

section Maps

variable {B τ : Type*} [CommRing B] [Algebra K B]
    (f : MvPolynomial σ A →+* MvPolynomial τ B)
    (hf : ∀ a : K, f (MvPolynomial.C (algebraMap K A a)) =
      MvPolynomial.C (algebraMap K B a))

include hf

omit [CharZero K] in
theorem map_dividedPower (P : MvPolynomial σ A) (n : ℕ) :
    f (dividedPower (K := K) P n) = dividedPower (K := K) (f P) n := by
  simp only [dividedPower, map_mul, map_pow, hf]

omit [CharZero K] in
theorem map_oddResponse (m : ℕ) (Q L : MvPolynomial σ A) :
    f (oddResponse (K := K) m Q L) = oddResponse (K := K) m (f Q) (f L) := by
  simp only [oddResponse, map_sum, map_mul, map_dividedPower f hf]

omit [CharZero K] in
theorem map_evenResponse (m : ℕ) (Q L : MvPolynomial σ A) :
    f (evenResponse (K := K) m Q L) = evenResponse (K := K) m (f Q) (f L) := by
  simp only [evenResponse, map_sum, map_mul, map_dividedPower f hf]

omit [CharZero K] in
theorem map_lowerOddResponse (m : ℕ) (Q L : MvPolynomial σ A) :
    f (lowerOddResponse (K := K) m Q L) =
      lowerOddResponse (K := K) m (f Q) (f L) := by
  simp only [lowerOddResponse, map_sum, map_mul, map_dividedPower f hf]

end Maps

/-- Literal extraction of another physical site, with every colour at that site
erased afterwards. Both terms are derived from the original finite odd sum. -/
theorem rootExtract_oddResponse {N D : ℕ} (m : ℕ)
    (Q L : MatchingPolynomial N D A) (q : V N) (h : Fin D) :
    RootResponse.rootExtract q h (oddResponse (K := K) m Q L) =
      RootResponse.rootExtract q h L *
        evenResponse (K := K) m (RootResponse.eraseSite q Q) (RootResponse.eraseSite q L) +
      RootResponse.rootExtract q h Q *
        lowerOddResponse (K := K) m (RootResponse.eraseSite q Q)
          (RootResponse.eraseSite q L) := by
  simp only [RootResponse.rootExtract, pderiv_oddResponse, map_add, map_mul,
    map_evenResponse (RootResponse.eraseSite q) (fun _ => RootResponse.eraseSite_C q _),
    map_lowerOddResponse (RootResponse.eraseSite q) (fun _ => RootResponse.eraseSite_C q _)]

section RootAlgebra

variable {R : Type*} [Field R] {N D : ℕ}

/-- Deletion and differentiation commute at distinct physical sites. -/
theorem pderiv_eraseSite_of_ne (P : MatchingPolynomial N D R)
    (p q : V N) (h : Fin D) (hpq : p ≠ q) :
    MvPolynomial.pderiv (q, h) (RootResponse.eraseSite p P) =
      RootResponse.eraseSite p (MvPolynomial.pderiv (q, h) P) := by
  classical
  induction P using MvPolynomial.induction_on with
  | C a => simp
  | add P Q hP hQ => simp only [map_add, hP, hQ]
  | mul_X P z hP =>
    by_cases hz : z.1 = p
    · have hzq : (q, h) ≠ z := by
        intro heq
        have := congrArg Prod.fst heq
        exact hpq (hz.symm.trans this.symm)
      simp [RootResponse.eraseSite_X, hz, MvPolynomial.pderiv_X, hzq]
    · simp only [map_mul, RootResponse.eraseSite_X, if_neg hz,
        MvPolynomial.pderiv_mul, map_add, hP]
      by_cases heq : (q, h) = z
      · simp [MvPolynomial.pderiv_X, heq]
      · simp [MvPolynomial.pderiv_X, heq]

/-- The derivative of an actual source row is its literal matrix entry. -/
theorem pderiv_rowPolynomial
    (S : SiteVariable N D → SiteVariable N D → R) (z t : SiteVariable N D) :
    MvPolynomial.pderiv t (rowPolynomial S z) = MvPolynomial.C (S z t) := by
  classical
  simp [rowPolynomial, MvPolynomial.pderiv_X, Pi.single_apply]

/-- A row contributes precisely the direct edge when another site is extracted. -/
theorem rootExtract_rowPolynomial
    (S : SiteVariable N D → SiteVariable N D → R) (z : SiteVariable N D)
    (q : V N) (h : Fin D) :
    RootResponse.rootExtract q h (rowPolynomial S z) = MvPolynomial.C (S z (q, h)) := by
  rw [RootResponse.rootExtract, pderiv_rowPolynomial, RootResponse.eraseSite_C]

end RootAlgebra

/-- The quadratic contribution in the omission formula is the other root's
actual incident row, restricted to the twice-deleted core. -/
theorem rootExtract_deletedQuadratic {N D : ℕ} (W : WeightsN N D K)
    (p q : V N) (h : Fin D) (hpq : p ≠ q) :
    RootResponse.rootExtract q h (RootResponse.deletedQuadratic W p) =
      RootResponse.eraseSite q
        (RootResponse.eraseSite p (rowPolynomial (edgeMatrix W) (q, h))) := by
  rw [RootResponse.rootExtract, RootResponse.deletedQuadratic,
    pderiv_eraseSite_of_ne _ p q h hpq, pderiv_sourceQuadratic]

end KrennAllOrders.EvenResponse
