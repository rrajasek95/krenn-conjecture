# Independent D12 round-1601 to round-1603 edge audit

Status: `PASS_EXACT_EDGE_HARD_RESOURCE_PASS_COOPERATIVE_NATIVE_OVERSHOOT`.

The input round-1601 checkpoint/cache are pinned at `83955dbc...` / `c9d85075...`.  The accepted output is round 1603 with 3,133,635 columns and support 5,517, checkpoint SHA-256 `0979e0a2b7c53425394d846062d5a9a78aca519eb656f625ccc1d72698e36c63` and cache SHA-256 `9148e9105eae5a63623f0b37eb0972e1f0d0af70d324d18234b8fd8374eb628b`.

An independent streaming parser verified both checkpoint headers/canonical order/target normalization and exact cache descent: all 3,104,755 parent records and 6,658,666,350 inherited payload bytes are byte-identical in the child; the child adds exactly 28,880 records.  No final candidate-pairing replay was performed in this bounded gate.

Native elapsed 126.429282 s exceeds the cooperative 120 s signal.  This is not classified as a hard resource failure: the sealed source checks `Gate::check` only at loop top, then the completed-round `ROUND_CAP` branch writes checkpoint/cache/result without a second native timer check.  The authoritative hard watchdog passes at 128.306338 s under its 150 s limit, return code zero, no breach, atomic outputs clean, and peak RSS 22,083,840 KiB below 36 GiB.  The amended one-round remaining-stage plan is pinned at SHA-256 `540956f1...`.
