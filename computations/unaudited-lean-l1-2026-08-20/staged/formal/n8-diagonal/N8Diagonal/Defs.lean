/-
UNAUDITED (lane L1 staging), 2026-08-20.
Part of `formal/n8-diagonal`; see that directory's README.md.
-/
import FormalConjectures.Paper.MonochromaticQuantumGraph

/-!
# The two definitions this development adds to the registry vocabulary

`IsDiagonal` and `EqSystemNZ` are exactly the definitions proposed for
`FormalConjectures/Paper/MonochromaticQuantumGraph.lean` (see `statement.lean`
and `statement.diff` in the lane directory). They are declared here, in the
upstream namespace and with the upstream text, so that this subtree compiles
against a **pristine** formal-conjectures checkout rather than a patched one.

If the registry addition lands, this file becomes redundant and should be
deleted; every other module here is unaffected, because the names and the
definitions are identical.
-/

namespace MonochromaticQuantumGraph

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

/-- The equation system in unnormalised form: every monochromatic inherited colouring has
nonzero perfect-matching sum, and every other one has sum $0$.

This asks for an unnormalised GHZ state $\sum_c \lambda_c e_c^{\otimes N}$ with all $\lambda_c$
nonzero, rather than the state with all $\lambda_c = 1$ that `EqSystemN` asks for. It is implied
by `EqSystemN` over any nontrivial semiring, so a non-existence result stated for `EqSystemNZ`
is stronger. -/
def EqSystemNZ {α : Type} [Semiring α] (N D : Nat) (W : WeightsN N D α) : Prop :=
  (∀ ι : V N → Fin D, allEqual ι → pmSumN N D W ι ≠ 0) ∧
    (∀ ι : V N → Fin D, ¬ allEqual ι → pmSumN N D W ι = 0)

theorem eqSystemNZ_of_eqSystemN {N D : Nat} {α : Type} [Semiring α] [Nontrivial α]
    {W : WeightsN N D α} (h : EqSystemN N D W) : EqSystemNZ N D W := by
  refine ⟨fun ι hι => ?_, fun ι hι => ?_⟩
  · rw [h ι, if_pos hι]
    exact one_ne_zero
  · rw [h ι, if_neg hι]

end MonochromaticQuantumGraph
