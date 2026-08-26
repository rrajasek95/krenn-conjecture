# Independent D12 round-1575 chain audit

Status: `PASS_EXACT_FULLY_TELEMETERED_ROUND1575_CAP3000_CHAIN`.

The six accepted stages cover exactly rounds 1564 through 1575 with no gap,
overlap, restore materialization, or alternate result-bearing directory. Every
checkpoint retains the preceding ordered column set, and every cache retains
all inherited vector records byte-identically under the same provider
fingerprint. The endpoint is round 1575 with 2,802,423 columns, support 4,229,
and target coefficient one; checkpoint SHA-256 is
`2012b6bcb82d9b4e873a23bb359b9285c9f2bb8fef080e18457648b127faba89`
and cache SHA-256 is
`82f85642cd0f1cd1062f748ee2dd661b0e4044cf1695076f72c9dd241f726ce0`.

The independent terminal replay checked all 2,802,423 cached columns and
286,376,890 terms. It found 11,737 candidate-hit terms, two target terms, and
zero verification failures. The predeclared block totals were 289.659816 and
301.756149 seconds; maximum RSS was 26,684,944 KiB, below 36 GiB.

This certifies an exact resumable exposed state through round 1575. It is not a
claim of CEGAR closure or a final global dual.
