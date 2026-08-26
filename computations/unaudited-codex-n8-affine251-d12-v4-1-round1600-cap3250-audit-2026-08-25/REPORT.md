# Independent D12 round-1600 chain audit

Status: `PASS_EXACT_FULLY_TELEMETERED_ROUND1600_CAP3250_CHAIN`.

The accepted cap-3.25m round-1588 state was independently followed through six exact, contiguous descendant edges covering rounds 1589--1600.  Checkpoint columns and cached invariant records are preserved byte-for-byte at every edge, with no gaps or overlaps.  The endpoint is round 1600 with 3,089,153 distinct columns, support 6,162, target coefficient 1, checkpoint SHA-256 `b0f8e3f0789f703577929f4b4612155da1fde7d16ad35d541d6bad8563881a6c`, and cache SHA-256 `acd25d4324fc20e67009d1f4e2e5b1fccb04571ba31cc5dc44f0e9e44d23e2a7`.

An independent one-pass binary replayed all 3,089,153 final columns and all 315,510,710 terms against the final candidate.  Every pairing is zero, the target coefficient is exactly 1, and the replay recorded zero verification failures.  The same scan independently checked checkpoint order/canonicality, cache/checkpoint equality, all six checkpoint descendant relations, all six cache descendant relations, inherited cache payload byte identity, and final cache fingerprints.

The producer source, binary, watchdog, input cap-equivalence audit, producer ledger/manifest, and compaction record are pinned in `results_round1600_chain_audit.json`.  All six stages pass atomic and telemetry guards.  Predeclared block watchdog sums are 352.461833 s and 353.115636 s, each below 540 s; maximum peak RSS is 24,879,776 KiB, below 36 GiB.

This certifies the exact exposed CEGAR state through round 1600 only.  It does not claim global closure, an all-orbit theorem, or any round-1601 continuation.
