# v4 integration handoff

This is an order-only optimization. The gate did not solve a round or emit a checkpoint/cache. Its exact contract is complete equality of the natural `(checked-u32 exposed_frequency, Mono)` rank stream. The accepted round-850 checkpoint/cache pair was independently rehashed, but an integrated v4 one-round A/B remains mandatory.

## Source to lift

Pinned source: `rare_order_index_gate.rs`, SHA-256 `594b7d0976e9d3f648512b966a49da0c92702ddaf6293c3edcbb496643efc85d`.

- `Entry`: line 35.
- `RareOrderIndex`: line 40.
- `RareOrderIndex::from_frequency`: line 47.
- `RareOrderIndex::bump`: line 84.
- `RareOrderIndex::commit`: line 97.
- `RareOrderIndex::indexed_order`: line 198 (gate form returning `(frequency, Mono)`; production should add a direct `Vec<Mono>` flatten with the identical nested bucket iteration).
- `RareOrderIndex::baseline_order`: line 209 (audit/control only; do not retain on the optimized production path).

The load-bearing algorithm is the committed sorted bucket body plus one folded remove/add delta per touched row. Do not replace this with per-hit swap removal, unordered bucket iteration, or a different `Mono` canonical order.

## Minimal v4 wiring

1. Keep the sealed `exposed_frequency: HashMap<Mono, usize>` initially, to avoid changing non-hierarchical and portfolio consumers. After cache restore and the complete initial frequency scan, build one sibling `RareOrderIndex` using checked `u32` values from that map.
2. In the existing new-vector materialization loop, for each non-target/nonzero row, update `exposed_frequency`, call `rare_index.bump(row)`, and require the returned/current index count to equal the checked map count. This per-hit assertion prevents duplicated state from drifting.
3. After all new vectors for the round are inserted and before any hierarchical solve, call `rare_index.commit()`, then flatten buckets in ascending numeric frequency and each bucket in natural `Mono` order to one immutable `rows_by_rank` shared by the solver task(s).
4. Split `hierarchical_rank_and_materialize`: retain the 16-shard FNV rank-map construction and parallel compact equation conversion unchanged, but accept the precomputed `rows_by_rank` instead of collecting/sorting `frequency`. FNV remains lookup-only and cannot choose order.
5. Preserve the full frequency map for other pivot strategies. At the A/B gate, additionally assert every adjacent rank pair satisfies `(frequency[row], row)` strict order and the full rank SHA equals the v3 control. This expensive full-map guard may remain gate-only after integration is sealed.
6. Do not serialize `RareOrderIndex`. Rebuild it from the vector cache after every process restart. Checkpoint and cache byte formats, provider pins, column order, and result mathematics therefore remain unchanged.

The gate version of `bump` returns `()`. For the duplicated-map integration, change it to return the new `u32` count (or add an accessor) solely for the per-hit equality assertion; this does not alter its transition semantics.

## Exact v4 A/B acceptance

Use APFS clones of the same frozen round-950 checkpoint/cache for v3 and v4, exactly one round to 951, 16 workers, cold/rare, identical provider/prime/caps. Require:

- identical complete rank count and rank SHA;
- byte-identical checkpoint and vector cache outputs;
- identical non-timing round record and all-column annihilation replay;
- no input/production mutation and no continuation beyond 951;
- v4 `incremental_commit + flatten` faster than v3 `ordered_sort` and peak RSS below 36 GiB.

Any index invariant, map-count divergence, rank SHA mismatch, state mismatch, watchdog failure, or performance regression is a hard fallback to sealed v3 full sorting.
