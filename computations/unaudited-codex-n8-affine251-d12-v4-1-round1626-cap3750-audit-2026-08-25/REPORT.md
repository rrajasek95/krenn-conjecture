# Independent D12 round-1626 chain audit

Status: **PASS exact resumable state.** Starting from the independently accepted cap-3.75m round-1614 state, the twelve producer stages cover rounds 1615 through 1626 exactly once, with no gap, overlap, failed stage, or temporary output.

The independent sole-reader scan verified all twelve checkpoint descendants and all twelve cache-prefix descendants. Every inherited vector record is byte-identical. It then replayed 359,872,273 terms across all 3,528,325 final cached columns: the target coefficient is one, 18,509 terms meet the candidate support, and every cached-column pairing is zero. Independent SHA-256 replay matches the final checkpoint `bbee936b...` and cache `0dd351df...` producer pins.

All twelve native runs stayed below 120 seconds; every hard watchdog passed below 150 seconds and 36 GiB, with maximum observed RSS 25,980,416 KiB. The four predeclared watchdog blocks were 314.608467, 314.753945, 345.447353, and 338.090960 seconds, each below 540 seconds. The proactive round-1624 compaction record was pinned and did not alter the accepted chain.

This certifies round 1626 as an exact restartable `ROUND_CAP` CEGAR state. It is not a closure certificate, a terminal global dual, or a proof of the conjecture; the degree-12 search remains open.
