# UNAUDITED STRESS TEST — spanning-tree flip-graph homotopy (2026-08-13)

Pinned HEAD 6426204 (constructors byte-identical to repair probe 1's pin).
Exact arithmetic. Scripts + JSON in this directory. UNAUDITED.

## One-line verdict

The tree contraction exists and is exact — but vacuously: monomial-ratio
edge weights TELESCOPE, so transport is path-independent and the canonical
construction reduces to the endpoint difference (K_tree ≡ K_phys, pinning
nothing). Every non-telescoping reading is non-canonical and its tree
differences EXIT the 7-dim freedom through shadow_2. And the obstruction
the strategy targeted is provably NOT on the flip graph.

## Key facts

- T1 (K6): corrected identity dH+Hd = 1 − P_root − P_cycle (tree retracts
  onto root ⊔ 31 circles). Exponent holonomy trivial on all 31 fundamental
  cycles BY CONSTRUCTION (ratios telescope). Provenance carried, empty.
- T2: "balanced ⟺ tree-independent" CONFIRMED (9 trees). Localization
  REFUTED: one negative 3-cycle changes 13/15 vertices (global switching-
  class effect). MAIN CLAIM REFUTED AS STATED: a colouring fibre yields at
  most ONE forced relation (measured max = 1), so no single fibre's flip
  graph carries a sign cycle — every O1 needs ≥ 2 colourings. The flip
  graph is fibrewise; the obstruction is cross-fibre, living on the CELL
  graph (colour-changing), where Zaslavsky machinery already sits.
- T3 (K8): 90-row support = exactly the {3,6}-avoiding matchings
  (connected 11-regular flip graph); all 90 Weyl edge signs +1; probe 1's
  7-dim freedom independently REPRODUCED. Telescoping variants: canonical,
  in-freedom, signature-matching — and identically K_phys (tautology).
  Alternating variant: 4/9 trees disagree; difference span dim 3, NOT in
  the freedom; smallest exit = 2·(1−s)(w−1)[M'] for the path's interior
  vertex M' = {06,17,23,45} — exits through shadow_2 itself.
- T4: controls pass; two informative non-breaks: the additive identity is
  path-blind (any connected routing satisfies it — identity alone cannot
  pin a tree), and the root + interior path signs are inert in K_tree.

## Reusable positives

1. The flip 2-COMPLEX is simply connected (H_1 = 0 after filling the 15
   triangles + 90 chordless squares, K6). The right home for a
   combinatorial homotopy is the 2-complex, not the 1-skeleton. Next
   cheap computation: H_1 of the signed/constrained 2-complex at N=8.
2. Cell-graph gauge fixing IS well posed (spanning tree there = gauge
   fixing; residual = frame lattice; sign character tree-independent,
   verified 9 trees on the 3P2 chart) — but where it is well defined the
   support is UNobstructed; where you need H_w, no lift exists.
3. AUDIT FLAG for the holonomy programme: the committed 3P2 chart of
   generalized-laurent-elimination.md §2 dies by O2 (470 kills, 0 O1)
   under full two-term + minor + Laurent-merge seeding, though the note
   presents it as O1. Mechanism labels may be BASIS-DEPENDENT; the
   programme note's O1/O2 census counts should be rechecked under a
   canonical basis convention.
