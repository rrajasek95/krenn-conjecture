/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import FullProof

/-!
# Real-weight consequences of the complex Krenn–Gu theorem

Semiring homomorphisms preserve the exact upstream matching recursion and
equation system. Applying the real-to-complex embedding gives the general
real theorem and the four real special cases recorded upstream.
-/

namespace KrennAllOrders.UpstreamRealProof

open MonochromaticQuantumGraph

variable {R S : Type} [Semiring R] [Semiring S] {N D : ℕ}

/-- Mapping weights through a semiring homomorphism commutes with every
fuel and vertex-list branch of the matching recursion. -/
theorem pmSumListAux_map (f : R →+* S) (W : WeightsN N D R)
    (ι : V N → Fin D) : ∀ (n : ℕ) (L : List (V N)),
      pmSumListAux (fun e => f (W e)) ι n L = f (pmSumListAux W ι n L)
  | 0, _ => (map_one f).symm
  | 1, _ => (map_zero f).symm
  | _ + 2, [] => (map_one f).symm
  | _ + 2, [_] => (map_zero f).symm
  | n + 2, a :: b :: L => by
    simp only [pmSumListAux, map_list_sum, List.map_map, Function.comp_def, map_mul]
    congr 1
    refine List.map_congr_left fun u _ => ?_
    rw [pmSumListAux_map f W ι n ((b :: L).erase u)]

/-- Mapping coefficients commutes with the complete matching sum. -/
theorem pmSumN_map (f : R →+* S) (W : WeightsN N D R) (ι : V N → Fin D) :
    pmSumN N D (fun e => f (W e)) ι = f (pmSumN N D W ι) :=
  pmSumListAux_map f W ι _ _

/-- A semiring homomorphism preserves every normalized source equation. -/
theorem eqSystemN_map (f : R →+* S) {W : WeightsN N D R} (hW : EqSystemN N D W) :
    EqSystemN N D (fun e => f (W e)) := by
  intro ι
  rw [pmSumN_map, hW]
  split_ifs <;> simp

/-- Every real solution would give a complex solution with the same amplitudes. -/
theorem eqSystemN_ofReal {W : WeightsN N D ℝ} (hW : EqSystemN N D W) :
    EqSystemN N D (fun e => (W e : ℂ)) :=
  eqSystemN_map Complex.ofRealHom hW

/-- Real-weight nonexistence for every even order at least six and every
palette of size at least three. -/
theorem no_solution_real (N D : ℕ) (hN : N ≥ 6) (heven : Even N) (hD : D ≥ 3) :
    ¬∃ W : WeightsN N D ℝ, EqSystemN N D W := by
  rintro ⟨W, hW⟩
  exact UpstreamFullProof.eqSystem_no_solution_ge6_ge3 N D hN heven hD
    ⟨fun e => (W e : ℂ), eqSystemN_ofReal hW⟩

/-- The exact affirmative answer to the general upstream real question. -/
theorem answer_true_eqSystem_no_solution_ge6_ge3_real :
    True ↔ ∀ N D : ℕ, N ≥ 6 → Even N → D ≥ 3 →
      ¬∃ W : WeightsN N D ℝ, EqSystemN N D W :=
  ⟨fun _ => no_solution_real, fun _ => trivial⟩

/-- The exact upstream real question at six vertices and three colours. -/
theorem answer_true_eqSystem6_no_solution_d3_real :
    True ↔ ¬∃ W : WeightsN 6 3 ℝ, EqSystemN 6 3 W :=
  ⟨fun _ => no_solution_real 6 3 (by omega) (by decide) (by omega), fun _ => trivial⟩

/-- The exact upstream real question at six vertices for every larger palette. -/
theorem answer_true_eqSystem6_no_solution_ge3_real :
    True ↔ ∀ D : ℕ, D ≥ 3 → ¬∃ W : WeightsN 6 D ℝ, EqSystemN 6 D W :=
  ⟨fun _ D hD => no_solution_real 6 D (by omega) (by decide) hD, fun _ => trivial⟩

/-- The exact upstream real question at eight vertices and three colours. -/
theorem answer_true_eqSystem8_no_solution_d3_real :
    True ↔ ¬∃ W : WeightsN 8 3 ℝ, EqSystemN 8 3 W :=
  ⟨fun _ => no_solution_real 8 3 (by omega) (by decide) (by omega), fun _ => trivial⟩

/-- The exact upstream real question at ten vertices and three colours. -/
theorem answer_true_eqSystem10_no_solution_d3_real :
    True ↔ ¬∃ W : WeightsN 10 3 ℝ, EqSystemN 10 3 W :=
  ⟨fun _ => no_solution_real 10 3 (by omega) (by decide) (by omega), fun _ => trivial⟩

end KrennAllOrders.UpstreamRealProof
