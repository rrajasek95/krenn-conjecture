# Independent r1464→r1484 short-chain audit

Verdict: `PASS_EXACT_FULLY_TELEMETERED_ROUND1484_CAP2500_CHAIN`.

Starting from the independently sealed r1464 cap-2.5m state, five stages cover exactly rounds 1465–1484 with no gaps or overlaps. All five checkpoint edges are descendants, and all inherited cache records are preserved byte-for-byte. The exact stage intervals are 1465–1469, 1470–1474, 1475–1479, 1480–1483, and 1484.

The final r1484 state has 2,142,848 columns, support 2,483, and target coefficient 1. Independent all-column replay checked 218,965,802 terms across all columns and found zero pairing failures. The final checkpoint SHA-256 is `2aa00dfd9e170aece91aa92321f3629f11a35afce43020452ec561dbf6ef7ac3`; the final cache SHA-256 is `4006f4d68afa7ad39d42d594757bc24a8a35d77f0dc9a4965d167a1b83d912bc`.

All watchdogs passed atomically. Aggregate elapsed time was 474.920176 seconds and maximum RSS was 25,372,336 KiB, below the 540-second / 36-GiB contracts. Producer ledger `d2ed13c78bd100d86a6f64c80d074e49c215770083d264b2793fa89f7f5a4a85`, report `9eca7d293c4325136e51e9d12687348ab4cbc862116d236edd4a4aefe3e40650`, manifest `9cb97f0957bbec51aca005be012517c5c188ce97bb3b968b7b023036886dd35d`, and updated compaction record `a589ec0f59f455b1c290c79b46e7d8196566ef68ab70c6b1f9481a5f90f069fe` are pinned.

This is an exact resumable `ROUND_CAP` state. It does not establish closure or make a claim about r1485.
