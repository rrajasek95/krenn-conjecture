# Audit record: SUPERSESSION-2026-08-01-04

Dependency: `LOCAL-INVERTIBLE`.

Replacement commit: `6e622d9a9572524246d7714ef7ddcb6c4742d7bf`.

Independent auditors:

* `/root/terminal_math_certification_audit`;
* Claude session `3a596df9-733e-4f60-b63e-dd1c89fd67d9`, subagent
  `agent-affa1534932acdab4` (corpus-wide optimized-mode audit).  The preserved
  source trace is
  `/Users/rishi/.claude/projects/-Users-rishi/3a596df9-733e-4f60-b63e-dd1c89fd67d9/subagents/agent-affa1534932acdab4.jsonl`.

Outcome: **PASS; no mathematical claim or hypothesis changes.**

The checker
`computations/verify_invertible_complete_anchor_one_hole_filtered_descent.py`
replaces 21 bare assertions with 21 raising checks and removes its
`__debug__` guard.  The proof note is unchanged.  The import auditor ran the
checker under `python3`, `python3 -O`, and `python3 -I -S`; every mode returned
the same 77 local subspace pairs, 14,448 isotropic-selector cases, 24 incidence
count pairs, and the same four PASS lines.  A substantive
formula mutation failed under both normal and optimized execution.  The
earlier corpus auditor independently mutation-tested the converted checker in
both modes and found no deleted work, optional-message failure, or altered
exception control flow.

`SUPERSESSION-2026-08-01-02` did not identify its auditor or provide a
permanent report, used an abbreviated commit identifier, and was not linked to
a consolidated-spine update.  This record is the append-only procedural
replacement for that incomplete entry.

SHA-256:

```text
f1c46626ad7d68d4a86be5baf758d11337702d793ff68bc9cd274a98e3211da0  notes/invertible-complete-anchor-one-hole-filtered-descent.md
6089e2b9a3105ebf1df499641727690ceba7ac02f1d476188b59bba53d1219c7  computations/verify_invertible_complete_anchor_one_hole_filtered_descent.py
```

The first hash is unchanged from the prior accepted audit.  The checker hash
replaces
`4be6c2add51e8da4c144f0332f6ad7b1cc2f3dadaf7b49629d08d56dd0227c8d`.
