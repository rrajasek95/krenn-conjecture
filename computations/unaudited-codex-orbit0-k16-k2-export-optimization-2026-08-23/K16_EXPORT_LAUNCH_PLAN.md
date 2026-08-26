# Staged launch plan: direct-K16/K2 K18-parent export

## Readiness verdict

`READY_AFTER_PRODUCTION-DRIVER HARDENING`; no full job is launched by this
plan.  The bounded cached implementation is exact, but it is still a
benchmark, while the existing restartable production exporter does not use
the validated child-signature cache.  The first launch must therefore pin a
production cached exporter and runner before consuming a 600-second gate.

## Fixed input and output contract

- Input: `checkpoint_direct_k16.bin`, exactly `24,097,095` H-orbit records.
- Exact source totals to certify after complete export:
  `24,003,767` pivotable rows, `129,939,187` first-pivot uses,
  `1,559,270,244` K18 parents, and `807,499,618` pivotable K18 parents.
- Paths: `D16:{224,233,242,323,332,422}|R:2-2`.
- Scale: `U=400591699200`, with `m1*m2 | U` asserted occurrencewise.
- Key/record schema: unchanged `K18PRF2`, component `3`, degree `2`,
  `profile29|signature12|p2` plus signed weight/use count and the reversible
  literal `(row,source,p1,t1,p2,m1,m2,packet=255)` witness.

## Production-driver delta

Port only the validated `child_sig(s16,p1,t1)` plus worker-local
`signature -> avail(signature)` cache from `benchmark_k16_row_cache.rs` into
the restartable exporter.  Preserve literal `r18`, profile computation,
signed aggregation, witness ordering and part schema.  Add a must-pass mode
that byte/census-compares the baseline and cached paths on the four frozen
2,000-row ranges before any full shard is accepted.

## Export gate

Partition `[0,24097095)` into 64 deterministic contiguous ranges
`[floor(i*N/64),floor((i+1)*N/64))`.  Use eight workers, at most eight active
ranges, and a 250,000-key worker sink.  Each range writes fresh attempt-named
sorted parts and then an atomic manifest containing interval, source counts,
parent/use counts, signed mass, denominator histogram, file sizes and SHA-256.
A shared validator must fully stream every part before accepting a manifest.

Hard gate: 600 seconds / 16 GB.  Stop scheduling at 450 seconds; finish or
checkpoint active ranges by 600 seconds.  Never infer full totals from a
partial catalog.  Current free space after the reviewed K15-part cleanup is
approximately 237,032,480 KiB; the 10.69 GB output estimate is sample-based,
not a disk bound, so the runner must recheck free space before every batch.

## Subsequent separate gates

1. External signed merge, at most 600 seconds / 16 GB, preserving exact-zero
   groups and minimum literal witnesses; source manifests and parts retained.
2. Read-only grouped six-ID K2 charge, at most 600 seconds / 16 GB, evaluating
   12 tails/profile; no row collection or K21 tails.

Neither subsequent gate starts before an independent export referee accepts
all 64 ranges and exact global totals.  Cleanup requires a separate explicit
post-referee instruction.

## Pinned controls

- `REPORT.md` SHA-256
  `fdafdbd67015f3d03ae2303c68197c71eea1a3711b1fe7490b4168e156ffdc16`
- `results_k16_k2_restartable_plan.json` SHA-256
  `9c5953df3ca5d025f4c0f79837360b8d87061e4d771f2faf492575d5e9fb07ae`
- `benchmark_k16_row_cache.rs` SHA-256
  `93d35cd6da0086d3a02f0d61e4f79feea330b918b2ac2c9e3c1f2f71b9c0164e`
- `results_k16_row_cache_benchmark.json` SHA-256
  `85e8efb3900120a1fc5badb0af7901dd15e07690bd94f28c63187753c12847e2`

