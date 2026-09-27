# Quantitative proof identities and a diagonal rate bound

Research package, September 26, 2026. **Not independently audited or admitted
to the certified proof spine.**

The [research note](../../notes/quantitative-proof-identities-2026-09-26.md)
proves a stability estimate for the finite response scaling equation, gives
the exact norm of the finite differential inverse, and constructs an
endpoint-error certificate directly from any diagonal two-color source.
It bounds all higher binary responses and original root-boundary residuals
by physical mixed-output error, then carries those bounds through a finite
covariance projection. A threshold argument handles arbitrarily small edges.
Together these give a written global rate theorem for every diagonal complex
three-color source on even \(n>4\) sites, with exponent \(4/(3n+2)\).
The constants are explicit but conservative. Arbitrary endpoint colors and
sharp global exponents remain outside the result.

See the [undergraduate guide and diagram](../../explainers/QUANTITATIVE-PROOF.md).

**Subsequent result:** the [general complex rate package](../general-complex-rate-2026-09-26/README.md)
uses this theorem to obtain an explicit exponent for arbitrary endpoint colors.
This package's pinned research note preserves the preceding diagonal-stage snapshot.

Run from the repository root with Python 3.10+ and no installed packages:

    python3 computations/quantitative-proof-identities-2026-09-26/verify.py

Expected result: a JSON report with status PASS. The
[saved output](results.json) includes hashes of the checker and research note.
The checker also runs with Python's optimization flag: its checks use explicit
exceptions rather than removable assert statements.

The replay includes:

- Exact finite inversion over rational and Gaussian-rational coefficients.
- Examples attaining the inverse's coefficient-norm bound.
- Truncated exponentials attaining the scaling bound's exponent.
- A small-edge example disproving uniform differential stability.
- Direct partial-matching evaluation of the isotropic two-copy kernel.
- The weighted four-site allowed source, including a zero direct edge.
- A pure two-color source whose nonzero auxiliary residual demonstrates the
  necessity of the third-color or higher-response premise.
- General diagonal complex sources on four, six, and eight sites, without assuming
  zero mixed output or exact matrix rigidity.
- Three-color higher-response and root-boundary bounds on signed diagonal
  sources and a perturbed prism, including sharper source-specific constants.
- Full covariance projection identities through ten sites: every generator
  is checked, rather than a sample of matrices. Exact projection norms are
  computed from the resulting rational coefficient operators.
- Scalar differential-residual extraction on every projected generator.
- Six-, eight-, and ten-site rate constants and the error budgets in the
  larger/smaller-edge comparison.

The analytic theorems are proved in the note; the checker is supporting
evidence rather than an automated proof for all sizes. The package supplies
an explicit bound for the entire diagonal class; it does not supply an
explicit rate exponent for general endpoint colors.
