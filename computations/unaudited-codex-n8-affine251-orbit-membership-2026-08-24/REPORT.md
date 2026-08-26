# Affine-251 orbit-compressed ideal-membership computation

## Purpose

This package implements the cost-capped local attack on the single
251-variable affine cover obtained by fixing `x67_01=1`.  It does not use
cloud compute.  Every degree is bounded by 1,800 wall seconds and 42 GiB RSS;
a cap produces `INCOMPLETE_RESOURCE_GATE`, never a mathematical verdict.

The affine equations are homogenized with a new variable `t` (ID 251).  A
degree-`D` Nullstellensatz certificate for the affine unit is equivalent to
`t^D` lying in the degree-`D` part of this homogeneous ideal.  The stabilizer
of the fixed coordinate is `S6 x C2`, of order 1,440.  Because the primes used
below do not divide 1,440 and the target is invariant, row and generator-
multiplier column orbit sums preserve the membership question exactly.

## Implementation

`src/main.rs` is a dependency-free native AArch64 Rust implementation.  It:

1. parses and independently homogenizes the frozen 6,561-equation msolve
   export (688,908 parsed terms, 688,906 distinct degree-four monomials);
2. constructs all 1,440 stabilizer actions and the exact bipartite incidence
   closure of the target row orbit;
3. checkpoints the complete/discovered row and column sets atomically;
4. constructs the Reynolds/orbit-sum matrix using
   `b_R * stabilizer(R)` for each row-orbit coefficient;
5. performs exact sparse modular column elimination; and
6. emits a separating left-nullspace dual whenever the target is absent.

Frontier expansion and matrix-column construction use up to 16 native worker
threads with thread-local canonicalization caches.  Sparse echelon insertion
remains deterministic and sequential.  The same D8 closure and dual files are
byte-identical between the original serial implementation, the parallel
release implementation, and a debug build.

`audit_affine251_orbit.py` is an independent Python referee.  In deep mode it
rebuilds the provider, group, complete orbit closure, integral orbit matrix,
rank test, and modular dual without invoking the Rust program.  It also lifts
the two D8 modular duals to an exact rational dual and verifies every integral
matrix pairing.

## Frozen inputs

- `canonical_triangle_pair_offdiag_full_p32003.ms`:
  `75a82d82a979d75507e682fd339e83d4ae35949653d624fb541148bd3957dcff`
- `canonical_triangle_pair_offdiag_full_p1073741827.ms`:
  `daa427528bbbeece064b09396023b66f32b804ba6d304178d19ced13e9b38a4e`

The two files have identical variable headers and equation bodies; only their
declared export prime differs.

## Degree-eight terminal control

The D8 computation gives exactly:

- 1,418 row orbits;
- 116 column orbits;
- 3,848 nonzero matrix entries;
- rank 107; and
- a nonzero target residual over both 1,073,741,827 and 1,073,741,789.

The independent referee reproduces the row and column sets literally and the
rank/counts exactly.  With the lower-fill reverse pivot order, the two modular separating duals lift to a 7-entry
rational dual with maximum denominator 2.  Direct exact arithmetic verifies
that it annihilates every integral orbit column and evaluates to 1 on `t^8`.
Therefore `t^8` is **not** in the homogeneous ideal over characteristic zero.
This is a rigorous degree-eight nonmembership statement, not merely modular
evidence and not a proof that the affine system has a solution.

The same support-local exact referee proves characteristic-zero nonmembership
at D4--D7 and D9--D11.  The D9--D11 separating functional is precisely the
seven-entry D8 functional shifted by one, two, or three powers of `t`.
The full D11 closure contains 3,722,556 row orbits and 195,924 column orbits;
the reverse-pivot matrix has 18,713,801 nonzeros and rank 194,006 over both
large primes.  Each modular run completed in about 250 seconds with roughly
3.2 GiB peak RSS.

The tempting all-degree prolongation is false.  An independent exact check
finds its first failure at D12: generator word 0 with canonical multiplier
`00096399a2abcfea` pairs to `-2`.  Thus D12 is the first genuinely new layer
and no all-degree or affine-consistency conclusion is inferred from D4--D11.

A separate sparse-dual CEGAR was bounded to 120 seconds.  It expanded through
five exact rounds (2, 9, 39, 114, then 308 exposed columns; dual support 3, 7,
18, 40, then 168) and stopped as `WALL_CAP` with 1,068 new incident columns.
This is diagnostic only: it supplies neither a D12 dual nor a membership
certificate.

## Native sparse D12 optimization

`src/bin/sparse_d12_dual.rs` exposes a native, dual-first D12 CEGAR engine
that shares the provider, group action, canonicalizer, invariant-column, and
exact modular kernels with `src/main.rs`.  With a cold/first policy and no D8
seed, its first five rounds reproduce the Python CEGAR counts exactly:
`(2,3)`, `(9,7)`, `(39,18)`, `(114,40)`, and `(308,168)` for
`(columns,support)`.  The native release reaches and atomically checkpoints
that state in 0.300 seconds; the earlier Python gate remained at the same
completed state when its 120.077-second allowance expired in the next round.

Restart cost was initially substantial because every saved column was
reconstructed from the 689k-term provider.  The new `AFF12VEC1` sidecar is
tied to a deterministic provider fingerprint, deterministically checksummed,
validated as an exact subset of the scalar checkpoint, and written
atomically.  At 93,754 columns, cold reconstruction took 68.698 seconds while
the 191 MiB warm cache loaded and validated in 1.022 seconds, a 67.24x
restore improvement.  A deliberately stale cache missing 1,731 columns
rebuilt only those columns and became byte-identical to the complete 95,485-
column cache.

The periodic six-choice pivot/repair portfolio is embarrassingly parallel.
Running its exact solves concurrently reduced a controlled portfolio solve
from 8.668 to 2.473 seconds (3.50x); the selected scalar checkpoint and vector
cache were byte-identical.  Ordinary rounds retain the stable cold/rare
policy.  Two exact micro-optimizations were rejected rather than promoted:
constant-prime reduction was 14.0% slower and sorted-vector merge elimination
was 1.3% slower than the `BTreeMap` reference on the three-round control.  A
raw persistent incremental basis caused rapid support/frontier expansion;
adaptive fallback contained it but remained slower, so production keeps it
disabled.

The optimized 300-second continuation advanced the restartable state from
round 453 to round 538, ending fail-closed as `INCOMPLETE_RESOURCE_GATE` with
147,230 exposed column orbits, dual support 233, and 4,236,672 KiB sampled
peak RSS.  Its 301 MiB sidecar reloads all 147,230 vectors in 1.811 seconds.
The constraint frontier is still nonempty; `global_annihilation`, target
pairing, and mathematical verdict therefore remain null.

`ACCELERATION_SURVEY.md` records the parallel library/paper survey.  At the
current roughly 233-by-147k geometry, deterministic CPU sparse elimination
is preferable to block Wiedemann/Lanczos or a Metal rewrite.  The next
bounded engineering gates are packed sort/dedup for the full closure,
canonical-image acceleration, and SpaSM equivalence on complete D10/D11.
Metal becomes appropriate only after a resident CSR/CSC block operator is
available and repeated SpMV or dense panels dominate; GPU discovery would
still require literal CPU certificate replay.

## Degree-twelve gate

The optimized D12 run was checkpointed across implementation-only restarts
and given a reduced final allowance so cumulative productive wall time stayed
near the agreed 30 minutes.  It terminated as `INCOMPLETE_RESOURCE_GATE` with:

- 46,684,183 discovered row orbits;
- 5,909,719 discovered column orbits;
- 7,022,137 rows and 4,326,761 columns still on the frontier;
- no rank computation, no emitted dual, and no membership result; and
- about 2.4 GiB peak RSS in the final pass.

The independent incomplete-result referee pins the checkpoint and confirms
that the only valid D12 conclusion is **no conclusion**.  The saved closure is
restartable if a future run is desired, but no additional computation is
recommended under the present budget without a new D12-specific algebraic
compression.

## Scope

A member result at some degree would give a finite affine infeasibility
certificate for this cover.  Nonmembership through finitely many degrees is
only a lower bound on certificate degree.  It neither establishes existence
of a point in this cover nor resolves the full conjecture, the other affine
charts, other support families, or other group orbits.

The final strict ledger records exact characteristic-zero nonmembership for
D4--D11 and a resource-gated D12 with a null mathematical verdict.  This is a
substantial certificate-degree lower bound for this one affine cover, not a
resolution of the conjecture.

## Verification

`results_exact_degree_ledger.json` is the fail-closed machine summary.
`results_d12_incomplete_audit.json` independently validates the resumable D12
checkpoint. `results_d12_native_sparse_audit_final.json` verifies the Python
equivalence trace, cache repair, rejected kernels, parallel portfolio, and
latest incomplete state. `results_d12_sparse_hostile_selftest_final.json`
records 16 hard cache/CLI rejections plus one valid fail-closed warm restart;
`results_hostile_selftest_final.json` replays the original seven native solver
guards. `MANIFEST.sha256` pins every non-build artifact in this package plus
both release executables; `shasum -a 256 -c MANIFEST.sha256` replays the
package integrity check.
