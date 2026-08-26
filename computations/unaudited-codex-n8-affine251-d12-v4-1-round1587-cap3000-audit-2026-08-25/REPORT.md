# Independent D12 round-1587 chain audit

Status: `PASS_EXACT_FULLY_TELEMETERED_ROUND1587_CAP3000_CHAIN`.

The six accepted stages cover exactly rounds 1576 through 1587 with no gap,
overlap, restore materialization, or alternate result-bearing directory. Every
checkpoint retains the preceding ordered column set, and every cache retains
all inherited vector records byte-identically under the same provider
fingerprint. The endpoint is round 1587 with 2,927,014 columns, support 5,598,
and target coefficient one; checkpoint SHA-256 is
`f8c334186186173654878c9f33f4c0d5f1911724e9c95cf5069b2fbd0c89f8aa`
and cache SHA-256 is
`38a4ff6bb1d8f0d39cb7c4914e0e549629fe37df069db2436874cb5ce51f41ae`.

The independent terminal replay checked all 2,927,014 cached columns and
299,051,831 terms. It found 14,868 candidate-hit terms, two target terms, and
zero verification failures. The predeclared block totals were 311.178750 and
329.973032 seconds; maximum RSS was 26,073,328 KiB, below 36 GiB.

The audit pins post-storage-compaction ledger
`e511bba126e2c0dbdfe65e0ab5964c8b55163d13db59f068fec2f46a063ae574`.
This certifies an exact resumable exposed state through round 1587, not CEGAR
closure or a final global dual.
