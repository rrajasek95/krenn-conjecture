# AUDIT A7 — the m=25 chain, W19, W20 — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD e0c4d7c. All-exact; engines from the model definition;
probe code imported only for comparison. Agent's write was
policy-blocked; this transcribes its report. 15 scripts + census/ +
perlemma/ sub-audits here.

## HEADLINE: W19's "m=25 CLOSED" IS REFUTED (explicit witness)
- DEFECT: w19_branchB.py:243 base_eqs() emits mu*k_x + A03*g; the
  true Branch-B consequence is mu*k_x − A03*g, which vanishes
  modulo the valid branch equation the same function emits; the
  flipped sign forces g = 0 (site 6 factoring) spuriously. Case 3 —
  the only case resting on base_eqs() — collapses.
- WITNESS (decisive): exact rational point, ALL 129 occupied cells
  nonzero, ALL 2,624 effectively-clean equations exact (two engine
  routes), squarely in case 3 / Branch B (D_x = E_x = 0 on the
  X_free words, rank M6 = 2, P_L = −1), NO SITE FACTORING; a
  12-member family. All valid W19 equations vanish at it (8,202 E1
  + 1,320 E2 + branch + case-3), 36/108 sign-flipped generators do
  not. NOT a Krenn–Gu counterexample (violates 3,820 non-clean
  equations).
- CONSEQUENCE: "the clean layer forces some site to factor" —
  W16's single remaining statement and W20's obligation — is FALSE
  at m=25. m=25 reverts to OPEN; the record "N=8 closed through 25"
  is RETRACTED to "through 24". The kill at 25..28 must consume
  equations beyond the clean layer (k=1/k=2 words, pures — matching
  W22-1's lesson).
- WHY THE CONTROL MISSED IT: W19's C5 explicit point has ALL EIGHT
  sites factoring, so every forcing target vanishes there by
  construction — a control inside the conclusion's variety is
  vacuous. LEDGER ITEM 18 proposed (adopted). Also: "search never
  reaches zero factoring sites" evidence is WORTHLESS — the same
  descent at m=25 never reaches zero while the zero-factoring point
  provably exists.

## Confirmed (and mostly strengthened)
W16-A dichotomy (exhaustive sweeps 262,144 x2 + sharp near-miss
3,456; STRENGTHENED: the exact effectively-clean X_free has 8
L-words incl. x1=0, so A14[0] constant is FORCED and W19's case 2
is vacuous — the honest split is two cases); the (E1)/(E2) family
(sound; complete as minors; plus the unused G=0 => K=0 family —
which the witness also satisfies); the downstream factoring=>kill
at every site of m=24..28 (pair-count tables reproduced exactly;
at m=25 any site except 1 kills); W19-K + the C_8 member (all
numbers); the census (STRONGER: all 794 classes certified by
explicit full in_R witnesses; |Gamma|=8 => C_8 by brute force over
all 3,108,105 8-subsets); W20-L; W20-R (CORRECTION: needs
deg_Gamma(t) >= 2 — 5 counterexamples at deg 1 in a 512-sweep;
harmless for (R)); the non-factoring clean points at 26/27/28
(CORRECTION: m=27 minimum is 1, not 2); the m=28 automorphism
(exhaustive over 241,920; trivial elsewhere); the L-free/R-free
reduction (STRENGTHENED to an exact polynomial identity in 148
variables; the 4,860 tests / 3,960 distinct words reconciled);
Pfaffian orientations verified with firing negative controls.
- LEMMA W20-P: statement TRUE, written proof step (B) INVALID
  (explicit gap); corrected induction proof supplied and
  machine-backed (exhaustive n=3: 560; n=4: 135,751; NEW n=5 fully
  exhaustive over 234,531,275 multisets — exactly the 5 coordinate
  configurations vanish); needs char != 2 (GF(2) fails 4/11/26) and
  through-the-origin hyperplanes. P4c proved (det S = 2 a1 a2 a3).
- W19's S_3^8 prose CORRECTED: 576 per-site elements preserve in_R
  (not 6); failure is ALWAYS (SC); survivors not a subgroup, so the
  operational census conclusion stands. S_8 x S_3(global) preserves
  241,920/241,920.

## Mutation-control ledger: ~40 rows, all behave (2 census controls
redesigned after failing to fire; the ledger-13 shadowing bug
reproduced with the guard bypassed).

## Bottom line
Promotion-ready: W16-A, W19-K + C_8, the census, W20-L, the L-free
reduction, the automorphism + non-factoring points, downstream
factoring=>kill 24..28, corrected W20-P. Withdraw: W19 HEADLINE 2;
the clean-layer forcing statement (false at 25); search-minimum
evidence. Repair: W20-P proof + hypotheses; W20-R deg >= 2; S_3^8
prose; m=27 minimum.
