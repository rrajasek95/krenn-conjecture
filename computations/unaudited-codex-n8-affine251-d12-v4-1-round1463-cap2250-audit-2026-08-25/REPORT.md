# Independent r1448→r1463 chain audit

Verdict: `PASS_EXACT_FULLY_TELEMETERED_ROUND1463_CAP2250_CHAIN`.

Starting from the independently sealed, cap-equivalent r1448 state, four accepted stages cover exactly rounds 1449–1463 with no gap or overlap. Every checkpoint is a descendant of its input, and the four streamed cache-edge scans preserve all 1,974,608 / 1,997,710 / 2,023,738 / 2,044,569 inherited records byte-for-byte while adding exactly 23,102 / 26,028 / 20,831 / 4,960 new records.

The final r1463 state has 2,049,529 columns, support 2,389, and target coefficient 1. Independent all-column replay checked 209,414,806 terms across all 2,049,529 columns and found zero pairing failures. The final checkpoint SHA-256 is `1b4dde9f009b4343099190e293913818b3df88dfc34c27653e7cfcd4acf08c8e`; the final cache SHA-256 is `46744c37b6c1ab30e6ce945a9f049e45683b4324470e661554f4ae4134b9d48c`.

All four watchdogs passed atomically with aggregate elapsed time 377.318548 seconds and maximum RSS 24,813,808 KiB, below the 540-second / 36-GiB contracts. Producer ledger `d33cffa67e244d96ea46b7602efc7fe0a41038771ad8496f327090b129282e91`, producer report `8253bb52a983d27805591207208ee140cb5ebd587de6e99c6ec7532a9af2fa93`, producer manifest `3caad9c6eabef67291000f90ddbab02ffc90e775e8010b72aeb6131cb2aca9ec`, and the updated compaction record `0b427cca75426a1b667d8cb94376d9e5738be67c43a561b8437c4fd34cee2685` are pinned.

This is an exact resumable `ROUND_CAP` state. It does not establish closure or make a claim about round 1464.
