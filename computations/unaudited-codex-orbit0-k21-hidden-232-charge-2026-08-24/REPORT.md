# Exact hidden D14 R2-3-2 K21 charge

## Verdict

`PASS_COMPLETE_D14_222_R_2_3_2_K21_CHARGE`, followed by
`PASS_INDEPENDENT_D14_222_R_2_3_2_K21_SOURCE_COUNT_SAMPLE_TERMINAL_REFEREE`.

The strict singleton contribution is

```text
D14:222|R:2-3-2
U                                      400591699200
full charge = irreducible charge       -879849881597204692992 / U
reduced                                 -381879288887675648/173867925
```

This closes exactly one K21 lineage ID.  It is an immediate scalar result,
not a K21 row checkpoint or a conjecture verdict.

## Exact retained source and response

The source is `hidden_k16_decorated_pair_orbits_full.bin`, SHA-256
`22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8`.
Its `H16ORM1` header and file size pin 101,545,723 nonzero 53-byte records,
each containing the exact decorated H-orbit
`(literal canonical K16 row, selected p2)`, signed coefficient after p2,
witness-use count, orbit size, and stabilizer size.

The decorated-H equivariance theorem is tail-degree independent.  Therefore
each retained representative emits its 32 K3 tails with the record's total
orbit mass.  For each literal K19 child the consumer recomputes every p3,
asserts exact division by its realized multiplicity, and evaluates all 12
terminal K2 tails.  Because the cycle functional is H-invariant, these scalar
values may be folded immediately: no canonical K19 or K21 child stream is
needed.

The full exact workload was:

| item | count/value |
|---|---:|
| decorated pair H-orbits | 101,545,723 |
| K3-to-K19 representative tail evaluations | 3,249,463,136 |
| pivotable K19 children | 1,067,611,872 |
| selected p3 uses | 1,774,721,368 |
| terminal K21 occurrences | 21,296,656,416 |
| response-cache hits | 1,662,908,870 |
| response-cache misses | 111,812,498 |
| exhaustive abstract terminal child checks | 1,341,749,976 |

Every realized terminal cache key checks all 12 child signatures with
`!pivotable_sig(child_sig(...))` before setting irreducible equal to full.
Cache hits reuse the identical `(profile29,signature12,p3)` response key.
The independent referee also seek-replayed 257 evenly distributed literal
source records, including both endpoints.  Of these, 212 had nonzero K19
continuations; it rebuilt 54,720 literal K21 children, checked every one
nonpivotable, and independently reproduced every recorded cycle charge.

## Provenance-use boundary

The upstream construction had 511,477,120 labelled selected-p2 uses before
exact-zero pair keys were removed.  The surviving nonzero decorated records'
`uses_u64` fields sum to 511,214,060.  This difference of 263,060 is expected:
`uses_u64` is witness provenance, while the coefficient authority is each
record's exact signed `weight_i128` and the header mass sum
`146230609431055564800`.

The first full evaluation correctly refused to publish at a final assertion
that had mistakenly equated those two use counts.  No response or charge
guard failed and no result was written.  After separating the pre-zero and
retained-use quantities, the unchanged scalar computation reran and completed
normally.

## Resource gate and artifacts

The eight-worker 10,000,000-record prefix completed in 24.264 seconds,
projected 246.387 seconds for the full source, and was observed at about
602,928 KiB RSS.  Its 257/257 samples were nonzero and exact.  The authorized
full rerun completed in 222.594 seconds, below the 600-second and 16-GiB
gates.  Cache chunks were capped at 100,000 pair records and peaked at 326,616
keys per worker chunk.  Only atomic JSON and bounded TSV outputs were written.

Pinned artifacts:

| artifact | SHA-256 |
|---|---|
| producer source | `4228a7ca6380329bae6c1351e32605bfad2cf04b0c7c5261c877e913cff0fe5c` |
| producer binary | `38d3e3e728af10e4632877e4f0a657ae076a2da9af1355e8738ba10fec4e65e4` |
| full result | `a58fa70195e5bb42ddad9b971a05145d15043f35af044c5339b1779ea56f3bae` |
| full literal samples | `113acc594bb35e2ab19a511f75b0dbb73e728806d08aa1566bca994d4074dd3d` |
| independent referee | `7cc51a5d537d41e00c0643f79e92ccf79a75ef908cae67bcf6d2f528ecd86846` |

The independent referee fully rehashed the 5.38-GB decorated ledger, pinned
the prior pair publisher/referee, checked header/schema/file size, result and
histogram arithmetic, signs and source guards, and performed the literal
sample replay.  It did not run a second 101,545,723-record charge evaluation.

Replay the referee with:

```sh
python3 computations/unaudited-codex-orbit0-k21-hidden-232-charge-2026-08-24/audit_hidden_232_independent.py
```

Scope excludes other K21 IDs, K21 coefficient collection, K22 prolongation,
residual assembly, membership, and a conjecture verdict.

