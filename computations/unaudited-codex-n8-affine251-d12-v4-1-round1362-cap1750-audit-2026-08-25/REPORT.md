# Independent D12 round1343→1362 cap1750 audit

Status: `PASS_EXACT_FULLY_TELEMETERED_ROUND1362_CAP1750_CHAIN`.

The sealed round1343 cap1750 input is pinned by manifest `c07168d65ba9caa604bf38235b4ff9f5442b217fd82934c84f18f4f0c9665e9b`, checkpoint `d2dbdee814cecca8f8528d84d2f386d3f042a54b62039a0350a834b5a1949dcf`, and cache `d5517dfdc00cb7c2e0844b2459385576dd84211eceebe3a0cb94815a1cd7a2c6`.

Three stages cover exactly rounds 1344 through 1362 with no gaps. Every checkpoint is a strict descendant of its predecessor and every inherited cache record is byte-identical. The state grows from 1,496,171 to 1,582,672 columns. The final candidate has support 2,043 and target coefficient 1. Independent replay checked all 1,582,672 cached columns / 161,563,157 terms with zero pairing failures.

Aggregate watchdog time is 294.746940 s, below 540 s. Maximum sampled RSS was 21,280,560 KiB, below 37,748,736 KiB. All watchdogs report PASS/no breach/atomic clean with frozen pins. Stage 1 wrapper finalization ended 0.386994 s after its last successful RSS sample; this is below two 0.25-second poll intervals and occurred after natural child exit, while stages 2–3 were within one-plus poll interval.

Authoritative endpoint artifacts:

- result: `d2d460d535a9aeb9a6ac0632849c8e507b242e3046be9f199ba1cf52e0f2ebab`
- checkpoint: `ddf8873518c4cef1551daacf1ce82ba67a54ecee9fab6f85af6154964c06112a`
- cache: `25f42b9b56010684e6f79f648c69ace5a9b09e06756dbe114af5ce9474020f85`
- watchdog: `8ef3d6b1b1a1ac3278de37fddc9463ac5a8fbf067fb5a181537e85cee4be04eb`

Scope caveat: round1362 ended at `INCOMPLETE_SEARCH_CAP / ROUND_CAP`. This is an exact resumable state, not a terminal global dual.
