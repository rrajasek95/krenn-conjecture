# Complete K23 hidden-collected singleton fold

Status: `PASS_COMPLETE_K23_HIDDEN_COLLECTED_SINGLETON_PACKAGE_AUDIT` for exactly `D14:222|R:2-2-2-3`.

The sealed H18PIV2 source was scanned in the exact atomic intervals `[0,52813321)`, `[52813321,105626643)`, and `[105626643,158439965)`, completing in 102.527828, 93.337264, and 96.412977 seconds. All were below the 540-second launch gate and 600-second hard stop. Their manifests replay, and the original prefix package remains unchanged and replayable.

The exact no-gap merge contains 158,439,965 source records, 399,275,484 selected K18 p3 uses, 570,281,318 pivotable K20 children/selected p4 uses, and 18,249,002,176 terminal K3 occurrences. The strict scalar is:

```text
U * charge  = -1992801869625330597888
charge      = -288310455674961024/57955975
full        = irreducible
```

Every occurrence uses the source-faithful sign `w -> -w/m3 -> +w/(m3*m4)` with exact `U` and coefficient divisions; retained K20 children have unique p4. Every K23 child has anchor-signature mass 1 and is terminal.

The independent merge checker rehashed the complete 12.675 GB source to `442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8`, validated every shard/result/sample hash, and seek-replayed 771 literal source records. A separate cache-free Rust referee rebuilt the entire literal recurrence for those 771 records, checking 2,894 pivotable K20 continuations and all 92,608 terminal K23 children; its sampled scaled charge agrees exactly with the merge checker.

`k23_hidden_collected_singleton_fragment_manifest.json` is the strict singleton assembler fragment. The frozen 59-ID assembler accepts its evidence and reports exactly 1 covered / 58 missing IDs, no duplicates or extras, and no complete-K23 claim.

The machine-readable audit has logical SHA-256 `b7c8da401a07bc23c1834db94228657df982e6506b6d1809dcf4ea76bb43f07b`. No rows, K24 work, membership test, or conjecture verdict is included.
