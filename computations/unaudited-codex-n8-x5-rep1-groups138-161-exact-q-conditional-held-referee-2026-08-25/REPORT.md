# Rep1 groups 138–161 conditional held-package referee

Verdict: `PASS_HELD_ONLY_FINAL_24_EXACT_Q_SOURCES_DEPENDENCY_ABSENT`.

The producer manifest `25a708451a790a3984052519a5fd129182a54b3fbe65dbc85279b998d0667bf5`
replays.  Independently regenerating groups 138 through 161 from the pinned
canonical census and authoritative quotient generator reproduces all 24
source bytes and hashes.  Every source has 91 variables and 6,577 generators;
the exact aggregate is 42,769,236 bytes.

The dependency adapter accepts the exact synthetic partition 0..87 plus
88..137 and rejects all 12 independent mutations: missing, duplicate, extra,
overlap, reorder, wrong union/status, skip, parallel, and relaunch.  The real
future terminal manifest/result hashes are null and their named files are
absent.  Thus union 0..137 is not established and launch remains blocked.

Static runner audit confirms exact order 138..161, one process at a time,
native/wrapper walls 240/250 seconds, 8 GiB process-group RSS through libproc,
atomic lane results, exclusive single-use marker, exact dependency admission,
and immediate whole-batch stop after the first non-unit, resource, process, or
transcript mismatch.

No acceptance, clearance, attempt, result, or solver artifact exists.  This
referee approves only the frozen conditional design; it grants no launch,
closes no group, and claims no mathematical coverage.
