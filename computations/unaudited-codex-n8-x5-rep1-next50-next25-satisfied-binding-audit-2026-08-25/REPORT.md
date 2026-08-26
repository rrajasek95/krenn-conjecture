# Rep1 next50 dependency binding audit

Status: **NEXT25 PROOF DEPENDENCY SATISFIED; HELD ACCEPTANCE ONLY; NOT LAUNCH-READY**.

The sealed next25 producer batch `b60bbf4f...` is a strict, unskipped, nonparallel, non-relaunched PASS over exactly groups `11,12,14,16..37`, and is a member of producer terminal manifest `155ebddc...`. Terminal referee result `a2599e9c...` is a member of final manifest `b5de471b...` and binds that producer pair. Combining the independently sealed baseline groups `0..10,13,15` with the 25 new groups gives exactly the disjoint union `0..37`.

The generated held acceptance binds the next50 producer manifest `db8aa8ac...`, prior conditional referee `e3522c8c...`, dependency spec `aba4c979...`, terminal result `a2599e9c...`, final manifest `b5de471b...`, and exact closed union. It remains only in this audit package: no acceptance was copied into the producer package, and no clearance exists.

Fail-closed interface caveat: the frozen next50 runner directly requires `future['closed_union']`, but the sealed next25 terminal result does not contain that field. The closed union is independently proved here, yet this held acceptance must not be used for launch until a separately audited runner/dependency normalization consumes this binding safely. No solver was launched.
