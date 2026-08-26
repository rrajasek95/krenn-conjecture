# Independent round 1613 chain audit

Verdict: **PASS_EXACT_ROUND1613_CAP3500_CHAIN_WITH_AUDITED_COOPERATIVE_OVERSHOOT**.

The accepted cap-equivalent round-1601 state continues through eleven
atomic descendant edges covering rounds 1602--1613 without a gap or overlap.
The final state has 3,301,528 ordered cached columns and dual support 6,711.
Its checkpoint SHA-256 is
`4bd2b4d8f854e1cedc147f9824b876d3c7d4715e42bbde0cf0112a1bd666b2ac`;
its cache SHA-256 is
`3defad7e9dba3495e1ecdb0f40f0148b1dbe0d79a6f34452db205dcd6a88ec16`.

One independent streaming pass parsed all twelve checkpoints, proved every
checkpoint/cache descendant relation, compared all inherited cache payloads
byte-for-byte, and replayed the final candidate against all 3,301,528
columns.  It processed 336,998,519 literal terms, found 17,371 candidate-hit
terms and two target terms, verified target coefficient one, and found zero
nonzero pairings.

Stage 01's native elapsed 126.429282 seconds exceeded the cooperative
120-second top-of-loop signal.  It is accepted only under the separately
sealed edge audit: the hard 150-second watchdog passed at 128.306338 seconds
with return code zero, no breach, atomic outputs and peak RSS below 36 GiB.
The amended one-round schedule covers all later stages.  Watchdog block sums
are 327.912771, 298.989993, 296.147388 and 196.808257 seconds; maximum peak
RSS is 22,083,840 KiB.

Round 1613 is an exact resumable `ROUND_CAP` state, not a global terminal or
closure certificate.  No continuation was launched by this audit.
