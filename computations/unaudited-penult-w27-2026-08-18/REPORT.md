# W27 — the penultimate rung + the skeleton law — REPORT (UNAUDITED, 2026-08-18)

Pinned HEAD 77efbe3. All-exact (Fraction / Singular Rabinowitsch;
mod-p only as a screen with exact re-checks). Control manifests 9/9.
Agent's write was policy-blocked; this transcribes its report.
Checkpoints: results_SUMMARY.json + 11 per-task JSONs.

## HEADLINE
1. X_5 = EXACT at N=8 (W27-P1: the only profile above off-count 4
   is (3,3,2)); hence EXACT ⊆ X_4 and **X_4 = ∅ at N=8 would PROVE
   Krenn–Gu at N=8**. On the monochrome-diagonal stratum X_4 =
   EXACT already (W27-D2: (3,3,2) has two odd parts) — so the
   diagonal cannot calibrate X_4; it can only prove the diagonal
   case, which W27 does (below).
2. NO X_4 POINT AT N=8 BUILT from ~4,300 backgrounds across
   fourteen structured families incl. an exhaustive stratum and the
   colour-symmetric slice. THE PROBE IS CALIBRATED: fires 40/40 at
   (6,3) and 25/25 at (8,3) (known nonempty), silent at (6,4)
   (known empty) — and **(8,4) has the signature of (6,4), not
   (8,3)**. [CONJECTURED: X_4 = ∅ at N=8.]
3. THE N=6 SKELETON WITNESS LAW IDENTIFIED AND EXACT (W27-S1):
   witness <=> some endpoint c1-simple (d_{c1} = 1) OR both
   endpoints almost-clean — separates all 279 live pairs of all 24
   classes, no exception; strictly sharper than W25-U3 (covers 194
   + 18 vs 138). N=6-ONLY (63/377 wrong at N=8, 12 mixed cells) —
   but the PHENOMENON survives at N=8 (W27-S3: witness set constant
   across weight points, 6/6 skeletons) — a non-local skeleton
   invariant exists, unidentified. New N=8 blocked-sufficient
   condition: npm(L_c1 | V \ {p,q}) = 0 => BLOCKED (36/36; FALSE at
   N=6 — the rungs genuinely differ).

## Proved
- W27-P1 (profile theorem), W27-D2 (diagonal collapse: diag X_4 =
  EXACT at N=8; N=8 is the special order — N=6 and N=10 have
  all-even top profiles).
- **W27-D3: the no-cancellation diagonal stratum at N=8 is EMPTY**
  — exhaustive over all 32,970 disjoint-PM triples of K_8:
  condition (C) ((4,4,0) words) <=> all three pairwise unions are
  Hamiltonian 8-cycles (16,800 pass); condition (D) ((4,2,2)
  words) passes 8,610; **BOTH: 0**. Census by cycle type recorded;
  raw-definition cross-check 20/20 with W25's engine. This proves
  "no diagonal exact source at N=8" MODULO the cancellation
  stratum — the classical edge-coloured Krenn statement at N=8,
  nearly closed by pure combinatorics.
- W27-R1 (site reduction, every N,k: X_k nonempty <=> a K_{N-1}
  source makes three linear systems consistent; the constant row
  outside the mixed rowspan; rank(mixed) <= 3(N-1) - 1 necessary);
  W27-R2 (an order-3 site symmetry + colour rotation collapses the
  three systems to one; verified with a non-vacuous negative
  control).
- W27-S1/S2/S3 as above; the X_4 obstruction on Delta^3_8
  backgrounds has SIZE-1 certificates (a single off-4 word row
  proportional to the constant row) and the cycle-type correlation
  (all-Hamiltonian buys 2 feasible colours; (D) takes the third
  back — the same tension as D3).

## X_3 at N=6 decomposition (T3)
120 more exact points stratified by site-kernel signature; the
RIGID stratum ([(0,0,0)x3, (6,6,6)x3]) has witness count EXACTLY 9
at all 51 points; minimum anywhere 3; ZERO all-blocked (977 objects
total with W25). "X_3 => witness at N=6" remains [CONJECTURED].

## Controls
F8 fully reproduced (membership, defect profile, 21/21 blocked over
Q + two 1-mod-3 primes, kernel table identical); doubled-delta43 =
the cleanest X_3 \ X_4 object at N=8 (exactly 6 group-constant
(4,4,0) defects); the 24-class table reproduced IN FULL; ledger
18/19/20/21/22 batteries incl. one vacuous control caught and
replaced; adversarial builders per NEVER claim (380 raw-tested
triples; probe-fires-on-nonempty 18/18).

## Soft spots
D3 covers the no-cancellation stratum only (the N=8 diagonal
cancellation stratum is THE remaining gap; 2^28-per-class makes
W25's exhaustion non-transferable); X_4 emptiness is a calibrated
search silence, not a proof; annealing objective gameable (family
sweep is the evidence); the N=8 skeleton dataset is a sample.

## Named next objects
(1) the diagonal cancellation stratum at N=8 (completes "no
diagonal exact source at N=8"); (2) the N=8 skeleton invariant
(training set on disk; 12 mixed cells the target); (3) the rank
statement "all three colour systems rank <= 20" via the symmetric
slice — ~7 orbit parameters, SYMBOLIC ELIMINATION FEASIBLE, would
settle the symmetric case of X_4 emptiness outright; (4) the
rigid-stratum theorem (51 points, constant 9 witnesses); (5)
W27-S1's cap mechanism (why one c1-simple endpoint suffices at N=6).
