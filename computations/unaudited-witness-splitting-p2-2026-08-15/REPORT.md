# P2 six-site calibration — REPORT (UNAUDITED PROBE, 2026-08-15)

Pinned HEAD 86a9479 (re-verified against a9dbf95: no dependency moved).
Exact arithmetic (Fraction + Singular GB over Q; modular fallbacks
flagged per pair). Full detail in the agent transcript; scripts and
JSON results in this directory. Headline findings:

1. PLAN FALSIFIED AS CALIBRATED: "(S)-everywhere is impossible" is
   wrong at six sites — it is GENERIC. Generic sources have NO
   clean-cap witness at ANY pair (750/750 generic pairs blocked); the
   h=3 appendix shows the same at a generic N=8 pair (kappa_c^3 lies
   in the degree-3 error span; exact certificate).
2. DICHOTOMY CORRECTED: E_pq is TENSOR-valued (81 quadrics at h=2;
   729 cubics at h=3). The right criterion is ideal-theoretic:
   no witness at a live pair <=> some monomial in L={s,k0,k1,k2} (ANY
   degree) lies in the error ideal. Degree-h splitting patterns are
   sound certificates but incomplete: minimal blocking degrees 2,3,4,5
   all occur; an explicit all-blocked source exists where the degree-2
   pattern list wrongly calls 13 of 15 pairs witness-carrying
   (example_all_blocked.json).
3. STRUCTURE (h=2, exhaustive): error components always lie in
   W = Sym^2 x Sym^2 (annihilator of the 2x2 minors of K; dim 36),
   and generically span it. Pattern classification: kappa_c*kappa_c'
   (c != c') NEVER blocks; s^2 forces rank A_pq <= 1; s*kappa_c forces
   row-c/column-c support; kappa_c^2 is UNCONDITIONAL. Frequencies on
   3,019 blocked live pairs match exactly.
4. GEOGRAPHY INVERTED: witness existence correlates NOT with density
   but with NON-COORDINATE rank-one factors. Generic rank-one census
   strata: witnesses nearly everywhere (3,077/3,420). Anchored
   COORDINATE blocks (what slice-cover + the defect budget force):
   blocking dominant; 19/128 instances fully blocked. The dense-defect
   end (|F|=6) is where blocking is STRONGEST.
5. PURE EQUATIONS ARE A GAUGE: any source with nonzero pure
   coefficients gauge-normalizes to pure = 1 with every pair's
   witness/blocking status unchanged (verified 75/75). ALL witness
   forcing must come from the mixed equations.
6. SHADOWS ABOUND: 42/48 hill-climbs reached all-live-pairs-blocked
   (36 pure-normalizable), across 15 of 19 strata. The only thing
   separating these from a counterexample is the mixed system.
7. K_4 LANDING CONTROL: the N=6 -> N=4 descent fires on constructible
   data and lands exactly on Delta_{4,3} (the K_4 exception),
   producing no contradiction — as the architecture predicts.
8. Soft spots stated: 4/3,420 undecided pairs (timeouts), some
   modular-only verdicts (flagged; 25/25 sampled agree over Q), no
   witness flips in the C5 mutation family (caught by span changes).

CONSEQUENCE FOR THE PLAN: Lemma I.3 cannot be generic/polyhedral; the
witness must be conjured from exactness. Revised route in the plan
note (v2): blocking-everywhere forces coordinate/monomial structure
(J.1), and coordinate/monomial exact structure dies by the O2/census
mechanisms (J.2) — the crux dichotomy quantified on the coordinate
axis, with the 36 shadows as the test fleet.
