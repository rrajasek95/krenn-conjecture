# Held D11 triangle cap-1.6m continuation

Status: **READY/HELD; useful progress plausible; no launch.**

The next bounded cap is 1,600,000, admitting at most 349,999 new columns from
the sealed 1,250,001-column / 1,378,456-support checkpoint (production manifest
`6a392f8f...`).  The source differs from the proven partial-batch engine only by
two fail-closed configuration restrictions: it accepts only p107 / the triangle
branch, and raises the maximum column cap from 1,250,001 to 1,600,000.  Full
incident scanning, natural-order prefix retention, incremental exact modular
solve, all-selected verification, and dual-first atomic persistence are byte-
identical to the sealed engine.

## Resource bound

The last run peaked at 18,207,312 KiB and accepted 336,365 columns while support
grew by 454,286, or 1.3505745 support rows per accepted column.  Linear scaling
to a full cap-1.6m checkpoint projects support 1,851,156 and peak RSS 24,450,958
KiB.  Applying a conservative 1.5 multiplier gives 36,676,437 KiB (34.98 GiB),
leaving 3.02 GiB below the hard 38 GiB limit.  The corresponding one-scale wall
projection is 222.3 seconds; even a two-scale 444.5-second envelope fits the
590/600-second gate.

This is an evidence-based bound, not a proof of allocator behaviour.  Cap 1.6m
is therefore the largest recommended next gate without first measuring the new
checkpoint; larger caps are rejected for now.

## Progress estimate

The prior full scan observed 730,426 violations and accepted 336,365, leaving
394,061 unaccepted with respect to the old dual.  The proposed 349,999 slots are
88.82% of that count, and recent exact rounds exposed 207,984, 397,767, and
730,426 violations.  Useful progress is consequently plausible.  It is not
guaranteed: recomputing the dual changes both support and pairings, so 394,061 is
not a certified count for the next frontier.

## Frozen acceptance

The held runner pins source `a5d91a45...`, binary `224f5d0a...`, p107, cap
1,600,000, native 590 / wrapper 600 seconds, and 38 GiB.  It refuses without a
new exact clearance and refuses pre-existing output.  The frozen validator
requires monotone seed containment, a complete incident scan before every
accepted batch, exact natural-prefix accounting on overflow, a normalized p107
dual, literal replay of every selected column, target coefficient one, no
temporary files, and an atomic restart pair.  No mathematical verdict is
inferred from an incomplete checkpoint.

Design audit and ten compiled selftests pass; four hostile binary configurations
and five hostile contracts are rejected.  No D12 file was read, and no launch,
p2, other branch, or automatic relaunch occurred.
