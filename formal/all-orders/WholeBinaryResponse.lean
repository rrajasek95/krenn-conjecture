import OddRotation
import WickPhysicalBridge
import WickEvenResponse
import PhysicalReflection
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-!
# The whole original binary receiving odd-response tower

The actual source coefficients are assembled with literal shifted Wick moments.
This module retains the terminal odd degree. Its final source theorem will use
the physical reflection identities, rather than accepting them as hypotheses.
-/

namespace KrennAllOrders.WholeBinaryResponse

open scoped BigOperators Classical
open MatchingModel SiteAlgebra RootResponse OddResponseVanishing
open WickCovariance WickCoefficientBridge WickRootBridge WickPhysicalBridge WickShiftedBridge
open MvPolynomial

variable {K : Type*} [Field K] [CharZero K] {N D : ℕ}

/-- The root row family is a genuine linear map in its independent parameters. -/
noncomputable def rootVector (p : V N) : (Fin D → K) →ₗ[K] PhysicalSpace N D K where
  toFun := physicalRoot p
  map_add' a b := by
    simp only [physicalRoot, Pi.add_apply, add_smul, Finset.sum_add_distrib]
  map_smul' c a := by
    simp only [physicalRoot, Pi.smul_apply, smul_eq_mul, RingHom.id_apply,
      Finset.smul_sum, smul_smul]

/-- The actual mean functional, as a linear family over the original root rows. -/
noncomputable def rootMean (W : WeightsN N D K) (p : V N) :
    (Fin D → K) →ₗ[K] (PhysicalSpace N D K →ₗ[K] K) :=
  (physicalCovariance W).comp (rootVector p)

omit [CharZero K] in
@[simp] theorem rootMean_apply (W : WeightsN N D K) (p : V N) (a : Fin D → K) :
    rootMean W p a = physicalCovariance W (physicalRoot p a) := rfl

omit [CharZero K] in
/-- A receiving coefficient depends only on the word on retained sites. -/
theorem wordExponent_congr_list (L : List (V N)) (ι ν : V N → Fin D)
    (h : ∀ v ∈ L, ι v = ν v) : wordExponent ι L = wordExponent ν L := by
  induction L with
  | nil => rfl
  | cons v L ih =>
    simp only [wordExponent, h v (List.mem_cons_self ..)]
    rw [ih (fun w hw => h w (List.mem_cons_of_mem _ hw))]

/-- The root colour itself never enters a retained odd-response coefficient. -/
theorem oddResponsePolynomial_congr (W : WeightsN N D K) (p : V N)
    (m r : ℕ) (ι ν : V N → Fin D)
    (h : ∀ v ∈ retainedSites p, ι v = ν v) :
    oddResponsePolynomial W p m r ι = oddResponsePolynomial W p m r ν := by
  apply MvPolynomial.funext
  intro a
  simp only [eval_oddResponsePolynomial, retainedCoefficient]
  congr 1
  exact wordExponent_congr_list _ _ _ (fun v hv => h v (List.mem_toFinset.mpr hv))

/-- A fixed mean-degree slice is the normalized literal moment with the
corresponding number of isotropic auxiliary root slots. -/
theorem meanSlice_eq_isotropic_root_moment {E ι : Type*}
    [AddCommGroup E] [Module K E] [Fintype ι]
    (B : E →ₗ[K] E →ₗ[K] K) (v : ι → E) (g : E) (k d : ℕ)
    (hcard : Fintype.card ι = 2 * k + d)
    (hgg : B g g = 0) (hcross : ∀ i, B (v i) g = B g (v i)) :
    meanSlice B (B g) d v = ((d.factorial : K)⁻¹) *
      centeredMoment B (Sum.elim v (fun _ : Fin d => g)) := by
  classical
  rw [meanSlice_eq_coeff B (B g) v d k (by omega),
    centeredMoment_isotropic_roots B v g k d hcard (Fintype.card_fin _) hgg hcross]
  rw [← MvPolynomial.coeff_C_mul]
  unfold dividedQuadratic
  congr 1
  ring

/-- Literal shifted moments equal the factorial-normalized sum of every actual
raw odd root coefficient, including the terminal response. -/
theorem shiftedMoment_eq_oddResponse_sum (m : ℕ)
    (W : WeightsN (2 * (m + 1)) D K) (p : V (2 * (m + 1)))
    (a : Fin D → K) (ι : V (2 * (m + 1)) → Fin D) :
    shiftedMoment (physicalCovariance W) (rootMean W p a)
      (fun q : ↥(retainedSites p) => physicalBasis (selectedInput (retainedSites p) ι q)) =
      ∑ r ∈ Finset.range (m + 1), (((2 * r + 1).factorial : K)⁻¹) *
        eval a (oddResponsePolynomial W p m r ι) := by
  classical
  have hcard : Fintype.card ↥(retainedSites p) = 2 * m + 1 := by
    simp only [Fintype.card_coe, retainedSites_card]
    omega
  rw [shiftedMoment_eq_sum_meanSlice, hcard,
    show 2 * m + 1 + 1 = 2 * (m + 1) by omega, WickEvenResponse.sum_range_pairs]
  apply Finset.sum_congr rfl
  intro r hr
  have hrm : r ≤ m := by simpa using Finset.mem_range.mp hr
  rw [WickEvenResponse.meanSlice_even_eq_zero _ _ _ m r hcard hrm, zero_add,
    rootMean_apply]
  rw [meanSlice_eq_isotropic_root_moment _ _ _ (m - r) (2 * r + 1)
    (by omega) (physicalRoot_isotropic W p a)
    (fun i => by rw [physicalCovariance_basis_root, physicalCovariance_root_basis])]
  rw [centeredMoment_eq_eval_oddResponsePolynomial m r hrm]

/-- Extend a Boolean receiving word to the irrelevant omitted root. -/
noncomputable def binaryWord (p : V N) (i j : Fin D)
    (w : ↥(retainedSites p) → Bool) : V N → Fin D :=
  fun v => if hv : v ∈ retainedSites p then if w ⟨v, hv⟩ then j else i else i

@[simp] theorem binaryWord_retained (p : V N) (i j : Fin D)
    (w : ↥(retainedSites p) → Bool) (v : ↥(retainedSites p)) :
    binaryWord p i j w v = if w v then j else i := by
  simp [binaryWord, v.property]

/-- The concrete binary receiving tensor is the normalized finite raw tower. -/
theorem responseTensor_eq_oddResponse_sum (m : ℕ)
    (W : WeightsN (2 * (m + 1)) D K) (p : V (2 * (m + 1)))
    (a : Fin D → K) (i j : Fin D) (w : ↥(retainedSites p) → Bool) :
    WickFinitePairing.responseTensor (physicalCovariance W) (rootMean W p a)
      (fun v : ↥(retainedSites p) => physicalBasis (v.1, i))
      (fun v : ↥(retainedSites p) => physicalBasis (v.1, j)) w =
      ∑ r ∈ Finset.range (m + 1), (((2 * r + 1).factorial : K)⁻¹) *
        eval a (oddResponsePolynomial W p m r (binaryWord p i j w)) := by
  rw [← shiftedMoment_eq_oddResponse_sum m W p a (binaryWord p i j w)]
  unfold WickFinitePairing.responseTensor
  congr 1
  funext v
  simp only [selectedInput, binaryWord_retained]
  cases w v <;> rfl

/-- Constant Boolean words select the corresponding actual pure response;
the arbitrary omitted-root extension is removed by retained-word congruence. -/
theorem oddResponsePolynomial_binary_const (W : WeightsN N D K) (p : V N)
    (m r : ℕ) (i j : Fin D) (b : Bool) :
    oddResponsePolynomial W p m r (binaryWord p i j (fun _ => b)) =
      oddResponsePolynomial W p m r (fun _ => if b then j else i) := by
  apply oddResponsePolynomial_congr
  intro v hv
  simp only [binaryWord, dif_pos hv]

/-- Assembly of the actual finite binary receiving tensor from its pure
common factors and its mixed-word zeros. These are intermediate reflection
outputs, not assumptions of the final source theorem. -/
theorem actual_binary_factorization (m : ℕ)
    (W : WeightsN (2 * (m + 1)) D K) (p : V (2 * (m + 1)))
    (q : ℕ → MvPolynomial (Fin D) K) (i j : Fin D)
    (hpure : ∀ r ≤ m, ∀ h : Fin D,
      oddResponsePolynomial W p m r (fun _ => h) = X h * q r)
    (hmixed : ∀ r ≤ m, ∀ w : ↥(retainedSites p) → Bool,
      w ≠ (fun _ => false) → w ≠ (fun _ => true) →
      oddResponsePolynomial W p m r (binaryWord p i j w) = 0)
    (a : Fin D → K) :
    WickFinitePairing.responseTensor (physicalCovariance W) (rootMean W p a)
      (fun v : ↥(retainedSites p) => physicalBasis (v.1, i))
      (fun v : ↥(retainedSites p) => physicalBasis (v.1, j)) =
      eval a (finiteScalarFactor m q) •
        (a i • BinaryPairing.pure false + a j • BinaryPairing.pure true) := by
  classical
  let : Nonempty ↥(retainedSites p) := Fintype.card_pos_iff.mp (by
    simp only [Fintype.card_coe, retainedSites_card]
    omega)
  funext w
  rw [responseTensor_eq_oddResponse_sum]
  by_cases hw0 : w = (fun _ => false)
  · subst w
    simp only [oddResponsePolynomial_binary_const, Bool.false_eq_true, ↓reduceIte]
    have hsum : (∑ r ∈ Finset.range (m + 1), (((2 * r + 1).factorial : K)⁻¹) *
        eval a (oddResponsePolynomial W p m r (fun _ => i))) =
        eval a (finiteScalarFactor m q) * a i := by
      simp only [finiteScalarFactor, map_sum, map_mul, eval_C, Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro r hr
      rw [hpure r (by simpa using Finset.mem_range.mp hr), map_mul, eval_X]
      ring
    rw [hsum]
    simp [BinaryPairing.pure, _root_.funext_iff]
  · by_cases hw1 : w = (fun _ => true)
    · subst w
      simp only [oddResponsePolynomial_binary_const, ↓reduceIte]
      have hsum : (∑ r ∈ Finset.range (m + 1), (((2 * r + 1).factorial : K)⁻¹) *
          eval a (oddResponsePolynomial W p m r (fun _ => j))) =
          eval a (finiteScalarFactor m q) * a j := by
        simp only [finiteScalarFactor, map_sum, map_mul, eval_C, Finset.sum_mul]
        apply Finset.sum_congr rfl
        intro r hr
        rw [hpure r (by simpa using Finset.mem_range.mp hr), map_mul, eval_X]
        ring
      rw [hsum]
      simp [BinaryPairing.pure, _root_.funext_iff]
    · have hz : (∑ r ∈ Finset.range (m + 1), (((2 * r + 1).factorial : K)⁻¹) *
          eval a (oddResponsePolynomial W p m r (binaryWord p i j w))) = 0 := by
        apply Finset.sum_eq_zero
        intro r hr
        rw [hmixed r (by simpa using Finset.mem_range.mp hr) w hw0 hw1, map_zero, mul_zero]
      rw [hz]
      simp [BinaryPairing.pure, hw0, hw1]

/-- Any two receiving colours leave a third coordinate available in the
ternary source, even if the displayed receiving colours coincide. -/
theorem exists_third_colour (i j : Fin 3) : ∃ h : Fin 3, h ≠ i ∧ h ≠ j := by
  fin_cases i <;> fin_cases j <;> decide

/-- A genuinely mixed Boolean word is nonconstant on the actual retained sites. -/
theorem binaryWord_nonconstant (p : V N) {i j : Fin D} (hij : i ≠ j)
    (w : ↥(retainedSites p) → Bool)
    (hw0 : w ≠ (fun _ => false)) (hw1 : w ≠ (fun _ => true)) :
    ¬∃ c, ∀ q ∈ (vertices N).erase p, binaryWord p i j w q = c := by
  classical
  have hf : ∃ v, w v = false := by
    by_contra h
    push Not at h
    apply hw1
    funext v
    cases hv : w v <;> simp_all
  have ht : ∃ v, w v = true := by
    by_contra h
    push Not at h
    apply hw0
    funext v
    cases hv : w v <;> simp_all
  obtain ⟨v, hv⟩ := hf
  obtain ⟨t, ht⟩ := ht
  rintro ⟨c, hc⟩
  have hv' := hc v (List.mem_toFinset.mp v.property)
  have ht' := hc t (List.mem_toFinset.mp t.property)
  rw [binaryWord_retained, hv] at hv'
  rw [binaryWord_retained, ht] at ht'
  simp only [Bool.false_eq_true, ↓reduceIte] at hv' ht'
  exact hij (hv'.trans ht'.symm)

/-- Physical reflection kills every genuinely mixed binary word polynomial,
without any higher-response premise. -/
theorem binary_mixed_response_zero (m r : ℕ) (hr : r ≤ m)
    (W : WeightsN (2 * (m + 1)) 3 K) (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p : V (2 * (m + 1))) {i j : Fin 3} (hij : i ≠ j)
    (w : ↥(retainedSites p) → Bool)
    (hw0 : w ≠ (fun _ => false)) (hw1 : w ≠ (fun _ => true)) :
    oddResponsePolynomial W p m r (binaryWord p i j w) = 0 := by
  obtain ⟨h, hhi, hhj⟩ := exists_third_colour i j
  apply mixed_response_zero_of_reflection _ _ _ _ _ h
  apply PhysicalReflection.mixed_response_cross m r hr W hW p _ h
  · exact binaryWord_nonconstant p hij w hw0 hw1
  · intro v hv
    have hv' : v ∈ retainedSites p := List.mem_toFinset.mpr hv
    simp only [binaryWord, dif_pos hv']
    split_ifs <;> exact Ne.symm ‹h ≠ _›

/-- A complete common-factor family is obtained from the actual source
reflection identities at every retained odd degree. -/
theorem exists_actual_pure_factors (m : ℕ)
    (W : WeightsN (2 * (m + 1)) 3 K) (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p : V (2 * (m + 1))) :
    ∃ q : ℕ → MvPolynomial (Fin 3) K,
      (∀ r ≤ m, ∀ i : Fin 3,
        oddResponsePolynomial W p m r (fun _ => i) = X i * q r) ∧
      (∀ r ≤ m, IsWeightedHomogeneous (fun _ : Fin 3 => (1 : ℕ)) (q r) (2 * r)) ∧
      q 0 = 1 := by
  classical
  have hex (r : ℕ) : ∃ q : MvPolynomial (Fin 3) K,
      r ≤ m → ∀ i : Fin 3, oddResponsePolynomial W p m r (fun _ => i) = X i * q := by
    by_cases hr : r ≤ m
    · obtain ⟨q, hq⟩ := pure_response_common_factor W p m r
        (a := (0 : Fin 3)) (b := (1 : Fin 3)) (by decide)
        (PhysicalReflection.pure_response_cross m r hr W hW p)
      exact ⟨q, fun _ => hq⟩
    · exact ⟨0, fun h => False.elim (hr h)⟩
  choose q hq using hex
  refine ⟨q, hq, ?_, ?_⟩
  · intro r hr
    exact pure_response_factor_homogeneous W p m r (0 : Fin 3) (q r) (hq r hr 0)
  · exact pure_linear_factor_eq_one m W hW p (0 : Fin 3) (q 0) (hq 0 (by omega) 0)

/-- The actual complete binary receiving odd tower vanishes above its original
linear term. The auxiliary scalar is only a field-level choice of a normalized
rotation, not an extra identity of the source. -/
theorem pure_response_zero_of_rotation (m r : ℕ) (hr : r ≤ m) (hpos : 0 < r)
    (W : WeightsN (2 * (m + 1)) 3 K) (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p : V (2 * (m + 1))) (i : Fin 3) (s : K) (hs : s * s + s * s = 1) :
    oddResponsePolynomial W p m r (fun _ => i) = 0 := by
  classical
  obtain ⟨q, hpure, hhom, hzero⟩ := exists_actual_pure_factors m W hW p
  let : Nonempty ↥(retainedSites p) := Fintype.card_pos_iff.mp (by
    simp only [Fintype.card_coe, retainedSites_card]
    omega)
  have hodd : Odd (Fintype.card ↥(retainedSites p)) := by
    simp only [Fintype.card_coe, retainedSites_card]
    exact ⟨m, by omega⟩
  have hfactor := actual_binary_factorization m W p q (0 : Fin 3) (1 : Fin 3) hpure
    (fun t ht w hw0 hw1 => binary_mixed_response_zero m t ht W hW p (by decide) w hw0 hw1)
  have hqzero := OddRotation.higher_factors_zero_of_actual_rotation
    (physicalCovariance W) (rootMean W p)
    (fun v : ↥(retainedSites p) => physicalBasis (v.1, (0 : Fin 3)))
    (fun v : ↥(retainedSites p) => physicalBasis (v.1, (1 : Fin 3)))
    m q hhom hzero (by decide) hodd hfactor s hs r hr hpos
  rw [hpure r hr i, hqzero, mul_zero]

/-- Once the receiving word omits a colour and is not pure, its actual
polynomial response is already zero by the physical reflection theorem. -/
theorem mixed_response_zero (m r : ℕ) (hr : r ≤ m)
    (W : WeightsN (2 * (m + 1)) 3 K) (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p : V (2 * (m + 1))) (ι : V (2 * (m + 1)) → Fin 3)
    (hnon : ¬∃ c, ∀ q ∈ (vertices (2 * (m + 1))).erase p, ι q = c)
    (havoid : ∃ h : Fin 3, ∀ q ∈ (vertices (2 * (m + 1))).erase p, ι q ≠ h) :
    oddResponsePolynomial W p m r ι = 0 := by
  obtain ⟨h, hh⟩ := havoid
  exact mixed_response_zero_of_reflection W p m r ι h
    (PhysicalReflection.mixed_response_cross m r hr W hW p ι h hnon hh)

/-- Any receiving word using at most two colours on the retained sites has
zero higher response, including the highest possible odd response. -/
theorem whole_binary_response_zero_of_rotation (m r : ℕ) (hr : r ≤ m) (hpos : 0 < r)
    (W : WeightsN (2 * (m + 1)) 3 K) (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p : V (2 * (m + 1))) (ι : V (2 * (m + 1)) → Fin 3)
    (hbinary : ∃ i j : Fin 3, ∀ v ∈ retainedSites p, ι v = i ∨ ι v = j)
    (s : K) (hs : s * s + s * s = 1) : oddResponsePolynomial W p m r ι = 0 := by
  classical
  by_cases hpure : ∃ c, ∀ q ∈ (vertices (2 * (m + 1))).erase p, ι q = c
  · obtain ⟨c, hc⟩ := hpure
    rw [oddResponsePolynomial_congr W p m r ι (fun _ => c)
      (fun v hv => hc v (List.mem_toFinset.mp hv))]
    exact pure_response_zero_of_rotation m r hr hpos W hW p c s hs
  · apply mixed_response_zero m r hr W hW p ι hpure
    obtain ⟨i, j, hij⟩ := hbinary
    obtain ⟨h, hhi, hhj⟩ := exists_third_colour i j
    refine ⟨h, ?_⟩
    intro v hv
    rcases hij v (List.mem_toFinset.mpr hv) with hvi | hvj
    · rw [hvi]; exact hhi.symm
    · rw [hvj]; exact hhj.symm

/-- A concrete normalized rotation in the complex coefficient field. -/
noncomputable def halfRotation : ℂ := (Real.sqrt 2 : ℂ) / 2

theorem halfRotation_normalized : halfRotation * halfRotation + halfRotation * halfRotation = 1 := by
  have hs : (Real.sqrt 2 : ℂ) * (Real.sqrt 2 : ℂ) = 2 := by
    norm_cast
    nlinarith [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
  unfold halfRotation
  field_simp
  linear_combination 2 * hs

/-- The actual ternary source equation alone forces the complete higher odd
response to vanish on every receiving word with at most two colours. -/
theorem whole_binary_response_zero (m r : ℕ) (hr : r ≤ m) (hpos : 0 < r)
    (W : WeightsN (2 * (m + 1)) 3 ℂ) (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p : V (2 * (m + 1))) (ι : V (2 * (m + 1)) → Fin 3)
    (hbinary : ∃ i j : Fin 3, ∀ v ∈ retainedSites p, ι v = i ∨ ι v = j) :
    oddResponsePolynomial W p m r ι = 0 :=
  whole_binary_response_zero_of_rotation m r hr hpos W hW p ι hbinary
    halfRotation halfRotation_normalized

/-- Pure receiving words are included without a separate tower hypothesis. -/
theorem pure_response_zero (m r : ℕ) (hr : r ≤ m) (hpos : 0 < r)
    (W : WeightsN (2 * (m + 1)) 3 ℂ) (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p : V (2 * (m + 1))) (i : Fin 3) :
    oddResponsePolynomial W p m r (fun _ => i) = 0 :=
  whole_binary_response_zero m r hr hpos W hW p (fun _ => i)
    ⟨i, i, fun _ _ => Or.inl rfl⟩

/-- Concrete raw row/quadratic coefficient version of the whole binary tower,
for arbitrary numerical combinations of original departure rows. -/
theorem whole_binary_coefficient_zero (m r : ℕ) (hr : r ≤ m) (hpos : 0 < r)
    (W : WeightsN (2 * (m + 1)) 3 ℂ) (hW : EqSystemN (2 * (m + 1)) 3 W)
    (p : V (2 * (m + 1))) (ι : V (2 * (m + 1)) → Fin 3)
    (hbinary : ∃ i j : Fin 3, ∀ v ∈ retainedSites p, ι v = i ∨ ι v = j)
    (a : Fin 3 → ℂ) :
    coeff (wordExponent ι ((vertices (2 * (m + 1))).erase p))
      (C (((m - r).factorial : ℂ)⁻¹) * rowAt W p a ^ (2 * r + 1) *
        deletedQuadratic W p ^ (m - r)) = 0 := by
  have h := congrArg (eval a) (whole_binary_response_zero m r hr hpos W hW p ι hbinary)
  simpa only [eval_oddResponsePolynomial, oddResponse, hr, if_true,
    retainedCoefficient_project, map_zero] using h

end KrennAllOrders.WholeBinaryResponse
