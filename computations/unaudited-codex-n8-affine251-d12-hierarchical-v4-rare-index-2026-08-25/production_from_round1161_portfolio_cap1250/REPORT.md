# D12 v4.1 exact continuation: round1161 to round1261

Producer status is `PASS_EXACT_PRODUCER_PENDING_INDEPENDENT_REPLAY`.

The fixed cold/rare, 16-worker hierarchical nonincremental solver continued the independently audited round1161 state through exact round1261. Ten atomic stages cover rounds1162--1261 without a gap or overlap. The final state has 1,238,541 exposed columns and support 1,065; it stopped at the requested round cap with 11,459 columns of headroom beneath the independently gated 1,250,000 column cap.

Every stage used frozen source `3139689f...`, binary `79410bc8...`, watchdog v2 `53d95032...`, and a 36 GiB live libproc RSS cap. Stages01--03 used a 95-second native wall. Because stage03 consumed 104.227826 of the wrapper's 105 seconds, stages04--10 conservatively lowered only the native wall to 90 seconds. All watchdog records passed with atomic outputs and no breach. Peak observed RSS was 14,755,360 KiB.

The traversal was divided into two resource blocks: rounds1162--1220 in 496.679810 seconds and rounds1221--1261 in 428.310805 seconds. Each block satisfies the 540-second aggregate gate; no arithmetic was repeated.

Independent all-column replay and exact cache-descendant scans are delegated to the separate referee. This producer report makes no terminal or conjecture claim before that referee seals.
