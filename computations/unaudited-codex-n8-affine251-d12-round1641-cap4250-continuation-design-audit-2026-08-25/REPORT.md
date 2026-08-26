# Independent r1641 held-design audit

Status: **APPROVE_HELD_ONE_ROUND_WITH_SUPPORT_CAP_DIAGNOSTIC_CAVEAT**.

The r1640 pins match the independently sealed attempt2 state. Column headroom is exactly 180,289; `ceil(101342*5/4)=126678`, so the one-round projection leaves 53,611 columns, while the same two-round projection exceeds the cap. The frozen round cap is 1641 and r1642 is forbidden. Source, binary, watchdog, fresh-clone, 240-second hard wall, 36-GiB RSS, storage-floor, atomic output, strict descendant, inherited-byte, and full-replay requirements are pinned.

The support cap has only 23,384 entries of headroom and was not projected. If it fires, it does so after new columns/vectors are materialized but before candidate and round commit. That output is a hybrid zero-r1641 diagnostic clone, not byte-unchanged like a `COLUMN_CAP` control; it must be quarantined, independently failure-sealed, and never resumed or promoted.

No large endpoint read, clone, or arithmetic launch was performed.
