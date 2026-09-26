/-
Copyright (c) 2026 Rishi. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/

import Mathlib.Algebra.Polynomial.Derivative

/-!
# Finite polynomial ODEs for the two-replica endpoint argument

Over an integral domain, a polynomial satisfying `p' + d * p = 0`, with `d ≠ 0`,
is zero. A polynomial satisfying `p' + d * p = k` is constant. No assumption on
the characteristic is needed. In particular, the coefficient domain may itself
be a polynomial ring in the additional invariant parameters.

This formalizes only the polynomial ODE step of
`proofs/krenn-gu-all-orders-two-replica-proof.md`, Section 4. It does not formalize
the source identities or their reduction to these equations.
-/

set_option autoImplicit false
set_option relaxedAutoImplicit false

namespace KrennAllOrders

open Polynomial

section Domain

variable {R : Type*} [CommRing R] [IsDomain R]

/-- A finite polynomial solving `p' + d * p = 0`, with `d ≠ 0`, vanishes. -/
theorem eq_zero_of_derivative_add_C_mul_eq_zero {p : R[X]} {d : R}
    (hd : d ≠ 0) (h : derivative p + C d * p = 0) : p = 0 := by
  by_contra hp
  have hcoeff := congrArg (fun q : R[X] => q.coeff p.natDegree) h
  have htop : p.coeff (p.natDegree + 1) = 0 :=
    coeff_eq_zero_of_natDegree_lt (Nat.lt_succ_self p.natDegree)
  have hleading : d * p.leadingCoeff = 0 := by
    simpa [coeff_derivative, coeff_C_mul, htop] using hcoeff
  exact (mul_ne_zero hd (leadingCoeff_ne_zero.mpr hp)) hleading

/-- A finite polynomial solving `p' + d * p = k`, with `d ≠ 0`, is constant. -/
theorem eq_C_coeff_zero_of_derivative_add_C_mul_eq_C {p : R[X]} {d k : R}
    (hd : d ≠ 0) (h : derivative p + C d * p = C k) : p = C (p.coeff 0) := by
  apply eq_C_of_natDegree_eq_zero
  by_contra hdegree
  have hp : p ≠ 0 := fun hp => hdegree (hp ▸ natDegree_zero)
  have hcoeff := congrArg (fun q : R[X] => q.coeff p.natDegree) h
  have htop : p.coeff (p.natDegree + 1) = 0 :=
    coeff_eq_zero_of_natDegree_lt (Nat.lt_succ_self p.natDegree)
  have hleading : d * p.leadingCoeff = 0 := by
    simpa only [coeff_add, coeff_derivative, coeff_C_mul, htop, zero_mul, zero_add,
      coeff_natDegree, coeff_C, if_neg hdegree] using hcoeff
  exact (mul_ne_zero hd (leadingCoeff_ne_zero.mpr hp)) hleading

/-- The constant coefficient of a polynomial ODE solution satisfies the scalar equation. -/
theorem mul_coeff_zero_of_derivative_add_C_mul_eq_C {p : R[X]} {d k : R}
    (hd : d ≠ 0) (h : derivative p + C d * p = C k) : d * p.coeff 0 = k := by
  have hp := eq_C_coeff_zero_of_derivative_add_C_mul_eq_C hd h
  have hderivative : derivative p = 0 := by rw [hp, derivative_C]
  simpa only [coeff_add, hderivative, coeff_zero, coeff_C_mul, coeff_C_zero, zero_add]
    using congrArg (fun q : R[X] => q.coeff 0) h

/-- Division-free form of the constant-solution theorem. -/
theorem eq_C_of_derivative_add_C_mul_eq_C_mul {p : R[X]} {d a : R}
    (hd : d ≠ 0) (h : derivative p + C d * p = C (d * a)) : p = C a := by
  have hcoeff : p.coeff 0 = a :=
    mul_left_cancel₀ hd (mul_coeff_zero_of_derivative_add_C_mul_eq_C hd h)
  simpa [hcoeff] using eq_C_coeff_zero_of_derivative_add_C_mul_eq_C hd h

/-- The scalar endpoint conclusion of the finite polynomial ODE argument. -/
theorem endpoint_eq_of_polynomial_ode {p : R[X]} {d β η α : R}
    (hd : d ≠ 0) (hη : η ≠ 0)
    (h : derivative p + C d * p = C (β * η))
    (hzero : p.coeff 0 = η * α) : β = d * α := by
  have hscalar := mul_coeff_zero_of_derivative_add_C_mul_eq_C hd h
  rw [hzero] at hscalar
  apply mul_right_cancel₀ hη
  simpa [mul_assoc, mul_comm, mul_left_comm] using hscalar.symm

end Domain

section Field

variable {K : Type*} [Field K]

/-- Over a field, the unique polynomial solution of `p' + d * p = k` is `k / d`. -/
theorem eq_C_div_of_derivative_add_C_mul_eq_C {p : K[X]} {d k : K}
    (hd : d ≠ 0) (h : derivative p + C d * p = C k) : p = C (k / d) := by
  have hcoeff : p.coeff 0 = k / d := by
    apply (eq_div_iff hd).2
    simpa [mul_comm] using mul_coeff_zero_of_derivative_add_C_mul_eq_C hd h
  simpa [hcoeff] using eq_C_coeff_zero_of_derivative_add_C_mul_eq_C hd h

end Field

end KrennAllOrders
