/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import RootResponse
import CofactorDiagonal

/-! # Literal cofactor sums as retained two-row coefficients -/

namespace KrennAllOrders.CofactorResponse

open MatchingModel SiteAlgebra RootResponse
open scoped BigOperators

variable {R : Type*} [Field R] [CharZero R] {N D : ℕ}

omit [CharZero R] in
/-- Deleting variables absent from a selected exponent cannot change that
coefficient, for an arbitrary polynomial representative. -/
theorem coeff_eraseSite_of_omitted (p : V N) (P : MatchingPolynomial N D R)
    (m : SiteVariable N D →₀ ℕ) (hm : ∀ i, m (p, i) = 0) :
    MvPolynomial.coeff m (eraseSite p P) = MvPolynomial.coeff m P := by
  classical
  induction P using MvPolynomial.induction_on generalizing m with
  | C a => rw [eraseSite_C]
  | add P Q hP hQ =>
    rw [map_add, MvPolynomial.coeff_add, MvPolynomial.coeff_add, hP _ hm, hQ _ hm]
  | mul_X P z hP =>
    rw [map_mul, eraseSite_X]
    by_cases hz : z.1 = p
    · have hmz : m z = 0 := by simpa only [← hz] using hm z.2
      simp only [if_pos hz, mul_zero, MvPolynomial.coeff_zero,
        MvPolynomial.coeff_mul_X', Finsupp.mem_support_iff, hmz, ne_eq,
        not_true_eq_false, if_false]
    · rw [if_neg hz, MvPolynomial.coeff_mul_X', MvPolynomial.coeff_mul_X']
      congr 1
      apply hP
      intro i
      simp only [Finsupp.tsub_apply, hm, Nat.zero_sub]

omit [CharZero R] in
theorem coeff_word_eraseSite (p : V N) (P : MatchingPolynomial N D R)
    (ι : V N → Fin D) (L : List (V N)) (hp : p ∉ L) :
    MvPolynomial.coeff (wordExponent ι L) (eraseSite p P) =
      MvPolynomial.coeff (wordExponent ι L) P :=
  coeff_eraseSite_of_omitted p P _ (wordExponent_not_mem ι L p hp)

theorem coeff_dividedSourcePower_list (W : WeightsN N D R) (ι : V N → Fin D)
    (k : ℕ) (L : List (V N)) (hlen : L.length = 2 * k) (hL : L.Pairwise (· < ·)) :
    MvPolynomial.coeff (wordExponent ι L) (dividedSourcePower W k) =
      pmSumList W ι L := by
  rw [dividedSourcePower, MvPolynomial.coeff_C_mul,
    coeff_sourceQuadratic_pow W ι k L hlen hL, pmSumList, hlen]
  rw [← mul_assoc, inv_mul_cancel₀ (Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero k)), one_mul]

/-- Laplace expansion at any retained root of any ordered even vertex list. -/
theorem pmSumList_rootExpansion (W : WeightsN N D R) (ι : V N → Fin D)
    (k : ℕ) (S : List (V N)) (hlenS : S.length = 2 * (k + 1))
    (hS : S.Pairwise (· < ·)) (p : V N) (hpS : p ∈ S) :
    pmSumList W ι S = ((S.erase p).map fun q =>
      edgeMatrix W (p, ι p) (q, ι q) * pmSumList W ι ((S.erase p).erase q)).sum := by
  have hSnodup : S.Nodup := hS.imp (fun h => ne_of_lt h)
  let L := S.erase p
  have hnodup : L.Nodup := hSnodup.erase p
  have hp : p ∉ L := hSnodup.not_mem_erase
  have hlen : L.length = 2 * k + 1 := by
    dsimp [L]
    rw [List.length_erase_of_mem hpS, hlenS]
    omega
  have hex : wordExponent ι (p :: L) = wordExponent ι S :=
    (wordExponent_erase ι S p hpS).symm
  have hrec := coeff_sourceQuadratic_pow_succ W ι k p L hp hnodup
  rw [hex, coeff_sourceQuadratic_pow W ι (k + 1) S hlenS hS] at hrec
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
      (List.Pairwise.erase q (List.Pairwise.erase p hS))]
    rw [pmSumList, hlq]
    ring
  rw [hterm] at hrec
  have hfac : ((k + 1).factorial : R) = (k + 1 : R) * (k.factorial : R) := by
    rw [Nat.factorial_succ, Nat.cast_mul, Nat.cast_add, Nat.cast_one]
  have hf : ((k + 1).factorial : R) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero _)
  apply mul_left_cancel₀ hf
  rw [pmSumList, hlenS]
  calc
    _ = (k + 1 : R) * ((k.factorial : R) *
      (L.map fun q => edgeMatrix W (p, ι p) (q, ι q) * pmSumList W ι (L.erase q)).sum) := hrec
    _ = _ := by rw [hfac]; ring

/-- Two row insertions expand into an ordered double sum. No factor one-half
appears: the rows are independently assigned their retained sites. -/
theorem coeff_two_rows_dividedPower (W : WeightsN N D R) (ι : V N → Fin D)
    (z t : SiteVariable N D) (k : ℕ) (L : List (V N))
    (hlen : L.length = 2 * (k + 1)) (hL : L.Pairwise (· < ·)) :
    MvPolynomial.coeff (wordExponent ι L)
      (rowPolynomial (edgeMatrix W) z * rowPolynomial (edgeMatrix W) t *
        dividedSourcePower W k) =
      (L.map fun r => edgeMatrix W z (r, ι r) *
        ((L.erase r).map fun s => edgeMatrix W t (s, ι s) *
          pmSumList W ι ((L.erase r).erase s)).sum).sum := by
  have hn : L.Nodup := hL.imp (fun h => ne_of_lt h)
  rw [mul_assoc, coeff_rowPolynomial_mul _ _ _ _ hn]
  congr 1
  apply List.map_congr_left
  intro r hr
  rw [coeff_rowPolynomial_mul _ _ _ _ (hn.erase r)]
  congr 1
  congr 1
  apply List.map_congr_left
  intro s hs
  have hlen' : ((L.erase r).erase s).length = 2 * k := by
    rw [List.length_erase_of_mem hs, List.length_erase_of_mem hr, hlen]
    omega
  rw [coeff_dividedSourcePower_list W ι k _ hlen' ((hL.erase r).erase s)]

def retainedVertices (p q : V N) : List (V N) := ((vertices N).erase p).erase q

theorem mem_retainedVertices (p q r : V N) :
    r ∈ retainedVertices p q ↔ r ≠ p ∧ r ≠ q := by
  constructor
  · intro hr
    constructor
    · intro h
      subst r
      exact (vertices_nodup N).not_mem_erase (List.mem_of_mem_erase hr)
    · intro h
      subst r
      exact ((vertices_nodup N).erase p).not_mem_erase hr
  · rintro ⟨hrp, hrq⟩
    exact (List.mem_erase_of_ne hrq).mpr
      ((List.mem_erase_of_ne hrp).mpr (mem_vertices r))

theorem retainedVertices_length (p q : V N) (hpq : p ≠ q) :
    (retainedVertices p q).length = N - 2 := by
  rw [retainedVertices, List.length_erase_of_mem
    ((List.mem_erase_of_ne hpq.symm).mpr (mem_vertices q)),
    List.length_erase_of_mem (mem_vertices p), vertices_eq_finRange]
  simp
  omega

theorem retainedVertices_nodup (p q : V N) : (retainedVertices p q).Nodup :=
  ((vertices_nodup N).erase p).erase q

theorem retainedVertices_sorted (p q : V N) : (retainedVertices p q).Pairwise (· < ·) :=
  ((vertices_pairwise_lt N).erase p).erase q

/-- Expand a pure cofactor at a root which is still retained in that cofactor. -/
theorem pureCofactor_retained_rootExpansion (k : ℕ) (W : WeightsN (2 * (k + 2)) D R)
    (h : Fin D) (p q r : V (2 * (k + 2)))
    (hpq : p ≠ q) (hrp : r ≠ p) (hrq : r ≠ q) :
    pureCofactor W h r q =
      (((retainedVertices p q).erase r).map fun s => edgeMatrix W (p, h) (s, h) *
        pmSumList W (fun _ => h) (((retainedVertices p q).erase r).erase s)).sum := by
  rw [pureCofactor, if_neg hrq]
  change pmSumList W (fun _ => h) (retainedVertices r q) = _
  have hlen : (retainedVertices r q).length = 2 * (k + 1) := by
    rw [retainedVertices_length r q hrq]
    omega
  have hp : p ∈ retainedVertices r q := (mem_retainedVertices r q p).mpr ⟨hrp.symm, hpq⟩
  rw [pmSumList_rootExpansion W (fun _ => h) k (retainedVertices r q) hlen
    (retainedVertices_sorted r q) p hp]
  have heq : (retainedVertices r q).erase p = (retainedVertices p q).erase r := by
    unfold retainedVertices
    rw [List.erase_comm q p, List.erase_comm r p, List.erase_comm r q]
  rw [heq]

/-- The off-diagonal cofactor matrix product is exactly the retained pure
two-row coefficient, with the normalization and ordered double sum proved. -/
theorem cofactorSum_eq_two_row_coefficient (k : ℕ) (W : WeightsN (2 * (k + 2)) D R)
    (i h : Fin D) (p q : V (2 * (k + 2))) (hpq : p ≠ q) :
    (∑ r, edgeMatrix W (p, i) (r, h) * pureCofactor W h r q) =
      MvPolynomial.coeff (wordExponent (fun _ => h) (retainedVertices p q))
        (rowPolynomial (edgeMatrix W) (p, i) * rowPolynomial (edgeMatrix W) (p, h) *
          dividedSourcePower W k) := by
  classical
  have hlen : (retainedVertices p q).length = 2 * (k + 1) := by
    rw [retainedVertices_length p q hpq]
    omega
  rw [coeff_two_rows_dividedPower W (fun _ => h) (p, i) (p, h) k
    (retainedVertices p q) hlen (retainedVertices_sorted p q)]
  have hrestrict :
      (∑ r, edgeMatrix W (p, i) (r, h) * pureCofactor W h r q) =
      ((retainedVertices p q).map fun r =>
        edgeMatrix W (p, i) (r, h) * pureCofactor W h r q).sum := by
    rw [← List.sum_toFinset _ (retainedVertices_nodup p q)]
    symm
    apply Finset.sum_subset (Finset.subset_univ _)
    intro r _ hr
    by_cases hrp : r = p
    · subst r
      rw [edgeMatrix_same_site, zero_mul]
    by_cases hrq : r = q
    · subst r
      rw [pureCofactor_self, mul_zero]
    exact False.elim (hr (List.mem_toFinset.mpr ((mem_retainedVertices p q r).mpr ⟨hrp, hrq⟩)))
  rw [hrestrict]
  congr 1
  apply List.map_congr_left
  intro r hr
  obtain ⟨hrp, hrq⟩ := (mem_retainedVertices p q r).mp hr
  rw [pureCofactor_retained_rootExpansion k W h p q r hpq hrp hrq]

omit [CharZero R] in
/-- Matching amplitudes only depend on the colours of the retained vertices. -/
theorem pmSumListAux_congr_word (W : WeightsN N D R) (ι κ : V N → Fin D) :
    ∀ n L, (∀ v ∈ L, ι v = κ v) → pmSumListAux W ι n L = pmSumListAux W κ n L
  | 0, _, _ => rfl
  | 1, _, _ => rfl
  | _ + 2, [], _ => rfl
  | _ + 2, [_], _ => rfl
  | n + 2, v :: u :: L, h => by
    simp only [pmSumListAux]
    congr 1
    apply List.map_congr_left
    intro r hr
    rw [h v (by simp), h r (List.mem_cons.mpr (Or.inr hr))]
    rw [pmSumListAux_congr_word W ι κ n ((u :: L).erase r)
      (fun x hx => h x (List.mem_cons.mpr (Or.inr (List.mem_of_mem_erase hx))))]

def oneDefectWord (p : V N) (i h : Fin D) : V N → Fin D :=
  fun v => if v = p then i else h

theorem allEqual_oneDefect_iff (hN : 2 ≤ N) (p : V N) (i h : Fin D) :
    allEqual (oneDefectWord p i h) ↔ i = h := by
  have : Nontrivial (Fin N) := by
    refine ⟨⟨⟨0, by omega⟩, ⟨1, by omega⟩, ?_⟩⟩
    intro heq
    have := congrArg Fin.val heq
    simp at this
  obtain ⟨q, hqp⟩ := exists_ne p
  rw [allEqual_iff_constant_at _ p]
  constructor
  · intro hw
    have hq := congrFun hw q
    simpa [oneDefectWord, hqp] using hq.symm
  · intro hi
    subst i
    funext v
    simp [oneDefectWord]

/-- Original one-defect amplitudes give the diagonal entries of every
endpoint-colour/cofactor matrix product. -/
theorem cofactorSum_same_root (k : ℕ) (W : WeightsN (2 * (k + 2)) D R)
    (hW : EqSystemN (2 * (k + 2)) D W)
    (p : V (2 * (k + 2))) (i h : Fin D) :
    (∑ r, edgeMatrix W (p, i) (r, h) * pureCofactor W h r p) =
      if i = h then 1 else 0 := by
  classical
  let word := oneDefectWord p i h
  have hEq := hW word
  rw [pmSumN_rootExpansion (k + 1) W word p] at hEq
  have heq :
      (((vertices (2 * (k + 2))).erase p).map fun r =>
        edgeMatrix W (p, word p) (r, word r) *
          pmSumList W word (((vertices (2 * (k + 2))).erase p).erase r)).sum =
      ∑ r, edgeMatrix W (p, i) (r, h) * pureCofactor W h r p := by
    let L := (vertices (2 * (k + 2))).erase p
    have hn : L.Nodup := (vertices_nodup _).erase p
    rw [← List.sum_toFinset _ hn]
    calc
      _ = ∑ r ∈ L.toFinset, edgeMatrix W (p, i) (r, h) * pureCofactor W h r p := by
        apply Finset.sum_congr rfl
        intro r hr
        have hrp : r ≠ p := by
          intro hrp
          subst r
          exact (vertices_nodup _).not_mem_erase (List.mem_toFinset.mp hr)
        simp only [word, oneDefectWord, if_neg hrp]
        rw [pureCofactor_symm W h r p, pureCofactor, if_neg hrp.symm]
        congr 1
        apply pmSumListAux_congr_word
        intro v hv
        have hvp : v ≠ p := by
          intro hvp
          subst v
          exact (vertices_nodup _).not_mem_erase (List.mem_of_mem_erase hv)
        simp [oneDefectWord, hvp]
      _ = _ := by
        apply Finset.sum_subset (Finset.subset_univ _)
        intro r _ hr
        have hrp : r = p := by
          by_contra h
          exact hr (List.mem_toFinset.mpr ((List.mem_erase_of_ne h).mpr (mem_vertices r)))
        subst r
        rw [edgeMatrix_same_site, zero_mul]
  rw [heq] at hEq
  simpa only [word, allEqual_oneDefect_iff (N := 2 * (k + 2)) (by omega)] using hEq

/-- The original equation system supplies every diagonal cofactor entry;
vanishing of the actual retained two-row coefficients supplies every
off-diagonal entry. Finite matrix cancellation then diagonalises the source. -/
theorem source_diagonal_of_two_row_vanishing (k : ℕ)
    (W : WeightsN (2 * (k + 2)) D R) (hW : EqSystemN (2 * (k + 2)) D W)
    (hvanish : ∀ p q, p ≠ q → ∀ i h,
      MvPolynomial.coeff (wordExponent (fun _ => h) (retainedVertices p q))
        (rowPolynomial (edgeMatrix W) (p, i) * rowPolynomial (edgeMatrix W) (p, h) *
          dividedSourcePower W k) = 0) :
    ∀ p q i h, i ≠ h → edgeMatrix W (p, i) (q, h) = 0 := by
  apply CofactorDiagonal.source_diagonal_of_cofactor_sums W (pureCofactor W)
  · intro h p q
    by_cases hpq : p = q
    · subst q
      simpa only [if_pos rfl] using cofactorSum_same_root k W hW p h h
    · rw [if_neg hpq, cofactorSum_eq_two_row_coefficient k W h h p q hpq]
      exact hvanish p q hpq h h
  · intro i h hih p q
    by_cases hpq : p = q
    · subst q
      simpa only [if_neg hih] using cofactorSum_same_root k W hW p i h
    · rw [cofactorSum_eq_two_row_coefficient k W i h p q hpq]
      exact hvanish p q hpq i h

/-- The two literal original root rows, with the omitted site deleted, paired
with the divided power of the quadratic retaining neither root. -/
noncomputable def omittedTwoRowPolynomial (W : WeightsN N D R)
    (p q : V N) (i h : Fin D) (k : ℕ) : MatchingPolynomial N D R :=
  eraseSite q (rowPolynomial (edgeMatrix W) (p, i)) *
    eraseSite q (rowPolynomial (edgeMatrix W) (p, h)) *
      (MvPolynomial.C ((k.factorial : R)⁻¹) *
        eraseSite q (deletedQuadratic W p) ^ k)

theorem cofactorSum_eq_omitted_two_row_coefficient (k : ℕ)
    (W : WeightsN (2 * (k + 2)) D R) (i h : Fin D)
    (p q : V (2 * (k + 2))) (hpq : p ≠ q) :
    (∑ r, edgeMatrix W (p, i) (r, h) * pureCofactor W h r q) =
      MvPolynomial.coeff (wordExponent (fun _ => h) (retainedVertices p q))
        (omittedTwoRowPolynomial W p q i h k) := by
  have hp : p ∉ retainedVertices p q := by simp [mem_retainedVertices]
  have hq : q ∉ retainedVertices p q := by simp [mem_retainedVertices]
  rw [cofactorSum_eq_two_row_coefficient k W i h p q hpq]
  rw [← coeff_word_eraseSite p _ (fun _ => h) _ hp,
    ← coeff_word_eraseSite q _ (fun _ => h) _ hq]
  congr 1
  simp only [dividedSourcePower, map_mul, map_pow, eraseSite_C,
    eraseSite_rowPolynomial, omittedTwoRowPolynomial, deletedQuadratic]

/-- The exact physical even-omission coefficient is the sole missing premise
of global diagonalisation at this stage. -/
theorem source_diagonal_of_omission_vanishing (k : ℕ)
    (W : WeightsN (2 * (k + 2)) D R) (hW : EqSystemN (2 * (k + 2)) D W)
    (hvanish : ∀ p q, p ≠ q → ∀ i h,
      MvPolynomial.coeff (wordExponent (fun _ => h) (retainedVertices p q))
        (omittedTwoRowPolynomial W p q i h k) = 0) :
    ∀ p q i h, i ≠ h → edgeMatrix W (p, i) (q, h) = 0 := by
  apply source_diagonal_of_two_row_vanishing k W hW
  intro p q hpq i h
  rw [← cofactorSum_eq_two_row_coefficient k W i h p q hpq,
    cofactorSum_eq_omitted_two_row_coefficient k W i h p q hpq]
  exact hvanish p q hpq i h

end KrennAllOrders.CofactorResponse
