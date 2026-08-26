# Acceleration survey for the affine-251 D12 attack

## Measured geometry

The native sparse CEGAR state is highly rectangular: roughly 96,000 exposed
column orbits but only about 200 active dual rows.  Ordinary rounds spend
about 0.4 seconds materializing new invariant columns and 2--3 seconds in an
exact sparse cold solve.  A six-choice portfolio audit formerly spent about
9 seconds in sequential solves.  Restoring 93,754 materialized vectors from
the provider took 68.70 seconds.

Two changes are already accepted:

- a 191 MiB provider-bound, checksummed vector cache reduces restore to 1.02
  seconds (67.24x), repairs interrupted subset caches deterministically, and
  produced a byte-identical repaired cache; and
- running independent portfolio solves concurrently reduces the measured
  portfolio solve from 8.67 to 2.47 seconds (3.50x), with byte-identical
  selected checkpoint and vector cache.

Constant-prime reduction and sorted-vector elimination were exact but did
not improve time on this CPU, so they remain rejected diagnostics.  A raw
incremental basis reduced update cost but caused explosive frontier growth;
adaptive fallback contained the growth but was slower than cold/rare, so
production keeps incremental mode disabled.

## Ranked next experiments

### 1. CPU sparse elimination and packed closure

At the current 200-row scale, deterministic sparse Gaussian elimination is
the right algorithm.  Block Wiedemann or Lanczos would first have to embed or
precondition a system whose small dimension is only about 200.  The practical
next library gate is [SpaSM](https://github.com/cbouilla/spasm), first on the
already complete D10 and D11 matrices, requiring exact rank/residual and dual
replay equality before any D12 use.  Dense tails can use
[FFLAS-FFPACK](https://linbox-team.github.io/fflas-ffpack/) over the odd
30-bit primes; [M4RI](https://github.com/malb/m4ri) applies only to GF(2).

For the much larger full-closure route, fixed-width row and column keys should
be generated in batches and radix/sample-sorted rather than inserted into
dynamic hash tables.  The raw discovered D12 keys fit in well under a GiB;
the observed hash-based peak was about 2.4 GiB.  Suitable controls include
[IPS4o](https://github.com/ips4o/ips4o) for parallel in-memory sorting and
[STXXL external sort](https://stxxl.org/tags/1.4.1/design_algo_sort.html) if a
later frontier exceeds RAM.  A minimal perfect hash such as
[BBHash](https://arxiv.org/abs/1702.03154) is useful only with exact stored-key
comparison, never as a nonmembership oracle by itself.

### 2. Canonical-image acceleration

The 1,440-action canonicalizer is another regular cost center.  A bounded
100,000-key A/B gate should compare the current natural minimum against GAP
Images `MinimalImage`, which can avoid enumerating every group element:
[GAP Images documentation](https://gap-packages.github.io/images/doc/chap2_mj.html).
Promotion requires byte-identical natural representatives and at least 2x
throughput.  Non-minimal canonical forms are not interchangeable with the
frozen natural ordering.

### 3. Metal, after a regular matrix kernel exists

Rust can drive Metal through
[`objc2-metal`](https://docs.rs/objc2-metal/latest/objc2_metal/); the older
[`metal-rs`](https://github.com/gfx-rs/metal-rs) repository directs users to
`objc2-metal`.  A pinned [`wgpu`](https://github.com/gfx-rs/wgpu) prototype is
also possible, but raw MSL/metallib gives tighter integer and artifact
control.  Apple's feature table documents 64-bit integer arithmetic on the
relevant Apple GPU families:
[Metal feature tables](https://developer.apple.com/metal/Metal-Feature-Set-Tables.pdf).

Metal should not implement dynamic pivoting, `HashMap`, or orbit
canonicalization first.  The first useful kernel is resident CSR/CSC block
SpMV/SpMM over the two 30-bit primes, with row ownership so no 64-bit atomics
are required.  The CPU retains CEGAR pivoting and certificate construction.
Apple unified memory reduces transfer cost, but a promotion gate still needs
1M-edge and 100M-edge exact-equality controls, adversarial maximum residues,
empty and long rows, pinned metallib SHA-256, total RSS, and at least 3x
projected end-to-end improvement.

### 4. Block Wiedemann contingency

[LinBox](https://linalg.org/linbox/linbox/) supplies Wiedemann and block
Wiedemann methods, while the primary exact-GPU SpMV study explains why the
matrix and Krylov vectors must remain resident:
[Dumas et al.](https://arxiv.org/abs/1004.3719).  This becomes plausible only
if the independent-row count reaches the low tens of thousands and sparse
elimination fill or memory dominates.  It is premature at roughly 200 rows.
Any modular discovery must still emit an explicit dual `A^T y = 0` with
nonzero target pairing, then pass the existing literal integer/rational
replay.  A probabilistic rank alone is not a characteristic-zero verdict.

## Rejected general-purpose routes

Full msolve, FGb, Singular/Oscar, or Macaulay2 computations in 251 raw
variables discard the exact 1,440-fold orbit compression and are unlikely to
beat the fixed-degree invariant Macaulay attack.  They remain useful only as
small bounded comparison controls.  NTL and FLINT dense matrices likewise
become attractive only after a sparse solver exposes a genuinely dense tail.

## Current decision

Continue the cached CPU CEGAR while support remains in the hundreds.  In
parallel, implement the packed sort/dedup microgate and a D10 SpaSM equality
gate.  Start a Metal backend only after a CSR/CSC operator exists and a CPU
profile shows repeated resident SpMV or dense panels dominate.  None of these
engineering results changes the current mathematical status: D12 remains
incomplete until an exact global dual or membership certificate is replayed.
