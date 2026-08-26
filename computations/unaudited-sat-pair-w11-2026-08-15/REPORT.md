# W11 — independent SAT verification pair — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 66841f8. Written from scratch from the mathematical
definitions + notes/slice-cover.md §2 only; W8's directory not opened
until all verdicts were fixed. Agent's write was policy-blocked; this
transcribes its delivered report. Full artefacts here (3,078 gzipped
DRUP proofs, 44 verified witnesses, independent rupcheck.c).

## Verdicts (all per-support, general cell model, (SC)-admissible,
## three constant fibres nonempty, zero singleton mixed words)
- m = 13,14,15: UNSAT (35 + 136 + 309 iso classes, lingeling DRUP,
  all RUP-verified; min-degree-3 restriction proved lossless by a
  full 1,557-class sweep at m=13).
- m = 16: SAT — COMPLETE census: exactly 1 support-graph class of
  465, carrying exactly 12 templates in 2 orbits under S8 x S3,
  Sigma = 34 (x6) and 40 (x6), block shapes {1:10,3:4,9:2} and
  {1:10,3:4,6:2}. Escape mechanism: an alternating 4-cycle through
  two full blocks pairs every fibre.
- m = 17..28: SAT everywhere (44 witnesses saved, all independently
  re-verified by a code-disjoint checker); m = 28 non-single-cell
  SAT (Sigma = 126).
- Diagonal restriction: UNSAT for every m <= 27, ALL 2,589 classes,
  proofs verified.
- (SC+) column (adding the support shadow of the committed activity
  clause C_pj != 0): does NOT rescue the band — m=16 objects pass
  (SC+), SAT persists at 17..22+ — but it bites (one m=17 class
  flips to UNSAT; several first witnesses fail it).

## Agreement with W8 (compared only after verdicts were fixed)
Identical on: threshold 16; m <= 15 empty; the m=16
12-template/2-orbit/Sigma {34,40} census; SAT everywhere above;
diagonal <= 27; m=28 non-single-cell existence. Two independently
written encodings (31-orbit constant-witness split vs 12,346
support-graph iso classes) reproducing the same fine census is the
strongest corroboration this pairing could produce. No mathematical
disagreement.

## CROSS-LANE HAZARD (important)
pysat's cadical get_proof() TRUNCATES proof files mid-clause. 7 of
W8's stored DRUP files do not replay (4 at m=15, 3 at m16_closure).
W8's MATHEMATICS IS NOT IN DOUBT: all four failing m=15 CNFs re-solve
UNSAT under cadical153/glucose42/lingeling, and verified replacement
lingeling proofs are in this directory's w8_reproofs/. ANY lane that
certified UNSAT via pysat + cadical get_proof() must re-check that
its proof files terminate in the empty clause and replay. See
notes/2026-08-15-pysat-cadical-proof-truncation-hazard.md.

## Controls (13, all pass)
m=28 positive control; diagonal cross-check; planted singleton /
planted (SC) violation; word-encoding vs naive on all 6,558 words;
equivariance (60 templates); 12,346-class enumeration vs known graph
counts; m=12 dead (cube chart audits admissible with exactly 6
singletons); UNSAT-is-singleton-driven control (dropping only the
zero-singleton clauses gives SAT at 13-16); rupcheck round-trips
40/40 + rejects corrupted/bogus lemmas.

## Soft spots
Activity clause faithful form is value-level (only its shadow is
encodable); J.1d budget not encoded (likeliest downgrade of SAT
witnesses; term-rank profiles suggest cheap); rupcheck is same-day
code (forward RUP, deletion-ignoring — sound); solver monoculture
for decisions (proofs lingeling); class counts at 17-20 are lower
bounds (verdicts are not); m=28 single-cell census control did not
complete (covered by W8/W2 + the mandated control 1).

## FINAL UPDATE (same day)
1. (SC+) COLUMN COMPLETE: the threshold is 16 under BOTH readings —
   (SC+) UNSAT at 13-15 (implied), SAT at every 16..28 with
   re-verified witnesses (full sweeps 21-27: 100/103, 51/52, 23/23,
   11/11, 5/5, 2/2, 1/1; 28 non-single-cell 1/1). (SC+) bites
   individual classes (m=19 needed a graph search near the m=18/20
   witnesses) but empties no support. Soft spot #1 closed.
2. Control 1b correction: the m=28 single-cell census run found 15
   templates (all Sigma=28) then hit budget mid-enumeration — 15 is
   a LOWER bound, consistent with but not confirming the known 28.
3. W8 certificate audit still partial (7 replay failures so far; the
   m=17 proofs still grinding; count may grow). Conclusion
   unchanged: file defect, not mathematics — re-solved UNSAT x3
   solvers, verified re-proofs in w8_reproofs/.
4. LIVE CAVEAT: the J.1d budget was not encoded in either lane's
   admissibility; witness term-rank profiles (mostly rank 1, 2-11
   rank-3 blocks) suggest the witnesses are budget-cheap, but the
   check has not run — the one thing that could downgrade the SAT
   verdicts. 49 witnesses + 3,078 verified proofs on disk.

## CLOSING UPDATE (audit conclusive for checkable families)
- W8 proof-file audit final: m15_nosingleton 27/31 replay + 4 fail;
  m16_closure 28/31 + 3 fail; all 7 failures = pysat truncation; all
  7 re-solved UNSAT unanimously (cadical153/glucose42/lingeling);
  verified lingeling replacements for all 7 in w8_reproofs/.
- SHARPER HAZARD FRAMING: the truncation is SILENT — most truncated
  proofs still replay (root conflict reached before the cut), so
  passing certificates do not vindicate the extraction method;
  ~1 in 9 checkable W8 certificates was unusable. Replay, don't
  trust.
- m17_closure proofs NOT audited (62 MB gz / ~66.5M lines — forward
  RUP impractical): open verification-debt item — check with
  drat-trim (backward) or regenerate solver-native.
- Control 1b remains a lower bound (15 of the known 28; still
  enumerating on its own budget; nothing depends on it).
