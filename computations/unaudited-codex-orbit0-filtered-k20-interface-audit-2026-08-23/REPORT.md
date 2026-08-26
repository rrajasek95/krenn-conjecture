# RETRACTED: incomplete K20 interface audit

The earlier PASS below is superseded.  No K18-prefix measurement was launched
or accepted after this guard.

The frozen K14-to-K16 collector discarded exactly 75,691,040 pivotable K16
tail occurrences before collection.  Its 1,848,174-row frozen output is only
the nonpivotable normal, so it cannot justify declaring the K14-derived K16
feed empty at higher degrees.  K20 has two omitted primitive paths:

- `(2,4)`: K14 -> K16 -> K20;
- `(2,2,2)`: K14 -> K16 -> K18 -> K20.

The second is an eleventh lineage and has denominator depth three.  A later
independent DP audited all 142 triple products (maximum 2,240) and proved their
LCM is still `U=400591699200`; the arithmetic concern is resolved, but the
lineage omission remains.  The smallest sound next step is to replay
the discarded 75,691,040 K16 occurrences with provenance, census their K4
tails and pivotable K2 children, and only then resume the visible K18 profile
census.

The retraction logical digest is
`8dc4eb6cce02ea7ca7d2830e7c34409e2aa17d87d66267e28ecbdda04f3159e5`;
the complete composition ledger is in `REPORT_K14_DAG_SUPERSESSION.md`.

## Superseded partial audit

K20 receives four degree buckets and ten signed source lineages.  K17 does
feed K20 through K3 tails; K19 cannot, because its minimum K2 tail lands at
K21.

| bucket | exact compact work currently available |
|---|---:|
| direct K20, profile 4+4+4 | 104,760,000 |
| pivotable K16 → K4 | 7,796,351,220 |
| pivotable K17 → K3 | 94,691,368,960 |
| pivotable K18 → K2 | missing; rigorous upper 2,083,678,064,208 |

The signs follow `P=-R8' E0 E1 E2` and `c*head -> -c/m*tail`:

- direct K20 is negative;
- direct K16 gives positive K4 response, while the K14-derived K16 lineage
  would be negative but is exactly empty because all its K16 rows are already
  nonpivotable;
- direct K17 gives positive K3 response; its K14- and K15-derived lineages
  give negative responses;
- direct K18 gives positive K2 response; its K14-, K15-, and direct-K16-
  derived response lineages give negative responses.

The known exact profile interface has 1,033,323 nonzero K16 keys.  The three
K17 lineages have respectively 2,661,633, 13,844,092, and 16,109,793 nonzero
keys; their unweighted union is exactly 25,163,280, giving at most 805,224,960
distinct K3-tail charge evaluations after coefficient cancellation.

The missing interface is precise.  The K18 charge pass retained scalar
pairings and evaluation counts, not its pre-filter parent profiles and
coefficients.  Its four lineages contain 2,226,151,778 pivotable provider-
level parent occurrences, but their outgoing pivot count and key union cannot
be reconstructed from the frozen scalars.

## Corrected integer plan

Use `U=400591699200 = 2^8*3^3*5^2*7^2*11^2*17*23`, not `S^2`, and assert
`U mod (m_first*m_second)=0` on every occurrence.  All exact denominator
products already observed through K17 divide U; their LCM is 1,517,392,800.
The missing K18 replay must stop at the first nonzero U remainder rather than
assuming coverage.  Even the hostile K18 upper bound leaves an i128 safety
margin above 22 billion.

Verdict: do not launch K20 charge yet.  The smallest sound next gate is a
profile-only replay of the four pre-filter K18 lineages, atomically
checkpointed, with exact outgoing-pivot counts, U-remainder audit, and sorted
key union.  A prefix-measured 600s/12GB gate is plausible; no K20 rows or tails
are needed.

Logical digest:
`ea7964f7d6a8120aa9251661a012fcc7965be18a63e9d0df9882fca9e488e57d`.
