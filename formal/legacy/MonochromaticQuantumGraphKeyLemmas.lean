import FormalConjectures.Paper.MonochromaticQuantumGraph

/-!
# Key lemmas for the monochromatic quantum graph (Krenn palette) problem — phase 1

This file is a **compile-checked, `sorry`-free** extension of

`FormalConjectures/Paper/MonochromaticQuantumGraph.lean`

from the Formal Conjectures repository.  It contains only statements that are
*completely proved here*.  Nothing about the Krenn conjecture itself is assumed: no open
implication is recorded as an axiom, a theorem, or a placeholder.

The mathematical sources are in the proof-search repository `krenn-conjecture`:

* `/Users/rishi/krenn_conjecture_agent_prompt.md`
* `notes/clean-pair-cap-exact-descent-target.md`
* `notes/uniform-selector-union-maximal-defect-shore.md`
* `notes/line-plus-plane-shore-clean-cap-pencil.md`
* `proofs/six-site-arbitrary-complex-obstruction.md`

See `FORMALIZATION.md` in this directory for the full dependency map, proposed Lean
declarations for the not-yet-formalized steps, and the identified mathematically open
*active-line-to-active-clean-point bridge*.

## Contents

1. **`N = 2`, arbitrary finite palette `D`, arbitrary semiring.**
   `KrennPhase1.eqSystem2_has_solution` produces a solution of `EqSystemN 2 D` for every
   `D`.  This is the missing `N = 2` equation-system witness in the upstream file.  Its
   identification with the decorated-source lower bound `k_max(2) = ∞` still requires the
   source-to-aggregate equivalence described in `FORMALIZATION.md`.

2. **Palette restriction.**  `KrennPhase1.eqSystemN_restrictColors` transports a solution
   along any injection of palettes `Fin D' → Fin D`.  This is the formal counterpart of
   the colour-projection step *inside the aggregate `WeightsN` model* of
   `proofs/six-site-arbitrary-complex-obstruction.md` §2, and it reduces every upstream
   `D ≥ 3` family to its single `D = 3` case
   (`KrennPhase1.no_solution_ge3_of_no_solution_d3`).

3. **Rank-one flattening.**  `KrennPhase1.eq_of_outer_diag` and friends: an outer-product
   ("rank ≤ 1") table which is diagonal has at most one nonzero diagonal entry.  This is
   the elementary fixed-label fact behind
   `notes/line-plus-plane-shore-clean-cap-pencil.md` (5), (8), (23), (27): the
   Schmidt-rank-one left side of the flattening identity cannot equal a right side with
   two or more nonzero fixed-label coefficients.

4. **Finite-hyperplane avoidance.**  `KrennPhase1.exists_forall_add_mul_ne_zero` and
   `KrennPhase1.exists_active_member_of_pencil`: over an infinite field a parametrised
   pencil contains a point off any finite family of nonzero linear forms.  The final theorem
   is the scalar fixed-label criterion used by the intended clean-pencil application; it
   does not itself encode dimension or cleanliness.

5. **Canonical-orientation dependence.**  `KrennPhase1.eqSystemN_congr_of_lt`: the upstream
   recursion reads only endpoint-ordered entries `e.u < e.v`.  This proves insensitivity to
   loops and reverse orientations.  It does not by itself prove equivalence with the
   decorated-source model; that aggregation bridge remains to be formalized.

6. **Parity and label nondegeneracy.**  `KrennPhase1.not_eqSystemN_of_odd`: for an inhabited
   palette, odd `N` forces `1 = 0`.  `KrennPhase1.exists_ordered_weight_ne_zero_of_eqSystemN`:
   for every `c : Fin D` in a solution, some canonical entry `W (mkEdge a u c c)` with
   `a < u` is nonzero.  Relating this necessary condition to the source palette `k(E)` still
   requires the aggregation bridge.
-/


set_option autoImplicit false
set_option relaxedAutoImplicit false

open MonochromaticQuantumGraph

namespace KrennPhase1

/- ## 0. Structural facts about the upstream recursion

Two bookkeeping lemmas used repeatedly below: the unfolding equation of `pmSumListAux` in
the only interesting case, and strict sortedness of the canonical vertex list.
-/

section Structure

variable {α : Type} [Semiring α] {N D : Nat}

/-- The unfolding equation of `pmSumListAux` on a list of length at least two: pair the
head with every later vertex and recurse. -/
theorem pmSumListAux_cons_cons (W : WeightsN N D α) (ι : V N → Fin D) (m : Nat)
    (a b : V N) (L : List (V N)) :
    pmSumListAux W ι (m + 2) (a :: b :: L) =
      ((b :: L).map fun u =>
        W (mkEdge a u (ι a) (ι u)) * pmSumListAux W ι m ((b :: L).erase u)).sum :=
  rfl

/-- The canonical vertex list `[0, 1, …, N-1]` is strictly increasing. -/
theorem vertices_pairwise_lt : ∀ N : Nat, (vertices N).Pairwise (· < ·)
  | 0 => List.Pairwise.nil
  | N + 1 => by
    refine List.pairwise_cons.2 ⟨fun b hb => ?_, ?_⟩
    · obtain ⟨x, -, rfl⟩ := List.mem_map.1 hb
      exact Fin.succ_pos x
    · exact List.Pairwise.map Fin.succ (fun _ _ h => Fin.succ_lt_succ_iff.2 h)
        (vertices_pairwise_lt N)

end Structure

/- ## 1. The `N = 2` witness for an arbitrary finite palette

The conjecture's first case is `k_max(2) = ∞`: on two output vertices the intended
decorated-source witness has `D` parallel sources, the `c`-th carrying colour `c` at both
endpoints and weight `1`.  The formal result below proves its aggregate equation-system
analogue, with the sole canonical block `A_{01} = I_D`.
-/

section TwoSites

variable {α : Type} [Semiring α] {D : Nat}

/-- On two vertices the canonical ordered vertex list is `[0, 1]`. -/
theorem vertices_two : vertices 2 = [(0 : V 2), (1 : V 2)] := rfl

/-- Evaluation of the perfect-matching sum on two sites: `K₂` has exactly one perfect
matching, the single edge `0—1`. -/
theorem pmSumN_two (W : WeightsN 2 D α) (ι : V 2 → Fin D) :
    pmSumN 2 D W ι = W (mkEdge 0 1 (ι 0) (ι 1)) := by
  simp [pmSumN, pmSumList, vertices, pmSumListAux]

/-- On two sites, `allEqual` is exactly equality of the two endpoint labels. -/
theorem allEqual_two (ι : V 2 → Fin D) : allEqual ι ↔ ι 0 = ι 1 := by
  simp [allEqual, allEqualList, vertices]

/-- The two-site aggregate witness: the identity block on the canonical pair `(0, 1)` and
zero on loops and the reverse orientation. -/
def Witness2 (D : Nat) (α : Type) [Semiring α] : WeightsN 2 D α :=
  fun e => if e.u < e.v ∧ e.i = e.j then (1 : α) else (0 : α)

/-- **The `N = 2` witness.**  For every palette size `D` and every semiring `α`,
`Witness2` solves the monochromatic quantum graph equation system on two vertices. -/
theorem eqSystemN_two : EqSystemN 2 D (Witness2 D α) := by
  intro ι
  rw [pmSumN_two]
  by_cases h : ι 0 = ι 1
  · have hall : allEqual ι := (allEqual_two ι).mpr h
    simp [Witness2, mkEdge, h, hall]
  · have hall : ¬ allEqual ι := fun hh => h ((allEqual_two ι).mp hh)
    simp [Witness2, mkEdge, h, hall]

/-- **`N = 2` is solvable in `EqSystemN` for every finite palette over every semiring.**
This fills the equation-system gap left by the `N = 4` and `N = 6` upstream witnesses. -/
theorem eqSystem2_has_solution : ∃ W : WeightsN 2 D α, EqSystemN 2 D W :=
  ⟨Witness2 D α, eqSystemN_two⟩

end TwoSites

/- ## 2. Palette restriction

`proofs/six-site-arbitrary-complex-obstruction.md` §2 projects a `q`-colour monochromatic
source onto any three chosen colours.  In the aggregate model this is the passage from
`A_{uv}` to the submatrix on the chosen rows and columns.  Formally: precompose the
endpoint labels of a weight function with an injection of palettes.
-/

section Restrict

variable {α : Type} [Semiring α] {N D D' : Nat}

/-- Restriction of a weight system along a map of palettes: keep only the endpoint colours
in the image of `f`.  On aggregate blocks this is `A'_{uv} (i, j) = A_{uv} (f i, f j)`. -/
def restrictColors (f : Fin D' → Fin D) (W : WeightsN N D α) : WeightsN N D' α :=
  fun e => W ⟨e.u, e.v, f e.i, f e.j⟩

omit [Semiring α] in
@[simp]
theorem restrictColors_mkEdge (f : Fin D' → Fin D) (W : WeightsN N D α)
    (u v : V N) (i j : Fin D') :
    restrictColors f W (mkEdge u v i j) = W (mkEdge u v (f i) (f j)) := rfl

/-- Restricting the palette is the same as pushing the label assignment forward. -/
theorem pmSumListAux_restrictColors (f : Fin D' → Fin D) (W : WeightsN N D α)
    (ι : V N → Fin D') : ∀ (n : Nat) (L : List (V N)),
      pmSumListAux (restrictColors f W) ι n L = pmSumListAux W (fun x => f (ι x)) n L
  | 0, _ => rfl
  | 1, _ => rfl
  | _ + 2, [] => rfl
  | _ + 2, [_] => rfl
  | n + 2, a :: b :: L => by
    rw [pmSumListAux_cons_cons, pmSumListAux_cons_cons]
    congr 1
    refine List.map_congr_left fun u _ => ?_
    rw [pmSumListAux_restrictColors f W ι n ((b :: L).erase u)]
    rfl

theorem pmSumN_restrictColors (f : Fin D' → Fin D) (W : WeightsN N D α) (ι : V N → Fin D') :
    pmSumN N D' (restrictColors f W) ι = pmSumN N D W (fun x => f (ι x)) :=
  pmSumListAux_restrictColors f W ι _ _

/-- An injection of palettes does not change whether all labels are equal. -/
theorem allEqual_comp (f : Fin D' → Fin D) (hf : Function.Injective f) (ι : V N → Fin D') :
    allEqual (fun x => f (ι x)) ↔ allEqual ι :=
  List.IsChain.iff fun _ _ => ⟨fun h => hf h, fun h => congrArg f h⟩

/-- **Palette restriction.**  A solution of `EqSystemN N D` restricts along any injection
`Fin D' → Fin D` to a solution of `EqSystemN N D'`.

Within the aggregate `WeightsN` model, this is the formal counterpart of colour projection in
`proofs/six-site-arbitrary-complex-obstruction.md` §2 and of the "project three selected
colour axes" step of `notes/clean-pair-cap-exact-descent-target.md` §5.  It uses only
injectivity of `f` and retains arbitrary aggregate coefficients.  The separate theorem that
decorated parallel sources aggregate to these coefficients is not proved in this file. -/
theorem eqSystemN_restrictColors {f : Fin D' → Fin D} (hf : Function.Injective f)
    {W : WeightsN N D α} (h : EqSystemN N D W) :
    EqSystemN N D' (restrictColors f W) := by
  intro ι
  rw [pmSumN_restrictColors, h]
  exact if_congr (allEqual_comp f hf ι) rfl rfl

/-- Solvability of the equation system is monotone downwards in the palette size. -/
theorem exists_eqSystemN_of_le (hD : D' ≤ D) (h : ∃ W : WeightsN N D α, EqSystemN N D W) :
    ∃ W : WeightsN N D' α, EqSystemN N D' W := by
  obtain ⟨W, hW⟩ := h
  exact ⟨restrictColors (Fin.castLE hD) W,
    eqSystemN_restrictColors (Fin.strictMono_castLE hD).injective hW⟩

/-- Contrapositive form: non-existence at palette size `D'` propagates upwards. -/
theorem not_exists_eqSystemN_of_le (hD : D' ≤ D)
    (h : ¬ ∃ W : WeightsN N D' α, EqSystemN N D' W) :
    ¬ ∃ W : WeightsN N D α, EqSystemN N D W :=
  fun hex => h (exists_eqSystemN_of_le hD hex)

end Restrict

/-- **The right-hand equation-system family in the upstream `D ≥ 3` statement reduces to
`D = 3`.**  It suffices to settle palette size three for each `N`. -/
theorem no_solution_ge3_of_no_solution_d3
    (h : ∀ N : Nat, N ≥ 6 → Even N → ¬ ∃ W : WeightsN N 3 ℂ, EqSystemN N 3 W) :
    ∀ N D : Nat, N ≥ 6 → Even N → D ≥ 3 → ¬ ∃ W : WeightsN N D ℂ, EqSystemN N D W :=
  fun N _ hN hNe hD => not_exists_eqSystemN_of_le hD (h N hN hNe)

/- ## 3. Rank-one flattening

`notes/line-plus-plane-shore-clean-cap-pencil.md` §4–§5 uses the following step.  The
flattening identity (23)/(27)

  `r(K_c) ⊗ q_A^{[h-1]} = Σ_i c_i d_i (e_i^{(u)} e_i^{(v)}) ⊗ Y_i^A`

has a left-hand side of Schmidt rank at most one across `B | A`.  In the two adapted bases
its coefficient table is therefore the outer product `x_i y_j` of the two factors, while
the right-hand side is *diagonal* with diagonal entries `c_i d_i`.  The conclusion "the
number of nonzero `c_i d_i` is at most one" is exactly the elementary fact below, and it
needs nothing beyond the absence of zero divisors — no positivity, no genericity, and no
termwise inference from a cancelling sum.
-/

section RankOneFlattening

variable {R : Type*} [MulZeroClass R] [NoZeroDivisors R] {ι : Type*}

/-- **Rank-one flattening, core form.**  If the outer-product table `(i, j) ↦ x i * y j`
vanishes off the diagonal, then at most one diagonal entry is nonzero. -/
theorem eq_of_outer_diag {x y : ι → R} (hoff : ∀ i j, i ≠ j → x i * y j = 0)
    {i j : ι} (hi : x i * y i ≠ 0) (hj : x j * y j ≠ 0) : i = j := by
  by_contra hij
  exact mul_ne_zero (left_ne_zero_of_mul hi) (right_ne_zero_of_mul hj) (hoff i j hij)

/-- **Rank-one flattening, set form.**  The diagonal support of a diagonal outer-product
table is a subsingleton.  This is equation (8) of
`notes/line-plus-plane-shore-clean-cap-pencil.md`. -/
theorem subsingleton_diag_support_of_outer_diag {x y : ι → R}
    (hoff : ∀ i j, i ≠ j → x i * y j = 0) : {i : ι | x i * y i ≠ 0}.Subsingleton :=
  fun _ hi _ hj => eq_of_outer_diag hoff hi hj

end RankOneFlattening

/-- **Fixed-label diagonal-support form.**  For labels `0, 1, 2`, an outer-product table
which vanishes off the diagonal cannot have all three diagonal entries nonzero.  In the
intended scalar-zero flattening this rules out three nonzero target coefficients; this
declaration does not define caps or the activity condition, which additionally involves a
nonzero direct scalar. -/
theorem not_forall_diag_ne_zero_of_outer_diag {x y : Fin 3 → ℂ}
    (hoff : ∀ i j, i ≠ j → x i * y j = 0) :
    ¬ ∀ i, x i * y i ≠ 0 :=
  fun h => absurd (eq_of_outer_diag hoff (h 0) (h 1)) (by decide)

/- ## 4. Finite-hyperplane avoidance and active members of a pencil

`notes/line-plus-plane-shore-clean-cap-pencil.md` §4 chooses `c` in a parametrised line
`u + t • v`, away from the three coordinate kernels and the kernel of the direct scalar.
The lemmas below prove this finite-avoidance step.  Their types do not assert that `u, v`
are independent or that the resulting pencil consists of clean caps.
-/

section Avoidance

variable {K : Type*} [Field K] [Infinite K]

/-- **Finite-hyperplane avoidance, scalar core.**  Over an infinite field, a finite family
of affine-linear functions `t ↦ a k + t * b k`, none of them identically zero, has a
common non-root. -/
theorem exists_forall_add_mul_ne_zero {ι : Type*} [Finite ι] (a b : ι → K)
    (h : ∀ k, a k ≠ 0 ∨ b k ≠ 0) : ∃ t : K, ∀ k, a k + t * b k ≠ 0 := by
  classical
  have hfin : ∀ k : ι, {t : K | a k + t * b k = 0}.Finite := by
    intro k
    rcases eq_or_ne (b k) 0 with hb | hb
    · have ha : a k ≠ 0 := (h k).resolve_right (not_not_intro hb)
      refine Set.Finite.subset Set.finite_empty fun t ht => ?_
      simp only [Set.mem_setOf_eq, hb, mul_zero, add_zero] at ht
      exact absurd ht ha
    · refine Set.Finite.subset (Set.finite_singleton (-(a k) / b k)) fun t ht => ?_
      simp only [Set.mem_setOf_eq] at ht
      simp only [Set.mem_singleton_iff, eq_div_iff hb]
      linear_combination ht
  obtain ⟨t, ht⟩ := ((Set.infinite_univ (α := K)).diff (Set.finite_iUnion hfin)).nonempty
  exact ⟨t, fun k hk => ht.2 (Set.mem_iUnion.2 ⟨k, hk⟩)⟩

/-- **Finite-hyperplane avoidance, pencil form.**  If every member of a finite family of
linear forms is nonzero somewhere on the pencil spanned by `u` and `v`, then some point
`u + t • v` of the pencil avoids all of their kernels. -/
theorem exists_pencil_forall_ne_zero {V : Type*} [AddCommGroup V] [Module K V]
    {ι : Type*} [Finite ι] (u v : V) (f : ι → V →ₗ[K] K)
    (h : ∀ k, f k u ≠ 0 ∨ f k v ≠ 0) : ∃ t : K, ∀ k, f k (u + t • v) ≠ 0 := by
  obtain ⟨t, ht⟩ := exists_forall_add_mul_ne_zero (fun k => f k u) (fun k => f k v) h
  exact ⟨t, fun k => by simpa [map_add, map_smul, smul_eq_mul] using ht k⟩

end Avoidance

/-- **The scalar fixed-label activity criterion on a parametrised pencil.**

If an external application identifies `span {u, v}` with the clean pencil `C₀`, identifies
`d` with the endpoint-kernel vector, and identifies `σ` with the direct cap scalar, then
the conclusion below is the nonvanishing part of activity condition (13).  Formally, if

* `d` has no vanishing coordinate (the negation of gate (6)),
* each fixed coordinate restricts to a nonzero linear form on `C₀` (the negation of gate
  (7)), and
* `σ` is not identically zero on `C₀`,

then some member of the parametrised pencil makes all four scalar factors nonzero.

The hypothesis `hσ` is assumed, not established.  Establishing it in the intended cap
application requires ruling out its negation using the tensor flattening; only the scalar
diagonal-support core `not_forall_diag_ne_zero_of_outer_diag` is proved above. -/
theorem exists_active_member_of_pencil (u v d : Fin 3 → ℂ) (σ : (Fin 3 → ℂ) →ₗ[ℂ] ℂ)
    (hd : ∀ i, d i ≠ 0) (hcoord : ∀ i, u i ≠ 0 ∨ v i ≠ 0) (hσ : σ u ≠ 0 ∨ σ v ≠ 0) :
    ∃ t : ℂ, σ (u + t • v) ≠ 0 ∧ ∀ i, (u + t • v) i * d i ≠ 0 := by
  obtain ⟨t, ht⟩ :=
    exists_forall_add_mul_ne_zero (K := ℂ) (ι := Option (Fin 3))
      (fun k => k.elim (σ u) fun i => u i) (fun k => k.elim (σ v) fun i => v i)
      (fun k => by
        cases k with
        | none => exact hσ
        | some i => exact hcoord i)
  refine ⟨t, ?_, fun i => ?_⟩
  · simpa [map_add, map_smul, smul_eq_mul] using ht none
  · exact mul_ne_zero (by simpa using ht (some i)) (hd i)

/- ## 5. Canonical-orientation dependence

The upstream `EdgeN N D` is an ordered tuple with no constraint `u < v`; it permits loops
and both orientations.  The perfect-matching recursion only queries `mkEdge a u` with `a`
the head of a strictly increasing list and `u` later, so its value depends only on entries
with `e.u < e.v`.  Identifying those entries with aggregates of decorated sources is a
separate, not-yet-formalized model theorem.
-/

section Faithfulness

variable {α : Type} [Semiring α] {N D : Nat}

theorem pmSumListAux_congr_of_lt {W W' : WeightsN N D α}
    (hWW : ∀ e : EdgeN N D, e.u < e.v → W e = W' e) (ι : V N → Fin D) :
    ∀ (n : Nat) (L : List (V N)), L.Pairwise (· < ·) →
      pmSumListAux W ι n L = pmSumListAux W' ι n L
  | 0, _, _ => rfl
  | 1, _, _ => rfl
  | _ + 2, [], _ => rfl
  | _ + 2, [_], _ => rfl
  | n + 2, a :: b :: L, hL => by
    rw [pmSumListAux_cons_cons, pmSumListAux_cons_cons]
    congr 1
    refine List.map_congr_left fun u hu => ?_
    have hlt : a < u := List.rel_of_pairwise_cons hL hu
    rw [hWW (mkEdge a u (ι a) (ι u)) hlt,
      pmSumListAux_congr_of_lt hWW ι n ((b :: L).erase u)
        (List.Pairwise.sublist List.erase_sublist hL.of_cons)]

/-- **`EqSystemN` only sees canonical endpoint orientations.**  Two weight systems that
agree on every entry with `e.u < e.v` satisfy the equation system simultaneously. -/
theorem eqSystemN_congr_of_lt {W W' : WeightsN N D α}
    (hWW : ∀ e : EdgeN N D, e.u < e.v → W e = W' e) :
    EqSystemN N D W ↔ EqSystemN N D W' := by
  have key : ∀ ι : V N → Fin D, pmSumN N D W ι = pmSumN N D W' ι := fun ι =>
    pmSumListAux_congr_of_lt hWW ι _ _ (vertices_pairwise_lt N)
  exact ⟨fun h ι => (key ι).symm.trans (h ι), fun h ι => (key ι).trans (h ι)⟩

end Faithfulness

/- ## 6. Parity and canonical-label nondegeneracy

Two checks internal to the upstream equation system.

* Odd `N` is degenerate: the perfect-matching sum is identically `0`, so `EqSystemN N D`
  forces `1 = 0` when `Fin D` is inhabited.  For `D = 0` and positive `N`, there are no
  assignments `V N → Fin 0`, so `EqSystemN` is vacuous.
* In a solution over a nontrivial semiring, every label `c : Fin D` occurs on a nonzero
  canonical diagonal entry.  Turning this into a statement about the source palette `k(E)`
  requires the decorated-source aggregation theorem that is outside this file.
-/

section Degeneracy

variable {α : Type} [Semiring α] {N D : Nat}

/-- Chain-equality holds along any list for a relation that always holds. -/
private theorem isChain_of_forall {β : Type} {R : β → β → Prop} (h : ∀ a b, R a b) :
    ∀ L : List β, L.IsChain R
  | [] => .nil
  | [a] => .singleton a
  | a :: b :: L => .cons_cons (h a b) (isChain_of_forall h (b :: L))

/-- A constant label assignment is monochromatic. -/
theorem allEqual_const (c : Fin D) : allEqual (fun _ : V N => c) :=
  isChain_of_forall (fun _ _ => rfl) (vertices N)

theorem length_vertices : ∀ N : Nat, (vertices N).length = N
  | 0 => rfl
  | N + 1 => by simp [vertices, length_vertices N]

theorem vertices_ne_nil (hN : N ≠ 0) : vertices N ≠ [] := by
  cases N with
  | zero => exact absurd rfl hN
  | succ n => simp [vertices]

/-- If every canonical weight read on a strictly increasing list vanishes, so does the
perfect-matching sum. -/
theorem pmSumListAux_eq_zero_of_forall_lt (W : WeightsN N D α) (ι : V N → Fin D)
    (hW : ∀ a u : V N, a < u → W (mkEdge a u (ι a) (ι u)) = 0) :
    ∀ (n : Nat) (L : List (V N)), n = L.length → L ≠ [] → L.Pairwise (· < ·) →
      pmSumListAux W ι n L = 0
  | 0, [], _, hL, _ => absurd rfl hL
  | 0, _ :: _, hn, _, _ => by simp at hn
  | 1, _, _, _, _ => rfl
  | _ + 2, [], _, hL, _ => absurd rfl hL
  | _ + 2, [_], _, _, _ => rfl
  | _ + 2, a :: b :: L', _, _, hL => by
    rw [pmSumListAux_cons_cons]
    refine List.sum_eq_zero fun x hx => ?_
    obtain ⟨u, hu, rfl⟩ := List.mem_map.1 hx
    have hau : a < u := List.rel_of_pairwise_cons hL hu
    rw [hW a u hau, zero_mul]

/-- **Odd orders are degenerate.**  For a list of odd length there are no perfect
matchings, so the sum vanishes. -/
theorem pmSumListAux_eq_zero_of_odd (W : WeightsN N D α) (ι : V N → Fin D) :
    ∀ (n : Nat) (L : List (V N)), n = L.length → Odd n → pmSumListAux W ι n L = 0
  | 0, _, _, hn => by simp [Nat.odd_iff] at hn
  | 1, _, _, _ => rfl
  | _ + 2, [], hn, _ => by simp at hn
  | _ + 2, [_], hn, _ => by simp at hn
  | m + 2, _ :: b :: L', hn, hodd => by
    have hm : m = L'.length := by simpa using hn
    have hodd' : Odd m := by rw [Nat.odd_iff] at hodd ⊢; omega
    rw [pmSumListAux_cons_cons]
    refine List.sum_eq_zero fun x hx => ?_
    obtain ⟨u, hu, rfl⟩ := List.mem_map.1 hx
    rw [pmSumListAux_eq_zero_of_odd W ι m ((b :: L').erase u) ?_ hodd', mul_zero]
    rw [List.length_erase_of_mem hu]
    simp [hm]

theorem pmSumN_eq_zero_of_odd (hN : Odd N) (W : WeightsN N D α) (ι : V N → Fin D) :
    pmSumN N D W ι = 0 :=
  pmSumListAux_eq_zero_of_odd W ι _ _ rfl (by rwa [length_vertices])

/-- **`EqSystemN` is unsatisfiable for odd `N`** over a semiring with `1 ≠ 0` when the
palette is inhabited, witnessed explicitly by `c : Fin D`. -/
theorem not_eqSystemN_of_odd (h1 : (1 : α) ≠ 0) (hN : Odd N) (c : Fin D)
    (W : WeightsN N D α) : ¬ EqSystemN N D W := by
  intro h
  have hval := h (fun _ => c)
  rw [pmSumN_eq_zero_of_odd hN, if_pos (allEqual_const c)] at hval
  exact h1 hval.symm

/-- **Canonical-label nondegeneracy.**  In any solution of `EqSystemN N D` over a semiring
with `1 ≠ 0` and `N ≠ 0`, each `c : Fin D` occurs on a nonzero canonical diagonal entry.
This is an equation-system fact; source-palette exactness additionally needs aggregation. -/
theorem exists_ordered_weight_ne_zero_of_eqSystemN (h1 : (1 : α) ≠ 0) (hN : N ≠ 0)
    {W : WeightsN N D α} (h : EqSystemN N D W) (c : Fin D) :
    ∃ a u : V N, a < u ∧ W (mkEdge a u c c) ≠ 0 := by
  by_contra hcon
  have hzero : ∀ a u : V N, a < u → W (mkEdge a u c c) = 0 := by
    intro a u hau
    by_contra hne
    exact hcon ⟨a, u, hau, hne⟩
  have hval := h (fun _ => c)
  rw [if_pos (allEqual_const c)] at hval
  rw [pmSumN, pmSumList,
    pmSumListAux_eq_zero_of_forall_lt W _ hzero _ _ rfl (vertices_ne_nil hN)
      (vertices_pairwise_lt N)] at hval
  exact h1 hval.symm

end Degeneracy

end KrennPhase1

/- ## Reproducing the axiom audit

    cd /Users/rishi/workplace/formal-conjectures
    lake env lean /Users/rishi/workplace/krenn-conjecture/formal/MonochromaticQuantumGraphKeyLemmas.lean

compiles with no errors and no warnings.  The public declarations report only
`[propext, Classical.choice, Quot.sound]` or a subset under `#print axioms`; the private
helper is covered transitively by `allEqual_const`.  There is no `sorryAx` or custom axiom. -/
