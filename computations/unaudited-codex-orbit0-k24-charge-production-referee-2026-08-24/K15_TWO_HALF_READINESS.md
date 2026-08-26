# K24 grouped K15 two-half production readiness

Status: `READY_CONDITIONAL_SEQUENTIAL_TWO_HALVES`. This audit launched no K15 production.

The frozen family is exactly six IDs in two source-faithful grouped scalars: `D15:{223,232,322}|R:2-3-4` and `D15:{223,232,322}|R:3-2-4`. Each three-ID packet group is counted once; the interface neither fabricates individual packet charges nor claims any other K24 family.

The source-backed literal patch is frozen at source SHA-256 `594701a258a9b9be9b6ec4516ba683eb758b3c4c026ce66b982899d17b2596c9` and binary SHA-256 `230918d02643e1cdc87c6de3e2f0d4a89ac37099a8449d42d8a3e6b063639b57`. On the eight-slice/eight-worker control it reproduced all 13 top-level and 16 per-group scalar fields exactly, took 11.658095 seconds, and independently replayed every emitted literal. Linear projections are 352.657374 seconds for `[0,242)` and 354.114636 seconds for `[242,485)`, leaving more than 185 seconds under each 540-second external alarm.

Run the halves sequentially, only after resource clearance, using the exact commands in `results_k15_two_half_schedule_audit.json`. The frozen launcher refuses overwrite, verifies all source/binary/validator/referee hashes, runs only one of the two intervals with eight workers, structurally validates it, independently replays its literal ledger, and only then publishes provenance. The terminal response cache is reset per R8 slice; slice 0 inserted 334,548 response keys across both groups. No rows are emitted, and the final ledger is only 514 records. Because the sandboxed prefix did not expose a direct peak-RSS counter, retain live RSS checks at 60, 120, and 240 seconds and abort at 15 GiB.

After both provenance reports pass, invoke `validate_merge_k15_fast.py merge` with the two result/ledger/provenance triples and the dedicated referee binary. It accepts only `[0,242)` plus `[242,485)`, enforces exact no-gap/no-overlap scope and full source pins, merges each scalar group once, requires every global bin 0 through 256 for each group, and independently replays all 514 literals before atomically publishing the strict six-ID fragment. It explicitly makes no complete-K24 claim.

The bounded contract passed 30 hostile cases under standard Python, `-O`, and `-I -S`, including wrong U/scope/IDs, an extra sink, fabricated individual charges, count/charge/histogram corruptions, malformed sample metadata, and independent literal mutations of the source seek, head ordinal/coefficient, pivot, child row, and terminal charge.
