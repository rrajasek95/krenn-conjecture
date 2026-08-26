# W8 — hybrid template-kill sweep — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD a1196b4. Exact verdicts only (int/Fraction/SAT+DRUP);
numpy boolean/mod-p work cross-checked pure-Python. Agent's write was
policy-blocked; this transcribes its delivered report. 19 scripts,
32 JSONs, 93 DRUP proofs (745 MB) here.

## Headline
- (SC) independently derived (as FIE) from slice-cover §2 eq.(6)
  BEFORE the mission change; A2 cross-check 99/99. All W6
  certificates re-verified zero-singleton but 27/27 violate (SC).
- ADMISSIBLE ZERO-SINGLETON THRESHOLD IS 16 (not 15): supports <= 15
  have NONE (31/31 orbit UNSAT, DRUP; <= 11 UNSAT outright,
  reproducing m >= 12). At 16: EXACTLY 12 templates = 2 classes up
  to S8 x S3 (complete enumeration), both O1-killed. 17: thousands
  exist. 18+: everywhere.
- VALUE-LEVEL CLOSURE: m <= 16 CLOSED (31/31, DRUP 25.1M lines);
  m <= 17 CLOSED (31/31, DRUP 66.5M lines; independent no-nogood
  cross-check: 564 templates / 77 classes all killed — 434 O1, 84
  K3, 46 one-live-class). m = 18: 12/31 orbits run, 9,907 verified
  kills, 0 survivors, NOT exhausted. m = 19: partial, 0 survivors.
- IMMUNITY THEOREM (m >= 20): a template whose constant fibres are
  nonempty and whose mixed fibres all have size not in {1,2} is
  PROVABLY immune to O2/O1/one-live-class/K3 in any exponent
  refinement (no binomials => lattice rank 0 => no relations ever).
  Construction: 12 single cells serving all 24 slots + nine-cell
  blocks carrying two disjoint 4-cycles; exists at every support
  20..28; sharp (immunity forces m >= 20). CEGAR independently
  found a different survivor at m = 20 (Sigma 58, beta 9, one
  rank->=2 block, fibre histogram {2:90,3:42,...}) with no hint.
- SLACK ON THE REAL CLASS: all 34 admissible zero-singleton
  templates incl. every survivor have W9-slack -7..-14; ZERO
  escalation signals. Survivors are certificate gaps, not
  counterexample candidates.
- Calibrations: W2 m=28 census reproduced 28/28 (new: exactly 2
  orbits; all 28 (SC)-admissible); diagonal <= 27 UNSAT reproduced
  (independent of A2 and the lanes).

## Per-support table
<= 11 impossible | 12-15 closed by singleton (DRUP) | 16 closed
(O2+O1) | 17 closed (O2/O1/one-live-class/K3) | 18-19 zero survivors
seen, not exhausted | 20-28 immune survivors exist | diagonal <= 27
empty | m=28 R_cell: 28 templates, O1-dead.

## Controls
C1-C9 + encoding controls (one caught a real unsoundness before any
run) + S1 completeness (8 known admissible templates SAT inside the
formula) / S2 soundness / S3 witness triples + independent
solver+encoding re-run of <= 15 (glucose4, long clauses: 31/31
UNSAT) + certificate verifier (caught a real dependency-closure bug;
CEGAR aborts rather than adding unsound nogoods).

## Soft spots
All conditional on (SC) + constant-witness inputs; 18/19 sampled not
exhausted; the >= 20 ceiling is a genuine limit of lattice reasoning
(any future kill must beat the immunity proposition); J(T) mod-p =
diagnostic only; class propagation capped (40 rounds); no Groebner
escalation run.

## Next
Finish 18/19 (shrink with W9-1 row death first); NON-lattice kill
for 20..28 (the support-20 survivor, Sigma 58, is the first target;
Singular available).
