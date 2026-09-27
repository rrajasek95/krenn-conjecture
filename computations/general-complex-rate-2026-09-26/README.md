# Explicit rate bounds for general complex sources

September 26, 2026. **Written research with supporting checks; not independently
audited or admitted to the certified proof spine.**

The [research note](../../notes/general-complex-rate-bound-2026-09-26.md)
gives a quantitative diagonal reduction and combines it with the preceding
diagonal theorem. The resulting rate exponent is
\(8/[n(3n+14)]\) for every even \(n>4\), allowing arbitrary complex endpoint
colors. The same exponent applies to every target dimension at least three.
Constants are explicit but conservative. The sharp global exponent remains open.

Read the [undergraduate explainer and diagram](../../explainers/GENERAL-RATE-BOUND.md).

From the repository root, with Python 3.10+ and no installed packages:

    python3 computations/general-complex-rate-2026-09-26/verify.py

Expected output is a JSON report with status PASS. The
[saved report](results.json) includes hashes of the note, checker, exact proof,
and preceding quantitative package. Checks remain active under `python3 -O`.
The checker imports Gaussian-rational arithmetic from the preceding package;
it is supporting verification, not an independent implementation or audit.

Coverage:

- 132 exact coefficient-division controls, including complex coefficients.
- Literal matching responses for two four-site sources, a perturbed six-site
  prism, and a dense complex six-site source, all with off-color entries.
- 204 full cubic omission polynomial identities and 306 cofactor polarization
  identities, including the repeated-root-color factor of two.
- Nine complete polynomial two-copy rotation identities on the sparse examples.
- Approximate common-scalar and cubic-response bounds. The very small off-color
  perturbation of the allowed four-site source satisfies the cofactor inverse
  hypothesis, exercising the conditional diagonal-reduction estimate.
- Exact rational budgets for six-, eight-, and ten-site rate constants.
- Three-color subset averaging and orthogonal projection through 12 target colors.

All complex polynomial identities use exact Gaussian-rational arithmetic.
For norm checks, the report labels the rational upper bounds `|Re|+|Im|`.
The arbitrary-size theorem is justified by the analytic note, not by
extrapolating these finite checks. Its dependency is the preceding written
[diagonal rate theorem](../../notes/quantitative-proof-identities-2026-09-26.md),
which also awaits independent audit.
