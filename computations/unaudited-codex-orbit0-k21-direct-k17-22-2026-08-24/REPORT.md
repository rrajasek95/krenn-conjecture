# Exact seven-ID direct-K17 `R:2-2` K21 charge

## Verdict

`PASS_COMPLETE_SEVEN_D17_R_2_2_K21_CHARGE`, followed by
`PASS_STRICT_SEVEN_ID_D17_R_2_2_TERMINAL_AUDIT`.

The authoritative direct-K17 source replay gives the exact U-scaled
77-cycle charge

```text
-196205097632820756480 / 400591699200 = -17142587904/35
```

for exactly

```text
D17:{234,243,324,333,342,423,432}|R:2-2.
```

No other K21 lineage ID is included or inferred.  All
`17,387,366,400` emitted K21 child occurrences were checked terminal:
full and irreducible occurrence counts and charges agree literally.

## Per-ID result

| ID | K17 heads | pivotable K17 | p1 uses | pivotable K19 children | p2 uses | terminal K21 occurrences | 77-charge |
|---|---:|---:|---:|---:|---:|---:|---:|
| `D17:234\|R:2-2` | 11,174,400 | 11,174,400 | 33,523,200 | 124,780,800 | 173,203,200 | 2,078,438,400 | `177073408` |
| `D17:243\|R:2-2` | 11,174,400 | 10,243,200 | 25,142,400 | 83,808,000 | 119,193,600 | 1,430,323,200 | `-789278208/7` |
| `D17:324\|R:2-2` | 11,174,400 | 11,174,400 | 50,284,800 | 201,139,200 | 312,883,200 | 3,754,598,400 | `2625549824/35` |
| `D17:333\|R:2-2` | 15,892,480 | 15,892,480 | 49,664,000 | 158,924,800 | 238,387,200 | 2,860,646,400 | `-8038687744/35` |
| `D17:342\|R:2-2` | 11,174,400 | 11,174,400 | 50,284,800 | 201,139,200 | 312,883,200 | 3,754,598,400 | `-1044019712/7` |
| `D17:423\|R:2-2` | 11,174,400 | 10,243,200 | 25,142,400 | 83,808,000 | 119,193,600 | 1,430,323,200 | `-236885504` |
| `D17:432\|R:2-2` | 11,174,400 | 11,174,400 | 33,523,200 | 124,780,800 | 173,203,200 | 2,078,438,400 | `-469537024/35` |
| **total** | **82,938,880** | **81,076,480** | **267,564,800** | **978,380,800** | **1,448,947,200** | **17,387,366,400** | **`-17142587904/35`** |

The p1 counts independently replay the frozen direct-K17 census.  The
`3,210,777,600 = 12 * 267,564,800` first K2 children are retained
occurrencewise until their literal second pivot set is known.

## Source-faithful compression boundary

The old K19 charge runs are not prolongable: they aggregate by a 43-byte
path-profile key and discard exact-zero aggregates.  This evaluator therefore
replays the 485 signed R8prime records and the seven explicit factor sectors
from `filtered_k16_structure.bin`.

Before the second pivot the memoization key is the complete sorted literal
K17 row plus the selected p1.  Thus no topology, anchor multiplicity, or
literal placement needed for the second pivot is omitted.  Equal keys emit
identical literal first tails, second pivot sets, terminal tails, and cycle
values, so exact source masses may combine by linearity.  In the full run all
267,564,800 such lookups were distinct; this is evidence that the literal
boundary is necessary rather than a claimed compression win.

Compression occurs only after the literal K19 child and p2 are known.  The
terminal response key is `(path profile, literal anchor signature, p2,
degree=2)`.  It is sufficient because no later pivot decision is made from
it.  Record-bounded caches made `1,362,609,882` exact hits from `86,337,318`
misses, with at most 551,680 literal first keys held per R8 record.  No row
checkpoint or large intermediate file was written.

For every terminal cache miss the evaluator ran the existing literal
response routine and asserted

```text
full_n = irreducible_n = 12
full_q = irreducible_q.
```

Cache hits reuse exactly that terminal key, proving all K21 children in this
seven-ID computation irreducible.

## Prefix, resource gate, and provenance

The current eight-record/eight-worker prefix completes in 2.321 seconds and
projects 140.681 seconds for all 485 records.  The full run completed in
145.499 seconds, below the hard 600-second gate.  Both caches are reset per R8
record, so memory does not grow with the full source length.  Package output
is below 1 MiB excluding the rebuildable executable; there is no bulk row
output.

The full sample TSV contains 257 literal witnesses at the evenly distributed
R8 indices `floor(j*484/256)`, `j=0,...,256`.  The checker reconstructs every
sample row from its R8 source and three literal factor tails, checks its signed
source mass, and independently recomputes first-pivot availability.

The sign is fixed occurrencewise.  If `M` is the signed R8prime orbit mass,
the direct coefficient in `P=-R8' E0 E1 E2` is `-M`; the first normalized
response is `+M/m1`, and the second is `-M/(m1*m2)`.  Every division asserts
`U mod (m1*m2) = 0` with `U=400591699200`.

## Replay and scope

```sh
rustc -O computations/unaudited-codex-orbit0-k21-direct-k17-22-2026-08-24/run_k21_direct_k17_22.rs \
  -o computations/unaudited-codex-orbit0-k21-direct-k17-22-2026-08-24/run_k21_direct_k17_22
computations/unaudited-codex-orbit0-k21-direct-k17-22-2026-08-24/run_k21_direct_k17_22 --workers 8
python3 computations/unaudited-codex-orbit0-k21-direct-k17-22-2026-08-24/audit_k21_direct_k17_22.py
```

This is an exact immediate K21 cycle-charge result for the seven named
lineages only.  It does not collect K21 rows, emit K22 tails, assemble other
lineages, infer K21 membership, or make a conjecture verdict.
