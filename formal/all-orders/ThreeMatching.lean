/-
Copyright (c) 2026 Rishi. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/

import Mathlib.Combinatorics.SimpleGraph.Matching

/-!
# Matching switches and the combinatorial closure of the Krenn--Gu argument

A perfect matching is represented by its fixed-point-free partner involution.
The constructions below are explicitly related to mathlib's
`SimpleGraph.Subgraph.IsPerfectMatching`. A receiving colour word is realized
only when both endpoints of each chosen edge receive its colour.

This file proves structural steps of the final graph argument, including
uniqueness for a fixed colour word and switching on a closed vertex set. It
does not assume the three-matching obstruction as an axiom.
-/

set_option autoImplicit false

namespace KrennAllOrders.ThreeMatching

open scoped Classical

variable {V C : Type*}

/-- A perfect matching, represented by its unique partner at each vertex. -/
@[ext]
structure Matching (V : Type*) where
  partner : V → V
  partner_partner : ∀ v, partner (partner v) = v
  partner_ne_self : ∀ v, partner v ≠ v

namespace Matching

theorem partner_injective (M : Matching V) : Function.Injective M.partner :=
  Function.Involutive.injective M.partner_partner

/-- The simple graph consisting of the edges of a partner matching. -/
def toGraph (M : Matching V) : SimpleGraph V where
  Adj v w := M.partner v = w
  symm := ⟨fun v w h => by rw [← h, M.partner_partner]⟩
  loopless := ⟨M.partner_ne_self⟩

@[simp]
theorem toGraph_adj (M : Matching V) (v w : V) :
    M.toGraph.Adj v w ↔ M.partner v = w := Iff.rfl

/-- The same matching as a spanning subgraph of any graph containing its edges. -/
def toSubgraph (M : Matching V) (G : SimpleGraph V)
    (hG : ∀ v, G.Adj v (M.partner v)) : G.Subgraph where
  verts := Set.univ
  Adj v w := M.partner v = w
  adj_sub := by
    intro v w h
    simpa only [h] using hG v
  edge_vert := fun _ => Set.mem_univ _
  symm := ⟨fun v w h => by rw [← h, M.partner_partner]⟩

theorem toSubgraph_isPerfectMatching (M : Matching V) (G : SimpleGraph V)
    (hG : ∀ v, G.Adj v (M.partner v)) :
    (M.toSubgraph G hG).IsPerfectMatching := by
  rw [SimpleGraph.Subgraph.isPerfectMatching_iff]
  intro v
  exact ⟨M.partner v, rfl, fun w h => (show M.partner v = w from h).symm⟩

/-- The partner representation has the usual parity consequence for finite vertex sets. -/
theorem even_card [Fintype V] (M : Matching V) : Even (Fintype.card V) :=
  (M.toSubgraph_isPerfectMatching M.toGraph (fun _ => rfl)).even_card

/-- Conversely, a mathlib perfect matching has a unique partner involution. -/
noncomputable def ofSubgraph {G : SimpleGraph V} (M : G.Subgraph)
    (hM : M.IsPerfectMatching) : Matching V where
  partner v := (SimpleGraph.Subgraph.isPerfectMatching_iff.mp hM v).choose
  partner_partner v := by
    let h := SimpleGraph.Subgraph.isPerfectMatching_iff.mp hM
    exact ((h ((h v).choose)).choose_spec.2 v (h v).choose_spec.1.symm).symm
  partner_ne_self v := by
    intro heq
    have hadj := (SimpleGraph.Subgraph.isPerfectMatching_iff.mp hM v).choose_spec.1
    rw [heq] at hadj
    exact G.irrefl (M.adj_sub hadj)

theorem ofSubgraph_partner_adj {G : SimpleGraph V} (M : G.Subgraph)
    (hM : M.IsPerfectMatching) (v : V) :
    M.Adj v ((ofSubgraph M hM).partner v) :=
  (SimpleGraph.Subgraph.isPerfectMatching_iff.mp hM v).choose_spec.1

theorem ofSubgraph_partner_eq_iff {G : SimpleGraph V} (M : G.Subgraph)
    (hM : M.IsPerfectMatching) (v w : V) :
    (ofSubgraph M hM).partner v = w ↔ M.Adj v w := by
  constructor
  · intro h
    simpa only [h] using ofSubgraph_partner_adj M hM v
  · intro h
    exact ((SimpleGraph.Subgraph.isPerfectMatching_iff.mp hM v).choose_spec.2 w h).symm

/-- A set is closed under a matching if every partner of a vertex in the set is in it. -/
def Closed (M : Matching V) (S : Set V) : Prop :=
  ∀ ⦃v⦄, v ∈ S → M.partner v ∈ S

theorem Closed.partner_mem_iff {M : Matching V} {S : Set V} (hS : M.Closed S)
    (v : V) : M.partner v ∈ S ↔ v ∈ S := by
  constructor
  · intro hv
    simpa only [M.partner_partner] using hS hv
  · exact fun hv => hS hv

/-- Use `F` inside a common closed set and `G` outside it. -/
noncomputable def switch (F G : Matching V) (S : Set V)
    (hF : F.Closed S) (hG : G.Closed S) : Matching V := by
  classical
  exact {
    partner := fun v => if v ∈ S then F.partner v else G.partner v
    partner_partner := fun v => by
      by_cases hv : v ∈ S
      · simp only [if_pos hv, if_pos (hF hv), F.partner_partner]
      · have hgv : G.partner v ∉ S := fun h => hv ((hG.partner_mem_iff v).mp h)
        simp only [if_neg hv, if_neg hgv, G.partner_partner]
    partner_ne_self := fun v => by
      by_cases hv : v ∈ S
      · simpa only [if_pos hv] using F.partner_ne_self v
      · simpa only [if_neg hv] using G.partner_ne_self v }

theorem switch_partner (F G : Matching V) (S : Set V)
    (hF : F.Closed S) (hG : G.Closed S) (v : V) :
    (switch F G S hF hG).partner v = if v ∈ S then F.partner v else G.partner v := by
  classical
  rfl

theorem closed_pair (M : Matching V) (v : V) : M.Closed {v, M.partner v} := by
  intro w hw
  rcases hw with rfl | hw
  · exact Set.mem_insert_of_mem _ (Set.mem_singleton _)
  · rw [Set.mem_singleton_iff] at hw
    rw [hw, M.partner_partner]
    exact Set.mem_insert _ _

end Matching

/-- A matching realizes a colour word when every chosen edge has that colour at both ends. -/
def Realizes (colours : C → Matching V) (word : V → C) (M : Matching V) : Prop :=
  ∀ v, M.partner v = (colours (word v)).partner v ∧ word (M.partner v) = word v

/-- A mixed perfect matching includes two vertices receiving different colours. -/
def HasMixedMatching (colours : C → Matching V) : Prop :=
  ∃ (M : Matching V) (word : V → C), Realizes colours word M ∧
    ∃ v w, word v ≠ word w

/-- Degree-one support in each colour prevents two distinct matchings realizing the same word. -/
theorem realizes_unique {colours : C → Matching V} {word : V → C}
    {M N : Matching V} (hM : Realizes colours word M) (hN : Realizes colours word N) :
    M = N := by
  apply Matching.ext
  funext v
  exact (hM v).1.trans (hN v).1.symm

/-- The closed-set switch realizes the word selecting its two component colours. -/
theorem realizes_switch (colours : C → Matching V) (a b : C) (S : Set V)
    (ha : (colours a).Closed S) (hb : (colours b).Closed S) :
    Realizes colours (fun v => if v ∈ S then a else b)
      (Matching.switch (colours a) (colours b) S ha hb) := by
  classical
  intro v
  by_cases hv : v ∈ S
  · simp only [Matching.switch_partner, if_pos hv, if_pos (ha hv)]
    trivial
  · have hgv : (colours b).partner v ∉ S := fun h => hv ((hb.partner_mem_iff v).mp h)
    simp only [Matching.switch_partner, if_neg hv, if_neg hgv]
    trivial

/-- A proper nonempty common closed set gives a mixed matching by switching colours. -/
theorem hasMixedMatching_of_closed_cut (colours : C → Matching V) {a b : C}
    (hab : a ≠ b) (S : Set V) (ha : (colours a).Closed S) (hb : (colours b).Closed S)
    (hin : S.Nonempty) (hout : Sᶜ.Nonempty) : HasMixedMatching colours := by
  classical
  refine ⟨Matching.switch (colours a) (colours b) S ha hb,
    fun v => if v ∈ S then a else b, realizes_switch colours a b S ha hb, ?_⟩
  obtain ⟨v, hv⟩ := hin
  obtain ⟨w, hw⟩ := hout
  refine ⟨v, w, ?_⟩
  simpa only [if_pos hv, if_neg hw] using hab

/-- A shared physical edge can be coloured one way, with the other matching used elsewhere. -/
theorem hasMixedMatching_of_shared_edge (colours : C → Matching V) {a b : C}
    (hab : a ≠ b) {p q r : V}
    (ha : (colours a).partner p = q) (hb : (colours b).partner p = q)
    (hrp : r ≠ p) (hrq : r ≠ q) : HasMixedMatching colours := by
  have hca : (colours a).Closed ({p, q} : Set V) := by
    simpa only [ha] using (colours a).closed_pair p
  have hcb : (colours b).Closed ({p, q} : Set V) := by
    simpa only [hb] using (colours b).closed_pair p
  apply hasMixedMatching_of_closed_cut colours hab {p, q} hca hcb
  · exact ⟨p, Set.mem_insert _ _⟩
  · exact ⟨r, by simp only [Set.mem_compl_iff, Set.mem_insert_iff,
      Set.mem_singleton_iff, not_or]; exact ⟨hrp, hrq⟩⟩

/-- The union of two colour matchings. -/
def pairGraph (colours : C → Matching V) (a b : C) : SimpleGraph V :=
  (colours a).toGraph ⊔ (colours b).toGraph

/-- A non-backtracking step after an edge of the first matching must use the second.

Applied repeatedly to a cycle, this is its two-colour alternation property. -/
theorem pairGraph_other_step (colours : C → Matching V) {a b : C} {v w z : V}
    (hfirst : (colours a).partner v = w) (hnext : (pairGraph colours a b).Adj w z)
    (hback : z ≠ v) : (colours b).partner w = z := by
  change (colours a).partner w = z ∨ (colours b).partner w = z at hnext
  rcases hnext with ha | hb
  · have hreturn : (colours a).partner w = v := by
      rw [← hfirst, (colours a).partner_partner]
    exact False.elim (hback (ha.symm.trans hreturn))
  · exact hb

/-- Every union component is closed under its first matching. -/
theorem pairGraph_reachable_closed_left (colours : C → Matching V) (a b : C) (p : V) :
    (colours a).Closed {v | (pairGraph colours a b).Reachable p v} := by
  intro v hv
  exact hv.trans (SimpleGraph.Adj.reachable (show (pairGraph colours a b).Adj v
    ((colours a).partner v) from Or.inl rfl))

/-- Every union component is closed under its second matching. -/
theorem pairGraph_reachable_closed_right (colours : C → Matching V) (a b : C) (p : V) :
    (colours b).Closed {v | (pairGraph colours a b).Reachable p v} := by
  intro v hv
  exact hv.trans (SimpleGraph.Adj.reachable (show (pairGraph colours a b).Adj v
    ((colours b).partner v) from Or.inr rfl))

/-- If two colour matchings have more than one union component, switching one gives a mixed word. -/
theorem hasMixedMatching_of_not_reachable (colours : C → Matching V) {a b : C}
    (hab : a ≠ b) {p q : V} (hpq : ¬(pairGraph colours a b).Reachable p q) :
    HasMixedMatching colours := by
  apply hasMixedMatching_of_closed_cut colours hab
    {v | (pairGraph colours a b).Reachable p v}
    (pairGraph_reachable_closed_left colours a b p)
    (pairGraph_reachable_closed_right colours a b p)
  · exact ⟨p, SimpleGraph.Reachable.refl p⟩
  · exact ⟨q, hpq⟩

/-- Consequently, absence of mixed matchings forces every two-colour union to be connected. -/
theorem pairGraph_preconnected_of_no_mixed (colours : C → Matching V) {a b : C}
    (hab : a ≠ b) (hno : ¬HasMixedMatching colours) :
    (pairGraph colours a b).Preconnected := by
  intro p q
  by_contra hpq
  exact hno (hasMixedMatching_of_not_reachable colours hab hpq)

/-- On more than two vertices, any edge shared by distinct colours gives a mixed matching. -/
theorem hasMixedMatching_of_shared_partner [Fintype V] (colours : C → Matching V)
    (hcard : 2 < Fintype.card V) {a b : C} (hab : a ≠ b) (p : V)
    (hshare : (colours a).partner p = (colours b).partner p) :
    HasMixedMatching colours := by
  classical
  have hex : ∃ r, r ≠ p ∧ r ≠ (colours a).partner p := by
    by_contra h
    have hsub : (Finset.univ : Finset V) ⊆ {p, (colours a).partner p} := by
      intro r _
      by_cases hrp : r = p
      · simp only [hrp, Finset.mem_insert, true_or]
      · have hrq : r = (colours a).partner p := by
          by_contra hrq
          exact h ⟨r, hrp, hrq⟩
        simp only [hrq, Finset.mem_insert, Finset.mem_singleton, or_true]
    have hle := Finset.card_le_card hsub
    rw [Finset.card_univ, Finset.card_pair ((colours a).partner_ne_self p).symm] at hle
    exact (Nat.not_le_of_lt hcard) hle
  obtain ⟨r, hrp, hrq⟩ := hex
  exact hasMixedMatching_of_shared_edge colours hab rfl hshare.symm hrp hrq

/-- Thus distinct colours have distinct partners at every vertex when there is no mixed matching. -/
theorem colour_partner_injective_of_no_mixed [Fintype V] (colours : C → Matching V)
    (hcard : 2 < Fintype.card V) (hno : ¬HasMixedMatching colours) (p : V) :
    Function.Injective (fun a => (colours a).partner p) := by
  intro a b hshare
  by_contra hab
  exact hno (hasMixedMatching_of_shared_partner colours hcard hab p hshare)

/-- The union of two edge-disjoint matchings has degree two at every vertex. -/
theorem pairGraph_isCycles (colours : C → Matching V) {a b : C}
    (hdisjoint : ∀ v, (colours a).partner v ≠ (colours b).partner v) :
    (pairGraph colours a b).IsCycles := by
  intro v _
  have hs : (pairGraph colours a b).neighborSet v =
      {(colours a).partner v, (colours b).partner v} := by
    ext w
    simp only [SimpleGraph.mem_neighborSet, pairGraph, SimpleGraph.sup_adj,
      Matching.toGraph_adj, Set.mem_insert_iff, Set.mem_singleton_iff, eq_comm]
  rw [hs]
  exact Set.ncard_pair (hdisjoint v)

/-- If no mixed matching exists, every two-colour union is a single spanning cycle.

This is the Hamilton-cycle reduction in the final graph proof, not the remaining
chord/parity obstruction involving the third matching. -/
theorem exists_spanning_cycle_of_no_mixed [Fintype V] (colours : C → Matching V)
    (hcard : 2 < Fintype.card V) (hno : ¬HasMixedMatching colours) {a b : C}
    (hab : a ≠ b) (p : V) :
    ∃ walk : (pairGraph colours a b).Walk p p,
      walk.IsCycle ∧ ∀ v, v ∈ walk.support := by
  have hconnected := pairGraph_preconnected_of_no_mixed colours hab hno
  have hdisjoint : ∀ v, (colours a).partner v ≠ (colours b).partner v := by
    intro v h
    exact hab (colour_partner_injective_of_no_mixed colours hcard hno v h)
  have hcycles := pairGraph_isCycles colours hdisjoint
  let component := (pairGraph colours a b).connectedComponentMk p
  have hp : p ∈ component.supp := by
    rw [SimpleGraph.ConnectedComponent.mem_supp_iff]
  have hn : ((pairGraph colours a b).neighborSet p).Nonempty :=
    ⟨(colours a).partner p, Or.inl rfl⟩
  obtain ⟨walk, hcycle, hverts⟩ :=
    hcycles.exists_cycle_toSubgraph_verts_eq_connectedComponentSupp hp hn
  refine ⟨walk, hcycle, fun v => ?_⟩
  rw [← walk.mem_verts_toSubgraph, hverts,
    SimpleGraph.ConnectedComponent.mem_supp_iff,
    SimpleGraph.ConnectedComponent.eq]
  exact hconnected v p

end KrennAllOrders.ThreeMatching
