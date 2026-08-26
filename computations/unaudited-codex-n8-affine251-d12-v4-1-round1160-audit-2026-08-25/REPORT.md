# Independent v4.1 round-1160 chain audit

Verdict: `PASS_EXACT_FULLY_TELEMETERED_ROUND1160_CHAIN`.

The accepted round-1061 portfolio input (`9927bfa1...` checkpoint, `acc0f960...` cache) advances through seven exact stages covering rounds 1062–1160 with no gap or overlap. All 99 round and column recurrences agree. Every checkpoint is an exact descendant with target coefficient one, and all seven cache edges preserve every inherited vector payload byte-for-byte. The final state has 959,506 columns, 227,598 new columns, and support 990.

Every stage uses pinned v4.1 source `3139689f...`, binary `79410bc8...`, and watchdog-v2. Block A's five-stage watchdog sum is 509.806545 seconds; Block B's two-stage sum is 173.761472 seconds, each below 540. All outputs are atomic and breach-free; maximum sampled RSS is 13,165,296 KiB, below 36 GiB.

Independent final replay streamed 959,506 columns and 97,784,365 terms, verified target normalization and the vector fingerprint, and found zero pairing failures. Final result/checkpoint/cache hashes are `0022c43b...`, `23d91d21...`, and `e622054e...`.

Round 1160 remains `INCOMPLETE_SEARCH_CAP/ROUND_CAP`: this is a fully audited resumable state, not a terminal global-dual claim.
