# Exception1114 58/6533 smallest modular diagnostic — held

This zero-run package binds the sealed rank-one refinement manifest
`aea0841b…` and exact symbolic-reduction manifest `785ec6cb…`.  Its sole
source is the exact 58-variable, 6,533-generator chart `ed6a47ec…`, reduced
to the established safe diagnostic field `F_32003` by one ring-token change.
Deleting the modular ring token and strong transcript replays the Q input
byte-for-byte; every rational denominator was independently checked nonzero
modulo 32,003.

The appended transcript uses `option(redSB)`, `slimgb(I)`, basis size,
`reduce(1,G)`, unit remainder, and a terminal unit/nonunit status.  A future
modular UNIT is diagnostic only and is accepted by the runner only with the
exact 58/6,533 shape, `GROEBNER_SIZE=1`, `UNIT_REMAINDER=0`, and a unique
`STATUS=UNIT_IDEAL` line.

The single-use runner is pinned to Singular and gtimeout, with native/wrapper
walls 300/315 seconds and a hard 8 GiB process-group RSS cap.  It uses direct
libproc process and process-group census, atomic result persistence, a
nonce/expiry clearance, an exclusive attempt marker, and refuses every
relaunch after any attempted start.  Its overlap census includes CaDiCaL,
drat-trim, Singular, gtimeout, and the D12 executables, so it cannot start
while the combined SAT lane/checker is active.

No `independent_referee_acceptance.json` or `launch_clearance.json` exists;
therefore the runner is held.  No attempt/result/lock exists and no solver
was launched.  Sixteen hostile contract/source/runner mutations were all
rejected.  Exact-Q follow-up is a separate conditional interface whose
future modular terminal, independent audit, Q design referee, and fresh
resource clearance hashes are all absent; it has no runner and no launch
authority.
