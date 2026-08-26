# Round-660 hierarchical geometry optimization gate

## Verdict

`PASS_EXACT_NONPROMOTION`: all 15 bounded configurations produced the byte-identical sealed round-660 checkpoint and verified every exposed equation, but no geometry change reliably improves the fair end-to-end solve beyond the sealed 2.610749x result. Keep the promoted 16-worker binary merge geometry unchanged.

The best single observation was 16 workers with merge arity 8: 3.272813 seconds fair solve, 2.666369x versus the sequential 8.726527-second baseline, 7.113607 seconds total, and 1,850,261,504 bytes peak RSS. That observation is exact but not stable enough to promote. Across three repetitions, 16x8 had a 3.520500-second median fair solve. Its median elimination-only time was 0.268323 seconds; combining that with the sealed common rank/materialization time of 3.075534 seconds gives 3.343857 seconds and 2.609719x, slightly worse than the sealed 3.342537-second/2.610749x result.

No continuation beyond round 660 was run, and neither the parent gate nor integration source was touched.

## Tested geometry

The sibling makes two deterministic geometry parameters configurable while retaining the original rare ordering, normalized exact arithmetic, full exposed-equation replay, candidate equality assertion, and checkpoint hash assertion:

- workers: 8, 16, 32, 48, and 64;
- merge arity: 2, 4, 8, and 16 where meaningful;
- richer local bases: the 8-worker cases double each local source interval relative to 16 workers;
- repeated comparison: three 16x2 controls and three 16x8 candidates.

All merge groups preserve contiguous source ancestry. Within each group, the left basis is retained and other bases are inserted in deterministic child order with each incoming basis sorted by rare pivot. Every run emitted the exact checkpoint SHA-256 `92185737bc273f112f91240ee58eb8d0b4cd842739490838ebd30c870b8b6155`, candidate support 352, and zero verification failures over 246,321 equations.

## Load-bearing measurements

| configuration | fair solve seconds | speedup | elimination-only seconds | peak RSS bytes |
|---|---:|---:|---:|---:|
| sealed 16x2 result | 3.342537 | 2.610749x | 0.267003 | 1,883,783,168 |
| 16x8 best observation | 3.272813 | 2.666369x | 0.260567 | 1,850,261,504 |
| 16x8 repeated median | 3.520500 | 2.478775x | 0.268323 | n/a |
| 16x2 repeated median | 3.423589 | 2.548941x | 0.297229 | n/a |
| 8x2 richer local bases | 3.507800 | 2.487749x | 0.302404 | 1,859,125,248 |
| 32x8 | 3.313253 | 2.633825x | 0.263791 | 1,860,648,960 |
| 48x8 | 4.041978 | 2.158974x | 0.311878 | 1,851,621,376 |
| 64x8 | 3.650768 | 2.390326x | 0.289405 | 1,866,334,208 |

The rare-rank/materialization pass accounts for roughly 3.0--3.7 seconds and is unaffected by merge geometry. Its run-to-run variation exceeds the observed wider-merge savings. The elimination-only 16x8 median is also 0.49% slower than the sealed elimination observation. Consequently the one 2.666x observation cannot support a production change.

All runs were separately bounded by 120 seconds and 36 GiB. The largest observed RSS in this package was 1,883,095,040 bytes; the slowest total wall time was 8.577021 seconds. Process inspection showed no competing affine/D12 computation before the benchmark series.

## Independent audit and recommendation

`audit_geometry.py` independently hashes the frozen vector fixture, sequential checkpoint, restored parent source, all 15 JSON results, and all 15 output checkpoints. It checks the configuration matrix, exact candidate/checkpoint identity, full-equation verification, and resource bounds, then recomputes the best observation and repeated medians. `validate_geometry.py` enforces the nonpromotion logic. Nine hostile mutations are rejected fail-closed, including false promotion/stability, checkpoint mismatch, hidden equation failure, missing run, continuation, and resource overruns.

Recommendation: **do not promote a geometry change**. Retain sealed 16 workers/arity 2. If a later optimization is pursued, target the serial rare-rank/materialization pass; merge geometry is only about 8% of the fair solve and has no stable headroom on this fixture.
