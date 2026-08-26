# Rep5 open84 same-stratum exact-Q conditional held pilot

This package is a zero-run, one-lane exact-Q continuation for the exact rep5 `k=2,t=1` open84 stratum. The 4,434,943-byte Q source is byte-identical to the v2 design source (SHA-256 `1e2f72c9...`) and retains the strong `slimgb`, basis-size, `reduce(1,G)`, and terminal-status transcript.

Admission is deliberately impossible in the sealed package. Four future producer/referee paths and hashes are null and `future_modular_unit_dependency.json` is absent. A later runner may proceed only after the independently sealed p32003 outcome is exactly `UNIT_IDEAL_MODULAR_DIAGNOSTIC`, both manifests replay, the same-stratum pins match, a new independent exact-Q acceptance is installed, and a fresh expiring manager/resource clearance passes the direct-libproc no-overlap census.

The runner permits one Q lane only, with native/wrapper walls 480/510 seconds, an 8 GiB process-group RSS cap, atomic result, and stop-after-any-outcome. Any attempt consumes the nonce even if process launch fails. Other strata, reuse of the consumed k0 timeout, parallelism, skipping, and automatic relaunch are forbidden.

The historical first modular held referee (`1c33eea1...`) is bound alongside the current superseding referee (`78ec2054...`); the current on-disk seal is replayed, while the historical hash is retained explicitly as provenance. This package has zero solver runs and no mathematical coverage.
