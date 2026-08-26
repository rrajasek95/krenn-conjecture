# Held deterministic D11 partial-batch checkpoint patch

Status: **READY/HELD; bounded gates PASS; no production authorized.**

## Exact refinement

The previous engine abandoned a round whenever the violating frontier exceeded
the remaining column capacity.  This sibling instead scans the entire incident
frontier and retains the natural-order minimum prefix of size
`min(remaining_capacity, violation_count)` in a bounded `BTreeMap`.  Only after
the exhaustive scan completes does it insert that prefix, recompute the
normalized modular dual, replay every selected pairing, atomically persist the
dual first and selected columns second, and return `INCOMPLETE_COLUMN_CAP` when
the frontier overflowed.

Natural column order is the already frozen derived order `(generator,
multiplier)`; the multiplier is the natural degree-eleven monomial tuple.  A
257-order hostile/permutation audit and the compiled selftest prove that the
retained prefix is independent of traversal order.  Six hostile source
mutations (reversed comparator, unordered retention, hidden overflow, disabled
terminal, early truncation, and wrong terminal reason) are rejected.

## Why this is exact CEGAR

Let `S` be the currently selected literal source columns and let `lambda` be a
normalized dual with `lambda(t^11)=1` and `lambda(S)=0`.  Every retained column
is independently checked to have nonzero pairing with `lambda`, hence is a
valid counterexample constraint.  For any deterministic subset `P` of those
violations, replacing `S` by `S union P` is a monotone, source-faithful CEGAR
refinement: any new normalized solution annihilates a strictly larger literal
column set, while inconsistency means only modular membership and remains
diagnostic pending exact rational replay.  Prefix choice affects checkpoint
presentation and reproducibility, not the source span or provider equations.

The provider, prime, branch, target, materialization, pairing, incremental
solver, and literal checkpoint formats are unchanged from source SHA
`1f6fdab1...`; only overflow retention/acceptance and result metadata change.

## Bounded evidence

The small fixture passed ten checks, including traversal-invariant natural
prefix selection and exact post-insertion dual replay.  The current
913,636-column / 924,170-support seed diagnostic admitted only eight columns,
so it is not production coverage.  It nevertheless exhausted 762,110 incident
columns, observed 730,426 violations, accepted the eight natural-prefix
columns, and landed a 913,644-column / 924,182-support checkpoint.  Independent
literal replay verified all 913,644 pairings, target coefficient one, and that
all eight additions were nonzero violations of the seed dual.  Wall was
110.355145 seconds and peak RSS 19,864,288 KiB under 38 GiB.

The earlier non-progress engine retained 336,366 materialized violation vectors
at peak RSS 14,563,824 KiB; combined with the new full-frontier top-eight gate,
this supports—but does not prove—the held 336,365-prefix resource projection.
Any future production run remains gated at native 170 / wrapper 180 seconds and
38 GiB and requires an exact clearance naming the sealed manifest.

## Explicit rejection

Further `+1` cap chasing is rejected: cap 1,250,000 found 336,365 violations,
and cap 1,250,001 found 336,366, accepting zero in both cases.  It changes the
boundary without processing a coherent violation batch.  The partial-batch
checkpoint is the exact monotone alternative.  No D12 cache was read, no
second prime or other branch was launched, and no mathematical verdict is
claimed.
