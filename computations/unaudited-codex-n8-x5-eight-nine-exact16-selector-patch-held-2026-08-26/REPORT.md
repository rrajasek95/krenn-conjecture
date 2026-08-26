# Combined eight+nine exact-16 selector patch: held producer

Verdict: **PASS_COMPACT_PATCH_MATERIALIZED__HELD_NO_BASE_READ_NO_SOLVER**.

The package binds the independent combined referee manifest `46a29e7f...`
and exact 35,892-support ledger `6bffb296...`. It materializes only the
standalone selector clause fragment: 35,892 selectors, 25 complete block-cube
implications per selector, and one global selector OR. The fragment has
897,301 clauses, 13,136,474 bytes, and SHA-256
`2ac0e05c9599f09066fc6b0bdd5812ac78e85328ec3928ef3f3f6498e7af2059`.

Against the original current max-16 base (`9e057710...`, header
428,247/3,083,172), the fragment would produce header
464,139/3,980,473. This must be a replacement materialization from that
original base. Appending to the already materialized narrow CNF
`dc5cd1ca...` is forbidden: selector IDs 428,248--433,755 are reused with a
different sorted ledger, and the narrow global OR would continue to restrict
the conjunction to the narrow subset.

Default operation remains held. Full materialization requires a fresh,
nonexpired post-checker manager clearance binding this package manifest and
the terminal exact-16 DRAT checker/resource-clear manifest. A future
materializer must stream-rehash/recount the original base, verify this exact
patch, rewrite only the header, append the fragment, promote atomically, and
launch no solver.

The large base was not read, no combined CNF was produced, no clearance was
consumed, and no solver ran.
