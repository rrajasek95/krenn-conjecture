/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import WickPhysicalBridge

/-!
# Original-source reflection identities

All retained tensors below are coefficients of the actual original source.
The determinant reflection is applied to its literal physical covariance;
no higher-response or covariance equation is introduced as a premise.
-/

namespace KrennAllOrders.PhysicalReflection

open scoped BigOperators Classical
open MatchingModel SiteAlgebra RootResponse OddResponseVanishing
open WickCovariance WickCoefficientBridge WickPhysicalBridge ReflectionTensorBridge

section Reindex

variable {K E ι κ : Type*} [Field K] [CharZero K]
  [AddCommGroup E] [Module K E] [Fintype ι] [Fintype κ]

noncomputable def reindexWord (e : ι ≃ κ) : (ι → Bool) ≃ (κ → Bool) :=
  Equiv.arrowCongr e (Equiv.refl Bool)

omit [CharZero K] in
theorem sign_reindexWord (e : ι ≃ κ) (w : ι → Bool) :
    BinaryPairing.sign (R := K) (reindexWord e w) = BinaryPairing.sign w := by
  exact Equiv.prod_comp e.symm (fun i => if w i then (-1 : K) else 1)

omit [CharZero K] in
theorem pairing_reindex (e : ι ≃ κ) (P Q : BinaryPairing.Tensor κ K) :
    BinaryPairing.pairing (fun w => P (reindexWord e w))
      (fun w => Q (reindexWord e w)) = BinaryPairing.pairing P Q := by
  classical
  rw [BinaryPairing.pairing, BinaryPairing.pairing]
  apply Fintype.sum_equiv (reindexWord e)
  intro w
  rw [sign_reindexWord]
  rfl

noncomputable def indexedMomentTensor {η : Type*} [Fintype η]
    (B : E →ₗ[K] E →ₗ[K] K) (u v : ι → E) (z : η → E) :
    BinaryPairing.Tensor ι K :=
  fun w => centeredMoment B (Sum.elim (fun i => if w i then v i else u i) z)

omit [CharZero K] in
theorem indexedMomentTensor_reindex {η : Type*} [Fintype η]
    (B : E →ₗ[K] E →ₗ[K] K) (e : ι ≃ κ) (u v : κ → E)
    (z : η → E) (w : ι → Bool) :
    indexedMomentTensor B (u ∘ e) (v ∘ e) z w =
      indexedMomentTensor B u v z (reindexWord e w) := by
  classical
  rw [indexedMomentTensor, indexedMomentTensor]
  convert! centeredMoment_relabel B
    (Equiv.sumCongr e (Equiv.refl η))
    (Sum.elim (fun i => if reindexWord e w i then v i else u i) z) using 1
  congr 1
  funext i
  cases i <;> simp [reindexWord, Function.comp_def]

theorem pairing_indexedMoment_roots_eq_zero (B : E →ₗ[K] E →ₗ[K] K)
    (u v : ι → E) (g : E) (p : ℕ) (hι : Odd (Fintype.card ι)) :
    BinaryPairing.pairing
      (indexedMomentTensor B u v (fun _ : Fin p => g))
      (indexedMomentTensor B u v (fun _ : Fin 1 => g)) = 0 := by
  classical
  let e := Fintype.equivFin ι
  let u' := u ∘ e.symm
  let v' := v ∘ e.symm
  have hreindex {η : Type} [Fintype η] (z : η → E) :
      indexedMomentTensor B u v z =
        fun w => momentTensor B (Fintype.card ι) u' v' z (reindexWord e w) := by
    funext w
    convert! indexedMomentTensor_reindex B e u' v' z w using 1
    simp [u', v', Function.comp_def]
  rw [hreindex (fun _ : Fin p => g), hreindex (fun _ : Fin 1 => g), pairing_reindex e]
  have hunit : momentTensor B (Fintype.card ι) u' v' (fun _ : Fin 1 => g) =
      momentTensor B (Fintype.card ι) u' v' (fun _ : Unit => g) := by
    funext w
    let t : Fin 1 ≃ Unit := Fintype.equivOfCardEq (by simp)
    unfold momentTensor
    convert! centeredMoment_relabel B (Equiv.sumCongr (Equiv.refl _) t)
      (Sum.elim (fun i => if w i then v' i else u' i) (fun _ : Unit => g)) using 1
    congr 1
    funext i
    cases i <;> rfl
  rw [hunit]
  exact pairing_momentTensor_roots_eq_zero B _ p hι u' v' g

end Reindex

section PhysicalTensors

variable {K : Type*} {N D : ℕ} [Field K] [CharZero K]

/-- A binary receiving choice on the actual selected physical sites. Values
outside the selected set are irrelevant to every extracted coefficient. -/
noncomputable def receivingWord (S : Finset (V N))
    (ι ρ : V N → Fin D) (w : ↥S → Bool) : V N → Fin D :=
  fun q => if hq : q ∈ S then if w ⟨q, hq⟩ then ρ q else ι q else ι q

theorem receivingWord_at (S : Finset (V N)) (ι ρ : V N → Fin D)
    (w : ↥S → Bool) (q : ↥S) :
    receivingWord S ι ρ w q = if w q then ρ q else ι q := by
  simp [receivingWord, q.2]

/-- The literal higher receiving response, as a finite binary tensor. -/
noncomputable def originalResponseTensor (k : ℕ)
    (W : WeightsN (2 * (k + 1)) D K) (p : V (2 * (k + 1))) (r : ℕ)
    (ι ρ : V (2 * (k + 1)) → Fin D) (a : Fin D → K) :
    BinaryPairing.Tensor (↥(retainedSites p)) K :=
  fun w => MvPolynomial.eval a
    (oddResponsePolynomial W p k r (receivingWord (retainedSites p) ι ρ w))

theorem originalResponseTensor_eq_moments (k r : ℕ) (hr : r ≤ k)
    (W : WeightsN (2 * (k + 1)) D K) (p : V (2 * (k + 1)))
    (ι ρ : V (2 * (k + 1)) → Fin D) (a : Fin D → K) :
    originalResponseTensor k W p r ι ρ a =
      indexedMomentTensor (physicalCovariance W)
        (fun q : ↥(retainedSites p) => physicalBasis (q.1, ι q.1))
        (fun q : ↥(retainedSites p) => physicalBasis (q.1, ρ q.1))
        (fun _ : Fin (2 * r + 1) => physicalRoot p a) := by
  classical
  funext w
  rw [originalResponseTensor, ← centeredMoment_eq_eval_oddResponsePolynomial k r hr]
  unfold indexedMomentTensor
  congr 1
  funext z
  cases z with
  | inl q =>
    simp only [Sum.elim_inl, selectedInput, receivingWord_at]
    cases w q <;> rfl
  | inr q => rfl

/-- The determinant reflection now applies to actual original response tensors,
with every retained receiving word and terminal response included. -/
theorem originalResponseTensor_reflection (k r : ℕ) (hr : r ≤ k)
    (W : WeightsN (2 * (k + 1)) D K) (p : V (2 * (k + 1)))
    (ι ρ : V (2 * (k + 1)) → Fin D) (a : Fin D → K) :
    BinaryPairing.pairing (originalResponseTensor k W p r ι ρ a)
      (originalResponseTensor k W p 0 ι ρ a) = 0 := by
  rw [originalResponseTensor_eq_moments k r hr,
    originalResponseTensor_eq_moments k 0 (Nat.zero_le k)]
  exact pairing_indexedMoment_roots_eq_zero _ _ _ _ _
    (by simpa only [Fintype.card_coe, retainedSites_card] using
      (show Odd (2 * (k + 1) - 1) from ⟨k, by omega⟩))

omit [CharZero K] in
theorem wordExponent_eq_constant_iff (ι : V N → Fin D) (L : List (V N))
    (hL : L.Nodup) (h : Fin D) :
    wordExponent ι L = wordExponent (fun _ => h) L ↔ ∀ q ∈ L, ι q = h := by
  constructor
  · intro heq q hq
    by_contra hne
    have hone : wordExponent ι L (q, ι q) = 1 := by
      rw [wordExponent_selected, hL.count, if_pos hq]
    rw [heq, wordExponent_wrong_color (fun _ => h) L q (ι q) hne] at hone
    exact Nat.one_ne_zero hone.symm
  · intro hagree
    induction L with
    | nil => rfl
    | cons q L ih =>
      rw [wordExponent, wordExponent, hagree q (by simp)]
      congr 1
      exact ih hL.of_cons (fun t ht => hagree t (by simp [ht]))

omit [CharZero K] in
theorem retainedCoefficient_pureRootWord_word (p : V N) (ι : V N → Fin D)
    (h : Fin D) :
    retainedCoefficient (K := K) p ι (project (pureRootWord p h)) =
      if ∀ q ∈ (vertices N).erase p, ι q = h then 1 else 0 := by
  classical
  rw [pureRootWord, retainedCoefficient_project, MvPolynomial.coeff_monomial]
  have heq : wordExponent (fun _ => h) ((vertices N).erase p) =
      wordExponent ι ((vertices N).erase p) ↔
        ∀ q ∈ (vertices N).erase p, ι q = h :=
    eq_comm.trans (wordExponent_eq_constant_iff ι _ ((vertices_nodup N).erase p) h)
  simp only [heq]

/-- The original source equations identify the complete linear response on
every receiving word, rather than only its pure coefficients. -/
theorem original_linear_response (k : ℕ) (W : WeightsN (2 * (k + 1)) D K)
    (hW : EqSystemN (2 * (k + 1)) D W) (p : V (2 * (k + 1)))
    (a : Fin D → K) (ι : V (2 * (k + 1)) → Fin D) :
    MvPolynomial.eval a (oddResponsePolynomial W p k 0 ι) =
      ∑ h, a h * if ∀ q ∈ (vertices (2 * (k + 1))).erase p, ι q = h then 1 else 0 := by
  rw [eval_oddResponsePolynomial, oddResponse_zero k W hW p a]
  change (retainedCoefficientHom p ι) _ = _
  rw [map_sum]
  change (∑ h, retainedCoefficient p ι (siteScalar (a h) * project (pureRootWord p h))) = _
  simp only [retainedCoefficient_scalar_mul, retainedCoefficient_pureRootWord_word]

omit [CharZero K] in
theorem wordExponent_congr_list (ι ρ : V N → Fin D) (L : List (V N))
    (h : ∀ q ∈ L, ι q = ρ q) : wordExponent ι L = wordExponent ρ L := by
  induction L with
  | nil => rfl
  | cons q L ih =>
    rw [wordExponent, wordExponent, h q (by simp)]
    congr 1
    exact ih (fun t ht => h t (by simp [ht]))

omit [CharZero K] in
/-- The receiving colour at the removed root is completely irrelevant. -/
theorem oddResponsePolynomial_congr_word (W : WeightsN N D K) (p : V N)
    (k r : ℕ) (ι ρ : V N → Fin D)
    (h : ∀ q ∈ (vertices N).erase p, ι q = ρ q) :
    oddResponsePolynomial W p k r ι = oddResponsePolynomial W p k r ρ := by
  apply MvPolynomial.ext
  intro m
  simp only [oddResponsePolynomial, coeff_coefficientPolynomial, retainedCoefficient]
  rw [wordExponent_congr_list ι ρ _ h]

theorem original_linear_response_of_constant (k : ℕ)
    (W : WeightsN (2 * (k + 1)) D K) (hW : EqSystemN (2 * (k + 1)) D W)
    (p : V (2 * (k + 1))) (a : Fin D → K) (ι : V (2 * (k + 1)) → Fin D)
    (i : Fin D) (hι : ∀ q ∈ (vertices (2 * (k + 1))).erase p, ι q = i) :
    MvPolynomial.eval a (oddResponsePolynomial W p k 0 ι) = a i := by
  rw [oddResponsePolynomial_congr_word W p k 0 ι (fun _ => i) hι,
    oddResponsePolynomial_zero_pure k W hW p i, MvPolynomial.eval_X]

theorem retainedSites_nonempty (k : ℕ) (p : V (2 * (k + 1))) :
    Nonempty (↥(retainedSites p)) := by
  apply Fintype.card_pos_iff.mp
  rw [Fintype.card_coe, retainedSites_card]
  omega

theorem originalResponseTensor_linear_pair (k : ℕ)
    (W : WeightsN (2 * (k + 1)) D K) (hW : EqSystemN (2 * (k + 1)) D W)
    (p : V (2 * (k + 1))) (a : Fin D → K) (i j : Fin D) (hij : i ≠ j) :
    originalResponseTensor k W p 0 (fun _ => i) (fun _ => j) a =
      a i • BinaryPairing.pure false + a j • BinaryPairing.pure true := by
  classical
  have : Nonempty (↥(retainedSites p)) := retainedSites_nonempty k p
  funext w
  by_cases hwf : w = fun _ => false
  · subst w
    rw [originalResponseTensor, original_linear_response_of_constant k W hW p a _ i]
    · simp [BinaryPairing.pure, funext_iff]
    · intro q hq
      have hqS : q ∈ retainedSites p := List.mem_toFinset.mpr hq
      simp [receivingWord, hqS]
  · by_cases hwt : w = fun _ => true
    · subst w
      rw [originalResponseTensor, original_linear_response_of_constant k W hW p a _ j]
      · simp [BinaryPairing.pure, funext_iff]
      · intro q hq
        have hqS : q ∈ retainedSites p := List.mem_toFinset.mpr hq
        simp [receivingWord, hqS]
    · have htrue : ∃ q, w q = true := by
        by_contra h
        apply hwf
        funext q
        have hq : w q ≠ true := fun ht => h ⟨q, ht⟩
        cases hw : w q <;> simp_all
      have hfalse : ∃ q, w q = false := by
        by_contra h
        apply hwt
        funext q
        have hq : w q ≠ false := fun ht => h ⟨q, ht⟩
        cases hw : w q <;> simp_all
      obtain ⟨q, hq⟩ := htrue
      obtain ⟨t, ht⟩ := hfalse
      rw [originalResponseTensor, original_linear_response k W hW p a]
      have hzero : ∀ h : Fin D, ¬∀ z ∈ (vertices (2 * (k + 1))).erase p,
          receivingWord (retainedSites p) (fun _ => i) (fun _ => j) w z = h := by
        intro h hc
        have hq' := hc q.1 (List.mem_toFinset.mp q.2)
        have ht' := hc t.1 (List.mem_toFinset.mp t.2)
        have hj : j = h := by simpa [receivingWord, q.2, hq] using hq'
        have hi : i = h := by simpa [receivingWord, t.2, ht] using ht'
        exact hij (hi.trans hj.symm)
      simp only [hzero, if_false, mul_zero, Finset.sum_const_zero,
        Pi.add_apply, Pi.smul_apply, smul_eq_mul, BinaryPairing.pure,
        if_neg hwf, if_neg hwt, mul_zero, add_zero]

omit [CharZero K] in
theorem originalResponseTensor_false (k r : ℕ)
    (W : WeightsN (2 * (k + 1)) D K) (p : V (2 * (k + 1)))
    (ι ρ : V (2 * (k + 1)) → Fin D) (a : Fin D → K) :
    originalResponseTensor k W p r ι ρ a (fun _ => false) =
      MvPolynomial.eval a (oddResponsePolynomial W p k r ι) := by
  rw [originalResponseTensor]
  congr 1
  apply oddResponsePolynomial_congr_word
  intro q hq
  have hqS : q ∈ retainedSites p := List.mem_toFinset.mpr hq
  simp [receivingWord, hqS]

omit [CharZero K] in
theorem originalResponseTensor_true (k r : ℕ)
    (W : WeightsN (2 * (k + 1)) D K) (p : V (2 * (k + 1)))
    (ι ρ : V (2 * (k + 1)) → Fin D) (a : Fin D → K) :
    originalResponseTensor k W p r ι ρ a (fun _ => true) =
      MvPolynomial.eval a (oddResponsePolynomial W p k r ρ) := by
  rw [originalResponseTensor]
  congr 1
  apply oddResponsePolynomial_congr_word
  intro q hq
  have hqS : q ∈ retainedSites p := List.mem_toFinset.mpr hq
  simp [receivingWord, hqS]

/-- Pure cross-identities follow from the actual determinant reflection and
the original source's linear response, without assuming any higher identity. -/
theorem pure_response_cross (k r : ℕ) (hr : r ≤ k)
    (W : WeightsN (2 * (k + 1)) D K) (hW : EqSystemN (2 * (k + 1)) D W)
    (p : V (2 * (k + 1))) (i j : Fin D) :
    MvPolynomial.X i * oddResponsePolynomial W p k r (fun _ => j) =
      MvPolynomial.X j * oddResponsePolynomial W p k r (fun _ => i) := by
  by_cases hij : i = j
  · subst j
    rfl
  apply MvPolynomial.funext
  intro a
  have href := originalResponseTensor_reflection k r hr W p (fun _ => i) (fun _ => j) a
  rw [originalResponseTensor_linear_pair k W hW p a i j hij,
    BinaryPairing.pairing_add_right, BinaryPairing.pairing_smul_right,
    BinaryPairing.pairing_smul_right, BinaryPairing.pairing_right_pure_false,
    BinaryPairing.pairing_right_pure_true, originalResponseTensor_true,
    originalResponseTensor_false] at href
  have ho : Odd (Fintype.card (↥(retainedSites p))) := by
    rw [Fintype.card_coe, retainedSites_card]
    exact ⟨k, by omega⟩
  rw [ho.neg_one_pow] at href
  simp only [map_mul, MvPolynomial.eval_X]
  linear_combination -href

theorem originalResponseTensor_linear_mixed (k : ℕ)
    (W : WeightsN (2 * (k + 1)) D K) (hW : EqSystemN (2 * (k + 1)) D W)
    (p : V (2 * (k + 1))) (a : Fin D → K) (ι : V (2 * (k + 1)) → Fin D)
    (h : Fin D)
    (hnon : ¬∃ c, ∀ q ∈ (vertices (2 * (k + 1))).erase p, ι q = c)
    (havoid : ∀ q ∈ (vertices (2 * (k + 1))).erase p, ι q ≠ h) :
    originalResponseTensor k W p 0 ι (fun _ => h) a =
      a h • BinaryPairing.pure true := by
  classical
  funext w
  by_cases hwt : w = fun _ => true
  · subst w
    rw [originalResponseTensor_true, oddResponsePolynomial_zero_pure k W hW p h,
      MvPolynomial.eval_X]
    simp [BinaryPairing.pure]
  · have hfalse : ∃ q, w q = false := by
      by_contra hn
      apply hwt
      funext q
      have hq : w q ≠ false := fun ht => hn ⟨q, ht⟩
      cases hw : w q <;> simp_all
    obtain ⟨t, ht⟩ := hfalse
    rw [originalResponseTensor, original_linear_response k W hW p a]
    have hzero : ∀ c, ¬∀ q ∈ (vertices (2 * (k + 1))).erase p,
        receivingWord (retainedSites p) ι (fun _ => h) w q = c := by
      intro c hc
      have ht' : ι t.1 = c := by
        simpa [receivingWord, t.2, ht] using hc t.1 (List.mem_toFinset.mp t.2)
      have hch : c ≠ h := by
        rw [← ht']
        exact havoid t.1 (List.mem_toFinset.mp t.2)
      have hwf : ∀ q : ↥(retainedSites p), w q = false := by
        intro q
        by_cases hq : w q = true
        · have hh : h = c := by
            simpa [receivingWord, q.2, hq] using hc q.1 (List.mem_toFinset.mp q.2)
          exact False.elim (hch hh.symm)
        · cases heq : w q <;> simp_all
      apply hnon
      refine ⟨c, ?_⟩
      intro q hq
      have hqS : q ∈ retainedSites p := List.mem_toFinset.mpr hq
      simpa [receivingWord, hqS, hwf ⟨q, hqS⟩] using hc q hq
    simp only [hzero, if_false, mul_zero, Finset.sum_const_zero,
      Pi.smul_apply, smul_eq_mul, BinaryPairing.pure, if_neg hwt, mul_zero]

/-- A nonconstant original receiving word avoiding colour `h` has zero cross
product with `X h`. The hypotheses concern only retained sites. -/
theorem mixed_response_cross (k r : ℕ) (hr : r ≤ k)
    (W : WeightsN (2 * (k + 1)) D K) (hW : EqSystemN (2 * (k + 1)) D W)
    (p : V (2 * (k + 1))) (ι : V (2 * (k + 1)) → Fin D) (h : Fin D)
    (hnon : ¬∃ c, ∀ q ∈ (vertices (2 * (k + 1))).erase p, ι q = c)
    (havoid : ∀ q ∈ (vertices (2 * (k + 1))).erase p, ι q ≠ h) :
    MvPolynomial.X h * oddResponsePolynomial W p k r ι = 0 := by
  apply MvPolynomial.funext
  intro a
  have href := originalResponseTensor_reflection k r hr W p ι (fun _ => h) a
  rw [originalResponseTensor_linear_mixed k W hW p a ι h hnon havoid,
    BinaryPairing.pairing_smul_right, BinaryPairing.pairing_right_pure_true,
    originalResponseTensor_false] at href
  simpa only [map_mul, MvPolynomial.eval_X, map_zero] using href

end PhysicalTensors

end KrennAllOrders.PhysicalReflection
