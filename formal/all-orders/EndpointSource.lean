/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import PhysicalEndpoint
import BinaryPairing
import RetainedBinary

/-! # Physical endpoint source inputs

This module specializes the constructed retained response to actual receiving
words. Its remaining higher-response premises are the original source's
finite odd response polynomials, not endpoint or retained-source equations.
-/

namespace KrennAllOrders.EndpointSource

open scoped BigOperators
open MatchingModel SiteAlgebra RootResponse PhysicalEndpoint
open MvPolynomial

variable {K : Type*} [Field K] [CharZero K] {N D : ℕ}

omit [CharZero K] in
/-- Changing a deleted site's receiving colour does not change the retained
physical word. -/
theorem wordExponent_update_not_mem (ι : V N → Fin D) (L : List (V N))
    (q : V N) (h : Fin D) (hq : q ∉ L) :
    wordExponent (Function.update ι q h) L = wordExponent ι L := by
  classical
  induction L with
  | nil => rfl
  | cons v L ih =>
    have hvq : v ≠ q := by intro hvq; subst v; simp at hq
    have hqL : q ∉ L := by intro h; exact hq (List.mem_cons.mpr (Or.inr h))
    simp only [wordExponent, Function.update_of_ne hvq, ih hqL]

omit [CharZero K] in
theorem retainedExponent_update (p q : V N) (ι : V N → Fin D) (h : Fin D) :
    wordExponent (Function.update ι q h) (CofactorResponse.retainedVertices p q) =
      wordExponent ι (CofactorResponse.retainedVertices p q) :=
  wordExponent_update_not_mem ι _ q h (by simp [CofactorResponse.mem_retainedVertices])

/-- The receiving word uses the original two-colour palette. -/
def OnPalette (ι : V N → Fin D) (b h : Fin D) : Prop :=
  ∀ v, ι v = b ∨ ι v = h

omit [CharZero K] in
theorem onPalette_update (ι : V N → Fin D) (b h j : Fin D) (q : V N)
    (hι : OnPalette ι b h) (hj : j = b ∨ j = h) :
    OnPalette (Function.update ι q j) b h := by
  classical
  intro v
  by_cases hv : v = q
  · simpa [hv] using hj
  · simpa [Function.update_of_ne hv] using hι v

/-- Actual whole binary higher-response information at the original root,
including the terminal odd response. No three-colour receiving vanishing is
assumed. -/
def OriginalHigherZeroOnPalette (m : ℕ) (W : WeightsN N D K) (p : V N)
    (b h : Fin D) : Prop :=
  ∀ ι, OnPalette ι b h → ∀ r, 0 < r → r ≤ m →
    OddResponseVanishing.oddResponsePolynomial W p m r ι = 0

/-- The actual source after diagonal reduction. -/
def DiagonalSource (W : WeightsN N D K) : Prop :=
  ∀ p q b h, b ≠ h → edgeMatrix W (p, b) (q, h) = 0

/-- The first-colour source boundary for any retained receiving word. -/
theorem scalar_boundary (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W) (hdiag : DiagonalSource W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (hz : OriginalHigherZeroOnPalette m W p b h)
    (ι : V (2 * (m + 1)) → Fin D) (hι : OnPalette ι b h) :
    ReplicaKernel.meanXAxis
      (pderiv 1 (endpointResponse m W p q b h
        (wordExponent ι (CofactorResponse.retainedVertices p q))) +
      C (edgeMatrix W (p, b) (q, b)) * X 0 * endpointResponse m W p q b h
        (wordExponent ι (CofactorResponse.retainedVertices p q))) =
      X 0 * C (coeff (wordExponent ι (CofactorResponse.retainedVertices p q))
        (pureRetainedWord p q b)) := by
  classical
  have he := mean_scalar_boundary m W hW p q hpq b h hbh
    (Function.update ι q b) (by simp) (hdiag p q h b hbh.symm)
    (hz (Function.update ι q b) (onPalette_update ι b h b q hι (Or.inl rfl)))
  rw [retainedExponent_update] at he
  rw [coeff_pureRootWord_eq_retained p q hpq _ b (by simp), retainedExponent_update] at he
  exact he

/-- The normal mixed boundary, with the same retained receiving word. -/
theorem mixed_boundary (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W) (hdiag : DiagonalSource W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (hz : OriginalHigherZeroOnPalette m W p b h)
    (ι : V (2 * (m + 1)) → Fin D) (hι : OnPalette ι b h) :
    ReplicaKernel.meanXAxis
      (pderiv 1 (pderiv 2 (endpointResponse m W p q b h
        (wordExponent ι (CofactorResponse.retainedVertices p q)))) +
      C (edgeMatrix W (p, b) (q, b)) * X 0 *
        pderiv 2 (endpointResponse m W p q b h
          (wordExponent ι (CofactorResponse.retainedVertices p q)))) = 0 := by
  classical
  have he := mean_mixed_boundary m W hW p q hpq b h hbh
    (Function.update ι q b) (by simp) (hdiag p q h b hbh.symm)
    (hz (Function.update ι q b) (onPalette_update ι b h b q hι (Or.inl rfl)))
  rw [retainedExponent_update] at he
  exact he

theorem v_boundary (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W) (hdiag : DiagonalSource W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (hz : OriginalHigherZeroOnPalette m W p b h)
    (ι : V (2 * (m + 1)) → Fin D) (hι : OnPalette ι b h) :
    ReplicaKernel.meanXAxis (pderiv 3 (endpointResponse m W p q b h
      (wordExponent ι (CofactorResponse.retainedVertices p q)))) = 0 := by
  classical
  have he := mean_v_boundary m W hW p q hpq b h hbh
    (Function.update ι q h) (by simp) (hdiag p q b h hbh)
    (hz (Function.update ι q h) (onPalette_update ι b h h q hι (Or.inr rfl)))
  rw [retainedExponent_update] at he
  exact he

omit [CharZero K] in
theorem retainedQuadratic_symm (W : WeightsN N D K) (p q : V N) :
    retainedQuadratic W p q = retainedQuadratic W q p := by
  exact eraseSite_commute q p (sourceQuadratic W)

omit [CharZero K] in
theorem retainedVertices_symm (p q : V N) :
    CofactorResponse.retainedVertices p q = CofactorResponse.retainedVertices q p :=
  List.erase_comm p q

omit [CharZero K] in
theorem eval_meanYAxis (P : ReplicaKernel.MeanPolynomial K) (a : Fin 4 → K) :
    eval a (ReplicaKernel.meanYAxis P) = eval ![0, a 1, 0, 0] P := by
  change eval₂ (RingHom.id K) a (eval₂ C ![0, X 1, 0, 0] P) = _
  rw [← eval₂_assoc]
  congr 1
  funext j
  fin_cases j <;> simp

/-- The opposite root supplies the `u` boundary. The deletion ordering and
receiving-colour restoration are both resolved on the literal core. -/
theorem u_boundary (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W) (hdiag : DiagonalSource W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (hz : OriginalHigherZeroOnPalette m W q b h)
    (ι : V (2 * (m + 1)) → Fin D) (hι : OnPalette ι b h) :
    ReplicaKernel.meanYAxis (pderiv 2 (endpointResponse m W p q b h
      (wordExponent ι (CofactorResponse.retainedVertices p q)))) = 0 := by
  classical
  apply MvPolynomial.funext
  intro a
  rw [eval_meanYAxis, eval_pderiv_endpointResponse]
  have hrow : (∑ j : Fin 4, C (![0, a 1, 0, 0] j) * endpointRows W p q b h j) =
      C (a 1) * retainedRow W q p b := by simp [Fin.sum_univ_succ, endpointRows]
  rw [hrow]
  dsimp [endpointRows]
  have he := numerical_second_source_boundary m W hW q p hpq.symm b h hbh
    (Function.update ι p h) (by simp) (hdiag q p b h hbh)
    (hz (Function.update ι p h) (onPalette_update ι b h h p hι (Or.inr rfl))) (a 1) 0
  rw [retainedExponent_update q p ι h, retainedVertices_symm q p] at he
  rw [retainedQuadratic_symm W q p] at he
  simpa only [mul_zero, zero_mul, C_0, zero_add, add_zero, coeff_zero, map_zero] using he

omit [CharZero K] in
theorem eraseSite_idempotent (q : V N) (P : PhysicalPolynomial N D K) :
    eraseSite q (eraseSite q P) = eraseSite q P := by
  induction P using MvPolynomial.induction_on with
  | C c => simp
  | add P Q hP hQ => simp only [map_add, hP, hQ]
  | mul_X P z hP =>
    rw [map_mul, map_mul, hP]
    by_cases hq : z.1 = q <;> simp only [eraseSite_X, hq, ite_true, ite_false, map_zero]

omit [CharZero K] in
/-- Erasing a row at a site absent from the receiving word leaves its
coefficient contribution unchanged, with no assumption on its other factor. -/
theorem coeff_erased_row_mul (q : V N) (L : List (V N)) (hq : q ∉ L)
    (ι : V N → Fin D) (row P : PhysicalPolynomial N D K) :
    coeff (wordExponent ι L) (eraseSite q row * P) =
      coeff (wordExponent ι L) (row * P) := by
  calc
    _ = coeff (wordExponent ι L) (eraseSite q (eraseSite q row * P)) :=
      (CofactorResponse.coeff_word_eraseSite q _ ι L hq).symm
    _ = coeff (wordExponent ι L) (eraseSite q (row * P)) := by
      simp only [map_mul, eraseSite_idempotent]
    _ = _ := CofactorResponse.coeff_word_eraseSite q _ ι L hq

omit [CharZero K] in
/-- Diagonal colour rows cannot contribute to a different pure receiving
word, even when multiplied by an arbitrary physical polynomial. -/
theorem coeff_retainedRow_pure_other (W : WeightsN N D K)
    (hdiag : DiagonalSource W) (p q : V N) (b h : Fin D) (hbh : b ≠ h)
    (P : PhysicalPolynomial N D K) :
    coeff (wordExponent (fun _ => h) (CofactorResponse.retainedVertices p q))
      (retainedRow W p q b * P) = 0 := by
  classical
  rw [retainedRow, coeff_erased_row_mul q _
    (by simp [CofactorResponse.mem_retainedVertices]), coeff_rowPolynomial_mul _ _ _ _
      (CofactorResponse.retainedVertices_nodup p q)]
  simp only [hdiag p _ b h hbh, zero_mul]
  have hz (L : List (V N)) : (L.map (fun _ => (0 : K))).sum = 0 := by
    induction L with
    | nil => rfl
    | cons v L ih => simp only [List.map_cons, List.sum_cons, ih, zero_add]
  exact hz _

/-- Pure second-colour receiving coefficients have zero first-colour
mean derivative. This uses actual diagonal physical rows. -/
theorem pure_second_response_pderiv_zero (m : ℕ) (W : WeightsN N D K)
    (hdiag : DiagonalSource W) (p q : V N) (b h : Fin D) (hbh : b ≠ h)
    (j : Fin 4) (hj : j = 0 ∨ j = 1) :
    pderiv j (endpointResponse m W p q b h
      (wordExponent (fun _ => h) (CofactorResponse.retainedVertices p q))) = 0 := by
  apply MvPolynomial.funext
  intro a
  rw [eval_pderiv_endpointResponse, map_zero]
  rcases hj with rfl | rfl
  · exact coeff_retainedRow_pure_other W hdiag p q b h hbh _
  · rw [retainedVertices_symm p q]
    exact coeff_retainedRow_pure_other W hdiag q p b h hbh _

/-- In characteristic zero a vanishing partial eliminates every coefficient
whose corresponding variable has positive exponent. -/
theorem coeff_zero_of_pderiv_zero (P : ReplicaKernel.MeanPolynomial K)
    (i : Fin 4) (n : Fin 4 →₀ ℕ) (hn : n i ≠ 0) (hP : pderiv i P = 0) :
    coeff n P = 0 := by
  classical
  have hle : Finsupp.single i 1 ≤ n := Finsupp.single_le_iff.mpr (by omega)
  have hi : (n - Finsupp.single i 1 : Fin 4 →₀ ℕ) i + 1 = n i := by
    simp only [Finsupp.tsub_apply, Finsupp.single_eq_same]
    omega
  have hc := congrArg (coeff (n - Finsupp.single i 1)) hP
  have hiK : ((n - Finsupp.single i 1 : Fin 4 →₀ ℕ) i : K) + 1 = (n i : K) := by
    exact_mod_cast hi
  rw [coeff_pderiv, tsub_add_cancel_of_le hle, hiK, coeff_zero] at hc
  exact (mul_eq_zero.mp hc).resolve_right (Nat.cast_ne_zero.mpr hn)

/-- Restricting the auxiliary means to zero leaves a constant polynomial
when both surviving first-colour partial derivatives vanish. -/
theorem binaryMean_constant_of_pderiv_zero (P : ReplicaKernel.MeanPolynomial K)
    (h₀ : pderiv 0 P = 0) (h₁ : pderiv 1 P = 0) (i : Fin 2) :
    ReplicaKernel.binaryMean i P = C (eval (0 : Fin 4 → K) P) := by
  classical
  have hmon (n : Fin 4 →₀ ℕ) (hn : n ∈ P.support) :
      ReplicaKernel.binaryMean i (monomial n (coeff n P)) =
        C (eval (0 : Fin 4 → K) (monomial n (coeff n P))) := by
    have hn₀ : n 0 = 0 := by
      by_contra h
      exact (mem_support_iff.mp hn) (coeff_zero_of_pderiv_zero P 0 n h h₀)
    have hn₁ : n 1 = 0 := by
      by_contra h
      exact (mem_support_iff.mp hn) (coeff_zero_of_pderiv_zero P 1 n h h₁)
    simp only [ReplicaKernel.binaryMean, eval₂Hom_monomial, eval_monomial, map_mul]
    simp [Fin.prod_univ_succ, hn₀, hn₁]
  calc
    _ = ∑ n ∈ P.support, ReplicaKernel.binaryMean i (monomial n (coeff n P)) := by
      rw [← map_sum, ← as_sum P]
    _ = ∑ n ∈ P.support, C (eval (0 : Fin 4 → K) (monomial n (coeff n P))) := by
      apply Finset.sum_congr rfl
      intro n hn
      exact hmon n hn
    _ = _ := by rw [← map_sum, ← map_sum, ← as_sum P]

/-- The second-colour cap expression is structurally independent of both
first-colour means, before any source equation is invoked. -/
theorem pure_second_cap_binaryMean (m : ℕ) (W : WeightsN N D K)
    (hdiag : DiagonalSource W) (p q : V N) (b h : Fin D) (hbh : b ≠ h) (i : Fin 2) :
    ReplicaKernel.binaryMean i
      (pderiv 2 (pderiv 3 (endpointResponse m W p q b h
        (wordExponent (fun _ => h) (CofactorResponse.retainedVertices p q)))) +
       C (edgeMatrix W (p, h) (q, h)) * endpointResponse m W p q b h
        (wordExponent (fun _ => h) (CofactorResponse.retainedVertices p q))) =
      C (eval (0 : Fin 4 → K)
        (pderiv 2 (pderiv 3 (endpointResponse m W p q b h
          (wordExponent (fun _ => h) (CofactorResponse.retainedVertices p q)))) +
        C (edgeMatrix W (p, h) (q, h)) * endpointResponse m W p q b h
          (wordExponent (fun _ => h) (CofactorResponse.retainedVertices p q)))) := by
  apply binaryMean_constant_of_pderiv_zero _ _ _ i
  · rw [(pderiv (R := K) (σ := Fin 4) 0).map_add,
      mean_pderiv_commute _ 0 2, mean_pderiv_commute _ 0 3,
      pure_second_response_pderiv_zero m W hdiag p q b h hbh 0 (Or.inl rfl)]
    simp only [pderiv_C_mul,
      pure_second_response_pderiv_zero m W hdiag p q b h hbh 0 (Or.inl rfl),
      map_zero, mul_zero, zero_add]
  · rw [(pderiv (R := K) (σ := Fin 4) 1).map_add,
      mean_pderiv_commute _ 1 2, mean_pderiv_commute _ 1 3,
      pure_second_response_pderiv_zero m W hdiag p q b h hbh 1 (Or.inr rfl)]
    simp only [pderiv_C_mul,
      pure_second_response_pderiv_zero m W hdiag p q b h hbh 1 (Or.inr rfl),
      map_zero, mul_zero, zero_add]

/-- Differentiating the full original second-colour plane and then
specializing all means to zero gives the actual pure retained cap. -/
theorem cap_origin (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W) (hdiag : DiagonalSource W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (hz : OriginalHigherZeroOnPalette m W p b h)
    (ι : V (2 * (m + 1)) → Fin D) (hι : OnPalette ι b h) :
    eval (0 : Fin 4 → K)
      (pderiv 2 (pderiv 3 (endpointResponse m W p q b h
        (wordExponent ι (CofactorResponse.retainedVertices p q)))) +
      C (edgeMatrix W (p, h) (q, h)) * endpointResponse m W p q b h
        (wordExponent ι (CofactorResponse.retainedVertices p q))) =
      coeff (wordExponent ι (CofactorResponse.retainedVertices p q))
        (pureRetainedWord p q h) := by
  classical
  have hs := mean_second_source_boundary m W hW p q hpq b h hbh
    (Function.update ι q h) (by simp) (hdiag p q b h hbh)
    (hz (Function.update ι q h) (onPalette_update ι b h h q hι (Or.inr rfl)))
  rw [retainedExponent_update, coeff_pureRootWord_eq_retained p q hpq _ h (by simp),
    retainedExponent_update] at hs
  have hd := congrArg (pderiv (R := K) (σ := Fin 4) 2) hs
  rw [pderiv_meanPplane_two] at hd
  rw [(pderiv (R := K) (σ := Fin 4) 2).map_add] at hd
  simp only [pderiv_mul, pderiv_C, pderiv_X_self, zero_mul, zero_add, mul_one] at hd
  have he := congrArg (eval (0 : Fin 4 → K)) hd
  rw [eval_meanPplane] at he
  have hvec : ![(0 : K), 0, 0, 0] = (0 : Fin 4 → K) := by
    funext j; fin_cases j <;> rfl
  simp only [Pi.zero_apply, hvec, map_add, map_mul, eval_C, eval_X, zero_mul,
    mul_zero, add_zero, map_one] at he
  simpa only [map_add, map_mul, eval_C, one_mul] using he

/-- The complete pure second-colour cap polynomial required by the kernel,
not just its value at the source point. -/
theorem pure_second_cap (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W) (hdiag : DiagonalSource W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (hz : OriginalHigherZeroOnPalette m W p b h) (i : Fin 2) :
    ReplicaKernel.binaryMean i
      (pderiv 2 (pderiv 3 (endpointResponse m W p q b h
        (wordExponent (fun _ => h) (CofactorResponse.retainedVertices p q)))) +
      C (edgeMatrix W (p, h) (q, h)) * endpointResponse m W p q b h
        (wordExponent (fun _ => h) (CofactorResponse.retainedVertices p q))) = 1 := by
  rw [pure_second_cap_binaryMean m W hdiag p q b h hbh i,
    cap_origin m W hW hdiag p q hpq b h hbh hz (fun _ => h) (fun _ => Or.inr rfl)]
  simp [pureRetainedWord]

omit [CharZero K] in
theorem evenResponse_zero_mean (m : ℕ) (Q : PhysicalPolynomial N D K) :
    EvenResponse.evenResponse (K := K) m Q 0 =
      EvenResponse.dividedPower (K := K) Q m := by
  classical
  unfold EvenResponse.evenResponse
  rw [Finset.sum_eq_single 0]
  · simp
  · intro r _ hr
    have hp : 2 * r ≠ 0 := by omega
    simp [EvenResponse.dividedPower, hp]
  · simp

/-- The zero-mean response is the literal retained pure-colour cofactor. -/
theorem response_origin_eq_pureCofactor (m : ℕ)
    (W : WeightsN (2 * (m + 1)) D K)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) :
    eval (0 : Fin 4 → K) (endpointResponse m W p q b h
      (wordExponent (fun _ => b) (CofactorResponse.retainedVertices p q))) =
      RootResponse.pureCofactor W b p q := by
  classical
  rw [eval_endpointResponse]
  simp only [Pi.zero_apply, C_0, zero_mul, Finset.sum_const_zero]
  rw [evenResponse_zero_mean]
  have hp : p ∉ CofactorResponse.retainedVertices p q := by
    simp [CofactorResponse.mem_retainedVertices]
  have hq : q ∉ CofactorResponse.retainedVertices p q := by
    simp [CofactorResponse.mem_retainedVertices]
  have hex : EvenResponse.dividedPower (K := K) (retainedQuadratic W p q) m =
      eraseSite q (eraseSite p (dividedSourcePower W m)) := by
    simp [EvenResponse.dividedPower, retainedQuadratic, deletedQuadratic,
      dividedSourcePower]
  rw [hex, CofactorResponse.coeff_word_eraseSite q _ _ _ hq,
    CofactorResponse.coeff_word_eraseSite p _ _ _ hp]
  have hlen : (CofactorResponse.retainedVertices p q).length = 2 * m := by
    rw [CofactorResponse.retainedVertices_length p q hpq]
    omega
  rw [dividedSourcePower, coeff_C_mul,
    coeff_sourceQuadratic_pow W (fun _ => b) m _ hlen
      (List.Pairwise.erase q (List.Pairwise.erase p (vertices_pairwise_lt _))),
    RootResponse.pureCofactor, if_neg hpq, pmSumList]
  change (m.factorial : K)⁻¹ * ((m.factorial : K) *
      pmSumListAux W (fun _ => b) (2 * m) (CofactorResponse.retainedVertices p q)) =
    pmSumListAux W (fun _ => b) (CofactorResponse.retainedVertices p q).length
      (CofactorResponse.retainedVertices p q)
  rw [hlen]
  have hf : (m.factorial : K) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero m)
  rw [← mul_assoc, inv_mul_cancel₀ hf, one_mul]

open RetainedBinary

/-- The receiving tensor of the actual two-root response. -/
noncomputable def endpointTensor (m : ℕ) (W : WeightsN N D K)
    (p q : V N) (b h : Fin D) :
    (RetainedSites p q → Bool) → ReplicaKernel.MeanPolynomial K :=
  fun w => endpointResponse m W p q b h
    (wordExponent (receivingWord p q b h w) (CofactorResponse.retainedVertices p q))

theorem receivingWord_onPalette (p q : V N) (b h : Fin D)
    (w : RetainedSites p q → Bool) : OnPalette (receivingWord p q b h w) b h := by
  intro v
  unfold receivingWord
  split_ifs <;> simp

/-- Literal signed-complement weights of the binary pairing. -/
noncomputable def binaryKernel (p q : V N)
    (w z : RetainedSites p q → Bool) : K :=
  if z = BinaryPairing.complement w then BinaryPairing.sign w else 0

omit [CharZero K] in
theorem C_binarySign (p q : V N) (w : RetainedSites p q → Bool) :
    (C (BinaryPairing.sign (R := K) w) : ReplicaKernel.MeanPolynomial K) =
      BinaryPairing.sign w := by
  classical
  rw [BinaryPairing.sign, map_prod]
  apply Finset.prod_congr rfl
  intro v _
  cases w v <;> simp only [Bool.false_eq_true, if_false, if_true, map_one, map_neg]

omit [CharZero K] in
/-- The replica's finite contraction is exactly the previously proved
binary alternating pairing; no pairing property is an extra hypothesis. -/
theorem contraction_eq_binaryPairing (p q : V N)
    (A B : (RetainedSites p q → Bool) → ReplicaKernel.MeanPolynomial K) :
    ReplicaKernel.contraction (binaryKernel (K := K) p q) A B =
      BinaryPairing.pairing A B := by
  classical
  unfold ReplicaKernel.contraction BinaryPairing.pairing
  refine Finset.sum_congr (by ext w; simp) ?_
  intro w _
  rw [Finset.sum_eq_single (BinaryPairing.complement w)]
  · simp only [binaryKernel, if_true, C_binarySign]
  · intro z _ hz
    simp only [binaryKernel, if_neg hz, map_zero, zero_mul]
  · simp

omit [CharZero K] in
theorem scalarContraction_eq_binaryPairing (p q : V N)
    (A B : (RetainedSites p q → Bool) → K) :
    ReplicaKernel.scalarContraction (binaryKernel (K := K) p q) A B =
      BinaryPairing.pairing A B := by
  classical
  unfold ReplicaKernel.scalarContraction BinaryPairing.pairing
  refine Finset.sum_congr (by ext w; simp) ?_
  intro w _
  rw [Finset.sum_eq_single (BinaryPairing.complement w)]
  · simp only [binaryKernel, if_true]
  · intro z _ hz
    simp only [binaryKernel, if_neg hz, zero_mul]
  · simp

/-- The actual pure first-colour tensor supplies the unchanged second-colour
cap to the kernel contraction. -/
theorem tensor_cap (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W) (hdiag : DiagonalSource W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (hz : OriginalHigherZeroOnPalette m W p b h) :
    ReplicaKernel.contraction (binaryKernel (K := K) p q)
      (fun w => C (BinaryPairing.pure false w))
      (fun w => ReplicaKernel.binaryMean 1
        (pderiv 2 (pderiv 3 (endpointTensor m W p q b h w)) +
          C (edgeMatrix W (p, h) (q, h)) * endpointTensor m W p q b h w)) = 1 := by
  rw [contraction_eq_binaryPairing]
  have hC : (fun w : RetainedSites p q → Bool =>
      (C (BinaryPairing.pure false w) : ReplicaKernel.MeanPolynomial K)) =
        BinaryPairing.pure false := by
    funext w
    unfold BinaryPairing.pure
    split_ifs <;> simp
  rw [hC, BinaryPairing.pairing_pure_false]
  change ReplicaKernel.binaryMean 1
    (pderiv 2 (pderiv 3 (endpointResponse m W p q b h
      (wordExponent (receivingWord p q b h (fun _ => true))
        (CofactorResponse.retainedVertices p q)))) +
      C (edgeMatrix W (p, h) (q, h)) * endpointResponse m W p q b h
        (wordExponent (receivingWord p q b h (fun _ => true))
          (CofactorResponse.retainedVertices p q))) = 1
  rw [receivingWord_true]
  exact pure_second_cap m W hW hdiag p q hpq b h hbh hz 1

theorem tensor_cap_origin (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W) (hdiag : DiagonalSource W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (hz : OriginalHigherZeroOnPalette m W p b h) (w : RetainedSites p q → Bool) :
    eval (0 : Fin 4 → K)
      (pderiv 2 (pderiv 3 (endpointTensor m W p q b h w)) +
        C (edgeMatrix W (p, h) (q, h)) * endpointTensor m W p q b h w) =
      BinaryPairing.pure true w := by
  rw [endpointTensor, cap_origin m W hW hdiag p q hpq b h hbh hz
    (receivingWord p q b h w) (receivingWord_onPalette p q b h w)]
  exact coeff_pureRetainedWord p q b h hbh w

omit [CharZero K] in
theorem receivingExponent_false (p q : V N) (b h : Fin D) :
    wordExponent (receivingWord p q b h (fun _ => false)) (CofactorResponse.retainedVertices p q) =
      wordExponent (fun _ => b) (CofactorResponse.retainedVertices p q) := by
  apply wordExponent_congr_on_list
  intro v hv
  have hpq := (CofactorResponse.mem_retainedVertices p q v).mp hv
  simp [receivingWord, hpq]

/-- The kernel origin is the actual first-colour hafnian cofactor, extracted
with the literal pure second-colour cap. -/
theorem tensor_origin (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W) (hdiag : DiagonalSource W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (hz : OriginalHigherZeroOnPalette m W p b h) :
    ReplicaKernel.scalarContraction (binaryKernel (K := K) p q)
      (fun w => eval (0 : Fin 4 → K) (endpointTensor m W p q b h w))
      (fun w => eval (0 : Fin 4 → K)
        (pderiv 2 (pderiv 3 (endpointTensor m W p q b h w)) +
          C (edgeMatrix W (p, h) (q, h)) * endpointTensor m W p q b h w)) =
      RootResponse.pureCofactor W b p q := by
  rw [scalarContraction_eq_binaryPairing]
  have hcap : (fun w : RetainedSites p q → Bool => eval (0 : Fin 4 → K)
      (pderiv 2 (pderiv 3 (endpointTensor m W p q b h w)) +
        C (edgeMatrix W (p, h) (q, h)) * endpointTensor m W p q b h w)) =
        BinaryPairing.pure true := by
    funext w
    exact tensor_cap_origin m W hW hdiag p q hpq b h hbh hz w
  rw [hcap, BinaryPairing.pairing_pure_right]
  simp only [Bool.not_true, BinaryPairing.sign_false, one_mul]
  rw [endpointTensor, receivingExponent_false]
  exact response_origin_eq_pureCofactor m W p q hpq b h

variable [IsAlgClosed K]

/-- The endpoint identity now needs only covariance of the actual constructed
kernel in addition to original binary-response vanishing and diagonalization.
Every source boundary, cap, and origin input is proved from the literal graph
model above. -/
theorem endpoint_of_original_source (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W) (hdiag : DiagonalSource W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (hp : OriginalHigherZeroOnPalette m W p b h)
    (hq : OriginalHigherZeroOnPalette m W q b h)
    (hd : edgeMatrix W (p, b) (q, b) ≠ 0)
    (hcov : ReplicaKernel.KernelInvariant
      (ReplicaKernel.kernel (binaryKernel (K := K) p q) (endpointTensor m W p q b h))) :
    edgeMatrix W (p, b) (q, b) * RootResponse.pureCofactor W b p q = 1 := by
  have he := ReplicaKernel.endpoint_of_tensor_kernel
    (binaryKernel (K := K) p q) (endpointTensor m W p q b h)
    (BinaryPairing.pure false) (d := edgeMatrix W (p, b) (q, b))
    (e := edgeMatrix W (p, h) (q, h)) (β := 1) (η := 1)
    (α := RootResponse.pureCofactor W b p q) hd one_ne_zero hcov
    (fun w => u_boundary m W hW hdiag p q hpq b h hbh hq
      (receivingWord p q b h w) (receivingWord_onPalette p q b h w))
    (fun w => v_boundary m W hW hdiag p q hpq b h hbh hp
      (receivingWord p q b h w) (receivingWord_onPalette p q b h w))
    (fun w => mixed_boundary m W hW hdiag p q hpq b h hbh hp
      (receivingWord p q b h w) (receivingWord_onPalette p q b h w))
    (by
      intro w
      have hs := scalar_boundary m W hW hdiag p q hpq b h hbh hp
        (receivingWord p q b h w) (receivingWord_onPalette p q b h w)
      rw [coeff_pureRetainedWord_false p q b h hbh w] at hs
      simpa only [endpointTensor, map_one, mul_one] using hs)
    (by simpa only [map_one] using tensor_cap m W hW hdiag p q hpq b h hbh hp)
    (by simpa only [one_mul] using tensor_origin m W hW hdiag p q hpq b h hbh hp)
  exact he.symm
end KrennAllOrders.EndpointSource
