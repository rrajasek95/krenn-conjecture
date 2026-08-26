# D12 r1641 cap4.25m one-round continuation — HELD

Status: **HELD_AWAIT_SYMBOLIC_REFEREE_AND_EXPLICIT_MANAGER_CLEARANCE**. No clone, large endpoint read, or arithmetic run has occurred.

The input is the independently accepted r1640 state: 4,069,711 columns, support 76,616, checkpoint `12f79c86...`, and cache `1d7ce92a...`. Independent replay `6cee2cf9...` checked all 414,162,800 terms with normalized target 1 and zero failures; referee manifest `15d1b995...` is pinned.

The previous round added 101,342 columns. Applying the prescribed conservative 1.25 multiplier gives `ceil(101342*1.25)=126678`. Current cap headroom is 180,289, so one projected round fits (`4,196,389`, leaving 53,611), while two do not (`253,356 > 180,289`). This is a resource projection, not a mathematical bound on actual growth; an over-ceiling but otherwise exact output must be held for review.

The pre-arithmetic admission guard is **not at risk under the 1.25 projection**: projected growth uses 70.264% of available headroom. It would reject only at 180,290 new columns or more, a growth factor of about 1.77903 over r1640. Because 1.25 is not a theorem, unconditional guard risk is nonzero and unquantified. If the guard fires, the only acceptable outcome is fail-closed `COLUMN_CAP`, zero r1641 coverage, byte-unchanged input, and no temporary output; it is not an algebraic failure or a resumable r1641 state.

If separately approved, the sole run is a fresh r1640 clone with frozen source/binary/watchdog, cap4.25m, target r1641, cold/rare/hierarchical/16/nonincremental, native210, wrapper240, and RSS36. It must publish exactly one r1641 record atomically, preserve all 4,069,711 inherited cache records byte-for-byte, pass a strict checkpoint-descendant scan and full replay, and contain no r1642. A hard wrapper breach is rejected. Native210 remains a cooperative top-of-loop bound; any reported native overshoot is held for individual classification rather than accepted generically.

The design-time free space was 153,585,356KiB, above the frozen 88,080,384KiB floor, but this must be remeasured immediately before cloning. All r1640/r1641 payloads are protected until an independent r1641 audit passes. Only afterward may the superseded r1640 cp/cache or separately sealed old clone payloads be proposed for exact enumerated compaction. The process must stop at r1641 for a mandatory cap review; r1642 is not authorized.
