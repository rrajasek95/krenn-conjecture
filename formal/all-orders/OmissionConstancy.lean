/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import OmissionRotation
import BinarySourceInterface

/-! # Constancy of the actual omitted even response

The rotation identity is the actual finite Wick tensor identity. Its derivative
and the original binary receiving response equations cancel the direct edge
term in the parameter polynomial domain.
-/

namespace KrennAllOrders.OmissionConstancy

open scoped BigOperators
open MvPolynomial MatchingModel SiteAlgebra RootResponse CofactorResponse
open PhysicalEndpoint RetainedBinary OmissionTensor OmissionRotation
open BinaryPairing FiniteResponseRigidity

variable {K : Type*} [Field K] [CharZero K]

omit [CharZero K] in
@[simp] theorem scaleVariables_X {σ : Type*} (s : K) (i : σ) :
    scaleVariables s (X i : MvPolynomial σ K) = C s * X i := by
  simp [scaleVariables]

omit [CharZero K] in
@[simp] theorem scaleVariables_C {σ : Type*} (s a : K) :
    scaleVariables s (C a : MvPolynomial σ K) = C a := by
  simp [scaleVariables]

omit [CharZero K] in
/-- Literal polynomial chain rule for simultaneous scalar substitution. -/
theorem pderiv_scaleVariables {σ : Type*} (j : σ) (s : K)
    (P : MvPolynomial σ K) :
    pderiv j (scaleVariables s P) = C s * scaleVariables s (pderiv j P) := by
  classical
  induction P using MvPolynomial.induction_on with
  | C a => simp
  | add P Q hP hQ => simp [hP, hQ, mul_add]
  | mul_X P i hP =>
    by_cases hi : i = j
    · subst i
      simp only [map_mul, scaleVariables_X, pderiv_mul, pderiv_C,
        pderiv_X_self, mul_one, hP, map_add, zero_mul, zero_add]
      ring
    · simp only [map_mul, scaleVariables_X, pderiv_mul, pderiv_C,
        pderiv_X_of_ne hi, mul_zero, add_zero, hP]
      ring

omit [CharZero K] in
/-- Removing the auxiliary direction commutes with scalar substitution. -/
theorem directionZero_scaleVariables (s : K) (P : ReplicaKernel.MeanPolynomial K) :
    directionZero (scaleVariables s P) = scaleVariables s (directionZero P) := by
  have h : directionZero.comp (scaleVariables s) =
      (scaleVariables s).comp directionZero := by
    ext j <;> simp [directionZero, scaleVariables]
    split_ifs <;> simp
  exact RingHom.congr_fun h P

omit [CharZero K] in
theorem scale_directPolynomial {N : ℕ} (s : K) (W : WeightsN N 3 K)
    (p q : V N) (h : Fin 3) :
    scaleVariables s (directPolynomial W p q h) = C s * directPolynomial W p q h := by
  simp only [directPolynomial, map_sum, map_mul, scaleVariables_X,
    scaleVariables_C, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  ring

omit [CharZero K] in
theorem map_pure {R S ι : Type*} [CommRing R] [CommRing S] [Fintype ι]
    (f : R →+* S) (b : Bool) (w : ι → Bool) :
    f (BinaryPairing.pure b w) = BinaryPairing.pure b w := by
  classical
  simp [BinaryPairing.pure]

/-- The pure receiving coefficient of the actual omitted tensor is a constant
polynomial in all three original row parameters. -/
theorem pure_tensor_constancy (m : ℕ) (W : WeightsN (2 * (m + 1)) 3 K)
    (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin 3) (hbh : b ≠ h)
    (s : K) (hsq : s * s = 2)
    (hzero : ∀ w : RetainedSites p q → Bool, ∀ r, 0 < r → r ≤ m →
      OddResponseVanishing.oddResponsePolynomial W p m r
        (receivingWord p q b h w) = 0) :
    directionZero (OmissionTensor.responseTensor m W p q b h (fun _ => false)) =
      C (eval (fun _ => 0)
        (OmissionTensor.responseTensor m W p q b h (fun _ => false))) := by
  classical
  let E := OmissionTensor.responseTensor m W p q b h
  let F := constantTensor E
  let Es := fun w => scaleVariables s (E w)
  let Vt := fun w => pderiv 3 (E w)
  let Vst := fun w => scaleVariables s (Vt w)
  have heven : Even (Fintype.card (RetainedSites p q)) := by
    rw [card_retainedSites p q hpq]
    exact ⟨m, by omega⟩
  have hrot := omitted_tensor_rotation m W p q hpq b h s hsq
  have hder : C s * pairing E Vt = pairing F Vst := by
    apply PairingDerivative.differentiated_norm_two_rotation heven 3 s hsq
      E F Es Vt Vst
    · intro w; rfl
    · intro w; exact pderiv_C
    · intro w; exact pderiv_scaleVariables 3 s (E w)
    · exact hrot
  let E0 := fun w => directionZero (E w)
  let F0 := fun w => directionZero (F w)
  let Es0 := fun w => directionZero (Es w)
  let V0 := fun w => directionZero (Vt w)
  let Vs0 := fun w => directionZero (Vst w)
  have hrot0 : pairing E0 E0 = pairing F0 Es0 := by
    have hh := congrArg directionZero hrot
    simpa only [PairingDerivative.map_pairing] using hh
  have hder0 : C s * pairing E0 V0 = pairing F0 Vs0 := by
    have hh := congrArg directionZero hder
    simpa only [map_mul, directionZero_C, PairingDerivative.map_pairing] using hh
  have hV0 : V0 = (X h.castSucc : ReplicaKernel.MeanPolynomial K) •
      BinaryPairing.pure true - directPolynomial W p q h • E0 := by
    funext w
    change directionZero (pderiv 3 (responseTensor m W p q b h w)) =
      X h.castSucc * BinaryPairing.pure true w -
        directPolynomial W p q h * directionZero (responseTensor m W p q b h w)
    rw [omitted_source_polynomial m W hW p q hpq b h hbh w (hzero w),
      map_pure (MvPolynomial.C (σ := Fin 4) (R := K)) true w]
  have hVs0 : Vs0 = (C s * X h.castSucc) • BinaryPairing.pure true -
      (C s * directPolynomial W p q h) • Es0 := by
    funext w
    have hh := congrArg (scaleVariables s) (congrFun hV0 w)
    simpa only [Vs0, Vst, Vt, E0, Es0, Es, directionZero_scaleVariables,
      Pi.sub_apply, Pi.smul_apply, smul_eq_mul, map_sub, map_mul,
      scale_directPolynomial, scaleVariables_X, map_pure] using hh
  have hs : s ≠ 0 := by
    intro hs
    simp [hs] at hsq
  have hCs : (C s : ReplicaKernel.MeanPolynomial K) ≠ 0 := C_ne_zero.mpr hs
  have hf : (X h.castSucc : ReplicaKernel.MeanPolynomial K) ≠ 0 := X_ne_zero _
  have hh := OmissionCancellation.pure_coefficient_eq_of_response_and_rotation
    E0 F0 Es0 V0 Vs0 (C s) (X h.castSucc) (directPolynomial W p q h)
    hCs hf hV0 hVs0 hrot0 hder0
  simpa only [E0, F0, F, constantTensor, directionZero_C] using hh

/-- Numeric constancy on the actual original incident-row family, in precisely
the form used by the quadratic omission coefficient extraction. -/
theorem pure_even_constancy (m : ℕ) (W : WeightsN (2 * (m + 1)) 3 K)
    (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin 3) (hbh : b ≠ h)
    (s : K) (hsq : s * s = 2)
    (hzero : ∀ w : RetainedSites p q → Bool, ∀ r, 0 < r → r ≤ m →
      OddResponseVanishing.oddResponsePolynomial W p m r
        (receivingWord p q b h w) = 0)
    (a : Fin 3 → K) :
    coeff (wordExponent (fun _ => b) (retainedVertices p q))
      (EvenResponse.evenResponse (K := K) m (retainedQuadratic W p q)
        (OmissionDegree.omittedRowLinear W p q a)) =
    coeff (wordExponent (fun _ => b) (retainedVertices p q))
      (EvenResponse.dividedPower (K := K) (retainedQuadratic W p q) m) := by
  classical
  have hc := pure_tensor_constancy m W hW p q hpq b h hbh s hsq hzero
  let a4 : Fin 4 → K := ![a 0, a 1, a 2, 0]
  have ha : (fun i : Fin 3 => a4 i.castSucc) = a := by
    funext i; fin_cases i <;> rfl
  have hexp : wordExponent (receivingWord p q b h (fun _ => false))
      (retainedVertices p q) = wordExponent (fun _ => b) (retainedVertices p q) := by
    apply wordExponent_congr_on_list
    intro v hv
    simp [receivingWord, (mem_retainedVertices p q v).mp hv]
  have hc0 := congrArg (eval (fun _ : Fin 4 => (0 : K))) hc
  have hca := congrArg (eval a4) hc
  rw [eval_directionZero_responseTensor, ha, hexp] at hca
  rw [eval_directionZero_responseTensor, hexp] at hc0
  rw [eval_C] at hca hc0
  rw [← hc0] at hca
  simpa only [OmissionDegree.omittedRowLinear, LinearMap.coe_mk, AddHom.coe_mk,
    OddResponseVanishing.rowAt, rootFamilyRow, zero_mul,
    Finset.sum_const_zero, map_zero, EndpointSource.evenResponse_zero_mean] using hca

/-- Over the original complex source, both the higher-response tower and the
norm-two scale are already theorems. Constancy requires only `EqSystemN`. -/
theorem pure_even_constancy_of_eqSystem (m : ℕ)
    (W : WeightsN (2 * (m + 1)) 3 ℂ)
    (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin 3) (hbh : b ≠ h)
    (a : Fin 3 → ℂ) :
    coeff (wordExponent (fun _ => b) (retainedVertices p q))
      (EvenResponse.evenResponse (K := ℂ) m (retainedQuadratic W p q)
        (OmissionDegree.omittedRowLinear W p q a)) =
    coeff (wordExponent (fun _ => b) (retainedVertices p q))
      (EvenResponse.dividedPower (K := ℂ) (retainedQuadratic W p q) m) :=
  pure_even_constancy m W hW p q hpq b h hbh
    BinarySourceInterface.normTwo BinarySourceInterface.normTwo_sq
    (BinarySourceInterface.omitted_higher_zero m W hW p q b h) a

end KrennAllOrders.OmissionConstancy
