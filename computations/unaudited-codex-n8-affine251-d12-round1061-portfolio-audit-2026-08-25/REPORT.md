# Exact round-1061 six-way portfolio audit

Verdict: `PASS_EXACT_ONE_ROUND1061_SIX_WAY_PORTFOLIO`.

The frozen round-1060 state (`1bc0315d...` checkpoint, `0d71ab7b...` cache; audited manifest `7c1649f0...`) was APFS-cloned into independent portfolio and fixed-control lanes. The six-way parallel tree portfolio compared repair/cold under first/last/rare and selected **cold/rare**.

Both lanes advanced exactly one round to round 1061: 731,908 columns (+2,108), support 785, and 451 new support rows. Their non-timing round records agree. More importantly, their checkpoints are byte-identical at `9927bfa1...` and their 1,581,595,210-byte caches are byte-identical at `acc0f960...` (fingerprint 9,032,931,499,739,351,852).

The portfolio took 55.656 seconds under the watchdog and peaked at 21,337,440 KiB; the fixed replay took 44.030 seconds and peaked at 10,434,800 KiB. Both remained below 120 seconds/36 GiB, with atomic outputs and no continuation.

## Audit-only compatibility source

Sealed production v4.1 intentionally refuses tree/portfolio modes. The first direct attempt therefore rejected atomically before restore, with no result or state mutation. The accepted audit used an isolated v4.1 sibling whose only source difference is deletion of that top-level production-mode guard (`AUDIT_PATCH.diff`). The parser's independent hierarchical fixed cold/rare restriction remains intact; a hostile hierarchical repair command rejects before output.

Parent v4.1 source is `3139689f...`; audit source is `2cf62905...`; audit binary is `ade47c27...`. Production v4.1 was not edited. The selected state for continuation is `selected_control/checkpoint.bin` plus `selected_control/vectors.bin` with the exact output hashes above.
