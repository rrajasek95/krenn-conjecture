import WickShiftedBridge
import Mathlib.Data.Finset.Sum

/-!
# Independence of actual shifted finite Wick moments

The proof separates every mean subset into its two replica parts, then uses the
already proved independence of the centered complements. No statistical or
Gaussian independence hypothesis is introduced.
-/

namespace KrennAllOrders.WickReplicaBridge

open scoped BigOperators Classical
open WickCovariance WickCoefficientBridge WickShiftedBridge

variable {K E ι κ : Type*} [Field K] [CharZero K]
  [AddCommGroup E] [Module K E] [Fintype ι] [Fintype κ]

/-- The means of the two independent replicas are kept separate. -/
def replicaMean (μ ν : E →ₗ[K] K) : (E × E) →ₗ[K] K :=
  μ.comp (LinearMap.fst K E E) + ν.comp (LinearMap.snd K E E)

omit [CharZero K] in
@[simp]
theorem replicaMean_apply (μ ν : E →ₗ[K] K) (x : E × E) :
    replicaMean μ ν x = μ x.1 + ν x.2 := rfl

/-- Decompose the complement of a replica-wise mean subset without discarding
any labels. -/
def complementSumEquiv (s : Finset ι) (t : Finset κ) :
    {z : ι ⊕ κ // z ∉ s.disjSum t} ≃ ({i : ι // i ∉ s} ⊕ {j : κ // j ∉ t}) :=
  Equiv.subtypeSum.trans (Equiv.sumCongr
    (Equiv.subtypeEquivRight (fun _ => not_congr Finset.inl_mem_disjSum))
    (Equiv.subtypeEquivRight (fun _ => not_congr Finset.inr_mem_disjSum)))

/-- Centered complement factorization, with the exact subset types needed by
the shifted-moment definition. -/
theorem centered_complement_independent (B : E →ₗ[K] E →ₗ[K] K)
    (v : ι → E) (w : κ → E) (s : Finset ι) (t : Finset κ) :
    centeredMoment (replicaCovariance B)
      (fun z : {z : ι ⊕ κ // z ∉ s.disjSum t} =>
        Sum.elim (fun i => (v i, (0 : E))) (fun j => ((0 : E), w j)) z.val) =
      centeredMoment B (fun i : {i // i ∉ s} => v i) *
        centeredMoment B (fun j : {j // j ∉ t} => w j) := by
  rw [← centeredMoment_relabel (replicaCovariance B) (complementSumEquiv s t).symm]
  have hfun : (fun i => Sum.elim (fun i => (v i, (0 : E)))
      (fun j => ((0 : E), w j)) ((complementSumEquiv s t).symm i).val) =
      Sum.elim (fun i : {i // i ∉ s} => (v i, (0 : E)))
        (fun j : {j // j ∉ t} => ((0 : E), w j)) := by
    funext i
    cases i <;> rfl
  rw [hfun]
  exact centeredMoment_independent_replicas B _ _

/-- Each separated mean subset factors literally, including its centered
complement and both deterministic products. -/
theorem shiftedTerm_independent_replicas (B : E →ₗ[K] E →ₗ[K] K)
    (μ ν : E →ₗ[K] K) (v : ι → E) (w : κ → E) (s : Finset ι) (t : Finset κ) :
    shiftedTerm (replicaCovariance B) (replicaMean μ ν) (s.disjSum t)
      (Sum.elim (fun i => (v i, (0 : E))) (fun j => ((0 : E), w j))) =
      shiftedTerm B μ s v * shiftedTerm B ν t w := by
  rw [shiftedTerm_apply, shiftedTerm_apply, shiftedTerm_apply]
  have hc := centered_complement_independent B v w s t
  let : DecidableEq (ι ⊕ κ) := Classical.decEq _
  have hc' : centeredMoment (replicaCovariance B)
      (fun i : {i : ι ⊕ κ // i ∉ s.disjSum t} =>
        Sum.elim (fun i => (v i, (0 : E))) (fun j => ((0 : E), w j)) i.val) =
      centeredMoment B (fun i : {i // i ∉ s} => v i) *
        centeredMoment B (fun j : {j // j ∉ t} => w j) := by
    convert hc using 1
    congr!
  rw [hc']
  rw [← Finset.prod_subtype (s.disjSum t) (fun _ => Iff.rfl)
    (fun z => replicaMean μ ν
      (Sum.elim (fun i => (v i, (0 : E))) (fun j => ((0 : E), w j)) z))]
  rw [Finset.prod_disjSum]
  simp only [Sum.elim_inl, Sum.elim_inr, replicaMean_apply, map_zero, add_zero, zero_add]
  rw [← Finset.prod_subtype s (fun _ => Iff.rfl) (fun i => μ (v i)),
    ← Finset.prod_subtype t (fun _ => Iff.rfl) (fun j => ν (w j))]
  ring

/-- Actual shifted finite Wick moments factor over independent replicas. The
proof sums over all mean subsets, rather than selecting a single parity sector. -/
theorem shiftedMoment_independent_replicas (B : E →ₗ[K] E →ₗ[K] K)
    (μ ν : E →ₗ[K] K) (v : ι → E) (w : κ → E) :
    shiftedMoment (replicaCovariance B) (replicaMean μ ν)
      (Sum.elim (fun i => (v i, (0 : E))) (fun j => ((0 : E), w j))) =
      shiftedMoment B μ v * shiftedMoment B ν w := by
  simp only [shiftedMoment, sum_apply]
  calc
    _ = ∑ st : Finset ι × Finset κ, shiftedTerm B μ st.1 v * shiftedTerm B ν st.2 w := by
      apply Fintype.sum_equiv Finset.sumEquiv.toEquiv
      intro s
      rw [← Finset.toLeft_disjSum_toRight (u := s), shiftedTerm_independent_replicas]
      simp [Finset.sumEquiv]
    _ = _ := by rw [Fintype.sum_prod_type, Finset.sum_mul_sum]

omit [CharZero K] in
/-- Relabelling a literal row form relabels its coefficients. -/
theorem linearPolynomial_rename_equiv (e : ι ≃ κ) (μ : κ → K) :
    MvPolynomial.rename e (WickRootBridge.linearPolynomial (fun i => μ (e i))) =
      WickRootBridge.linearPolynomial μ := by
  simp only [WickRootBridge.linearPolynomial, map_sum, map_mul,
    MvPolynomial.rename_C, MvPolynomial.rename_X]
  exact Fintype.sum_equiv e _ _ (fun _ => rfl)

/-- The complete shifted moment is independent of the enumeration of its slots.
This is proved from the literal coefficient bridge, with every mean term kept. -/
theorem shiftedMoment_relabel (B : E →ₗ[K] E →ₗ[K] K) (μ : E →ₗ[K] K)
    (e : ι ≃ κ) (v : κ → E) :
    shiftedMoment B μ (fun i => v (e i)) = shiftedMoment B μ v := by
  have hc := Fintype.card_congr e
  rw [shiftedMoment_eq_coeff_sum, shiftedMoment_eq_coeff_sum, hc]
  apply Finset.sum_congr rfl
  intro d _
  split_ifs
  · rw [← coeff_top_rename_equiv e]
    apply congrArg (MvPolynomial.coeff (topExponent κ))
    simp only [map_mul, map_pow, MvPolynomial.rename_C,
      linearPolynomial_rename_equiv e (fun i => μ (v i)),
      dividedQuadratic_rename_equiv e (fun i j => B (v i) (v j))]
  · rfl

/-- Full slot symmetry of the actual shifted multilinear moment. -/
theorem shiftedMoment_permute (B : E →ₗ[K] E →ₗ[K] K) (μ : E →ₗ[K] K)
    (τ : Equiv.Perm ι) (v : ι → E) :
    shiftedMoment B μ (fun i => v (τ i)) = shiftedMoment B μ v :=
  shiftedMoment_relabel B μ τ v

end KrennAllOrders.WickReplicaBridge
