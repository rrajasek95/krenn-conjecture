# Formalization ledger — phase 1

Dependency map from the original decorated-source statement of Krenn's conjecture toward
the upstream `EqSystemN` formulation, and from there toward the audited cap/descent lemmas
of this repository.  The arrows whose model-equivalence theorems are not yet in Lean are
marked explicitly below.

**The conjecture is not solved.** Nothing in this ledger or in
`MonochromaticQuantumGraphKeyLemmas.lean` asserts an unproved implication. Proposed Lean
declarations for not-yet-mechanized steps appear here as *markdown code blocks only*; they
are deliberately **not** present in any `.lean` file, so no open statement can be mistaken
for an axiom or a theorem. §5 states the mathematically open bridge identified by the
current proof route.

## 0. Files, toolchain, compile command

| file | role |
| --- | --- |
| `formal/MonochromaticQuantumGraphKeyLemmas.lean` | the compile-checked, `sorry`-free extension |
| `formal/FORMALIZATION.md` | this ledger |

Upstream: `/Users/rishi/workplace/formal-conjectures`, pinned at the checkout's current
`main` (`85f8637`), `FormalConjectures/Paper/MonochromaticQuantumGraph.lean`.
Toolchain `leanprover/lean4:v4.27.0`, Mathlib `v4.27.0` (`a3a10db0e9d6`).

```
cd /Users/rishi/workplace/formal-conjectures
lake env lean /Users/rishi/workplace/krenn-conjecture/formal/MonochromaticQuantumGraphKeyLemmas.lean
```

Exit code `0`, no errors, no warnings. `#print axioms` on every public declaration reports
`[propext, Classical.choice, Quot.sound]` or a subset.  The private helper is covered
transitively by `allEqual_const`.  There is no `sorryAx` or custom axiom.

No commit was made.  The sibling `formal-conjectures` checkout was used only for imports
and compilation; the two phase-1 deliverables live in the proof-search workspace.

## 1. Status legend

* **F** — formalized: a compile-checked Lean proof exists (here, or upstream *in this
  checkout*).
* **F\*** — formalized upstream but **not in this checkout**: the upstream declaration is
  a `sorry` carrying a `formal_proof using formal_conjectures at <URL>` attribute that
  points at a different commit. Usable as literature, **not** usable as a Lean hypothesis
  here.
* **R** — ready to formalize: the mathematics is complete in this repository (or is
  standard), and mechanization is a bounded engineering task. Cost estimate given.
* **O** — still mathematically open. No Lean statement is asserted for these.

## 2. Layer A — decorated sources ⟶ `EqSystemN`

The task statement (`/Users/rishi/krenn_conjecture_agent_prompt.md`) is about
`G = (A, B, E, k, w)` with `deg(a) = 2`, the weight
`w_G(c) = Σ_{M ∈ 𝓜(c)} ∏_{a ∈ M} w(a)`, and
`k_max(n) = sup |k(E)|` over monochromatic `G` with `|B| = n`.

| id | statement | status | Lean |
| --- | --- | --- | --- |
| A1 | **Aggregation.** `A_uv = Σ_{a : N(a)={u,v}} w(a) e_{k(a,u)} ⊗ e_{k(a,v)}`; the coefficient of `e_{c(0)} ⊗ … ⊗ e_{c(n-1)}` in `H_B(A)` is `w_G(c)`. Retains parallel sources, endpoint asymmetry, zero weights and cancellation. (`six-site-arbitrary-complex-obstruction.md` §2, eq. (3)) | **R** | needs the decorated-source model, §6 A1 |
| A2 | **`pmSumN` is the perfect-matching sum.** `pmSumListAux` with fuel `= L.length` enumerates each perfect matching of `L` exactly once. Upstream this is a *definitional convention*, sanity-checked by `native_decide` for `N = 4, 6` only. | **R** | §6 A2; needs a `Finset` of perfect matchings — the largest single Layer-A cost |
| A3a | **Canonical-orientation dependence.** `pmSumN` and `EqSystemN` depend only on entries with `e.u < e.v`; loops and reverse orientations are unread. | **F** | `eqSystemN_congr_of_lt`, `pmSumListAux_congr_of_lt` |
| A3b | **`WeightsN` represents aggregate decorated sources.** Under aggregation, `W ⟨u, v, i, j⟩ = A_uv(i,j)`, and every aggregate `W` has a finite decorated-source realization on the canonical pairs. | **R** | needs A1 and A2; proposed source model in §6 |
| A4a | **Canonical-label nondegeneracy.** In a solution over a nontrivial semiring with `N ≠ 0`, every `c : Fin D` occurs on some nonzero canonical diagonal entry `W (mkEdge a u c c)` with `a < u`. | **F** | `exists_ordered_weight_ne_zero_of_eqSystemN` |
| A4b | **Source-palette exactness.** Under the decorated-source equivalence, the preceding nonzero aggregate forces each label to occur in the source palette, so `D = |k(E)|`. | **R** | needs A1–A2 and a palette/range lemma |
| A5 | **Odd orders with a nonempty palette are impossible.** The matching sum is `0` for odd `N`; if `c : Fin D` exists, `EqSystemN N D W` forces `1 = 0`. For `D = 0` and positive `N`, the system is vacuous. | **F** | `pmSumN_eq_zero_of_odd`, `not_eqSystemN_of_odd` |
| A6 | **`k_max n` equals the supremum of solvable natural palette sizes in `EqSystemN`**, and that set is downward closed. | **R** (downward closure is **F**) | closure: `exists_eqSystemN_of_le`; identification needs A1–A4b and the corrected §6 A6 signature |
| A7 | **Palette projection.** A solution with `D` colours restricts along any injection `Fin D' → Fin D` to a solution with `D'` colours. (`six-site…` §2 "project every local color space"; `clean-pair-cap-exact-descent-target.md` §5.) | **F** | `eqSystemN_restrictColors`, `exists_eqSystemN_of_le`, `not_exists_eqSystemN_of_le` |

**Consequence of A7 that is new here.** Every upstream `D ≥ 3` family collapses to its
`D = 3` case:

```lean
theorem KrennPhase1.no_solution_ge3_of_no_solution_d3
    (h : ∀ N : Nat, N ≥ 6 → Even N → ¬ ∃ W : WeightsN N 3 ℂ, EqSystemN N 3 W) :
    ∀ N D : Nat, N ≥ 6 → Even N → D ≥ 3 → ¬ ∃ W : WeightsN N D ℂ, EqSystemN N D W
```

so upstream `eqSystem_no_solution_ge6_ge3` and `eqSystem6_no_solution_ge3` now reduce to
their `D = 3` right-hand sides (specialize the generic restriction theorem at `N = 6`
for the fixed case). The same holds verbatim over `ℝ`, `ℤ`
and the trinary restriction, since `restrictColors` is defined over any semiring.

## 3. Layer B — lower bounds

| id | statement | status | Lean |
| --- | --- | --- | --- |
| B1a | `EqSystemN 2 D` is solvable for every finite `D` and every semiring. | **F (new)** | `eqSystem2_has_solution`, `eqSystemN_two`, `Witness2` |
| B1b | `k_max(2) = ∞`: realize those canonical identity blocks by parallel decorated sources and invoke A6. | **R in Lean** | explicit mathematics; needs A1–A2 and A6 |
| B2 | The `EqSystemN` analogue of `k_max(4) ≥ 3` is formalized by the `K₄` 1-factorization witness.  The literal `k_max` statement still needs A6. | equation system: **F** upstream; `k_max`: **R** | `eqSystem4_has_solution_d3` (also `…_d2`) |
| B3 | The `EqSystemN` palette-2 witness at `N = 6` is upstream; the general even-`N` cycle witness and its `k_max` interpretation remain targets. | `N = 6` equation system: **F** upstream; general: **R** | `eqSystem6_has_solution_d2`; §6 B3 |

B1a is the equation-system gap this phase fills: the upstream file had witnesses for `N = 4` (`D = 2, 3`)
and `N = 6` (`D = 2`) but none for `N = 2`. The witness is the single aggregate block
`A_{01} = I_D`, valid over *any* semiring and *any* finite `D`:

```lean
def KrennPhase1.Witness2 (D : Nat) (α : Type) [Semiring α] : WeightsN 2 D α :=
  fun e => if e.u < e.v ∧ e.i = e.j then (1 : α) else (0 : α)

theorem KrennPhase1.eqSystemN_two {α : Type} [Semiring α] {D : Nat} :
    EqSystemN 2 D (Witness2 D α)

theorem KrennPhase1.eqSystem2_has_solution {α : Type} [Semiring α] {D : Nat} :
    ∃ W : WeightsN 2 D α, EqSystemN 2 D W
```

Supporting: `vertices_two`, `pmSumN_two` (`K₂` has exactly one perfect matching),
`allEqual_two`.

## 4. Layer C — upper bounds: the audited cap/descent chain

The substantive burden is `k_max(n) = 2` for even `n ≥ 6`, i.e. "no exact ternary
decorated source".  After A1–A2 and A6 are formalized, A7 reduces this to
`¬ ∃ W : WeightsN N 3 ℂ, EqSystemN N 3 W` for even `N ≥ 6`.  Within the current
Lean artifact only the equation-system reduction A7 is formalized.  The route in this
repository is *base case + descent*.

### 4.1 Base cases

| id | statement | status |
| --- | --- | --- |
| C0a | `N = 4`, `D ≥ 4` over `ℂ` has no equation-system solution (`eqSystem4_no_solution_ge4`).  With B2 and the model bridge this gives `k_max(4) = 3`. | equation system: **F\*** (upstream `sorry` + external `formal_proof` URL); `k_max`: **R** pending A6 |
| C0b | `D = N` even `≥ 4` over `ℂ` has no solution (`eqSystem_no_solution_even_ge4_d_eq_n_explicit`). | **F\*** |
| C1 | **Six-site obstruction:** `H₆(A) = Δ_{6,3}` has no complex solution (`proofs/six-site-arbitrary-complex-obstruction.md`, Theorem 1.1). Its `EqSystemN` formulation is `¬ ∃ W : WeightsN 6 3 ℂ, EqSystemN 6 3 W`; proving the equivalence in Lean uses A1–A2. | **R**, but expensive — see below |

C1 is proved on paper here (aggregation, forced anchors via `slice-cover.md`, defect
budget `d_F(v) ≤ 2`, enumeration of the 19 graph types on `|F| ≤ 6`, rectangle/Laurent
implications, primitive-lattice lemma, exceptional-triangle rigidity), but the finite
strata are discharged by SAT/DRUP and exact-support certificate scripts. Mechanizing C1
means either re-deriving those strata by hand in Lean, or importing DRUP certificates
through a verified checker. This is the single largest item in the ledger and is **not**
phase-2 scope.

### 4.2 The descent

Notation of `notes/clean-pair-cap-exact-descent-target.md`: `U = B \ {p, q}`, `|U| = 2h`;
site-square-zero algebra `𝒮_U`; `x = Σ_{{a,b} ⊂ U} A_ab`; cap covector `K`; direct scalar
`s = ⟨K, A_pq⟩`; response `r = Σ_{{a,b} ⊂ U} R_ab`; targets `κ_c = K(e_c^{(p)}, e_c^{(q)})`;
clean error `𝓔_{p,q}(K) = Σ_{k=2}^{h} s^{h-k} r^k x^{h-k} / (k! (h-k)!)`.

| id | statement | status | note |
| --- | --- | --- | --- |
| C2a | Cap expansion (12): `K ⌟ H_B(A) = [(s + r) exp(x)]_U`. | **R** | needs `𝒮_U`; phase 2 |
| C2b | Canonical error identity (15)–(16): `𝓔_{p,q}(K) = 0 ↔ H_U(x + r/s) = s⁻¹ (K ⌟ H_B(A))`. | **R** | needs `𝒮_U`; phase 2 |
| C2c | **Clean-pair descent (Theorem 1.1).** If `s κ₀ κ₁ κ₂ ≠ 0` and `𝓔_{p,q}(K) = 0` then there is a finite endpoint-coloured aggregate source on `U` with matching tensor exactly `Δ_{U,3}`; diagonal renormalization (19)–(20) and the ≤ `9·C(|U|,2)` decorated sources of (21)–(22). | **R** | phase 2/3; the aggregate half is short once C2a–C2b exist |
| C3 | **Uniform selector-union shore (`uniform-selector-union-maximal-defect-shore.md`, Thm 1.1).** If the two rank-three Rado matroids have no disjoint bases, there is `B ⊂ W`, `1 ≤ b ≤ 5`, with `b + ρ_P(A) + ρ_S(A) = 5` and the shore table (5); plus the rootless support bounds of §6. | **R**, expensive | needs matroid union rank + Rado's theorem; Mathlib has `Matroid` but **not** the union rank formula, so this is a Mathlib-contribution-sized task |
| C4 | **The whole `b = 2` pencil is clean (`line-plus-plane-shore-clean-cap-pencil.md` §3).** For `K_c = c dᵀ` with `c ∈ C₀ = ker P_A` and `d` spanning `ker S_A`, the response `r(K_c) ∈ V_u ⊗ V_v`, so `r(K_c)^{[2]} = 0` and `𝓔(K_c) = 0`. | **R** | phase 2; needs `𝒮_U` and the two-site support argument |
| C5 | **Rank-one flattening (same note, §4–§5, eqs. (8), (23), (27)).** A Schmidt-rank-≤1 left side cannot equal a diagonal right side with two or more nonzero fixed-label coefficients. | coordinate core: **F (new)**; tensor transport: **R** | see below |
| C6a | **Finite-hyperplane avoidance for a parametrised pencil.** A finite family of nonzero scalar linear forms has a common non-root. | **F (new)** | see below |
| C6b | **Application to an actual two-dimensional clean-cap pencil.** Identify the formal parameters with `C₀`, its kernel vector and direct scalar, and establish cleanliness/nondegeneracy. | **R** | depends on C4, C5 transport, and the stated nondegeneracy hypotheses |
| C7 | **The active-line-to-active-clean-point bridge.** | **O** | §5 |

**C5, formalized core.** The flattening identity, written in the two adapted bases, says
the coefficient table of the left side is an outer product `x_i y_j` while the right side
is diagonal with entries `c_i d_i`. The needed conclusion is then purely algebraic and
holds in any `MulZeroClass` without zero divisors — no positivity, no genericity, no
termwise inference from a cancelling sum:

```lean
theorem KrennPhase1.eq_of_outer_diag {R ι : Type*} [MulZeroClass R] [NoZeroDivisors R]
    {x y : ι → R} (hoff : ∀ i j, i ≠ j → x i * y j = 0)
    {i j : ι} (hi : x i * y i ≠ 0) (hj : x j * y j ≠ 0) : i = j

theorem KrennPhase1.subsingleton_diag_support_of_outer_diag {x y : ι → R}
    (hoff : ∀ i j, i ≠ j → x i * y j = 0) : {i : ι | x i * y i ≠ 0}.Subsingleton

theorem KrennPhase1.not_forall_diag_ne_zero_of_outer_diag {x y : Fin 3 → ℂ}
    (hoff : ∀ i j, i ≠ j → x i * y j = 0) : ¬ ∀ i, x i * y i ≠ 0
```

`subsingleton_diag_support_of_outer_diag` is literally eq. (8) of the note;
`not_forall_diag_ne_zero_of_outer_diag` is its three-label corollary.  In the scalar-zero
flattening used in §4, it rules out three nonzero target coefficients.  It is not itself an
activity theorem: condition (13) also requires a nonzero direct scalar, whereas that
flattening is invoked under scalar zero.  What remains (**R**, phase 2) is the *transport*:
producing `x` and `y` from `r(K_c)` and `q_A^{[h-1]}`, i.e. proving that a tensor of the form
`X ⊗ Z` has outer-product coefficients in the chosen product bases.

**C6a, formalized.** Over an infinite field a finite family of affine-linear functions with
no identically-zero member has a common non-root; on a parametrised pencil this is
hyperplane avoidance:

```lean
theorem KrennPhase1.exists_forall_add_mul_ne_zero {K ι : Type*} [Field K] [Infinite K]
    [Finite ι] (a b : ι → K) (h : ∀ k, a k ≠ 0 ∨ b k ≠ 0) :
    ∃ t : K, ∀ k, a k + t * b k ≠ 0

theorem KrennPhase1.exists_pencil_forall_ne_zero {V : Type*} [AddCommGroup V] [Module K V]
    [Finite ι] (u v : V) (f : ι → V →ₗ[K] K) (h : ∀ k, f k u ≠ 0 ∨ f k v ≠ 0) :
    ∃ t : K, ∀ k, f k (u + t • v) ≠ 0

theorem KrennPhase1.exists_active_member_of_pencil (u v d : Fin 3 → ℂ)
    (σ : (Fin 3 → ℂ) →ₗ[ℂ] ℂ) (hd : ∀ i, d i ≠ 0) (hcoord : ∀ i, u i ≠ 0 ∨ v i ≠ 0)
    (hσ : σ u ≠ 0 ∨ σ v ≠ 0) :
    ∃ t : ℂ, σ (u + t • v) ≠ 0 ∧ ∀ i, (u + t • v) i * d i ≠ 0
```

The last theorem is only the fixed-label scalar instance.  If external definitions identify
`span {u, v}` with the clean pencil, `d` with a generator of `ker S_A`, and
`σ(c) = cᵀ a d` with the direct cap scalar, then its conclusion is activity condition
(13), `σ κ₀ κ₁ κ₂ ≠ 0` with `κ_i = c_i d_i`.  Its Lean type does not assert linear
independence, dimension, kernel membership, or cleanliness.  Those identifications and the
three nondegeneracy hypotheses are assumed, not established; the actual clean-cap
application is C6b (**R**) and is discussed in §5.

### 4.3 The conditional resolution

`clean-pair-cap-exact-descent-target.md` Corollary 5.1: *if* every finite exact ternary
aggregate source on every even `|B| ≥ 8` admits `p, q, K` satisfying (5), *then* (with C1
as base case) no exact ternary aggregate exists on any even set of size ≥ 6.  A7 extends
the equation-system obstruction to every `D ≥ 3`; A1–A2 and A6 are additionally required
to conclude the source-palette upper bound 2. Status: the aggregate implication is **R**
(given C1, C2c and A7); its hypothesis is **O**.

## 5. The open step — stated clearly

> **The active-line-to-active-clean-point bridge is OPEN.**

Precisely, the following is *not proved*, here or anywhere in this repository:

> For every finite exact ternary aggregate source on an even site set `B` with `|B| ≥ 8`,
> there exist `p ≠ q ∈ B` and a cap covector `K ∈ (V_p ⊗ V_q)*` with
> `s(K) · κ₀(K) · κ₁(K) · κ₂(K) ≠ 0` **and** `𝓔_{p,q}(K) = 0`.

This is the boxed target (7) of `clean-pair-cap-exact-descent-target.md`. What *is*
proved, and where the gap sits:

1. `line-plus-plane-shore-clean-cap-pencil.md` §3 gives a whole projective **line** of
   *clean* caps `K_c = c dᵀ`, `[c] ∈ ℙ(C₀)` — but only **on the `b = 2` line-plus-plane
   shore** of the selector-union classification (C3). The `b = 1` common-coloop shore and
   the `b ≥ 3` endpoint-dark shores produce no such line at all.
2. On that line, §4 shows the activity polynomial `𝒜(c) = (cᵀ a d) ∏_i c_i d_i` is not
   identically zero **unless** gate (6) (`d_i = 0` for some `i`) or gate (7)
   (`C₀ = {c : c_i = 0}` for some `i`) holds. §6 of that note states explicitly that it
   "does not claim that (6) or (7) is impossible".
3. `exists_active_member_of_pencil` proves only the scalar conditional: its conclusion has
   the four nonzero factors needed for activity.  After C4 and the model identifications
   establish that the parameter line consists of clean caps, it yields an active clean cap.
   Formalizing C4 and the identifications is **R**.  Proving that an arbitrary exact source
   reaches the relevant shore and avoids the remaining coordinate gates is the **O** part;
   only then are the scalar hypotheses available in the required case.

So the bridge is open in three separate places: the `b = 2` shore is not known to occur;
the two coordinate gates (6)–(7) are not known to be empty; and the non-`b = 2` shores
have no clean-line argument. `uniform-selector-union-maximal-defect-shore.md` §6 removes
some rows of the shore table in the rootless branch (`b = 5` always, and any zero-rank row
with `h > b`), which narrows but does not close the classification.

Because this is open, **no Lean declaration asserting it exists**. If a future phase wants
a name for it, the honest shape is a `def … : Prop` used only as an explicit hypothesis of
conditional theorems — never a `theorem`, never an `axiom`:

```lean
/-- OPEN.  Never state this as a `theorem` or an `axiom`; use it only as an explicit
hypothesis of a conditional result. -/
def ActiveCleanCapExists : Prop :=
  ∀ (N : Nat), Even N → 8 ≤ N → ∀ A : AggregateSource N 3,
    A.matchingTensor = diagonalTensor N 3 →
      ∃ p q : V N, ∃ _ : p ≠ q, ∃ K : CapCovector A p q,
        K.scalar ≠ 0 ∧ (∀ c : Fin 3, K.kappa c ≠ 0) ∧ K.cleanError = 0
```

## 6. Exact proposed Lean declarations (phase-2+ targets)

Signatures below are targets, not claims. `V N`, `WeightsN`, `EqSystemN`, `pmSumN`,
`mkEdge` are the upstream names.

**A1 — decorated-source model and aggregation.**

```lean
/-- A finite decorated degree-two source whose endpoint colours lie in the ambient label
type `Fin D`.  Exact use of every label is the separate predicate below. -/
structure DecoratedSource (n D : Nat) where
  Src : Type
  fintypeSrc : Fintype Src
  fst snd : Src → V n
  distinct : ∀ a, fst a ≠ snd a
  colFst colSnd : Src → Fin D
  weight : Src → ℂ

def DecoratedSource.UsesEveryColor {n D : Nat} (G : DecoratedSource n D) : Prop :=
  ∀ c : Fin D, ∃ a : G.Src, G.colFst a = c ∨ G.colSnd a = c

/-- `w_G(c)` of the task statement, as a sum over `c`-consistent subsets. -/
noncomputable def DecoratedSource.wG {n D : Nat} (G : DecoratedSource n D)
    (c : V n → Fin D) : ℂ

/-- Aggregation, eq. (3) of `six-site-arbitrary-complex-obstruction.md` §2. -/
noncomputable def DecoratedSource.aggregate {n D : Nat} (G : DecoratedSource n D) :
    WeightsN n D ℂ

theorem DecoratedSource.wG_eq_pmSumN {n D : Nat} (G : DecoratedSource n D)
    (c : V n → Fin D) : G.wG c = pmSumN n D G.aggregate c

/-- Converse: every canonical aggregate is realized by a finite decorated source.  Needed
for the `k_max` identification A6. -/
theorem exists_decoratedSource_aggregate_eq {n D : Nat} (W : WeightsN n D ℂ) :
    ∃ G : DecoratedSource n D, ∀ e : EdgeN n D, e.u < e.v → G.aggregate e = W e

/-- An exact aggregate equation system forces every ambient label to occur in the source.
This combines canonical-label nondegeneracy with the finite aggregation formula. -/
theorem DecoratedSource.usesEveryColor_of_eqSystem {n D : Nat} (hn : n ≠ 0)
    (G : DecoratedSource n D) (hG : EqSystemN n D G.aggregate) : G.UsesEveryColor
```

`aggregate` must first orient each distinct endpoint pair canonically (`u < v`) and swap
the two endpoint colours when the stored source orientation is reversed.

**A2 — `pmSumN` is the perfect-matching sum.**

```lean
/-- Perfect matchings of `Fin N` as fixed-point-free involutions, or as a `Finset` of
`Finset (Sym2 (V N))`; the concrete encoding is an implementation choice. -/
def perfectMatchings (N : Nat) : Finset (Finset (V N × V N))

theorem pmSumN_eq_sum_perfectMatchings {α : Type} [CommSemiring α] (N D : Nat)
    (W : WeightsN N D α) (ι : V N → Fin D) :
    pmSumN N D W ι =
      ∑ M ∈ perfectMatchings N, ∏ e ∈ M, W (mkEdge e.1 e.2 (ι e.1) (ι e.2))
```

Note this needs `CommSemiring`: see mismatch M3 in §7.

**A6 — the `k_max` identification.**

```lean
noncomputable def kMax (n : Nat) : ℕ∞

theorem kMax_eq_sSup (n : Nat) :
    kMax n =
      sSup ((fun D : ℕ => (D : ℕ∞)) ''
        {D : ℕ | ∃ W : WeightsN n D ℂ, EqSystemN n D W})
```

The coercion image is essential: `WeightsN` and `EqSystemN` take a natural `D`, while the
supremum lives in `ℕ∞`.

**B3 — the even-`N` cycle witness, palette 2.**

```lean
/-- The two alternating perfect matchings of `C_N`: colour `0` on `{2i, 2i+1}`,
colour `1` on `{2i+1, 2i+2}` (indices mod `N`). -/
def WitnessCycle (N : Nat) (α : Type) [Semiring α] : WeightsN N 2 α

theorem eqSystemN_has_solution_d2 {α : Type} [Semiring α] (N : Nat)
    (hN : Even N) (hN' : 2 ≤ N) : ∃ W : WeightsN N 2 α, EqSystemN N 2 W
```

**C1 — six-site obstruction.**

```lean
theorem eqSystem6_no_solution_d3 : ¬ ∃ W : WeightsN 6 3 ℂ, EqSystemN 6 3 W
```

Together with `KrennPhase1.not_exists_eqSystemN_of_le` (already **F**), this settles every
`D ≥ 3` right-hand equation-system instance at `N = 6`.

**C2 — square-zero site algebra and the cap identities (phase 2, see §8).**

```lean
/-- `𝒮_U = ⨁_{T ⊆ U} ⨂_{u ∈ T} V_u` of eq. (8): products with overlapping site support
vanish. -/
def SiteAlgebra (N D : Nat) : Type

instance (N D : Nat) : CommRing (SiteAlgebra N D)

/-- Full-support component `[·]_U`. -/
def topComponent {N D : Nat} (U : Finset (V N)) : SiteAlgebra N D →ₗ[ℂ] TopTensor U D

/-- (12). -/
theorem cap_contract_eq {N D : Nat} (A : AggregateSource N 3) (p q : V N) (K : CapCovector A p q) :
    K.contract A.matchingTensor = topComponent _ ((K.scalar + K.response) * exp A.x)

/-- (16), both directions. -/
theorem cleanError_eq_zero_iff {N : Nat} (A : AggregateSource N 3) (p q : V N)
    (K : CapCovector A p q) (hs : K.scalar ≠ 0) :
    K.cleanError = 0 ↔
      matchingTensorOn (A.restrict p q) (A.x + K.scalar⁻¹ • K.response) =
        K.scalar⁻¹ • K.contract A.matchingTensor

/-- Theorem 1.1 of `clean-pair-cap-exact-descent-target.md`. -/
theorem exists_eqSystem_sub_two_of_clean_active {N : Nat} (hN : Even N) (hN' : 8 ≤ N)
    (W : WeightsN N 3 ℂ) (hW : EqSystemN N 3 W) (p q : V N) (K : CapCovector _ p q)
    (hactive : K.scalar ≠ 0 ∧ ∀ c : Fin 3, K.kappa c ≠ 0) (hclean : K.cleanError = 0) :
    ∃ W' : WeightsN (N - 2) 3 ℂ, EqSystemN (N - 2) 3 W'
```

**C3 — selector-union shore.**

```lean
theorem exists_maximal_deficient_shore {W : Finset (V N)} (P S : EndpointStar W)
    (h : ¬ ∃ bP bS : Finset (V N), Disjoint bP bS ∧ P.IsBasis bP ∧ S.IsBasis bS) :
    ∃ B ⊆ W, 1 ≤ B.card ∧ B.card ≤ 5 ∧
      B.card + P.rho (W \ B) + S.rho (W \ B) = 5 ∧
      ∀ x ∈ W \ B, P.rho ((W \ B).erase x) = P.rho (W \ B) ∧
                    S.rho ((W \ B).erase x) = S.rho (W \ B)
```

Blocked on Mathlib: `Mathlib/Combinatorics/Matroid/` in `v4.27.0` has bases, circuits,
closure, minors and rank, but **no** matroid union/partition and **no** Rado's theorem, so
formula (6) and the Rado formula (10) must both be built. Hall's theorem is available
(`Mathlib/Combinatorics/Hall/Basic.lean`) as a starting point. Expect a
Mathlib-contribution-sized subproject.

**C5 — flattening transport (makes `eq_of_outer_diag` applicable).**

```lean
/-- A tensor of the form `X ⊗ Z` has outer-product coefficients in any product basis. -/
theorem coeff_tprod_eq_mul {ι κ : Type*} (X : ι → ℂ) (Z : κ → ℂ) (i : ι) (j : κ) :
    coeff (i, j) (tprod X Z) = X i * Z j
```

## 7. Model comparison: our graph model vs upstream `WeightsN`

Five structural differences were found.  They are compatible with the intended existence
questions, but the compatibility with decorated sources is a mathematical claim until
A1–A2 are mechanized; each difference changes what a bare statement about `W` means.

* **M1 — `EdgeN` is an ordered pair with no `u < v` constraint, and `WeightsN` is a
  function on all of it.** `EdgeN N D` allows `u = v` (loops) and both orientations, so
  `WeightsN N D α` has `N² D²` free entries while the model has only `C(N,2) D²`. The
  recursion reads only entries with `e.u < e.v`. Proved here:

  ```lean
  theorem KrennPhase1.eqSystemN_congr_of_lt {W W' : WeightsN N D α}
      (hWW : ∀ e : EdgeN N D, e.u < e.v → W e = W' e) :
      EqSystemN N D W ↔ EqSystemN N D W'
  ```

  Consequences proved now: any *uniqueness*, counting, or dimension statement about the
  full function `W` would be wrong because of unread entries, and imposing
  `W ⟨u,v,i,j⟩ = W ⟨v,u,j,i⟩` would be an **extra** constraint absent from the model —
  no endpoint symmetry is assumed by `EqSystemN`.  The additional conclusion that
  `∃ W, EqSystemN N D W` is exactly decorated-source existence requires A1–A2 and is **R**,
  not a consequence of `eqSystemN_congr_of_lt` alone.

* **M2 — `WeightsN` stores one proposed aggregate coefficient per canonical label.** It has
  room for the sum of parallel sources with the same neighbour and endpoint-colour data,
  and `pmSumN` never separates such a coefficient into individual terms.  But the theorem
  that this coefficient is the sum of source weights, and that expanding products gives
  `w_G`, is exactly A1–A2 (**R**).  Thus parallel sources and complex cancellation are
  respected by the intended encoding, not yet discharged by a Lean equivalence theorem.

* **M3 — `α` is only a `Semiring`, so `pmSumN` depends on the multiplication order.**
  `pmSumListAux` multiplies `W (mkEdge v u …)` on the left of the recursive value, in the
  order the recursion picks edges. Over a non-commutative semiring the value is
  enumeration-order-dependent, so `pmSumN` is *not* "the sum over perfect matchings" there.
  The conjecture application is over `ℂ`, so this is harmless there.  The general-semiring
  lemmas in the Lean file avoid commutativity (`Witness2` and its proof do), while target A2
  must be stated for `CommSemiring`.

* **M4 — odd `N` is admitted by the definitions and is degenerate for `D > 0`.** `pmSumListAux`
  returns `0` at fuel `1`, so `pmSumN N D W ι = 0` identically for odd `N`, and
  an inhabited palette makes `EqSystemN N D W` imply `1 = 0`. Proved here
  (`pmSumN_eq_zero_of_odd`, `not_eqSystemN_of_odd`). So an upstream statement
  "`∀ N ≥ 6, ¬∃ W …`" with `D > 0` but *without*
  `Even N` would be true for a trivial reason on the odd part; upstream correctly carries
  `Even N`. For `D = 0`, `EqSystemN N 0 W` holds for every `N`: when `N > 0` there is no
  assignment `V N → Fin 0`, and at `N = 0` the empty product is `1`.

* **M5 — `D` is an exact ambient label set for `EqSystemN`, not yet a formal source
  palette.** `EqSystemN N D` demands coefficient `1` for every constant assignment in
  `Fin D`.  For `N ≠ 0`, `exists_ordered_weight_ne_zero_of_eqSystemN` proves that every
  label has a nonzero canonical diagonal entry.  Turning this into `D = |k(E)|` is A4b and
  needs A1–A2.  Independently, downward closure (`exists_eqSystemN_of_le`) proves that the
  equation-system-solvable natural sizes form a threshold.  Identifying that threshold with
  `k_max` is A6 (**R**).

Within the equation-system model, `EqSystemN` fixes every represented coefficient exactly,
not merely its support (audit item 5), and A7 proves palette-restriction validity.  Claims
about arbitrary finite source sets, their palettes, and `k_max` (items 1, 3–4, 6–7 and 9)
become formal only after A1–A2, A4b and A6.  Item 10 is not applicable to an affirmative
route.

## 8. Phase-2 scope

Deliberately **excluded** from phase 1, as instructed: the large custom square-zero site
algebra `𝒮_U` of eq. (8). Phase 2 should build, in order:

1. `SiteAlgebra` (`𝒮_U`) as a graded commutative `ℂ`-algebra with the site-square-zero
   relation, its `exp`/divided-power calculus, and the full-support projection `[·]_U`.
   This is the prerequisite for C2a, C2b, C4 and for `𝓔_{p,q}(K)` even to be *stated*.
2. The decorated-source model A1 and aggregation, then A2 (`pmSumN` = perfect-matching
   sum), source-palette lemma A4b, and A6.  These make `k_max` expressible and connect it
   to equation-system solvability in Lean.
3. C5's flattening transport, which turns the already-formalized `eq_of_outer_diag` into
   the actual Schmidt-rank step of the note.
4. C4 (`𝓔(K_c) = 0` on the whole rank-one pencil), which combined with C6
   (the scalar theorem is **F**, while the clean-pencil identifications are **R**) gives the
   conditional §4 conclusion of `line-plus-plane-shore-clean-cap-pencil.md` in Lean.
5. B3 (the general even-`N` palette-2 witness), which is independent and cheap.

C1 (six-site) and C3 (selector-union/matroid-union) are separate, larger subprojects.
C7 stays open until the mathematics is done.
