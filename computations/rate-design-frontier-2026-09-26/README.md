# Rate design frontier: reproducible research package

**Written research; not independently audited or Lean formalized.**

[Illustrated guide](../../explainers/RATE-DESIGN-FRONTIER.md) ·
[Aggregate margin and optimizer](../../notes/rate-design-frontier-2026-09-26.md) ·
[Prism optimum](../../notes/prism-optimal-rate-2026-09-26.md) ·
[Singular-boundary theorem](../../notes/singular-kernel-rate-exclusion-2026-09-26.md)

## Replay the saved certificates

Use Python 3.10 or later. Verification needs only its standard library.

```sh
python3 computations/rate-design-frontier-2026-09-26/verify.py > /tmp/rate-design.json
diff -u computations/rate-design-frontier-2026-09-26/results.json /tmp/rate-design.json
python3 -O computations/rate-design-frontier-2026-09-26/verify.py > /tmp/rate-design-optimized.json
diff -u /tmp/rate-design.json /tmp/rate-design-optimized.json
```

Both differences should be empty. All acceptance checks use exact rational
or Gaussian-rational arithmetic, and remain enabled under `-O`.

## Contents and evidence

| Artifact | Purpose |
|---|---|
| `core.py` | Build the fixed-core response, compute its fidelity ceiling, and check rational upper/lower rate certificates. |
| `search.py` | Use NumPy to propose a certificate, then accept it only after exact verification. |
| `prism-core.json` | Example five-site core; root site 5 remains free. |
| `certificates.json` | Four fixed-core frontier intervals at fidelity floors 0.9, 0.99, 0.999, and 0.9999. |
| `complex-certificate.json` | A genuinely complex source example. |
| `cycle-certificate.json` | A case with a degenerate maximizing eigenspace and exact fidelity ceiling 2/3. |
| `boundary.py` | Reconstruct the singular linear response and its bilinear kernel lift. |
| `singular-certificate.json` | Rational normal-equation solutions for the kernel projection and enlarged target projection. |
| `verify.py`, `results.json` | Complete supporting replay and source hashes. |

The singular checker proves a nine-dimensional kernel, verifies a 162-by-162
positive matrix after partial transposition, and proves an enlarged-space
fidelity ceiling of 11/20. Analytic perturbation estimates then give the
full-neighborhood ceiling 6724/8649. The new base passes all six old rank tests.

The replay also checks the high-fidelity aggregate-margin example, replays the
3,375-triple positive cover, checks prism identities and constants, compares
729 complex output coefficients with the root formula, and rejects corrupt
upper certificates, zero-output witnesses, and a corrupt boundary projection.
It rejects the invalid lower bound on unrestricted formal tensor coefficients;
the valid bound uses actual product vectors.

The analytic arguments establishing universal statements within their stated
classes are in the notes. These finite certificates are not an independent
audit. Existing arithmetic, matching-cover code, and rank routines are reused
as explicit dependencies. Earlier pinned packages and the exact all-orders
proof are checked for changes before replay.

## Optimize another fixed core

The optional search requires NumPy. The repository's existing virtual
environment can run the example:

```sh
.venv/bin/python computations/rate-design-frontier-2026-09-26/search.py computations/rate-design-frontier-2026-09-26/prism-core.json --fidelity 9999/10000 --output /tmp/new-rate-certificate.json
python3 computations/rate-design-frontier-2026-09-26/verify.py --certificate /tmp/new-rate-certificate.json
```

The search refuses to overwrite an existing output. Discovery is numerical;
the saved certificate contains rational entries and must pass the independent
verification step in `core.py` before it is written. This is a separation of
search from checking, not an independent mathematical audit.

To supply another core, use the format in `prism-core.json`: `root` is a site
index from 0 to 5, and each entry has `cell: [p,q,i,j]` with `p<q`, and
`value: [real, imaginary]` as rational strings. Omitted cells are zero; core
cells must not touch the root. The 45 witness coordinates are ordered by root
color, then increasing other-site index, then that site's color.

Search currently requires a positive fidelity floor strictly below the exact
ceiling. Numerical search or rounding can fail to find a certificate; failure
is not evidence that no design exists. A valid certificate optimizes only the
incident entries of its specified core. It is not a global architecture bound
or a direct Gaussian success-probability optimum.
