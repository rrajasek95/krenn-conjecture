# Exact K24 relative-column interface gate

## Outcome

The load-bearing interface is implemented and **production remains held**.
The terminal operator is

```text
B = (L,T),       L=P_<24 B on K20,K22,K23,       T=P_24 B,
A24_rel = T restricted to ker(L).
```

An explicit positive certificate is a rational natural-H-orbit source vector
`x` satisfying both `Lx=0` and `Tx=R24`.  Equivalently,
`B*x=(0,0,0,R24)`.  Because the source map is H-equivariant and the target is
H-invariant over `Q`, Reynolds averaging makes the H-orbit-sum source domain
complete.  If no explicit `x` is available, a complete full-incidence closure
may instead produce a kernel basis `K`, relative columns `T*K`, and an exact
rank-plus-norm certificate.

The closed JSON schema is `k24_relative_column_certificate.schema.json`.  It
requires exact 35-ID coverage, the frozen all-dividing-pivots reducer,
natural-order H keys, multiplier-aware columns, exact orbit division, a frozen
R24 hash, zero merged K20/K22/K23 projections, byte/exact equality of the K24
projection with R24, terminality, and either an explicit vector or COMPLETE
relative Gram evidence.  A capped closure cannot validate the schema.

## Bounded semantic control

`k24_relative_column_provider.py` extends the pinned factorized provider from
top outputs to the **full filtered column**.  It canonicalizes columns by
natural `(word tuple, multiplier bytes)` order, expands the complete 384-column
H orbit, and emits exact H-row-orbit masses in all four possible degrees.

The first accepted D17 prefix witness was replayed with coefficient `-128`.
One column orbit of size 384 has exactly 40,320 literal outputs and the exact
coordinate/mass census:

| K degree | orbit coordinates | unit orbit mass | weighted orbit mass |
|---:|---:|---:|---:|
| 20 | 1 | 384 | -49,152 |
| 22 | 12 | 4,608 | -589,824 |
| 23 | 32 | 12,288 | -1,572,864 |
| 24 | 60 | 23,040 | -2,949,120 |

The K24 block is byte-for-coordinate identical to the prior factorized top
provider.  The K20/K22/K23 block is nonzero, so the control correctly rejects
this raw top ledger as a relative certificate.  Its natural representative
also differs from the provider's `repr`-sorted first representative, exercising
the canonical-order guard.

The proof implementation took about 26.9 seconds and wrote 105 coordinates
(7,620 bytes).  This is a semantic control, not a production throughput gate:
its exhaustive row-orbit canonicalization cannot be extrapolated to millions
of columns.  No K24 production or closure was launched while K23 work was
active.

## Exact closure and solve

The eventual membership computation must start at `supp(R24)` and alternately
close through every incident literal column and every lower/top row of each
column.  Closing only the top Gram graph misses lower-kernel relations.  The
closure is complete only when neither a row nor a column is queued; any cap is
inconclusive.

On a complete component there are two equivalent exact routes:

1. solve the full filtered system `B*x=(0,0,0,R24)` and export `x`; or
2. compute a Q-basis `K` of `ker(L)`, form `A24_rel=T*K`, then prove target
   membership by an exact solve or complete Gram rank equality plus norm.

Modular ranks may screen or guide reconstruction, but final publication needs
the exact rational replay and the source coefficient ledger.

## What the source folds must retain

Every K20-to-K24 family must retain its exact atomic interval manifests and
hashes; natural-canonical compact `(w,U)` coefficient runs; column orbit size,
orbit-total `W`, and per-labelled `alpha=W/orbit_size`; exact cancellation
counts; and the full K20 cancellation coefficient ledger that generated R24.
A charge or top-row ledger alone is insufficient.  Raw labelled runs remain
until natural H collection is independently accepted.

Relative closure must additionally retain lower-only correction columns,
sorted K20/K22/K23/K24 projection runs, complete closure checkpoints, the
lower matrix/kernel or direct solve transcript, and the frozen R24 orbit-mass
content.  The 257 distributed witnesses must include source occurrence and
pivot provenance, full multiplier and coefficient, natural representative,
lower outputs, and a terminal K24 output.

## Next bounded gates

After K23 resource clearance, the next gate is a batched 257-column cache
control, followed by a one-source-record alternating closure.  Only measured
shards projecting below 540 seconds, 8 GiB family RSS, 16 GiB aggregate RSS,
and the declared disk floor may proceed.  Scheduling stops by 450 seconds;
outputs are atomic; no cap may be reported as membership.

Scope: schema, theorem, proof provider, and bounded prefix controls only.  No
K24 residual, charge, kernel, membership, or conjecture verdict is claimed.
