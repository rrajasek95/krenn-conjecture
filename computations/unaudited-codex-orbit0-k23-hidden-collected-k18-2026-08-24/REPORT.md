# K23 hidden-collected K18 singleton: prefix-gate report

## Verdict

`PASS_K23_HIDDEN_COLLECTED_SINGLETON_PREFIX_GATES_FULL_HELD` for the strict singleton `D14:222|R:2-2-2-3`. The literal producer, three required prefix gates, and an independent 257-record distributed replay pass. Full production was not launched because the direct-K23 shard was active.

## Frozen source and recurrence

- H18PIV2 source: `computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin`
- Source SHA-256: `442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8`
- Exact geometry: 16-byte header plus 158,439,965 records of 80 bytes; total 12,675,197,280 bytes; scale `U=400591699200`.
- Literal path: H18PIV2 `D14 R2-2` -> response K2 -> retain pivotable K20 -> its unique pivot -> response K3 -> terminal K23.
- Occurrencewise coefficients are `w -> -w/m3 -> +w/(m3*m4)`, with exact division at both stages and `m4=1` universally on retained K20 children.
- Every emitted K23 child has anchor mass 1, hence no outgoing pivot. Therefore full charge equals irreducible charge for this singleton.

No K24 continuation, row residual, membership result, or conjecture conclusion is produced here.

## Required prefix gates

| Records | Elapsed (s) | Terminal K3 tails | Scaled charge `U*charge` | Linear full projection (s) |
|---:|---:|---:|---:|---:|
| 1 | 0.002294 | 128 | -2043889061068800 | 363474.430227 |
| 4,096 | 0.042772 | 742,144 | -7837849435786444800 | 1654.482722 |
| 1,000,000 | 2.951014 | 120,571,904 | -128019438175017664512 | 467.558614 |

The million-record gate is the scheduling basis. Cache cardinalities were 261,322 K18 response entries and 201,265 K20/K3 response entries. The shell sandbox did not expose a reliable peak-RSS counter; the structural memory bound is non-increasing relative to the sealed H18PIV2 K22 full fold (<1.4 GiB), because this producer uses the same key/value cache abstraction, a smaller K18 plan, and emits no rows.

## Independent literal referee

The referee re-read 257 distributed source records spanning indices 0 through 999,999, without consuming producer sample values. It replayed 1,036 retained pivotable K20 continuations and all 33,152 resulting terminal K23 children, confirming exact division, signs, source provenance, terminality, and the strict singleton label. Its sampled scaled charge is `66584177055055872`.

## Held production schedule

The exact gap-free, non-overlapping schedule is:

1. `[0, 52813321)`
2. `[52813321, 105626643)`
3. `[105626643, 158439965)`

Using a conservative 2x cache-reset multiplier, the maximum projected shard time is 311.706 seconds, below the 540-second launch gate and 600-second hard limit. Each shard must be written atomically and retained for an exact no-gap/no-overlap merge. The family RSS gate is 8 GiB and the aggregate gate is 16 GiB. This report authorizes no full shard launch.

The machine-readable authority is `results_k23_hidden_gate_audit.json`, with logical SHA-256 `7c4b4d2eb621c03af5ff81bef5d8696363a0600ac58adf4a836c3453c949189c`.
