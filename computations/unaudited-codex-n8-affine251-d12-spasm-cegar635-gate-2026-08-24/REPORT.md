# SpaSM gate on the exact D12 CEGAR round-635 system

Status: **FAIL CLOSED — no SpaSM solution, no promotion.**

This package tested only the current local round-635 CEGAR state at the pinned
prime 1,073,741,827. It did not extend the CEGAR search, launch D12 full
closure, or run a second prime.

The source-faithful streaming bridge checked the checkpoint and vector-cache
headers, exact 222,676-column order, internal cache FNV, and the retained
support-315 tree candidate. The retained candidate has target value 1 and
annihilates every cached column. It then exported the exact system
`A^T y = -target` in SpaSM's left-solve orientation:

- cached equations: 222,676
- non-target variables: 14,814,561
- matrix nonzeros: 22,539,255
- RHS nonzeros: 2
- SMS matrix: 376,423,806 bytes, SHA-256
  `f8ec63f06931384707a97d284ba3767ea9d11934af26d7b38a3069051f65c487`
- export: 15.744 seconds

SpaSM did not complete within the 180-second end-to-end export-plus-solve
gate. It was terminated after receiving the remaining approximately 163.278
seconds, while scanning a second 14,591,895-row Schur complement; its last
progress record was 12,604,048 rows. No rank or solution was emitted. Thus
there is no SpaSM solution to replay, no warm run to time, and no exact
equivalence result to accept.

The retained Rust tree solve for this same round was 6.230818 seconds. The
incomplete SpaSM cold path was at least 180 seconds including export, so the
decision is `DO_NOT_PROMOTE`. A sandboxed `setrlimit` preflight failed before
spawning a process; the accepted run therefore used hard process-group wall
termination. Peak RSS was not captured for the terminated solver, and this is
another reason no result is accepted.

Authoritative failure result:
`results_cegar635_spasm_gate_failure.json`, SHA-256
`9bc6056f5a2f1ab10b7712ab31ba568a2a16bdf41c75caaf00dec753398a30ae`.
The final fail-closed audit rejected 9/9 hostile mutations.
