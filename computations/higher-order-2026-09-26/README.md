# Higher-order singular behavior and the two-root W optimum

**Written proofs with exact supporting calculations; independent audit
pending. These are not additions to the Lean-verified proof.**

[Illustrated guide](../../explainers/BOUNDARY-STRUCTURE.md) ·
[Critical-core proof](../../notes/critical-core-higher-jets-2026-09-26.md) ·
[W-state proof](../../notes/two-root-w-connected-reduction-2026-09-26.md)

## Results and limits

* At the critical monochromatic core, a full-complex near-GHZ signal is
  at most fourth order in the distance to the core. A precise inequality
  includes both error and distance. Straight rays have limiting fidelity
  at most one third. Curved approaches at fourth or higher order remain open.
* Every exact W source with two unrestricted roots and a **connected**
  scalar-core cofactor graph reduces to one root without increasing source
  energy. Bipartite graphs and singular matrices are included, at every
  even site count at least six.
* At **six sites**, disconnected cofactor graphs satisfy the strict upper
  bound `1/144`. Thus the exact optimum for the whole two-root architecture
  is `1/65`, attained by the earlier complete-core design.

The W theorem still assumes that edges away from the two roots carry only
the ground color. It does not establish a universal optimum over colored
cores. At eight or more sites, disconnected cofactor graphs also remain open.
The unrestricted square-root rate law is not proved by the onset result.

## Replay

Python 3.10+, standard library only, from the repository root:

```sh
python3 computations/higher-order-2026-09-26/verify.py > /tmp/higher-order.json
diff -u computations/higher-order-2026-09-26/results.json /tmp/higher-order.json
python3 -O computations/higher-order-2026-09-26/verify.py > /tmp/higher-order-optimized.json
diff -u /tmp/higher-order.json /tmp/higher-order-optimized.json
```

All acceptance checks remain enabled under `-O`. `dependencies.json` pins
the preceding exact arithmetic, example definitions, graph helpers, proof
dependencies, and their recorded evidence. Those files are not edited here.

## What the checker establishes

`critical.py` uses 540 independent formal variables for all 135 entries of
each of four source jets. It checks all 729 first-order output coefficients,
the two cubic reconstruction identities, and the two quartic identities
modulo earlier output constraints. It verifies the finite-increment formula
on a full-complex example and rejects an identity missing a cover term.

`w_connected.py` checks three complex bipartite constructions, preserving all
729 outputs under the reduction and decreasing source energy. Two examples
have both excitation roots active, and the third tests the pure-type branch.
It checks the exact norm deficit and rejects an unbalanced transformation.
It also enumerates all 64 four-vertex supports and verifies the scalar
factorizations underlying the disconnected six-site bound.

These finite checks support the analytic proofs. They do not substitute for
the universal graph argument, the hafnian inequality, or independent audit.
