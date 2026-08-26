# Independent r1527→r1538 cap-2.75m chain audit

Status: **PASS_EXACT_FULLY_TELEMETERED_ROUND1538_CAP2750_CHAIN**.

Six accepted descendants cover every round from 1528 through 1538 exactly once. All six checkpoint ancestry checks and byte-identical inherited-cache scans passed. The endpoint has 2,476,308 columns, support 3,910, target coefficient 1, checkpoint SHA-256 `d436b820bdc1746d2c99a46e22fcc83dcd354836bce76223cb071fdb2aabf607`, and cache SHA-256 `c8527569930d927c9f4f2e1935635c8b9cb372444f6b8d6b991830d973d6f972`.

Independent replay checked all 2,476,308 columns and 253,095,370 terms, including 11,129 candidate-hit terms and two target terms, with zero failures. Replay SHA-256 is `7e571aa3dca04a1ca3300ce66b90c57eeba4a5df62df6fcdb9745824c66c4510`.

Resource/provenance guards pass: watchdog blocks total 259.032220 and 240.574562 seconds, each below 540 seconds, and peak RSS was 26,069,568 KiB below 36 GiB. Source, binary, watchdog, cap, mode, pivot, strategy, and stage commands match the frozen contract.

The authoritative chain audit is `results_round1538_chain_audit.json` (SHA-256 `ec7e14549b8d54112a0f502a22b1f908ebdd8566b97fe8e25fda20f313141159`). Round 1538 is exact and resumable; no r1539 or closure claim is made.
