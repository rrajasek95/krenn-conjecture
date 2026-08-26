# Exact K19 charge-only reduction

The seven signed K19 lineages were reduced through per-thread sorted
`(43-byte profile key, i128 weight)` runs, externally merged, and evaluated
against the frozen 77-cycle functional.  No K19 rows or K20 tails were
collected.

| lineage | full charge | K19-irreducible charge |
|---|---:|---:|
| direct K19 | 202278912 | 141570048 |
| K15 → K4 | -4085887720192/150535 | -15060098304/1309 |
| direct K16 → K3 | -759399129088/385 | -700002729984/385 |
| K14/K2 → K16 → K3 | 0 | 0 |
| direct K17 → K2 | -33926011904/35 | -32586626048/35 |
| K14/K3 → K17 → K2 | -1365535285184128/687225 | -26680301182796032/15806175 |
| K15/K2 → K17 → K2 | -308432594172288/45815 | -31784007866120448/5268725 |
| **combined** | **-25935229532575232/2258025** | **-14857399077330176/1436925** |

The K19-irreducible charge is therefore exactly nonzero.  This is a filtered
charge-migration result, not an ideal nonmembership statement: later K20–K24
tails may carry compensating charge.

All divisions were checked at the uniform scale
`S^2=79412096674310400`.  An independent literal self-test compared 83,968
profile-derived cycle partitions against explicit row replacement, including
K2, K3, and K4 tails.  The K16/K14-derived lineage is exactly empty because
every frozen K14/K2 K16 row is already nonpivotable.

The initial merge reader incorrectly treated the seven-byte `K19WGT1` magic
as eight bytes; it panicked before arithmetic.  The reader was corrected to
the frozen 15-byte header without regenerating runs, as independently flagged.
All merged weights and component results are atomically checkpointed and
pinned by `finalize_k19_charge.py`.

Logical digest:
`bb662ab00ebc3cc9c438da4e82c2cac5c179f30ffdbfb2705c38ec5c4e5f9327`.
