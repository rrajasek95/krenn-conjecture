# Rep5 rank-stratified guard-pivot design v2

Status: `PASS_SUPERSEDING_CORRECTED_NINE_STRATA_ZERO_SOLVES`.

This package supersedes the rejected v1 design and binds rejection manifest
`8a1c4e5faf9e73cffcfb5a8b52c697aa79fbb15e45aa9cae6d27911dd62ffea7`.
The rejection was literal, not abstract: four removed A37 symbols survived in
already-expanded A35 and A36 expressions in every open source.

The v2 builder reconstructs the dependency graph from raw retained entries.
It defines the proportional A37 accessor first, then expands the A35 partner
column, A36 reconstruction, A06/A17 substitutions, and finally all 6,561
amplitudes.  An independent identifier census finds zero occurrences of every
removed A17 and A37 symbol, and no equation identifier outside its ring.

Six open sources were regenerated from scratch.  Each has 84 variables and
6,562 generators (6,561 amplitudes plus one combined saturation).  The three
literal-valid closed-complement sources were copied byte-for-byte from v1 and
revalidated at 86 variables and 6,570 generators.  Their hashes are unchanged.

Exact sparse-polynomial checks replay `u0.v=0`, `u0.w=d*abar`,
`u0 x (tm*(w x v))=-tm*d*abar*v`, the cleared A17 and proportional-A37
forward/reverse identities, and the exhaustive per-chart decomposition
`D(t1) union D(t2) union V(t1,t2)`.  Three pivot charts therefore produce the
claimed nine design strata.

No Singular process or ideal computation was run.  These are design inputs,
not unit certificates: mathematical coverage, rep5 closure, and performance
remain unclaimed.  The consumed k0 modular attempt was not reused.
