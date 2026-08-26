# Full K14/K4 scalar-parent profile census and K20 charge

## Verdict

**PASS, complete for the single `D14:222 | R:4-2` K20 path.**  The audited
exporter processed the full source range `[0,485)` in 16 atomic shards under
the 600 s / 16 GB gate.  The external signed merge and the occurrencewise K2
full/irreducible 77-charge evaluation both terminalized.  No rows were
collected and no K21 tails were generated.

This packet does not cover the K15/K3 or K16/K2 scalar-parent streams, and it
is not a complete K20 charge.

## Exact parent and merge census

- generated K18 parents: **397,156,800**
- K0-pivotable K18 parents: **357,580,800**
- outgoing K2 pivot uses: **910,713,600**
- atomic sorted parts: **490** in 16 complete source shards
- atomic nonzero records: **120,812,123**
- atomic retained record uses: **909,789,873**
- merged nonzero signed profiles: **18,217,226**
- cross-part exact-zero profiles: **1,150,525**
- merged retained uses: **886,145,203**
- signed merged weight at `U=400591699200`:
  **496,321,127,773,883,596,800**

The 357,580,800 pivotable parents compress by 19.63x and the 910,713,600
outgoing uses compress by 49.99x to the merged profile checkpoint.  The 490
parts plus merged file occupy about 13 GB; the merged file is 1.8 GB.

Every parent construction recomputed the valid 25-cover first-pivot set,
every outgoing pivot set and anchor signature, and asserted exact division by
both `m1` and `m2` at the universal scale.  The aggregate `(m1,m2)` histogram
contains exactly 357,580,800 parents and uses only products dividing `U`.

## K2 response charge

The merged key stores `profile29 | signature12 | outgoing pivot`, its signed
`i128` weight, use count, and a reversible literal witness.  Streaming the
18,217,226 keys required 218,606,712 literal K2 tail evaluations:

| quantity | scaled by U | reduced unscaled value |
|---|---:|---:|
| full `[4,2]` K20 charge | 84,209,668,521,245,245,440 | 13,561,905,490,048 / 64,515 |
| irreducible `[4,2]` K20 charge | 81,163,935,546,464,010,240 | 91,499,746,963,456 / 451,605 |

The evaluator replayed 17,806 distributed literal witnesses against the
stored profile/signature/pivot and checked every stored signature and outgoing
pivot.  Exact-zero signed profiles are omitted, so retained occurrence counts
are not a census of cancelling literal occurrences; the full and irreducible
linear charges are unaffected.

## Runtime and replay

- 16-shard export: approximately 38 s wall (maximum shard kernel 21.12 s)
- 490-way external merge: 124.47 s
- K2 charge stream: 9.29 s
- independent full hash/header/merged-order replay: approximately 34 s

The independent replay checks source-shard coverage, all 490 part headers,
sizes and SHA-256 hashes, exact parent/use/weight totals, merged strict key
order and nonzero weights, the full merged sums, response count, and a hostile
one-weight mutation.

## Artifacts and hashes

- Original audited exporter source:
  `../unaudited-codex-orbit0-k18-three-stream-exporters-2026-08-23/export_k18_parent_profiles.rs`
  — SHA `adb7edbec6fb251ad55cc688183e3344f45fa45e5486c925e5edbbb0d9f0ebe9`
- shard launcher: `run_export_shards.sh`
  — SHA `8b25cfc88f4df05e27385989466decb7981ed009938d02ceb4604e3f6ee42a87`
- merger: `merge_k14_profiles.rs`
  — SHA `fc5d66d90e5f2779b7a886654631aa33d65aeb51438ecbdc32551d8451393071`
- merged checkpoint: `k14_k4_enriched_profiles.bin`
  — SHA `5cc8c15b2333937ddfaefac1ec056b2f2fd899f5b89ea5b0276d374b05d92d7f`
- merge result: `results_k14_k4_profile_merge.json`
  — SHA `ae8224a7345b763cc8cf2c5ebd6c4c606a9cbe7b19a4653a73ad89e6b28a9278`
- evaluator: `evaluate_k14_k4_k2_charge.rs`
  — SHA `d978c084141c15efbea317879c7b82552d344b407e5973144780b324d47fba3f`
- charge result: `results_k14_k4_k2_charge.json`
  — SHA `0aec524a3b104965d97ed1f18e27d07355f58180c7751e9cda4db78488b67f31`
- independent audit: `audit_k14_k4_full_profiles.py`
  — SHA `8e59158e8aeac74c89a24041a2f0b6e557aec917b87f41b4821f6572086935ed`
- replay result with all 490 part hashes: `results_k14_k4_full_replay.json`
  — SHA `8c3c0a602e469522d8a2cae39440f7b9532d1ac01fbd967b7ff91cbf0670238a`
