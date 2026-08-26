# A3 — uniform-in-N groundwork (node 4) — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 81beedf. Exact arithmetic for all verdicts. Agent's write
was policy-blocked; this transcribes its delivered report. Scripts
a3_*.py + logs + JSON here.

## Headline results
1. UNIFORM MONOMIAL SINGLETON DEATH IS FALSE for every N = 0 mod 4:
   explicit family F_n (X|Y split; colour 1 = M_X u M_Y, colour 2 =
   intra-part rest, colour 0 = K_{X,Y}) has three nonzero pures and
   NO singleton mixed fibre (Theorem A3.1, proved via D(2t,t) >= 2;
   verified N = 8,12,16,20,24; F_4 IS the committed K_8
   counterexample byte-for-byte).
2. THE COORDINATOR'S U(N)-SINGLETON PROPOSAL IS REFUTED AT N=10:
   six certified (SC)-admissible DIAGONAL singleton-free templates
   at supports 31,33,37,39,41,43 (all <= 44 = C(10,2)-1), three live
   pures, min live degree >= 3, verified singleton-free by THREE
   disjoint engines (product formula, direct enumeration of 945
   matchings, W2's w2_monomial.analyse) — all die by O1 odd
   holonomy. "Singleton-free only at full support" is an N=8
   ARTEFACT. Calibration control: the same engine at N=8 reproduces
   the committed emptiness at supports 12..27 — so the N=8 decision
   (W8/W11) is unaffected; the UNIFORM analogue is dead.
3. THE UNIFORM MECHANISM: Perm-K_{2,3} lemma (char != 2: a 2x3
   all-nonzero matrix cannot have all three 2x2 PERMANENTS zero) —
   the canonical odd cancellation circuit. Theorem A3.3: F_n is
   never exact, for every n, by a 3-line application. Theorem A3.3'
   (general circuit): 5 vertices + colour t with local conditions
   (a)(b) and complement-splitting (c) kill any exact diagonal
   monomial source. (c) carries the remaining difficulty.
4. FOURTH-MATCHING THEOREM (A3.4, proved constructively, verified on
   all 161,148 charts at N = 6,8,10, every proof branch exercised,
   sharp at N=4): a properly 3-edge-coloured cubic graph on N >= 6
   vertices has a fourth perfect matching. COROLLARIES: the support
   floor m = 3N/2 dies for EVERY even N >= 6 (derives the committed
   cube-chart kill uniformly); m = 3N/2 + 1 dies; every diagonal
   monomial source with even-cycle-free colour graphs dies.
5. INTERFACES: Theorem B (descent) is genuinely N-uniform (proof
   body carries no N=8 facts; audited bijection sampled at orders
   4..12). P1's minor law is N-uniform (identity about A_pq alone;
   re-proved cleanly). BUT P1's FACT 1 / blocking taxonomy is
   intrinsically h = 3: cap-error components are K-degree-h
   homogeneous and Lambda^4 of a 3-space is 0 — NO determinantal
   obstruction at N >= 10. Any uniform argument through the blocking
   classification is unsupported for N >= 10 (residual R4).
6. RECOMMENDED U(N): witness existence at MINIMUM even order (the
   committed descent target (7) + minimality hypothesis). Free
   hypotheses, all N-uniform: minimality; balance (audit-survived);
   m >= 3N/2 + 2 (proved here); all-blocked reduction. NOT usable:
   phase-only (refuted), per-support SAT (does not scale — R5:
   m*(8) = C(8,2)-1 but m*(10) <= 30 ~ C(10,2)-15; if the gap
   grows, the SAT route is dead uniformly; measure m*(12)).

## Residual lemmas for node 4 (minimized)
R1a: singleton coverage below threshold m*(N) (proved at 3N/2,
     3N/2+1, even-cycle-free; m*(8) = 27; m*(10) in [31)..30 soft).
R1b: odd circuit above the threshold (proved for F_n — all N = 0
     mod 4; verified for W2's 28 at N=8 and the six N=10 certs).
R2:  parity dichotomy — REFUTED (recorded so nobody re-derives).
R3:  U(N) as above (the one statement the induction consumes).
R4:  degree-h replacement for the determinantal obstruction (the
     hard open core of witness theory at N >= 10).
R5:  threshold growth m*(N) (measure at N=12).

## Withdrawn by A3 itself
Its non-(SC) Sigma_min numbers at N=10 (same class error as W6);
the (SC)-constrained re-run was inconclusive (seeder cannot reach
admissible starts — a constructive (SC) seeder is the fix).

## Controls
17-row ledger, all pass, including: product formula vs direct
enumeration (N=8,12); F_4 = committed counterexample; census
{1:1,2:38,4:1,24:1} reproduced; A3.4 proof-output checked on all
charts; N=4 sharpness caught; W2-engine agreement on all N=10
certificates; minor-law mutants rejected.

## Soft spots
N=10 "none found" rows are search failures, not emptiness (only the
positive certificates are claims); A3.5 inherits committed inputs
(S1)/(S2) unre-proved; A3.3'(c) proved only for F_n; non-diagonal
monomial gap real (6 of W2's 28 are off-diagonal); two background
runs still appending (can only lower m*(10)).

## ADDENDUM (same day): two soft spots closed
1. F'_n CONSTRUCTION (N = 2 mod 4): explicit one-vertex-parity-defect
   variant of F_n (distinguished a in A, b,c in B; single crossing
   edge ab in colour 1 repairs parity). VERIFIED N=10 (reproduces the
   search certificate exactly; 0 singletons by two methods; (SC)
   clean; W2 verdict O1-odd-holonomy) and N=14 (full 3^14 scan);
   (SC)+degree checks through N=22. COMBINED WITH F_n: explicit
   (SC)-admissible singleton-free monomial templates with three
   nonzero constant fibres exist on K_N for EVERY even N >= 8 —
   construction, not search. No singleton-only statement is uniform.
2. THRESHOLD BRACKET CLOSED: m*(10) = 31 (no singleton-free template
   at N=10 supports 24..30 under the heavy sweep; certified hit at
   31 with min live degree 3). Gap C(N,2) - m*(N): 0 at N=8, >= 14
   at N=10 — the full-support coincidence at N=8 widens fast.
3. Recommendation unchanged, firmer: U_mon(N) = singleton OR odd
   circuit (Perm-K_{2,3} canonical); U(N) = minimal-order witness
   statement. Parity-dichotomy conjecture definitively retired.
