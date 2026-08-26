# Current augmented degree-four at-most-17 base generation: held plan

Verdict: **PASS_STATIC_HELD_ZERO_RUN__NO_CLEARANCE**.

The plan pins the current generator and support library and compares against
the sealed current max-16 build. The future max-17 command preserves minimum
degree 0, center degree 4, the absence of the degree-five-plane option, and
write-only mode. Its sole semantic CLI change is `--maximum-edges 16` to
`17`; output paths change only to fresh nonce-suffixed temporary names.

The pinned source consults `maximum_edges` once, in a 25-literal Sinz
sequential counter. Bound 16 uses 384 counter variables and 776 clauses;
bound 17 uses 408 and 823. Therefore the exact expected delta is +24
variables/+47 clauses and the expected fresh base header is
428,271/3,083,219. That header remains provisional until generation and an
independent full hash/header/clause replay agree.

Generation is held while the exact-16 lane is active. A future clearance must
bind a fresh nonce, terminal exact-16 resource-clear manifest, independently
approved direct-libproc runner, empty process census, absent output paths,
and at least 32 GiB free. The single generator run is limited to 8 GiB RSS,
120 seconds native/150 seconds outer wall, writes only same-filesystem temp
paths, and promotes atomically after producer checks. Every failure is zero
coverage and quarantines the temporary outputs.

After terminal generation, one independent reader must stream-hash and
recount the complete candidate, verify header 428,271/3,083,219, replay the
JSON/options/source/telemetry, and seal an acceptance manifest. Until that
manifest and a separate clearance exist, the exact-17 ledger
`f280c2b3...` cannot be patched and no solver may start. Conditional on the
base seal, that patch would add 18,180 variables/454,501 clauses and yield
header 446,451/3,537,720.

No CNF was generated or read, no patch was materialized, no clearance was
consumed, and no solver ran.
