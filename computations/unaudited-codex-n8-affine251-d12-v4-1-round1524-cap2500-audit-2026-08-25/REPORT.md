# Independent r1504→r1524 cap-2.5m chain audit

Status: **PASS_EXACT_FULLY_TELEMETERED_ROUND1524_CAP2500_CHAIN**.

The eight accepted descendants cover every round from 1505 through 1524 exactly once. Checkpoint order/preservation and cache byte preservation passed on all eight edges. The accepted endpoint has 2,379,326 columns, support 3,484, target coefficient 1, checkpoint SHA-256 `376f83253a3f901f7ae565d8ded6cb31c9758203ef9a7a91657cd3d3b65501a0`, and cache SHA-256 `6a3aa33a4706beac36fd4860ccf96e693e56b9cf9eab5a15c66198668821fc07`.

The independent final replay checked all 2,379,326 cached columns and 243,168,068 terms, including 9,949 candidate-hit terms and two target terms, with zero failures. Its SHA-256 is `58691230bb43b2ab186d718f28e245b65c0f336db70e03374da1c409e43a4c56`.

Resource/provenance guards pass. The accepted stages split into watchdog blocks of 423.732552 and 330.441382 seconds, each below 540 seconds; peak RSS was 26,063,072 KiB below 36 GiB. The first block pins the 90-second native watchdog and the second pins the authorized 120-second native watchdog; source, binary, mathematical mode, pivot, strategy, worker count, and cap are unchanged.

The failed original `stage03` is quarantined with no result and zero accepted coverage. The native-90 `stage05_cap1518` emitted no rounds and was independently confirmed byte-identical to its r1516 input; it is an identity diagnostic, not a continuation edge. The distinct recovery stages alone supply the missing rounds.

The authoritative chain audit is `results_round1524_chain_audit.json` (SHA-256 `bb477e89e63aafbceaca857f7132d0cbfebca007dd9b10906c97db2b74f6e0e9`). Round 1524 is an exact resumable state; this package does not claim round 1525, closure, or a terminal global dual.
