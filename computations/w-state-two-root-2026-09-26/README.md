# Exact support for the all-even two-root W-state optimum

**Written theorem; independent audit pending.**

[Proof](../../notes/w-state-two-root-optimum-2026-09-26.md) ·
[Illustrated guide](../../explainers/BOUNDARY-STRUCTURE.md)

For every even site count, two unrestricted roots with an arbitrary complex
scalar ground-color core have the same exact optimal normalized rate as one
root. The connected case reduces to one root; every disconnected case has a
strict quantitative gap, proved using a published subhafnian norm inequality.
Arbitrary colored cores remain open.

Run from the repository root with Python 3.10+; no third-party dependencies:

```sh
python3 computations/w-state-two-root-2026-09-26/verify.py > /tmp/w-two-root.json
diff -u computations/w-state-two-root-2026-09-26/results.json /tmp/w-two-root.json
python3 -O computations/w-state-two-root-2026-09-26/verify.py > /tmp/w-two-root-optimized.json
diff -u /tmp/w-two-root.json /tmp/w-two-root-optimized.json
```

The replay checks the exact polynomial gap identity, the induction identity
for the reciprocal-power estimate, the equivalent constants for 48 even
orders, a four-site connected reduction, and exact disconnected examples at
six, eight, and ten sites. Acceptance checks remain enabled under `-O`.

The all-orders theorem is the written inequality argument, not an inference
from the checked orders. Earlier proof and code dependencies are pinned by
SHA-256 and are not edited by this package.
