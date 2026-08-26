# Round 1464 external sequential six-lane portfolio design

Verdict: **launch-ready but held for explicit clearance**.  The sealed r1463
input is checkpoint `1b4dde9f...`, cache `46744c37...`, 2,049,529 columns and
support 2,389.  Independent replay checked all columns with zero failures.

The internal six-way family is superseded because its evidence-based projection
was about 616 seconds, beyond the 520/540-second family gate.  This design runs
the exact ordered tasks `repair/{first,last,rare}`, then
`cold/{first,last,rare}`, each from a fresh identical input clone, one process
at a time under 135 native / 150 wrapper seconds, 36 GiB, tree/nonincremental.

The pinned scorer reuses the accepted Rust provider/checkpoint parsers and
incident-column enumerator.  It selects by the exact built-in key
`(unseen incident frontier, support, stable task index)`.  Every lane atomically
seals result, watchdog, command, metrics, frontier, and checkpoint/cache hashes
before pruning.  Only the current winner and active lane retain large payloads;
losers lose only their derived checkpoint/cache after evidence is sealed.

After all six lanes, a fresh fixed winner replay must byte-match the winner's
checkpoint/cache.  A cold/rare winner additionally runs cap 2.5m from the same
r1463 input and must byte-match cap 2.25m with the cap literal as the sole
normalized command difference.  No state advances past r1464.

The 30 GiB preflight currently passes following compaction record `14e32d19...`.
`LAUNCH_CLEARANCE.json` is intentionally absent, so no clone or solver can
start until the manager explicitly authorizes this exact schedule.
