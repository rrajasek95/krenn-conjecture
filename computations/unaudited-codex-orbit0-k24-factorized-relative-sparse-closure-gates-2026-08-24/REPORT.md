# K24 mandatory sparse-closure gates and launch decision

## Outcome

Both mandatory bounded gates passed their exact local checks and returned a
decisive **NO-LAUNCH** for broad K24 relative closure or the 103 source shards.
No cap was raised and no broad K24 computation was launched while K15 was
active.

The source-side 257-column Gram is sparse and cheap, but it is not remotely an
ambient closure.  One retained source slice already has 2,042,880 natural
nonzero column orbits after exact cross-group merging, which exceeds the
frozen 1,000,000-column cap before one incidence edge is traversed.  The
arbitrary-word repair then shows that the ambient lower-transfer domain is
strictly larger than the special 78-word/four-block source domain.

## Exact 257-column Gram gate

The 257 distributed literal witnesses supply 257 distinct natural-H column
keys.  The Rust gate expands each unnormalised H-orbit-sum column, sorts
labelled rows blockwise, and accumulates exact upper-triangular Gram entries.
It stores no row output after each block is reduced.

| block | labelled events | unique labelled rows |
|---:|---:|---:|
| K20 | 98,688 | 98,688 |
| K22 | 1,184,256 | 1,184,256 |
| K23 | 3,158,016 | 3,158,016 |
| K24 | 5,921,280 | 5,921,280 |

No labelled row is shared by two sampled columns.  Thus the induced sparse
Gram has `N=257`, `E=257` nonzero upper edges, all diagonal, versus 33,153
dense pairs.  Every diagonal realizes all four special source blocks.

The exact induced algebra has

```text
rank(G20+G22+G23) = 257,     nullity = 0,
dim(K^T G24 K) = 0.
```

For the synthetic target formed with the 257 retained literal coefficients,
the relative-kernel route and full filtered-Gram route both reject bounded
membership.  The exact top norm is `2836062535680/49`, the full-Gram projected
norm is `11344250142720/343`, and their positive gap is
`8508187607040/343`.  Because the induced sample is not ambiently closed, the
only global verdict is `INCONCLUSIVE_INCOMPLETE_CLOSURE`.

The exact Gram plus source-merge gate took 4.874870 seconds, of which 0.942111
seconds was blockwise Gram construction.  Its retained column/edge files are
23,963 bytes.

## Exact one-source-unit gate

The retained direct D17/D18 slice-zero compact binaries were streamed in
natural order and independently re-canonicalized.  Their exact merge is:

| quantity | count |
|---|---:|
| D17 records | 1,689,600 |
| D18 records | 476,160 |
| premerge records | 2,165,760 |
| cross-group duplicate keys | 122,880 |
| exact zero sums | 0 |
| retained natural nonzero columns `N` | 2,042,880 |

All retained orbit sizes are 384.  At minimum, every column contributes its
nonzero self edge, so `E >= 2,042,880`.  Since `N > 1,000,000`, the gate stops
before incidence with `COLUMN_CAP_BEFORE_INCIDENCE`, 2,042,880 queued columns,
and `lower_transfer_below_K20_complete=false`.  This is an exact cap result,
not a performance extrapolation or closure claim.

## Smallest sound arbitrary-word repair

The source fold may keep its compact 78-entry special-word dictionary.  The
relative closure may not: its inverse-incidence oracle must admit every
literal mixed word and create the 105-term matching table on demand.  Columns
and rows are deduplicated in natural `(word tuple,multiplier bytes)` and row
byte order, with the frozen 384-action H group.

One K20 row has 56 natural incident column orbits; only eight use a word in the
special source dictionary and 48 do not.  Completing the next column-to-row
layer over all 56 columns gives 5,077 natural row orbits and 5,880 incidence
edges.  Expanding only the first 257 of those rows already reaches 14,852
columns and 16,391 edges.  The state is therefore
`ROW_LAYER_CAP_257_NOT_COMPLETE`.

The distributed gate starts independently from 257 lower K20 rows and 257
literal K24 target rows:

| layer | unique columns/rows | incidence edges |
|---|---:|---:|
| 257 lower rows -> columns | 18,898 columns | 18,903 |
| 257 target rows -> columns | 21,720 columns | 21,727 |
| combined natural columns | 40,361 columns | — |
| first 257 combined columns -> rows | 26,752 rows | 26,985 |

The forward layer leaves 40,104 columns queued and is
`COLUMN_LAYER_CAP_257_NOT_COMPLETE`.  The engine generated 83 word tables on
demand, including 75 realized arbitrary non-source word tables.  The entire
layered run took 40.408739 seconds, peaked at 580,546,560 bytes RSS, and
retained 4,798,381 bytes.

## Ambient lower-operator correction

The special 35-path source columns have multiplier K degree 20 and output only
in K20, K22, K23, and K24.  Their local lower Gram is correctly
`G20+G22+G23`.  Ambient inverse incidence introduces arbitrary words and
columns whose multipliers can begin below K20.  In the one-row control alone,
the next outputs occupy every block K16 through K24, including 1,354 K21 row
orbits.

Therefore a global relative negative test must use

```text
L = P_<24 B on every realized lower K block,
G_L = sum_{q<24} G_q,
A24_rel = P_24 B restricted to ker(L).
```

Restricting ambient closure to the 78 source words or omitting K21/lower blocks
is now an explicitly rejected hostile mode.  A positive vector from the
special source domain remains valid if all of its lower blocks replay to zero;
failure in that domain is not global nonmembership.

## Projection and shard decision

Linear projection of the measured 257-column forward layer to its current
40,361-column queue is 2,526.10 seconds, 4,201,314 rows, and 4,237,905 edges.
That exceeds both the 540-second and 1,000,000-row gates before any subsequent
alternating layer.  Broad relative closure and all 103 source shards are
therefore not launchable.

The largest presently recommended next action is **one further bounded tile
of at most 2,048 columns**, after explicit resource clearance.  Conservative
linear projections are 128.18 seconds, 4,626,300,992 bytes peak RSS, 213,184
rows, and 215,040 edges.  This is a measurement tile only.  One source unit
would require at least 998 such seed tiles even before ambient growth, and
cross-tile incidence must be globally merged; no collection of capped tile
passes is a completeness certificate.

The independent referee passes under standard Python, `-O`, and isolated
`-I -S`, and rejects six hostile incomplete-lower/word/cap/verdict mutations.
Scope is bounded gates, the arbitrary-word repair, and next bounded-tile
sizing only.  No K24 charge, membership, negative certificate, or production
claim is made.
