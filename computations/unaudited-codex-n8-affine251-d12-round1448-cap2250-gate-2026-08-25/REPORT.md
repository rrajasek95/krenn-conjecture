# Round-1448 column-cap equivalence gate

Verdict: **PASS_EXACT_CAP_EXTENSION_EQUIVALENCE**. Production remains held pending independent light audit.

Two sequential one-round runs began from the independently audited round-1447 checkpoint/cache (`82d53e68e3f1bd483518996fed2dbffa80910163e8c7234f9ccce7c88afeb3cb` / `b806d22cac98ce4dd45928baf01401a8a7afaa12fcbd6d9c56f07cb1f9dab091`). Both used frozen v4.1 source/binary, cold/rare, 16-worker hierarchical nonincremental mode, native wall 90 seconds, watchdog wall 115 seconds, and the 36 GiB live RSS cap. They differed only in `--column-cap`: 2,000,000 for the control and 2,250,000 for the candidate.

Both runs stopped exactly at round 1448 with 1,974,608 exposed columns, support 2,131, 4,286 new columns, and 1,102 new support rows. Their checkpoints are byte-identical at SHA-256 `4a4ceb16738127a41af8f783265f745cccbf849b827f97d7e0618e609cf3055a`; their vector caches are byte-identical at `829028724fb39e37fd9ffb07d5d85094515a0a84e8634307fab17c2833e45007`.

After deleting file paths and timing-only fields, the exact normalized result difference is the singleton key `column_cap`; deleting that key makes the objects identical. The checker also rejects an in-memory changed-round hostile and a non-atomic-watchdog hostile.

Telemetry:

- control: native 57.957938 seconds; watchdog 58.634889 seconds; peak RSS 23,594,320 KiB; atomic PASS
- candidate: native 56.785024 seconds; watchdog 57.372459 seconds; peak RSS 22,970,448 KiB; atomic PASS

The candidate round-1448 pair is eligible as the input to future production only after the assigned independent audit seals this package.
