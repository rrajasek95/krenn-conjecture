# Read-only storage audit at accepted round 1442

Status: `PASS_READ_ONLY_PRUNE_PLAN_NOT_EXECUTED`. No file was deleted.

Only 101 MiB was free when audited. The accepted restart frontier is stage14 at round1442: checkpoint `094c339af0be4684323f4d576b0b608d521da76bb44083b71c4c65a9425e4bdb`, cache `1fd9cd661feef3957c0dda310b3213ff11784a48c520b76d73323e950a9db7c1`, result `7a157be7945ad11362e9b98c694d532ea0341978fa4c9215c98378a25a8d31da`, watchdog `8962c07b2c0a1bf024175301afb68380dad67b6f5a532c6153030f4636c4ccc1`.

Do not prune any accepted stages 01–14 yet: their independent edge audit has not been sealed. Preserve the exact stage14 state, the sealed round1363 input, frozen engine/provider, small result/watchdog/log records, and Stage 15 failure telemetry.

The preferred reclamation target is the independently sealed older `production_from_round1262_portfolio_cap1500/stage01..stage09` set: 25.013 GiB logical. Its stage10 endpoint remains preserved, and audit `bd17df82…` already records exact descendant/cache checks. Removing those old intermediate artifacts will make that historical manifest non-replayable, so its manifest and an intentional-compaction record must be retained.

Additional candidates are the sealed round1343→1362 intermediate stages01–02 (6.277 GiB), redundant round1363 portfolio/control copies identical to the retained cap2000 candidate (6.453 GiB), and the unaccepted Stage 15 clone (3.959 GiB logical, probably much less physical due APFS sharing). Check `df` after each approved deletion because clone-aware reclamation can differ from `du`.
