# Independent referee: K15/K3 stage 2 `[242,485)`

## Verdict

**PASS.** Stage 2 is complete, disjoint, source-faithful, and within its
resource gate.  This verdict covers only the 243 atomic K15/K3 source shards
for records `[242,485)`.  The referee launched no merge, charge calculation,
K16 work, or producer run.

## Independent replay

- Source coverage is exactly `242..484`, in order, with one manifest and one
  part per source record and no gap, overlap, reuse, retry, reject, or orphan.
- Every one of the 243 manifest hashes and 243 part hashes matches the
  catalog.  The shard directory contains exactly those 486 referenced files.
- Every part has `K18PRF2`, version 2, component 2, response degree 2,
  104-byte records, scale `U=400591699200`, and part index zero.
- All 89,716,017 records were independently streamed: keys are strict-sorted,
  signed weights are nonzero, uses are positive, and every part's record/use/
  weight totals equal its header and one-record manifest.
- Every manifest has 3,690,496 generated parents, 1,903,616 pivotable
  parents, and 4,861,952 outgoing uses.  Its denominator histogram sums to
  the pivotable-parent count and each `m1*m2` divides `U`.

Exact totals reproduced:

| quantity | value |
|---|---:|
| generated parents | 896,790,528 |
| pivotable parents | 462,578,688 |
| outgoing pivot uses | 1,181,454,336 |
| locally unique records | 89,716,017 |
| signed scaled weight | 2,183,623,986,207,050,956,800 |
| part bytes | 9,330,489,096 |

The catalog SHA is
`855df701663cc08313c44b924ca7dc80c13e04dee45b6adfe93a1c8c59e70a9f`;
the ordered set of part hashes has digest
`8920ede16d69a56b493c965591e2e8cf8d4e26e375eed788a2f61edeab56d756`.

## Physical/profile semantics

The producing runner applied the pinned exact source verifier to all 243
parts before accepting them, and the independent hashes confirm the same
bytes.  The referee additionally reran that verifier on 16 distributed shards
including both endpoints, covering 5,776,739 records.  It reversed each
stored first tail to the literal K15 source head and recomputed both pivot
sets, denominator divisibility, signature, profile, ordering, uses, and
signed weight; all passed.

This distributed semantic replay uses the pinned verifier binary rather than
a second physical-profile implementation.  The independent catalog/header/
order audit is separate; source and binary hashes remain `1f92b6ef...` and
`062a16c0...`.

## Resource scope

Measured wall time was 224.389626 seconds under the 600-second gate.  Free
space changed from 233,690,304,512 to 224,351,789,056 bytes.  Direct RSS was
unavailable under sandboxed inspection; the fixed one-million-key layout has
the recorded analytic bound of about 0.35 GB per worker for two workers.

Replay files: `audit_stage2_referee.py`,
`results_stage2_independent_referee.json`, `audit_stage2_record_order.rs`,
`results_stage2_record_order.json`, and
`results_stage2_literal_semantics_sample.json`.
