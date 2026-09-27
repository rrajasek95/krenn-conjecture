# Useful-consequences replay

New research deductions dated September 26, 2026. **Not independently audited
or admitted to the certified spine.** Read the
[written proofs](../../notes/useful-consequences-2026-09-26.md) and
[illustrated explanation](../../explainers/USEFUL-CONSEQUENCES.md).

Run from the repository root with Python 3.10+; only the standard library is used:

```sh
python3 computations/useful-consequences-2026-09-26/verify.py
python3 -O computations/useful-consequences-2026-09-26/verify.py
```

The checker:

* pins the exact upstream proof texts by SHA-256;
* enumerates the prism's four matchings by two methods and expands their words;
* checks all 19,683 occupation vectors with 0, 1, or 2 pairs in each source;
  any occupation >=2 fails exact one-photon-per-site selection, so higher
  emissions are excluded analytically as well;
* verifies fidelity, source normalization, and the full squeezed-vacuum
  probability on exact rational controls;
* verifies the pump derivative as an exact two-variable polynomial identity;
* checks the leakage slice identity and Cauchy–Schwarz bounds with rational
  positive and negative weights, and preserves the off-color limitation;
* checks allowed binary cycles, the two-site exception, and the nonbipartite
  four-site example; rejects edge-weight and derivative mutations.

The all-size bipartite exclusion, compactness argument, and Jensen proof of
optimality remain written mathematical proofs. Finite controls do not certify
them at every order. `PASS` does not constitute repository admission.

[prism.json](prism.json) defines the construction.
[calibration.csv](calibration.csv) gives rounded values computed at 70 decimal
digits. [verification.json](verification.json) records the checks. To make new
copies, choose output paths that do not exist:

```sh
python3 computations/useful-consequences-2026-09-26/verify.py \
  --output /tmp/useful-consequences-receipt.json \
  --calibration /tmp/useful-consequences-calibration.csv
```

The calibration is an ideal lossless postselection probability for balanced
prism sources. It is not a device count-rate forecast, a heralding probability,
or an upper bound across all architectures. The independent-source vacuum
factors are included exactly, not truncated at low gain.
