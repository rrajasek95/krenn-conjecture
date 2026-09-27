/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import RootResponse
import ResponseFactor
import FiniteResponseRigidity
import Mathlib.Algebra.CharZero.Infinite

/-!
# Actual finite odd root responses

The response objects here are constructed from the original incident rows and
literal deleted quadratic. Parameter-polynomial coefficients are extracted
from the physical-site quotient by a proved additive coefficient map. The
terminal response of degree N-1 is present. Reflection and replica rotation
will be connected to these objects through the explicit finite Wick bridge;
they are not built into the definitions.
-/

namespace KrennAllOrders.OddResponseVanishing

open scoped BigOperators
open MatchingModel SiteAlgebra RootResponse

variable {K : Type*} {N D : ℕ}

section Ring

variable [CommRing K]

/-- Scalars embedded into the actual physical-site algebra. -/
noncomputable def siteScalar : K →+* SiteRing N D K := project.comp MvPolynomial.C

@[simp]
theorem siteScalar_apply (a : K) :
    siteScalar (N := N) (D := D) a = project (MvPolynomial.C a) := rfl

/-- Receiving-word coefficients on the root-deleted sites. -/
noncomputable def retainedCoefficient (p : V N) (ι : V N → Fin D)
    (q : SiteRing N D K) : K :=
  MvPolynomial.coeff (wordExponent ι ((vertices N).erase p)) (Quotient.out q)

@[simp]
theorem retainedCoefficient_project (p : V N) (ι : V N → Fin D)
    (P : MatchingPolynomial N D K) :
    retainedCoefficient p ι (project P) =
      MvPolynomial.coeff (wordExponent ι ((vertices N).erase p)) P := by
  apply coeff_eq_of_project_eq ι _ ((vertices_nodup N).erase p)
  exact Ideal.Quotient.mk_out (project P)

/-- Coefficient extraction on the retained physical tensor is additive. -/
noncomputable def retainedCoefficientHom (p : V N) (ι : V N → Fin D) :
    SiteRing N D K →+ K where
  toFun := retainedCoefficient p ι
  map_zero' := by
    rw [← map_zero project, retainedCoefficient_project]
    exact MvPolynomial.coeff_zero _
  map_add' := by
    intro q r
    obtain ⟨P, rfl⟩ := Ideal.Quotient.mk_surjective q
    obtain ⟨Q, rfl⟩ := Ideal.Quotient.mk_surjective r
    change retainedCoefficient p ι (project P + project Q) =
      retainedCoefficient p ι (project P) + retainedCoefficient p ι (project Q)
    calc
      _ = retainedCoefficient p ι (project (P + Q)) :=
        congrArg (retainedCoefficient p ι) (map_add project P Q).symm
      _ = _ := by rw [retainedCoefficient_project, MvPolynomial.coeff_add,
        retainedCoefficient_project, retainedCoefficient_project]

/-- Scalar linearity of retained-word extraction. -/
theorem retainedCoefficient_scalar_mul (p : V N) (ι : V N → Fin D)
    (a : K) (q : SiteRing N D K) :
    retainedCoefficient p ι (siteScalar a * q) = a * retainedCoefficient p ι q := by
  obtain ⟨P, rfl⟩ := Ideal.Quotient.mk_surjective q
  change retainedCoefficient p ι (project (MvPolynomial.C a) * project P) =
    a * retainedCoefficient p ι (project P)
  calc
    _ = retainedCoefficient p ι (project (MvPolynomial.C a * P)) :=
      congrArg (retainedCoefficient p ι) (map_mul project (MvPolynomial.C a) P).symm
    _ = _ := by rw [retainedCoefficient_project, MvPolynomial.coeff_C_mul,
      retainedCoefficient_project]

/-- A polynomial in independent row parameters, with physical tensors as coefficients. -/
abbrev ParameterTensor (N D : ℕ) (K : Type*) [CommRing K] :=
  MvPolynomial (Fin D) (SiteRing N D K)

/-- Apply a receiving-word coefficient functional coefficientwise to the row parameters. -/
noncomputable def coefficientPolynomial (p : V N) (ι : V N → Fin D)
    (T : ParameterTensor N D K) : MvPolynomial (Fin D) K :=
  AddMonoidAlgebra.map (retainedCoefficientHom p ι) T

@[simp]
theorem coeff_coefficientPolynomial (p : V N) (ι : V N → Fin D)
    (T : ParameterTensor N D K) (s : Fin D →₀ ℕ) :
    MvPolynomial.coeff s (coefficientPolynomial p ι T) =
      retainedCoefficient p ι (MvPolynomial.coeff s T) :=
  MvPolynomial.coeff_addMonoidAlgebraMap _ _ _

/-- Parameter specialization commutes with the literal physical coefficient functional. -/
theorem eval_coefficientPolynomial (p : V N) (ι : V N → Fin D)
    (T : ParameterTensor N D K) (a : Fin D → K) :
    MvPolynomial.eval a (coefficientPolynomial p ι T) =
      retainedCoefficient p ι (MvPolynomial.eval (fun i => siteScalar (a i)) T) := by
  classical
  induction T using MvPolynomial.induction_on' with
  | monomial m c =>
    unfold coefficientPolynomial
    have hmap : AddMonoidAlgebra.map (retainedCoefficientHom p ι)
        (MvPolynomial.monomial m c) =
        MvPolynomial.monomial m (retainedCoefficient p ι c) :=
      AddMonoidAlgebra.map_single _ _ _
    rw [hmap, MvPolynomial.eval_monomial, MvPolynomial.eval_monomial]
    have hprod : m.prod (fun i n => siteScalar (N := N) (D := D) (a i) ^ n) =
        siteScalar (m.prod (fun i n => a i ^ n)) := by
      rw [map_finsuppProd]
      simp only [map_pow]
    rw [hprod, mul_comm c, retainedCoefficient_scalar_mul]
    ring
  | add P Q ih ih' =>
    have hadd : retainedCoefficient p ι
        (MvPolynomial.eval (fun i => siteScalar (a i)) P +
          MvPolynomial.eval (fun i => siteScalar (a i)) Q) =
        retainedCoefficient p ι (MvPolynomial.eval (fun i => siteScalar (a i)) P) +
          retainedCoefficient p ι (MvPolynomial.eval (fun i => siteScalar (a i)) Q) :=
      (retainedCoefficientHom p ι).map_add _ _
    simp only [coefficientPolynomial, AddMonoidAlgebra.map_add, map_add] at ih ih' ⊢
    rw [hadd, ih, ih']

/-- Extraction cannot create a monomial of a new parameter degree. -/
theorem coefficientPolynomial_homogeneous (p : V N) (ι : V N → Fin D)
    (T : ParameterTensor N D K) (n : ℕ)
    (hT : MvPolynomial.IsWeightedHomogeneous (fun _ : Fin D => (1 : ℕ)) T n) :
    MvPolynomial.IsWeightedHomogeneous (fun _ : Fin D => (1 : ℕ))
      (coefficientPolynomial p ι T) n := by
  intro m hm
  rw [coeff_coefficientPolynomial] at hm
  apply hT
  intro hz
  rw [hz] at hm
  exact hm ((retainedCoefficientHom p ι).map_zero)

end Ring

section Field

variable [Field K] [CharZero K]

/-- The original incident row family evaluated at a numerical parameter vector. -/
noncomputable def rowAt (W : WeightsN N D K) (p : V N) (a : Fin D → K) :
    MatchingPolynomial N D K := rootFamilyRow W p (fun i => MvPolynomial.C (a i))

/-- The raw odd response at degree 2r+1; degrees beyond the retained sites are explicitly zero. -/
noncomputable def oddResponse (W : WeightsN N D K) (p : V N)
    (k r : ℕ) (a : Fin D → K) : SiteRing N D K :=
  if r ≤ k then project (MvPolynomial.C (((k - r).factorial : K)⁻¹) *
    rowAt W p a ^ (2 * r + 1) * deletedQuadratic W p ^ (k - r)) else 0

/-- The complete finite odd tower is represented by the actual coordinate row parameters. -/
noncomputable def parameterRow (W : WeightsN N D K) (p : V N) : ParameterTensor N D K :=
  ∑ i : Fin D, MvPolynomial.X i *
    MvPolynomial.C (project (rowPolynomial (edgeMatrix W) (p, i)))

/-- The same raw response as a polynomial family; no higher response identity is assumed. -/
noncomputable def oddResponseTensor (W : WeightsN N D K) (p : V N)
    (k r : ℕ) : ParameterTensor N D K :=
  if r ≤ k then MvPolynomial.C (siteScalar (((k - r).factorial : K)⁻¹)) *
    parameterRow W p ^ (2 * r + 1) *
      MvPolynomial.C (project (deletedQuadratic W p)) ^ (k - r) else 0

/-- The actual receiving-word response polynomial used by the reflection argument. -/
noncomputable def oddResponsePolynomial (W : WeightsN N D K) (p : V N)
    (k r : ℕ) (ι : V N → Fin D) : MvPolynomial (Fin D) K :=
  coefficientPolynomial p ι (oddResponseTensor W p k r)

omit [CharZero K] in
theorem eval_parameterRow (W : WeightsN N D K) (p : V N) (a : Fin D → K) :
    MvPolynomial.eval (fun i => siteScalar (N := N) (D := D) (a i)) (parameterRow W p) =
      project (rowAt W p a) := by
  classical
  unfold parameterRow rowAt rootFamilyRow
  simp only [map_sum, map_mul, MvPolynomial.eval_X, MvPolynomial.eval_C, siteScalar_apply]

omit [CharZero K] in
/-- Evaluation of the formal parameter tensor gives the actual physical response. -/
theorem eval_oddResponseTensor (W : WeightsN N D K) (p : V N)
    (k r : ℕ) (a : Fin D → K) :
    MvPolynomial.eval (fun i => siteScalar (N := N) (D := D) (a i))
      (oddResponseTensor W p k r) = oddResponse W p k r a := by
  unfold oddResponseTensor oddResponse
  by_cases hr : r ≤ k
  · rw [if_pos hr, if_pos hr]
    simp only [map_mul, map_pow, MvPolynomial.eval_C]
    rw [eval_parameterRow]
    simp only [siteScalar_apply]
  · rw [if_neg hr, if_neg hr, map_zero]

omit [CharZero K] in
/-- The constructed parameter response polynomial evaluates to its literal receiving amplitude. -/
theorem eval_oddResponsePolynomial (W : WeightsN N D K) (p : V N)
    (k r : ℕ) (ι : V N → Fin D) (a : Fin D → K) :
    MvPolynomial.eval a (oddResponsePolynomial W p k r ι) =
      retainedCoefficient p ι (oddResponse W p k r a) := by
  rw [oddResponsePolynomial, eval_coefficientPolynomial, eval_oddResponseTensor]

/-- The actual source's linear response is its original pure target family. -/
theorem oddResponse_zero (k : ℕ) (W : WeightsN (2 * (k + 1)) D K)
    (hW : EqSystemN (2 * (k + 1)) D W) (p : V (2 * (k + 1))) (a : Fin D → K) :
    oddResponse W p k 0 a = ∑ i : Fin D, siteScalar (a i) * project (pureRootWord p i) := by
  simp only [oddResponse, Nat.zero_le, if_true, Nat.sub_zero, Nat.mul_zero,
    zero_add, pow_one, rowAt, siteScalar_apply]
  exact rootFamily_response_eq_pure k W hW p _

omit [CharZero K] in
/-- The terminal degree N-1 is the raw row power, not omitted by a negative divided power. -/
theorem oddResponse_terminal (W : WeightsN N D K) (p : V N) (k : ℕ) (a : Fin D → K) :
    oddResponse W p k k a = project (rowAt W p a ^ (2 * k + 1)) := by
  simp [oddResponse]

omit [CharZero K] in
@[simp]
theorem oddResponse_above_terminal (W : WeightsN N D K) (p : V N)
    (k r : ℕ) (hr : k < r) (a : Fin D → K) : oddResponse W p k r a = 0 := by
  simp [oddResponse, Nat.not_le_of_gt hr]

omit [CharZero K] in
/-- The actual parameter row is linear in the independent row coordinates. -/
theorem parameterRow_homogeneous (W : WeightsN N D K) (p : V N) :
    MvPolynomial.IsWeightedHomogeneous (fun _ : Fin D => (1 : ℕ)) (parameterRow W p) 1 := by
  classical
  unfold parameterRow
  apply MvPolynomial.IsWeightedHomogeneous.sum
  intro i _
  simpa using
    (MvPolynomial.isWeightedHomogeneous_X (SiteRing N D K) (fun _ : Fin D => (1 : ℕ)) i).mul
      (MvPolynomial.isWeightedHomogeneous_C (fun _ : Fin D => (1 : ℕ))
        (project (rowPolynomial (edgeMatrix W) (p, i))))

omit [CharZero K] in
/-- Every raw response has exactly its claimed odd parameter degree, including terminal degree. -/
theorem oddResponseTensor_homogeneous (W : WeightsN N D K) (p : V N) (k r : ℕ) :
    MvPolynomial.IsWeightedHomogeneous (fun _ : Fin D => (1 : ℕ))
      (oddResponseTensor W p k r) (2 * r + 1) := by
  unfold oddResponseTensor
  by_cases hr : r ≤ k
  · rw [if_pos hr]
    simpa [nsmul_eq_mul] using
      ((parameterRow_homogeneous W p).pow (2 * r + 1)).C_mul
        (siteScalar (((k - r).factorial : K)⁻¹)) |>.mul
      ((MvPolynomial.isWeightedHomogeneous_C (fun _ : Fin D => (1 : ℕ))
        (project (deletedQuadratic W p))).pow (k - r))
  · rw [if_neg hr]
    exact MvPolynomial.isWeightedHomogeneous_zero _ _ _

omit [CharZero K] in
theorem oddResponsePolynomial_homogeneous (W : WeightsN N D K) (p : V N)
    (k r : ℕ) (ι : V N → Fin D) :
    MvPolynomial.IsWeightedHomogeneous (fun _ : Fin D => (1 : ℕ))
      (oddResponsePolynomial W p k r ι) (2 * r + 1) :=
  coefficientPolynomial_homogeneous p ι _ _ (oddResponseTensor_homogeneous W p k r)

omit [CharZero K] in
/-- A pure receiving word extracts precisely its matching pure target coordinate. -/
theorem retainedCoefficient_pureRootWord (p q : V N) (hqp : q ≠ p) (h i : Fin D) :
    retainedCoefficient (K := K) p (fun _ => h) (project (pureRootWord (R := K) p i)) =
      if h = i then 1 else 0 := by
  classical
  rw [pureRootWord, retainedCoefficient_project, MvPolynomial.coeff_monomial]
  by_cases hi : h = i
  · simp [hi]
  · have hq : q ∈ (vertices N).erase p :=
      (List.mem_erase_of_ne hqp).mpr (mem_vertices q)
    have hone : wordExponent (fun _ : V N => i) ((vertices N).erase p) (q, i) = 1 := by
      rw [wordExponent_selected, ((vertices_nodup N).erase p).count, if_pos hq]
    have hzero := wordExponent_wrong_color (fun _ : V N => h) ((vertices N).erase p)
      q i (Ne.symm hi)
    have hex : wordExponent (fun _ : V N => i) ((vertices N).erase p) ≠
        wordExponent (fun _ : V N => h) ((vertices N).erase p) := by
      intro heq
      rw [heq, hzero] at hone
      norm_num at hone
    rw [if_neg hex, if_neg hi]

/-- The linear pure response polynomial is the independent coordinate X_h.
This is the actual source input to polynomial cancellation in the reflection proof. -/
theorem oddResponsePolynomial_zero_pure (k : ℕ) (W : WeightsN (2 * (k + 1)) D K)
    (hW : EqSystemN (2 * (k + 1)) D W) (p : V (2 * (k + 1))) (h : Fin D) :
    oddResponsePolynomial W p k 0 (fun _ => h) = MvPolynomial.X h := by
  classical
  have hlen : ((vertices (2 * (k + 1))).erase p).length = 2 * k + 1 := by
    rw [List.length_erase_of_mem (mem_vertices p)]
    simp
    omega
  have hne : (vertices (2 * (k + 1))).erase p ≠ [] := by
    intro hh
    rw [hh] at hlen
    simp at hlen
  obtain ⟨q, hq⟩ := List.exists_mem_of_ne_nil _ hne
  have hqp : q ≠ p := by
    intro hh
    subst q
    exact (vertices_nodup _).not_mem_erase hq
  apply MvPolynomial.funext
  intro a
  rw [eval_oddResponsePolynomial, oddResponse_zero k W hW p a, MvPolynomial.eval_X]
  have hsum : retainedCoefficient p (fun _ => h)
      (∑ i : Fin D, siteScalar (a i) * project (pureRootWord p i)) =
      ∑ i : Fin D, retainedCoefficient p (fun _ => h)
        (siteScalar (a i) * project (pureRootWord p i)) :=
      map_sum (retainedCoefficientHom p (fun _ => h)) _ _
  rw [hsum]
  simp_rw [retainedCoefficient_scalar_mul, retainedCoefficient_pureRootWord p q hqp]
  simp

omit [CharZero K] in
/-- Once the explicitly stated reflection cross identities are supplied, the actual
pure response polynomials have a common polynomial factor, without rational division. -/
theorem pure_response_common_factor (W : WeightsN N D K) (p : V N) (k r : ℕ)
    {a b : Fin D} (hab : a ≠ b)
    (hreflection : ∀ i j : Fin D,
      MvPolynomial.X i * oddResponsePolynomial W p k r (fun _ => j) =
        MvPolynomial.X j * oddResponsePolynomial W p k r (fun _ => i)) :
    ∃ q : MvPolynomial (Fin D) K, ∀ i : Fin D,
      oddResponsePolynomial W p k r (fun _ => i) = MvPolynomial.X i * q :=
  ResponseFactor.exists_common_factor _ hab hreflection

omit [CharZero K] in
/-- The common scalar factor has its exact even degree. -/
theorem pure_response_factor_homogeneous (W : WeightsN N D K) (p : V N) (k r : ℕ)
    (i : Fin D) (q : MvPolynomial (Fin D) K)
    (hq : oddResponsePolynomial W p k r (fun _ => i) = MvPolynomial.X i * q) :
    MvPolynomial.IsWeightedHomogeneous (fun _ : Fin D => (1 : ℕ)) q (2 * r) := by
  intro m hm
  have hpoly := oddResponsePolynomial_homogeneous W p k r (fun _ => i)
  rw [hq] at hpoly
  have hc : MvPolynomial.coeff (Finsupp.single i 1 + m) (MvPolynomial.X i * q) ≠ 0 := by
    rw [MvPolynomial.coeff_X_mul]
    exact hm
  have hd := hpoly hc
  rw [map_add, Finsupp.weight_single] at hd
  simp only [one_nsmul] at hd
  omega

/-- A nonzero independent linear response kills a mixed coefficient once its
reflection product is known. It does not cancel at individual parameter values. -/
theorem mixed_response_zero_of_reflection (W : WeightsN N D K) (p : V N)
    (k r : ℕ) (ι : V N → Fin D) (h : Fin D)
    (hreflection : MvPolynomial.X h * oddResponsePolynomial W p k r ι = 0) :
    oddResponsePolynomial W p k r ι = 0 :=
  ResponseFactor.mixed_response_eq_zero (MvPolynomial.X_ne_zero h) hreflection

/-- The finite scalar factor uses exactly the odd-response factorial normalization. -/
noncomputable def finiteScalarFactor (k : ℕ) (q : ℕ → MvPolynomial (Fin D) K) :
    MvPolynomial (Fin D) K :=
  ∑ r ∈ Finset.range (k + 1), MvPolynomial.C (((2 * r + 1).factorial : K)⁻¹) * q r

omit [CharZero K] in
/-- Exact even degrees and the original linear response give the normalization at zero. -/
theorem finiteScalarFactor_eval_zero (k : ℕ) (q : ℕ → MvPolynomial (Fin D) K)
    (hq : ∀ r ≤ k, MvPolynomial.IsWeightedHomogeneous (fun _ : Fin D => (1 : ℕ)) (q r) (2 * r))
    (hzero : q 0 = 1) : MvPolynomial.eval (fun _ => 0) (finiteScalarFactor k q) = 1 := by
  classical
  unfold finiteScalarFactor
  rw [map_sum, Finset.sum_eq_single 0]
  · simp [hzero]
  · intro r hr hr0
    have hrk : r ≤ k := by
      have := Finset.mem_range.mp hr
      omega
    have heval : MvPolynomial.eval (fun _ => 0) (q r) = 0 := by
      rw [MvPolynomial.eval_zero']
      change MvPolynomial.coeff 0 (q r) = 0
      exact (hq r hrk).coeff_eq_zero 0 (by simp only [map_zero]; omega)
    rw [map_mul, MvPolynomial.eval_C, heval, mul_zero]
  · simp

/-- The actual original linear pure response fixes its common factor to one. -/
theorem pure_linear_factor_eq_one (k : ℕ) (W : WeightsN (2 * (k + 1)) D K)
    (hW : EqSystemN (2 * (k + 1)) D W) (p : V (2 * (k + 1)))
    (i : Fin D) (q : MvPolynomial (Fin D) K)
    (hq : oddResponsePolynomial W p k 0 (fun _ => i) = MvPolynomial.X i * q) : q = 1 := by
  rw [oddResponsePolynomial_zero_pure k W hW p i] at hq
  apply mul_left_cancel₀ (MvPolynomial.X_ne_zero (R := K) i)
  simpa only [mul_one] using hq.symm

/-- Distinct even homogeneous degrees prevent cancellation between normalized response factors. -/
theorem factors_zero_of_finiteScalarFactor_eq_one (k : ℕ)
    (q : ℕ → MvPolynomial (Fin D) K)
    (hq : ∀ r ≤ k, MvPolynomial.IsWeightedHomogeneous (fun _ : Fin D => (1 : ℕ)) (q r) (2 * r))
    (hsum : finiteScalarFactor k q = 1) (r : ℕ) (hr : r ≤ k) (hpos : 0 < r) : q r = 0 := by
  classical
  let w := fun _ : Fin D => (1 : ℕ)
  have hh := congrArg (MvPolynomial.weightedHomogeneousComponent w (2 * r)) hsum
  unfold finiteScalarFactor at hh
  rw [map_sum, Finset.sum_eq_single r] at hh
  · have hsame : MvPolynomial.weightedHomogeneousComponent w (2 * r)
        (MvPolynomial.C (((2 * r + 1).factorial : K)⁻¹) * q r) =
        MvPolynomial.C (((2 * r + 1).factorial : K)⁻¹) * q r :=
      MvPolynomial.weightedHomogeneousComponent_eq_self ((hq r hr).C_mul _)
    have hone : MvPolynomial.weightedHomogeneousComponent w (2 * r)
        (1 : MvPolynomial (Fin D) K) = 0 :=
      (MvPolynomial.isWeightedHomogeneous_one K w).weightedHomogeneousComponent_ne (2 * r) (by omega)
    rw [hsame, hone] at hh
    have hnz : (MvPolynomial.C (((2 * r + 1).factorial : K)⁻¹) : MvPolynomial (Fin D) K) ≠ 0 := by
      apply MvPolynomial.C_ne_zero.mpr
      exact inv_ne_zero (Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero _))
    exact (mul_eq_zero.mp hh).resolve_left hnz
  · intro s hs hsr
    have hs' : s ≤ k := by
      have := Finset.mem_range.mp hs
      omega
    have hhom := (hq s hs').C_mul (((2 * s + 1).factorial : K)⁻¹)
    exact hhom.weightedHomogeneousComponent_ne (2 * r) (by omega)
  · intro hnot
    exact False.elim (hnot (Finset.mem_range.mpr (by omega)))

/-- Degree rigidity removes every higher pure factor once the genuine replica
rotation has provided the explicitly stated rescaling equation. -/
theorem factors_zero_of_rescaling_square (k : ℕ)
    (q : ℕ → MvPolynomial (Fin D) K)
    (hq : ∀ r ≤ k, MvPolynomial.IsWeightedHomogeneous (fun _ : Fin D => (1 : ℕ)) (q r) (2 * r))
    (s : K) (hs : s ≠ 0)
    (hzero : MvPolynomial.eval (fun _ => 0) (finiteScalarFactor k q) = 1)
    (hrotation : (FiniteResponseRigidity.scaleVariables s (finiteScalarFactor k q)) ^ 2 =
      finiteScalarFactor k q) (r : ℕ) (hr : r ≤ k) (hpos : 0 < r) : q r = 0 := by
  have hg := FiniteResponseRigidity.eq_one_of_rescaling_square _ s hs hzero hrotation
  exact factors_zero_of_finiteScalarFactor_eq_one k q hq hg r hr hpos

/-- The complete algebraic tail, with only the genuine replica rescaling identity
left explicit; the normalization is derived from the original linear factor. -/
theorem factors_zero_of_normalized_rotation (k : ℕ)
    (q : ℕ → MvPolynomial (Fin D) K)
    (hq : ∀ r ≤ k, MvPolynomial.IsWeightedHomogeneous (fun _ : Fin D => (1 : ℕ)) (q r) (2 * r))
    (hzero : q 0 = 1) (s : K) (hs : s ≠ 0)
    (hrotation : (FiniteResponseRigidity.scaleVariables s (finiteScalarFactor k q)) ^ 2 =
      finiteScalarFactor k q) (r : ℕ) (hr : r ≤ k) (hpos : 0 < r) : q r = 0 :=
  factors_zero_of_rescaling_square k q hq s hs (finiteScalarFactor_eval_zero k q hq hzero)
    hrotation r hr hpos

end Field

end KrennAllOrders.OddResponseVanishing
