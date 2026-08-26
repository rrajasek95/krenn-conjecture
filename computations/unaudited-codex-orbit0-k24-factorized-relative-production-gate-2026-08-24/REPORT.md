# Factorized exact K24 relative-interface production gate

## Outcome

The exact relative interface has been reduced to a sparse, word-factorized
representation and its algebra has passed a bounded literal control.  No K24
production was launched.  The implementation is ready for the next bounded
257-column and one-source-unit closure gates, but a full relative closure is
**not yet resource-cleared**.

For a natural-H column orbit `C=[(w,U)]`, store the mixed word `w` once through
an at-most-78-entry word dictionary and retain only

```text
word_id:u8 | sorted_multiplier:u8[20] | orbit_size:u16_le
| orbit_total_mass_scaled_U:i128_le                         (39 bytes)
```

The shared table for `w` contains its 105 physical-perfect-matching terms and
their K degrees.  Every literal output is reconstructed exactly as
`sort(U + term)`.  Thus the same source record supplies all four blocks
`K20,K22,K23,K24`; no output row or row-orbit canonicalization is retained.

## Exact factorization theorem

Let `H` be the frozen 384-action group, let `B_q(C)` be the literal output
counter of `C` in K degree `q`, and let the unnormalised orbit-sum column be
`B_q[C]=sum_{c in Orb(C)} B_q(c)`.  H-invariance and transitivity give

```text
<B_q[C],B_q[D]>
  = |Orb(C)| * sum_{d in Orb(D)} <B_q(C_0),B_q(d)>.
```

The reverse expression with `C,D` interchanged is checked as an exact symmetry
guard.  Each literal inner product is a sparse matching-term convolution:
`M-M' = U'-U` in the selected K block.  Consequently Gram entries require one
shared 105-term table per word and one H orbit of the right multiplier, not a
materialized row orbit.  The sparse upper-triangular edge record is

```text
left_id:u64 | right_id:u64 | G20:u64 | G22:u64
| G23:u64 | G24:u64                                    (48 bytes)
```

Set `G_L=G20+G22+G23`.  Positive definiteness of the rational row inner
product proves `ker(G_L)=ker(L20)`.  For an exact rational kernel basis `K`,
the relative Gram is

```text
G_rel = K^T G24 K,
```

which is equivalent to solving with the full filtered Gram
`G_L+G24` against `(0,R24)`.  A complete certificate must pass exact rank and
norm identities (or export and replay an explicit rational solution); modular
ranks may only be screening aids.

## Bounded equivalence control

The natural column
`00000022:0d0d11192d50525667748591b0b2becfdfe9eaed` has orbit size 384.
The pinned exhaustive provider emits 40,320 literal outputs and 105 row-orbit
coordinates.  The factorized provider stores no rows and reproduces the exact
block self-Grams:

| block | exact Gram |
|---:|---:|
| K20 | 384 |
| K22 | 4,608 |
| K23 | 12,288 |
| K24 | 23,040 |

The lower Gram is 17,280 and the top Gram is 23,040.  The exhaustive column
took approximately 26.9 seconds; the factorized replay took 0.099128 seconds,
an observed 271.37-fold speedup.  The test also proves the fast natural
minimum-word/fibre canonicalization equals brute-force H canonicalization and
that the minimum word fibre has 32 actions and 32 distinct multiplier images.

The one-column relative algebra control has lower rank one and nullity zero,
so it cannot span its nonzero target.  Both the kernel and full-Gram routes
agree, but the component status is `COLUMN_CAP_1_NOT_COMPLETE`; its only valid
global verdict is **INCONCLUSIVE**.

## Coverage and shard plan

The held source plan pins the frozen 35-path/10-group contract exactly and
partitions it into six disjoint source families:

| source family | IDs | shards |
|---|---:|---:|
| hidden collected K18 | 1 | 6 |
| hidden decorated K16 pair source | 1 | 6 |
| K14 formula source | 2 | 8 |
| grouped direct K15 source | 6 | 16 |
| grouped direct K16 rows | 12 | 6 |
| direct D17/D18 formula source | 13 | 61 |
| **total** | **35** | **103** |

Every explicit interval is exact, positive, contiguous, and has neither a gap
nor overlap.  The direct D17/D18 family uses the frozen rule
`[8*j,min(8*(j+1),485))`, `j=0..60`; it supersedes the unsafe eight-large-shard
proposal.  Global merge is an exact signed-i128 merge on natural column key,
requires identical orbit sizes on duplicate keys, and drops only exact zeros.

## Resource projection

The measured direct D17/D18 one-slice prefix contains 2,165,760 column orbits:
84,464,640 bytes in the 39-byte compact format and 227,504,853 retained core
bytes.  Linear full-source projections are 40,965,350,400 compact bytes and
110,339,853,705 retained core bytes.  The optimized source prefix took
47.647184 seconds; an eight-slice shard projects to 381.177472 seconds, below
the 540-second internal gate, whereas the serial full source projects to
23,108.88424 seconds.

Dense Gram construction is impossible and is fail-closed: the single-slice
prefix alone would have 2,345,259,271,680 upper-triangle pairs, or
112,572,445,040,640 bytes at 48 bytes per edge.  Production must instead use
target-rooted alternating incidence closure and retain only reached nonzero
edges.  Its exact storage formula is

```text
39*N_reached_columns + 48*E_nonzero_edges + checkpoint metadata.
```

Neither `N` nor `E` is projected from the one-column control.  Relative
closure/kernel production is therefore held until the 257-column control and
one-source-unit closure measure edge growth, wall time, RSS, and disk.

## Fail-closed publication rules

Source families run one at a time with atomic outputs, no overwrite, scheduling
stopped by 450 seconds, a 540-second internal wall, a 600-second external
alarm, 8 GiB family RSS, 16 GiB aggregate RSS, and a disk preflight of at least
the projected retained output plus 8 GiB (never less than 16 GiB).  Any
`COLUMN_CAP`, `ROW_CAP`, `EDGE_CAP`, `WALL_CAP`, or `DISK_CAP` is inconclusive.
Duplicate/missing/extra IDs, inexact orbit division, inconsistent orbit sizes,
dense-pair requests, non-atomic intervals, and incomplete queues are rejected.

There is one essential scope distinction.  An explicit `x` in the B20 domain
with `L20*x=0` and `T*x=R24` is a valid global positive certificate.  Failure
inside that domain is **not** a global negative certificate: a negative result
also requires complete lower-transfer source closure below K20.  The schema and
validator encode this correction.

The referee passes under standard Python, `-O`, and isolated `-I -S` execution
and rejects five hostile mutations.  Scope is the factorized B20 theorem,
bounded controls, and held exact all-35 plan only.  No K24 charge, residual,
membership, or conjecture verdict is claimed.
