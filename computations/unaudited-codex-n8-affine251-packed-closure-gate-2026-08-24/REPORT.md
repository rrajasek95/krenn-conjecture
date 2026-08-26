# Bounded packed D12 closure and capped natural-minimum gates

Status: **PASS for a bounded integration experiment; no D12 production run is authorized.** The existing `affine251-orbit-membership` package was not edited.

## Frozen inputs and scope

- Retained incomplete D12 closure: `closure_d12.bin`, SHA-256 `d9f3a71525b2a5070d9e911b12f313a0d20e0d1763c3e3adfaa1294cb638f241`.
- Production source inspected but not modified by this gate: the authoritative package manifest pins `src/main.rs` at SHA-256 `241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0`. A concurrent executor changed that working file to `f6fc8d65194d64449f4b66e4c4959766e6741014c601630c8625c570434d2146` at 16:58, after this sibling was implemented. That later source is neither used nor assessed here; this package preserves the earlier manifest pin explicitly instead of silently repinning its provenance.
- The checkpoint supplies 46,684,183 exact D12 row-orbit keys and 5,909,719 exact D12 column-orbit keys. Each gate draws sorted, nonoverlapping blocks distributed over 16 positions in the retained populations.
- Candidate streams contain exactly 4/5 distinct retained keys and 1/5 deterministic repeats. This makes duplicate handling reproducible, but it is a benchmark workload rather than a claim about the eventual production duplicate distribution.
- The legacy benchmark uses the production field shapes and verifies `size_of::<Mono>()=13` and `size_of::<Column>()=16`. The alternative encodes a fixed-degree row or column in a naturally ordered `u128`, sorts eight chunks in parallel, performs an exact k-way merge, and deduplicates.
- Timings below are medians of seven isolated processes. RSS is the per-process `getrusage(RUSAGE_SELF)` high-water mark. Loading and SHA computation are excluded from `dedup_seconds` but included in RSS.

## Exact packed sort/dedup gate

For every backend pair, both the exact sorted SHA-256 and output count agree. Counts are 80,000 at 100k input and 800,000 at 1m input.

| keys | scale | HashSet/sort | packed parallel sort | speedup | RSS HashSet -> packed |
|---|---:|---:|---:|---:|---:|
| rows | 100k | 0.005648 s | 0.001700 s | 3.32x | 8,304 -> 7,728 KiB |
| columns | 100k | 0.005510 s | 0.001592 s | 3.46x | 8,400 -> 6,128 KiB |
| rows | 1m | 0.076728 s | 0.017114 s | 4.48x | 59,536 -> 48,672 KiB |
| columns | 1m | 0.074460 s | 0.014853 s | 5.01x | 64,976 -> 45,568 KiB |

The exact 1m row digests are `09d394dacfa3e6e0186d78f32492b51b5415cedc8c449814a140c5865c9d61bf`; column digests are `83e2e420e71eb566389f0fe9cf1f127f974f203cd8eb3f210de8c2e54d7788e5`.

**Verdict:** the packed candidate collector clears the requested 2x threshold at both bounded scales and materially lowers peak RSS at 1m (18.3% rows, 29.9% columns in the final sealed run). Promote only to a next bounded integration gate that merges a packed sorted batch into the persistent sorted closure. This gate does not establish the cost of persistent membership, checkpoint conversion, or round-to-round merging, so it does not justify replacing the main engine or starting D12 broadly.

## Exact natural-minimum alternative

GAP is absent from the host, so no package was installed. The tested internal alternative retains the exact 1,440-action natural minimum but, after the first miss, memoizes every realized translate of that orbit. Its sorted output SHA/count equals the existing exact-input cache on 10k and 100k action-transformed retained D12 rows.

- Uncapped 100k correlated gate: 1.003123 s -> 0.033099 s, **30.31x**, but RSS 7,728 -> 30,640 KiB and 332,356 memo entries.
- Fixed-cap correlated gate (100k candidates, 256 orbit families): 100k and 250k FIFO caps both thrash to zero hits; they take 29.71 s and 18.36 s in the independently sealed cap run. A 400k cap holds all 332,356 realized keys, has 99,744 hits / 256 misses (99.744%), takes 0.038350 s, and is **27.57x** faster than the exact cache.
- Adversarial gate (2,000 distinct retained orbit representatives): every cap has zero hits. The 400k cap takes 0.405135 s versus 0.085519 s, a **4.74x slowdown**, and peaks at 53,696 KiB.

**Exact promotion point:** at most 400,000 entries, only after a 10,000-key shard-local probe reports both hit rate >= 90% and speedup >= 2.0. Otherwise use the ordinary exact-input cache. The capped memo always computes the same 1,440-action minimum on a miss, so eviction affects speed only, not semantics. The promotion is conditional and bounded; it is not a general canonicalizer replacement.

## Referee and hostile coverage

- Engine selftests cover row/column pack round trips, natural ordering, parallel dedup, production 13/16-byte legacy layouts, and an independent SHA-256 vector.
- Checkpoint hostiles reject bad magic, degree, row length/order, column word, and trailing bytes.
- The semantic audit checks the exact run matrix, SHA/count equality, repetition counts, ratios, source/binary/input pins, promotion scope, and the cap/hit/eviction invariants.
- Fifteen result-contract mutations are rejected: missing runs, changed SHA/count/input pin, cap overflow, inconsistent hits, weakened probe, broad authorization, wrong canonical SHA, and extra fields.

Authoritative result files are `results_packed_gate.json` and `results_capped_orbit_memo.json`. Independent audit summaries are `audit_results.json` and `audit_capped_orbit_memo.json`.
