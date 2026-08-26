# A9 — promotion-gate audit of W29-T1 — FINAL (UNAUDITED lane record, 2026-08-20)

PINNED_HEAD 10eeae2; target pinned 0016ec5. Transcribed by the manager
from A9's final message (agent writes outside this dir are blocked).

## BOTTOM LINE
**W29-T1 CONFIRMED — and slightly stronger than stated. Committable
as spine.** Independently re-derived, re-encoded (inverted polarity,
own layout), re-solved by 5 engines, drat-trim proof-checked
(87/87 + 64/64 s VERIFIED). Two claims AROUND the theorem corrected:

1. **REFUTED: "uniform in even N".** At N=10 the exact level is X_6,
   not X_4 (even profile (4,4,2) has off-count 6). The N=10 k=4 run
   was a strict relaxation (5310/14760 partition rows, 174/384 FREE
   rows) and mostly SAT (35/42 sampled orbits); at the true k=6 the
   abstraction is STILL SAT (2/7 sampled orbits so far). Honest
   scope: **N=6 and N=8 closed; N >= 10 open for this machine.**
   (The manager stopped the in-flight N=10 k=4 run on this verdict.)
2. **Over-claimed control**: W29's "1,200 site checks on 150 real
   X_3 sources" all land in ONE case orbit (R=(Q,Q,Q)). Repaired:
   320 checks across 37 distinct cases, 0 violations.

## Verdicts per link (all CONFIRMED)
1. Reduction W28-FREE/B1/B2 (hand + machine; product formula vs raw
   105-matching evaluation, 50 sources x 6561 words, 0 disagreements;
   every FREE row inside X_4 — 480 rows, 0 malformed).
2. Case ledger 4096/87 (two independent routes: canonical forms +
   Burnside; N-table 1/13/87/386/1324 for N=4..12).
3. Eight clause families (field facts only; A2 rows = exactly the
   1638 mixed all-even words re-derived from scratch — k=4 drops
   NOTHING at N=8, EXACT = X_4, off-count histogram {2:168, 4:1470};
   XF licence comes from the true point — biconditional legitimate).
4. UNSAT: 4096/4096 + 87/87 at k=4; k=3 calibration 4096/4096 SAT;
   N=6 all UNSAT; N=4 SAT; 5 solvers agree; drat-trim verified;
   truncated/corrupted/cross-case proofs all REJECTED (ledger 5).
5. Any-field soundness + STRENGTHENING: the machine never uses
   haf(t^c|V)=1, only != 0 — so the theorem covers unnormalised GHZ
   (all three constant amplitudes nonzero, all mixed zero) with no
   roots/closure needed. Cancellation genuinely free (structural +
   operational checks).
6. W29-A1 (T1h not unit): 21-param family kills all 96 generators;
   its free sets are the maximal case, which k=4 kills — family is
   not a counterexample. Retirement correct.
7. Groebner N=6: rebuilt from own generators — 13/13 unit in char
   0, 2, 3, 7, 32003; N=4 correctly NOT unit (dim 3).
8. Load-bearing map: CASE 87 SAT -> +FREE 54 -> +XF 0; drop-one
   analysis nontrivial everywhere; no empty clause in any CNF.

## Scope note
"Diagonal" = BLOCK-diagonal (A_uv = diag(t^0,t^1,t^2), three
independent weight functions) — strictly contains the single-cell
edge-coloured reading; the classical Krenn-Gu statement at N=8 is
a corollary.

## Mutation ledger: all fire (MU0-MU7 + planted off-diagonal +
corrupted sources + proof corruption + independent B2 witness).

## Recommendation
COMMIT as spine with three repairs in the write-up: (i) strike
uniform-in-N / N=10 / N=12 claims; (ii) qualify the 1,200-check
control as single-case, cite the 37-case replacement; (iii) state
block-diagonal scope + the amplitude-nonzero strengthening.
Nothing in the proof chain itself needs repair.

In flight at close: run_a9_12 (N=10 k=6 spot check, 7/16, 2 SAT)
— sharpens the N=10 refutation only; cannot change gate items.
