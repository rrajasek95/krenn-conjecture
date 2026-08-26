# K15/K3 grouped occurrencewise K2 charge

`PASS`. After the full profile merge passed independent review (logical
`16aea24f…`), an eight-worker read-only pass evaluated the 12 literal K2 tails
of every one of the 25,564,391 nonzero merged profiles in 13.983197 seconds.
It did not collect rows, generate K21 tails, clean up inputs, or touch K16.

The exact grouped DAG component is
`D15:{223,232,322}|R:3-2`. Its producer intentionally combined the three
packet weights before the profile merge, retaining only one minimum literal
witness. Therefore the aggregate below is source-faithful, while three
individual scalars are not reconstructible from this checkpoint and are
explicitly reported as `null` rather than inferred.

Exact results at `U=400591699200`:

- profile records: `25,564,391`;
- profile-tail evaluations: `306,772,692`;
- full source occurrences: `27,742,646,256`;
- irreducible profile-tail evaluations: `268,748,622`;
- irreducible source occurrences: `24,587,895,984`;
- full coefficient mass: `22,381,186,445,623,060,070,400`;
- irreducible coefficient mass: `20,521,282,992,848,083,353,600`;
- grouped full 77-charge: `1,505,666,730,204,685,762,560`;
- grouped irreducible 77-charge: `1,461,387,462,129,632,378,880`.

Every merged record—not merely a sample—passed literal signature, profile,
pivot, denominator, witness, and source-range checks before its tails were
evaluated. `k15_k3_group_charge_samples.tsv` retains 256 distributed literal
response witnesses (SHA-256 `3a1fc64a…`). The result JSON SHA-256 is
`6de9c573ba136304e91db2a9fc83ad1ab2804cee5103102cd77ef568fb60fdb7`;
evaluator source SHA-256 is `10f94217…` and optimized binary SHA-256 is
`947c6832…`.

The merged checkpoint and all 485 producer parts remain present.
