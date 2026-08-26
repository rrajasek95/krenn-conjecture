# D12 v4.1 exact continuation: round 1627 to round 1639

Producer verdict: `PASS_PRODUCER_EXACT_CHAIN_HELD_FOR_INDEPENDENT_AUDIT`.

The fixed cold/rare hierarchical 16-worker nonincremental solver advanced the
independently accepted round-1627 state through twelve contiguous one-round
stages to round 1639. The endpoint has `3,968,369` exposed columns and dual
support `32,704`; it retains `INCOMPLETE_SEARCH_CAP / ROUND_CAP` status, so this
package does not claim a completed finite certificate.

Every stage loaded exactly the preceding stage's column count, published atomic
checkpoint/cache/result files, and has a PASS hard watchdog with no breach and
peak RSS below 36 GiB. Watchdog block totals were `342.493546`, `359.461065`,
`408.832617`, `303.108930`, and `167.219453` seconds, each below 540 seconds.

The load-bearing exceptions are explicit and narrow. Rounds 1633, 1634, 1638,
and 1639 completed their exact target round after the cooperative native-wall
check but before their hard watchdog; the already audited top-of-loop semantics
apply individually and do not create a generic relaxation. Round 1635 alone is
the authorized exact-target `WALL_CAP` endpoint with atomic hard-watchdog PASS.
The growth guard was raised metadata-only to 75,000 for round 1639, whose actual
growth was 66,458. Source, binary, arithmetic, strategy, cap, RSS, and watchdog
logic remained frozen.

A disk hold after round 1636 was resolved by an explicitly authorized 18-file
compaction. The exact pre-delete hashes/sizes are retained in the central
compaction ledger; measured recovery was `29,418,060 KiB`. The active chain,
accepted input, all small evidence, and the refused wrapper-155 attempt were
preserved.

Final pins:

- result: `fa13a36deac596f3b01cb1781208f6e4459c5cd1ade1ceb071f64f30cf60423b`
- watchdog: `1841fed59e55911fdca24c5b4b6d115a412b611a01dfc6b5e23163cd1039fc6c`
- checkpoint: `ab63c22095dd44d771525af9ba218ee36c9e6f4236a80addbc15692165c531a5`
- cache: `4d342801fa9e6d25aff95d7b1172f5bff803e8436c01f9237b79e5a42bf6999e`

No round-1640 directory or arithmetic exists. Independent review must verify all
twelve descendant edges and replay all `3,968,369` final cached columns before
the endpoint is accepted for further mathematical continuation.
