# W24 — the residual-linear-kill theorem — REPORT (UNAUDITED, 2026-08-15/16)

Pinned HEAD 0631c68. Exact-only; independent engine (cross-checked
39/39 verdicts, 0/7,800 Phi mismatches vs W21 with a strictly
smaller row set). Agent's write was policy-blocked; this transcribes
its report.

## PROVED
- THEOREM W24-A: the residual degree-<=1 system kills at EVERY clean
  point with all Gamma cells nonzero ON WHICH haf_Gamma VANISHES
  IDENTICALLY (all 6,561 words) — m = 25,26,27,28, every char != 2.
  Proof via virtual words: coefficients c_e depend on neither of
  e's switching coordinates, so solo rows read c_e(v*) z_e = 0 with
  some c_e(v*) != 0 by W24-C. Certificates machine-enumerated
  (330-400 virtual words per vertex at 26/27/28; vertex 3 at m=25 +
  the monomial second certificate). The stratum holds 41/56 fresh +
  28/39 stored points.
- LEMMA W24-C (no hypotheses, every word): the three residual
  coefficients at an L-vertex satisfy (c_1,c_2,c_3)^T = M (F)^T with
  M the symmetric off-diagonal matrix of X_a = G_{bc} D_a, so
  det M = 2 X_1 X_2 X_3. Corollary: all cells nonzero + matching
  edges present => at every word some c_k != 0 (char != 2 GENUINE:
  fails 800/800 at p=2, holds 800/800 at p = 7, 13, 31 — the
  p = 1 mod 3 residues per ledger 19). 0/5,760 mismatches.
- W24-E/F/G (m=25): exact two-term factorisation Phi = A_56 P +
  A_67 Q (neither P nor Q sees y6); the MONOMIAL coefficient
  c_(2,6) = A_13 A_07 A_45 at m = 25/26/27 (nonzero at every word);
  the case split closing m=25 EXCEPT for "Case 2b" (v_0 || v_2,
  v_1 not || v_0, at ALL nine (y5,y7)) — never observed (rank 1 at
  9/9 on all tested points; partial forcing chain derived but not
  closed).

## THE FINITE REDUCTION
Survival <=> NO PURE ROW (a live cell e and an e-solo word with
Phi = 0 and c_e != 0). 95/95 exact clean points have one
(1,018-1,929 each). The system splits into row-isolating
sub-systems in 1-3 unknowns; minimal certificates size 1-2; all six
sub-systems killed at 39/39 stored + 54/56 fresh (full system
killed the other 2).

## CORRECTION (record)
The regime dichotomy (haf_Gamma = 0 identically <=> consistent) is
FALSE — explicit m=27 point with Phi not identically zero and the
system CONSISTENT (10 cells forced); adversarial lane found the
same shape at m=25/27. The kill claim is unaffected; do not build
on the dichotomy.

## ADVERSARIAL BUILDER (ledger 20): NO SURVIVOR
124 fresh clean points over Q, Q(omega), Q(i); all 39 stored
re-scored; the factoring ansatz closed by elimination; the lane
independently re-derived det M = 2 X_1 X_2 X_3.

## THE EXACT BLOCKER (per m)
Prove the pure-row statement where haf_Gamma does NOT vanish
identically: m=25 = rule out Case 2b; m=26/27 = the one-unknown
(2,6) sub-system with the monomial coefficient ("some (2,6)-solo
word has Phi = 0, or two give different ratios"); m=28 = the
three-unknown 0|{(0,4),(0,5),(0,6)} sub-system.

## Controls
C1 template/matching/word identity vs w21_core; C2 39/39 verdict
agreement; C3 multi-characteristic (ledger 19, with the p=2 firing
control); C4 other-side controls (consistent relaxations reported
NOT KILLED, incl. a 176-row consistent family — ledger 18); C5
planted-solution positive; C6 mutation; ledger 17 discipline
(identities at random points; verdicts only at constructed
on-variety points). Soft spots: main statement [CONJECTURED] off
the vanishing stratum; Case-2b partial chain is unaudited scratch;
no Singular elimination run (out of budget => ledger 13/14 guards
unexercised here); A7's family covered via W21's stored verdicts
only.
