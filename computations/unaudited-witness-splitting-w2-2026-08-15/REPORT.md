# W2 — Lemma J.2 (coordinate death) — REPORT (UNAUDITED PROBE, 2026-08-15)

Pinned HEAD 26ba69f (deps re-verified at 181a4c0). Exact arithmetic
(integer HNF with transform; no floats). Scripts + JSON in this
directory. Full detail in the agent transcript. Headlines:

1. J.2 IS A THEOREM AT N<=8 IN R_cell, BY COMPLETE EXHAUSTION, with a
   sharp mechanism split: support <= 27 => literal mixed singleton
   (O2); support 28 => odd holonomy (O1). Exactly 28 no-singleton
   templates exist over all 13 colour-triple orbits (22 diagonal, 6
   off-diagonal; all share fibre census {1:1,2:38,4:1,24:1}); every
   one carries an O1 circuit. Survivors: 0. Six sites: 2,000,000
   templates exhausted, all singleton-killed at EVERY support
   (min singleton counts 1..6 by support; the support-15 column
   reproduces the committed counterexample-search note exactly).
   Multi-cell upgrades (R_mon depth 1-2 of the 28): 174,048 templates,
   all singleton-killed. Annealed band hunts: 0 zero-singleton hits.
   THE COORDINATE-REGIME COUNTEREXAMPLE HUNT IS AN EMPTINESS PROOF at
   N<=8 (R_cell), not a failed search.
2. REGIME DEFINITION FIXED: R_mon = every aggregate block a MONOMIAL
   matrix (partial injection support); R_cell = at most one cell per
   block. Gauge/relabelling/colour-closed; implied by the combined
   blocking chain (two s*kappa patterns => monomial support; + s^2 =>
   single cell — Claims C/D/E, exhaustive over all 512 supports).
   Unified kill engine: fibre(c) = PM(G_c) with +1 coefficients;
   mechanisms K0/O2a/O1/O2b/K3 in committed order over Q^* characters;
   calibrated exactly on the committed orbit-40 K_8 boundary template.
3. THE kappa_c^2 SLOT IS STRUCTURALLY VACUOUS: it blocks iff the error
   span fills W, which is generic (1,405/1,405 span-36 live pairs in
   P2's data, 0 witnesses). Hence the PLAN'S J.1 DOES NOT COMPOSE as
   stated: on the generic stratum the blocking hypothesis adds zero
   information; the content must come from exactness (P1's
   slice-dirtiness correction is the right replacement). Also:
   independent exhaustive confirmation that P2's h=2 laws ARE the h=2
   case of P1's uniform minor law.
4. THE MISSING BRIDGE, NAMED (J.1c): minor-law outputs are RANK
   conditions; J.2 consumes SUPPORT conditions. The bridge = at every
   blocked live pair, at least TWO mixed s*kappa patterns fire. At
   h=2 the bridge exists (entries = complementary 1x1 minors); at h=3
   it is open. ALTERNATIVE COUNTING ROUTE (flagged most promising,
   unwritten): the defect-budget arithmetic generalizes to
   #coordinate-R-edges >= N(7-N)/2 + |F|, saturation iff
   |F| >= N(N-4)/2 — attained at N=6 (|F|=6: WHY six sites worked),
   but = 16 at N=8: the six-site coordinatization mechanism degrades
   sharply, and a cells-vs-support counting lemma (noncoordinate
   rank-one blocks cost >= 2 cells; constant matchings consume 12)
   is the unwritten replacement.
5. PORTRAIT SHARPENED: any counterexample must be NON-MONOMIAL on some
   edge (a non-permutation rank>=2 block or a noncoordinate rank-one
   factor) — exactly the defect the slice-cover budget counts.
6. J.2's REMAINING GAP, exact: the uniform statement for N >= 10
   (= section 3 of the committed monomial-fiber-counterexample note,
   confirmed as the right target); R_mon multi-cell exhaustion at N=8;
   K3 in full quotient-ring form. The N=8 data locates the crossing:
   singletons carry every support <= 27; circuits are needed ONLY at
   full support.
7. W4 CALIBRATION WARNING: "blocking = Pluecker degeneration" is
   predicted to reduce to span = W — vacuous; W4 notified.
8. Soft spots honestly listed (N<=8 only; R_mon probed not exhausted;
   conservative Z-span engine; the general-N budget formula needs
   re-derivation).
