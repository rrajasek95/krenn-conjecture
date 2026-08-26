# Round 1262 internal sequential portfolio

This gate evaluates the exact built-in six-task tree portfolio sequentially in one process (`auto/best`, `portfolio-period 1`, `portfolio-parallel no`). The tasks, solutions, frontier/support objective, stable tie-break, and final selected state are the same semantics as the failed parallel attempts; only evaluation scheduling changes.

The portfolio uses native 520 seconds and watchdog 540 seconds at 36 GiB. The watchdog is an exact two-literal ceiling/message change from the audited 155-second sibling. After selection, fixed control and 1.5M-cap candidate use native 110/watchdog 120 and must produce byte-identical state. No round beyond 1262 is authorized.
