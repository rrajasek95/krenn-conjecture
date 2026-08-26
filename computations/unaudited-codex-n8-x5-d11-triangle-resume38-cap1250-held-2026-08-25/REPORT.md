# Held D11 cap-1.25m continuation

`PASS_HELD`: this package freezes the next triangle continuation from cap-1m
production manifest `07410690da03aa6b1509081db9051ca0d1858daf77c502d0b4c2f307658310d8`
and its independently replayed 913,636-column / 924,170-support checkpoint.

The sole engine-source change is the permitted column ceiling
`1,000,000 -> 1,250,000`.  Prime, provider, arithmetic, pivot order,
590-second native wall, checkpoint cadence, and dual-then-selected atomic write
order are unchanged.  The watchdog changes only its RSS contract `32 -> 38 GiB`
and identifying text/schema; wrapper wall remains 600 seconds.

The latest measured peak was 20,707,504 KiB at 913,636 selected columns.
Column-linear projection to 1.25m is 28,331,173.47 KiB; adding a 25% margin
gives 35,413,966.83 KiB (33.773 GiB), below the 38-GiB cap with 4,431,921 KiB
remaining.  This is a feasibility projection rather than a guarantee.  The
latest scan exposed 86,365 violations, while the new cap leaves 336,364 slots
from the sealed seed.

No clearance file or production output exists.  Runner refusal, exact source
and watchdog diffs, selftest, checkpoint pins, and the projection are audited.
No arithmetic was launched and no D12 file was read.
