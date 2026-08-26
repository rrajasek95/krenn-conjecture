# Independent r1538→r1550 cap-2.75m chain audit

Status: **PASS_EXACT_FULLY_TELEMETERED_ROUND1550_CAP2750_CHAIN**.

Six accepted descendants cover every round from 1539 through 1550 exactly once. All checkpoint ancestry checks and byte-identical inherited-cache scans passed. The endpoint has 2,575,033 columns, support 4,084, target coefficient 1, checkpoint SHA-256 `1c3e84f5cd97a44886b99d17f6f1a178d3cb5802c2254a95ad90f78dee9c10e3`, and cache SHA-256 `1ee5934a99dc70a15ecd651fec7ec1886891026bddf338c3f1b7430d066bdc12`.

Independent replay checked all 2,575,033 columns and 263,191,303 terms, including 11,470 candidate-hit terms and two target terms, with zero failures. Replay SHA-256 is `632f02be3980136464d1285edec9bf83777cd06e1ef439153d46bdd4c2593a4d`.

Resource/provenance guards pass: watchdog blocks total 259.463647 and 264.024950 seconds, each below 540 seconds, and peak RSS was 26,375,648 KiB below 36 GiB. Source, binary, watchdog, cap, mode, pivot, strategy, and stage commands match the frozen contract.

The authoritative chain audit is `results_round1550_chain_audit.json` (SHA-256 `6f29cd96d8083fe5ace24c1937fbf8daa5eed34b9009168f3016edd59347a1f0`). Round 1550 is exact and resumable; no r1551 or closure claim is made.
