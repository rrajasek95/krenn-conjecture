# D12 r1640 cap4.25m v3 attempt2 producer report

Status: **PASS_EXACT_R1640_DESCENDANT_HELD_FOR_INDEPENDENT_FULL_REPLAY**.

The independently approved resource-only retry reached exactly r1640 in one atomic round. The result is `INCOMPLETE_SEARCH_CAP / ROUND_CAP`, with 4,069,711 columns, 76,616 support rows, and no r1641. Native time was 196.456243s; the external watchdog passed in 198.715821s with no breach, atomic outputs, and peak RSS 21,528,480KiB below the 36GiB contract.

A record-aware canonical merge verified all 3,968,369 input cache records byte-for-byte and found exactly 101,342 new records. A parsed checkpoint set comparison likewise preserved all input columns and found exactly 101,342 new columns; the normalized target coefficient remains 1. The parser is pinned at SHA `976dba4...`. A raw byte-prefix comparison is intentionally not used because the cache rewrites its fingerprint/count header and inserts new records into canonical sort order.

The result/checkpoint/cache hashes are `896a0763...`, `12f79c86...`, and `1d7ce92a...`. This producer validation does not substitute for the required independent descendant scan and full 4,069,711-column replay. Continuation and r1641 remain forbidden until that referee passes and the manager separately authorizes further work.
