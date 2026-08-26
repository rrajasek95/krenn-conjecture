# K15/K3 stage 1 terminal report

`PASS`. Only source records `[0,242)` were exported. Two workers with a
one-million-key cap completed 242 atomic one-record shards in 237.320503
seconds, below the 600-second gate. No stage 2, global merge, charge
evaluation, or K16 work ran.

Every shard has one complete manifest and one locally sorted K18PRF2 part.
The runner replayed the literal source head, first tail, both pivot sets,
denominator divisibility, signature, profile key, ordering, local counts, and
signed sum for every part, then stored SHA-256 for each part and manifest in
the atomic catalog. There were no retries, rejected artifacts, orphan parts,
or reused attempts.

Exact totals:

- generated parents: `893,100,032`;
- pivotable parents: `460,675,072`;
- outgoing pivot uses: `1,176,592,384`;
- locally unique nonzero profile records: `112,628,530`;
- signed scaled weight: `-318,525,115,738,462,617,600`;
- parts: `242`;
- part bytes: `11,713,390,352`;
- free space: `245,437,206,528` bytes before and `233,701,359,616` after.

The authoritative catalog is `stage1_catalog.json`, SHA-256
`e9dbee8ac2c9e80db4fa8a7cae86795927bc5d7c9f509d116c3a075f488f1537`.
Exporter source SHA-256 is
`1f92b6ef1e27efa6386f57bf07dd85b032621e2f88b158a3e1c0144b1725a094`;
the exact optimized binary used had SHA-256
`062a16c00d5af2e075874ccc55341b3778f3fdbd129c7cbc28c712c6c1738294`.

Direct process RSS was unavailable because sandboxed process inspection was
denied. The fixed two-worker layout bound from the prelaunch audit is about
0.35 GB of core hash/sort storage per worker, safely below the 16 GB gate;
this is stated as an analytic bound, not a measured RSS value.
