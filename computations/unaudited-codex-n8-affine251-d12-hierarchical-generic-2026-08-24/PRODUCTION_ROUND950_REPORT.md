# D12 hierarchical production continuation through round 950

## Verdict

Producer chain `PASS`: the frozen v3 cold/rare/16-worker hierarchical,
nonincremental solver advanced exactly rounds 851--950 from the independently
accepted round-850 state.  The terminal state has 563,342 exposed columns and
a 518-row candidate and stopped at the requested `ROUND_CAP`.  This is a
resumable search state, not a D12 completion claim.

## Exact chain

| Stage | Rounds | Columns | Support | Watchdog wall (s) | Peak RSS (KiB) |
|---|---:|---:|---:|---:|---:|
| 01 | 851--873 | 482,702 | 395 | 97.834983 | 7,565,808 |
| 02 | 874--894 | 504,463 | 393 | 97.762423 | 6,894,624 |
| 03 | 895--915 | 527,037 | 454 | 100.124322 | 7,973,984 |
| 04 | 916--934 | 545,580 | 393 | 98.005648 | 8,193,568 |
| 05 | 935--950 | 563,342 | 518 | 82.018345 | 8,291,984 |

All 100 round indices occur once.  Aggregate watchdog wall is 475.745721
seconds, below 540 seconds.  Every stage has complete race-fixed libproc
telemetry, return code zero, no breach, clean atomic outputs, and peak RSS below
the 37,748,736-KiB cap.

## Frozen lineage

The accepted round-850 checkpoint/cache are
`c2ea7cc0b72218e06866c3db2bd3a269a7ccdbdbf276132e62415d23a23f0fa7`
and
`df181c0b86de9a2827d1146a318682482b9af2cae66b470fdf5d11fa036d1ec4`.
Producer source, binary, and watchdog v2 are respectively `17382802...`,
`86257213...`, and `53d95032...` (full pins in the result ledger).

The round-950 result/checkpoint/cache SHA-256 values are respectively
`a799c4b7c78305cdc37b6465ad68a97336f1d2200a820ca5a112611e2a08383b`,
`8eee9ce80e36b105d1b7d7a733628639b2ecadff302551367c86709804dcbb4b`,
and
`1a8eeb6fe4467466a99089f833f519665af802b512bead394c86ed953c2c8def`.

## Independent replay

The independent streaming referee replayed all 563,342 terminal cached columns
and 57,278,657 terms against the round-950 candidate.  It observed 1,363
candidate-hit terms, two target terms, and zero failed pairings.  Replay result
SHA-256 is
`96cc92350d475b286abde2e9f44889a018d5da1a261ff42cb1ea3b167e0965e7`.

All five adjacent cache edges also passed complete byte-record descendant
scans: `461464+21238`, `482702+21761`, `504463+22574`,
`527037+18543`, and `545580+17762`.  The independently sealed referee package
is
`computations/unaudited-codex-n8-affine251-d12-round950-chain-audit-2026-08-24`.
Its audit result, report, and manifest SHA-256 values are respectively
`8e60e9d33483bd493d1e16b4664382ecb56a62db4b4a10b71236b600a5e20c6e`,
`32274b46e0bc6be8fb16e33683d23700fe1459af91636d35b7c638238a200e9d`,
and `1e61b818d9a8aa85488a4b90a2f68934b65696fe2f4870764ef7942d78ca0ae0`.
