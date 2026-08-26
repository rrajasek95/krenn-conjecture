# W18 — the m=18/19 finisher — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 1486392. All verdicts exact (int/Fraction, SAT +
replayed DRUP; numpy = search accelerator only, every hit re-proved
by reference code). Agent's write was policy-blocked; this
transcribes its report (sweep still running at hand-off; agent
revived to shepherd it to completion).

## HEADLINE
The MECHANISM is closed; the EXHAUSTION is 84% done. New purely
combinatorial kill LEMMA W18-A (cut contradiction: split words
factor F_w = F^L F^R; pinned sub-words (P1 unique supported PM /
P2 split constant) on both sides of a mixed split word contradict;
certificate = cut + word + pinning kinds + a 7-28-literal REASON SET
machine-checked to force the kill on every completion; ~1 ms) plus
LEMMA W18-D (cut-local ratio kill on side-internal cells, <= 3-term
equations regardless of whole-B thickness) kill EVERYTHING this lane
has seen: 48/48 W11 witnesses, 31/31 W8 m=18 orbit witnesses, all
~1,700 sweep templates. ZERO SURVIVORS ANYWHERE. Closed: m=18
416/437 support-graph classes; m=19 211/310 (627/747). W8's stall
quantified: the admissible zero-singleton space is enormous (m=16
census = 12 exactly as W8/W11; m=17 census = 29,190 complete; one
m=18 class alone >= 3.8e5 labelled) — generalising reason-set
nogoods are mandatory, per-template killing hopeless.

## LEMMA W18-E (independent third derivation): family (R) is empty
at m <= 19 from (SC) alone (>= 12 thin server edges, thin <= 3
cells => not full => |Gamma| <= m - 12 <= 7 < 8 = minimum spanning
2-connected edge count). Verified exhaustively at each step.

## Exhaustion state at hand-off
m=18: 416/437 closed (415 proofs replay OK, ONE REPLAY FAILURE —
class 7847550, RUP failure at lemma 549,610 of 1,063,780; likely a
RAT step from lingeling inprocessing vs a RUP-only checker; class
UNVERIFIED until re-proved; cross-check with W11's rupcheck running).
m=19: 211/310, all proofs OK. Kill distribution (CEGAR rounds): O2
~219k, W18-A 1,540, W18-D 122, W18-C 19,174; W18-B (Singular)
NEVER FIRED — no verdict rests on Singular. Remaining: 21 + 99
class masks listed in run files; sweep resumable (--skip-done).

## Controls (all pass except the flagged replay)
C1/C2 anchors (48 W11 + 31 W8 witnesses accepted AND killed with
verified certificates); C3 equivariance 40/40 (licenses nogood
transport); C4 mutated checker's 9 bogus certificates rejected 9/9;
C5 468 literal drops all detected; C6 proof-mutation ladder on both
checkers; C7 planted survivor surfaces; C8 solver independence of
censuses; C9 dropped-class filters proved sound (318 classes
UNSAT-for-encoder too); C10 EXPLICIT-POINT CONTROLS (ledger 13):
121 feasible systems from explicit rational points, ZERO false
kills; shadowing guard enforced (zz* identifiers); Rabinowitsch
only, no sat().

## New hazard (ledger item 16)
A solver-native proof file is not enough: THE CHECKER'S PROOF
SYSTEM MUST MATCH THE SOLVER'S — RUP-only checkers reject
legitimate DRAT proofs (RAT steps). Pair lingeling with a
DRAT-capable checker or disable inprocessing.

## Soft spots
120 classes open (sweep running); one replay failure open; (SC)
inherited; certificate store 3.9 GB (prune to hashes + sample on
promotion); the constant-witness-orbit second decomposition is
implemented + validated but not run (natural cross-check).

## SECOND REPORT (revival phase; sweep continuing)
- STATE: m=18 428/437 closed, m=19 233/310 (all 86 open classes
  ATTEMPTED — wall-clock budget under load ~50, never a survivor or
  certificate failure). Zero survivors anywhere, ever.
- 7847550 RESOLVED (fresh proof replays, empty clause, rc 0;
  defective artifacts parked). Strict sweep found TWO more defective
  stored proofs (m18 15433212, m19 15449727 — terminate in the empty
  clause yet fail replay: corrupted in-memory extraction); both
  re-solving. MEASURED DEFECT RATE for pysat get_proof(): ~0.45%
  (3 of ~660) — any lane using it should assume the same and replay
  everything.
- ENGINE BREAKTHROUGHS: (a) 6-site sides in W18-D (reason-carrying
  kills replace orbit-blocking W18-C at m=19; 5400 s timeouts ->
  20-170 s); (b) GAUGE FIXING in W18-B (half-systems invariant under
  site scalings; divisibility of C* licences pinning independent
  incidence rows to 1 — no unimodularity needed; hardest template:
  undecided-5400s -> infeasible over Q in 17 s). New controls GC1-GC3
  (explicit-point half-systems: 0 false kills; 1,171 orbit-invariance
  checks; rank licences).
- ESCALATION RESOLVED: the first templates ever to survive
  O2/W18-A/W18-D/W18-C (classes 6258429, 6250494 — site 7 degree 3
  with all-single blocks => the system splits into three 6-site
  SECTORS; only 3-5 of 63 cuts carry content; the obstruction is a
  rank-2 identity inside one sector). ALL KILLED with verified lift
  certificates (6258429: 298 rounds, 565 s, VERIFIED 49,121 lemmas,
  empty clause; W18-B fired 3x). Independent numerics: solutions only
  at the toric boundary (exp(-c scale) residual decay), vs residual
  1.0 for verified kills.
- Controls all re-run with gauge fixing enabled; C6 rebuilt on
  PHP(8,7) after its fixture was found bad; EPC2b had a __main__-
  ordering bug that silently skipped it (fixed; pattern recorded as
  ledger item 21). Singular hygiene fully per ledger (zz*, list-form
  sat, elim.lib, shadowing guard exercised both directions).
- LEFT RUNNING: 21+ workers, supervisor (STOP_SWEEP to halt), disk
  monitor (stops below 12 GiB), two proof repairs. Cross-lane fix
  relayed: H1's cadical 3.0.1 + drat-trim binaries exist — switch
  emission to solver-native and drat-trim replay; re-emit the
  pysat-emitted stock at completion.

## PROGRESS TICK (native emission live)
- Native emission DONE: cadical binary (H1's build) + drat-trim
  primary + rup18 second opinion; a row verifies only if the proof
  ends in the empty clause AND both checkers pass; fallback rows
  stamped "NATIVE BINARY MISSING" so degradation cannot hide.
- Backfill: re-emit EVERYTHING decided (662 stored proofs, 7.1 GB
  gz, only 50 >= 40 MB) — run_reemit.py re-solves stored CNFs
  directly (no CEGAR rerun, no artefact races), replaces .drup.gz
  only on verified fresh proofs, appends corrected ledger rows.
  Failed pair (m18 15433212, m19 15449727) re-solving first.
- Sweep: m18 430/437, m19 235/310 (82 open), 19 workers +
  supervisor, zero survivors / zero certificate failures ever.

## MATERIAL UPDATE (cadence change pass)
- FOURTH defective pysat proof found by the strict criterion: m19
  class 14663420 (RUP FAILURE at lemma 832,087; the 1.29 GB proof —
  the store's largest). Revised defect rate ~0.6% (4 of ~665), all
  caught by replay, none touching a verdict. Full-set backfill (not
  sampling) confirmed as the right call.
- Backfill now fully chained + unattended (run_backfill_chain.sh:
  wait -> fixrows -> re-emit failures -> fixrows -> full 662-proof
  backfill -> fixrows -> BACKFILL_DONE), --rup-max-mb 100
  throughout. Notification discipline: single material-events
  watcher (survivors/certificate failures fire immediately).

## MILESTONE: m = 18 FULLY CLOSED (437/437)
0 missing, 0 survivors; 437/437 proofs replay AND terminate in the
empty clause; 111,176 verified kill certificates; slowest class
752 s. Kill distribution: O2-singleton 110,592 / W18-A 500 / W18-D
63 / W18-C 21 (W18-B never fired at m=18). Honest scope: 432/437
proofs are pysat-emitted (replay-clean; native conversion running
in backfill step 4); the closure is of the SAT encoding — the
value-level exhaustion W8 left open, with every kill clause
justified by an independently re-verified certificate. m19 at
254/310 (56 open).
