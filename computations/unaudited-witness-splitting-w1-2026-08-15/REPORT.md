# W1 — J.1/J.2 bridge probe (exactness push) — FINAL REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 26ba69f (deps sha256 in PINNED_HEAD.txt). Exact rationals;
witness verdicts are P2's decide_pair (Singular GB over Q) verbatim.
All 4,139 live-pair verdicts over Q; zero modular fallbacks, zero
undecided. 37 runs = 36 distinct shadows + gauged example.

## 1. Machinery
- STAR LINEARITY (proved; verified on 13,122 x 6 coefficients): fixing
  a site z, every matching uses exactly one z-edge, so all 729 GHZ
  equations are LINEAR in the 45 star coordinates and decouple by
  colour into three 243x15 systems. Imposition = consistency test +
  exact orthogonal projection; cycling z is a monotone exact push.
- COLOUR-SLICE CERTIFICATES: Slice(z,c) exactable iff pure row not in
  span of its mixed rows; 1,684 dependency certificates verified (279
  are O2 in linear form). 556/564 (source,site) pairs admit NO
  exactable slice; never more than one colour.
- MONOMIAL CLASS LEMMA: monomial blocks => each matching contributes
  to exactly one word; GHZ system = matching-class cancellation;
  singleton classes cannot cancel.
- Controls: W1-W10 new (4 star mutations visible; rescaling changes no
  verdict; 145,800-coefficient class-lemma check; 371 random monomial
  sources) + P2's C0-C7 re-run. All pass.

## 2. Push results (37/37)
- WITNESS-APPEARED 37/37: every shadow loses all-blockedness on the
  imposition ladder (onset after imposing 0.15%-88% of violations;
  k=1 for 8 shadows). Unconstrained stalls 99.17-99.86% satisfied,
  0/37 all-blocked, 7-11 witness pairs; 26/37 have every live pair
  witnessed. In 35/37 stalls violated-set = SINGLETON-set exactly.
- Constrained all-blocked frontier: 20.2-98.6%; 11/37 optima carry
  non-coordinate rank-one blocks. Full table: results_push.json.
- MECHANISM (hunt50010): imposing one singleton-constrained equation
  kills block A_{0,3}; support 15->14; FOUR pairs acquire witnesses
  at once. Singleton (O2) => forced block death => error degeneration
  => witness.

## 3. Extremal objects
- Sharpest coordinate shadow hunt50010: all-monomial, 716/726
  (98.62%), all 15 pairs live+blocked over Q (degrees 2/3/4), violated
  = its 10 singleton fibres EXACTLY. Exact on a full colour slice
  (site 4, colour 1) => "slice-exactness forces a witness" is FALSE.
- J.1 FALSIFIER (example_noncoordinate_all_blocked.json): 14 monomial
  blocks + one fully non-coordinate rank-one block
  A_{2,5}=(2,-1,0)^T (x) (0,2,-2), pure=(1,1,1), 707/726 (97.4%),
  all 15 pairs live and blocked over Q. Violated = its 19 singletons.
- Record all-blocked source: 717/726 = 98.76% (14 live).
- De-coordination cheap: 819/2476 (33%) single-block de-coordinations
  preserve all-blockedness; non-coordinate frontier 98.21%.

## 4. Near-exact census (232 sources, 7 families)
211 stalls reach >=95%: NONE all-blocked (2-12 witness pairs), NONE
singleton-free (1-24). All-blocked stalls survive only at 49-81% and
are rank-2/3 dominated. Blocking is generic at the bottom of the
exactness axis and dies at the top — except in the monomial regime.

## 5. Refuted / proved
- REFUTED (exact certificate): J.1 as coordinate-phrased. Blocking
  does not force coordinate structure.
- PROVED (exhaustive, 2,000,000 configurations = the entire monomial
  regime up to S6 x S3; no Groebner): MONOMIAL SIX-SITE DEATH — a
  monomial source with nonzero pures has three pairwise disjoint
  monochromatic matchings (2 orbits of 480 ordered triples); ZERO
  configurations are singleton-free. Min singletons by live edges:
  9->1, 10->2, 11->2, 12->3, 13->3, 14->5, 15->4. So the monomial
  regime satisfies at most 726 - s <= 725 mixed equations; the
  extremal object (prism graph, 725/726, violated word 002121) has
  witnesses at ALL nine live pairs.
- CORRECTED BRIDGE (the strongest honestly supported statement): the
  right invariant is the FIBRE structure, not coordinate-ness. In
  every near-exact all-blocked source found, violated = singleton
  words exactly; pushing past them kills a block and produces
  witnesses (37/37, 7/7 monomial hits, 211/211 census stalls).

## 6. Fold-in of W3 and W2
- CEILING SATURATION (key law): where violated-set = singleton-set,
  the stall is at the modulus-level ceiling 726 - #singletons for its
  support, hence OPTIMAL OVER C (W3 phase-only reduction), not just
  over Q. The all-blocked frontier saturates the ceiling exactly on 3
  shadows (hunt50010 716/716, hunt50020 696/696, hunt50024 694/694 —
  all 15 live, all coordinate); within 5 on 12; median gap 18, max
  199 (dense-defect supports — where a phase-torus search would pay;
  not run; flagged as lower bounds). On coordinate-rich supports
  BLOCKING COSTS NOTHING: the all-blocked locus reaches the support's
  exactness ceiling.
- One case (example) stalls 6 violated vs 5 singletons — only
  Q-suboptimal stall; residual fibre is phase-cancellable per W3.
- W2's B.3 REPRODUCED INDEPENDENTLY: min 4 singleton fibres at
  support 15, same 2M templates, different code path.

## 7. Soft spots
Frontier numbers are search lower bounds except where they saturate
the W3 ceiling. Full phase-torus search not implemented. The 2M
classification is exhaustive only for the monomial regime.
run_w1_falsifier.py written, not run (ground covered). Three process
pools OOM-killed earlier; all reported rows are from completed
incremental runs.

Files: w1_core.py, run_w1_{push,nearexact,slice,monomial,sharpest,
controls,falsifier}.py, analyse_w1.py, results_*.json,
example_noncoordinate_all_blocked.json, PINNED_HEAD.txt.
