# D11 compact-representation microgate

## Verdict

`PASS_EXACT_REJECT_NONPERFORMANT`: the comparator-ranked `u32` row / compact sparse row / natural-order `u128` column representation is exact on the sealed first 1,000 and 5,000 D11 triangle checkpoint columns, but it is rejected for production. It did not achieve the required 2x measured memory or materialization-throughput improvement; it was materially worse on both measures.

No D11 resume, solve, CEGAR continuation, global incident scan, or D12 cache read occurred. Four accepted representation lanes ran sequentially under independent 4-GiB/120-second watchdogs.

## Exactness

The baseline and compact lanes used provider SHA `06df5052...`, selected checkpoint SHA `1f70a322...`, and dual SHA `a91f2be5...`. The compact engine:

- packs the derived natural `Column` order exactly into 112 bits of a `u128` (13 generator bits plus eleven 9-bit multiplier slots with a checked sentinel);
- assigns checked `u32` row IDs in the exact frozen comparator order `(frequency,Mono)`;
- stores vectors as sorted `(u32,u64)` pairs and decodes them before canonical hashing;
- interns the complete realized-row/dual-support union, using `u32::MAX` frequency for dual-only rows.

At 1,000 columns, both modes produced 106,000 terms and materialized semantic SHA `3f06393e...`. At 5,000 columns, both produced 527,074 terms and SHA `609a481e...`. Selected-prefix SHA, all 13,116 dual support rows, and all literal modular pairings also agree; pairing failures are zero. Five hostile mutations—semantic SHA, selected SHA, pairing count, column count, and an extra field—are rejected.

## Performance rejection

| columns | baseline peak RSS | compact peak RSS | compact RSS penalty | baseline representation | compact representation | compact slowdown |
|---:|---:|---:|---:|---:|---:|---:|
| 1,000 | 41,524 KiB | 58,656 KiB | 1.41x | 0.011346 s | 0.062545 s | 5.51x |
| 5,000 | 57,616 KiB | 150,500 KiB | 2.61x | 0.056278 s | 0.462243 s | 8.21x |

The row-frequency table, row-ID hash map, dual union, second materialization pass, and compact-vector storage outweigh the 32-byte to 16-byte term-payload saving at these gates. Accounted retained memory is likewise worse in compact mode. Full-checkpoint scaling is deliberately not inferred from these prefixes.

The first attempted telemetry sampler returned no RSS samples and is retained as four zero-coverage rejected lanes. A second result generation was superseded because baseline timing/accounting omitted its dual lookup. Only the final four `runs/` lanes are accepted.
