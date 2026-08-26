# Independent r1484→r1504 short-chain audit

Verdict: `PASS_EXACT_FULLY_TELEMETERED_ROUND1504_CAP2500_CHAIN`.

Starting from the independently sealed r1484 state, five stages cover exactly rounds 1485–1504 with no gaps or overlaps. Every checkpoint is a descendant and all inherited cache records are byte-identical. The exact intervals are 1485–1488, 1489–1492, 1493–1496, 1497–1500, and 1501–1504.

The final r1504 state has 2,256,332 columns, support 2,705, and target coefficient 1. Independent replay checked 230,581,991 terms across all columns and found zero pairing failures. The final checkpoint SHA-256 is `10807f9505b37832a29d17be7b02b4ac295db5e6fda4b11140c5d2e54b0e8a52`; the final cache SHA-256 is `2e52546ad403df0b5c45151f34350025fd3fe85262a8aa5423dff4cb3d31ccfd`.

All watchdogs passed atomically. Aggregate elapsed time was 522.860128 seconds and maximum RSS was 25,914,336 KiB, below 540 seconds / 36 GiB. The last stage reached the requested r1504 target and then reported `WALL_CAP`, not `ROUND_CAP`; no r1505 record was produced. This distinction does not affect the exactness or resumability of the accepted r1504 endpoint.

Producer ledger `fdd3dd6f9855e16ae8083a8d1c59e00ee585714f1278f715d14560a2ae10483e`, report `22c08c0c39c6668bde7522e9d92fd1220ac95cd33eddeadba0388921f268a110`, manifest `d1c447b8799e14d86541f137956e64c088f808d2d76682bf9efffe0c32741f28`, and compaction record `674e60bb37961cc48375086420415db2ec81cc0fb27d88009dd86f079d7b45e6` are pinned.

This is an exact resumable target-round state, not a closure result.
