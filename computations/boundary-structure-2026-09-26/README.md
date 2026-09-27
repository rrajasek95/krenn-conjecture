# Boundary structure: exact supporting package

**Written proofs awaiting independent audit. The unrestricted complex
square-root law and unrestricted W-state optimality remain open.**

[Illustrated guide](../../explainers/BOUNDARY-STRUCTURE.md) ·
[Regular triangle limits](../../notes/regular-triangle-rate-classification-2026-09-26.md) ·
[Diagonal support exclusions](../../notes/diagonal-support-rate-exclusions-2026-09-26.md) ·
[Two-root W reduction](../../notes/two-root-w-state-reduction-2026-09-26.md)

## Replay

Python 3.10+, standard library only:

```sh
python3 computations/boundary-structure-2026-09-26/verify.py > /tmp/boundary-structure.json
diff -u computations/boundary-structure-2026-09-26/results.json /tmp/boundary-structure.json
python3 -O computations/boundary-structure-2026-09-26/verify.py > /tmp/boundary-structure-optimized.json
diff -u /tmp/boundary-structure.json /tmp/boundary-structure-optimized.json
```

The checks remain active under `-O`. The earlier proof and quantitative files
are pinned by SHA-256 and are not edited by this package.

## What is checked

| File | Evidence |
|---|---|
| `exact.py` | Exact arithmetic in Q(omega), where omega is a nonreal cube root of unity; matching tensors and matrix ranks. |
| `graphs.py` | Enumerates all 32,768 six-site edge supports. Verifies every positive cover against all 15 matchings, and independently checks linear feasibility for every support. |
| `prism_jets.py` | A symbolic identity in 325 formal variables: every internal first jet and all second and third jets remain free. |
| `examples.py` | A completely singular diagonal limit, mixed-output reconstruction, four-site cofactor formulas, weighted-prism gauges, and two-root W examples. |
| `verify.py`, `results.json` | Combined evidence, negative controls, and pinned dependencies. |

The graph census finds 6,510 supports with a matching-cover certificate.
Its independent rank check uses arithmetic modulo 101. This is an exact
rational-rank certificate here: Hadamard bounds all relevant integer minors
strictly below 16 in absolute value, so none can vanish solely modulo 101.
The finite-rank calculation is not being generalized to larger matrices.

The critical five-site monochromatic core has all 15 four-site hafnians zero.
Therefore its six-site derivative is zero on all 135 source entries and all
six single-root response maps are zero. A different exact identity nonetheless
excludes a full **diagonal** neighborhood, with fidelity at most
`39205/117612` at radius `1/100`. The full-complex neighborhood is unresolved.

The prism jet calculation verifies

```
l * E3_protected - sum_h E2_left_h * E2_right_h = l^4.
```

Thus a first-order nonzero target with zero second-order error necessarily
has third-order error. The checker does not set the second or third source
jets to zero. The existing analytic local theorem also covers later leading
orders and nonanalytic approaches; this finite identity is a supporting
elimination certificate, not a replacement for that theorem.

The regular-triangle classification uses the whole-binary and omission
identities from sections 2--3 of the existing written proof, including their
three-site odd-core case. The finite replay checks cofactor formulas, six
four-site color assignments, 36 pairs of triangle color assignments, and all
729 coefficients of a full-complex gauge covariance example. Those examples
do not themselves prove the analytic classification.

The W examples include a connected nonbipartite cofactor graph with a singular
matrix: removing eight units of invisible source energy leaves every output
unchanged. A bipartite example has two active excitation roots and exact
W output at rate `48/4913`; it lies outside the reduction theorem and does
not beat `1/65`.

## Continuing the two research paths

The main target is the unrestricted complex six-site square-root law.
Regular disconnected-triangle limits are now covered by local bounds, but
rank-deficient triangle limits and other zero-output configurations remain.
The exact monochromatic Q(omega) core is a concrete severe test: its whole
first derivative vanishes, and off-diagonal perturbations escape the new
diagonal certificate. A next calculation should retain all endpoint colors
and analyze second and higher jets at that base. Since the other two pure
colors have no base entries, a first nonzero GHZ term there cannot occur
before order three.

The secondary target is W-state optimality with two unrestricted roots when
the cofactor graph is bipartite or disconnected. Alternating excitation
ratios survive there, as the exact example demonstrates. The missing step is
to optimize those genuine cancellation branches or prove a norm-preserving
reduction; the odd-cycle proof alone does not cover them.
