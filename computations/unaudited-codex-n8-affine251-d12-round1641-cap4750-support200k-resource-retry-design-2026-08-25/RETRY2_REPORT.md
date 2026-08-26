# D12 r1641 cap4.75/support200k retry2 — rejected at hard wall

Status: **REJECT_HARD_WALL_ZERO_COVERAGE**.

The independently approved resource-only retry2 used the exact frozen source, binary, provider, caps, mode, and audited r1640 input. Its only resource changes from attempt1 were native wall 300 seconds and wrapper wall 360 seconds. The wrapper terminated the process at 362.269854 seconds after its last successful sample at 360.091925 seconds. Peak RSS was 16,288,288KiB, below the 36GiB limit.

No `result.json`, `dual.tsv`, or temporary output exists. Both stdout and stderr are empty. The cloned checkpoint and vector cache rehash exactly to audited r1640 (`12f79c86...` / `1d7ce92a...`), so retry2 contributes zero accepted rounds; neither r1641 nor r1642 exists.

This attempt is evidence only and must not be resumed or reused. No relaunch or continuation was performed in this turn.
