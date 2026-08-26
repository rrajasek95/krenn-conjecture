# Independent D12 round-1562 chain audit

Status: `PASS_EXACT_FULLY_TELEMETERED_ROUND1562_CAP2750_CHAIN`.

The six accepted stages cover exactly rounds 1551 through 1562 with no gap,
overlap, restore materialization, or alternate result-bearing directory. Every
checkpoint retains the preceding ordered column set, and every cache retains
all inherited vector records byte-identically under the same provider
fingerprint. The endpoint is round 1562 with 2,682,705 columns, support 4,103,
and target coefficient one; its checkpoint SHA-256 is
`1273f400531e889b304d05ada9b0d3611747e7a108dd8791c116da063bdbe37e`
and cache SHA-256 is
`194b364a86d50d1763952c90389c7c5556094edd7ee139f5c48578c3b720d7fe`.

The independent terminal replay checked all 2,682,705 cached columns and
274,179,927 terms against the candidate. It found 11,478 candidate-hit terms,
two target terms, and zero verification failures. The two predeclared
three-stage watchdog aggregates were 270.739863 and 281.042807 seconds; the
maximum observed RSS was 26,943,536 KiB, below the 36 GiB bound.

This certifies an exact resumable exposed state through round 1562. It is not a
claim of CEGAR closure or a final global dual.
