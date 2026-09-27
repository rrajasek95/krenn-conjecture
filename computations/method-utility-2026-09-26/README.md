# Reusable methods: exact research package

**Written analytic proofs with exact supporting replay; awaiting independent
audit. No new Lean verification. The unrestricted sharp GHZ rate remains open.**

[Illustrated guide](../../explainers/METHOD-UTILITY.md) ·
[W-state optimum](../../notes/w-state-optimal-design-2026-09-26.md) ·
[Response certificates](../../notes/reusable-response-certificates-2026-09-26.md) ·
[Integral-rate certificates](../../notes/integral-rate-certificates-2026-09-26.md)

## Replay

Python 3.10 or later; only its standard library is required for verification.

```sh
python3 computations/method-utility-2026-09-26/verify.py > /tmp/method-utility.json
diff -u computations/method-utility-2026-09-26/results.json /tmp/method-utility.json
python3 -O computations/method-utility-2026-09-26/verify.py > /tmp/method-utility-optimized.json
diff -u /tmp/method-utility.json /tmp/method-utility-optimized.json
```

Acceptance checks remain enabled under `-O`. Earlier sources are pinned in
`dependencies.json`; this package does not modify them.

## What the replay establishes

- Every one of 729 W6 output coefficients, a minimum-norm preimage certificate,
  the exact attained rate `1/65`, and the all-even formula's constants at
  4, 6, 8, 10, and 12 sites.
- All 729 coefficients and a minimum-norm certificate for a different complex
  core and a nonuniform complex weighted-W target.
- A two-quality design certificate with fidelity at least `99/100`, selected
  event probability at most `29/100`, and relative upper/lower gap below `1e-4`.
- The rational constants and matrix bound used for a radius `1e-6` core ball.
- Exact witnesses for the three-requirement relaxation gap.
- Monic polynomial identities and norm majorants for integral-dependence
  examples; exact matching expansions along three polynomial source paths.
- All 18,420 columns in the preceding cubic nonmembership certificate.
  The new consequence excluding direct holomorphic SOS is proved in the note.
- Rejection of corrupt upper bounds, unmet requirements, zero-output witnesses,
  false integral identities, wrong ideal powers, invalid norm majorants,
  invalid response norm bounds, and an indefinite holomorphic Gram matrix.

The universal W architecture theorem uses the written argument plus the
published sharp scalar hafnian inequality. Finite examples do not prove the
all-size theorem. The core-ball perturbation estimate and general two-quality
rank theorem are likewise analytic arguments, not consequences of sampling.

## Files and interfaces

| File | Purpose |
|---|---|
| `quality.py` | Build target/event constraints; verify actual source vectors and rational dual bounds; extend bounds to a core ball. |
| `search.py` | Optional numerical proposal using NumPy and SciPy, followed by exact validation. |
| `two-quality-problem.json` | A core and two output requirements. |
| `two-quality-certificate.json` | The accepted rational primal and dual data. |
| `polynomial.py` | Exact sparse polynomial algebra, integral certificates, and complete polynomial source paths. |
| `examples.py` | Explicit integral/path fixtures and W-state construction checks. |
| `shared.py` | Reuse pinned Gaussian-rational arithmetic and response routines. |
| `verify.py`, `results.json` | Supporting replay, negative controls, and hashes. |

Run another two-quality search with the repository's existing environment:

```sh
.venv/bin/python computations/method-utility-2026-09-26/search.py computations/method-utility-2026-09-26/two-quality-problem.json --output /tmp/new-two-quality.json
python3 computations/method-utility-2026-09-26/verify.py --quality /tmp/new-two-quality.json
```

Search refuses to overwrite an existing output. Numerical optimization can
fail, particularly at eigenvalue crossings; an unsuccessful search says
nothing about impossibility. Only an accepted certificate supplies a bound.

Core entries use the previous package's `cell: [p,q,i,j]`, `value: [real,imag]`
format. A quality has `kind: target` with sparse `word`/`value` entries, or
`kind: events` with a list of distinct words; `sense` is `min` or `max`, and
`threshold` is a rational probability. Targets are normalized internally.

`verify.py --integral FILE` accepts a certificate in the format produced by
`examples.toy_integral()` or `examples.prism_integral()`. A polynomial is a
list of `powers` and Gaussian-rational `coefficient` entries. In coefficient
group `j`, every term supplies a multiplier and exactly `j` error indices.
The checker tests the complete monic identity and its norm constant. It does
not discover integral relations or claim that bounded-degree failure is a
disproof.

`verify.py --arc FILE` accepts the format produced by `examples.prism_arc()`.
Each source cell carries its complete one-variable polynomial. The checker
expands all perfect matchings, computes desired/error orders, and flags
`s > 3*r`. It rejects paths without a nonzero source limit or without a
nonzero high-fidelity output asymptotic. These exact path checks are not a
complete search over all analytic degenerations.
