# Exact incremental rare-order design

Status: **READY, NOT RUN**. This sibling package compiles and its in-memory/tiny-cache controls pass, but it has not hashed or read either frozen ~1 GB production cache. `run_when_cleared.py` refuses to do so unless explicitly invoked with `--production-clear`.

## Result

The exact production comparator is the derived Rust tuple order `(checked-u32 frequency, Mono)`. At round 849 the sealed log records 27,357,752 ranked rows and 1.275067 seconds in `ordered_sort`. Round 850 adds only 788 columns and, from the exact cache byte delta, 80,267 terms. Re-sorting all 27.36 million tuples is therefore avoidable.

The proposed `RareOrderIndex` keeps one naturally sorted row vector per frequency. During a round, the existing frequency map records the current count and a touched-row set records which rows changed. At commit, each touched row contributes at most one removal from its old committed bucket and one addition to its final bucket. Those small deltas are sorted and merged with the already sorted bucket bodies. Iterating buckets by numeric frequency and each body by natural `Mono` order is definitionally the same total order as the sealed comparator; hash-table iteration never selects rank.

Multiple appearances of a row among the 788 new columns are folded before commit, so the row moves directly from its old to final frequency. New rows have no removal. Checked `u32` arithmetic, strict delta/bucket assertions, removal-subset checks, duplicate/collision checks, complete old-column descendant checks, cache fingerprint checks, and final full-vector equality make the gate fail closed.

## Compatibility

The index is in-memory only. Checkpoint and vector-cache schemas are unchanged. On restart, the current cache scan reconstructs the frequency map and then the bucket index; no new state is trusted from disk. The benchmark compares complete round-849 and round-850 order vectors and hashes. If that passes and is fast enough, a second cloned-source one-round replay must still reproduce checkpoint `c2ea7cc0...` and cache `df181c0...` before integration. The order-only theorem is strong—identical rank order supplied to unchanged deterministic materialization/elimination implies identical solve state—but the second replay remains the promotion guard.

## Memory

`Mono` is 13 bytes and `(u32, Mono)` is 20 bytes (verified by the compiled self-test). At 27,357,752 rows:

- persistent bucket payload: 355,650,776 bytes (339.18 MiB);
- current full owned-tuple sort payload: 547,155,040 bytes (521.81 MiB);
- required `rows_by_rank` payload in either implementation: 355,650,776 bytes;
- worst frequency-bucket headers through count 460,676: 11,056,248 bytes;
- both removal/addition vector-header tables: 22,112,496 bytes;
- at most 80,267 touched rows at round 850 (small relative to the census).

The frequency map's 8-byte `usize` value can be replaced by the 8-byte `{current:u32, committed:u32}` value, so the production index does not require a duplicate 27-million-key map. A conservative integrated projection is below 8 GiB, versus the sealed fixed cold/rare one-round peak of 5,220,304 KiB and the hard 36 GiB cap. The standalone equivalence gate intentionally holds baseline and indexed tuple vectors simultaneously; even that is projected below 8 GiB and is externally killed at 36 GiB.

## Gate and fallback

After explicit resource clearance, run `python3 run_when_cleared.py --production-clear` from this directory. It first verifies the frozen cache and binary SHA-256 pins, then watches the read-only gate at 120 seconds/36 GiB. Acceptance requires exact internal cache fingerprints, all 460,676 old columns present in the 461,464-record descendant, exact baseline/index order equality and SHA-256 at both rounds, and no cache/checkpoint write.

Promotion requires all exact guards plus repeatable order-phase speedup of at least 1.5x; otherwise keep the sealed full sort. Any invariant or resource failure discards the experimental in-memory state and falls back to the existing source—never to a partial order. The tiny positive cache and corrupted-magic hostile pass; no production cache was opened by those controls.
