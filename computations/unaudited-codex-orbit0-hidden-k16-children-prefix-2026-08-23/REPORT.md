# Hidden K16 child recovery: measured one-slice prefix

## Terminal result

`PASS_MEASURED_CHILD_PREFIX` under the 120-second / 8-GB gate.  This is one
frozen H slice (156,064 of 75,691,040 parent occurrences), not a full child
evaluation.

The shared parent pass sees 1,054,592 second-pivot uses and compresses them to
62,678 labelled path/signature/pivot cache keys (16.826x).  Keys with aggregate
weight zero are intentionally retained for exact occurrence counts; this is a
cache-key count, not the full file's 6,229,700 nonzero-profile count.

## K2 -> K18 path `[2,2]`

The 12 K2 tails give 12,655,104 raw children, of which 6,122,752 are already
irreducible by the next pivot test.  Exact literal collection followed by H
canonicalization gives 694,172 nonzero canonical rows (18.231x raw/support
compression): 408,972 pivotable and 285,200 irreducible.  There are no exact
zeros in this prefix after canonical collection.  The scaled weight is
`-28885058653048012800`, exactly 12 times the incoming profile weight.

`k18_k2_canonical_prefix.bin` is 52,757,136 bytes (SHA-256
`64bbc2b4820a1eb0a9650dbd2e38a74c531906b181d1b3b48b221fcc30a4d9a5`).
Each 76-byte row retains the canonical row/weight/pivotability plus the parent,
second pivot, tail index, pivot count, and raw child row.  The raw witness is
required: an untransported pivot label alone would not be provenance-safe after
H canonicalization.

## K3/K4 cycle charges

The profile response is a source-faithful factor: the four residual paths plus
closed cycles and the selected tail reconstruct the literal 24-port cycle
partition.  All 62,678 keys and all 92 K3/K4 tails were compared to literal
rows: 5,766,376 exact abstract/literal cycle checks pass.

The replayable sorted profile ledger is `hidden_child_profiles_prefix.bin`:
5,641,084 bytes, SHA-256
`c6b2579c6dac804620859fa5788978248ec2dca9f6c5936a0f57312b758b28d3`.
Each 90-byte record stores `profile29, signature12, p2, weight:i128,
uses:u64, witness_row24`, so the charges and all literal guards can be replayed
without reconstructing the parent collection.

- `[2,3]` K19: 33,746,944 full / 23,070,720 irreducible occurrences; scaled
  charges `-4310060400861511680` / `-3762784545831124992`.
- `[2,4]` K20: 63,275,520 full / 53,606,400 irreducible occurrences; scaled
  charges `460536785434312704` / `440759609843318784`.

The common sign is `w2=-w1/m2`, and all divisibility/count guards pass.

## Timing and full-size projection

Collection through literal K2 took 1.77 seconds, H canonicalization 0.96
seconds, and both charge paths with exhaustive literal guards 1.68 seconds;
total 4.48 seconds.  Naive full parent scaling is about 2,173 seconds and a
25.59-GB K2 checkpoint upper bound.  Cross-run external collection may reduce
disk, but the prefix does not justify a tighter bound.

Scaling the guarded charge pass to 6,229,700 merged profiles gives 167 seconds.
An abstract-only full charge pass should be cheaper because the measured pass
also builds 5.77 million literal comparison rows, but that speedup was not
claimed or run.

## Shared-pass verdict and scope

One shared provider pass is **mathematically sound**: K2 needs the literal
parent, while K3/K4 depend only on the certified profile key.  It is not the
efficient full implementation.  The efficient design is a restartable
parent-run/external merge for K2 and a separate pass over the already merged
profiles for K3/K4 charges.

No full child evaluation, downstream pivot reduction, or new membership claim
was made.  Result SHA-256 is
`6d1b02f99c35d8afbe64b2cf027354aba1937120ebded8aaecddee21f8a3a980`;
canonical logical digest is
`25de086144cea3054fc386123ab3041a4952c80b5e892deb4ab35855269ae969`.
