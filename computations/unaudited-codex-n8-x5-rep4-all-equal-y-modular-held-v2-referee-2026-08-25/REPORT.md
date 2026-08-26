# Rep4 hardened-v2 held-package referee

Status: **PASS / HELD ONLY**.

The p=32003 source is byte-for-byte the independently reconstructed specialization of the pinned rep4 exact-Q source plus only the solver epilogue. It has exactly 91 variables and 6,577 generators. The package is distinct from the consumed v1 lane and reuses no prior clearance, attempt, result, or execution artifact.

The corrected runner matches the accepted rep5-v2 safety semantics: fresh fail-closed libproc census, correct PID-count interpretation, process-group RSS summation with fail-closed rusage, internally pinned 195-second `gtimeout`, short-lived nonce plus manager/resource/no-overlap clearance, an exclusive pre-Popen attempt marker, and stale/abrupt-exit refusal. The six prior safety defects are fixed.

No acceptance, clearance, attempt, result, log, watchdog, temporary file, or solver run exists. Approval is held-package design approval only: it gives zero mathematical coverage and authorizes neither launch, exact Q, a second lane, nor relaunch.
