# D12 v4.1 exact continuation: round1262 to safe-stop round1342

Producer status is `PASS_EXACT_SAFE_STOP_PENDING_INDEPENDENT_REPLAY`.

The fixed cold/rare, 16-worker hierarchical nonincremental solver continued the independently audited round1262 state through exact round1342. Ten atomic stages cover rounds1263--1342 without a gap or overlap. The final state has 1,491,824 exposed columns and support 1,954.

Every stage used frozen source `3139689f...`, binary `79410bc8...`, watchdog v2 `53d95032...`, a 90-second native wall, and a 36 GiB live libproc RSS cap. Stages01--06 used a 110-second watchdog; stages07--10 used 115 seconds as wrapper-only post-write safety headroom. All watchdog records passed with atomic outputs and no breach. Peak observed RSS was 21,139,296 KiB.

The traversal was divided into two resource blocks: rounds1263--1307 in 492.138955 seconds and rounds1308--1342 in 489.726234 seconds. Each block satisfies the 540-second aggregate gate; no arithmetic was repeated.

Production stopped before launching stage11 because only 8,176 columns remained beneath the 1,500,000 cap. No `COLUMN_CAP` state was published or inferred. Further arithmetic requires the planned exact 1,500,000-to-1,750,000 cap equivalence gate from round1342.

Independent all-column replay and exact cache-descendant scans are delegated to the separate referee. This producer report makes no terminal or conjecture claim before that referee seals.
