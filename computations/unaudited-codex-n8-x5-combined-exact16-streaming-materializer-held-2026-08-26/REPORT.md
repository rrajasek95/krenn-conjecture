# Combined exact-16 streaming materializer: launch-ready held

Verdict: **PASS_LAUNCH_READY_HELD_ZERO_RUN**.

The materializer binds the compact patch package manifest `745f5fa1...`,
patch SHA `2ac0e05c...`, and the newly sealed exact-16 terminal VERIFIED
manifest `bcd2cc5f...` / audit result `3264b7a8...`. Its default action reads
only those compact artifacts and refuses all large-base access.

After a fresh nonexpired manager clearance is instantiated, the one-shot
execute path accepts only the original max-16 base `9e057710...`. It rejects
the narrow CNF `dc5cd1ca...`, reads and hashes the original header/body once,
writes replacement header 464,139/3,980,473, copies only the original body,
appends the exact patch, fsyncs, and atomically renames without overwrite.
The deterministic output size is 244,617,151 bytes; no output hash is
preclaimed.

Execution additionally requires terminal resource clear, zero matching heavy
processes, at least 16 GiB free, a fresh nonce, and this package's final
manifest hash. Any mismatch quarantines only the nonce temp and grants zero
coverage. The materializer never launches a solver. A separate independent
full output hash/header/clause/body/suffix replay remains mandatory before any
future solve.

Manager clearance, nonce, expiry, materializer-manifest binding, and live
resource census remain null. No large base was read and no target was built.
