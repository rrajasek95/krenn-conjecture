# Independent referee: K15/K3 stage 1 `[0,242)`

## Verdict

**PASS.**  Stage 1 is complete, disjoint, source-faithful, and within its
resource gate.  This verdict covers only the 242 atomic K15/K3 source shards
for records `[0,242)`.  No stage 2, external merge, charge calculation, or
K16 work was launched by the referee.

## Independent checks

The independent catalog/header/hash replay establishes:

- exactly one accepted attempt, manifest, and part for each source record
  `0..241`, in order and with no gap or overlap;
- exactly 484 files in `stage1_shards`, all referenced by the catalog; no
  orphan, reused, rejected, or retry attempt;
- every manifest SHA and all 242 part SHA-256 values match the atomic catalog;
- every part has `K18PRF2`, version 2, component 2, response degree 2,
  104-byte records, scale `U=400591699200`, and part index zero;
- all 112,628,530 records across every part are in strict 42-byte key order,
  with nonzero signed weight and positive use count;
- each part header count/use/weight agrees with its complete one-record
  manifest, and each `(m1,m2)` product divides `U`;
- every per-source manifest has 3,690,496 generated parents, 1,903,616
  pivotable parents, and 4,861,952 outgoing uses.

The resulting exact totals are:

| quantity | value |
|---|---:|
| generated parents | 893,100,032 |
| pivotable parents | 460,675,072 |
| outgoing pivot uses | 1,176,592,384 |
| locally unique records | 112,628,530 |
| signed scaled weight | -318,525,115,738,462,617,600 |
| part bytes | 11,713,390,352 |

The catalog SHA is
`e9dbee8ac2c9e80db4fa8a7cae86795927bc5d7c9f509d116c3a075f488f1537`;
the ordered set of 242 part hashes has digest
`9af24e8d8364a307305582474b97483f6cdebde9a4d204681f5249ae89d1a241`.

## Source/profile semantics

The producer's runner applied the pinned exact verifier to every part before
catalog acceptance.  Independent byte hashing confirms those are exactly the
same files.  The referee additionally reran the pinned verifier on 16
distributed source shards (7,243,738 records), including endpoints 0 and 241.
It reversed the stored first tail to the literal K15 source head and
recomputed both pivot sets, denominator divisibility, signature, profile key,
ordering, use sum, and signed weight; all passed.

This distributed replay invokes the pinned verifier binary rather than a
second independently implemented physical-profile decoder.  The independent
catalog/header/order code is separate, and the exporter/verifier source and
binary hashes are pinned respectively as `1f92b6ef...` and `062a16c0...`.

## Resource scope

The run completed in 237.320503 seconds under the 600-second gate, with two
workers and no retries.  Free space changed from 245,437,206,528 to
233,701,359,616 bytes.  Direct RSS was unavailable under sandboxed process
inspection; the fixed one-million-key cap gives the recorded analytic core
bound of about 0.35 GB per worker.  Thus timing and disk are measured, while
the memory conclusion is an analytic bound, not an RSS measurement.

## Replay artifacts

- `audit_stage1_referee.py`
- `results_stage1_independent_referee.json`
- `audit_stage1_record_order.rs`
- `results_stage1_record_order.json`
- `results_stage1_literal_semantics_sample.json`
