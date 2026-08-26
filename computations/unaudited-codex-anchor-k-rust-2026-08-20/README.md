# Anchor-K Rust sparse accelerator (unaudited)

This dependency-free binary reads the deterministic sparse JSONL interface
emitted by `probe_degree6_chart26_residual.py`, constructs a common sparse
echelon over `F_1009`, and completely reduces the target. A free low row never
halts reduction at higher pivots. Repeated `(row,value)` entries are summed,
not converted to a set.

The output solution is indexed by producer column number. It is discovery
data only and must be expanded to labelled rows and replayed over `Q` by the
existing Python exact checker before any proof claim.

```sh
cargo test
cargo build --release
target/release/anchor-k-echelon solve INPUT.jsonl OUTPUT.json
target/release/anchor-k-echelon project BASIS.jsonl TRANSFERS.jsonl PROJECTED.jsonl
```

`project` freezes one common echelon, reduces every transfer/lower-tail column
completely, reindexes the free quotient rows, and emits solver-compatible
JSONL. Its `source_free_rows` and `source_column` fields retain the map needed
for labelled back-substitution. A negative result is only as complete as the
provided transfer file; omitted lower-kernel tails invalidate a global dual.
