# Round 1442 to 1447 recovery

Verdict: **PASS_ATOMIC_RECOVERY_STOP_BEFORE_COLUMN_CAP**.

The distinct recovery attempt used a fresh APFS clone of the independently accepted round-1442 checkpoint/cache; it did not reuse or overwrite the failed stage-15 state. Frozen v4.1 cold/rare, 16-worker hierarchical nonincremental execution completed rounds 1443–1447 and atomically published round 1447 with 1,970,322 exposed columns and dual support 2,136.

The native process stopped on its 90-second wall gate (99.730982 seconds including cache publication). The sealed watchdog returned PASS in 100.241902 seconds, observed peak RSS 24,894,816 KiB under the 36 GiB cap, recorded 393 samples, and confirmed clean atomic outputs.

Pinned outputs:

- result: `a313bf00b597c3253edc32e33550ad4a0bb83d539e31eb77d3b34e6c617c22c6`
- checkpoint: `82d53e68e3f1bd483518996fed2dbffa80910163e8c7234f9ccce7c88afeb3cb`
- vector cache: `b806d22cac98ce4dd45928baf01401a8a7afaa12fcbd6d9c56f07cb1f9dab091`
- watchdog: `81c27fe5f12c066645f64f5620570af8c2d463dcbc520e5b065ce7a959e650c7`
- stderr: `fd48fe7dd3d7fe5d3d02854f45f204d903ab6a0a60420dd2ea883247fb5bd538`

Production is intentionally held. Only 29,678 columns remain under the 2,000,000-column cap, versus recent growth near 4,700 columns per round. A further stage requires an independent cap-extension equivalence gate from this exact round-1447 pair.
