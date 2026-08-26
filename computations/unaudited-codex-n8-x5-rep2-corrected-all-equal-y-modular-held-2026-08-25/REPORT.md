# Held rep2 corrected all-equal-y modular pilot

Status: **solver-ready, sealed, and unlaunched; independent referee acceptance
and a separate explicit launch clearance are both mandatory.**

The only staged lane is the corrected rep2 Cramer-contracted chart
`all-equal-y/i0/p00/x0/y0/d01`.  Its sealed exact-Q parent has 91 variables
and 6,577 distinct generators.  The modular source is derived byte-for-byte
by replacing the unique `ring r=0,` token with `ring r=32003,`; no variable,
order, generator, or polynomial text changes.  The parent `quit;` is replaced
by one `slimgb(I)` call, literal `reduce(1,G)`, basis-size/remainder prints, and
an explicit unit/nonunit status branch.

The runner is refusal-by-default.  Before `Popen`, it rechecks the sealed
parent, Q source, modular source, Singular, GNU timeout, and runner bindings.
It additionally requires both `independent_referee_acceptance.json` and
`launch_clearance.json` with exact schemas and hashes tied to this package's
future manifest.  Neither file exists in the sealed held package.  A direct
refusal test exited before any Singular process or result artifact appeared.

If later cleared, the sole command is:

```text
gtimeout 195 python3 run_one_lane.py
```

The live Singular child is placed in a fresh process group and measured via
`/usr/lib/libproc.dylib` every 0.1 seconds.  Native limits are 180 seconds and
8 GiB RSS; termination is TERM followed by KILL after five seconds.  Standard
output and error are captured into a fresh `result.json` written atomically.
A pre-existing result forbids relaunch.

Every possible outcome is diagnostic only.  A modular unit closes only this
one localized chart over `F_32003`; it provides no characteristic-zero,
representative, family, or conjecture closure.  Nonunit, timeout, RSS, process,
or schema failure likewise has zero mathematical coverage.  Exact Q, a second
modular chart, and automatic relaunch are not authorized.
