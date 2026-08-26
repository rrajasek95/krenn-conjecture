# D12 exact five-stage production through round 950

## Verdict

`PASS_EXACT_FULLY_TELEMETERED_ROUND950_CHAIN`.

The accepted round-850 portfolio state continues through exactly rounds
851–950 with no missing or duplicate round, no persisted-column drift, target
coefficient 1, complete watchdog-v2 evidence, and zero pairing on every final
cached column.  All production and aggregate resource gates pass.

Round 950 is `INCOMPLETE_SEARCH_CAP/ROUND_CAP`; this is an exact resumable
state, not a terminal global dual or a completion claim for D12.

## Input and no-gap chain

The input is the independently accepted cold/rare round-850 portfolio state:

- checkpoint SHA-256 `c2ea7cc0b72218e06866c3db2bd3a269a7ccdbdbf276132e62415d23a23f0fa7`
- cache SHA-256 `df181c0b86de9a2827d1146a318682482b9af2cae66b470fdf5d11fa036d1ec4`
- state: 461,464 columns, support 327, target coefficient 1.

The five stages contain exactly 100 round records:

| Stage | Rounds | Columns | Added | Support | Native status |
|---|---:|---:|---:|---:|---|
| 01 | 851–873 | 461,464 → 482,702 | 21,238 | 395 | wall cap |
| 02 | 874–894 | 482,702 → 504,463 | 21,761 | 393 | wall cap |
| 03 | 895–915 | 504,463 → 527,037 | 22,574 | 454 | wall cap |
| 04 | 916–934 | 527,037 → 545,580 | 18,543 | 393 | wall cap |
| 05 | 935–950 | 545,580 → 563,342 | 17,762 | 518 | round cap |

The aggregate is 101,878 new columns.  Every round satisfies the exact running
column recurrence across stage boundaries.

All six checkpoints (input plus five outputs) pass the native `AFF12CEG1`
schema, prime, header census, canonical total orders, exact EOF, and target-row
coefficient-1 checks.  Exact record-level scans establish that every cache
preserves all predecessor records byte for byte and adds exactly the stage
delta shown above.  Provider fingerprint remains `9218588987274412661`.

## Final round-950 replay

The independent streaming referee replayed all 563,342 cached columns and
57,278,657 terms against the 518-row candidate.  It observed 1,363
candidate-hit terms and two target terms, with `verification_failures=0`.
The final cache fingerprint is `9367659149255904209`.

Replay result SHA-256:
`96cc92350d475b286abde2e9f44889a018d5da1a261ff42cb1ea3b167e0965e7`.

## Resource and atomic-output evidence

Every stage pins v3 source
`173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a`,
binary `8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a`,
and watchdog v2
`53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97`.
All commands retain prime, 16 workers, cold/rare hierarchical mode, 95-second
native wall, 36-GiB RSS, and round cap 950.

| Stage | Watched seconds | Samples | Peak KiB | Last-sample→exit |
|---|---:|---:|---:|---:|
| 01 | 97.834983 | 384 | 7,565,808 | 0.275136 s |
| 02 | 97.762423 | 384 | 6,894,624 | 0.256362 s |
| 03 | 100.124322 | 393 | 7,973,984 | 0.256463 s |
| 04 | 98.005648 | 385 | 8,193,568 | 0.256143 s |
| 05 | 82.018345 | 322 | 8,291,984 | 0.256384 s |

The watched aggregate is 475.745721 seconds, below 540 seconds.  The maximum
sampled RSS is 8,291,984 KiB, below the 37,748,736-KiB cap.  All telemetry has
breach null, return code zero, monotone live-child samples, final artifact/log
hashes, `atomic_outputs_clean=true`, and no remaining temporary path.

## Authoritative stage hashes

| Stage | Result | Checkpoint | Cache | Watchdog |
|---|---|---|---|---|
| 01 | `be91f5c18f8cf35fd6d581f123a02fb9bd60773e54e99fcf615c5ad65b26f33c` | `c8fd72320c101a2e37640dcbcf356de63175009ce906a373da9422096ea28762` | `43bf60dc6957a19cfc22966503df388b1087c5933914af67b49c8a80b5440e55` | `fcccb1b387eae4b3b317e2aa5ba2b5b0b233d279ffd108a179395d8c73edaf3f` |
| 02 | `faae5fbd37dc95874cf59ef810ae41b302602f4c61a4e9c902556594477bcade` | `792aa4b12b49b02fefe586824bd5db30f034e8a465c2a68f0a9dea96fd9a87c6` | `56932c40d0645a21eb439426d406ab70cd7b6012a27a71870d81616906ce95c2` | `b2fe563dfe3e048b00a9f911d9c0f0f88ee976717ecead5bfa5cf608f8427c9f` |
| 03 | `f9e22d28d46ea4b81a44366b6ddb43439a9311edb7e83b53b60046c48d9f8c12` | `d0dea4b47fa23339f27d62d551375bda39415cc470b2f1024ab5a5f92ed94d7c` | `7df080b98ea9c108d28bf0803a6533d1c2453a5becf0ee14aaabb6cc7aac6ed5` | `e0a6e233ea38fac4aaf34bf96f2aaba2da97fc9a0ec908d8b59aede5c5901806` |
| 04 | `8c9c501e3aeaacad7c7fa1baf12df375b44c6a5e9d84bbd3fa7159b5283f6750` | `976c2d51add31269563b030e53ef76601e75027943f55cdd2cfa1a38fdbc1330` | `635031957d98cd1267d8e398951f720c3295a3678c3199a36532f70fc1ed3e54` | `7547ff1c0e3e265c725b272f191281214d28ca8fd7022dd48e3b76b357bd179e` |
| 05 | `a799c4b7c78305cdc37b6465ad68a97336f1d2200a820ca5a112611e2a08383b` | `8eee9ce80e36b105d1b7d7a733628639b2ecadff302551367c86709804dcbb4b` | `1a8eeb6fe4467466a99089f833f519665af802b512bead394c86ed953c2c8def` | `092a7e3fddcf7a0489d6889069fcc5acf7764eaacb06263ef0bb474be41d0b8b` |

## Scope

This referee hashed the input and all stage artifacts, parsed six checkpoints,
compared five complete cache edges, audited all telemetry samples, and streamed
the final cache.  It did not evaluate provider columns, run elimination, or
continue to round 951.

