# Exact pre-filter K17 profile census for K19

The three omitted pre-filter K17 streams were reconstructed source-linearly
without emitting K19 tails or collecting K19 rows.

| lineage | sign at K19 | children | pivotable | outgoing pivots | unique enriched keys |
|---|---:|---:|---:|---:|---:|
| direct K17 | + | 82,938,880 | 81,076,480 | 267,564,800 | 2,792,924 |
| K14/K3 response | - | 211,816,960 | 197,414,400 | 815,482,880 | 14,764,328 |
| K15/K2 response | - | 671,208,960 | 451,445,760 | 1,876,057,600 | 17,066,512 |
| **total** | | **965,964,800** | **729,936,640** | **2,959,105,280** | **34,623,764 before overlap** |

The exact union is 25,163,280 enriched response keys.  It would require
301,959,360 distinct K2-tail charge evaluations after coefficient aggregation,
versus 35,509,263,360 without the cache.  The three censuses plus sorted merge
finished in about 112 seconds and wrote 1.42 GiB of key files.

Every key records the labelled endpoint path profile, closed cycles, anchor
signature, and outgoing pivot.  The program checked
`S^2 mod (m_first*m_second) = 0` on every one of the 2,959,105,280 outgoing
pivot uses, so `S=281801520` gives an exact uniform denominator guard.

Verdict: a K19 charge-only pass is feasible, but should use per-thread sorted
`(key,i128 coefficient)` runs and an external merge under a 300s/8GB gate,
checkpointed after each lineage.  A monolithic 180-second in-memory map is too
close to the measured boundary.  This result makes no K19 charge or membership
claim.

Logical digest:
`c39a37ad2c64c0bff75dda15483bcdd59fe5fd65868c1882fa3b0e40f87b4a3b`.
