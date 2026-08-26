# Independent referee: held r1640 cap-exhaustion contract

Status: **PASS_PRELAUNCH_PROOF_CONTRACT_APPROVED_HELD**.

The altered proof contract is sound. On frozen source SHA `3139689f...`, `column_cap` has exactly six identifier occurrences and only two runtime configuration reads: result serialization and the whole-next-set capacity guard. The deterministic incident difference is sorted before that guard. Its failure branch writes the unchanged `columns`/`candidate`, leaves vector content unchanged, reports `COLUMN_CAP`, and returns before invariant-column arithmetic, ranking, elimination, backsolve, or verification. Raising the cap therefore admits the same already-enumerated whole set; it does not change its enumeration or arithmetic.

This is deliberately not lane byte equivalence. Acceptance after a run requires: normalized commands differing only in `--column-cap`; a cap-4.0m control that stops at r1639 with `COLUMN_CAP`, no r1640/tmp, and checkpoint/cache hashes equal to the audited input; then a fresh cap-4.25m candidate with exactly one r1640 `ROUND_CAP` record, a strict checkpoint descendant, all 3,968,369 inherited vector records byte-identical in order, target normalized to 1, and zero pairing against every final cached column. Candidate launch is forbidden if any control guard fails.

The design is bound externally to the sealed r1639 audit/replay/manifest `a99a307f...`/`4996c85d...`/`de3d1a5e...`, checkpoint `ab63c220...`, and cache `4d342801...`; its original PLAN retains intentional null independent-input fields. This referee approves the proof contract but does not authorize arithmetic. Manager clearance, binding this manifest, and the 88,080,384-KiB pre-lane storage gate remain mandatory. No r1641 or D12/conjecture claim follows.
