# Combined exact16 materialization referee and held solver plan

Verdict: **PASS_EXACT_STREAM_DERIVATION_HELD_NO_SOLVER**.

The independent replay bound the exact16 eight-block terminal manifest
`bcd2cc5f...`, materializer manifest `cf720d0e...`, clearance `477098f5...`,
build record `e68b8d0b...`, patch package `745f5fa1...`, and patch
`2ac0e05c...`.  It parsed every one of 3,980,473 output clauses and proved
that output `c96d4ac1...` (244,617,151 bytes; 464,139 variables) consists of
only the replacement header, the byte-identical original-base body, and the
byte-identical patch, with no trailing bytes.

The compact patch was also replayed semantically from the sealed 35,892-line
support ledger: all 897,300 selector implications and the one global OR are
exact.  This independently enforces the original-base-only/replacement guard;
the narrow exact16 CNF was not used as a base.

The producer validator correction is sound for the sealed held state: its
four expected `zero_run` keys are present and false, and setting any one true
is rejected by the corrected `all(value is False ...)` predicate.  Its
post-materialization refusal is expected, so it is not reused as a terminal
validator; this referee package supplies the terminal replay instead.

The companion CaDiCaL 1.9.5 plan is **HELD**.  It permits exactly one fresh
lane under 7,200 seconds/16 GiB only after a new manager clearance, package
manifest replay, exact input rehash, resource/no-overlap census, and atomic
artifact preflight.  SAT requires a full model/clause replay and selector
extraction; UNSAT requires the pinned drat-trim checker to exit 0 with literal
`s VERIFIED`.  No solver was launched and no SAT/UNSAT theorem is claimed.
