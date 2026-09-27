# Exact fifth-order onset for sparse first rows, with separate exploration tools

**Written branch theorem; independent audit pending.**

[Proof](../../notes/critical-core-fifth-order-branch-2026-09-26.md) ·
[Illustrated guide](../../explainers/BOUNDARY-STRUCTURE.md)

At the critical monochromatic core, a nonzero root row supported only in
ground color on at most two core sites, within the selected binary palette,
cannot produce a leading GHZ signal before order five. The theorem retains
all other first-jet entries and all later jets. It does not cover every
critical-core direction or prove the universal square-root rate law.

## Exact replay

Python 3.10+, standard library only:

```sh
python3 computations/critical-extension-search-2026-09-26/verify.py > /tmp/critical-extension.json
diff -u computations/critical-extension-search-2026-09-26/results.json /tmp/critical-extension.json
python3 -O computations/critical-extension-search-2026-09-26/verify.py > /tmp/critical-extension-optimized.json
diff -u /tmp/critical-extension.json /tmp/critical-extension-optimized.json
```

The checker verifies 30 resonant and 15 single-support or nonresonant cases
as full-color polynomial identities. Each resonant branch leaves 405 higher
source-jet entries free. Restoring the forbidden cells breaks the identity,
which is checked as a negative control. Acceptance stays enabled under `-O`.

## Exploratory scripts

`search.py` needs NumPy and explores binary sections over the finite field
of order 1009. It solves the quadratic kernel and the cubic extension equation.
Its generic scan reports 960 directions, 761 cubic extensions, and no surviving
nonzero quartic. These are finite-field observations, not a complex proof.

`identity_search.py` uses the standard library to search a degree-four modular
identity space. Neither a found modular identity nor failure in the specified
space is accepted as a characteristic-zero theorem. These scripts guided
the exact branch analysis; the acceptance checker does not call them.
