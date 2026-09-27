# Unrestricted local W optimality at every even count

**Written proof with exact supporting checks; independent audit pending.**
This is a local theorem, not the unrestricted global design theorem.

[All-even proof](../../notes/w-state-all-even-local-optimum-2026-09-27.md) ·
[Four-site higher-order obstruction](../../notes/w-state-four-site-local-obstruction-2026-09-27.md) ·
[Illustrated guide](../../explainers/W-LOCAL-OPTIMALITY.md) ·
[W project](../../research/w-state-design/README.md)

For every even $n\ge4$, the known one-root W design is a strict local
rate optimum among arbitrary complex colored sources, modulo output
scaling and site phases. At fixed output, departing from the local phase
orbit costs at least a constant times squared source distance.

The proof gives universal sums of squares for $n\ge6$.
At four sites, the linearized Lagrangian really has negative directions.
The higher output equations exclude their dangerous row-sum modes,
establishing the same local conclusion.

From the repository root, with Python 3.11 or later and the standard library:

~~~sh
python3 computations/w-all-even-local-optimum-2026-09-27/verify.py > /tmp/all-even-w-local.json
diff -u computations/w-all-even-local-optimum-2026-09-27/results.json /tmp/all-even-w-local.json
python3 -O computations/w-all-even-local-optimum-2026-09-27/verify.py > /tmp/all-even-w-local-optimized.json
diff -u /tmp/all-even-w-local.json /tmp/all-even-w-local-optimized.json
~~~

The replay:

- Enumerates actual matchings at 4, 6, 8, 10, and 12 sites, checking
  the complete base output, Jacobian, stationarity multiplier, and
  weighted output Hessian.
- Constructs the full tangent parameterization, verifies its dimension,
  and compares every coefficient of both second-variation formulas.
- Checks all independent site-phase directions and the positive polynomial
  giving the all-size coefficient $\kappa_N$.
- Verifies the four-site quadratic and cubic identities symbolically.
  An exact complex direction has negative quadratic value and cancels
  every second-order output, but has a nonzero third-order obstruction.
- Rejects a corrupted Hessian coefficient.

All acceptance checks remain active in optimized Python. Arithmetic is
rational, with $\mathbb Q(\omega)$ used for the exceptional complex fixture.
The universal theorem also depends on the written counting, decomposition,
and local-analytic arguments. Finite checks do not replace those proofs.
No explicit neighborhood radius or global optimum is certified.

Code, proof, and dependency hashes are recorded in the adjacent JSON files.
