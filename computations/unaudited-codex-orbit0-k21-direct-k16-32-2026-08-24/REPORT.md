# Exact grouped direct-K16 `R:3-2` K21 charge

## Verdict

`PASS_COMPLETE_GROUPED_SIX_D16_R_3_2_K21_CHARGE`, followed by
`PASS_STRICT_GROUPED_SIX_ID_D16_R_3_2_TERMINAL_AUDIT`.

For exactly the grouped six-ID packet

```text
D16:{224,233,242,323,332,422}|R:3-2
```

the exact U-scaled 77-cycle charge is

```text
-643522419678967234560 / 400591699200 = -618475450368/385.
```

All `24,501,392,256` emitted K21 child occurrences are irreducible: full and
irreducible counts and charges agree exactly.

No individual-ID scalars are reported.  The authoritative
`checkpoint_direct_k16.bin` record is only a canonical literal row plus its
collected signed coefficient; the producer stores no packet label.  The six
source packets are therefore inseparable after exact collection, and assigning
individual scalars would fabricate provenance.

## Exact grouped counts

| quantity | exact value |
|---|---:|
| retained direct-K16 rows | 24,097,095 |
| signed source coefficient | 1,464,625,152 |
| source coefficient L1 | 13,978,655,136 |
| pivotable K16 rows | 24,003,767 |
| selected p1 uses | 129,939,187 |
| K3 / K19 child occurrences | 4,158,053,984 |
| pivotable K19 child occurrences | 1,295,008,880 |
| selected p2 uses | 2,041,782,688 |
| terminal K2 / K21 child occurrences | 24,501,392,256 |

The first six values replay the frozen direct-K16 producer and its previous
literal export exactly.  The identities

```text
4,158,053,984 = 32 * 129,939,187
24,501,392,256 = 12 * 2,041,782,688
```

hold occurrencewise.  The `(m1,m2)` histogram sums to 1,295,008,880 and its
m2-weighted sum is 2,041,782,688.

## Literal provenance and exact compression

Every retained K16 row and p1 is expanded through all 32 literal K3 tails.
The resulting literal K19 row determines its exact second pivot set.  Thus no
profile-only artifact is consulted before p2, and no topology or decorated
anchor information needed by the second pivot is lost.

Compression begins only after the last pivot decision.  Terminal K2 response
values are cached by

```text
(path profile, literal anchor signature, p2, degree=2).
```

This key is sufficient at that boundary because no later pivot decision is
made from it.  For every cache miss the literal response routine asserts

```text
full_n = irreducible_n = 12
full_q = irreducible_q.
```

Exact-key hits then reuse that terminal fact.  The full run made
1,958,648,097 cache hits and 83,134,591 misses.  Deterministic range resets
bounded the peak cache to 1,282,417 keys.  No row checkpoint or large
intermediate output was written.

The sign is also occurrencewise.  If `v` is the retained direct coefficient
in `P`, the first normalized response has coefficient `-v/m1` and the second
has `+v/(m1*m2)`.  Every occurrence asserts
`U mod (m1*m2) = 0` for `U=400591699200`.

## Prefix and resource gate

A small leading prefix was correctly rejected as a runtime estimator because
the sorted early rows have 14--15 first pivots, versus 5.39 on average in the
full checkpoint.  The accepted bounded gate used 800,000 rows in 256 evenly
spaced contiguous slices.  It completed in 7.715 seconds and projected
232.394 seconds full.

The full 24,097,095-row replay used the same 256-range, eight-worker schedule
and completed in 201.593 seconds, under the hard 600-second alarm and source
assertion.  Cache resets at each deterministic range bound memory independently
of total stream length.  Output consists only of compact JSON/TSV metadata and
a rebuildable executable; there is no bulk-row artifact.

The terminal TSV contains 257 literal witnesses at checkpoint indices
`floor(j*(24097095-1)/256)`, `j=0,...,256`.  The checker seeks directly into
the frozen checkpoint to reproduce each literal row and coefficient, then
independently recomputes its first-pivot set.

## Replay and scope

```sh
rustc -O computations/unaudited-codex-orbit0-k21-direct-k16-32-2026-08-24/run_k21_direct_k16_32.rs \
  -o computations/unaudited-codex-orbit0-k21-direct-k16-32-2026-08-24/run_k21_direct_k16_32
computations/unaudited-codex-orbit0-k21-direct-k16-32-2026-08-24/run_k21_direct_k16_32 --workers 8
python3 computations/unaudited-codex-orbit0-k21-direct-k16-32-2026-08-24/audit_k21_direct_k16_32.py
```

This is one exact grouped scalar for the six named K21 lineages only.  It does
not reconstruct individual packet charges, include another K21 ID, collect
K21 rows, emit K22 tails, infer membership, or make a conjecture verdict.
