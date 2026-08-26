# Held D11 cap-1m continuation

`PASS_HELD`: the next triangle continuation is frozen from the sealed cap-750
production manifest `7d5176a70b409a21b362725d7ae8f710640d5688604d2b10e04d5e3f611d8198`
and its independently replayed 515,869-column / 427,712-support checkpoint.

The sole engine-source change is the accepted column-cap ceiling
`750,000 -> 1,000,000`.  Prime, provider, branch, arithmetic, pivot order,
590-second native wall, checkpoint interval, and dual-then-selected atomic
write order are unchanged.  The watchdog changes only its sealed RSS contract
`24 -> 32 GiB` and identifying strings/schema; its 600-second wrapper and
process-group accounting are unchanged.

The latest measured peak was 12,067,360 KiB at 515,869 selected columns.  A
deliberately conservative column-linear projection is 23,392,295.33 KiB at
one million columns and 29,240,369.16 KiB after a 25% margin (27.886 GiB),
below 32 GiB.  This is a feasibility projection, not a guarantee.  The latest
scan exposed 234,132 violations and the new cap leaves 484,131 slots from the
sealed seed, so one corresponding batch fits arithmetically; later growth is
unknown and remains guarded by checkpoint-first persistence and the watchdog.

No clearance file or output directory exists.  The runner refuses arithmetic
until an explicit clearance names this package manifest.  No D12 file was
read and no arithmetic was launched while preparing this package.
