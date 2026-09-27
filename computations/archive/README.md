# Archived research outputs

The repository cleanup on 2026-09-26 moved these saved outputs out of the
repository root without changing their bytes:

- [candidates/](candidates/): 62 numerical candidate arrays (`candidate_*.npz`).
- [results/](results/): the historical `results_w38_gate_n6.json` report.
- [manifest.json](manifest.json): original paths, archive paths, and SHA-256 hashes.

These are research artifacts with their original scope; a numerical candidate
is not an exact solution certificate. The completed Lean proof and its
verification instructions are in the [main README](../../README.md).

Scripts accepting a candidate path can use the new repository-relative path,
for example `computations/archive/candidates/candidate_n6_q3_seed2.npz`.
Several historical generators write relative to the working directory; run
them from a separate output directory to keep generated files out of the root.
