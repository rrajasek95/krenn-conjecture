# Held D11 exact one-step cap-1,250,001 continuation

`PASS_HELD`: this package keeps the unchanged 913,636-column / 924,170-support
checkpoint from production manifest
`97b468162f7c5c58ecfc3c35f124d5c052738bc63cd8d6a2eaa2a995e7553825`.

The sole engine-source change is the cap guard `1,250,000 -> 1,250,001`.
The launch command has the identical one-column cap change.  The 38-GiB
watchdog is byte-identical, and prime, provider, math, pivot order, native
590-second wall, wrapper 600-second wall, and checkpoint-first dual-then-selected
write order are unchanged.

This exposes exactly 336,365 slots from the seed, matching the 336,365
violations observed before the prior scan truncated.  That equality guarantees
capacity for the observed prefix, not that the full unseen violation set has no
additional column; a 336,366th violation would still fail closed without a
partial batch.  Latest-peak linear projection with a 25% margin is 35.022 GiB,
below 38 GiB.

No clearance or production output exists.  Runner refusal and exact diffs are
audited; no arithmetic was launched and no D12 file was read.
