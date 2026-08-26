# Rep5 torus-cover smallest same-chart exact-Q conditional pilot

Verdict: **PASS held only / zero run**.  This package preserves selected chart
Q source `13c204f7...` byte-for-byte and derives runtime source `4c788634...`
solely by replacing the census-only final `quit` with the strong
`slimgb/size/reduce(1,G)` transcript.  The chart remains exactly 73 variables,
6,561 generators, with assignment `yn1=yn2=t0=1,t2=0`.

The exact-Q lane is structurally inert.  It requires a future producer result
and independent referee proving `UNIT_IDEAL_MODULAR_DIAGNOSTIC` for modular
source `c36bd3b7...` on this identical chart.  All four future paths and hashes
are null and `future_modular_unit_dependency.json` is absent.  The verifier
reopens both future manifests and results, replays their manifests, checks the
full strong transcript and exact assignment/source/shape, and refuses stale,
fabricated, cross-chart, nonunit, or unsealed dependencies.

Runner `e44b4168...` is single-use and fail closed: direct libproc process
census and group RSS, 480-second native wall, 510-second wrapper, 8 GiB RSS,
exclusive pre-Popen attempt consumption, atomic result, stop after every
outcome, and no other chart or relaunch.  It also rehashes the torus producer
`2b220f91...`, torus referee `20f24c8d...`, modular held package `21df0017...`,
held referee `16a32d07...`, and prior consumed timeout `0cb2ba30...`.

No dependency binding, independent acceptance, manager clearance, attempt,
result, log, lock, temporary, Singular run, or mathematical coverage exists.
This package does not close the chart, the 16-way cover, or rep5, and does not
authorize exact-Q execution by itself.
