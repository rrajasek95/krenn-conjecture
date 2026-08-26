# Independent r1614 direct cap3.5m to cap3.75m audit

Status: `PASS_EXACT_DIRECT_CAP3500_TO_CAP3750_EQUIVALENCE`.

The independently sealed round-1613 state was pinned by audit, replay, manifest, checkpoint, vector-cache, and post-audit compaction hashes. Fresh control and candidate lanes used the same source, binary, watchdog, prime, worker count, strategy, pivot rule, elimination mode, time limits, and RSS limit. Their normalized commands differ only in the column cap, `3500000` versus `3750000`.

Both lanes terminate at round 1614 with 3,319,280 columns and support 6,349. The resulting checkpoints are byte-identical at SHA-256 `4c84bb8978083a0b2437bcc10730b40fc260fce90068f597c408789546c7f76e`; the vector caches are byte-identical at SHA-256 `ab1da9e006abd643b977fe1af879c9f7c7ee99b80be95ac82fcb71c9a960d88d`. Both results are atomic PASS states, no dual outputs exist, and no computation continued beyond round 1614.

The maximum observed wrapper elapsed time was 107.206217 seconds and maximum peak RSS was 20,245,376 KiB, within the frozen 150-second and 36-GiB hard limits. The accepted restart state is `candidate_cap3750`; this audit authorizes no continuation and makes no claim of D12 closure or conjecture completion.
