# A8 final tally (UNAUDITED lane record, 2026-08-19)

Completes the audit whose main verdicts are recorded in master-plan
v46. Pinned HEAD 0016ec56. Independent implementation throughout
(generator construction, ring compression, Singular driver all
written independently of W28's).

## The full free-set ideal sweep — COMPLETE
- 127 cases (every nonempty subset of V': sizes 7/21/35/35/21/7/1)
- **381/381 unit-ideal verdicts (dim = -1)**: 127 in char 0,
  127 in char 1000003 (= 1 mod 3), 127 in char 32003
- 0 non-unit, 0 non-OK, 0 timeouts
- Controls: k=3 calibration NOT-unit (dim 10) with an exact
  rational point exhibited (ledger-18 control satisfied)

=> **W28-T1's computational core CONFIRMED AT FULL SCALE** on an
independent implementation (previously only 15 sampled cases).

## T1h
The 99-generator/66-variable T1h run was stopped without verdict
(no information, per ledger practice). NOTE (manager): A8's framing
"T1h in char 0 is the one computation that would commit the
diagonal chain" is superseded — W29-A1 proved the T1h ideal is NOT
unit (explicit 21-parameter family; formulation artifact), and the
diagonal theorem now rides on W29-T1's normal-form route, gated by
audit A9.

## Standing verdicts (unchanged from v46)
Diagonal chain confirmed in claimed scope (cancellation-free case,
now with a structural hand proof of the D3 census); repair list =
six write-up corrections + the two missing size profiles (5,6,6),
(6,6,6) — the latter subsumed by W29's cancellation-covering route.

Artifacts: results_SUMMARY.json + 13 more checkpoints, 32
scripts/logs, PINNED_HEAD.txt. No tracked file touched.
