# Integration contract: 16-shard rare-rank materialization

## Exact implementation pins

- sibling source: `src/main.rs`, SHA-256 `d6e259fb67c9e51e3cd6c7c3d3684870a53c684584c0cf5b7fb1cc6b50a3ae44`;
- sibling binary: `target/release/d12_hierarchical_rank_gate`, SHA-256 `5ab53be4c8ae8770fec8bfb69c6f8d5e267386138d22b3b75787f10231e8a185`;
- restored native parent source consumed by every control: SHA-256 `241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0`;
- accepted configuration: 16 solver/materialization workers, 16 rank shards, existing binary merge arity 2.

Port the following sibling regions without changing the checkpoint/vector schemas or outer CEGAR policy:

- `FnvHasher` and `FastRankMap` at source lines 96--117;
- `row_hash` at line 555;
- `materialize_chunk` at line 561;
- `rank_equations_sharded` at line 594;
- the `rank_equations_sharded(raw_equations, frequency, workers_count, rank_shards)` call at line 1031.

Line numbers refer to the pinned source above and are advisory; the symbol names and source hash are authoritative.

## Deterministic equality proof

1. The old order sorts `(Row, frequency)` with comparator `(frequency, Row)`. The replacement consumes the frequency map into owned `(u32 frequency, Row)` tuples and uses natural tuple sort. These are exactly the same total order because `u32` and `Row` use the same `Ord`; a strict adjacent-order assertion is exhaustive over every realized row.
2. A row's rank is only its index in that sorted vector. FNV hashing never selects a rank or ordering. It selects one of 16 exact lookup maps by `row_hash(row) & 15`; ordinary collision resolution still compares the complete row key.
3. Every `(row, rank)` is inserted once, duplicate insertion is fatal, and the sum of shard-map sizes must equal the sorted-row count.
4. Each raw term is looked up by its complete row, retains its residue unchanged, and each compact equation is sorted strictly by rank with duplicate/order assertions.
5. Raw equations are partitioned into balanced contiguous source intervals. Thread handles are joined in interval order, and their compact equation vectors are appended in the same order. A final census requires exactly 246,321 equations.
6. The existing hierarchical solver then verifies every equation, requires candidate-map identity, writes the checkpoint, and requires the exact checkpoint SHA-256 `92185737bc273f112f91240ee58eb8d0b4cd842739490838ebd30c870b8b6155`.

All nine controls satisfy this proof. The three accepted 16-shard repetitions also land the same checkpoint. The previously sealed independent literal replay (SHA-256 `3f19e125292cb75e00fd2267f1f0dfd234735ca0095ddae6bed385fe38318a2d`) scans 246,321 columns/24,950,813 source-variable terms with zero failures against that exact checkpoint.

## Memory ownership and lifetime

- `frequency` is consumed, not cloned, into the owned `(frequency,row)` vector.
- `rows_by_rank` is formed once; the owned sort vector is dropped before shard-map construction.
- The rank buckets temporarily own `(row,rank)` pairs and are consumed by their map-building threads. The 16 maps jointly contain one copy of each row/rank association.
- Raw equations are moved into worker chunks; their term arrays are not cloned. Compact u32 equations are constructed in parallel, so raw and compact representations coexist transiently during conversion.
- Rank maps are immutable during conversion and dropped before hierarchical elimination. `rows_by_rank` and compact equations remain for backsolve and verification.
- Observed worst-process RSS across all controls was 2,800,779,264 bytes (2.608 GiB), versus a 36-GiB hard cap. Do not infer a later-round bound from round 660; retain the existing live RSS/wall gates.

## Native hook and fail-closed controls

Use this replacement only for the existing cold/rare hierarchical preparation path. Preserve the original path for unsupported strategies. Require exactly 16 workers and 16 shards for the promoted configuration. In the first generic integration control, run solve-only at an already exposed checkpoint and require:

- source/checkpoint/vector input pins;
- exact old/new sorted-row order and equation count;
- zero full-equation failures;
- exact candidate equality against the old path;
- byte-identical checkpoint;
- less than 120 seconds and 36 GiB;
- no incident search or continuation.

If any assertion fails, disable the optimized path. FNV collisions cannot change mathematical output, but an adversarial distribution can degrade performance; the resource gate remains mandatory.
