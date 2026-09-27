# An all-even W-design gap from Legendre polynomials

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted W optimum remains open.

[Proof](../../notes/w-state-equal-split-legendre-2026-09-27.md) ·
[Illustrated guide](../../explainers/W-GLOBAL-GUARANTEE.md) ·
[W project](../../research/w-state-design/README.md)

Split $n=2m\ge6$ sites into two equal groups. Give each group one
uniform complex ground weight, and all cross edges a third weight.
Every colored exact-W completion has rate **strictly below
$(80/81)R_*$**, where $R_*$ is the rate of the known one-root design.
Other colored entries remain unrestricted.

Counting matchings turns the zero-ground-amplitude equation into a
Legendre polynomial. Each root gives one cancellation branch.
The proof shows that imbalance between the two groups increases
the scalar response cost. At balance, that cost is an explicit
expression involving a Gauss--Legendre quadrature weight.
The bound includes every branch and the disconnected cases.

The uniform scalar comparison $F\ge(81/80)F_*$ is sharp only at the
previously studied six-site balanced source. At every larger size it
is strict. From 16 sites onward a stronger explicit bound decays
geometrically relative to $R_*$. These are upper bounds on exact W
rates, not asserted optima within the family.

From the repository root, with Python 3.11 or later:

~~~sh
python3 computations/w-equal-split-legendre-2026-09-27/verify.py > /tmp/w-equal-split-legendre.json
diff -u computations/w-equal-split-legendre-2026-09-27/results.json /tmp/w-equal-split-legendre.json
python3 -O computations/w-equal-split-legendre-2026-09-27/verify.py > /tmp/w-equal-split-legendre-optimized.json
diff -u /tmp/w-equal-split-legendre.json /tmp/w-equal-split-legendre-optimized.json
~~~

Only the Python standard library is required. The replay checks:

- Matching and cofactor polynomials from an independent endpoint
  recursion, through half-size 12.
- Rodrigues coefficients against the integral expansion, three-term
  recurrence, orthogonality, derivative, and polynomial-kernel identities,
  through degree 16.
- The scalar branch-cost identity against the counted cofactors,
  modulo the root polynomials, through half-size 12.
- Exact polynomial remainders proving all five small-degree cases.
- The exact tail base case and positive coefficients in the all-size
  induction, plus finite algebra checks of its ratio formula.
- Reciprocal-row and imbalance formulas on exact rational examples.

Every check survives optimized Python. No floating-point calculation,
root approximation, or numerical optimization is used.
The written proof supplies the all-size arguments, complex-root
classification, and monotonicity for all imbalances. Finite replay
checks are supporting evidence, not a substitute for those arguments.
The strict six-site rate conclusion uses the pinned earlier completion
obstruction. The package does not extend the local-minimum theorem
to other dimensions and is not Lean-certified.
