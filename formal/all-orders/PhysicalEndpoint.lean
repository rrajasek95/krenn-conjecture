/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import EvenResponse
import ReplicaKernel
import CofactorResponse
import OmittedResponse
import Mathlib.Algebra.MvPolynomial.Equiv

/-!
# Actual retained quadratic and endpoint response polynomials

The four mean variables are parameters; their coefficients are literal
physical-site polynomials. Receiving-word extraction is applied
coefficientwise. In particular, differentiating a mean is not differentiation
of an already specialized source equation.
-/

namespace KrennAllOrders.PhysicalEndpoint

open scoped BigOperators
open MatchingModel SiteAlgebra RootResponse
open MvPolynomial

variable {K : Type*} [Field K] {N D : ℕ}

abbrev PhysicalPolynomial (N D : ℕ) (K : Type*) [CommRing K] :=
  MatchingPolynomial N D K

abbrev MeanTensor (N D : ℕ) (K : Type*) [CommRing K] :=
  MvPolynomial (Fin 4) (PhysicalPolynomial N D K)

/-- A literal physical receiving-word coefficient, applied to every parameter
coefficient of the tensor polynomial. -/
noncomputable def receivingPolynomial (n : SiteVariable N D →₀ ℕ)
    (P : MeanTensor N D K) : ReplicaKernel.MeanPolynomial K :=
  AddMonoidAlgebra.map (MvPolynomial.lcoeff K n).toAddMonoidHom P

@[simp] theorem coeff_receivingPolynomial (n : SiteVariable N D →₀ ℕ)
    (P : MeanTensor N D K) (a : Fin 4 →₀ ℕ) :
    coeff a (receivingPolynomial n P) = coeff n (coeff a P) :=
  coeff_addMonoidAlgebraMap _ _ _

@[simp] theorem receivingPolynomial_add (n : SiteVariable N D →₀ ℕ)
    (P Q : MeanTensor N D K) :
    receivingPolynomial n (P + Q) = receivingPolynomial n P + receivingPolynomial n Q :=
  AddMonoidAlgebra.map_add _ _ _

@[simp] theorem receivingPolynomial_zero (n : SiteVariable N D →₀ ℕ) :
    receivingPolynomial (K := K) n (0 : MeanTensor N D K) = 0 :=
  AddMonoidAlgebra.map_zero _

/-- Mean partial differentiation commutes with the actual physical
coefficient functional, including all terminal coefficients. -/
theorem receivingPolynomial_pderiv (n : SiteVariable N D →₀ ℕ)
    (P : MeanTensor N D K) (j : Fin 4) :
    receivingPolynomial n (pderiv j P) = pderiv j (receivingPolynomial n P) := by
  ext a
  simp only [coeff_receivingPolynomial, coeff_pderiv]
  have hcast : ((a j : PhysicalPolynomial N D K) + 1) = C ((a j : K) + 1) := by
    simp
  rw [hcast, mul_comm, coeff_C_mul, mul_comm]

@[simp] theorem receivingPolynomial_C (n : SiteVariable N D →₀ ℕ)
    (P : PhysicalPolynomial N D K) :
    receivingPolynomial n (C P) = C (coeff n P) := by
  unfold receivingPolynomial
  exact AddMonoidAlgebra.map_single _ _ _

/-- Numeric specialization commutes with the physical receiving coefficient. -/
theorem eval_receivingPolynomial (n : SiteVariable N D →₀ ℕ)
    (P : MeanTensor N D K) (a : Fin 4 → K) :
    eval a (receivingPolynomial n P) =
      coeff n (eval (fun j => C (a j)) P) := by
  classical
  induction P using MvPolynomial.induction_on' with
  | monomial s q =>
    unfold receivingPolynomial
    have hmap : AddMonoidAlgebra.map (lcoeff K n).toAddMonoidHom (monomial s q) =
        monomial s (coeff n q) := AddMonoidAlgebra.map_single _ _ _
    rw [hmap, eval_monomial, eval_monomial]
    have hprod : s.prod (fun j k => (C (a j) : PhysicalPolynomial N D K) ^ k) =
        C (s.prod (fun j k => a j ^ k)) := by
      rw [map_finsuppProd]
      simp only [map_pow]
    rw [hprod, mul_comm q, coeff_C_mul]
    ring
  | add P Q hP hQ =>
    simp only [receivingPolynomial_add, map_add, coeff_add, hP, hQ]

/-- The actual quadratic left after both physical roots are erased. -/
noncomputable def retainedQuadratic (W : WeightsN N D K) (p q : V N) :
    PhysicalPolynomial N D K := eraseSite q (deletedQuadratic W p)

/-- A literal incident row restricted to the same twice-deleted core. -/
noncomputable def retainedRow (W : WeightsN N D K) (p q : V N) (i : Fin D) :
    PhysicalPolynomial N D K := eraseSite q (rowPolynomial (edgeMatrix W) (p, i))

/-- Endpoint row order is `x,y,u,v`: first colour at roots `p,q`, then
second colour at those roots. -/
noncomputable def endpointRows (W : WeightsN N D K) (p q : V N) (b h : Fin D) :
    Fin 4 → PhysicalPolynomial N D K :=
  ![retainedRow W p q b, retainedRow W q p b,
    retainedRow W p q h, retainedRow W q p h]

noncomputable def meanRow (rows : Fin 4 → PhysicalPolynomial N D K) :
    MeanTensor N D K := ∑ j : Fin 4, X j * C (rows j)

@[simp] theorem pderiv_meanRow (rows : Fin 4 → PhysicalPolynomial N D K) (j : Fin 4) :
    pderiv j (meanRow rows) = C (rows j) := by
  classical
  simp [meanRow, pderiv_X, Pi.single_apply]

@[simp] theorem eval_meanRow (rows : Fin 4 → PhysicalPolynomial N D K)
    (a : Fin 4 → K) :
    eval (fun j => C (a j)) (meanRow rows) = ∑ j : Fin 4, C (a j) * rows j := by
  simp [meanRow]

variable [CharZero K]

/-- The complete finite even response of the actual retained core. -/
noncomputable def physicalEvenResponse (m : ℕ)
    (Q : PhysicalPolynomial N D K) (rows : Fin 4 → PhysicalPolynomial N D K) :
    MeanTensor N D K :=
  EvenResponse.evenResponse (K := K) m (C Q) (meanRow rows)

omit [CharZero K] in
/-- The mean tensor evaluates to the literal finite physical response. -/
theorem eval_physicalEvenResponse (m : ℕ)
    (Q : PhysicalPolynomial N D K) (rows : Fin 4 → PhysicalPolynomial N D K)
    (a : Fin 4 → K) :
    eval (fun j => C (a j)) (physicalEvenResponse m Q rows) =
      EvenResponse.evenResponse (K := K) m Q (∑ j : Fin 4, C (a j) * rows j) := by
  unfold physicalEvenResponse
  have hf : ∀ c : K, eval (fun j => (C (a j) : PhysicalPolynomial N D K))
      (C (algebraMap K (PhysicalPolynomial N D K) c)) =
      (C (algebraMap K K c) : PhysicalPolynomial N D K) := by simp
  rw [EvenResponse.map_evenResponse (eval (fun j => C (a j))) hf]
  simp

/-- Its mean derivative is derived from the finite divided-power sum. -/
theorem pderiv_physicalEvenResponse (m : ℕ)
    (Q : PhysicalPolynomial N D K) (rows : Fin 4 → PhysicalPolynomial N D K)
    (j : Fin 4) :
    pderiv j (physicalEvenResponse m Q rows) =
      C (rows j) * EvenResponse.lowerOddResponse (K := K) m (C Q) (meanRow rows) := by
  unfold physicalEvenResponse
  rw [EvenResponse.pderiv_evenResponse_of_pderiv_quadratic_zero m _ _ j
    (by simp), pderiv_meanRow]

/-- A completely general physical row list, before endpoint labels or
diagonal reduction are imposed. -/
theorem eval_pderiv_receivingEvenResponse (m : ℕ)
    (Q : PhysicalPolynomial N D K) (rows : Fin 4 → PhysicalPolynomial N D K)
    (n : SiteVariable N D →₀ ℕ) (a : Fin 4 → K) (j : Fin 4) :
    eval a (pderiv j (receivingPolynomial n (physicalEvenResponse m Q rows))) =
      coeff n (rows j * EvenResponse.lowerOddResponse (K := K) m Q
        (∑ k : Fin 4, C (a k) * rows k)) := by
  rw [← receivingPolynomial_pderiv, eval_receivingPolynomial,
    pderiv_physicalEvenResponse]
  have hf : ∀ c : K, eval (fun k => (C (a k) : PhysicalPolynomial N D K))
      (C (algebraMap K (PhysicalPolynomial N D K) c)) =
      (C (algebraMap K K c) : PhysicalPolynomial N D K) := by simp
  rw [map_mul, eval_C, EvenResponse.map_lowerOddResponse
    (eval (fun k => C (a k))) hf]
  simp

/-- This is the tensor used by the finite replica kernel; no source identity
is included in its definition. -/
noncomputable def endpointResponse (m : ℕ) (W : WeightsN N D K)
    (p q : V N) (b h : Fin D) (n : SiteVariable N D →₀ ℕ) :
    ReplicaKernel.MeanPolynomial K :=
  receivingPolynomial n
    (physicalEvenResponse m (retainedQuadratic W p q) (endpointRows W p q b h))

omit [CharZero K] in
theorem eval_endpointResponse (m : ℕ) (W : WeightsN N D K)
    (p q : V N) (b h : Fin D) (n : SiteVariable N D →₀ ℕ) (a : Fin 4 → K) :
    eval a (endpointResponse m W p q b h n) =
      coeff n (EvenResponse.evenResponse (K := K) m (retainedQuadratic W p q)
        (∑ j : Fin 4, C (a j) * endpointRows W p q b h j)) := by
  rw [endpointResponse, eval_receivingPolynomial, eval_physicalEvenResponse]

theorem eval_pderiv_endpointResponse (m : ℕ) (W : WeightsN N D K)
    (p q : V N) (b h : Fin D) (n : SiteVariable N D →₀ ℕ) (a : Fin 4 → K)
    (j : Fin 4) :
    eval a (pderiv j (endpointResponse m W p q b h n)) =
      coeff n (endpointRows W p q b h j *
        EvenResponse.lowerOddResponse (K := K) m (retainedQuadratic W p q)
          (∑ k : Fin 4, C (a k) * endpointRows W p q b h k)) := by
  exact eval_pderiv_receivingEvenResponse m _ _ n a j

omit [CharZero K] in
theorem eraseSite_commute (p q : V N) (P : PhysicalPolynomial N D K) :
    eraseSite p (eraseSite q P) = eraseSite q (eraseSite p P) := by
  have h : (eraseSite (R := K) (D := D) p).comp (eraseSite q) =
      (eraseSite q).comp (eraseSite p) := by
    apply MvPolynomial.ringHom_ext
    · intro c
      simp
    · intro z
      simp only [RingHom.comp_apply, eraseSite_X]
      split_ifs <;> simp_all only [map_zero, eraseSite_X, ite_true, ite_false]
  exact RingHom.congr_fun h P

theorem extractedQuadratic_eq_retainedRow (W : WeightsN N D K)
    (p q : V N) (h : Fin D) (hpq : p ≠ q) :
    rootExtract q h (deletedQuadratic W p) = retainedRow W q p h := by
  rw [EvenResponse.rootExtract_deletedQuadratic W p q h hpq,
    eraseSite_commute, eraseSite_rowPolynomial]
  rfl

noncomputable def twoColorParameters (b h : Fin D) (s t : K) : Fin D → K :=
  fun i => (if i = b then s else 0) + (if i = h then t else 0)

omit [CharZero K] in
theorem rowAt_twoColorParameters (W : WeightsN N D K) (p : V N)
    (b h : Fin D) (s t : K) :
    OddResponseVanishing.rowAt W p (twoColorParameters b h s t) =
      C s * rowPolynomial (edgeMatrix W) (p, b) +
      C t * rowPolynomial (edgeMatrix W) (p, h) := by
  classical
  have hc (i : Fin D) (j : Fin D) (a : K) :
      (C (if i = j then a else 0) : PhysicalPolynomial N D K) =
        if i = j then C a else 0 := by split_ifs <;> simp
  simp only [OddResponseVanishing.rowAt, rootFamilyRow, twoColorParameters,
    map_add, hc, add_mul, Finset.sum_add_distrib, ite_mul, zero_mul]
  simp

omit [CharZero K] in
theorem eraseSite_rowAt_twoColorParameters (W : WeightsN N D K) (p q : V N)
    (b h : Fin D) (s t : K) :
    eraseSite q (OddResponseVanishing.rowAt W p (twoColorParameters b h s t)) =
      C s * retainedRow W p q b + C t * retainedRow W p q h := by
  rw [rowAt_twoColorParameters]
  simp [retainedRow]

omit [CharZero K] in
/-- Exact extraction of the original two-colour departure plane. The direct
mixed-colour edge is retained here explicitly, before diagonal reduction. -/
theorem rootExtract_rowAt_twoColorParameters (W : WeightsN N D K) (p q : V N)
    (b h j : Fin D) (s t : K) :
    rootExtract q j (OddResponseVanishing.rowAt W p (twoColorParameters b h s t)) =
      C (s * edgeMatrix W (p, b) (q, j) + t * edgeMatrix W (p, h) (q, j)) := by
  rw [rowAt_twoColorParameters, rootExtract_add]
  simp only [rootExtract_mul, rootExtract_C, eraseSite_C, zero_mul, zero_add,
    EvenResponse.rootExtract_rowPolynomial]
  rw [← map_mul, ← map_mul, ← map_add]

omit [CharZero K] in
/-- An original pure root word has zero coefficient if the receiving colour
at another retained site is different. -/
theorem coeff_pureRootWord_wrong_color (p q : V N) (hpq : p ≠ q)
    (ι : V N → Fin D) (h : Fin D) (hh : h ≠ ι q) :
    coeff (wordExponent ι ((vertices N).erase p)) (pureRootWord (R := K) p h) = 0 := by
  classical
  have hq : q ∈ (vertices N).erase p :=
    (List.mem_erase_of_ne hpq.symm).mpr (mem_vertices q)
  have hn : ((vertices N).erase p).Nodup := (vertices_nodup N).erase p
  have heq : wordExponent (fun _ => h) ((vertices N).erase p) ≠
      wordExponent ι ((vertices N).erase p) := by
    intro heq
    have he := congrArg (fun n : SiteVariable N D →₀ ℕ => n (q, h)) heq
    rw [wordExponent_selected, hn.count, if_pos hq,
      wordExponent_wrong_color ι _ q h hh] at he
    exact Nat.one_ne_zero he
  rw [pureRootWord, coeff_monomial]
  exact if_neg heq

noncomputable def meanPplane : ReplicaKernel.MeanPolynomial K →+*
    ReplicaKernel.MeanPolynomial K := eval₂Hom C ![X 0, 0, X 2, 0]

noncomputable def meanQplane : ReplicaKernel.MeanPolynomial K →+*
    ReplicaKernel.MeanPolynomial K := eval₂Hom C ![0, X 1, 0, X 3]

omit [CharZero K] in
theorem eval_meanPplane (P : ReplicaKernel.MeanPolynomial K) (a : Fin 4 → K) :
    eval a (meanPplane P) = eval ![a 0, 0, a 2, 0] P := by
  change eval₂ (RingHom.id K) a (eval₂ C ![X 0, 0, X 2, 0] P) = _
  rw [← eval₂_assoc]
  congr 1
  funext j
  fin_cases j <;> simp

/-- The original finite odd tower supplies the numerical endpoint omission
identity. Its higher-response hypotheses concern the actual original root. -/
theorem numerical_source_boundary (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (ι : V (2 * (m + 1)) → Fin D) (hι : ι q = b)
    (hdiag : edgeMatrix W (p, h) (q, b) = 0)
    (hzero : ∀ r, 0 < r → r ≤ m →
      OddResponseVanishing.oddResponsePolynomial W p m r ι = 0) (s t : K) :
    coeff (wordExponent ι (CofactorResponse.retainedVertices p q))
      (C (s * edgeMatrix W (p, b) (q, b)) *
          EvenResponse.evenResponse (K := K) m (retainedQuadratic W p q)
            (C s * retainedRow W p q b + C t * retainedRow W p q h) +
        retainedRow W q p b *
          EvenResponse.lowerOddResponse (K := K) m (retainedQuadratic W p q)
            (C s * retainedRow W p q b + C t * retainedRow W p q h)) =
      s * coeff (wordExponent ι ((vertices (2 * (m + 1))).erase p))
        (pureRootWord p b) := by
  classical
  have hz := OmittedResponse.coeff_omitted_source m W hW p q hpq ι
    (twoColorParameters b h s t) hzero
  rw [hι, rootExtract_rowAt_twoColorParameters, hdiag, mul_zero, add_zero,
    extractedQuadratic_eq_retainedRow W p q b hpq,
    eraseSite_rowAt_twoColorParameters] at hz
  unfold retainedQuadratic
  rw [hz]
  have hpure := coeff_pureRootWord_wrong_color (K := K) p q hpq ι h
    (hι.symm ▸ hbh.symm)
  simp only [twoColorParameters, add_mul, Finset.sum_add_distrib, ite_mul, zero_mul]
  simp only [Finset.sum_ite_eq', Finset.mem_univ, if_true, hpure, mul_zero, add_zero]

/-- The `p`-plane source boundary is an equality of constructed mean
polynomials, proved from the literal omitted source coefficients. -/
theorem mean_source_boundary (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (ι : V (2 * (m + 1)) → Fin D) (hι : ι q = b)
    (hdiag : edgeMatrix W (p, h) (q, b) = 0)
    (hzero : ∀ r, 0 < r → r ≤ m →
      OddResponseVanishing.oddResponsePolynomial W p m r ι = 0) :
    meanPplane (pderiv 1 (endpointResponse m W p q b h
        (wordExponent ι (CofactorResponse.retainedVertices p q))) +
      C (edgeMatrix W (p, b) (q, b)) * X 0 * endpointResponse m W p q b h
        (wordExponent ι (CofactorResponse.retainedVertices p q))) =
      X 0 * C (coeff (wordExponent ι ((vertices (2 * (m + 1))).erase p))
        (pureRootWord p b)) := by
  apply MvPolynomial.funext
  intro a
  rw [eval_meanPplane]
  simp only [map_add, map_mul, eval_C, eval_X]
  rw [eval_pderiv_endpointResponse, eval_endpointResponse]
  have hrow : (∑ j : Fin 4, C (![a 0, 0, a 2, 0] j) * endpointRows W p q b h j) =
      C (a 0) * retainedRow W p q b + C (a 2) * retainedRow W p q h := by
    simp [Fin.sum_univ_succ, endpointRows]
  rw [hrow]
  have hn := numerical_source_boundary m W hW p q hpq b h hbh ι hι hdiag hzero
    (a 0) (a 2)
  rw [coeff_add, coeff_C_mul] at hn
  dsimp [endpointRows]
  convert hn using 1
  ring

omit [CharZero K] in
/-- Ordinary independent mean partials commute as literal polynomial
operations. This does not differentiate a source constraint at a point. -/
theorem mean_pderiv_commute (P : ReplicaKernel.MeanPolynomial K) (i j : Fin 4) :
    pderiv i (pderiv j P) = pderiv j (pderiv i P) := by
  classical
  by_cases hij : i = j
  · subst j
    rfl
  · ext n
    simp only [coeff_pderiv, Finsupp.add_apply, Finsupp.single_apply,
      if_neg hij, if_neg (Ne.symm hij), add_zero]
    rw [show (n + Finsupp.single i 1) + Finsupp.single j 1 =
      (n + Finsupp.single j 1) + Finsupp.single i 1 by ac_rfl]
    ring

omit [CharZero K] in
theorem pderiv_meanPplane_two (P : ReplicaKernel.MeanPolynomial K) :
    pderiv 2 (meanPplane P) = meanPplane (pderiv 2 P) := by
  rw [meanPplane, ReplicaKernel.pderiv_substitution]
  simp [Fin.sum_univ_succ, pderiv_X]

omit [CharZero K] in
theorem meanXAxis_meanPplane (P : ReplicaKernel.MeanPolynomial K) :
    ReplicaKernel.meanXAxis (meanPplane P) = ReplicaKernel.meanXAxis P := by
  have h : ReplicaKernel.meanXAxis.comp (meanPplane (K := K)) =
      ReplicaKernel.meanXAxis := by
    apply MvPolynomial.ringHom_ext
    · intro c
      simp [ReplicaKernel.meanXAxis, meanPplane]
    · intro j
      fin_cases j <;> simp [ReplicaKernel.meanXAxis, meanPplane]
  exact RingHom.congr_fun h P

/-- Differentiating the proved full original-root plane identity supplies
the normal `yu` boundary required by the actual replica kernel. -/
theorem mean_mixed_boundary (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (ι : V (2 * (m + 1)) → Fin D) (hι : ι q = b)
    (hdiag : edgeMatrix W (p, h) (q, b) = 0)
    (hzero : ∀ r, 0 < r → r ≤ m →
      OddResponseVanishing.oddResponsePolynomial W p m r ι = 0) :
    ReplicaKernel.meanXAxis
      (pderiv 1 (pderiv 2 (endpointResponse m W p q b h
        (wordExponent ι (CofactorResponse.retainedVertices p q)))) +
      C (edgeMatrix W (p, b) (q, b)) * X 0 *
        pderiv 2 (endpointResponse m W p q b h
          (wordExponent ι (CofactorResponse.retainedVertices p q)))) = 0 := by
  have hs := congrArg (pderiv (R := K) (σ := Fin 4) 2)
    (mean_source_boundary m W hW p q hpq b h hbh ι hι hdiag hzero)
  rw [pderiv_meanPplane_two] at hs
  rw [(pderiv (R := K) (σ := Fin 4) 2).map_add] at hs
  simp only [pderiv_mul, pderiv_C, pderiv_X_of_ne (by decide : (0 : Fin 4) ≠ 2),
    zero_mul, mul_zero, zero_add, add_zero] at hs
  rw [mean_pderiv_commute _ 2 1] at hs
  have hh := congrArg ReplicaKernel.meanXAxis hs
  rw [meanXAxis_meanPplane, map_zero] at hh
  exact hh

/-- The scalar `x`-axis source equation is obtained by restricting the
already proved two-colour departure-plane equation. -/
theorem mean_scalar_boundary (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (ι : V (2 * (m + 1)) → Fin D) (hι : ι q = b)
    (hdiag : edgeMatrix W (p, h) (q, b) = 0)
    (hzero : ∀ r, 0 < r → r ≤ m →
      OddResponseVanishing.oddResponsePolynomial W p m r ι = 0) :
    ReplicaKernel.meanXAxis
      (pderiv 1 (endpointResponse m W p q b h
        (wordExponent ι (CofactorResponse.retainedVertices p q))) +
      C (edgeMatrix W (p, b) (q, b)) * X 0 * endpointResponse m W p q b h
        (wordExponent ι (CofactorResponse.retainedVertices p q))) =
      X 0 * C (coeff (wordExponent ι ((vertices (2 * (m + 1))).erase p))
        (pureRootWord p b)) := by
  have hs := congrArg ReplicaKernel.meanXAxis
    (mean_source_boundary m W hW p q hpq b h hbh ι hι hdiag hzero)
  rw [meanXAxis_meanPplane] at hs
  simpa [ReplicaKernel.meanXAxis] using hs

/-- The second-colour omission keeps the same actual four-row response;
only its selected receiving colour at the deleted root changes. -/
theorem numerical_second_source_boundary (m : ℕ)
    (W : WeightsN (2 * (m + 1)) D K) (hW : EqSystemN (2 * (m + 1)) D W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (ι : V (2 * (m + 1)) → Fin D) (hι : ι q = h)
    (hdiag : edgeMatrix W (p, b) (q, h) = 0)
    (hzero : ∀ r, 0 < r → r ≤ m →
      OddResponseVanishing.oddResponsePolynomial W p m r ι = 0) (s t : K) :
    coeff (wordExponent ι (CofactorResponse.retainedVertices p q))
      (C (t * edgeMatrix W (p, h) (q, h)) *
          EvenResponse.evenResponse (K := K) m (retainedQuadratic W p q)
            (C s * retainedRow W p q b + C t * retainedRow W p q h) +
        retainedRow W q p h *
          EvenResponse.lowerOddResponse (K := K) m (retainedQuadratic W p q)
            (C s * retainedRow W p q b + C t * retainedRow W p q h)) =
      t * coeff (wordExponent ι ((vertices (2 * (m + 1))).erase p))
        (pureRootWord p h) := by
  classical
  have hz := OmittedResponse.coeff_omitted_source m W hW p q hpq ι
    (twoColorParameters b h s t) hzero
  rw [hι, rootExtract_rowAt_twoColorParameters, hdiag, mul_zero, zero_add,
    extractedQuadratic_eq_retainedRow W p q h hpq,
    eraseSite_rowAt_twoColorParameters] at hz
  unfold retainedQuadratic
  rw [hz]
  have hpure := coeff_pureRootWord_wrong_color (K := K) p q hpq ι b
    (hι.symm ▸ hbh)
  simp only [twoColorParameters, add_mul, Finset.sum_add_distrib, ite_mul, zero_mul]
  simp only [Finset.sum_ite_eq', Finset.mem_univ, if_true, hpure, mul_zero, zero_add]

/-- This is the complete original second-colour plane source equation, with
all finite higher odd responses, rather than an inherited retained source. -/
theorem mean_second_source_boundary (m : ℕ)
    (W : WeightsN (2 * (m + 1)) D K) (hW : EqSystemN (2 * (m + 1)) D W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (ι : V (2 * (m + 1)) → Fin D) (hι : ι q = h)
    (hdiag : edgeMatrix W (p, b) (q, h) = 0)
    (hzero : ∀ r, 0 < r → r ≤ m →
      OddResponseVanishing.oddResponsePolynomial W p m r ι = 0) :
    meanPplane (pderiv 3 (endpointResponse m W p q b h
        (wordExponent ι (CofactorResponse.retainedVertices p q))) +
      C (edgeMatrix W (p, h) (q, h)) * X 2 * endpointResponse m W p q b h
        (wordExponent ι (CofactorResponse.retainedVertices p q))) =
      X 2 * C (coeff (wordExponent ι ((vertices (2 * (m + 1))).erase p))
        (pureRootWord p h)) := by
  apply MvPolynomial.funext
  intro a
  rw [eval_meanPplane]
  simp only [map_add, map_mul, eval_C, eval_X]
  rw [eval_pderiv_endpointResponse, eval_endpointResponse]
  have hrow : (∑ j : Fin 4, C (![a 0, 0, a 2, 0] j) * endpointRows W p q b h j) =
      C (a 0) * retainedRow W p q b + C (a 2) * retainedRow W p q h := by
    simp [Fin.sum_univ_succ, endpointRows]
  rw [hrow]
  have hn := numerical_second_source_boundary m W hW p q hpq b h hbh ι hι hdiag hzero
    (a 0) (a 2)
  rw [coeff_add, coeff_C_mul] at hn
  dsimp [endpointRows]
  convert hn using 1
  ring

/-- The zero `v` response on the first-colour axis is a direct restriction
of the original second-colour source equation. -/
theorem mean_v_boundary (m : ℕ) (W : WeightsN (2 * (m + 1)) D K)
    (hW : EqSystemN (2 * (m + 1)) D W)
    (p q : V (2 * (m + 1))) (hpq : p ≠ q) (b h : Fin D) (hbh : b ≠ h)
    (ι : V (2 * (m + 1)) → Fin D) (hι : ι q = h)
    (hdiag : edgeMatrix W (p, b) (q, h) = 0)
    (hzero : ∀ r, 0 < r → r ≤ m →
      OddResponseVanishing.oddResponsePolynomial W p m r ι = 0) :
    ReplicaKernel.meanXAxis (pderiv 3 (endpointResponse m W p q b h
      (wordExponent ι (CofactorResponse.retainedVertices p q)))) = 0 := by
  have hs := congrArg ReplicaKernel.meanXAxis
    (mean_second_source_boundary m W hW p q hpq b h hbh ι hι hdiag hzero)
  rw [meanXAxis_meanPplane] at hs
  simpa [ReplicaKernel.meanXAxis] using hs

/-- A pure physical word on the two-root-deleted core. -/
noncomputable def pureRetainedWord (p q : V N) (h : Fin D) : PhysicalPolynomial N D K :=
  monomial (wordExponent (fun _ => h) (CofactorResponse.retainedVertices p q)) 1

omit [CharZero K] in
theorem rootExtract_pureRootWord (p q : V N) (hpq : p ≠ q) (i h : Fin D) :
    rootExtract q i (pureRootWord (R := K) p h) =
      if i = h then pureRetainedWord p q h else 0 := by
  classical
  have hq : q ∈ (vertices N).erase p :=
    (List.mem_erase_of_ne hpq.symm).mpr (mem_vertices q)
  have hn : ((vertices N).erase p).Nodup := (vertices_nodup N).erase p
  unfold rootExtract pureRootWord
  rw [pderiv_monomial]
  by_cases hi : i = h
  · subst i
    rw [if_pos rfl, wordExponent_selected, hn.count, if_pos hq]
    simp only [Nat.cast_one, mul_one]
    rw [wordExponent_erase (fun _ => h) _ q hq, add_tsub_cancel_left]
    exact eraseSite_wordMonomial q _ _ hn.not_mem_erase
  · rw [if_neg hi, wordExponent_wrong_color (fun _ => h) _ q i hi]
    simp

theorem coeff_pureRootWord_eq_retained (p q : V N) (hpq : p ≠ q)
    (ι : V N → Fin D) (h : Fin D) (hι : ι q = h) :
    coeff (wordExponent ι ((vertices N).erase p)) (pureRootWord (R := K) p h) =
      coeff (wordExponent ι (CofactorResponse.retainedVertices p q))
        (pureRetainedWord p q h) := by
  rw [← OmittedResponse.coeff_retained_rootExtract _ p q hpq ι, hι,
    rootExtract_pureRootWord p q hpq h h, if_pos rfl]

end KrennAllOrders.PhysicalEndpoint
