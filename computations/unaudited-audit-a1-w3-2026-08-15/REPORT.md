# AUDIT A1 of probe W3 (GIT/moment) — REPORT (UNAUDITED, 2026-08-15)

Adversarial from-scratch audit; independent code by different routes
(hafnian recursion vs matching lists; exact rational simplex for both
LP branches; fpm-polytope vertex enumeration). Pinned HEAD 81beedf.
Agent's write was policy-blocked; this transcribes its delivered
report. Scripts a1_*.py + OUT_*.txt here.

## Verdicts
1. L1 (gauge weights equal on every matching of a word; gauge-initial
   = restriction): CONFIRMED. 688,905-monomial multidegree reproduced
   by a third enumerator; 7 mutation controls all killed.
2. THEOREM A.1 (no exact source gauge-unstable; alternative (D) exact
   degeneration to strictly smaller cell support / (P) balanced with
   load(v,c)=mu_c, 21 conditions at n=8): CONFIRMED. Exact simplex
   both branches; exclusivity clean on all tested supports; 60/60
   cross-agreement with W3; (D) preserves all equation values
   (0/19,683 bad). D4: attribution nit (Stiemke vs Kempf-Ness).
3. COROLLARY A.2 (WLOG minimum-CELL-support counterexample balanced):
   CONFIRMED, airtight. Measure is CELLS.
4. PHASE-ONLY REDUCTION: narrow per-fibre claim vacuously true;
   BROAD CLAIM REFUTED.
   - D1 (material): w3_modulus.py's certification is a TAUTOLOGY
     (xfail == 0 by construction; (m3) never evaluated).
   - D2 (material): coupled >=2-term fibres generate modulus-level
     conditions outside (m1)-(m5). Explicit exact witness: 13-cell
     n=8 support, no singleton mixed fibre, forced |a1 a4| =
     2|a0 a6|; solvable exactly over Q with general moduli (moduli
     {1,2}), IMPOSSIBLE with all moduli 1 on the ENTIRE gauge orbit
     (L1 makes fibres equilateral on orbits). Three further supports
     found. "Fix all moduli to 1" is a codimension-(|S|-3n)
     RESTRICTION (equilateral ansatz), not a normalization — the v5
     licence must be withdrawn. W1 v6.1's over-C ceiling survives
     via the elementary singleton bound; re-cite it.
5. MONOTONE POTENTIAL: CONFIRMED-WITH-CORRECTION (D3, material for
   Route II): potential descends in CELLS, not blocks; W3's "19->16
   / 20->16 block reductions" are colour-class reductions at fixed
   aggregate block count 28. Independent-4-set proposition CONFIRMED
   exhaustively (537,355 min-degree-3 graphs, 0 violations, sharp at
   min degree 2; independent fpm-vertex route).
6. NUMERICS: CONFIRMED. eps^{-1/23} never had repo backing (git -S
   forensics); prism collapse reproduces exactly (nine surviving
   cells = the finite-obstruction prism); divergence is closed-orbit
   gauge motion. D5 labelling nit immaterial. D6: W3's float LP
   cannot prove the negative branch (no error found; 60/60 agree).

## Bottom line
Build on: L1, A.1, A.2, the four-set identification + exhaustion,
the numerics corrections — so W9's case-(D)/(P) usage is sound.
Stop building on: the phase-only reduction and the all-moduli-1
licence; do not read the cell potential as a block-support ratchet.
16-row mutation-control ledger in the delivered report; all killed.
