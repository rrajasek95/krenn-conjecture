# The balanced GHZ frontier and an unrestricted W response bound

**Written proofs with exact supporting checks; independent audit pending.**

[Triangle classification](../../notes/triangle-response-rank-classification-2026-09-27.md) ·
[Unrestricted W response bound](../../notes/w-state-unrestricted-response-bound-2026-09-27.md) ·
[All-even W optimum without ground matchings](../../notes/w-state-no-ground-matching-optimum-2026-09-27.md) ·
[Illustrated guide](../../explainers/BALANCED-FRONTIER.md)

The triangle theorem classifies every singular response with three nonzero
edge blocks. At three colors its rank is 7, 8, or 9. A balanced two-triangle
six-site limit therefore has full derivative rank at least 49. A separate
balanced complete-support zero-output example has rank 25, identifying a
remaining class outside that theorem.

The W theorem gives an upper bound for every fully colored architecture,
computed from the scalar ground-core cofactor rows. Its uniform form is
`R <= B_n ((m-1)/m)^(m-1)`, where `n=2m` and
`B_n=((n-1)!!)^2 / binom(n,2)^m`. At six sites this is `4/135`.
A sharper open scalar inequality would prove the unrestricted value `1/65`.
The known W optimum is now proved at every even order whenever the ground
support has no perfect matching, allowing all other entries to be fully
colored. Any better design must cancel supported ground perfect matchings.
Neither unrestricted research objective is completed by this package.

Python 3.10+, standard library only, from the repository root:

```sh
python3 computations/balanced-frontier-2026-09-27/verify.py > /tmp/balanced-frontier.json
diff -u computations/balanced-frontier-2026-09-27/results.json /tmp/balanced-frontier.json
python3 -O computations/balanced-frontier-2026-09-27/verify.py > /tmp/balanced-frontier-optimized.json
diff -u /tmp/balanced-frontier.json /tmp/balanced-frontier-optimized.json
```

Exact checks cover all three triangle ranks, reconstructed determinant
certificates, all six possible two-triangle Jacobian ranks, the rank-25
complete-support example and its algebraic balance equation, the attained
one-root W bound, the four-site cancellation negative control, all fifteen
two-excitation completion identities on a complex example, and the uniform
constant algebra. The analytic proofs establish the general statements.
An exhaustive six-site support census checks the two-odd-component reduction;
exact split comparisons through 80 sites support the all-orders analytic gap.

`dependencies.json` pins imported exact arithmetic and the analytic
dependencies. `results.json` records the package and proof hashes. Acceptance
checks use `require`, so they remain active with Python `-O`.

## Optional numerical exploration

`explore_w.py` searches the open six-site scalar inequality with 1,000 seeded
local starts, including the known extremizer. It requires NumPy and SciPy:

```sh
.venv/bin/python computations/balanced-frontier-2026-09-27/explore_w.py > /tmp/w-exploration.json
```

`exploration.json` records versions, feasibility counts, an objective-gradient
check, and the best candidate. It is excluded from exact acceptance and from
the proof receipt's content hashes. Local numerical optimization cannot prove
the global scalar inequality or unrestricted W optimality.
