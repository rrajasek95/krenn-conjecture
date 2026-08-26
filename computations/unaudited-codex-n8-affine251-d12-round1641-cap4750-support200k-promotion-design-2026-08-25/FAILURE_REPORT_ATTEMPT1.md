# r1641 cap4.75/support200k attempt1 failure seal

Status: **REJECT_HARD_WALL_ZERO_COVERAGE**.

The independently approved single candidate was killed by the external 240-second wall at 241.229560s (return code -15). Peak RSS was 18,523,808KiB, well below 36GiB; the last successful sample at 240.167356s was only 2,688,096KiB, consistent with a late output/finalization tail rather than memory pressure.

No result, dual, or temporary file exists; stdout and stderr are empty. The checkpoint and vector cache rehash exactly to the audited r1640 input (`12f79c86...` / `1d7ce92a...`). Attempt1 therefore provides zero r1641 coverage and no resumable state. It is evidence only and must never be resumed or reused for a retry.

No relaunch or r1642 was attempted. Any retry requires a distinct fresh r1640 clone, a separately approved resource-only contract, and explicit manager clearance.
