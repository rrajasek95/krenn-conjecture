# Combined exact-16 materialization referee and held solver plan

The materialized combined CNF is an exact streaming composition: only the
original base header is replaced, all 3,083,172 original body clauses are
byte-identical, and the exact 897,301-clause combined patch follows with no
trailing data.  The resulting 244,617,151-byte CNF has SHA-256 `c96d4ac1...`
and exact header `p cnf 464139 3980473`.

The referee checked all 35,892 canonical ledger entries and every one of the
897,300 selector-to-block implications, plus the single global selector OR.
It binds the independently rebuilt 92-class union (nine shared classes),
35,892 support union, and 3,492 cross-layer support overlap.  The original
base hash/path guard and actual stream derivation prove replacement; appending
to the narrow `dc5cd1ca...` CNF is explicitly rejected because selector IDs
alias and its old global OR cannot remain.

The CaDiCaL 1.9.5 plan is held with zero launches.  One future cleared lane
must rehash the exact input and terminate once: SAT requires a complete
464,139-variable assignment, a full 3,980,473-clause replay, and selector /
support / graph-class extraction; UNSAT requires a fresh DRAT proof followed
by independent pinned `drat-trim` verification.  Any other outcome is zero
proof coverage with no relaunch.  Manager, nonce, resource, and package-
manifest clearance fields remain null.
