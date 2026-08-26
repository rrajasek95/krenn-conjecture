# W29 — the diagonal closer — REPORT (UNAUDITED, 2026-08-19/20)

Pinned HEAD 0016ec5. 24 scripts, 26 checkpoints. Agent's write was
policy-blocked; this transcribes its report.

## HEADLINE
1. W29-A1 [PROVED]: W28's T1h ideal IS NOT UNIT — explicit
   21-parameter rational family in its variety (verified three ways
   incl. W28's own generator builder). The 900 s timeout was a
   FORMULATION problem (T1h keeps only the |S_0| = 1 rows; the
   |S_0| = 3 rows kill the family instantly). "Make T1h terminate"
   retired. The family points are NOT counterexamples (no colour
   X_4-feasible there).
2. **W29-T1 [PROVED]: NO DIAGONAL EXACT SOURCE EXISTS ON K_8 OVER
   ANY FIELD, ANY CHARACTERISTIC** — equivalently X_4 contains no
   diagonal point at N=8. The classical edge-coloured Krenn–Gu
   statement at the open order.
3. W29-T1+ [PROVED]: the same machine closes N=6 (Groebner-
   confirmed: 13/13 case ideals unit in char 0 + two 1-mod-3
   primes) and CORRECTLY FAILS at N=4 (the exceptional source is
   SAT and violates zero clauses). Uniform in even N; N=10 k=4 in
   flight (k=3 calibration 386/386 SAT), N=12 queued.

## The machine
- W29-B1/B2 (the free-set-triple normal form): the three
  witness sites y_0, y_1, y_2 are forced DISTINCT and F_c is inside
  {y_c} u Q with Q = V' minus the y's (|Q| = N-4). Case ledger =
  triples of subsets of Q: 4096 cases / 87 S_Q x S_3 orbits at N=8
  (13 at N=6, 386 at N=10, 1324 at N=12; profile formula = brute
  orbit count exactly).
- W29-VAN (the vanishing-pattern Boolean abstraction): one Boolean
  per hafnian; eight one-line clause validities (A0-A3, CASE, FREE,
  XF), each sound at every true point in every characteristic;
  CANCELLATION FULLY ALLOWED (A3 only forces vanishing), so UNSAT
  proves nonexistence over any field. Load-bearing structure:
  CASE alone SAT, CASE+FREE SAT, CASE+FREE+XF UNSAT.
- VERDICTS: N=8 k=4 UNSAT on all 4096 cases AND all 87 orbits (run
  twice); k=3 SAT on all (as it must be — X_3 diagonal sources
  exist and pass the encoder end-to-end: 1,200 site checks on 150
  real X_3 sources + the canonical one, 0 violations).
- PROOF-CHECKED THREE WAYS: five SAT solvers agree; an own-written
  RUP checker (passes accept/reject/TRUNCATION controls — the
  ledger-5 hazard — after one found-and-fixed unit-seeding bug)
  replays 87/87 + 13/13; third-party drat-trim verifies 87/87 +
  13/13. Independent algebraic confirmation at N=6/N=4 by Groebner
  (both outcomes exercised).
- Minimal UNSAT core: 361 constraints / 1,226 clauses for the
  singleton case (all groups deletable) — the hand-proof target.

## Controls (all pass, incl. firing negatives)
N=4 positive control end-to-end; the X_3-at-every-site control;
W28-T1 reproduced (10 cases, char 0 + two primes); W28's honest
boundary point stays feasible; ledger 6/11/13/20/22 batteries;
two independent hafnian engines agree 100/100 over Q and Q(omega);
adversarial LM builder calibrated at N=4 (3 hits at 1.1e-16) and
silent at N=6/8 (in flight).

## Honest scope
DIAGONAL only — the product structure H_w = prod haf(A^c|w^{-1}(c))
is exactly what diagonality buys; no non-diagonal transfer (the
sigma non-diagonal slice stays search-silent). General X_4 = empty
at N=8 remains CONJECTURED. The N=8 verdict is SAT-based with
Groebner corroboration at N=4/6 (N=8 case ideals in flight); the
minimal core is not yet a hand proof. A8's missing-profile repair
item for W28's sweep is SUBSUMED by this theorem (cancellation
fully covered).
