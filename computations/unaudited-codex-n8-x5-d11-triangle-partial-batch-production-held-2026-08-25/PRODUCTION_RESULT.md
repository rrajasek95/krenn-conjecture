# D11 deterministic partial-batch production result

Status: **PASS exact restart checkpoint; resource-terminal at column cap.**

The one cleared p107 triangle run under launch acceptance `cdfe4d47...`
completed without watchdog breach.  It exhaustively scanned 762,110 unselected
incident columns, found 730,426 violations, retained the natural-order minimum
prefix fitting the 336,365 remaining slots, and atomically landed a
1,250,001-column / 1,378,456-support checkpoint.  Engine status is
`INCOMPLETE_COLUMN_CAP`; this is a restart checkpoint, not a mathematical
verdict.

Engine wall was 165.515125 seconds, wrapper wall 174.758121 seconds, and peak
RSS 18,207,312 KiB under 38 GiB.  Independent source-literal replay verified all
1,250,001 selected pairings with zero failures, target coefficient one, seed
subset preservation, every one of the 336,365 additions nonzero on the seed
dual, and equality of the first eight additions with the prior independent
top-eight gate.

- selected SHA-256: `3218c0c3b2dd357a12dc87fb8bc139e03379d5ef434166b6d481db9a34af98b5`
- dual SHA-256: `6ba8e603921e0c7c3eb1e92026e46aa42dde94bc18ed8452acf272d193cfbcdd`
- result SHA-256: `cbaade504ad2c10e8f7d0912ff1bdc0cdc2812ba41c391f9e6221581c6a24045`
- independent audit SHA-256: `8dbb4cd55a71af8d35bd4a4a9b8314da21589ba363c2cb61dffe60d68114a27a`

No p2, other branch, D12 read, or automatic relaunch occurred.  D12 resources
are clear after the completed independent replay.
