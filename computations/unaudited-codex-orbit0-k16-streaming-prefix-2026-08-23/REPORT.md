# Orbit-zero K16 streaming-prefix audit

## Verdict

The literal K14-to-K16 source operator is streamable with complete provenance,
but the 42-row lexicographic seed is not a terminal leaf block.  For Tail's
fixed K14 monomial there are exactly eight source pivots.  Their 96 K16 tail
occurrences collect to 42 rows, the resulting matrix `B` has exact rank eight,
and the common K14 head has a seven-dimensional kernel whose image in `B` has
rank seven.  Every one of the 16 raw private rows is itself K0-pivotable, so
the private leaves feed the next filtration page rather than closing it.

## Exact local census

The source monomial is

```text
q      = 000004080d1955627575797d97c4c6cfd3d7e0e6eaeef2f3
r8     = 000d1955627597c4c6e0e6f3
packet = 00040875797dcfd3d7eaeef2
```

and `q = sort(r8 + packet)`.  The eight dividing mixed rows have pair-colour
labels

```text
0100 0200 1000 1100 1200 2000 2100 2200.
```

Each full source column has the exact K-profile

```text
K14: 1, K16: 12, K17: 32, K18: 60.
```

At K16 the owner histogram on the 42 distinct rows is

```text
owner multiplicity 1: 16 rows
owner multiplicity 2:  8 rows
owner multiplicity 3: 16 rows
owner multiplicity 8:  2 rows
```

Thus every column has two raw private rows.  Exact rational elimination gives

```text
rank(B) = 8
rank(common K14 head) = 1
dim ker(common head) = 7
rank(B restricted to the explicit seven head differences) = 7.
```

The packet records, for every emitted row, the source word, anchor, multiplier,
matching index, physical perfect matching, generator term, and coefficient.
A deterministic leaf peel was interrupted after four pivots, serialized,
resumed, and checked byte-for-byte against an uninterrupted eight-pivot peel.

## Symmetry and streaming consequence

The factor stabilizer has order 384, while the stabilizer of this literal `q`
inside it is trivial.  Therefore an H-orbit provider must transport `q` and
its source provenance together; quotienting the 42 local rows alone is not
sound.  The local rows have 21 literal anchor signatures and nine canonical
signature types.  Only two lie in the selected global 25-type irreducible
cover because this local shell deliberately includes the 16 immediately
reducible rows.

The frozen collected K16 residual has 3,740,320 irreducible occurrences,
1,848,174 nonzero H-orbits, 25 projected anchor signatures, and 701,717,184
labelled rows.  Its source operator is nevertheless local:

```text
(q, scalar, word, anchor, provenance)
    -> sort((q-anchor) + tail_j), j=1,...,12.
```

It needs only `O(12)` row memory per occurrence.  Lossless global collection
requires an external keyed sort/reducer or an equivalent bounded partition;
the 25 projected signatures alone discard literal labels and coefficients.
This is an engineering feasibility result, not a K16 membership theorem.

Tail independently reports that closure from the 42-row shell reaches 3,625
source columns and 67,315 K<=16 rows, and a partial whole-row BFS already
reaches 5,839 columns and 102,110 rows after 73 processed rows.  Those counts
are pinned in the result as a crosscheck, not recomputed here.

## Replay

```bash
python3 computations/unaudited-codex-orbit0-k16-streaming-prefix-2026-08-23/audit_k16_streaming_prefix.py
```

The exact result logical SHA-256 is
`ad9c10dc122e74a600e2eea03fa63f44f3f86b875ef232c1c3efd43eff044126`.
The packet logical SHA-256 is
`600cddfb75dd31fa9766bc9ce539ada7580ac400316783e564757320aa0f64e1`.
The local row and column digests are respectively
`01449c5df38736f3ad0e3404e684f12ed762c4cad596eac3ffaa74afef1b1331`
and
`d7d1b37f152df3e720767be1aa395599228994b6240193db91a8d18b4a82fff5`.
