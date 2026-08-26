# UNAUDITED — W30 probe lane: Route A's residual pairwise exclusion

**NOTHING IN THIS DIRECTORY IS A PROVED CLAIM OF THE REPOSITORY.**
This is an unaudited probe lane. Every verdict here is the output of a
single lane's engines and has not been independently audited.

- Pinned git HEAD: see `PINNED_HEAD.txt` (`021b1a307e8edb10b964fadefd4b823bdb589035`).
- Date: 2026-08-19/20.
- Target: the residual statement left open by W26
  (`computations/unaudited-blockers-w26-2026-08-16/`): the pairwise vertex
  failure exclusion "L2 and R5 (or L2 and R6) never both fail", on which
  W26's joint residual theorem depends at supports m = 25, 27, 28.
- Arithmetic: EXACT ONLY (`fractions.Fraction`, integers mod p). No floats.
- Fields: Q and F_p for p ∈ {13, 31} (both ≡ 1 mod 3, ledger 19).

## What is here

| file | contents |
|---|---|
| `w30_lib.py` | the EXHAUSTIVE vertex deliver/fail engine (all ~500 index choices per vertex; W26 sampled ~10) |
| `w30_quick.py`, `results_quick.json` | exhaustive re-analysis of the 39 stored W20/W21 exact points + engine-agreement control C1 |
| `w30_cal.py` | calibration + exhaustive re-census against W26's own recorded verdicts |
| `w30_mech.py`, `results_mech*.json` | failure-MECHANISM classifier (N1 det-nonzero vs N2 letter-collapse; slice-matrix ranks) |
| `w30_hunt.py`, `results_hunt_*.json` | the adversarial co-failure hunters (ledger 20): steering hill-climb on the clean layer |
| `w30_verify.py`, `results_verify*.json` | independent re-verification of every candidate refutation object + control manifest |
| `w30_factory.py`, `points_*.json` | exact clean-point factories (checkpointed) |
| `w30_build.py` | the hafL/hafR-annihilation construction attempt |
| `REPORT.md` | the lane's findings |

## Discipline followed

- Detached `nohup` compute with per-piece JSON checkpoints (machine sleeps).
- Every control script ends by asserting a manifest of executed controls
  (ledger 21).
- Every infeasibility verdict carries an explicit OUTSIDE-LOCUS control
  (ledger 18) and a mutation control.
- No claims are drawn from search minima (ledger 18 companion): a failed
  search is reported as a failed search, never as evidence of impossibility.
- Nothing is written outside this directory; no git commit.
