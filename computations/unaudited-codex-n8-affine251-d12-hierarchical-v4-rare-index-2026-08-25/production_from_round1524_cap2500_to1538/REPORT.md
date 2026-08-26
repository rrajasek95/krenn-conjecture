# D12 round 1524 to 1538 producer checkpoint

Stage 1 is exact and accepted through round 1526. It exposed 2,393,602 columns with support 3,341 in 86.134508 watchdog seconds and peaked at 25,713,664 KiB RSS.

Production stopped before stage 2 under the frozen cap-safety rule. The first two rounds added 14,276 columns. With six stages remaining, the 1.25-times projection needs 107,070 columns of headroom, while the 2.5 million cap leaves only 106,398. The 672-column shortfall is small but positive, so no round1527 arithmetic was launched.

Disk and resource gates passed. Continuation now requires a separately accepted cap increase or explicit replacement of the projection rule; this package makes no round1538 claim.
