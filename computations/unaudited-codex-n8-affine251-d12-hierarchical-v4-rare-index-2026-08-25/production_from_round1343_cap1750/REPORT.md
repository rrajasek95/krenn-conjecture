# D12 v4.1 exact continuation: round1343 to round1362

Producer status is `PASS_EXACT_PRODUCER_PENDING_INDEPENDENT_REPLAY`.

The fixed cold/rare, 16-worker hierarchical nonincremental solver continued the independently gated round1343 state through exact round1362. Three atomic stages cover rounds1344--1362 without a gap or overlap. The final state has 1,582,672 exposed columns and support 2,043; it stopped at the requested round cap with 167,328 columns of headroom beneath the 1,750,000 cap.

Every stage used frozen source `3139689f...`, binary `79410bc8...`, watchdog v2 `53d95032...`, a 90-second native wall, a 115-second wrapper wall, and a 36 GiB live libproc RSS cap. All watchdog records passed with atomic outputs and no breach. Peak observed RSS was 21,280,560 KiB.

The exact rounds1344--1362 block consumed 294.746940 watchdog seconds, below the 540-second aggregate cap. No arithmetic was repeated.

Independent all-column replay and exact cache-descendant scans are delegated to the separate referee. This producer report makes no terminal or conjecture claim before that referee seals.
