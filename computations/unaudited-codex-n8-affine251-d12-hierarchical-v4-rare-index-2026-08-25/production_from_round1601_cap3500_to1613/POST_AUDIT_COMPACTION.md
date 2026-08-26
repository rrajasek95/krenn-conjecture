# Post-audit compaction at round 1613

Status: PASS

This operation is authorized only after the independent eleven-edge audit sealed PASS. It removes the superseded large checkpoint/cache payloads below and retains every result, watchdog, log, plan, ledger, report, manifest, the accepted round1613 endpoint, and all independent audit evidence.

Independent seal pins:

- chain audit: `e8bd3caac9c4d6fe7d1a88e9b8b087ae4810a1858f6d32b2ef1fda26fb62d9cc`
- final replay: `ba80a02d3e94c2eec1414ea94c23e081e7371ecea2356d5251125ed017e04200`
- audit manifest: `55c6506523d207796a658bbde398ca18ec52d60471c1ebc8dd985dc219a412a0`
- replay census: 3,301,528 columns / 336,998,519 terms / target 1 / zero failures

Pre-execution free space: 64,993,056 KiB.

Exact deleted paths (22 files):

- `stage01_cap1603/checkpoint.bin`
- `stage01_cap1603/vectors.bin`
- `stage02_cap1604/checkpoint.bin`
- `stage02_cap1604/vectors.bin`
- `stage03_cap1605/checkpoint.bin`
- `stage03_cap1605/vectors.bin`
- `stage04_cap1606/checkpoint.bin`
- `stage04_cap1606/vectors.bin`
- `stage05_cap1607/checkpoint.bin`
- `stage05_cap1607/vectors.bin`
- `stage06_cap1608/checkpoint.bin`
- `stage06_cap1608/vectors.bin`
- `stage07_cap1609/checkpoint.bin`
- `stage07_cap1609/vectors.bin`
- `stage08_cap1610/checkpoint.bin`
- `stage08_cap1610/vectors.bin`
- `stage09_cap1611/checkpoint.bin`
- `stage09_cap1611/vectors.bin`
- `stage10_cap1612/checkpoint.bin`
- `stage10_cap1612/vectors.bin`
- `../../unaudited-codex-n8-affine251-d12-round1601-direct-cap3500-gate-2026-08-25/candidate_cap3500/checkpoint.bin`
- `../../unaudited-codex-n8-affine251-d12-round1601-direct-cap3500-gate-2026-08-25/candidate_cap3500/vectors.bin`

The deleted stage hashes remain pinned by `MANIFEST.sha256`; the superseded input hashes are checkpoint `83955dbcc460c5fe39623e25b8337eb80bcfc9921eeafb4c1a887cfa6f5abb01` and cache `c9d850754e9451015a3bf4fa6b51d6f0bb8c3ecdaeecbdef456abaa5fae7b046`.

Retained endpoint expected hashes:

- checkpoint: `4bd2b4d8f854e1cedc147f9824b876d3c7d4715e42bbde0cf0112a1bd666b2ac`
- cache: `3defad7e9dba3495e1ecdb0f40f0148b1dbe0d79a6f34452db205dcd6a88ec16`

Post-execution verification:

- all 22 enumerated paths are absent;
- free space is 139,983,844 KiB;
- retained checkpoint rehash is `4bd2b4d8f854e1cedc147f9824b876d3c7d4715e42bbde0cf0112a1bd666b2ac`;
- retained cache rehash is `3defad7e9dba3495e1ecdb0f40f0148b1dbe0d79a6f34452db205dcd6a88ec16`.

The independently accepted round1613 state is therefore unchanged and remains the sole restart point.
