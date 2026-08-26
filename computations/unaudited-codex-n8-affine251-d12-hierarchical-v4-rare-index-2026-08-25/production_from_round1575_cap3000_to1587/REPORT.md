# Round1575 to round1587 producer report

Six accepted two-round stages cover rounds 1576–1587 without gaps or overlaps under the frozen v4.1 cold/rare hierarchical contract: prime 1073741827, 16 workers, nonincremental mode, 3,000,000-column cap, native 120-second wall, wrapper 150-second wall, and 36 GiB live RSS limit.

Block A covers rounds 1576–1581 in 311.178750 watchdog seconds. Block B covers rounds 1582–1587 in 329.973032 watchdog seconds. Every stage stopped naturally at its exact round cap with atomic watchdog PASS; maximum observed live RSS was 26,073,328 KiB.

After exact round1583, the next launch was held because free disk was 58,181,520 KiB, below the frozen 58,720,256 KiB floor. No stage05 work began. Root then removed only old checkpoint/cache payloads already sealed by the independent round1261 audit, recorded by compaction ledger SHA `e511bba126e2c0dbdfe65e0ab5964c8b55163d13db59f068fec2f46a063ae574`. The active chain was untouched, round1583 checkpoint/cache hashes were reverified, and free space recovered to 82,285,872 KiB before production resumed.

The exact endpoint is round1587 with 2,927,014 exposed columns and dual support 5,598. Result SHA is `a78f142ec4cf01cb0b2b94dc101b5fb7f80dd3f7d8a19460c90758f43a947a0c`; checkpoint SHA is `f8c334186186173654878c9f33f4c0d5f1911724e9c95cf5069b2fbd0c89f8aa`; vector-cache SHA is `38a4ff6bb1d8f0d39cb7c4914e0e549629fe37df069db2436874cb5ce51f41ae`. The producer is sealed and held for an independent six-edge descendant audit plus final all-column replay.
