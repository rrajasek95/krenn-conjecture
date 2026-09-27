/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import SiteAlgebra
import Mathlib.Algebra.MvPolynomial.Rename

/-!
# Literal root deletion and response tensors

Deleting the root after formal differentiation is essential: differentiation
alone does not descend to the physical-site quotient. This file constructs the
actual root-deletion operation and connects it to the quadratic incident rows.
No response-vanishing or reflection identity is assumed.
-/

namespace KrennAllOrders.RootResponse

open scoped BigOperators
open MatchingModel SiteAlgebra

variable {R : Type*} {N D : ℕ}

section Ring

variable [CommRing R]

/-- Set every local colour at one physical site to zero. -/
noncomputable def eraseSite (p : V N) :
    MatchingPolynomial N D R →+* MatchingPolynomial N D R :=
  MvPolynomial.eval₂Hom MvPolynomial.C
    (fun z => if z.1 = p then 0 else MvPolynomial.X z)

@[simp]
theorem eraseSite_C (p : V N) (a : R) :
    eraseSite (D := D) p (MvPolynomial.C a) = MvPolynomial.C a := by
  simp [eraseSite]

@[simp]
theorem eraseSite_X (p : V N) (z : SiteVariable N D) :
    eraseSite (R := R) p (MvPolynomial.X z) =
      if z.1 = p then 0 else MvPolynomial.X z := by
  simp [eraseSite]

/-- The ordinary representative of root extraction; the root is deleted after differentiation. -/
noncomputable def rootExtract (p : V N) (i : Fin D)
    (P : MatchingPolynomial N D R) : MatchingPolynomial N D R :=
  eraseSite p (MvPolynomial.pderiv (p, i) P)

@[simp]
theorem rootExtract_add (p : V N) (i : Fin D) (P Q : MatchingPolynomial N D R) :
    rootExtract p i (P + Q) = rootExtract p i P + rootExtract p i Q := by
  simp [rootExtract]

@[simp]
theorem rootExtract_C (p : V N) (i : Fin D) (a : R) :
    rootExtract p i (MvPolynomial.C a) = 0 := by simp [rootExtract]

/-- Product rule with both surviving factors evaluated on the deleted-root core. -/
theorem rootExtract_mul (p : V N) (i : Fin D) (P Q : MatchingPolynomial N D R) :
    rootExtract p i (P * Q) =
      rootExtract p i P * eraseSite p Q + eraseSite p P * rootExtract p i Q := by
  simp only [rootExtract, MvPolynomial.pderiv_mul, map_add, map_mul]

/-- Root deletion preserves the physical-site ideal. -/
theorem eraseSite_mem_siteIdeal (p : V N) (P : MatchingPolynomial N D R)
    (hP : P ∈ siteIdeal N D R) : eraseSite p P ∈ siteIdeal N D R := by
  classical
  induction hP using Submodule.span_induction with
  | mem P hP =>
    rcases hP with ⟨v, i, j, rfl⟩
    by_cases hv : v = p
    · simp [hv]
    · simp only [map_mul, eraseSite_X, if_neg hv]
      exact Ideal.subset_span ⟨v, i, j, rfl⟩
  | zero => simp
  | add P Q _ _ ih ih' =>
    rw [map_add]
    exact (siteIdeal N D R).add_mem ih ih'
  | smul A P _ ih =>
    rw [smul_eq_mul, map_mul]
    exact (siteIdeal N D R).mul_mem_left _ ih

/-- Deleting the root makes differentiation well defined modulo the physical-site ideal. -/
theorem rootExtract_mem_siteIdeal (p : V N) (i : Fin D)
    (P : MatchingPolynomial N D R) (hP : P ∈ siteIdeal N D R) :
    rootExtract p i P ∈ siteIdeal N D R := by
  classical
  induction hP using Submodule.span_induction with
  | mem P hP =>
    rcases hP with ⟨v, a, b, rfl⟩
    by_cases hv : v = p
    · simp [rootExtract, hv]
    · have hpa : (p, i) ≠ (v, a) := by
        intro h
        exact hv (congrArg Prod.fst h).symm
      have hpb : (p, i) ≠ (v, b) := by
        intro h
        exact hv (congrArg Prod.fst h).symm
      simp [rootExtract, hpa, hpb]
  | zero => simp [rootExtract]
  | add P Q _ _ ih ih' =>
    rw [rootExtract_add]
    exact (siteIdeal N D R).add_mem ih ih'
  | smul A P hP ih =>
    rw [smul_eq_mul, rootExtract_mul]
    exact (siteIdeal N D R).add_mem
      ((siteIdeal N D R).mul_mem_left _ (eraseSite_mem_siteIdeal p P hP))
      ((siteIdeal N D R).mul_mem_left _ ih)

/-- Equality in the physical-site quotient is preserved by literal root extraction. -/
theorem project_rootExtract_eq (p : V N) (i : Fin D)
    (P Q : MatchingPolynomial N D R) (h : project P = project Q) :
    project (rootExtract p i P) = project (rootExtract p i Q) := by
  have hmem : P - Q ∈ siteIdeal N D R :=
    (Ideal.Quotient.mk_eq_mk_iff_sub_mem P Q).mp h
  have hroot := rootExtract_mem_siteIdeal p i (P - Q) hmem
  apply (Ideal.Quotient.mk_eq_mk_iff_sub_mem _ _).mpr
  simpa [rootExtract] using hroot

end Ring

section Field

variable [Field R] [CharZero R]

omit [CharZero R] in
/-- Actual incident rows have no variables at the deleted root. -/
theorem eraseSite_rowPolynomial (W : WeightsN N D R) (p : V N) (i : Fin D) :
    eraseSite p (rowPolynomial (edgeMatrix W) (p, i)) =
      rowPolynomial (edgeMatrix W) (p, i) := by
  classical
  unfold rowPolynomial
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro z _
  rw [map_mul, eraseSite_C, eraseSite_X]
  rcases z with ⟨v, j⟩
  by_cases hv : v = p
  · subst v
    simp
  · simp [hv]

/-- The actual quadratic on the core obtained by deleting one physical root. -/
noncomputable def deletedQuadratic (W : WeightsN N D R) (p : V N) :
    MatchingPolynomial N D R := eraseSite p (sourceQuadratic W)

/-- The actual root response is its incident row times the divided retained quadratic power. -/
noncomputable def quadraticRootResponse (W : WeightsN N D R)
    (p : V N) (i : Fin D) (k : ℕ) : MatchingPolynomial N D R :=
  MvPolynomial.C ((k.factorial : R)⁻¹) *
    rowPolynomial (edgeMatrix W) (p, i) * deletedQuadratic W p ^ k

/-- Literal formal differentiation gives the exact divided root response, including k=0. -/
theorem rootExtract_dividedSourcePower (W : WeightsN N D R)
    (p : V N) (i : Fin D) (k : ℕ) :
    rootExtract p i (dividedSourcePower W (k + 1)) =
      quadraticRootResponse W p i k := by
  unfold rootExtract dividedSourcePower
  rw [MvPolynomial.pderiv_C_mul, MvPolynomial.pderiv_pow, pderiv_sourceQuadratic]
  simp only [Nat.add_sub_cancel, map_mul, map_pow, eraseSite_C, eraseSite_rowPolynomial]
  have hcast : eraseSite (D := D) p (↑(k + 1) : MatchingPolynomial N D R) =
      MvPolynomial.C (k + 1 : R) := by simp
  rw [hcast]
  have hk : (k + 1 : R) ≠ 0 := by exact_mod_cast Nat.succ_ne_zero k
  have hfactor : ((k + 1).factorial : R)⁻¹ * (k + 1 : R) = (k.factorial : R)⁻¹ := by
    rw [Nat.factorial_succ, Nat.cast_mul, mul_inv_rev]
    simp only [Nat.cast_add, Nat.cast_one]
    rw [mul_assoc, inv_mul_cancel₀ hk, mul_one]
  unfold quadraticRootResponse deletedQuadratic
  have hC : (MvPolynomial.C (((k + 1).factorial : R)⁻¹) *
      MvPolynomial.C (k + 1 : R) : MatchingPolynomial N D R) =
      MvPolynomial.C ((k.factorial : R)⁻¹) := by rw [← map_mul, hfactor]
  calc
    _ = (MvPolynomial.C (((k + 1).factorial : R)⁻¹) * MvPolynomial.C (k + 1 : R)) *
        (rowPolynomial (edgeMatrix W) (p, i) * eraseSite p (sourceQuadratic W) ^ k) := by ring
    _ = _ := by rw [hC]; ring

/-- The model matching tensor has exactly the actual quadratic root response in the quotient. -/
theorem project_rootExtract_matchingPolynomial (k : ℕ)
    (W : WeightsN (2 * (k + 1)) D R) (p : V (2 * (k + 1))) (i : Fin D) :
    project (rootExtract p i (matchingPolynomialN W)) =
      project (quadraticRootResponse W p i k) := by
  have h := project_rootExtract_eq p i _ _ (project_dividedSourcePower_full (k + 1) W)
  rw [rootExtract_dividedSourcePower] at h
  exact h.symm

/-- The recursive matching sum satisfies Laplace expansion at every physical root,
with arbitrary endpoint colours and canonical orientation in either vertex order. -/
theorem pmSumN_rootExpansion (k : ℕ) (W : WeightsN (2 * (k + 1)) D R)
    (ι : V (2 * (k + 1)) → Fin D) (p : V (2 * (k + 1))) :
    pmSumN (2 * (k + 1)) D W ι =
      (((vertices (2 * (k + 1))).erase p).map fun q =>
        edgeMatrix W (p, ι p) (q, ι q) *
          pmSumList W ι (((vertices (2 * (k + 1))).erase p).erase q)).sum := by
  let L := (vertices (2 * (k + 1))).erase p
  have hnodup : L.Nodup := (vertices_nodup _).erase p
  have hp : p ∉ L := (vertices_nodup _).not_mem_erase
  have hlen : L.length = 2 * k + 1 := by
    dsimp [L]
    rw [List.length_erase_of_mem (mem_vertices p)]
    simp
    omega
  have hex : wordExponent ι (p :: L) = wordExponent ι (vertices (2 * (k + 1))) := by
    exact (wordExponent_erase ι _ p (mem_vertices p)).symm
  have hrec := coeff_sourceQuadratic_pow_succ W ι k p L hp hnodup
  rw [hex, coeff_sourceQuadratic_pow_full] at hrec
  have hterm : (L.map fun q => edgeMatrix W (p, ι p) (q, ι q) *
      MvPolynomial.coeff (wordExponent ι (L.erase q)) (sourceQuadratic W ^ k)).sum =
      (k.factorial : R) * (L.map fun q => edgeMatrix W (p, ι p) (q, ι q) *
        pmSumList W ι (L.erase q)).sum := by
    rw [← List.sum_map_mul_left]
    congr 1
    apply List.map_congr_left
    intro q hq
    have hlq : (L.erase q).length = 2 * k := by
      rw [List.length_erase_of_mem hq, hlen]
      omega
    rw [coeff_sourceQuadratic_pow W ι k (L.erase q) hlq
      (List.Pairwise.erase q (List.Pairwise.erase p (vertices_pairwise_lt _)))]
    rw [pmSumList, hlq]
    ring
  rw [hterm] at hrec
  have hfac : ((k + 1).factorial : R) = (k + 1 : R) * (k.factorial : R) := by
    rw [Nat.factorial_succ, Nat.cast_mul, Nat.cast_add, Nat.cast_one]
  have hf : ((k + 1).factorial : R) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero _)
  apply mul_left_cancel₀ hf
  calc
    _ = (k + 1 : R) * ((k.factorial : R) *
      (L.map fun q => edgeMatrix W (p, ι p) (q, ι q) * pmSumList W ι (L.erase q)).sum) := hrec
    _ = _ := by rw [hfac]; ring

/-- The actual pure-colour deleted-pair matching amplitude, with zero diagonal. -/
noncomputable def pureCofactor (W : WeightsN N D R) (h : Fin D) (p q : V N) : R :=
  if p = q then 0 else pmSumList W (fun _ => h) (((vertices N).erase p).erase q)

omit [CharZero R] in
@[simp]
theorem pureCofactor_self (W : WeightsN N D R) (h : Fin D) (p : V N) :
    pureCofactor W h p p = 0 := by simp [pureCofactor]

omit [CharZero R] in
theorem pureCofactor_symm (W : WeightsN N D R) (h : Fin D) (p q : V N) :
    pureCofactor W h p q = pureCofactor W h q p := by
  simp only [pureCofactor]
  by_cases hpq : p = q
  · simp [hpq]
  · rw [if_neg hpq, if_neg (Ne.symm hpq), List.erase_comm]

/-- The unit pure target gives the literal arbitrary-root edge/cofactor row sum. -/
theorem pureCofactor_rowSum_eq_one (k : ℕ) (W : WeightsN (2 * (k + 1)) D R)
    (hW : EqSystemN (2 * (k + 1)) D W) (p : V (2 * (k + 1))) (h : Fin D) :
    ∑ q : V (2 * (k + 1)), edgeMatrix W (p, h) (q, h) * pureCofactor W h p q = 1 := by
  classical
  have htarget : pmSumN (2 * (k + 1)) D W (fun _ => h) = 1 := by
    rw [hW]
    have hc : ∀ L : List (V (2 * (k + 1))), List.IsChain (fun _ _ => True) L := by
      intro L
      induction L with
      | nil => simp
      | cons v L ih => exact List.isChain_cons.mpr ⟨fun _ _ => True.intro, ih⟩
    simp only [allEqual, allEqualList, hc, if_true]
  rw [pmSumN_rootExpansion k W (fun _ => h) p] at htarget
  let L := (vertices (2 * (k + 1))).erase p
  have hL : L.Nodup := (vertices_nodup _).erase p
  have heq : (L.map fun q => edgeMatrix W (p, h) (q, h) *
      pmSumList W (fun _ => h) (L.erase q)).sum =
      ∑ q : V (2 * (k + 1)), edgeMatrix W (p, h) (q, h) * pureCofactor W h p q := by
    rw [← List.sum_toFinset _ hL]
    calc
      _ = ∑ q ∈ L.toFinset, edgeMatrix W (p, h) (q, h) * pureCofactor W h p q := by
        apply Finset.sum_congr rfl
        intro q hq
        have hqp : q ≠ p := by
          intro hqp
          subst q
          exact (vertices_nodup _).not_mem_erase (List.mem_toFinset.mp hq)
        rw [pureCofactor, if_neg (Ne.symm hqp)]
      _ = _ := by
        apply Finset.sum_subset (Finset.subset_univ _)
        intro q _ hq
        have hqp : q = p := by
          by_contra hh
          exact hq (List.mem_toFinset.mpr ((List.mem_erase_of_ne hh).mpr (mem_vertices q)))
        subst q
        simp
  rw [← heq]
  exact htarget

end Field

section SourceTensor

variable [Field R] [CharZero R]

/-- Constant receiving words are monochromatic, including the empty list. -/
theorem allEqual_constant (h : Fin D) : allEqual (fun _ : V N => h) := by
  have hc : ∀ L : List (V N), List.IsChain (fun _ _ => True) L := by
    intro L
    induction L with
    | nil => simp
    | cons v L ih => exact List.isChain_cons.mpr ⟨fun _ _ => True.intro, ih⟩
  simpa only [allEqual, allEqualList] using hc (vertices N)

private theorem colour_pairwise_rel (ι : V N → Fin D) (L : List (V N))
    (hL : L.Pairwise (fun v u => ι v = ι u)) :
    ∀ v ∈ L, ∀ u ∈ L, ι v = ι u := by
  induction L with
  | nil => simp
  | cons a L ih =>
    rcases List.pairwise_cons.mp hL with ⟨hhead, htail⟩
    intro v hv u hu
    rcases List.mem_cons.mp hv with hva | hvL
    · rcases List.mem_cons.mp hu with hua | huL
      · rw [hva, hua]
      · rw [hva]
        exact hhead u huL
    · rcases List.mem_cons.mp hu with hua | huL
      · rw [hua]
        exact (hhead v hvL).symm
      · exact ih htail v hvL u huL

/-- On a nonempty set of physical sites, monochromatic means a literal constant word. -/
theorem allEqual_iff_constant_at (ι : V N → Fin D) (p : V N) :
    allEqual ι ↔ ι = fun _ => ι p := by
  constructor
  · intro h
    have : Trans (fun v u : V N => ι v = ι u)
        (fun v u : V N => ι v = ι u) (fun v u : V N => ι v = ι u) :=
      ⟨fun h₁ h₂ => h₁.trans h₂⟩
    have hp := (show List.IsChain (fun v u => ι v = ι u) (vertices N) from h).pairwise
    funext v
    exact colour_pairwise_rel ι _ hp v (mem_vertices v) p (mem_vertices p)
  · intro h
    rw [h]
    exact allEqual_constant _

/-- Full-site monomials faithfully encode receiving words. -/
theorem wordExponent_full_injective :
    Function.Injective (fun ι : V N → Fin D => wordExponent ι (vertices N)) := by
  intro ι ν heq
  change wordExponent ι (vertices N) = wordExponent ν (vertices N) at heq
  funext v
  by_contra hv
  have hown : wordExponent ι (vertices N) (v, ι v) = 1 := by
    rw [wordExponent_selected, (vertices_nodup N).count]
    simp
  have hzero := wordExponent_wrong_color ν (vertices N) v (ι v) hv
  rw [heq, hzero] at hown
  norm_num at hown

/-- The explicit diagonal target polynomial. Its nonempty-site interpretation is essential. -/
noncomputable def diagonalPolynomial (N D : ℕ) : MatchingPolynomial N D R :=
  ∑ h : Fin D, MvPolynomial.monomial (wordExponent (fun _ => h) (vertices N)) 1

omit [CharZero R] in
theorem coeff_diagonalPolynomial (ι : V N → Fin D) (p : V N) :
    MvPolynomial.coeff (wordExponent ι (vertices N)) (diagonalPolynomial (R := R) N D) =
      if allEqual ι then 1 else 0 := by
  classical
  unfold diagonalPolynomial
  rw [MvPolynomial.coeff_sum]
  by_cases hι : allEqual ι
  · rw [if_pos hι]
    have hc := (allEqual_iff_constant_at ι p).mp hι
    rw [Finset.sum_eq_single (ι p)]
    · rw [← hc]
      simp
    · intro h _ hh
      have hex : wordExponent (fun _ : V N => h) (vertices N) ≠ wordExponent ι (vertices N) := by
        intro heq
        have heq' := wordExponent_full_injective heq
        exact hh (congrFun heq' p)
      simp only [MvPolynomial.coeff_monomial, if_neg hex]
    · simp
  · rw [if_neg hι]
    apply Finset.sum_eq_zero
    intro h _
    have hex : wordExponent (fun _ : V N => h) (vertices N) ≠ wordExponent ι (vertices N) := by
      intro heq
      have heq' := wordExponent_full_injective heq
      apply hι
      rw [← heq']
      exact allEqual_constant h
    simp only [MvPolynomial.coeff_monomial, if_neg hex]

/-- Full pure words have ordinary degree N. -/
theorem wordExponent_full_degree (ι : V N → Fin D) :
    exponentDegree (wordExponent ι (vertices N)) = N := by
  classical
  unfold exponentDegree siteDegree
  have hsite (v : V N) : (∑ i : Fin D, wordExponent ι (vertices N) (v, i)) = 1 := by
    rw [Finset.sum_eq_single (ι v)]
    · rw [wordExponent_selected, (vertices_nodup N).count]
      simp
    · intro i _ hi
      exact wordExponent_wrong_color ι _ v i hi
    · simp
  simp_rw [hsite]
  simp

omit [CharZero R] in
theorem diagonalPolynomial_totalHomogeneous :
    MvPolynomial.IsWeightedHomogeneous (fun _ : SiteVariable N D => (1 : ℕ))
      (diagonalPolynomial (R := R) N D) N := by
  classical
  unfold diagonalPolynomial
  apply MvPolynomial.IsWeightedHomogeneous.sum
  intro h _
  apply MvPolynomial.isWeightedHomogeneous_monomial
  rw [weight_one_eq_exponentDegree, wordExponent_full_degree]

omit [CharZero R] in
/-- The original graph equations give the literal GHZ top tensor in the physical-site algebra. -/
theorem project_matchingPolynomial_eq_diagonal (W : WeightsN N D R)
    (hW : EqSystemN N D W) (p : V N) :
    project (matchingPolynomialN W) = project (diagonalPolynomial (R := R) N D) := by
  apply project_eq_of_full_coefficients _ _ (matchingPolynomialN_totalHomogeneous W)
    diagonalPolynomial_totalHomogeneous
  intro ι
  rw [coeff_matchingPolynomialN, coeff_diagonalPolynomial ι p]
  exact hW ι

omit [CharZero R] in
/-- Root deletion leaves monomials supported on other physical sites unchanged. -/
theorem eraseSite_wordMonomial (p : V N) (ι : V N → Fin D) (L : List (V N))
    (hp : p ∉ L) :
    eraseSite p (MvPolynomial.monomial (wordExponent ι L) (1 : R)) =
      MvPolynomial.monomial (wordExponent ι L) 1 := by
  induction L with
  | nil => simp [wordExponent, MvPolynomial.monomial_eq]
  | cons v L ih =>
    have hvp : v ≠ p := by
      intro h
      subst v
      exact hp (by simp)
    have hpL : p ∉ L := by
      intro h
      exact hp (List.mem_cons_of_mem v h)
    have heq : (MvPolynomial.monomial (wordExponent ι (v :: L)) (1 : R)) =
        MvPolynomial.monomial (wordExponent ι L) 1 * MvPolynomial.X (v, ι v) := by
      rw [wordExponent, add_comm, MvPolynomial.monomial_add_single, pow_one]
    rw [heq, map_mul, eraseSite_X, if_neg hvp, ih hpL]

/-- The pure target with its root removed. -/
noncomputable def pureRootWord (p : V N) (h : Fin D) : MatchingPolynomial N D R :=
  MvPolynomial.monomial (wordExponent (fun _ => h) ((vertices N).erase p)) 1

omit [CharZero R] in
theorem rootExtract_pureWord (p : V N) (i h : Fin D) :
    rootExtract p i (MvPolynomial.monomial (wordExponent (fun _ : V N => h) (vertices N)) (1 : R)) =
      if i = h then pureRootWord p h else 0 := by
  classical
  unfold rootExtract
  rw [MvPolynomial.pderiv_monomial]
  by_cases hi : i = h
  · subst i
    rw [if_pos rfl, wordExponent_selected, (vertices_nodup N).count]
    simp only [mem_vertices, if_true, Nat.cast_one, mul_one]
    rw [wordExponent_erase (fun _ => h) (vertices N) p (mem_vertices p),
      add_tsub_cancel_left]
    exact eraseSite_wordMonomial p _ _ (vertices_nodup N).not_mem_erase
  · rw [if_neg hi, wordExponent_wrong_color (fun _ => h) (vertices N) p i hi]
    simp

omit [CharZero R] in
theorem rootExtract_diagonalPolynomial (p : V N) (i : Fin D) :
    rootExtract p i (diagonalPolynomial (R := R) N D) = pureRootWord p i := by
  classical
  unfold diagonalPolynomial rootExtract
  simp only [map_sum]
  change (∑ h : Fin D, rootExtract p i
    (MvPolynomial.monomial (wordExponent (fun _ => h) (vertices N)) (1 : R))) = _
  simp_rw [rootExtract_pureWord]
  simp

/-- The actual original incident response has only its corresponding pure receiving word. -/
theorem quadraticRootResponse_eq_pure (k : ℕ) (W : WeightsN (2 * (k + 1)) D R)
    (hW : EqSystemN (2 * (k + 1)) D W) (p : V (2 * (k + 1))) (i : Fin D) :
    project (quadraticRootResponse W p i k) = project (pureRootWord p i) := by
  rw [← project_rootExtract_matchingPolynomial]
  have h := project_rootExtract_eq p i _ _ (project_matchingPolynomial_eq_diagonal W hW p)
  rw [rootExtract_diagonalPolynomial] at h
  exact h

/-- A linear family of actual incident rows; the multipliers may themselves be polynomials. -/
noncomputable def rootFamilyRow (W : WeightsN N D R) (p : V N)
    (a : Fin D → MatchingPolynomial N D R) : MatchingPolynomial N D R :=
  ∑ i : Fin D, a i * rowPolynomial (edgeMatrix W) (p, i)

/-- Original graph equations determine the whole root-row family response, with
arbitrary polynomial multipliers and no retained-response hypothesis. -/
theorem rootFamily_response_eq_pure (k : ℕ) (W : WeightsN (2 * (k + 1)) D R)
    (hW : EqSystemN (2 * (k + 1)) D W) (p : V (2 * (k + 1)))
    (a : Fin D → MatchingPolynomial (2 * (k + 1)) D R) :
    project (MvPolynomial.C ((k.factorial : R)⁻¹) *
        rootFamilyRow W p a * deletedQuadratic W p ^ k) =
      ∑ i : Fin D, project (a i) * project (pureRootWord p i) := by
  classical
  have hpoly : MvPolynomial.C ((k.factorial : R)⁻¹) * rootFamilyRow W p a *
      deletedQuadratic W p ^ k = ∑ i : Fin D, a i * quadraticRootResponse W p i k := by
    unfold rootFamilyRow quadraticRootResponse
    simp only [Finset.mul_sum, Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [hpoly, map_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [map_mul, quadraticRootResponse_eq_pure k W hW p i]

end SourceTensor

end KrennAllOrders.RootResponse
