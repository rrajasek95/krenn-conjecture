# Independent terminal audit: r1641 retry3 SUPPORT_CAP

Status: **PASS_TERMINAL_SUPPORT_CAP_ZERO_COVERAGE_STOP_GEOMETRY**.

Retry3 exposed exactly 223,328 new columns, taking the cached system from 4,069,711 to 4,293,039 columns. Its deterministic solve produced support 464,887, exceeding support200k by 264,887. The guard returned atomic `INCOMPLETE_SEARCH_CAP/SUPPORT_CAP` with an empty round ledger at round 1640; neither r1641 nor r1642 was accepted.

The full producer manifest replayed. Independent header parsing confirms the checkpoint is round 1640 with 4,293,039 columns but the old 76,616-support candidate, and the vector cache has the same enlarged column count. The computed 464,887-support candidate was not committed. This exact hybrid is diagnostic evidence only: it is neither the audited r1640 input nor a valid r1641 descendant, and it must never be resumed or reused.

No dual or temporary output exists. The watchdog passed atomically in 505.836726 seconds, without breach, at peak 27,407,936 KiB below 36 GiB. Resource success does not change the zero-coverage mathematical verdict.

The geometry is stopped. A fourth wall escalation, continuation from the hybrid, or any claim of r1641/full replay acceptance is forbidden. No new D12 arithmetic was run by this audit.
