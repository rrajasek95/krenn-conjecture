# W20 — the last two N=8 residuals — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD d5494d0. Exact verdicts only (floats confined to the
labelled feasibility probe); independent engine (0 mismatches vs
W19 on 39,366 word supports); full ledger discipline incl.
explicit-point controls and the zz-prefix shadowing guard. Agent's
write was policy-blocked; this transcribes its report.

## NEW GENERAL TOOLS [PROVED-HERE]
- THEOREM W20-L (site linearity): H_w = sum_s A_ts[w_t][w_s]
  C^t_s(w) with coefficients free of site t; the whole clean layer
  is three independent homogeneous LINEAR systems per site; a
  1-dimensional common kernel PROVES the site factors; each solve
  lands exactly ON the clean variety (constructs exact points).
- THEOREM W20-R (pattern-rank criterion): rank of the clean
  coefficient family at a neighbour pattern is <= deg_Gamma(t) - 1;
  regular (equality) patterns that are connected and covering force
  the site to factor.

## RESIDUAL 1 (m = 26/27/28 forcing): NOT PROVED; boxed in
- EXPLICIT exact clean points (all Gamma cells nonzero, all 2,152
  clean equations exact) where sites 0-3 do NOT factor — so NO
  fixed-site forcing argument exists (the analogue of W19's
  no-order-<=2). Cause at m=28: a real automorphism (u -> 7-u with
  global colour flip; |Aut| = 2; trivial at 24-27 and C_8).
- The criterion fires where it should (at those points the R-sites
  have all 57 patterns regular/connected/covering => proved to
  factor there).
- Hard exact search (random orders, greedy rank maximisation,
  400-step walks): NEVER reaches zero factoring sites (min 3/2/1 at
  26/27/28); at ~97% of visited factoring sites the common kernel
  is already 1-dim (provably unbreakable from there).
- Clean-set structure: IDENTICAL 2,152-word product boxes at
  26/27/28; Gamma is Pfaffian at 25..28 and C_8 (Phi = +/-Pf) —
  noted, unexploited.
- Remaining obligation, stated exactly: at every all-nonzero clean
  point some site has a connected covering regular family — a rank
  statement about hafnian-entried matrices (degree ~12 elimination
  in 144 variables; the Pfaffian frame is the suggested route).
  Downstream is certified at EVERY site, so "at least one factors"
  suffices to kill all three.

## RESIDUAL 2 (empty-clean stratum, C_8 member): MECHANISM BUILT
- L-FREE/R-FREE REDUCTION [proved, 0/4,860 mismatches]: 30 L-free
  words x 81 (and mirror) give H = per B(x,y) — 3,960 of 6,558
  mixed equations are PURE 4x4 PERMANENT conditions on the 16 cross
  blocks; the 12 single cells drop out. First structural handle on
  the stratum (W15/W16/W19 all need clean words; there are none).
- LEMMA W20-P [proved]: hyperplanes V_1..V_n (n >= 3) with
  per = 0 on their product iff all are the SAME COORDINATE
  hyperplane (exhaustive 640,000-config sweep at n=4 per ledger 12;
  false at n=2 and false without the hyperplane hypothesis —
  explicit witnesses). P4c: three hyperplanes + one all-nonzero
  vector force per != 0.
- Derived: every L-free word forces some 4x3 cross matrix to rank
  <= 2 (two dead-cell-free words force TWO); covering arithmetic:
  the minimum box cover of the 30 L-free words is exactly 9 (+9
  mirror), each box a codim->=2 coincidence in a 12-line
  arrangement. A single L-free word is provably insufficient (the
  explicit (1,1,2,2) all-nonzero solution) — the kill must use >= 2
  L-free words' FULL permanent conditions simultaneously.
- Feasibility probe (floats, evidence only): the member's signature
  is indistinguishable from the two proved-dead calibration
  templates (0.248 residual, no convergence, cells collapse) and
  clearly unlike the feasible control (8e-30).
- Verdict: NOT yet killed; conjectured dead with an explicit
  obstruction ladder.

## NEW HAZARD (ledger 17)
The generic-specialisation form of the site-linear pure-coefficient
test is VACUOUS: at a random non-solution specialisation the mixed
matrix has full column rank, so the pure row lies in the row space
trivially — the test reports a kill for EVERY template (verified on
proved-dead m=24: all 24 slots "kill"). Content only at points of
the solution variety; must be done as elimination (maximal minors),
never by specialisation.

## Controls
Engine cross-check 0 mismatches; C_8 re-audit exact; 252/252
template mutations; clean counts reproduce W19/A6; Singular guard
self-tests fire 4/4; explicit-point controls at 26/27/28 with 24/24
firing perturbations; L-free predicate exact on all 81; rank
detector planted controls; lemma controls (exhaustive sweeps,
symbolic coefficients, 3 firing mutations); probe calibrated on two
proved-dead negatives + one feasible positive.

## Soft spots
Residual-1 statement unproved (evidence = unreachable-zero search +
proved per-point criterion); clean-point construction explores one
component; residual-2 rank conditions necessary-only; probe float;
W20-P proved for hyperplanes only (the two needed cases); Pfaffian
frame unexploited; C_8 is one of 214 stratum classes (the reduction
should generalise — unchecked over the census).
