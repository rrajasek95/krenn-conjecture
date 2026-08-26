# Bounded exact D12 Metal/CSR acceleration gate

## Verdict

`PASS_METAL_CSR_PROMOTION_GATE` for the narrow, regular CSR pairing/SpMV
operator only.  On an Apple M5 Pro, the 32-repetition gate measured **10.9200x**
aggregate cold end-to-end speedup (including runtime shader/pipeline setup,
buffer allocation/upload, dispatch, wait, and shared-buffer readback) and
**14.5702x** as the weakest per-case warm end-to-end speedup.  Both exceed the
frozen 3x threshold.  Peak process RSS was 161,759,232 bytes.

This is not a D12 closure, rank, membership, or higher-degree result.  It
licenses integration/profiling of this regular pairing primitive, not a broad
GPU closure run.

## Native source and representative interface

The inspected native source is
`../unaudited-codex-n8-affine251-orbit-membership-2026-08-24/src/main.rs`
(SHA-256 `241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0`).
Its `sparse_pairing` computes a modular sparse dot product, and its
`sparse_write_vectors` writes strict sorted `(column, [(row,residue)])`
records.  The frozen cache used here is exactly that format:

- cache SHA-256: `2f6e21c52af1528cff68db91b293052f4a3e2627ebe199586b4e9efb7a883320`
- header prime: 1,073,741,827
- provider fingerprint: 9,218,588,987,274,412,661
- vector fingerprint: 16,816,770,837,132,312,102
- total cache records: 147,230

The exporter selects the first 32,768 records in the cache's strict canonical
order, maps their union of row words to deterministic dense coordinates, and
writes row-owned CSR.  It validates the cache SHA/header/order and requires a
unique centered integral lift bounded by 1,440 before the second-prime test.
The resulting 25 MiB interface has 2,820,144 coordinates and 3,296,157
nonzeros; its SHA-256 is
`78af8f53288fb4149082fd13cf49c0e0524f05e111204d32216c667a355c96f1`.
No solver state or closure frontier is synthesized.

## Exactness and hostile coverage

The Swift host computes an independent `% prime` reference, a separate CPU
special-reducer path, and a Metal result.  The Metal kernel assigns one thread
to each CSR record and therefore needs no atomics.  It has exact special
reducers for both frozen primes:

- `1,073,741,827 = 2^30 + 3`
- `1,073,741,789 = 2^30 - 35`

For each prime it tests a deterministic SplitMix-derived regular dense vector
and the hostile all-`p-1` maximum-residue vector.  CPU and Metal arrays are
required to be byte-identical before atomically writing evidence.  Output
digests are:

| Prime | Input | Output SHA-256 | Nonzero rows |
|---:|---|---|---:|
| 1,073,741,827 | regular | `22fa668241192428ce3f7d8fcde06bafc6354bf04599e61c99a842548ac1ff20` | 32,768 |
| 1,073,741,827 | max residue | `8c3495e6b5ed2ff1983d86e0b0eee32f211039bf54d6e3cf7effa47efab3cb1c` | 32,767 |
| 1,073,741,789 | regular | `c57151385d3f09db0ae95704760755aa28c13dc098360c32d705c561ee0935ff` | 32,768 |
| 1,073,741,789 | max residue | `32f1cfe0ed2a8f9d069a56525dcfb35fc8035b0f6154af6a46a12fb28425dbee` | 32,767 |

The independent Python referee reparses and pins the CSR, uses ordinary Python
integer modular arithmetic, and replays all 13,184,628 edge terms (four full
passes).  It also rejects a flipped output byte, a changed promotion Boolean,
a missing prime/mode case, a changed CSR pin, and a lowered threshold.  The
same referee passed under standard Python, `python3 -O`, and `python3 -I -S`;
the three audit JSON files are byte-identical.

## Timing evidence

The two-repetition control intentionally did not promote: cold aggregate was
0.3515x and its weakest warm case was 2.3128x because pipeline and transfer
overheads dominate such a small batch.  The bounded 32-repetition run reported:

- CPU exact special-reducer total: 1.294094291 s
- Metal cold end-to-end total: 0.118506294 s
- runtime pipeline/immutable-buffer setup: 0.038296667 s
- aggregate cold speedup: 10.920046922x
- minimum warm end-to-end speedup: 14.570164091x
- total measured program time: 1.500738958 s

The timed Metal region includes per-case value/vector/output buffer creation,
dispatches, synchronization, and reading the final shared output.  Pipeline
compilation plus immutable CSR buffer creation is included once in the cold
aggregate.  Common frozen-CSR parsing and deterministic input-vector creation
are outside both arithmetic timers.  As an additional conservative check, the
independent single-pass reference timings multiplied by 32 would still exceed
the 3x threshold against the measured Metal end-to-end totals.

## Frozen implementation and replay

- Swift source SHA-256: `d790e08580f70bc25e5487a2f0f599901cbd6348993a8c03376cdf413be5e2c4`
- Metal shader SHA-256: `f45752c1a92780bef7b04de877c711505a4c60aa3260b6cad197920fd8db26a5`
- arm64 binary SHA-256: `2621b5dec28cf36d7a06249fd769834b59a94467af52b7b77ae1942cbba98892`
- production result SHA-256: `ff270fbca2a14ac331138b4f9e8b5d5970718e6fa1aa89829024c8633866fd6b`
- independent audit SHA-256: `7ed9de7cc6a7f3c9a3e4fd91c6c1120afba2953e7c3bb6901984f5be48f6e2ce`

Compiler/platform: Apple Swift 6.3.3, arm64-apple-macosx26.0, macOS 26.5.1,
Apple M5 Pro (20 GPU cores).  Runtime Metal access is unavailable inside the
restricted command sandbox (`MTLCreateSystemDefaultDevice` returns nil), so
the approved bounded GPU command ran outside that sandbox.  The CPU-only
referee needs no elevated access.

Recompile command:

```sh
xcrun swiftc -O -whole-module-optimization \
  -o computations/unaudited-codex-n8-affine251-d12-metal-csr-gate-2026-08-24/d12_metal_csr_gate \
  computations/unaudited-codex-n8-affine251-d12-metal-csr-gate-2026-08-24/d12_metal_csr_gate.swift
```

The exact production and referee arguments are recoverable directly from the
required CLI fields in the sources and the pinned paths in
`results_metal_csr_gate.json` / `results_independent_audit.json`.
