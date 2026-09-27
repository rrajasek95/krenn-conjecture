/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import MatchingModel
import FormalConjectures.Paper.MonochromaticQuantumGraph

/-!
# Identification with the upstream equation system

This file compares the definitions in `MatchingModel` with the actual
`FormalConjectures.Paper.MonochromaticQuantumGraph` definitions. It proves
the comparison through the recursion; no equivalence is assumed.
The upstream source revision used by the verification script is
`e2c4441f9545b85790aebcfaa445e194fcab9d5b`.
-/

namespace KrennAllOrders.UpstreamAdapter

variable {N D : ℕ} {R : Type}

/-- Preserve all four edge coordinates, including the ordered endpoints. -/
def toLocalWeights (W : MonochromaticQuantumGraph.WeightsN N D R) :
    MatchingModel.WeightsN N D R :=
  fun e => W ⟨e.u, e.v, e.i, e.j⟩

def toUpstreamWeights (W : MatchingModel.WeightsN N D R) :
    MonochromaticQuantumGraph.WeightsN N D R :=
  fun e => W ⟨e.u, e.v, e.i, e.j⟩

@[simp] theorem toLocal_toUpstream (W : MatchingModel.WeightsN N D R) :
    toLocalWeights (toUpstreamWeights W) = W := by
  funext e
  cases e
  rfl

@[simp] theorem toUpstream_toLocal (W : MonochromaticQuantumGraph.WeightsN N D R) :
    toUpstreamWeights (toLocalWeights W) = W := by
  funext e
  cases e
  rfl

theorem vertices_eq : ∀ n : ℕ,
    MatchingModel.vertices n = MonochromaticQuantumGraph.vertices n
  | 0 => rfl
  | n + 1 => by
    simp only [MatchingModel.vertices, MonochromaticQuantumGraph.vertices, vertices_eq n]

theorem allEqual_iff (ι : Fin N → Fin D) :
    MatchingModel.allEqual ι ↔ MonochromaticQuantumGraph.allEqual ι := by
  simp only [MatchingModel.allEqual, MonochromaticQuantumGraph.allEqual,
    MatchingModel.allEqualList, MonochromaticQuantumGraph.allEqualList, vertices_eq]

variable [Semiring R]

theorem pmSumListAux_eq (W : MonochromaticQuantumGraph.WeightsN N D R)
    (ι : Fin N → Fin D) : ∀ (n : ℕ) (L : List (Fin N)),
      MatchingModel.pmSumListAux (toLocalWeights W) ι n L =
        MonochromaticQuantumGraph.pmSumListAux W ι n L
  | 0, _ => rfl
  | 1, _ => rfl
  | _ + 2, [] => rfl
  | _ + 2, [_] => rfl
  | n + 2, a :: b :: L => by
    simp only [MatchingModel.pmSumListAux, MonochromaticQuantumGraph.pmSumListAux]
    congr 1
    refine List.map_congr_left fun u _ => ?_
    rw [pmSumListAux_eq W ι n ((b :: L).erase u)]
    rfl

theorem pmSumN_eq (W : MonochromaticQuantumGraph.WeightsN N D R)
    (ι : Fin N → Fin D) :
    MatchingModel.pmSumN N D (toLocalWeights W) ι =
      MonochromaticQuantumGraph.pmSumN N D W ι := by
  simp only [MatchingModel.pmSumN, MonochromaticQuantumGraph.pmSumN,
    MatchingModel.pmSumList, MonochromaticQuantumGraph.pmSumList,
    vertices_eq, pmSumListAux_eq]

theorem eqSystemN_iff (W : MonochromaticQuantumGraph.WeightsN N D R) :
    MatchingModel.EqSystemN N D (toLocalWeights W) ↔
      MonochromaticQuantumGraph.EqSystemN N D W := by
  simp only [MatchingModel.EqSystemN, MonochromaticQuantumGraph.EqSystemN,
    pmSumN_eq, allEqual_iff]

/-- An exact equivalence, in both directions, of solution existence. -/
theorem exists_solution_iff :
    (∃ W : MatchingModel.WeightsN N D R, MatchingModel.EqSystemN N D W) ↔
      ∃ W : MonochromaticQuantumGraph.WeightsN N D R,
        MonochromaticQuantumGraph.EqSystemN N D W := by
  constructor
  · rintro ⟨W, hW⟩
    refine ⟨toUpstreamWeights W, (eqSystemN_iff _).mp ?_⟩
    simpa only [toLocal_toUpstream] using hW
  · rintro ⟨W, hW⟩
    exact ⟨toLocalWeights W, (eqSystemN_iff W).mpr hW⟩

end KrennAllOrders.UpstreamAdapter

#print axioms KrennAllOrders.UpstreamAdapter.toLocal_toUpstream
#print axioms KrennAllOrders.UpstreamAdapter.toUpstream_toLocal
#print axioms KrennAllOrders.UpstreamAdapter.vertices_eq
#print axioms KrennAllOrders.UpstreamAdapter.allEqual_iff
#print axioms KrennAllOrders.UpstreamAdapter.pmSumListAux_eq
#print axioms KrennAllOrders.UpstreamAdapter.pmSumN_eq
#print axioms KrennAllOrders.UpstreamAdapter.eqSystemN_iff
#print axioms KrennAllOrders.UpstreamAdapter.exists_solution_iff
