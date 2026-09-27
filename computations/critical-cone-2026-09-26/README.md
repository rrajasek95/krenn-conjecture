# Exact cubic-extension obstruction at the critical core

[Proof and interpretation](../../notes/critical-cone-extension-obstruction-2026-09-26.md) ·
[Illustrated guide](../../explainers/BOUNDARY-STRUCTURE.md)

The saved sixteen-cell direction cancels all quadratic output but has a
nonzero quartic expression. A four-word exact left-null certificate proves
that no choice of the 135 complex second-jet entries can cancel its cubic
error. This is a rejected candidate direction, not a counterexample to the
square-root rate law or a classification of the remaining directions.

Python 3.10+, standard library only, from the repository root:

```sh
python3 computations/critical-cone-2026-09-26/verify.py > /tmp/critical-cone.json
diff -u computations/critical-cone-2026-09-26/results.json /tmp/critical-cone.json
python3 -O computations/critical-cone-2026-09-26/verify.py > /tmp/critical-cone-optimized.json
diff -u /tmp/critical-cone.json /tmp/critical-cone-optimized.json
```

`verify.py` checks the saved exact fixture independently of the exploratory
search: all 729 quadratic coefficients, the nonzero quartic, all 135 columns
of the cubic extension equation against the witness, and two negative controls.
Acceptance checks remain enabled under `-O`.

`probe.py` searches finite-field sections; `exact_probe.py` constructs and
simplifies a characteristic-zero example and solves its extension equation.
These discovery scripts are not substitutes for the acceptance certificate.
Earlier dependencies are pinned by SHA-256. Independent audit is pending.
