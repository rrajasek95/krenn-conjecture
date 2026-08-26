# Independent D12 v4 rare-order audit

Verdict: `PASS_PROMOTE_EXACT_V4_RARE_INDEX_WARM10` for the separately frozen, production-representative round-950 to round-960 gate.

The v4 index is persistent only within a running process. It is deliberately not serialized: every resume rebuilds it from the authoritative vector cache, leaving the v3 checkpoint and cache schemas unchanged. Static review pins source `c83c6801...`, binary `191eb088...`, and index schema `abc718ee...`; it verifies checked `u32` frequencies, per-hit map/index equality, strict folded bucket deltas, census guards, 16 lookup-only FNV shards, natural source-order append, and hard rejection of unsupported modes. The five hostile mode cases all rejected.

Attempt 3's independent rebuild reproduced its round-951 checkpoint and cache byte-for-byte (`9ba56042...` and `00944b20...`). The external read-only order gate then compared the accumulated round-960 index against a fresh canonical `(frequency, Mono)` sort: all 32,480,668 ranked rows agreed, with identical order SHA-256 `e87d2920...`.

The predeclared matched warm gate used byte-identical round-950 clones and exactly ten uninterrupted rounds, 951 through 960. V3 and v4 produced byte-identical final checkpoint `2e7b7a56...` and cache `76e93752...`, with the same 576,401 columns and 540-term candidate. Independent replay streamed all 58,615,777 cached terms, checked target normalization, and found zero failing columns.

Performance passes both frozen thresholds: v4 native elapsed was 48.399962 s versus v3's 54.648754 s, an improvement of 6.248792 s (11.4345%). Aggregate order work improved from 15.466606 s of v3 sorting to 3.068920 s of v4 commit plus flatten, a 5.0398x speedup. Both watchdog-v2 records passed with no breach, clean atomic outputs, and peaks below 36 GiB (v3 8,800,512 KiB; v4 10,722,704 KiB).

The earlier one-round attempt 3 remains `REJECT_PERFORMANCE`; warm promotion does not reclassify it. Attempts 1 and 2 are also preserved as performance rejections. Promotion is justified specifically by the frozen ten-round amortization gate, matching the roughly twenty-round production staging pattern.
