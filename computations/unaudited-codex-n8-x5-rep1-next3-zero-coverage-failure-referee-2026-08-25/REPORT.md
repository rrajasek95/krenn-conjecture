# Independent rep1 next-three zero-coverage failure referee

Status: **PASS fail-closed; zero coverage; the cleared next-three plan is terminal.**

The producer manifest replays. The runner created only an empty `group15/` directory and then received `PermissionError: [Errno 1] Operation not permitted` while invoking `/bin/ps` for the mandatory fresh per-lane census. Source inspection confirms materialization and Singular creation occur strictly after that census.

No group-15 source, preflight, result, watchdog, log, temporary file, or Singular process was created. Groups 17 and 25 are absent, and no batch result exists. Thus accepted coverage is exactly zero. The plan may not be patched, relaunched, or continued to later groups.

This is not a geometric failure: no arithmetic occurred. A wholly new, independently reviewed group-15-only contract is logically permissible, but remains held. It must use a fresh sibling/directory, direct libproc census and RSS accounting with no `/bin/ps`, the original source and limits, explicit fresh clearance, atomic outputs, and a stop-after-any-terminal/no-relaunch rule. It cannot authorize groups 17 or 25.
