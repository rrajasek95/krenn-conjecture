# D12 hierarchical production continuation through round 849

## Verdict

`PASS_EXACT_ROUND849_CHAIN_WITH_STAGE01_RESOURCE_CAVEAT`.

Starting from the accepted round-749 checkpoint/cache, the frozen hierarchical
producer advanced exactly 100 rounds to round 849.  The final state has 460,676
exposed columns and a 312-row candidate.  It stopped at the requested
`INCOMPLETE_SEARCH_CAP/ROUND_CAP`; this is a resumable state, not a terminal
global dual and not a D12 completion claim.

The independent audit package is
`computations/unaudited-codex-n8-affine251-d12-round849-chain-audit-2026-08-24`.
Its chain result SHA-256 is
`156b55fc8f86c2f842d02875854e15f0d81ec3d9236b8c33a8c2fe40a2f9743e`.

## Exact chain

| Stage | Rounds | Columns | Support | Stop | Resource verdict |
|---|---:|---:|---:|---|---|
| 01 | 750–778 | 368,432 | 556 | wall cap | telemetry incomplete |
| 02 | 779–805 | 405,259 | 518 | wall cap | PASS |
| 03 | 806–829 | 442,452 | 556 | wall cap | PASS |
| 04 | 830–849 | 460,676 | 312 | round cap | PASS |

All round indices 750–849 occur exactly once.  The chain adds 126,378 columns.
The independent referee verified each checkpoint header/order/count/target and
each cache descendant edge byte-for-byte: stage01→02 retains all 368,432 input
records and adds 36,827; stage02→03 retains 405,259 and adds 37,193; stage03→04
retains 442,452 and adds 18,224.

The final checkpoint SHA-256 is
`ce87c58cf79ddebbc0f9ce39eb36f08b6bf85a8f0f764f7728c3565da13fab49`.
The final 993,313,251-byte cache SHA-256 is
`040b1b59bad7693fbd7ed71d8ff9f760b39b30943c77f452eae3b4047b5ac254`.

## Final literal replay

The independent streaming referee replayed all 460,676 cached columns and
46,796,079 terms against the final candidate.  It observed 800 candidate-hit
terms, two target terms, target coefficient exactly one, and zero nonzero
pairings.  Replay SHA-256:
`a2ea0f27800bf2d46b0367cf6e7eb5a9dba93af74f2d9400bd4a772cbc60046c`.

## Resource evidence and caveat

The frozen producer remained source `1738280214…`, binary `8625721373…`, with
literal cold/rare/16-worker/nonincremental configuration throughout.  Stages
02–04 used race-fixed watchdog v2 `53d9503260…`; each has complete process-group
telemetry, no breach, return code zero, and clean atomic outputs.  Their peaks
were 7,687,664, 7,230,160, and 7,942,672 KiB, respectively, versus the
37,748,736-KiB cap.

The staged wall ledger is 372.796382 seconds, below the requested 540-second
aggregate budget.

Stage01's arithmetic is independently exact, but its frozen watchdog hit a
post-exit zero-member race before writing telemetry.  That stage therefore
remains `REJECT_QUARANTINE_RESOURCE_PROVENANCE`; later telemetry does not repair
the historical gap.  Its state is accepted only as
`PASS_EXACT_RESUMABLE_STATE`, pinned by `stage01/RECOVERY.json` SHA-256
`c1368b31b026920501ef847c41fd1f3b2f878a56548bf848cea3575226333d5b`.
