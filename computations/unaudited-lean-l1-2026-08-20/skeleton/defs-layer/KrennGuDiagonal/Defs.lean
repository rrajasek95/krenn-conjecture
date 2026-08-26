/-
UNAUDITED — lane L1, staged 2026-08-20, pinned HEAD f9a3bd6.

The definitional layer of the future certificate repository: the diagonal
predicate, the unnormalised system, and the restatement of the three target
theorems as standalone propositions over the official `formal-conjectures`
definitions.

This mirrors algal's `KrennGuCertificate/OfficialBridge.lean`, whose job is to
pin the conventions of the pinned dependency rather than to restate them. The
target theorems appear here only as `Target*` abbreviations so that the
proposition being aimed at is fixed in one place and cannot drift; nothing here
asserts them.
-/
import FormalConjectures.Paper.MonochromaticQuantumGraph

/-!
# Target propositions for the eight-site diagonal obstruction

Fixes, in one place, the three propositions the certificate repository aims at,
stated over the official `formal-conjectures` definitions.
-/

namespace KrennGuDiagonal

open MonochromaticQuantumGraph

/-- The proposition of `eqSystem8_no_solution_d3_diagonal`. -/
abbrev TargetC : Prop :=
  ¬ ∃ W : WeightsN 8 3 ℂ, IsDiagonal W ∧ EqSystemN 8 3 W

/-- The proposition of `eqSystem8_no_solution_d3_diagonal_domain`. -/
abbrev TargetDomain (α : Type) [CommRing α] [IsDomain α] : Prop :=
  ¬ ∃ W : WeightsN 8 3 α, IsDiagonal W ∧ EqSystemN 8 3 W

/-- The proposition of `eqSystem8_no_solution_d3_diagonal_nz_domain`; the
strongest of the three, and the one the proof of record establishes. -/
abbrev TargetNZ (α : Type) [CommRing α] [IsDomain α] : Prop :=
  ¬ ∃ W : WeightsN 8 3 α, IsDiagonal W ∧ EqSystemNZ 8 3 W

/-- `TargetNZ` implies `TargetDomain`: the unnormalised system is the weaker
hypothesis, so its non-existence statement is the stronger one. Sorry-free. -/
theorem targetDomain_of_targetNZ {α : Type} [CommRing α] [IsDomain α]
    (h : TargetNZ α) : TargetDomain α := by
  rintro ⟨W, hd, he⟩
  exact h ⟨W, hd, eqSystemNZ_of_eqSystemN he⟩

/-- `TargetDomain` at `ℂ` is `TargetC`. Sorry-free. -/
theorem targetC_of_targetDomain (h : TargetDomain ℂ) : TargetC := h

/-- The `ℤ`-with-weights-in-`{-1,0,1}` reading, for the record: it follows from
`TargetDomain ℤ` with no extra work. Sorry-free. -/
theorem target_trinary_int (h : TargetDomain ℤ) :
    ¬ ∃ W : WeightsN 8 3 ℤ,
        (∀ e, W e = (-1 : ℤ) ∨ W e = 0 ∨ W e = 1) ∧ IsDiagonal W ∧ EqSystemN 8 3 W := by
  rintro ⟨W, -, hd, he⟩
  exact h ⟨W, hd, he⟩

end KrennGuDiagonal
