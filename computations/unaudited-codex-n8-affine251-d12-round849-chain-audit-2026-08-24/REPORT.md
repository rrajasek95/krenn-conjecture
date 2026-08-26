# D12 exact four-stage chain through round 849

## Verdict

`PASS_EXACT_ROUND849_CHAIN_WITH_STAGE01_RESOURCE_CAVEAT`.

The algebraic chain from the sealed round-749 state through round 849 is exact,
no-gap, target-normalized, and resumable.  Stages02–04 are fully telemetered
watchdog-v2 passes.  Stage01 retains its previously sealed, non-retroactive
resource/provenance quarantine; its algebraic output is nevertheless exact and
is accepted as the first chain edge.

Round 849 is `INCOMPLETE_SEARCH_CAP/ROUND_CAP`.  This report does not claim a
terminal global dual or completion of the D12 search.

## No-gap chain

The four supplied stages contain exactly the 100 records for rounds 750–849:

| Stage | Rounds | Columns | Added | Final support | Native status |
|---|---:|---:|---:|---:|---|
| 01 | 750–778 | 334,298 → 368,432 | 34,134 | 556 | wall cap |
| 02 | 779–805 | 368,432 → 405,259 | 36,827 | 518 | wall cap |
| 03 | 806–829 | 405,259 → 442,452 | 37,193 | 556 | wall cap |
| 04 | 830–849 | 442,452 → 460,676 | 18,224 | 312 | round cap |

The aggregate is 126,378 new columns.  Every round number is present exactly
once and every `columns = previous_columns + new_columns` identity holds across
stage boundaries.

All five checkpoints (start plus four outputs) pass the native `AFF12CEG1`
header, prime, count, support, canonical total-order, exact-EOF, and target-row
coefficient-1 checks.  Each checkpoint column set contains its complete
predecessor with exactly the stage delta above.

Complete record-level cache comparisons establish:

- sealed stage01→02: all 368,432 input records unchanged, plus 36,827;
- stage02→03: all 405,259 input records unchanged, plus 37,193;
- stage03→04: all 442,452 input records unchanged, plus 18,224.

Provider fingerprint remains `9218588987274412661` throughout.  The final
cache fingerprint is `10032382362786725155`.

## Final round-849 replay

An independent streaming parser replayed every one of the 460,676 cached
columns and all 46,796,079 terms against the 312-row candidate.  It observed
800 candidate-hit terms, two target terms, and zero nonzero pairings.  The
final candidate target coefficient is exactly 1.

Replay result SHA-256:
`a2ea0f27800bf2d46b0367cf6e7eb5a9dba93af74f2d9400bd4a772cbc60046c`.

## Stage artifacts

Stage03:

- result `37c66605e3fc55c37d25445eae9c46773ccee280d69cf07071dcddf9ce319f53`
- checkpoint `63c48ef7beb77c022d73c9d5912b191e414faab7c33608277f52deb57766e452`
- cache `b9c2ab1382cfb1e3bcbeb2f814e384ecace292d8a06a45a136da9024d467de51`
- watchdog `fda7a511a221ebdc4f134730c4152467813c55edd87950cc97073a7d6c3e299e`

Stage04:

- result `ee0764c6496a9837024443c0fdcd6322b5fcba4770e015eaacf34188455832a7`
- checkpoint `ce87c58cf79ddebbc0f9ce39eb36f08b6bf85a8f0f764f7728c3565da13fab49`
- cache `040b1b59bad7693fbd7ed71d8ff9f760b39b30943c77f452eae3b4047b5ac254`
- watchdog `80284d050ca6cd51e7c14b4d3dfd6ca53dcc0c2a51208a8c5ef7e63df78ebddf`

The machine ledger also pins the round-749 start, stages01–02, sealed prior
audit results, v3 source/binary, and watchdog-v2 source.

## Resource evidence

Stages02–04 each have watchdog schema v2, exact source/binary/command pins,
breach null, child return code zero, final logs, clean atomic outputs, and no
remaining temporary paths.  Their live libproc evidence is:

| Stage | Samples | Peak KiB | 36-GiB cap KiB | Last-sample→exit |
|---|---:|---:|---:|---:|
| 02 | 387 | 7,687,664 | 37,748,736 | 0.258587 s |
| 03 | 387 | 7,230,160 | 37,748,736 | 0.256807 s |
| 04 | 306 | 7,942,672 | 37,748,736 | 0.258025 s |

Stage01 has exact state/replay evidence but no persisted watchdog telemetry;
its logs remain `.tmp`.  Its resource/provenance verdict therefore remains
`REJECT_QUARANTINE_RESOURCE_PROVENANCE`.  Later stage telemetry cannot repair
that historical evidence gap.

## Scope

This referee hashed supplied artifacts, parsed checkpoints, compared exact
cache records, audited telemetry, and streamed the final cache.  It did not
evaluate provider columns, run elimination, or continue to round 850.

