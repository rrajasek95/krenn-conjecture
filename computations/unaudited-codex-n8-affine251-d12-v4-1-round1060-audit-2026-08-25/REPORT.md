# Independent v4.1 round-1060 chain audit

Verdict: `PASS_EXACT_FULLY_TELEMETERED_ROUND1060_CHAIN`.

The audited round-961 input (`2fac10fb...` checkpoint, `8bce26ef...` cache) advances through five exact, non-overlapping stages: rounds 962–985, 986–1008, 1009–1029, 1030–1047, and 1048–1060. All 99 round records are gap-free, their column recurrences agree, and every checkpoint/cache edge preserves every inherited column or vector byte-for-byte. The final state has 729,800 columns, 152,155 new columns, support 826, and target coefficient one.

Every stage used pinned v4.1 source `3139689f...`, binary `79410bc8...`, and watchdog-v2. All telemetry reports natural, atomic exits with no breach. Aggregate watchdog elapsed is 478.579028 seconds, below 540; maximum sampled RSS is 11,883,200 KiB, below 36 GiB.

Independent final replay streamed all 729,800 cached columns and 74,296,977 terms, validated the cache fingerprint and target normalization, and found zero pairing failures. Final result/checkpoint/cache hashes are `ca3be36a...`, `1bc0315d...`, and `0d71ab7b...`.

Round 1060 remains `INCOMPLETE_SEARCH_CAP/ROUND_CAP`: this is a fully audited resumable state, not a terminal global-dual claim.
