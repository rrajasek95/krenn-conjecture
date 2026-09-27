/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import ReflectionResponses
import WickRootBridge
import BinaryPairing

/-! # The receiving-word expansion of the actual determinant contraction -/

namespace KrennAllOrders.ReflectionTensorBridge

open scoped BigOperators Classical
open ReflectionResponses WickCovariance WickCoefficientBridge

variable {R E F U κ : Type*} [Field R]
  [AddCommGroup E] [Module R E] [AddCommGroup F] [Module R F]
  [AddCommGroup U] [Module R U]

/-- A recursive Boolean word, using the same site order as the slot contraction. -/
@[reducible] def Words : ℕ → Type
  | 0 => Unit
  | n + 1 => Bool × Words n

instance wordsFintype (n : ℕ) : Fintype (Words n) := by
  induction n with
  | zero => exact inferInstanceAs (Fintype Unit)
  | succ n ih => exact inferInstanceAs (Fintype (Bool × Words n))

def wordSign : (n : ℕ) → Words n → R
  | 0, _ => 1
  | n + 1, w => (if w.1 then -1 else 1) * wordSign n w.2

/-- The selected first/second replica inputs in a determinant expansion term. -/
def wordInputs : (n : ℕ) → (E →ₗ[R] F) → (E →ₗ[R] F) →
    (Fin n → E) → (Fin n → E) → Words n → (κ → F) → PairSlots n κ → F
  | 0, _, _, _, _, _, z => z
  | n + 1, l, r, u, v, w, z =>
      Sum.elim (fun i : Fin 2 =>
        if i = 0 then l (if w.1 then v 0 else u 0)
        else r (if w.1 then u 0 else v 0))
        (wordInputs n l r (Fin.tail u) (Fin.tail v) w.2 z)

/-- Expansion is proved for every multilinear slot map, not only Wick moments. -/
theorem contractSites_expansion (n : ℕ)
    (f : MultilinearMap R (fun _ : PairSlots n κ => F) U)
    (l r : E →ₗ[R] F) (u v : Fin n → E) (z : κ → F) :
    contractSites n f l r u v z =
      ∑ w : Words n, wordSign (R := R) n w • f (wordInputs n l r u v w z) := by
  induction n with
  | zero => simp [contractSites, wordSign, wordInputs]
  | succ n ih =>
    simp only [contractSites, ih, Fintype.sum_prod_type, Fintype.sum_bool,
      wordSign, wordInputs, contractSite, pairAlternation, pairValue_eq, sub_apply,
      MultilinearMap.currySum_apply', ite_true, Bool.false_eq_true, ite_false]
    simp only [one_mul, neg_one_mul, smul_sub, neg_smul]
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro w _
    module

/-- Recursive words are exactly receiving colour functions on the ordered sites. -/
def wordsEquiv : (n : ℕ) → Words n ≃ (Fin n → Bool)
  | 0 => {
      toFun := fun _ i => Fin.elim0 i
      invFun := fun _ => ()
      left_inv := fun w => by cases w; rfl
      right_inv := fun w => by funext i; exact Fin.elim0 i }
  | n + 1 => {
      toFun := fun w => Fin.cons w.1 (wordsEquiv n w.2)
      invFun := fun w => (w 0, (wordsEquiv n).symm (Fin.tail w))
      left_inv := fun w => by
        simp only [Fin.cons_zero, Fin.tail_cons, Equiv.symm_apply_apply, Prod.mk.eta]
      right_inv := fun w => by
        simp only [Equiv.apply_symm_apply]
        exact Fin.cons_self_tail w }

theorem wordSign_eq_sign (n : ℕ) (w : Words n) :
    wordSign (R := R) n w = BinaryPairing.sign (wordsEquiv n w) := by
  induction n with
  | zero => simp [wordSign, BinaryPairing.sign]
  | succ n ih =>
    rw [wordSign, BinaryPairing.sign, Fin.prod_univ_succ]
    simp only [wordsEquiv, Equiv.coe_fn_mk, Fin.cons_zero, Fin.cons_succ]
    rw [ih]
    rfl

/-- Insert one physical slot at the beginning of a replica's labelled family. -/
def prependSlot (n : ℕ) : Fin n ⊕ κ → Fin (n + 1) ⊕ κ := Sum.map Fin.succ id

/-- Split ordered site-pairs into the two independent replica label sets,
retaining every auxiliary root label in its selected replica. -/
def splitSlotsEquiv {η : Type*} : (n : ℕ) →
    PairSlots n (κ ⊕ η) ≃ (Fin n ⊕ κ) ⊕ (Fin n ⊕ η)
  | 0 => {
      toFun := Sum.elim (fun i => Sum.inl (Sum.inr i)) (fun j => Sum.inr (Sum.inr j))
      invFun := Sum.elim (Sum.elim Fin.elim0 Sum.inl) (Sum.elim Fin.elim0 Sum.inr)
      left_inv := fun i => by cases i <;> rfl
      right_inv := fun i => by
        cases i with
        | inl i => cases i with
          | inl i => exact Fin.elim0 i
          | inr i => rfl
        | inr i => cases i with
          | inl i => exact Fin.elim0 i
          | inr i => rfl }
  | n + 1 => by
      let e : PairSlots n (κ ⊕ η) ≃ (Fin n ⊕ κ) ⊕ (Fin n ⊕ η) :=
        splitSlotsEquiv (η := η) n
      let f : PairSlots (n + 1) (κ ⊕ η) →
          (Fin (n + 1) ⊕ κ) ⊕ (Fin (n + 1) ⊕ η) :=
        Sum.elim (fun i : Fin 2 => if i = 0 then Sum.inl (Sum.inl 0) else Sum.inr (Sum.inl 0))
          (fun i => Sum.map (prependSlot n) (prependSlot n) (e i))
      let g : ((Fin (n + 1) ⊕ κ) ⊕ (Fin (n + 1) ⊕ η)) →
          PairSlots (n + 1) (κ ⊕ η) :=
        Sum.elim
          (Sum.elim (Fin.cases (Sum.inl 0) (fun i => Sum.inr (e.symm (Sum.inl (Sum.inl i)))))
            (fun i => Sum.inr (e.symm (Sum.inl (Sum.inr i)))))
          (Sum.elim (Fin.cases (Sum.inl 1) (fun i => Sum.inr (e.symm (Sum.inr (Sum.inl i)))))
            (fun i => Sum.inr (e.symm (Sum.inr (Sum.inr i)))))
      have hg (i : (Fin n ⊕ κ) ⊕ (Fin n ⊕ η)) :
          g (Sum.map (prependSlot n) (prependSlot n) i) = Sum.inr (e.symm i) := by
        cases i with
        | inl i => cases i <;> rfl
        | inr i => cases i <;> rfl
      refine { toFun := f, invFun := g, left_inv := ?_, right_inv := ?_ }
      · intro i
        cases i with
        | inl i => fin_cases i <;> simp [f, g]
        | inr i =>
          change g (Sum.map (prependSlot n) (prependSlot n) (e i)) = Sum.inr i
          rw [hg, e.symm_apply_apply]
      · intro i
        cases i with
        | inl i => cases i with
          | inl i =>
            cases i using Fin.cases with
            | zero => simp [f, g]
            | succ i => simp [f, g, e.apply_symm_apply, prependSlot]
          | inr i => simp [f, g, e.apply_symm_apply, prependSlot]
        | inr i => cases i with
          | inl i =>
            cases i using Fin.cases with
            | zero => simp [f, g]
            | succ i => simp [f, g, e.apply_symm_apply, prependSlot]
          | inr i => simp [f, g, e.apply_symm_apply, prependSlot]

def leftWord (n : ℕ) (u v : Fin n → E) (w : Words n) : Fin n → E :=
  fun i => if wordsEquiv n w i then v i else u i

def rightWord (n : ℕ) (u v : Fin n → E) (w : Words n) : Fin n → E :=
  fun i => if wordsEquiv n w i then u i else v i

def splitReplicaInputs {η : Type*} (n : ℕ) (u v : Fin n → E) (w : Words n)
    (z : κ → E) (t : η → E) : (Fin n ⊕ κ) ⊕ (Fin n ⊕ η) → E × E :=
  Sum.elim (fun i => (Sum.elim (leftWord n u v w) z i, 0))
    (fun i => (0, Sum.elim (rightWord n u v w) t i))

theorem wordInputs_eq_split {η : Type*} (n : ℕ) (u v : Fin n → E) (w : Words n)
    (z : κ → E) (t : η → E) :
    wordInputs n (replicaLeft (R := R)) replicaRight u v w
      (Sum.elim (fun i => (z i, 0)) (fun i => (0, t i))) =
      fun i => splitReplicaInputs n u v w z t (splitSlotsEquiv (κ := κ) (η := η) n i) := by
  induction n with
  | zero =>
    funext i
    cases i <;> rfl
  | succ n ih =>
    funext i
    cases i with
    | inl i =>
      fin_cases i <;>
        simp [wordInputs, splitSlotsEquiv, splitReplicaInputs, leftWord, rightWord, wordsEquiv]
    | inr i =>
      have h := congrFun (ih (Fin.tail u) (Fin.tail v) w.2) i
      simp only [wordInputs, Sum.elim_inr]
      rw [h]
      cases he : splitSlotsEquiv (κ := κ) (η := η) n i with
      | inl i => cases i with
        | inl i =>
          simp [splitSlotsEquiv, splitReplicaInputs, prependSlot, leftWord, wordsEquiv, he]
          rfl
        | inr i => simp [splitSlotsEquiv, splitReplicaInputs, prependSlot, he]
      | inr i => cases i with
        | inl i =>
          simp [splitSlotsEquiv, splitReplicaInputs, prependSlot, rightWord, wordsEquiv, he]
          rfl
        | inr i => simp [splitSlotsEquiv, splitReplicaInputs, prependSlot, he]

/-- Each selected determinant term factors into the two actual centered
moments by a proved relabelling and the literal block-covariance bridge. -/
theorem centeredMoment_wordInputs_factor [CharZero R] [Fintype κ]
    {η : Type*} [Fintype η] (B : E →ₗ[R] E →ₗ[R] R)
    (n : ℕ) (u v : Fin n → E) (w : Words n) (z : κ → E) (t : η → E) :
    centeredMoment (replicaCovariance B)
      (wordInputs n (replicaLeft (R := R)) replicaRight u v w
        (Sum.elim (fun i => (z i, 0)) (fun i => (0, t i)))) =
      centeredMoment B (Sum.elim (leftWord n u v w) z) *
        centeredMoment B (Sum.elim (rightWord n u v w) t) := by
  rw [wordInputs_eq_split]
  rw [centeredMoment_relabel _ (splitSlotsEquiv (κ := κ) (η := η) n)]
  exact centeredMoment_independent_replicas B _ _

/-- The complete alternating Wick contraction is exactly the signed
receiving-word sum of products of independently constructed moments. -/
theorem reflectedMoment_factor_sum [CharZero R] [Fintype κ]
    {η : Type*} [Fintype η] (B : E →ₗ[R] E →ₗ[R] R)
    (n : ℕ) (u v : Fin n → E) (z : κ → E) (t : η → E) :
    reflectedMoment B n u v
      (Sum.elim (fun i => (z i, 0)) (fun i => (0, t i))) =
      ∑ w : Words n, wordSign (R := R) n w *
        (centeredMoment B (Sum.elim (leftWord n u v w) z) *
          centeredMoment B (Sum.elim (rightWord n u v w) t)) := by
  rw [reflectedMoment, contractSites_expansion]
  apply Finset.sum_congr rfl
  intro w _
  rw [centeredMoment_wordInputs_factor, smul_eq_mul]

/-- A literal receiving tensor of centered moments with retained auxiliary roots. -/
noncomputable def momentTensor [Fintype κ] (B : E →ₗ[R] E →ₗ[R] R)
    (n : ℕ) (u v : Fin n → E) (z : κ → E) : BinaryPairing.Tensor (Fin n) R :=
  fun w => centeredMoment B (Sum.elim (fun i => if w i then v i else u i) z)

/-- The determinant construction is the exact finite alternating pairing of
receiving tensors, with all independent replica factors retained. -/
theorem reflectedMoment_eq_pairing [CharZero R] [Fintype κ]
    {η : Type*} [Fintype η] (B : E →ₗ[R] E →ₗ[R] R)
    (n : ℕ) (u v : Fin n → E) (z : κ → E) (t : η → E) :
    reflectedMoment B n u v
      (Sum.elim (fun i => (z i, 0)) (fun i => (0, t i))) =
      BinaryPairing.pairing (momentTensor B n u v z) (momentTensor B n u v t) := by
  classical
  rw [reflectedMoment_factor_sum, BinaryPairing.pairing]
  convert! (Fintype.sum_equiv (wordsEquiv n)
    (fun w => wordSign (R := R) n w *
      (centeredMoment B (Sum.elim (leftWord n u v w) z) *
        centeredMoment B (Sum.elim (rightWord n u v w) t)))
    (fun w => BinaryPairing.sign w * momentTensor B n u v z w *
      momentTensor B n u v t (BinaryPairing.complement w)) ?_) using 1
  · congr 1
    ext w
    simp
  intro w
  rw [wordSign_eq_sign]
  have hr : Sum.elim (rightWord n u v w) t =
      Sum.elim (fun i => if BinaryPairing.complement (wordsEquiv n w) i then v i else u i) t := by
    funext i
    cases i with
    | inl i =>
      cases h : wordsEquiv n w i <;> simp [rightWord, BinaryPairing.complement, h]
    | inr i => rfl
  rw [hr]
  change BinaryPairing.sign (wordsEquiv n w) *
      (momentTensor B n u v z (wordsEquiv n w) *
        momentTensor B n u v t (BinaryPairing.complement (wordsEquiv n w))) = _
  ring

/-- The actual odd-site reflection gives the higher-root/linear-root cross
identity before any matching-coefficient interpretation is applied. -/
theorem pairing_momentTensor_roots_eq_zero [CharZero R]
    (B : E →ₗ[R] E →ₗ[R] R) (n p : ℕ) (hn : Odd n)
    (u v : Fin n → E) (g : E) :
    BinaryPairing.pairing
      (momentTensor B n u v (fun _ : Fin p => g))
      (momentTensor B n u v (fun _ : Unit => g)) = 0 := by
  rw [← reflectedMoment_eq_pairing]
  have hz : Sum.elim (fun _ : Fin p => (g, 0)) (fun _ : Unit => (0, g)) =
      Function.update (fun _ : Fin p ⊕ Unit => (g, 0)) (Sum.inr ()) (0, g) := by
    funext i
    cases i with
    | inl i => simp
    | inr i => cases i; simp
  rw [hz]
  convert! (one_root_replacement_eq_zero (κ := Fin p ⊕ Unit) B n hn u v g (Sum.inr ())) using 1
  congr 1
  funext i
  simp [Function.update]

end KrennAllOrders.ReflectionTensorBridge
