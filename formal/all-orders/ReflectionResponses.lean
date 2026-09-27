/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import WickCovariance
import OddResponseVanishing
import Mathlib.LinearAlgebra.Multilinear.Curry
import Mathlib.Tactic.FinCases

/-!
# Antisymmetric contractions of actual finite Wick moments

The determinant transformation below is derived from multilinearity and
symmetry of the constructed moments. No reflection identity for a physical
response is assumed. The connection to receiving-word quadratic coefficients
uses the separate Wick coefficient bridge.
-/

namespace KrennAllOrders.ReflectionResponses

open scoped BigOperators Classical
open WickCovariance

variable {R E F U κ : Type*} [Field R]
  [AddCommGroup E] [Module R E] [AddCommGroup F] [Module R F]
  [AddCommGroup U] [Module R U]

/-- A two-slot multilinear map evaluated on its two labelled entries. -/
def pairValue (f : MultilinearMap R (fun _ : Fin 2 => F) U) (x y : F) : U :=
  f.curryLeft x (fun _ => y)

theorem pairValue_add_left (f : MultilinearMap R (fun _ : Fin 2 => F) U)
    (x y z : F) : pairValue f (x + y) z = pairValue f x z + pairValue f y z := by
  simp [pairValue, map_add]

theorem pairValue_smul_left (f : MultilinearMap R (fun _ : Fin 2 => F) U)
    (a : R) (x y : F) : pairValue f (a • x) y = a • pairValue f x y := by
  simp [pairValue, map_smul]

theorem pairValue_add_right (f : MultilinearMap R (fun _ : Fin 2 => F) U)
    (x y z : F) : pairValue f x (y + z) = pairValue f x y + pairValue f x z := by
  have h := (f.curryLeft x).map_update_add (fun _ => (0 : F)) 0 y z
  have hu (w : F) : Function.update (fun _ : Fin 1 => (0 : F)) 0 w = (fun _ => w) := by
    funext i
    fin_cases i
    rfl
  rw [hu, hu, hu] at h
  exact h

theorem pairValue_smul_right (f : MultilinearMap R (fun _ : Fin 2 => F) U)
    (a : R) (x y : F) : pairValue f x (a • y) = a • pairValue f x y := by
  have h := (f.curryLeft x).map_update_smul (fun _ => (0 : F)) 0 a y
  have hu (w : F) : Function.update (fun _ : Fin 1 => (0 : F)) 0 w = (fun _ => w) := by
    funext i
    fin_cases i
    rfl
  rw [hu, hu] at h
  exact h

/-- One local determinant contracted against a symmetric two-slot map. -/
def pairAlternation (f : MultilinearMap R (fun _ : Fin 2 => F) U)
    (l r : E →ₗ[R] F) (u v : E) : U :=
  pairValue f (l u) (r v) - pairValue f (l v) (r u)

/-- Same-replica terms cancel by slot symmetry; the cross terms contribute
the literal determinant, for an arbitrary coefficient module. -/
theorem pairAlternation_determinant (f : MultilinearMap R (fun _ : Fin 2 => F) U)
    (hsym : ∀ x y, pairValue f x y = pairValue f y x)
    (l r : E →ₗ[R] F) (a b c d : R) (u v : E) :
    pairAlternation f (a • l + c • r) (b • l + d • r) u v =
      (a * d - b * c) • pairAlternation f l r u v := by
  simp only [pairAlternation, LinearMap.add_apply, LinearMap.smul_apply,
    pairValue_add_left, pairValue_add_right, pairValue_smul_left, pairValue_smul_right]
  rw [hsym (l v) (l u), hsym (r v) (r u), hsym (r u) (l v), hsym (r v) (l u)]
  module

/-- Ordered pairs of site slots, followed by any auxiliary root slots. -/
@[reducible] def PairSlots (n : ℕ) (κ : Type*) : Type _ :=
  match n with
  | 0 => κ
  | n + 1 => Fin 2 ⊕ PairSlots n κ

instance pairSlotsFintype [Fintype κ] (n : ℕ) : Fintype (PairSlots n κ) := by
  induction n with
  | zero => exact inferInstanceAs (Fintype κ)
  | succ n ih => exact inferInstanceAs (Fintype (Fin 2 ⊕ PairSlots n κ))

/-- Full symmetry in the labelled slots; actual centered moments satisfy it. -/
def SlotSymmetric {ι : Type*} (f : MultilinearMap R (fun _ : ι => F) U) : Prop :=
  ∀ (τ : Equiv.Perm ι) (z : ι → F), f (fun i => z (τ i)) = f z

@[simp]
theorem pairValue_eq (f : MultilinearMap R (fun _ : Fin 2 => F) U) (x y : F) :
    pairValue f x y = f (fun i => if i = 0 then x else y) := by
  unfold pairValue
  rw [MultilinearMap.curryLeft_apply]
  congr 1
  funext i
  fin_cases i <;> rfl

theorem pairValue_currySum_symmetric
    (f : MultilinearMap R (fun _ : Fin 2 ⊕ κ => F) U) (hf : SlotSymmetric f)
    (x y : F) : pairValue f.currySum x y = pairValue f.currySum y x := by
  ext z
  simp only [pairValue_eq, MultilinearMap.currySum_apply']
  have h := hf (Equiv.sumCongr (Equiv.swap (0 : Fin 2) 1) (Equiv.refl κ))
    (Sum.elim (fun i => if i = 0 then x else y) z)
  have hv : (fun i => Sum.elim (fun j => if j = 0 then x else y) z
      (Equiv.sumCongr (Equiv.swap (0 : Fin 2) 1) (Equiv.refl κ) i)) =
      Sum.elim (fun j => if j = 0 then y else x) z := by
    funext i
    cases i with
    | inl i => fin_cases i <;> simp
    | inr i => rfl
  rw [hv] at h
  exact h.symm

theorem currySum_symmetric_right
    (f : MultilinearMap R (fun _ : Fin 2 ⊕ κ => F) U) (hf : SlotSymmetric f)
    (z : Fin 2 → F) : SlotSymmetric (f.currySum z) := by
  intro τ w
  have h := hf (Equiv.sumCongr (Equiv.refl (Fin 2)) τ) (Sum.elim z w)
  have hv : (fun i => Sum.elim z w (Equiv.sumCongr (Equiv.refl (Fin 2)) τ i)) =
      Sum.elim z (fun i => w (τ i)) := by
    funext i
    cases i <;> rfl
  rw [hv] at h
  exact h

/-- Contract one site determinant while retaining all other slots. -/
def contractSite (f : MultilinearMap R (fun _ : Fin 2 ⊕ κ => F) U)
    (l r : E →ₗ[R] F) (u v : E) : MultilinearMap R (fun _ : κ => F) U :=
  pairAlternation f.currySum l r u v

theorem contractSite_symmetric
    (f : MultilinearMap R (fun _ : Fin 2 ⊕ κ => F) U) (hf : SlotSymmetric f)
    (l r : E →ₗ[R] F) (u v : E) : SlotSymmetric (contractSite f l r u v) := by
  intro τ z
  unfold contractSite pairAlternation
  simp only [pairValue_eq, sub_apply]
  rw [currySum_symmetric_right f hf _ τ z, currySum_symmetric_right f hf _ τ z]

theorem contractSite_determinant
    (f : MultilinearMap R (fun _ : Fin 2 ⊕ κ => F) U) (hf : SlotSymmetric f)
    (l r : E →ₗ[R] F) (a b c d : R) (u v : E) :
    contractSite f (a • l + c • r) (b • l + d • r) u v =
      (a * d - b * c) • contractSite f l r u v :=
  pairAlternation_determinant f.currySum (pairValue_currySum_symmetric f hf) l r a b c d u v

theorem contractSite_smul
    (f : MultilinearMap R (fun _ : Fin 2 ⊕ κ => F) U)
    (a : R) (l r : E →ₗ[R] F) (u v : E) :
    contractSite (a • f) l r u v = a • contractSite f l r u v := by
  ext z
  simp [contractSite, pairAlternation, pairValue_eq, smul_sub]

/-- The complete product of local determinants, contracted in the actual slot map. -/
def contractSites : (n : ℕ) →
    MultilinearMap R (fun _ : PairSlots n κ => F) U →
    (E →ₗ[R] F) → (E →ₗ[R] F) → (Fin n → E) → (Fin n → E) →
    MultilinearMap R (fun _ : κ => F) U
  | 0, f, _, _, _, _ => f
  | n + 1, f, l, r, u, v =>
      contractSites n (contractSite f l r (u 0) (v 0)) l r (Fin.tail u) (Fin.tail v)

theorem contractSites_smul (n : ℕ)
    (f : MultilinearMap R (fun _ : PairSlots n κ => F) U)
    (a : R) (l r : E →ₗ[R] F) (u v : Fin n → E) :
    contractSites n (a • f) l r u v = a • contractSites n f l r u v := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [contractSites]
    rw [contractSite_smul]
    exact ih _ _ _

/-- A replica coordinate change multiplies the full determinant contraction
by one determinant per physical site. -/
theorem contractSites_determinant (n : ℕ)
    (f : MultilinearMap R (fun _ : PairSlots n κ => F) U) (hf : SlotSymmetric f)
    (l r : E →ₗ[R] F) (a b c d : R) (u v : Fin n → E) :
    contractSites n f (a • l + c • r) (b • l + d • r) u v =
      (a * d - b * c) ^ n • contractSites n f l r u v := by
  induction n with
  | zero => simp only [contractSites, pow_zero, one_smul]
  | succ n ih =>
    simp only [contractSites]
    rw [contractSite_determinant f hf l r a b c d, contractSites_smul]
    rw [ih _ (contractSite_symmetric f hf l r (u 0) (v 0))]
    rw [smul_smul, pow_succ']

theorem contractSites_symmetric (n : ℕ)
    (f : MultilinearMap R (fun _ : PairSlots n κ => F) U) (hf : SlotSymmetric f)
    (l r : E →ₗ[R] F) (u v : Fin n → E) :
    SlotSymmetric (contractSites n f l r u v) := by
  induction n with
  | zero => exact hf
  | succ n ih =>
    exact ih _ (contractSite_symmetric f hf l r (u 0) (v 0)) _ _

theorem contractSite_compLinearMap
    (f : MultilinearMap R (fun _ : Fin 2 ⊕ κ => F) U)
    (T : F →ₗ[R] F) (l r : E →ₗ[R] F) (u v : E) :
    contractSite (f.compLinearMap (fun _ => T)) l r u v =
      (contractSite f (T.comp l) (T.comp r) u v).compLinearMap (fun _ => T) := by
  ext z
  simp only [contractSite, pairAlternation, pairValue_eq, sub_apply,
    MultilinearMap.compLinearMap_apply, MultilinearMap.currySum_apply', LinearMap.comp_apply]
  congr 1 <;> congr 1 <;> funext i <;> cases i with
  | inl i => fin_cases i <;> rfl
  | inr i => rfl

theorem contractSites_compLinearMap (n : ℕ)
    (f : MultilinearMap R (fun _ : PairSlots n κ => F) U)
    (T : F →ₗ[R] F) (l r : E →ₗ[R] F) (u v : Fin n → E) :
    contractSites n (f.compLinearMap (fun _ => T)) l r u v =
      (contractSites n f (T.comp l) (T.comp r) u v).compLinearMap (fun _ => T) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [contractSites, contractSite_compLinearMap]
    exact ih _ _ _

/-- The first and second replica inclusions. -/
def replicaLeft : E →ₗ[R] E × E := (LinearMap.id : E →ₗ[R] E).prod 0

def replicaRight : E →ₗ[R] E × E := (0 : E →ₗ[R] E).prod LinearMap.id

@[simp] theorem replicaLeft_apply (x : E) : replicaLeft (R := R) x = (x, 0) := rfl
@[simp] theorem replicaRight_apply (x : E) : replicaRight (R := R) x = (0, x) := rfl

theorem replicaLinear_comp_left (a b c d : R) :
    (replicaLinear (E := E) a b c d).comp replicaLeft = a • replicaLeft + c • replicaRight := by
  ext x <;> simp [replicaLinear, replicaLeft, replicaRight]

theorem replicaLinear_comp_right (a b c d : R) :
    (replicaLinear (E := E) a b c d).comp replicaRight = b • replicaLeft + d • replicaRight := by
  ext x <;> simp [replicaLinear, replicaLeft, replicaRight]

/-- The physical product of local alternating factors, contracted by the
explicit finite centered Wick construction. Auxiliary slots remain multilinear. -/
noncomputable def reflectedMoment [Fintype κ] (B : E →ₗ[R] E →ₗ[R] R)
    (n : ℕ) (u v : Fin n → E) : MultilinearMap R (fun _ : κ => E × E) R :=
  contractSites n (centeredMoment (ι := PairSlots n κ) (replicaCovariance B))
    replicaLeft replicaRight u v

theorem centeredMoment_slotSymmetric [Fintype κ]
    (B : E →ₗ[R] E →ₗ[R] R) (n : ℕ) :
    SlotSymmetric (centeredMoment (ι := PairSlots n κ) (replicaCovariance B)) :=
  centeredMoment_permute _

/-- Orthogonal replica covariance and slot symmetry give the determinant law
for the whole alternating moment, including the auxiliary root variables. -/
theorem reflectedMoment_replicaLinear [Fintype κ]
    (B : E →ₗ[R] E →ₗ[R] R) (n : ℕ) (u v : Fin n → E)
    (a b c d : R) (hfirst : a ^ 2 + c ^ 2 = 1)
    (hsecond : b ^ 2 + d ^ 2 = 1) (hcross : a * b + c * d = 0)
    (z : κ → E × E) :
    reflectedMoment B n u v (fun i => replicaLinear a b c d (z i)) =
      (a * d - b * c) ^ n * reflectedMoment B n u v z := by
  let f := centeredMoment (ι := PairSlots n κ) (replicaCovariance B)
  let T := replicaLinear (E := E) a b c d
  have hinv : f.compLinearMap (fun _ => T) = f := by
    ext w
    change centeredMoment _ (fun i => T (w i)) = centeredMoment _ w
    have hcov : (replicaCovariance B).compl₁₂ T T = replicaCovariance B := by
      apply LinearMap.ext
      intro x
      apply LinearMap.ext
      intro y
      exact replicaLinear_covariance B a b c d hfirst hsecond hcross x y
    rw [← centeredMoment_naturality, hcov]
  have h := contractSites_compLinearMap n f T replicaLeft replicaRight u v
  rw [hinv, replicaLinear_comp_left, replicaLinear_comp_right,
    contractSites_determinant n f (centeredMoment_slotSymmetric B n)] at h
  have he := congrArg (fun g : MultilinearMap R (fun _ : κ => E × E) R => g z) h
  simp only [MultilinearMap.compLinearMap_apply, smul_apply, smul_eq_mul] at he
  have hdet : (a * d - b * c) ^ 2 = 1 := by
    calc
      _ = (a ^ 2 + c ^ 2) * (b ^ 2 + d ^ 2) - (a * b + c * d) ^ 2 := by ring
      _ = 1 := by rw [hfirst, hsecond, hcross]; ring
  have hpow : (a * d - b * c) ^ n * (a * d - b * c) ^ n = 1 := by
    rw [← mul_pow, ← pow_two, hdet, one_pow]
  change (contractSites n f replicaLeft replicaRight u v) (fun i => T (z i)) =
    (a * d - b * c) ^ n * (contractSites n f replicaLeft replicaRight u v) z
  calc
    _ = ((a * d - b * c) ^ n * (a * d - b * c) ^ n) *
        (contractSites n f replicaLeft replicaRight u v) (fun i => T (z i)) := by rw [hpow, one_mul]
    _ = (a * d - b * c) ^ n * (contractSites n f replicaLeft replicaRight u v) z := by
      rw [mul_assoc, ← he]

/-- An odd number of site determinants changes sign under a root-fixing
orthogonal reflection, so its actual finite Wick contraction is zero. -/
theorem reflectedMoment_eq_zero_of_reflection [Fintype κ] [CharZero R]
    (B : E →ₗ[R] E →ₗ[R] R) (n : ℕ) (hn : Odd n) (u v : Fin n → E)
    (a b c d : R) (hfirst : a ^ 2 + c ^ 2 = 1)
    (hsecond : b ^ 2 + d ^ 2 = 1) (hcross : a * b + c * d = 0)
    (hdet : a * d - b * c = -1) (z : κ → E × E)
    (hfix : ∀ i, replicaLinear a b c d (z i) = z i) :
    reflectedMoment B n u v z = 0 := by
  have h := reflectedMoment_replicaLinear B n u v a b c d hfirst hsecond hcross z
  simp only [hfix, hdet, hn.neg_one_pow, neg_one_mul] at h
  have htwo : (2 : R) * reflectedMoment B n u v z = 0 := by
    calc
      _ = reflectedMoment B n u v z - -reflectedMoment B n u v z := by ring
      _ = 0 := sub_eq_zero.mpr h
  exact (mul_eq_zero.mp htwo).resolve_left (by norm_num)

/-- The explicit reflection in a nonisotropic root direction. All quantities
are finite algebraic expressions; no real inner product is required. -/
theorem reflectedMoment_const_eq_zero [Fintype κ] [CharZero R]
    (B : E →ₗ[R] E →ₗ[R] R) (n : ℕ) (hn : Odd n) (u v : Fin n → E)
    (L : E) (s t : R) (hst : s ^ 2 + t ^ 2 ≠ 0) :
    reflectedMoment B n u v (fun _ : κ => (s • L, t • L)) = 0 := by
  let a : R := (s ^ 2 - t ^ 2) / (s ^ 2 + t ^ 2)
  let b : R := (2 * s * t) / (s ^ 2 + t ^ 2)
  have hnorm : a ^ 2 + b ^ 2 = 1 := by
    dsimp [a, b]
    field_simp
    ring
  have hs : a * s + b * t = s := by
    dsimp [a, b]
    field_simp
    ring
  have ht : b * s + (-a) * t = t := by
    dsimp [a, b]
    field_simp
    ring
  apply reflectedMoment_eq_zero_of_reflection B n hn u v a b b (-a)
  · exact hnorm
  · simpa only [neg_sq, add_comm] using hnorm
  · ring
  · calc
      a * -a - b * b = -(a ^ 2 + b ^ 2) := by ring
      _ = -1 := by rw [hnorm]
  · intro i
    simp only [replicaLinear_apply, smul_smul, ← add_smul]
    rw [hs, ht]

/-- The literal bivariate polynomial for repeated root input, obtained by
expanding the actual multilinear map over all choices of root replicas. -/
noncomputable def rootPolynomial [Fintype κ]
    (f : MultilinearMap R (fun _ : κ => F) R) (X Y : F) : MvPolynomial (Fin 2) R :=
  ∑ A : Finset κ,
    MvPolynomial.C (f (A.piecewise (fun _ => Y) (fun _ => X))) *
      MvPolynomial.X 0 ^ (Fintype.card κ - A.card) * MvPolynomial.X 1 ^ A.card

/-- Its evaluation equals the complete repeated-root moment, with no
polynomial coefficient or Wick identification supplied as a premise. -/
theorem eval_rootPolynomial [Fintype κ]
    (f : MultilinearMap R (fun _ : κ => F) R) (X Y : F) (s t : R) :
    MvPolynomial.eval (fun i => if i = 0 then s else t) (rootPolynomial f X Y) =
      f (fun _ => s • X + t • Y) := by
  classical
  unfold rootPolynomial
  simp only [map_sum, map_mul, MvPolynomial.eval_C, map_pow, MvPolynomial.eval_X,
    ite_true, show (1 : Fin 2) ≠ 0 by decide, ite_false]
  rw [show (fun _ : κ => s • X + t • Y) =
      (fun _ => t • Y) + (fun _ => s • X) by funext i; simp [add_comm]]
  rw [f.map_add_univ]
  apply Finset.sum_congr rfl
  intro A _
  have hv : A.piecewise (fun _ => t • Y) (fun _ => s • X) =
      (fun i => (if i ∈ A then t else s) •
        (A.piecewise (fun _ => Y) (fun _ => X) i)) := by
    funext i
    by_cases hi : i ∈ A <;> simp [Finset.piecewise, hi]
  rw [hv, f.map_smul_univ]
  have hp : (∏ i : κ, if i ∈ A then t else s) =
      t ^ A.card * s ^ (Fintype.card κ - A.card) := by
    rw [Finset.prod_ite]
    have hA : Finset.univ.filter (fun i : κ => i ∈ A) = A := by ext i; simp
    have hAc : Finset.univ.filter (fun i : κ => i ∉ A) = Aᶜ := by ext i; simp
    rw [hA, hAc, Finset.prod_const, Finset.prod_const, Finset.card_compl]
  rw [hp, smul_eq_mul]
  ring

/-- Odd-site reflection is an identity of the actual root polynomial,
including the isotropic root directions omitted by the reflection chart. -/
theorem rootPolynomial_reflectedMoment_eq_zero [Fintype κ] [CharZero R]
    (B : E →ₗ[R] E →ₗ[R] R) (n : ℕ) (hn : Odd n) (u v : Fin n → E) (L : E) :
    rootPolynomial (reflectedMoment B n u v (κ := κ)) (L, 0) (0, L) = 0 := by
  let P := rootPolynomial (reflectedMoment B n u v (κ := κ)) (L, 0) (0, L)
  let δ : MvPolynomial (Fin 2) R := MvPolynomial.X 0 ^ 2 + MvPolynomial.X 1 ^ 2
  have hzero : δ * P = 0 := by
    apply MvPolynomial.funext
    intro z
    have hz : (fun i : Fin 2 => if i = 0 then z 0 else z 1) = z := by
      funext i
      fin_cases i <;> rfl
    have he : MvPolynomial.eval z P =
        reflectedMoment B n u v (fun _ : κ => (z 0 • L, z 1 • L)) := by
      rw [← hz]
      rw [eval_rootPolynomial]
      congr 1
      funext i
      simp
    simp only [map_mul, map_zero]
    by_cases hh : z 0 ^ 2 + z 1 ^ 2 = 0
    · have hd : MvPolynomial.eval z δ = 0 := by simpa [δ] using hh
      rw [hd, zero_mul]
    · rw [he, reflectedMoment_const_eq_zero B n hn u v L (z 0) (z 1) hh, mul_zero]
  have hδ : δ ≠ 0 := by
    intro h
    have he := congrArg (MvPolynomial.eval (fun i : Fin 2 => if i = 0 then (1 : R) else 0)) h
    norm_num [δ] at he
  exact (mul_eq_zero.mp hzero).resolve_left hδ

/-- The exponent of the specific `s^a t^b` coefficient. -/
noncomputable def twoExponent (a b : ℕ) : Fin 2 →₀ ℕ := Finsupp.single 0 a + Finsupp.single 1 b

theorem twoExponent_eq_iff (a b c d : ℕ) :
    twoExponent a b = twoExponent c d ↔ a = c ∧ b = d := by
  constructor
  · intro h
    constructor
    · simpa [twoExponent] using congrArg (fun m => m 0) h
    · simpa [twoExponent] using congrArg (fun m => m 1) h
  · rintro ⟨rfl, rfl⟩
    rfl

theorem X_pow_mul_X_pow (a b : ℕ) :
    (MvPolynomial.X 0 ^ a * MvPolynomial.X 1 ^ b : MvPolynomial (Fin 2) R) =
      MvPolynomial.monomial (twoExponent a b) 1 := by
  rw [MvPolynomial.X_pow_eq_monomial, MvPolynomial.X_pow_eq_monomial,
    MvPolynomial.monomial_mul]
  simp only [one_mul]
  rfl

/-- The coefficient with exactly one second-replica root slot is the sum
of the corresponding literal one-slot replacements. -/
theorem coeff_rootPolynomial_one [Fintype κ]
    (f : MultilinearMap R (fun _ : κ => F) R) (X Y : F) :
    MvPolynomial.coeff (twoExponent (Fintype.card κ - 1) 1) (rootPolynomial f X Y) =
      ∑ i : κ, f (Function.update (fun _ : κ => X) i Y) := by
  classical
  unfold rootPolynomial
  rw [MvPolynomial.coeff_sum]
  have heach (A : Finset κ) :
      MvPolynomial.coeff (twoExponent (Fintype.card κ - 1) 1)
        (MvPolynomial.C (f (A.piecewise (fun _ => Y) (fun _ => X))) *
          MvPolynomial.X 0 ^ (Fintype.card κ - A.card) * MvPolynomial.X 1 ^ A.card) =
      if A.card = 1 then f (A.piecewise (fun _ => Y) (fun _ => X)) else 0 := by
    rw [mul_assoc, X_pow_mul_X_pow, MvPolynomial.coeff_C_mul]
    simp only [MvPolynomial.coeff_monomial, twoExponent_eq_iff]
    by_cases hA : A.card = 1
    · simp [hA]
    · simp [hA]
  simp_rw [heach]
  rw [← Finset.sum_filter]
  have hfilter : Finset.univ.filter (fun A : Finset κ => A.card = 1) =
      (Finset.univ : Finset κ).powersetCard 1 := by
    ext A
    simp
  rw [hfilter, Finset.powersetCard_one, Finset.sum_map]
  apply Finset.sum_congr rfl
  intro i _
  congr 1
  funext j
  simp [Finset.piecewise, Function.update, eq_comm]

/-- This is the exact `s^p t` extraction from odd-site Wick reflection. -/
theorem sum_one_root_replacements_eq_zero [Fintype κ] [CharZero R]
    (B : E →ₗ[R] E →ₗ[R] R) (n : ℕ) (hn : Odd n) (u v : Fin n → E) (L : E) :
    (∑ i : κ, reflectedMoment B n u v
      (Function.update (fun _ : κ => (L, 0)) i (0, L))) = 0 := by
  rw [← coeff_rootPolynomial_one]
  rw [rootPolynomial_reflectedMoment_eq_zero B n hn u v L]
  exact MvPolynomial.coeff_zero _

theorem symmetric_one_root_replacements
    (f : MultilinearMap R (fun _ : κ => F) R) (hf : SlotSymmetric f)
    (X Y : F) (i j : κ) :
    f (Function.update (fun _ : κ => X) i Y) =
      f (Function.update (fun _ : κ => X) j Y) := by
  have h := hf (Equiv.swap i j) (Function.update (fun _ : κ => X) i Y)
  simpa only [Function.update_apply_equiv_apply, Equiv.symm_swap,
    Equiv.swap_apply_left, Function.comp_def] using h.symm

/-- Slot symmetry cancels the exact positive integer multiplicity, leaving
the actual alternating moment with `p` first roots and one second root. -/
theorem one_root_replacement_eq_zero [Fintype κ] [CharZero R]
    (B : E →ₗ[R] E →ₗ[R] R) (n : ℕ) (hn : Odd n) (u v : Fin n → E)
    (L : E) (j : κ) :
    reflectedMoment B n u v (Function.update (fun _ : κ => (L, 0)) j (0, L)) = 0 := by
  have hs : SlotSymmetric (reflectedMoment B n u v (κ := κ)) :=
    contractSites_symmetric n _ (centeredMoment_slotSymmetric B n) _ _ u v
  have h := sum_one_root_replacements_eq_zero (κ := κ) B n hn u v L
  have he (i : κ) := symmetric_one_root_replacements _ hs (L, 0) (0, L) i j
  simp_rw [he] at h
  simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul] at h
  have hc : (Fintype.card κ : R) ≠ 0 := by
    apply Nat.cast_ne_zero.mpr
    exact Nat.ne_of_gt (Fintype.card_pos_iff.mpr ⟨j⟩)
  exact (mul_eq_zero.mp h).resolve_left hc

end KrennAllOrders.ReflectionResponses
