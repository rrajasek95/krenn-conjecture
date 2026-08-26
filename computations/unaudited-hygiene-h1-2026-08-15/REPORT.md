# H1 — promotion-blocker hygiene — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 0b2c0ce (drafts were written at e0c4d7c — checklist A3
stays open). All-exact. Agent's write was policy-blocked; this
transcribes its report.

## BLOCKER 1 — fourth-matching layer audit: DISCHARGED, with a
## SPINE DEFECT found
- Theorem A3.4 CONFIRMED (independent engines; 161,148 charts
  reproduced exactly; every emitted matching brute-force-checked;
  N=4 sharpness).
- STEP 5's printed proof (draft AND committed
  proofs/odd-near-perfect-gadget-obstruction.md lines 56-58) is a
  NON-SEQUITUR — explicit counterexamples to the parity-class
  descent at N = 8, 16, 24. Theorem TRUE via two sound committed
  proofs (finite-obstruction §7 adjacent-residue descent — verified
  N = 8..20; termwise-rank3 §3.5 B3 minimal-arc — independently
  re-derived) + H1's new one-line contraction proof + exhaustive
  residual emptiness to N = 20 (893,025 configs, 0 survivors,
  matching the §3.6 census). RECORDED AS SUPERSESSION-2026-08-15-01
  (canonical file stays byte-frozen; correction note
  notes/2026-08-15-step5-defect-and-repair.md).
- A3.5 (m = 3N/2 floor) CONFIRMED — the J.1d forcing is genuine
  (EXACTLY ONE budget solution at N = 6..12).
- m = 3N/2 + 1: combinatorics PROVED + exhaustive at N = 6/8/10
  (576 / 90,432 / 14,330,880 templates, 0 singleton-free) but the
  FORCING STEP IS ABSENT (13 budget solutions, not 1) — MUST NOT be
  promoted; the gap is forcing, not combinatorics.
- Even-cycle-free corollary: TRUE ONLY FOR N >= 6 — at N = 4 the
  six K_4 one-factorisations are counterexamples (the exceptional
  witness's third appearance). Promoted form must carry N >= 6.
  Checkers built for both corollaries (exhaustive at N=6; N=8 to
  two extra edges).
- Structural bonus: N = 2 mod 4 always exits via Step 3 (odd parity
  class) — explains the branch census; the draft lacks a labelled
  Step 2.

## BLOCKER 2 — W12 C1/C2 controls: EVIDENCED (B1 partial)
C1a (NEW exact exponent identity, 424 checks), C1b (324 = original
scale), C2 (54): 0 mismatches, saved JSONs, deterministic points,
5 firing mutation controls. LIMITATION recorded: V is not unique —
"C2 passes" certifies the reconstructed character solves the
binomial system, not that V equals W12's matrix. C3 not re-run
(needs cross-lane load + 1,800 s Singular; A4-D3 rephrasing due
first).

## BLOCKER 3 — proof replays: DISCHARGED
Built drat-trim (backward, full RAT) + cadical 3.0.1 binary.
The 31 m=17 proofs (66.5M lines, 66 min): 28 VERIFIED, 3 FAILED
(o13/o19 missing lemmas before the empty clause; o20 never closes).
All 3 re-solved cadical-native from the byte-identical stored CNFs:
UNSAT, fresh proofs VERIFIED — **the m <= 17 closure now has 31/31
drat-trim-verified proofs** (replacements in reproofs/, untracked).
The 7 W11 replacement proofs: 7/7 VERIFIED by the second checker.
0 RAT lemmas in any core (why RUP-only checkers got lucky; ledger
16 stands). 4 of 31 stored proofs lack an explicit empty-clause
line (fatal only for o20) — "passing certificates do not vindicate
the method", again.

## BLOCKER 4 — portability scan: DELIVERED (+免 free extras)
83/83 cited artifacts exist. Debts: 17 scripts hard-code /Users/
rishi; 52 sys.path manipulations (6 genuinely cross-lane); 13
Singular scripts, 0 of 13 carry the zz-guard, 4 parse '?', 2 load
elim.lib, 1 uses list-form sat; 26 scripts / 84 bare asserts (incl.
two load-bearing guards in a3_core/a3_task2_floor that vanish under
-O; a Cyrillic homoglyph identifier in a3_core). EXTRAS: the
zz-guard run over all 35 .sing files — 0 LIVE COLLISIONS (ledger 13
is procedural debt, not an active false kill); 3 files carry the
sat()[1] trap, 1 omits elim.lib (a6_A4_singular.sing has BOTH —
that combination fails silently; A6's Singular route for the m=24
membership is defective and must be re-run under guard at
promotion; the hand-expansion and W15/W16 routes are unaffected).
BUILD CALIBRATION corrects ledger 6: on Singular 4.4.1p05 only
`mult` is reserved (e1 and I are fine); two hazard probes error
with rc 0, demonstrating ledger 11.

## Not discharged
Checklist A3 (cert-commit re-execution); B1 partial (C3); the two
corollaries must not be promoted as stated; ledger rule 5 for the
A3 lane needs a permanent certification/audits record beyond this
probe (partially satisfied by SUPERSESSION-2026-08-15-01 for the
Step-5 slice).

## Soft spots
Step-5 sweep exhaustive up to relabelling (argument, not
computation); contraction proof hand-only; W6's budget inequalities
transcribed, not re-derived; both fibre engines are H1's own;
regenerated proofs live untracked at a different HEAD; the zz-guard
regex does not cover piped-text Singular callers (w12_core,
w15_forcing).
