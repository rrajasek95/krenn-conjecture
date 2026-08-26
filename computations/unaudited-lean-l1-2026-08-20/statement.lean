/-
UNAUDITED — lane L1 (Lean formalization), staged 2026-08-20.
Pinned krenn-conjecture HEAD: f9a3bd6b93417a43d86ad782d1f76b62f14bc50a
Not spine. Not submitted anywhere. This banner is a staging artifact and is
NOT part of the proposed diff.

WHAT THIS FILE IS
  The exact text proposed for addition to
      FormalConjectures/Paper/MonochromaticQuantumGraph.lean
  of google-deepmind/formal-conjectures, in that file's own style and
  namespace. Four additive hunks, no deletions. `statement.diff` in this
  directory is the machine-generated unified diff: 84 additions, 0 deletions.

  `eqSystem8_no_solution_d3` itself is NOT touched. It is the general
  bicoloured system and stays `category research open`.

VERIFIED
  Spliced into a shallow clone of google-deepmind/formal-conjectures at the
  toolchain the repository pins for itself (`lean-toolchain` =
  leanprover/lean4:v4.27.0, mathlib a3a10db0e9d66acbebf76c5e6a135066525ac900)
  and built with

      lake --wfail build FormalConjectures.Paper.MonochromaticQuantumGraph

  -> rc=0, 8057 jobs, no warnings (--wfail makes warnings fatal, as CI does).

  The three lemmas carrying real proofs are sorry-free:
      eqSystemNZ_of_eqSystemN            [propext]
      isDiagonal_witness4_d3             [propext, Classical.choice, Quot.sound]
      eqSystem4_has_diagonal_solution_d3 [propext, Classical.choice, Quot.sound]

  The three N=8 theorems are `sorry` placeholders carrying `formal_proof`
  links, the shape formal-conjectures PR #4610 uses for the (6,3) case.
  Their statements were type-checked against the intended propositions, and
  `eqSystem8_no_solution_d3_diagonal_domain` was checked to specialise
  directly to the C, R and Z readings, with the {-1,0,1} reading following
  from the Z one in three lines. One theorem therefore covers the diagonal
  case of all four open n=8 d=3 registry coefficient domains.

BEFORE SUBMISSION
  The `formal_proof using lean4 at "..."` links are PLACEHOLDERS. Replace them
  with commit-pinned URLs into the published certificate repository. See
  architecture.md sec. 10 and feasibility.md sec. 5.
-/

-- ===========================================================================
-- HUNK 1 - insert after `def mkEdge` (upstream line 100), with the other
--          edge/weight definitions.
-- ===========================================================================

/-- A weighting is **diagonal** if it vanishes on every edge label whose two endpoint indices
differ.

Write $A_{uv}$ for the $D \times D$ block $(i, j) \mapsto W \langle u, v, i, j \rangle$. The
condition says that each $A_{uv}$ is a diagonal matrix
$\operatorname{diag}(t^0_{uv}, \dots, t^{D-1}_{uv})$, so a matching edge contributes to
`pmSumN` only when both of its endpoints receive the same index. Diagonal weightings are the
edge-coloured multigraphs of [Krenn2017] and [MO2018], carrying one weight function per
colour; a general `WeightsN` is the bicoloured relaxation studied in [Chandran2022]. -/
def IsDiagonal {N D : Nat} {α : Type} [Zero α] (W : WeightsN N D α) : Prop :=
  ∀ e : EdgeN N D, e.i ≠ e.j → W e = 0

-- ===========================================================================
-- HUNK 2 - insert after `instance instDecidableEqSystemN` (upstream line 207).
-- ===========================================================================

/-- The equation system in unnormalised form: every monochromatic inherited colouring has
nonzero perfect-matching sum, and every other one has sum $0$.

This asks for an unnormalised GHZ state $\sum_c \lambda_c e_c^{\otimes N}$ with all $\lambda_c$
nonzero, rather than the state with all $\lambda_c = 1$ that `EqSystemN` asks for. It is implied
by `EqSystemN` over any nontrivial semiring, so a non-existence result stated for `EqSystemNZ`
is stronger. -/
def EqSystemNZ {α : Type} [Semiring α] (N D : Nat) (W : WeightsN N D α) : Prop :=
  (∀ ι : V N → Fin D, allEqual ι → pmSumN N D W ι ≠ 0) ∧
    (∀ ι : V N → Fin D, ¬ allEqual ι → pmSumN N D W ι = 0)

@[category API, AMS 5 14 81]
theorem eqSystemNZ_of_eqSystemN {N D : Nat} {α : Type} [Semiring α] [Nontrivial α]
    {W : WeightsN N D α} (h : EqSystemN N D W) : EqSystemNZ N D W := by
  refine ⟨fun ι hι => ?_, fun ι hι => ?_⟩
  · rw [h ι, if_pos hι]
    exact one_ne_zero
  · rw [h ι, if_neg hι]

-- ===========================================================================
-- HUNK 3 - insert after `end N4_D3` (upstream line 283).
-- ===========================================================================

/- ## $N = 4$, $D = 3$: the witness is diagonal

The witness already recorded for $N = 4$, $D = 3$ is diagonal, so the $N = 8$ obstruction below
is specific to $N = 8$ and is not an artefact of the diagonal restriction. -/

@[category test, AMS 5 14 81]
theorem isDiagonal_witness4_d3 {α : Type} [Semiring α] :
    IsDiagonal (Witness4_d3 (α := α)) := by
  rintro ⟨u, v, i, j⟩ hij
  simp only [Witness4_d3, mkEdge]
  fin_cases i <;> fin_cases j <;> simp_all [EdgeN.mk.injEq]

@[category test, AMS 5 14 81]
theorem eqSystem4_has_diagonal_solution_d3 {α : Type} [Semiring α] :
    ∃ W : WeightsN 4 3 α, IsDiagonal W ∧ EqSystemN 4 3 W := by
  refine ⟨Witness4_d3 (α := α), isDiagonal_witness4_d3, ?_⟩
  intro ι
  have h :
      ∀ a b c d : Fin 3,
        pmSumN 4 3 (W := Witness4_d3 (α := α)) ![a, b, c, d] =
          (if allEqual ![a, b, c, d] then (1 : α) else (0 : α)) := by
    intro a b c d
    simp [pmSumN, pmSumList, pmSumListAux, vertices,
        allEqual, allEqualList, Witness4_d3, mkEdge]
    fin_cases a <;> simp <;> fin_cases b <;> simp <;> fin_cases c <;> simp <;> fin_cases d <;>
      simp
  have hι : ι = ![ι 0, ι 1, ι 2, ι 3] := by funext k; fin_cases k <;> simp
  rw [hι]; exact h (ι 0) (ι 1) (ι 2) (ι 3)

-- ===========================================================================
-- HUNK 4 - insert after `eqSystem8_no_solution_d3` (upstream line 455).
--          That declaration is left exactly as it is.
-- ===========================================================================

/-- For $N = 8$ and $D = 3$, there is no *diagonal* solution to the monochromatic quantum graph
equation system over $\mathbb{C}$.

Equivalently: no edge-coloured multigraph on eight vertices with three colours and complex edge
weights has all three monochromatic inherited colourings of weight $1$ and every other inherited
colouring of weight $0$. This is the model of [Krenn2017] and [MO2018]; the general bicoloured
case `eqSystem8_no_solution_d3` is open. -/
@[category research solved, AMS 5 14 81, formal_proof using lean4 at
"https://example.com/PLACEHOLDER-pinned-certificate-url"]
theorem eqSystem8_no_solution_d3_diagonal :
    ¬ ∃ W : WeightsN 8 3 ℂ, IsDiagonal W ∧ EqSystemN 8 3 W := by
  sorry

/-- For $N = 8$ and $D = 3$, there is no diagonal solution to the monochromatic quantum graph
equation system over any field.

The proof of `eqSystem8_no_solution_d3_diagonal` uses only that the coefficients have no zero
divisors and that $1 \neq 0$, so it needs neither $\mathbb{C}$, nor algebraic closure, nor any
root extraction. Specialising $\alpha$ covers the $\mathbb{C}$, $\mathbb{R}$ and
$\mathbb{Z}$ readings of the diagonal problem at once, and the $\mathbb{Z}$ reading in turn
covers weights restricted to $\{-1, 0, 1\}$. -/
@[category research solved, AMS 5 14 81, formal_proof using lean4 at
"https://example.com/PLACEHOLDER-pinned-certificate-url"]
theorem eqSystem8_no_solution_d3_diagonal_domain {α : Type} [CommRing α] [IsDomain α] :
    ¬ ∃ W : WeightsN 8 3 α, IsDiagonal W ∧ EqSystemN 8 3 W := by
  sorry

/-- For $N = 8$ and $D = 3$, there is no diagonal solution to the *unnormalised* equation system
over any field.

This strengthens `eqSystem8_no_solution_d3_diagonal_domain`: no diagonal weighting produces an
unnormalised GHZ state $\sum_c \lambda_c e_c^{\otimes 8}$ with all three amplitudes
$\lambda_c$ nonzero. -/
@[category research solved, AMS 5 14 81, formal_proof using lean4 at
"https://example.com/PLACEHOLDER-pinned-certificate-url"]
theorem eqSystem8_no_solution_d3_diagonal_nz_domain {α : Type} [CommRing α] [IsDomain α] :
    ¬ ∃ W : WeightsN 8 3 α, IsDiagonal W ∧ EqSystemNZ 8 3 W := by
  sorry
