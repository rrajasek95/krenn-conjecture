# Exact parallel rank/materialization gate at D12 round 660

## Verdict

`PASS_EXACT_REPRODUCIBLE_PROMOTION`: promote the 16-shard rare-rank construction and parallel compact equation conversion for the 16-worker cold/rare hierarchical solver. Across three interleaved repetitions, the dominant phase fell from a 3.037482-second median to 0.766349 seconds (3.9636x faster). The fair solve median fell from 3.297912 to 1.028965 seconds (3.2051x faster), giving an 8.480874x speedup over the sealed sequential 8.726527-second solve.

All nine controls produced the byte-identical sealed checkpoint, candidate support 352, and zero failures over all 246,321 equations. No continuation beyond round 660 was run. No parent or integration source was modified.

## Optimization

The promoted path combines three exact representation changes:

1. Consume the frequency map into owned `(frequency, Row)` tuples and natural-sort them. This exactly implements the old `(frequency,row)` comparator while avoiding repeated tuple reconstruction in the comparator.
2. Assign ranks by sorted index, then build 16 fixed-FNV lookup shards in parallel. Hashing only chooses the lookup shard; full row equality resolves keys, and hash-map iteration never chooses rank or equation order.
3. Move the raw equations into 16 balanced contiguous chunks and convert their terms to compact `(u32 rank,u32 residue)` form in parallel. Join and append chunks in source order, with exhaustive count and strict-rank assertions.

The sibling preserves the existing 16-worker/binary-tree elimination geometry. Configuration sweeps covered sharded maps with 1, 4, 16, and 32 shards plus three original-path baselines. Sixteen shards were the best reproducible choice: four shards gave a 1.074381-second fair solve, 16 gave 1.013664 seconds in its first run and 1.028965 seconds median, while 32 gave 1.027283 seconds once with no material advantage.

## Repeated measurements

| path | repetition fair solves (s) | median rank phase (s) | median fair solve (s) | median sequential speedup |
|---|---|---:|---:|---:|
| original baseline | 3.340815, 3.297912, 3.277622 | 3.037482 | 3.297912 | 2.646076x |
| 16-shard promoted | 1.013664, 1.028965, 1.044601 | 0.766349 | 1.028965 | 8.480874x |

In the first promoted run the rank subphases were 0.554269 seconds for owned tuple sort, 0.110963 seconds for shard-map construction, and 0.090934 seconds for parallel compact conversion. The promoted median peak RSS was 2,800,091,136 bytes; the maximum observed across all nine runs was 2,800,779,264 bytes (2.608 GiB), safely below 36 GiB. Every run completed in under 7.35 seconds total and below the 120-second wall gate.

## Exactness and referee

The source contains exhaustive adjacency, duplicate, shard-census, chunk-coverage, equation-order, candidate-equality, all-equation, and checkpoint-hash assertions. `audit_rank_gate.py` independently hashes all inputs, results, and output checkpoints, pins the existing independent 24,950,813-term literal replay, and recomputes the medians. The strict validator reports promotion PASS. Eleven hostile mutations are rejected fail-closed, including rank/source order changes, checkpoint mismatch, hidden equation failure, missing repetition, false speedup, continuation, and wall/RSS overruns.

The full deterministic-order proof, memory lifetimes, exact symbols, and generic integration controls are in `INTEGRATION.md`.

## Recommendation

Promote exactly `workers=16`, `rank_shards=16`, and the existing merge arity 2. Keep full equation verification and the live resource gates at every production round. This gate establishes the solve-only round-660 kernel and does not claim later-round memory or continuation performance.
