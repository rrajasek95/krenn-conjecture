# Full hidden-K16 orbit-aware K2 collection

## Gate verdict

After the complete pre-merge state passed independent review, the authorized
291-way signed merge completed in 49.4 seconds.  Atomic H18PIV2 and H18IRR2
checkpoints are present and locally replayed.  All 291 input chunks remain
retained for the independent final referee.  This is a completed K18 `[2,2]`
collection, not a K20 result; cleanup and the K20 consumer have not run.

## Exact completed state

- 31 parent runs cover all 75,691,040 hidden K16 parent occurrences.
- All 511,477,120 labelled second-pivot uses were aggregated into 126,544,084
  per-run exact decorated-pair records.
- Global exact-key merge had 126,420,124 keys and 52 exact zeros.
- H-canonical external merge produced 101,545,723 nonzero decorated pair
  orbits and 305 further exact-zero orbit keys.
- The pair coefficient sum is `146230609431055564800` at scale
  `U=400591699200`.
- The exact decorated-pair stabilizer histogram is
  `{1: 99314228, 2: 2212958, 4: 16210, 8: 2099, 16: 224, 32: 4}`;
  every record satisfies `orbit_size*stabilizer=384`.
- All 291 parallel child chunks cover the exact interval
  `[0,101545723)` once, generate exactly `1,218,548,676 = 12*101,545,723`
  K2 tails, and contain 516,225,702 within-chunk nonzero rows.
- Chunk coefficient sums equal
  `1754767313172666777600 = 12*146230609431055564800` exactly.
- Final merge produced 158,439,965 pivotable rows of mass
  `724159651336720220160` and 110,465,931 irreducible rows of mass
  `1030607661835946557440`.
- Exactly 3,346 cross-chunk row groups cancelled to zero.
- H18PIV2 SHA-256 is
  `442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8`;
  H18IRR2 SHA-256 is
  `c60fd9763d604f27213542a3bec9376849e046be06edf4e68035c849b097e111`.

The complete parent ledger is
`hidden_k16_decorated_pair_orbits_full.bin` (53-byte records).  Child chunks
are `pchild_chunk_0000.bin` through `pchild_chunk_0290.bin` (80-byte records).
Each child record is

```
row[0:24], weight_i128[24:40], witness_pair_row[40:64],
p2[64], tail2[65], pair_uses_u64[66:74], orbit_u16[74:76],
stabilizer_u16[76:78], pivotable[78], m2[79].
```

This provenance is sufficient for a later `[2,2,2]` consumer: its next
denominator `m3` must be recomputed from the available pivots of `row`; `m2`
is retained only as the preceding-page witness denominator.  No K20 tails
were generated here.

## Replay

`audit_full_k2_premerge.py` checks all headers, file sizes, ordered interval
coverage, raw child count, and coefficient conservation.  Its logical digest
is `621e779367b28145a64b6878e7d8963afd5e3b16171982c72773a8cfbb5ec2a4`.
`audit_full_pair_stabilizers.rs` separately streams the complete pair ledger,
checks strict key order, weight sum, and `orbit_size*stabilizer=384`.

The large child chunks have no stored content digests.  Resume validation is
therefore exact for magic, scale, schema, interval, declared/raw counts, and
byte size, while pre-merge child content provenance was the atomic generator
plus these guards.  The final merge has now streamed every child record, and
`audit_final_k18_checkpoints.rs` independently streams both final checkpoints,
checking strict order, flags, masses, provenance fields, and EOF.  The pair
ledger was also fully streamed and replayed.  `results_resume_safety.json`
records the hostile truncation and empty-histogram guards.

The merge retains all 291 `pchild` chunks.  Cleanup is a separate
`--cleanup-refereed-child-chunks` command and is refused unless both final
checkpoints validate and `independent_k18_referee_pass.json` carries the
expected independent PASS status plus both checkpoint hash fields.  The
hostile eager-cleanup test failed as required and left all 291 chunks present.

`run_full_hidden_k16_k2_orbits.rs` is patched for resumable continuation: it
validates and skips all frozen pair/child chunks, then enters only the final
merge.  The caught pre-merge bug was an 8-byte magic compared against a
7-byte literal; it is corrected to `H18CHC1\0`.  No row arithmetic had begun
when that assertion fired.

The atomic final result is `results_full_hidden_k16_k2_orbits.json`, logical
digest `08bd41bff78bb8be4351f46abfda3bb764ee517f8f6186f0a5a09f48849a6e6c`.
`CHECKPOINTS.sha256` freezes both large-file hashes.  Independent final
acceptance is still required before the guarded cleanup command may remove
the 291 chunks.
