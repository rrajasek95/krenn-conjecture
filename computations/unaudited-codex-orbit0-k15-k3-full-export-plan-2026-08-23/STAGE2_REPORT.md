# K15/K3 stage 2 terminal report

`PASS`. After the independent stage-1 referee passed with logical digest
`256bc673…`, only source records `[242,485)` were exported. Two workers with a
one-million-key cap completed all 243 atomic one-record shards in 224.389626
seconds, below the 600-second gate. No global merge, charge evaluation, K16
work, or modification of stage 1 ran.

Every shard has one complete manifest and one locally sorted K18PRF2 part.
The exact verifier replayed the literal source head, first tail, both pivot
sets, denominator divisibility, signature, profile key, ordering, local counts,
and signed sum for every part; the atomic catalog stores SHA-256 for every part
and manifest. There were no retries, rejected artifacts, orphan parts, or
reused attempts.

Exact totals:

- generated parents: `896,790,528`;
- pivotable parents: `462,578,688`;
- outgoing pivot uses: `1,181,454,336`;
- locally unique nonzero profile records: `89,716,017`;
- signed scaled weight: `2,183,623,986,207,050,956,800`;
- parts: `243`;
- part bytes: `9,330,489,096`;
- free space: `233,690,304,512` bytes before and `224,351,789,056` after.

The authoritative catalog is `stage2_catalog.json`, SHA-256
`855df701663cc08313c44b924ca7dc80c13e04dee45b6adfe93a1c8c59e70a9f`.
Exporter source SHA-256 is
`1f92b6ef1e27efa6386f57bf07dd85b032621e2f88b158a3e1c0144b1725a094`;
the optimized binary SHA-256 is
`062a16c00d5af2e075874ccc55341b3778f3fdbd129c7cbc28c712c6c1738294`.

Direct process RSS remained unavailable because sandboxed process inspection
was denied. The prelaunch analytic core bound is about 0.35 GB per worker;
this is not presented as a measured RSS value.
