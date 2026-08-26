# K23 direct-K16 R3-4 shard0 reconciliation

Verdict: **ACCEPT** the existing `[0,12048547)` file as the complete output of the originally authorized shard0 traversal. It is not a stale or unrelated result.

The original command ran in exec session `15261`. Its completion was recovered from yielded cell `439`: exit code `0`, chunk `c35acf`, and complete stdout equal to the producer JSON fields, including interval `[0,12048547)`, elapsed `214.595321s`, and scaled charge `-361020309111179182080`. The source writes the same `text` bytes atomically and then prints that same value. The result and samples have the same `04:47:22+0530` birth/mtime and no `.tmp` remains.

The attempted stop did not reach the process. It waited on privilege escalation; after the producer had already exited, `kill -INT 80617` returned `no such process`. Thus it neither truncated nor altered the accepted files. The traversal did overlap the restarted direct23 job, but stayed within its own accepted wall/RSS gate and terminated normally before the 540-second alarm.

Pinned evidence:

- Producer source SHA-256: `9409c81ab504fed476c9715dfb25091c0e07f768b58508e6a675f43eaadc40dd`; source mtime `04:27:39+0530`.
- Exact run binary SHA-256: `3756d3c8cb8269f93339c992bf2ed80d831b48fd0125a0336f9875b10d11e08e`; binary mtime `04:29:14+0530`, before launch.
- Result SHA-256: `fd3660034107570102d2019ebacd8f9b1a125caed67a09577a3312bc155d1655`.
- Samples SHA-256: `bda8a13cabf9e4ecc8ae2766c57138326b80e784899841c62bc624a221e818be`.

Independent checks re-read checkpoint bytes for all 12,048,547 source records and reproduced signed coefficient `587336448` and L1 coefficient `6903021408`. Aggregate identities passed (`32*p1`, exact histogram count/weight, `60*p2`, full=irreducible). The independent literal evaluator replayed all 129 distributed samples from checkpoint bytes through the literal K3 then terminal K4 continuation, including frozen pivots, `U/(m1*m2)`, nonzero charge, and irreducibility.
