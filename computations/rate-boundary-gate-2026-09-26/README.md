# Non-prism boundary exclusions

[Undergraduate explainer and diagram](../../explainers/RATE-BOUNDARIES.md) ·
[Full proof](../../notes/rate-boundary-exclusions-2026-09-26.md)

**New research, not independently audited or certified.** The universal complex
rate bound is still open. This package checks two exclusions and a necessary
condition that narrows the remaining limiting configurations.

## Results

* At fixed five-site core, orthogonal projection gives the exact best fidelity
  over all 45 incident entries. Every perfect-fidelity limit must pass six
  augmented-response rank tests.
* The specified colored five-cycle has maximum fidelity 2/3. Every core within
  distance 1/200 has maximum fidelity at most 1346/1875, below 3/4; incident
  source entries remain arbitrary.
* The specified two-versus-four identity-block source has a 54-dimensional
  linear response with maximum fidelity 2/5. Every source within distance
  1/1000 has fidelity at most 10609/21609, below 1/2.
* The second source passes every single-site rank test, showing why the second
  decomposition adds a separate exclusion. The known prism border family also
  passes those rank tests and remains available, as required.

## Replay

Python 3.10+, standard library only, from the project root:

```sh
python3 computations/rate-boundary-gate-2026-09-26/verify.py
python3 -O computations/rate-boundary-gate-2026-09-26/verify.py
python3 -I -S computations/rate-boundary-gate-2026-09-26/verify.py
```

The checks take less than a second locally. There is no numerical optimizer,
floating-point rank decision, external solver, or downloaded certificate.

The checker reconstructs the coefficient maps from perfect matchings and checks
the two-versus-four response independently by grouping edges across that cut.
Integer matrix identities verify its complete Gram spectrum and the exact
projection equations. Rational elimination checks response ranks; rational
inequalities check the neighborhood constants. A corrupted Gram matrix is
deliberately rejected. A separate exact prism calculation prevents the rank
screen from being mistaken for an exclusion of all GHZ-approaching limits.

[verification.json](verification.json) records the results and source hashes.
The written continuity and norm estimates, and the completeness of the general
boundary interpretation, still require independent mathematical audit. The
existing certified proof packages are unchanged.
