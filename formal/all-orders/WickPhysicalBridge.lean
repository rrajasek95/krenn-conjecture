/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import ReflectionTensorBridge
import Mathlib.LinearAlgebra.Matrix.BilinearForm

/-!
# Literal physical covariance and selected-site coefficient restrictions

The covariance is the original canonically oriented endpoint-colour matrix.
Receiving-word restriction uses the genuine `killCompl` algebra map and its
exact coefficient theorem, so no selector-evaluation surrogate is used.
-/

namespace KrennAllOrders.WickPhysicalBridge

open scoped BigOperators Classical
open MatchingModel SiteAlgebra RootResponse OddResponseVanishing
open WickCovariance WickCoefficientBridge WickRootBridge ReflectionTensorBridge

variable {K : Type*} {N D : ℕ} [Field K]

/-- Coordinate vectors for the original endpoint-colour variables. -/
abbrev PhysicalSpace (N D : ℕ) (K : Type*) := SiteVariable N D → K

noncomputable def physicalBasis (z : SiteVariable N D) : PhysicalSpace N D K := Pi.single z 1

/-- The actual aggregate edge matrix as a bilinear covariance. -/
noncomputable def physicalCovariance (W : WeightsN N D K) :
    PhysicalSpace N D K →ₗ[K] PhysicalSpace N D K →ₗ[K] K :=
  Matrix.toBilin' (edgeMatrix W)

@[simp]
theorem physicalCovariance_basis (W : WeightsN N D K) (z t : SiteVariable N D) :
    physicalCovariance W (physicalBasis z) (physicalBasis t) = edgeMatrix W z t :=
  Matrix.toBilin'_single _ _ _

/-- Every original root-row combination is represented by one coordinate vector. -/
noncomputable def physicalRoot (p : V N) (a : Fin D → K) : PhysicalSpace N D K :=
  ∑ i, a i • physicalBasis (p, i)

theorem physicalCovariance_root_basis (W : WeightsN N D K) (p : V N)
    (a : Fin D → K) (z : SiteVariable N D) :
    physicalCovariance W (physicalRoot p a) (physicalBasis z) =
      ∑ i, a i * edgeMatrix W (p, i) z := by
  simp only [physicalRoot, map_sum, map_smul, LinearMap.sum_apply,
    LinearMap.smul_apply, smul_eq_mul, physicalCovariance_basis]

theorem physicalCovariance_basis_root (W : WeightsN N D K) (p : V N)
    (a : Fin D → K) (z : SiteVariable N D) :
    physicalCovariance W (physicalBasis z) (physicalRoot p a) =
      ∑ i, a i * edgeMatrix W (p, i) z := by
  simp only [physicalRoot, map_sum, map_smul, smul_eq_mul, physicalCovariance_basis]
  apply Finset.sum_congr rfl
  intro i _
  rw [edgeMatrix_symm]

/-- Root isotropy is derived from the physical same-site zero rule. -/
theorem physicalRoot_isotropic (W : WeightsN N D K) (p : V N) (a : Fin D → K) :
    physicalCovariance W (physicalRoot p a) (physicalRoot p a) = 0 := by
  simp only [physicalRoot, map_sum, map_smul, LinearMap.sum_apply,
    LinearMap.smul_apply, smul_eq_mul, physicalCovariance_basis,
    edgeMatrix_same_site, mul_zero, Finset.sum_const_zero]

section Restriction

variable {σ τ A : Type*} [Fintype σ] [Fintype τ] [AddCommMonoid A]

/-- An injective finite coordinate family accounts for the complete sum when
all coordinates outside its image have zero contribution. -/
theorem sum_of_supported_injection (f : σ → τ) (hf : Function.Injective f)
    (g : τ → A) (hg : ∀ j, j ∉ Set.range f → g j = 0) :
    (∑ j : τ, g j) = ∑ i : σ, g (f i) := by
  classical
  calc
    _ = ∑ j ∈ Finset.univ.image f, g j := by
      symm
      apply Finset.sum_subset (Finset.subset_univ _)
      intro j _ hj
      apply hg
      rintro ⟨i, rfl⟩
      exact hj (Finset.mem_image.mpr ⟨i, Finset.mem_univ _, rfl⟩)
    _ = _ := Finset.sum_image (fun i _ j _ hij => hf hij)

end Restriction

section PolynomialRestriction

variable {σ τ : Type*} [Fintype σ] [Fintype τ]

omit [Fintype σ] [Fintype τ] in
theorem killCompl_X_image (f : σ → τ) (hf : Function.Injective f) (i : σ) :
    MvPolynomial.killCompl (R := K) hf (MvPolynomial.X (f i)) = MvPolynomial.X i := by
  simpa only [MvPolynomial.rename_X] using
    MvPolynomial.killCompl_rename_app hf (MvPolynomial.X i : MvPolynomial σ K)

omit [Fintype σ] [Fintype τ] in
theorem killCompl_X_outside (f : σ → τ) (hf : Function.Injective f) (j : τ)
    (hj : j ∉ Set.range f) :
    MvPolynomial.killCompl (R := K) hf (MvPolynomial.X j) = 0 := by
  simp only [MvPolynomial.killCompl, MvPolynomial.aeval_X, dif_neg hj]

theorem killCompl_linearPolynomial (f : σ → τ) (hf : Function.Injective f) (μ : τ → K) :
    MvPolynomial.killCompl hf (linearPolynomial μ) = linearPolynomial (fun i => μ (f i)) := by
  simp only [linearPolynomial, map_sum, map_mul, MvPolynomial.killCompl_C]
  rw [sum_of_supported_injection f hf]
  · simp_rw [killCompl_X_image]
  · intro j hj
    rw [killCompl_X_outside f hf j hj, mul_zero]

theorem killCompl_symmetricQuadratic (f : σ → τ) (hf : Function.Injective f)
    (S : τ → τ → K) :
    MvPolynomial.killCompl hf (WickCoefficientBridge.symmetricQuadratic S) =
      WickCoefficientBridge.symmetricQuadratic (fun i j => S (f i) (f j)) := by
  simp only [WickCoefficientBridge.symmetricQuadratic, rawQuadratic,
    map_mul, map_sum, MvPolynomial.killCompl_C]
  congr 1
  rw [sum_of_supported_injection f hf]
  · apply Finset.sum_congr rfl
    intro i _
    rw [sum_of_supported_injection f hf]
    · simp_rw [killCompl_X_image]
    · intro j hj
      rw [killCompl_X_outside f hf j hj, mul_zero]
  · intro j hj
    simp only [killCompl_X_outside f hf j hj, mul_zero, zero_mul, Finset.sum_const_zero]

end PolynomialRestriction

section SelectedSites

/-- One receiving colour at each member of an arbitrary retained site set. -/
def selectedInput (S : Finset (V N)) (ι : V N → Fin D) (q : ↥S) :
    SiteVariable N D := (q.1, ι q.1)

theorem selectedInput_injective (S : Finset (V N)) (ι : V N → Fin D) :
    Function.Injective (selectedInput S ι) := by
  intro q r h
  apply Subtype.ext
  exact congrArg Prod.fst h

/-- Actual deletion of every variable except the specified receiving word. -/
noncomputable def selectedRestriction (S : Finset (V N)) (ι : V N → Fin D) :
    MatchingPolynomial N D K →ₐ[K] MvPolynomial (↥S) K :=
  MvPolynomial.killCompl (selectedInput_injective S ι)

theorem topExponent_map_selectedInput (S : Finset (V N)) (ι : V N → Fin D) :
    (topExponent (↥S)).mapDomain (selectedInput S ι) =
      ∑ q ∈ S, Finsupp.single (q, ι q) 1 := by
  classical
  rw [topExponent]
  change (Finsupp.mapDomain.addMonoidHom (selectedInput S ι))
    (∑ i : ↥S, Finsupp.single i 1) = _
  rw [map_sum (Finsupp.mapDomain.addMonoidHom (selectedInput S ι))]
  change (∑ i : ↥S, (Finsupp.single i 1).mapDomain (selectedInput S ι)) = _
  simp only [Finsupp.mapDomain_single, selectedInput]
  symm
  exact Finset.sum_subtype S (fun q => Iff.rfl) _

/-- This coefficient theorem applies to every polynomial, without any
homogeneity or matching-support premise. -/
theorem coeff_selectedRestriction (S : Finset (V N)) (ι : V N → Fin D)
    (P : MatchingPolynomial N D K) :
    MvPolynomial.coeff (topExponent (↥S)) (selectedRestriction S ι P) =
      MvPolynomial.coeff (∑ q ∈ S, Finsupp.single (q, ι q) 1) P := by
  rw [selectedRestriction, MvPolynomial.coeff_killCompl,
    topExponent_map_selectedInput]

theorem wordExponent_eq_list_sum (ι : V N → Fin D) (L : List (V N)) :
    wordExponent ι L = (L.map (fun q => Finsupp.single (q, ι q) 1)).sum := by
  induction L with
  | nil => rfl
  | cons q L ih => simp only [wordExponent, List.map_cons, List.sum_cons, ih]

/-- Canonical nodup lists and finite site sets have exactly the same exponent. -/
theorem wordExponent_eq_finset_sum (ι : V N → Fin D) (L : List (V N))
    (hL : L.Nodup) :
    wordExponent ι L = ∑ q ∈ L.toFinset, Finsupp.single (q, ι q) 1 := by
  rw [wordExponent_eq_list_sum]
  exact (List.sum_toFinset _ hL).symm

theorem coeff_selectedRestriction_list (ι : V N → Fin D) (L : List (V N))
    (hL : L.Nodup) (P : MatchingPolynomial N D K) :
    MvPolynomial.coeff (topExponent (↥L.toFinset))
      (selectedRestriction L.toFinset ι P) =
        MvPolynomial.coeff (wordExponent ι L) P := by
  rw [coeff_selectedRestriction, wordExponent_eq_finset_sum ι L hL]

/-- Deleting an unselected physical site commutes with literal word restriction. -/
theorem selectedRestriction_eraseSite (S : Finset (V N)) (ι : V N → Fin D)
    (p : V N) (hp : p ∉ S) (P : MatchingPolynomial N D K) :
    selectedRestriction S ι (eraseSite p P) = selectedRestriction S ι P := by
  classical
  induction P using MvPolynomial.induction_on with
  | C a => simp only [eraseSite_C]
  | add P Q ihP ihQ => simp only [map_add, ihP, ihQ]
  | mul_X P z ih =>
    simp only [map_mul, ih, eraseSite_X]
    by_cases hz : z.1 = p
    · rw [if_pos hz, map_zero]
      have hout : z ∉ Set.range (selectedInput S ι) := by
        rintro ⟨q, hq⟩
        have hqp : q.1 = p := (congrArg Prod.fst hq).trans hz
        exact hp (hqp ▸ q.2)
      rw [show selectedRestriction S ι (MvPolynomial.X z) = 0 from
        killCompl_X_outside _ _ _ hout]
    · rw [if_neg hz]

theorem selectedRestriction_rowAt (S : Finset (V N)) (ι : V N → Fin D)
    (W : WeightsN N D K) (p : V N) (a : Fin D → K) :
    selectedRestriction S ι (rowAt W p a) =
      linearPolynomial (fun q : ↥S =>
        physicalCovariance W (physicalRoot p a) (physicalBasis (selectedInput S ι q))) := by
  classical
  simp only [rowAt, rootFamilyRow, map_sum, map_mul,
    selectedRestriction, MvPolynomial.killCompl_C]
  have hrow : ∀ i, MvPolynomial.killCompl (selectedInput_injective S ι)
      (rowPolynomial (edgeMatrix W) (p, i)) =
        linearPolynomial (fun q : ↥S => edgeMatrix W (p, i) (selectedInput S ι q)) :=
    fun i => killCompl_linearPolynomial _ _ _
  simp_rw [hrow]
  simp only [linearPolynomial, physicalCovariance_root_basis, map_sum,
    Finset.mul_sum, Finset.sum_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro q _
  apply Finset.sum_congr rfl
  intro i _
  rw [map_mul]
  ring

theorem selectedRestriction_deletedQuadratic (S : Finset (V N))
    (ι : V N → Fin D) (W : WeightsN N D K) (p : V N) (hp : p ∉ S) :
    selectedRestriction S ι (deletedQuadratic W p) =
      WickCoefficientBridge.symmetricQuadratic (fun q r : ↥S =>
        physicalCovariance W (physicalBasis (selectedInput S ι q))
          (physicalBasis (selectedInput S ι r))) := by
  rw [deletedQuadratic, selectedRestriction_eraseSite S ι p hp]
  change MvPolynomial.killCompl (selectedInput_injective S ι)
    (WickCoefficientBridge.symmetricQuadratic (edgeMatrix W)) = _
  rw [killCompl_symmetricQuadratic]
  simp only [physicalCovariance_basis]

end SelectedSites

section PhysicalRootMoments

variable [CharZero K]

/-- Literal Wick moments of repeated physical root rows, for any selected
retained site set. No source equation is used in this coefficient bridge. -/
theorem centeredMoment_selected_roots {κ : Type*} [Fintype κ] [DecidableEq κ]
    (S : Finset (V N)) (ι : V N → Fin D) (W : WeightsN N D K) (p : V N)
    (a : Fin D → K) (k d : ℕ) (hS : S.card = 2 * k + d)
    (hκ : Fintype.card κ = d) (hp : p ∉ S) :
    centeredMoment (physicalCovariance W)
      (Sum.elim (fun q : ↥S => physicalBasis (selectedInput S ι q))
        (fun _ : κ => physicalRoot p a)) =
      MvPolynomial.coeff (∑ q ∈ S, Finsupp.single (q, ι q) 1)
        (MvPolynomial.C ((k.factorial : K)⁻¹) *
          rowAt W p a ^ d * deletedQuadratic W p ^ k) := by
  classical
  rw [centeredMoment_isotropic_roots (physicalCovariance W) _ (physicalRoot p a)
    k d (by simpa using hS) hκ (physicalRoot_isotropic W p a)
    (fun q => by rw [physicalCovariance_basis_root, physicalCovariance_root_basis])]
  rw [← coeff_selectedRestriction S ι]
  simp only [map_mul, map_pow, selectedRestriction_rowAt,
    selectedRestriction_deletedQuadratic S ι W p hp]
  rw [show selectedRestriction S ι (MvPolynomial.C ((k.factorial : K)⁻¹)) =
    MvPolynomial.C ((k.factorial : K)⁻¹) from MvPolynomial.killCompl_C _ _]

/-- The physical site set remaining after deleting one arbitrary root. -/
noncomputable def retainedSites (p : V N) : Finset (V N) :=
  ((vertices N).erase p).toFinset

theorem root_not_mem_retainedSites (p : V N) : p ∉ retainedSites p := by
  simpa only [retainedSites, List.mem_toFinset] using
    (vertices_nodup N).not_mem_erase (a := p)

theorem retainedSites_card (p : V N) : (retainedSites p).card = N - 1 := by
  rw [retainedSites, List.toFinset_card_of_nodup ((vertices_nodup N).erase p),
    List.length_erase_of_mem (mem_vertices p)]
  simp

/-- Actual retained moments equal the previously defined polynomial response
coefficient, for every receiving word and every odd response through its terminal
degree. This derives the bridge rather than assuming a Wick representation. -/
theorem centeredMoment_eq_eval_oddResponsePolynomial (k r : ℕ) (hr : r ≤ k)
    (W : WeightsN (2 * (k + 1)) D K) (p : V (2 * (k + 1)))
    (a : Fin D → K) (ι : V (2 * (k + 1)) → Fin D) :
    centeredMoment (physicalCovariance W)
      (Sum.elim (fun q : ↥(retainedSites p) =>
        physicalBasis (selectedInput (retainedSites p) ι q))
        (fun _ : Fin (2 * r + 1) => physicalRoot p a)) =
      MvPolynomial.eval a (oddResponsePolynomial W p k r ι) := by
  rw [centeredMoment_selected_roots (retainedSites p) ι W p a (k - r) (2 * r + 1)
    (by rw [retainedSites_card]; omega) (Fintype.card_fin _) (root_not_mem_retainedSites p)]
  rw [eval_oddResponsePolynomial]
  simp only [oddResponse, hr, if_true, retainedCoefficient_project]
  rw [wordExponent_eq_finset_sum ι _ ((vertices_nodup _).erase p)]
  rfl

end PhysicalRootMoments

end KrennAllOrders.WickPhysicalBridge
