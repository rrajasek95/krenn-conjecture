# Post-referee K18 K2 intermediate cleanup

`PASS`. After verifying Tail's independent final-referee logical digest
`9b2ab638c40cb0145814e86e55520884abc9ef0ea55d80bb76174fe4b094bca2`
and rehashing both final checkpoints against `CHECKPOINTS.sha256`, exactly the
291 contiguous intermediates `pchild_chunk_0000.bin` through
`pchild_chunk_0290.bin` were removed.

The deleted byte total was exactly `41,298,079,440`; no `pchild` file remains.
The 5,381,923,399-byte parent/pair ledger, exact parent-run ledgers,
12,675,197,280-byte H18PIV2 checkpoint, and 8,837,274,560-byte H18IRR2
checkpoint remain present. No other file was deleted.

The old cleanup helper was not invoked because its marker parser expects the
obsolete status `PASS_INDEPENDENT_K18_REFEREE` and flat hash fields, while the
accepted referee artifact uses `PASS_INDEPENDENT_FINAL_K18_REFEREE` and nested
checkpoint hashes. The cleanup instead used the already audited exact filename
ledger after independently checking all headers, intervals, sizes, and final
hashes; this avoids fabricating or weakening a pass marker.

If the intermediates are ever needed again,
`run_full_hidden_k16_k2_orbits.rs::build_child_chunks_parallel` regenerates
each missing atomic chunk from the retained
`hidden_k16_decorated_pair_orbits_full.bin` and frozen filtered-K16 structure,
then validates complete interval coverage before merging. That is a full
resource-intensive job and requires a fresh explicit gate.
