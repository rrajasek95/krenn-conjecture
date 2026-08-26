# Independent r1524→r1526 cap-2.5m audit

Status: **PASS_EXACT_FULLY_TELEMETERED_ROUND1526_CAP2500_CHAIN**.

The sole accepted edge covers rounds 1525–1526 exactly. It preserves all 2,379,326 inherited checkpoint columns and cached vectors byte-identically and adds 14,276 records. The endpoint has 2,393,602 columns, support 3,341, target coefficient 1, checkpoint SHA-256 `9697ab86d0bad92922927ed0357b1620e0a6d013cd729e9041b948534d31e10f`, and cache SHA-256 `406747a3f4cb832d29532e0d21995ef0f976dd53ff5e9a7a899785bf8a564896`.

Independent replay checked 2,393,602 columns and 244,630,536 terms with zero failures. The replay SHA-256 is `33399bebd372e038d3aeb73caccd63cc65af6d4ce80e804d4ebcbd55c7a7fe3d`.

The frozen cap guard stopped fail-closed before stage 2: headroom 106,398 was 672 below the required 107,070. No r1527 production was launched. Round 1526 is exact and resumable only under separately audited higher-cap authority.
