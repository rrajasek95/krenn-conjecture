/-
Copyright (c) 2026 Rishi. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/

import ThreeMatching

/-!
# Axiom audit for the proved matching-switch and Hamilton-cycle reduction lemmas

This file checks the compiled structural results; it does not assert that the
remaining three-matching chord obstruction has been formalized.
-/

#print axioms KrennAllOrders.ThreeMatching.Matching.partner_injective
#print axioms KrennAllOrders.ThreeMatching.Matching.toGraph_adj
#print axioms KrennAllOrders.ThreeMatching.Matching.toSubgraph_isPerfectMatching
#print axioms KrennAllOrders.ThreeMatching.Matching.even_card
#print axioms KrennAllOrders.ThreeMatching.Matching.ofSubgraph_partner_adj
#print axioms KrennAllOrders.ThreeMatching.Matching.ofSubgraph_partner_eq_iff
#print axioms KrennAllOrders.ThreeMatching.Matching.Closed.partner_mem_iff
#print axioms KrennAllOrders.ThreeMatching.Matching.switch_partner
#print axioms KrennAllOrders.ThreeMatching.Matching.closed_pair
#print axioms KrennAllOrders.ThreeMatching.realizes_unique
#print axioms KrennAllOrders.ThreeMatching.realizes_switch
#print axioms KrennAllOrders.ThreeMatching.hasMixedMatching_of_closed_cut
#print axioms KrennAllOrders.ThreeMatching.hasMixedMatching_of_shared_edge
#print axioms KrennAllOrders.ThreeMatching.pairGraph_other_step
#print axioms KrennAllOrders.ThreeMatching.pairGraph_reachable_closed_left
#print axioms KrennAllOrders.ThreeMatching.pairGraph_reachable_closed_right
#print axioms KrennAllOrders.ThreeMatching.hasMixedMatching_of_not_reachable
#print axioms KrennAllOrders.ThreeMatching.pairGraph_preconnected_of_no_mixed
#print axioms KrennAllOrders.ThreeMatching.hasMixedMatching_of_shared_partner
#print axioms KrennAllOrders.ThreeMatching.colour_partner_injective_of_no_mixed
#print axioms KrennAllOrders.ThreeMatching.pairGraph_isCycles
#print axioms KrennAllOrders.ThreeMatching.exists_spanning_cycle_of_no_mixed

-- Constructors with proof fields, and the generated structure extensionality lemma.
#print axioms KrennAllOrders.ThreeMatching.Matching.toGraph
#print axioms KrennAllOrders.ThreeMatching.Matching.toSubgraph
#print axioms KrennAllOrders.ThreeMatching.Matching.ofSubgraph
#print axioms KrennAllOrders.ThreeMatching.Matching.switch
#print axioms KrennAllOrders.ThreeMatching.Matching.ext
