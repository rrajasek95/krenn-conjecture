#!/usr/bin/env python3
"""Splice the proposed diagonal statements into the upstream registry module.

Three additive hunks, in the file's own order:
  H1  IsDiagonal              -- after `mkEdge`, with the other edge/weight defs
  H2  EqSystemNZ + bridge     -- after `instDecidableEqSystemN`
  H3  N=4 sharpness           -- after the `N4_D3` section
  H4  N=8 diagonal theorems   -- after `eqSystem8_no_solution_d3`

Nothing existing is modified or deleted.
"""
import re, sys, shutil, os

FC = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/work/fc"
TGT = f"{FC}/FormalConjectures/Paper/MonochromaticQuantumGraph.lean"
BAK = TGT + ".orig"
if not os.path.exists(BAK):
    shutil.copy(TGT, BAK)
src = open(BAK).read()

H1 = '''
/-- A weighting is **diagonal** if it vanishes on every edge label whose two endpoint indices
differ.

Write $A_{uv}$ for the $D \\times D$ block $(i, j) \\mapsto W \\langle u, v, i, j \\rangle$. The
condition says that each $A_{uv}$ is a diagonal matrix
$\\operatorname{diag}(t^0_{uv}, \\dots, t^{D-1}_{uv})$, so a matching edge contributes to
`pmSumN` only when both of its endpoints receive the same index. Diagonal weightings are the
edge-coloured multigraphs of [Krenn2017] and [MO2018], carrying one weight function per
colour; a general `WeightsN` is the bicoloured relaxation studied in [Chandran2022]. -/
def IsDiagonal {N D : Nat} {α : Type} [Zero α] (W : WeightsN N D α) : Prop :=
  ∀ e : EdgeN N D, e.i ≠ e.j → W e = 0
'''

H2 = '''
/-- The equation system in unnormalised form: every monochromatic inherited colouring has
nonzero perfect-matching sum, and every other one has sum $0$.

This asks for an unnormalised GHZ state $\\sum_c \\lambda_c e_c^{\\otimes N}$ with all $\\lambda_c$
nonzero, rather than the state with all $\\lambda_c = 1$ that `EqSystemN` asks for. It is implied
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
'''

H3 = '''
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
'''

URL = "https://example.com/PLACEHOLDER-pinned-certificate-url"
H4 = f'''
/-- For $N = 8$ and $D = 3$, there is no *diagonal* solution to the monochromatic quantum graph
equation system over $\\mathbb{{C}}$.

Equivalently: no edge-coloured multigraph on eight vertices with three colours and complex edge
weights has all three monochromatic inherited colourings of weight $1$ and every other inherited
colouring of weight $0$. This is the model of [Krenn2017] and [MO2018]; the general bicoloured
case `eqSystem8_no_solution_d3` is open. -/
@[category research solved, AMS 5 14 81, formal_proof using lean4 at
"{URL}"]
theorem eqSystem8_no_solution_d3_diagonal :
    ¬ ∃ W : WeightsN 8 3 ℂ, IsDiagonal W ∧ EqSystemN 8 3 W := by
  sorry

/-- For $N = 8$ and $D = 3$, there is no diagonal solution to the monochromatic quantum graph
equation system over any field.

The proof of `eqSystem8_no_solution_d3_diagonal` uses only that the coefficients have no zero
divisors and that $1 \\neq 0$, so it needs neither $\\mathbb{{C}}$, nor algebraic closure, nor any
root extraction. Specialising $\\alpha$ covers the $\\mathbb{{C}}$, $\\mathbb{{R}}$ and
$\\mathbb{{Z}}$ readings of the diagonal problem at once, and the $\\mathbb{{Z}}$ reading in turn
covers weights restricted to $\\{{-1, 0, 1\\}}$. -/
@[category research solved, AMS 5 14 81, formal_proof using lean4 at
"{URL}"]
theorem eqSystem8_no_solution_d3_diagonal_domain {{α : Type}} [CommRing α] [IsDomain α] :
    ¬ ∃ W : WeightsN 8 3 α, IsDiagonal W ∧ EqSystemN 8 3 W := by
  sorry

/-- For $N = 8$ and $D = 3$, there is no diagonal solution to the *unnormalised* equation system
over any field.

This strengthens `eqSystem8_no_solution_d3_diagonal_domain`: no diagonal weighting produces an
unnormalised GHZ state $\\sum_c \\lambda_c e_c^{{\\otimes 8}}$ with all three amplitudes
$\\lambda_c$ nonzero. -/
@[category research solved, AMS 5 14 81, formal_proof using lean4 at
"{URL}"]
theorem eqSystem8_no_solution_d3_diagonal_nz_domain {{α : Type}} [CommRing α] [IsDomain α] :
    ¬ ∃ W : WeightsN 8 3 α, IsDiagonal W ∧ EqSystemNZ 8 3 W := by
  sorry
'''

def after(text, anchor, block, tag):
    i = text.find(anchor)
    if i < 0:
        sys.exit(f"anchor not found for {tag}: {anchor[:60]!r}")
    j = i + len(anchor)
    return text[:j] + block + text[j:]

src = after(src, "def mkEdge {N D : Nat} (u v : V N) (i j : Fin D) : EdgeN N D :=\n  ⟨u, v, i, j⟩\n", H1, "H1")
src = after(src, "instance instDecidableEqSystemN {N D : Nat} {α : Type} [Semiring α] [DecidableEq α]\n    (W : WeightsN N D α) : Decidable (EqSystemN N D W) :=\n  Fintype.decidableForallFintype\n", H2, "H2")
src = after(src, "end N4_D3\n", H3, "H3")
src = after(src, """theorem eqSystem8_no_solution_d3 :
    answer(sorry) ↔
      ¬ ∃ W : WeightsN 8 3 ℂ, EqSystemN 8 3 W := by
  sorry
""", H4, "H4")

open(TGT, "w").write(src)
print("spliced; new length", len(src.splitlines()), "lines (was", len(open(BAK).read().splitlines()), ")")
