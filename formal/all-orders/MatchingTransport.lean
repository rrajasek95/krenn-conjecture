/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import ThreeMatching

/-! # Transporting matchings and recovering their receiving colour words -/

namespace KrennAllOrders.ThreeMatching

variable {V W C : Type*}

/-- Relabel vertices of a matching through a bijection. -/
def Matching.map (M : Matching V) (e : V ≃ W) : Matching W where
  partner w := e (M.partner (e.symm w))
  partner_partner w := by simp only [Equiv.symm_apply_apply, M.partner_partner, Equiv.apply_symm_apply]
  partner_ne_self w := by
    intro h
    have : M.partner (e.symm w) = e.symm w := by simpa using congrArg e.symm h
    exact M.partner_ne_self _ this

@[simp] theorem Matching.map_partner (M : Matching V) (e : V ≃ W) (v : V) :
    (M.map e).partner (e v) = e (M.partner v) := by
  simp only [Matching.map, Equiv.symm_apply_apply]

theorem Realizes.map {colours : C → Matching V} {word : V → C} {M : Matching V}
    (h : Realizes colours word M) (e : V ≃ W) :
    Realizes (fun c => (colours c).map e) (word ∘ e.symm) (M.map e) := by
  intro w
  obtain ⟨v, rfl⟩ := e.surjective w
  simpa only [Function.comp_apply, Equiv.symm_apply_apply, Matching.map_partner] using
    And.intro (congrArg e (h v).1) (h v).2

theorem HasMixedMatching.map {colours : C → Matching V}
    (h : HasMixedMatching colours) (e : V ≃ W) :
    HasMixedMatching (fun c => (colours c).map e) := by
  obtain ⟨M, word, hreal, v, w, hne⟩ := h
  refine ⟨M.map e, word ∘ e.symm, hreal.map e, e v, e w, ?_⟩
  simpa only [Function.comp_apply, Equiv.symm_apply_apply] using hne

/-- A matching assembled from edge-disjoint colour matchings has a consistent receiving word. -/
theorem exists_realizes_of_partner_cover (colours : C → Matching V) (M : Matching V)
    (hdisjoint : ∀ v, Function.Injective (fun c => (colours c).partner v))
    (hcover : ∀ v, ∃ c, M.partner v = (colours c).partner v) :
    ∃ word : V → C, Realizes colours word M := by
  classical
  choose word hword using hcover
  refine ⟨word, fun v => ⟨hword v, ?_⟩⟩
  apply hdisjoint (M.partner v)
  change (colours (word (M.partner v))).partner (M.partner v) =
    (colours (word v)).partner (M.partner v)
  rw [← hword (M.partner v), M.partner_partner]
  rw [hword v, (colours (word v)).partner_partner]

/-- Two differently coloured edges in such an assembled matching certify a mixed word. -/
theorem hasMixedMatching_of_partner_cover (colours : C → Matching V) (M : Matching V)
    (hdisjoint : ∀ v, Function.Injective (fun c => (colours c).partner v))
    (hcover : ∀ v, ∃ c, M.partner v = (colours c).partner v)
    {a b : C} (hab : a ≠ b) {v w : V}
    (ha : M.partner v = (colours a).partner v)
    (hb : M.partner w = (colours b).partner w) :
    HasMixedMatching colours := by
  obtain ⟨word, hreal⟩ := exists_realizes_of_partner_cover colours M hdisjoint hcover
  have hva : word v = a := hdisjoint v ((hreal v).1.symm.trans ha)
  have hwb : word w = b := hdisjoint w ((hreal w).1.symm.trans hb)
  refine ⟨M, word, hreal, v, w, ?_⟩
  simpa only [hva, hwb] using hab

end KrennAllOrders.ThreeMatching
