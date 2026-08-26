# Generic hierarchical integration audit

## Verdict

**PASS: promote the sealed generic hierarchical v3 kernel for its explicit
16-worker cold/rare mode.**  The exact round-748-to-749 A/B is byte-identical
to the native tree result, replays every cached column, stays below the watched
36 GiB limit, and solves in 2.585664 s versus 11.050344 s for tree: a
4.273697x speedup, strictly above the required 2x.

This supersedes the v2 fail-closed performance verdict.  It does not authorize
other pivots, strategies, worker counts, incremental mode, or an unbounded
continuation.

## Exact evidence

- The untouched parent source is pinned at SHA-256 `241ffd55...`.  The sealed
  v3 source is `17382802...`, and its binary is `86257213...`.
- The input is the accepted round-748 state: 333,199 columns, support 436,
  checkpoint `fe44b33e...`, and cache `7af04cec...`.  v3 loaded all 333,199
  cached vectors and materialized zero vectors during restore.
- Native tree and v3 reached round 749 with 334,298 columns and support 418.
  Their candidate/checkpoint bytes are identical (`dda7fb51...`), and their
  vector-cache bytes are identical (`93e3eeee...`).
- The independent compiled referee parsed the native formats/internal FNV and
  replayed all 334,298 columns / 33,907,235 terms against the candidate, with
  zero failures.
- The four persistence functions for checkpoint and vector-cache read/write
  are literally unchanged from the restored parent source, independently
  supporting native schema preservation and arbitrary resume.
- Eight parser-only hostile modes were rejected before I/O: wrong worker count,
  `first`/`last`/`auto` pivot, `repair`/`best` strategy, incremental mode, and
  unknown elimination.
- The macOS watchdog sampled the complete process group 39 times with
  `libproc`, observed peak RSS 4,676,672 KiB against 37,748,736 KiB, saw no
  breach, and accepted clean atomic outputs only.

## Sharded-rank integration

The independently sealed round-660 rank gate passed three exact repeats, with
rank/materialization times 0.756167, 0.766349, and 0.781537 seconds.  v3 ports
its correctness-critical contract:

1. Convert counts to checked `u32` and sort owned `(frequency, Mono)` pairs by
   natural total order.  This alone assigns the global rare ranks.
2. Use FNV-1a only to select one of 16 lookup-map shards.  FNV never selects a
   pivot and cannot alter the natural rank order.
3. Verify the 16 map shards cover the complete ranked-row census.
4. Split native sorted columns into 16 quotient/remainder contiguous slices,
   materialize compact `u32` equations in parallel, join handles in spawn
   order, and append chunks in that same source order.
5. Require strict rank order/no duplicates inside every equation, exact total
   equation count, deterministic merge order, and full-column pairing before
   returning.

The v3 phase accounting is:

| Phase | Seconds |
|---|---:|
| natural owned sort | 0.943361 |
| 16 FNV rank-map shards | 0.250911 |
| parallel compact materialization | 0.225443 |
| local worker wall | 0.062516 |
| fixed merge tree | 0.134990 |
| backsolve | 0.182981 |
| all-column verification | 0.672468 |

These account for 2.472670 of 2.585664 seconds.  The output log records
21,066,364 variables, 334,288 basis records, 34,083,985 basis terms, and shard
sizes 1,203,599 through 1,430,479.

## Scope

This referee performed source/schema checks, parser-only hostiles, and a
read-only cache replay.  It did not run an elimination, provider evaluation,
or CEGAR continuation.  Promotion is limited to the source-enforced
`--workers 16 --pivot rare --strategy cold --elimination hierarchical
--incremental no` interface with the existing per-run resource gates.
