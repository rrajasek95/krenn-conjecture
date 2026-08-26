# Rep1 next-50 exact-Q schedule — conditional held zero-run

This package regenerates the 50 lowest canonical rep1 groups that would remain after groups 0 through 37 are closed: exactly groups 38 through 87 in strict ascending order. The 50 exact-Q inputs total 89,221,420 bytes and byte-match the sealed canonical census.

The schedule is deliberately not launchable yet. `future_next25_dependency.json` names the future next25 terminal-referee manifest and result, leaves both hashes null, and records `satisfied=false`. At execution time the runner requires those external files, exact PASS status and group ledgers, manifest membership of the result, and both hashes bound independently in later acceptance and clearance files.

If that prerequisite is eventually satisfied, the runner is single-use and strictly sequential, with per-lane 240-second native wall, internally wrapped 250-second wall, 8 GiB direct-libproc process-group RSS, atomic lane results, and immediate whole-batch stop on the first nonunit/resource/process/transcript failure. Skip, reorder, relaunch, and parallel execution are forbidden.

No solver, attempt, result, acceptance, or clearance exists in this package. It establishes no new mathematical coverage.
