# Independent r1527 cap-2.5m→2.75m equivalence audit

Verdict: **PASS_EXACT_DIRECT_CAP2500_TO_CAP2750_EQUIVALENCE**.

Both isolated `cold/rare`, hierarchical, nonincremental lanes resumed the same sealed r1526 state and added exactly round 1527. After output-directory normalization, `--column-cap 2500000` versus `2750000` is the sole command difference. Round records and all non-timing semantic fields are equal.

The outputs are byte-identical: checkpoint SHA-256 `a18ac93c6cd33a6182cfa91342e4496de4f6e7cdd15ac15c737480747a0f8e3a` and cache SHA-256 `1e5b9bbbfb2a4c7245c0e999d298675445737056c9dee24af3b1b917cf9cb7d9`. The accepted candidate endpoint is round 1527 with 2,400,337 columns, support 3,389, and 6,735 new columns.

Both watchdogs passed atomically under 36 GiB; maximum elapsed time was 69.601392 seconds and maximum RSS was 25,019,552 KiB. This package accepts `candidate_cap2750` as the restart state. It certifies cap equivalence through r1527 only and makes no r1528 or closure claim.
