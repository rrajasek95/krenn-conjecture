# Codex X4 all-blocked builder lane

Run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  computations/unaudited-codex-x4-allblocked-builder-2026-08-20/run_builder.py
```

The runner pins the hazards ledger and both calibration objects, writes only
`results_builder.json` in this directory, uses two raw hafnian engines on all
6,561 words, decides every live pair by exact Qbar Rabinowitsch saturation,
and certifies the W40 local-rigidity minors.
