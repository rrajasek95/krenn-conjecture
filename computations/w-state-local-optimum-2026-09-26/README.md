# Exact unrestricted local optimality of the six-site W design

**Written local theorem; independent audit pending.**

[Proof](../../notes/w-state-unrestricted-local-optimum-2026-09-26.md) ·
[Illustrated guide](../../explainers/BOUNDARY-STRUCTURE.md)

The rate `1/65` design is a strict local optimum among arbitrary complex
six-site sources, modulo phase changes and overall scaling. This allows
colored-core perturbations outside the proved two-root architecture.
The theorem supplies no numerical neighborhood radius and no global bound
over unrestricted sources.

Python 3.10+, standard library only, from the repository root:

```sh
python3 computations/w-state-local-optimum-2026-09-26/verify.py > /tmp/w-local.json
diff -u computations/w-state-local-optimum-2026-09-26/results.json /tmp/w-local.json
python3 -O computations/w-state-local-optimum-2026-09-26/verify.py > /tmp/w-local-optimized.json
diff -u /tmp/w-local.json /tmp/w-local-optimized.json
```

The checker uses rational coordinates for all 60 complex binary source
variables and all 64 outputs. It verifies exact stationarity, a Jacobian
rank of 32, and positive rational Schur pivots on the 28-dimensional kernel.
The real form is positive definite. The imaginary form has exactly five
zero directions, all independently verified vertex phases.

Projection onto the two target colors extends the written theorem to all
135 ternary cells and larger finite palettes. The analytic proof handles
the dependent output constraints explicitly; it does not assume a smooth
feasible set. Corrupt stationarity data and a negative quadratic form are
rejected. All acceptance checks remain active under `-O`.
