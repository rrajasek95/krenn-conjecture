# Groebner engine benchmark (2026-08-21)

This is a discovery/runtime benchmark, not a proof certificate.

## Input

All engines received the same reduced `p=1009` D0-pivot ideal exported by
`probe_branch0_cycle_d0_c0_pivot.py`.  The input has four variables
`b0,d1,d4,z` and five polynomials, including the localization equation.

Input:
`../unaudited-codex-root-integration-2026-08-20/benchmark_d0_pivot_p1009.ms`

## Results

| Engine | Outcome | Wall time | Observed memory / size |
| --- | --- | ---: | --- |
| msolve 0.10.1, inverse-variable input | **invalid/retracted** | 511.16 s | input used `z*(pivot)-1`, which msolve silently misparsed |
| msolve 0.10.1 native F4SAT, 8 threads | completed | 223.72 s | about 2.6 GB RSS; 37 basis elements and 9,316 terms |
| Singular 4.4.1 `slimgb` | timeout | 600.06 s | under 1 GB RSS at timeout |
| Symbolica 2.2.0 Rust API | interrupted after explosive growth | under 180 s | about 12.6 GB RSS; already more than 1,800 intermediate basis elements |

The original ordinary-msolve comparison is retracted.  msolve 0.10.1
silently misparses a parenthesized Rabinowitsch expression such as
`z*(pivot)-1`; `#invalid equations: 0` does not detect this.  Its timing and
basis statistics therefore do not describe the intended localized ideal.
The Symbolica harness expanded that expression with its own parser, and the
Singular benchmark used a polynomial variable `P`, so those two inputs did
represent the intended ideal.

The native F4SAT run represented the localization as four compatibility
equations saturated by the pivot, instead of introducing `z*pivot-1`.  It
reduced 205,643 rows, but its largest matrix was only 11,836 by 17,911.  This
mode requires a sufficiently large 32-bit prime in msolve 0.10.1, so the
benchmark used `p=1073741827`; `p=1009` is rejected as too small.  Combining
`-S` and `-e 2` also aborted in this release, so saturation and elimination
must be staged as separate computations.

## Operational decision

Use msolve native F4SAT for localized finite-field discovery, and ordinary
msolve F4 only on fully expanded, parser-audited inputs for the remaining
large basis/decomposition steps.  Use Singular
and independent sparse replay for exact-Q reconstruction and certificate
verification.  Symbolica remains useful for Rust-native polynomial plumbing,
but is not the preferred basis engine for this fill-heavy family.

Every future msolve run must reject parentheses, compare expanded row hashes,
and pass the parser must-fire `<x,z*x-1> = <1>`.  The native F4SAT output
contains leading-ideal data only (`-g 1`); it is adequate for the runtime
benchmark and modular non-unit diagnosis, but is not an exact-Q proof.
