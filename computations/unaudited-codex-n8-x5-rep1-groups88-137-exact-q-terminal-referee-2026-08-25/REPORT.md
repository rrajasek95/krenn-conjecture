# Groups88–137 terminal compatibility alias

Status: **PASS / exact interface compatibility / zero new arithmetic**.

The independently sealed terminal audit uses the fields
`dependency_closed_union_before_batch` and `closed_union_after_batch`; the
frozen groups138–161 adapter expects the equivalent names
`baseline_closed_union` and `closed_union` at this path.  This alias maps only
those names after replaying producer batch `a26b032d...`, producer terminal
manifest `4fa50b0e...`, audit result `1de758a8...`, and audit manifest
`23d2a558...`.  The exact sets are 0–87, 88–137, and 0–137 respectively.

No source, runner, solver result, or mathematical conclusion is changed.  The
alias adds zero solver runs and exists solely to satisfy the frozen adapter's
field/path interface.
