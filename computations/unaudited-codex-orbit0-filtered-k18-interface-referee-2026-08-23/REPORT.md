# Exact K18 interface and cost audit

K18 has exactly four inputs; K17 does not contribute because every pivot tail
raises K-degree by at least two.

| component | raw compact occurrences |
|---|---:|
| direct `E2E4E4 + E3E3E4` | 152,251,200 |
| K14/K4 response | 397,156,800 |
| K15/K3 response | 1,789,890,560 |
| K16-pivotable/K2 response | 1,559,270,244 |
| total | 3,898,568,804 |

The K16 census is exact: 24,003,767 pivotable H-orbits, 129,939,187
orbit/pivot uses, maximum orbit mass 8,448, and reduced averaging denominators
`1,5,7,11`.  Together with the previous components, the one-page scale
`281,801,520` suffices to construct K18.  Even a hostile collision of every
raw occurrence is over `2.0e16` below `i128::MAX`.

Compact-level correction: 44,342,881 is the collected K15 H-orbit pivot-use
count.  The source-linear stream uses 55,934,080 precollection compact
source-pair pivot uses, hence 1,789,890,560 K3 evaluations.  This is an exact
engineering count for that provider, but it should not be added to collected
H-orbit counts as though they were one literal occurrence measure.

A full K18 row collection is not justified at this cost.  The smallest exact
charge computation uses an enriched local cache keyed by four-path/cycle
profile, anchor-base signature, and pivot word.  It streams about 345 million
parent/lookup operations and accumulates only i128 scalars.  An uncoloured
1,162-profile table alone is insufficient because it forgets the anchor
support needed to decide K18 pivotability.

Proposed hard gate: 180 seconds, 2 GiB, 250,000 cached enriched keys, with an
atomic checkpoint after each of the four components.  No K18 rows or charge
were computed in this audit.

Logical digest:
`24f0c4f28c830b21dda330249359cb98bcde7fed1f44de3662666e35951462a2`.
