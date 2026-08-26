# D12 v4.1 exact continuation: round1061 to round1160

Producer status is `PASS_EXACT_PRODUCER_PENDING_INDEPENDENT_REPLAY`.

The fixed cold/rare, 16-worker hierarchical nonincremental solver continued the independently audited round1061 state through exact round1160. Seven atomic stages cover rounds1062--1160 without a gap or overlap. The final state has 959,506 exposed columns and support 990; it stopped only at the requested round cap.

Every stage used frozen source `3139689f...`, binary `79410bc8...`, watchdog v2 `53d95032...`, and a 36 GiB live libproc RSS cap. All watchdog records passed with atomic outputs and no breach. Peak observed RSS was 13,165,296 KiB.

The measured round cost made a single 540-second aggregate projection unsound after stage01. The traversal therefore remained continuous but was divided into two explicit resource blocks: rounds1062--1137 in 509.806545 seconds and rounds1138--1160 in 173.761472 seconds. Each block satisfies the aggregate gate; no arithmetic was repeated.

Independent all-column replay and exact cache-descendant scans are intentionally delegated to the separate referee. This producer report makes no terminal or conjecture claim before that referee seals.
