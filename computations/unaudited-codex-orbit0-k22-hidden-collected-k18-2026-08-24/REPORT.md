# Hidden collected-K18 two-sink K22 charge

Status: `PASS_EXACT_TWO_SINK_HIDDEN_COLLECTED_K18_K22_CHARGE`.

One complete scan of all 158,439,965 pinned `H18PIV2` records produced two
strict, separately named scalars:

| lineage | terminal occurrences | scaled charge | reduced charge |
|---|---:|---:|---:|
| `D14:222|R:2-2-4` | 23,956,529,040 | `70538993620749287424` | `257276324772224/1461075` |
| `D14:222|R:2-2-2-2` | 6,843,375,816 | `1440150591691685265408` | `625065360977293952/173867925` |

For the K4 sink the next coefficient is `-w2/m3`; its 399,275,484 selected
K18 pivots each have 60 terminal tails.  For the deep K2 sink, 570,281,318
pivotable K20 children each have exactly one selected K20 pivot and 12
terminal tails, with coefficient `+w2/(m3*m4)`.  All divisions are exact at
`U=400591699200`.

Both sinks have final active-anchor mass two, below every pivot mass four;
full and irreducible counts and charges therefore agree.  The required
1/4,096/1,000,000 gates passed, a 10,000,000-record cache-growth gate projected
393.88 seconds, and the full scan completed in 387.878229 seconds.  Observed
RSS remained below 1.4 GiB, within the 600-second/16-GiB limits.

The producer stored no parent rows.  Its 257-row ledger was independently
random-access replayed from H18PIV2: 40,620 literal K4 and 11,808 literal deep
K2 K22 children were evaluated, and every child was terminal.  No K23 or K24
sink was multiplexed.

Logical SHA-256:
`52bce2d91e3b59fe0bd78e0bbf8932d307d2b91510d55231b57af8058d24b4b5`.
