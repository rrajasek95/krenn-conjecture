# AUDIT A8 — the ladder-route theorem chain — REPORT (UNAUDITED, 2026-08-19)

Pinned HEAD 0016ec5. Fully independent code (recursive PM expansion,
raw 105-term H, own sigma-orbit parametrisation, own polynomial
class). Agent's write was policy-blocked; this transcribes its
report.

## THE DIAGONAL CHAIN: FULLY CONFIRMS (in its claimed scope)
- W27-P1 (X_5 = EXACT at N=8) CONFIRMED (max off-count = N -
  ceil(N/3), exhaustive N=2..12; 12 live profiles exact).
- W25-D1/D1' CONFIRMED (exhaustive N=4,6 + sampled N=8; controls
  fire). W27-D2 CONFIRMED.
- W27-D3 CENSUS CONFIRMED BY THREE ROUTES (raw-condition
  enumeration; pure inclusion-exclusion — 6300 ordered pairs = 5040
  Hamiltonian + 1260, 31*5040 + 33*1260 = 197,820 = 6*32,970;
  cycle-type stratification). The "(C) <=> pairwise-Hamiltonian"
  shortcut DERIVED, 0/32,970 mismatches.
- **NEW RESULT (audit gift): a short structural PROOF of the D3
  incompatibility** — (C) => not-(D): if M_2 uses a distance-3
  chord of the M_0-M_1 Hamiltonian cycle, an adjacent pair
  completes a (2,1,1) matching; otherwise M_2 preserves parity and
  the four Hamiltonicity survivors each carry an explicit (2,1,1)
  matching. Machine-verified on all 16,800 cases (13,440 step 1 /
  3,360 step 2 / 0 counterexamples). The exhaustion is now a
  theorem with a hand proof.
- W28-DEL: CONCLUSION CONFIRMED; PRINTED JUSTIFICATION REFUTED as
  unqualified (explicit cancelling-weight witness where deletion
  CREATES a violation; W28's deletion control used positive weights
  only — vacuous against exactly this). Repair known and cleaner:
  inside the stratum haf = 0 <=> npm = 0 and npm is
  deletion-monotone; no rescaling needed.
- W28-LAM: "=" REFUTED (explicit exact X_3-not-X_4 point whose
  Waring polynomial is identically lambda^4-sum — two
  (D)-violations cancel); downgrade to one-way implication /
  discriminator.
- W28-GOOD CONFIRMED — including on 60 configurations with supports
  STRICTLY containing a PM (a regime W28 never tested).
- w27_core docstring "L_c pairwise disjoint" REFUTED (explicit
  overlap point); only the GOOD classes are disjoint — which makes
  the cancellation sweep's disjoint-support restriction REAL.
- SCOPE CORRECTION: the cancellation sweep actually completed 8
  profiles / 1,543,746,960 triples (more than reported) but
  (5,6,6) and (6,6,6) WERE NEVER RUN — coverage is 8 of 10
  PM+<=2-extra profiles.
- N=10 remark corrected: the special-order criterion is N = 2 mod 6
  (N = 8, 14, 20, ... behave alike; N=10's top shapes are (4,4,2)
  AND (4,3,3)).

## W28-T1: CONFIRMED (computation and argument)
Own re-encoding: 45/45 selected ideals unit in char 0 + 1000003 +
32003; full 127-sweep relaunched independently (81 done, 243/243
unit at report time); k=3 calibration exact (not-unit, dim 10);
the orbit-reduction unsoundness catch CONFIRMED with a witness
(sigma carries colour-0 to colour-1); informativeness confirmed at
sample scale WITH THE FULL 21-UNKNOWN SYSTEM (no DEC shortcut);
ledger-18 explicit-point control SUPPLIED BY THE AUDIT (an exact
on-X_3 point where 7/214 k=4 generators are nonzero). Corrections:
W28-SYM needs |H| invertible (unstated) and IS NOT USED by T1 (T1
rests on DEC + FREE); rung implementations are two, not three (W27
imports W25's in_Xk; its hafnian is independent).

## For W29 (load-bearing)
T1h's reduction independently re-derived and CONFIRMED SOUND (three
distinct free sites forced; the S_7 relabelling legitimate on the
unrestricted diagonal family — trivial colour action, unlike the
sigma slice); its k=3 calibration returns not-unit dim 57 as
required; A8's own k=4 run also did not terminate (char 0
abandoned, char 32003 still running) — no verdict. **A mod-p unit
verdict would NOT prove the char-0 kill; the char-0 run is the
load-bearing one.**

## Repair list before promotion (none breaks a theorem)
(a) rewrite W28-DEL around the no-cancellation hypothesis + re-run
its deletion control with signed weights; (b) W28-LAM to an
implication; (c) re-attribute T1 to DEC+FREE, add |H|-invertibility
to SYM; (d) fix the disjointness docstring + the sweep's stated
scope; (e) run the missing (5,6,6)/(6,6,6) profiles or restate
coverage; (f) N = 2 mod 6 criterion; (g) "two implementations".

## Controls
16-row mutation ledger all fired (incl. the cancelling-weight
deletion counterexample and the vacuity demonstration of W28's
positive-weight control); manifests clean in every runner;
multi-characteristic throughout; no verdict by specialisation.

## Bottom line
If W29's T1h terminates unit IN CHAR 0 and is audited to this
standard, "no diagonal exact source at N=8" — the classical
edge-coloured Krenn–Gu statement at the open order — is a
COMMITTABLE THEOREM. Nothing found that would invalidate it.
