# Rep2 groups26–75 conditional held-package referee

Verdict: **PASS / CONDITIONALLY HELD / ZERO RUNS**.

All 50 sources for canonical groups 26 through 75 were independently rebuilt
from the pinned rep2 contraction and authoritative census `5ee661f3...`.  They
match ledger `0a9ad8df...` byte-for-byte, total 92,375,796 bytes, and each has
91 variables and 6,577 generators.

The future groups1–25 dependency remains deliberately unsatisfied: both hashes
are null and both referenced terminal paths are absent.  Adapter `c4625a17...`
derives exactly the duplicate-free union 0–25 only from the required future
schema/status/order, and independently replayed mutations reject all 12
packaged hostile cases.  Consequently no normalized dependency exists.

Runner `2cdcfa47...` requires that normalized dependency before its exclusive
attempt marker and sole process launch.  It is sequential and stop-first, with
per-lane native/wrapper/RSS limits 240 seconds, 250 seconds, and 8 GiB; skip,
reorder, relaunch, and parallelism are forbidden.  No acceptance, clearance,
attempt, result, temporary, or solver artifact exists.  This seal is held-only
and adds no mathematical coverage.
