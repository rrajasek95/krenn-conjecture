# Independent D12 round-1627 cap-equivalence audit

Status: **PASS.** The cap-3.75m control and cap-4.0m candidate each restored the independently audited round-1626 state and executed exactly round 1627. Both produced 3,547,162 columns with dual support 7,888.

After removing timing fields and the declared cap, the one-round records, semantic result fields, and normalized commands are equal. The sole normalized configured difference is `--column-cap 3750000` versus `4000000`. Independent full-byte SHA-256 reads prove the two checkpoints are identical (`40a76f72...`) and the two vector caches are identical (`4ae60b26...`).

Both watchdogs passed atomically with no breach or dual output. Maximum watchdog elapsed time was 120.241367 seconds under the 150-second hard wrapper, and maximum RSS was 22,301,792 KiB under 36 GiB. The frozen source, binary, watchdog, input audit/replay/manifest, and post-audit compaction record all match their pins.

The accepted restart is `candidate_cap4000`. This is cap equivalence for one exact round only; it is not a closure certificate or a proof of the conjecture, and no continuation was run by this audit.
