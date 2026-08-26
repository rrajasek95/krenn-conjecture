# Round 1464 external sequential six-lane portfolio v2

Verdict: **explicitly cleared for one fresh sequential launch**.  The sealed r1463
input is checkpoint `1b4dde9f...`, cache `46744c37...`, 2,049,529 columns and
support 2,389.  Independent replay checked all columns with zero failures.

The v1 lane0 attempt is separately sealed fail-closed by failure-manifest
`b41b7b09...`: its 150-second wrapper stopped the process at 150.80268 seconds,
peak 25,907,776 KiB, before any result or accepted lane evidence existed.  It
therefore contributes zero portfolio coverage.

The internal six-way family is superseded because its evidence-based projection
was about 616 seconds, beyond the 520/540-second family gate.  This design runs
the exact ordered tasks `repair/{first,last,rare}`, then
`cold/{first,last,rare}`, each from a fresh identical input clone, one process
at a time under 300 native / 330 wrapper seconds, 36 GiB, tree/nonincremental.
This wall geometry is the sole operational change from v1; the exact six tasks,
order, scorer, inputs, evidence-before-prune rules, RSS limit, and post-selection
replay/cap contracts are unchanged.

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

The 30 GiB preflight passes following compaction record `14e32d19...`.
The manager explicitly authorized this widened v2 schedule; its clearance file
pins this package manifest before the runner may clone or launch anything.
