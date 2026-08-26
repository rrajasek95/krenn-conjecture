# Exact round-635 D12 Metal block-operator gate

## Verdict

`PASS_PRODUCTION_READY_EXACT_METAL_BLOCK_OPERATORS` for the sealed resident
`A`/`A^T` primitives at block widths 1, 8, and 16.  This verdict is limited to
future use of these operators.  It is not a closure, rank, block Wiedemann,
Krylov, membership, or higher-degree result, and it does not authorize any such
launch without a separate resource/projection gate.

All 24 required cases (two directions x three widths x two primes x regular or
all-maximum-residue input) were CPU/Metal byte-exact.  The weakest width-8/16
warm end-to-end speedup was **29.5878378x**, comfortably above the frozen 3x
production-readiness threshold.  The complete gate took 16.281899 seconds and
peaked at 5,890,179,072 bytes (5.485 GiB), below the strict 180-second/6-GiB
limits.  Because RSS headroom is only about 552 MiB, future runs must remain
exclusive and must be re-gated if their retained state grows.

## Authoritative round-635 inputs

- `tree635_vectors.bin`: 478,445,989 bytes, SHA-256
  `dd74d7392a005fb9c7726d9a0cc5c86e5b16d987bcb707d1c3a0f90e6e4d9e40`
- `tree635_checkpoint.bin`: 3,346,799 bytes, SHA-256
  `761804372a3f7e12b1915dd2718f7f69ef00b799dc6f90cd083b2fa7d2fc3c88`
- source prime: 1,073,741,827
- provider fingerprint: 9,218,588,987,274,412,661
- vector fingerprint: 6,593,799,974,443,584,084
- round: 635; exposed columns: 222,676; candidate support: 315

The exporter requires exact checkpoint/cache column-set equality, strict
column/row order, valid headers, and nonzero source residues with a unique
centered integral lift bounded by 1,440.  This lift lets the same physical
integer matrix be tested exactly at both primes; checkpoint candidate values
remain tied to the source prime.

## Exact resident interface and build cost

The 420,784,888-byte matrix artifact (SHA-256
`30ff854947b1b0f76ff01b07297b6aef8797ae44c0fca3b1b11ffae60e0d0439`)
contains both layouts, not an inferred transpose:

- `A` has 14,814,562 coordinate rows, 222,676 exposed-vector columns, and
  22,539,257 nonzeros;
- CSC stores column pointers, dense row indices, and centered `i32` values;
- CSR stores row pointers, column indices, and centered `i32` values;
- the terminal provenance ledger stores all 315 checkpoint candidate rows,
  values, and dense IDs.

Export/build timings, kept separate from warm operator timings, were:

| Phase | Seconds |
|---|---:|
| Source/checkpoint SHA-256 | 1.583137 |
| First parse and coordinate sort/dedup | 1.039092 |
| Dense map and exact second parse | 4.596094 |
| Exact CSC-to-CSR scatter | 0.327366 |
| Atomic write and output SHA-256 | 1.324663 |
| Total export/build | **8.870352** |

Exporter peak RSS was 1,341,947,904 bytes.  Runtime matrix loading, Metal
pipeline compilation, and copying both resident layouts took another 0.348045
seconds before any warm operator timing.

## Warm block results

Each Metal timing is after one untimed warm-up dispatch.  It includes command
commit, synchronization, and visibility of the shared output, but excludes
deterministic input construction and input-buffer/output-buffer allocation;
those costs are recorded separately in every case.  Across all 24 cases,
input construction totaled 0.372843 seconds, upload/allocation 0.332513 seconds,
CPU operators 11.926782 seconds, and warm Metal operators 0.306549 seconds.

| Direction | Width | Warm speedup range | Metal time range (s) |
|---|---:|---:|---:|
| `A` | 1 | 16.0206x–38.0610x | 0.002380–0.005326 |
| `A` | 8 | 30.4523x–38.7993x | 0.012693–0.015424 |
| `A` | 16 | 47.1970x–51.9722x | 0.019154–0.019949 |
| `A^T` | 1 | 20.9926x–30.4959x | 0.005186–0.007049 |
| `A^T` | 8 | 29.5878x–43.7620x | 0.009764–0.017284 |
| `A^T` | 16 | 40.6664x–46.4347x | 0.017160–0.019102 |

The inputs cover primes `2^30+3 = 1,073,741,827` and
`2^30-35 = 1,073,741,789`, with both deterministic regular blocks and hostile
all-`p-1` blocks.  CPU uses the same exact special-reduction identities through
a separately compiled host implementation; every full output buffer is
compared byte-for-byte, a one-byte mutation is rejected, and a digest for each
large output is retained in `results_metal_block_gate.json` rather than writing
multi-gigabyte row output.

## Current-candidate annihilation

At the source prime, the exact round-635 checkpoint candidate satisfies
`A^T y = 0` on all 222,676 currently exposed columns:

- candidate support/dense records: 315/315;
- CPU and Metal nonzero output entries: 0;
- zero-output SHA-256:
  `5bf43517c3c6ed09a923f1af6b38a920e8b13bc1be11e183ea33ad692fe69c0c`;
- warm Metal `A^T y`: 0.006270 seconds (GPU interval 0.005552 seconds).

The independent referee did not rely on the dense interface for this claim. It
read the authoritative checkpoint candidate and rescanned all 22,539,257
literal source terms; 798 terms hit candidate support and every one of the
222,676 modular pairings was exactly zero.

## Independent referee and fail-closed behavior

The referee also performed an exact, entrywise 22,539,257-edge CSC-to-CSR
transpose replay: for every CSC `(column,row,value)` it consumed the uniquely
corresponding CSR slot and required exact column and coefficient equality, then
required all 14,814,562 CSR rows complete.  It pins all sources/binaries and
rejects a changed readiness Boolean, missing/duplicate case, and RSS exactly at
the forbidden 6-GiB boundary.

An initial unsealed attempt completed arithmetic but correctly refused to write
a result at the resource gate because per-case Metal allocations remained
retained.  The final source changes only allocation lifetime: every case now
runs inside a drained autorelease scope and widths run largest-first for buffer
reuse.  The exact arithmetic, matrix, primes, case set, and comparison rules
were unchanged.  Only the final passing JSON is packaged.

## Evidence pins

- exporter source: `68f7fcfafe54cab084bbc4a2ccd96d9ba7a6156339249802fed185809ab6844c`
- exporter binary: `221bc8a93002bb086b4d54457eb0695b459db51bea9ff57907664264ef33ed30`
- Metal shader: `14e407f1d86dc334ba4d5b7e64031b3601770b15f21b9d97ccad36dbea06e503`
- Swift source: `6517017f508dccaa189e9362737623dc52f936ccf42d1e3287151c014123d927`
- Swift arm64 binary: `014aa125e0eb0f07a588d8c399954f276b80054818b61e7854e76d9a0e04858c`
- production result: `cdde3f199f782d9070ac5a993f1449a53f831e27025d77e605e26b7632a120e5`
- independent audit: `2226e52d17a353c57ac3d487a313e95cf35ed898aeaeb71c941eb0000512311a`

Compiler/platform: Rust release LTO exporter; Apple Swift 6.3.3 targeting
arm64-apple-macosx26.0; macOS 26.5.1; Apple M5 Pro with 20 GPU cores.  Runtime
Metal access requires the approved unsandboxed local GPU command; the exporter
and independent referee are CPU-only.
