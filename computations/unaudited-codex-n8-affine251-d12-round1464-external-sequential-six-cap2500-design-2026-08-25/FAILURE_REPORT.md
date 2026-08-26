# r1464 external portfolio launch failure

The sealed launch failed closed on the first ordered task, `repair/first`.
The watchdog terminated it at 150.80268 seconds for `WALL_CAP` (return code
`-15`), with peak RSS 25,907,776 KiB.  The native 135-second gate was not
observed during the long solve and produced no atomic result before the
150-second wrapper acted.

There is no result, frontier score, or lane evidence, so this attempt provides
zero portfolio coverage.  The remaining five lanes, fixed replay, and cap-2.5m
candidate were not launched.  No state advanced beyond r1463/r1464 input.

The APFS clone checkpoint/cache retain the source sizes and mtimes and no
temporary output exists.  They were not pruned because the evidence-before-
prune precondition was not met, and they were not rehashed.  The exact sealed
135/150-second schedule is not feasible for `repair/first`; retry or widening
requires new authority.
