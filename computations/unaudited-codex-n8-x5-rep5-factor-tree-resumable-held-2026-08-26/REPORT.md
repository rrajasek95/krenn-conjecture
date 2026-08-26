# Rep5 memoized factor-tree closure — held zero-run design

This package designs a resumable exact factor-tree closure for the 18 unresolved localization siblings recorded in the sealed capped outcome. It is held: no clearance exists, no rep5 state was expanded, and no Singular or other solver was launched.

## Canonical finite-state invariant

Relative to the fixed 64-coordinate order, a state is a disjoint pair `(Z,U)`: coordinates set to zero and coordinates localized nonzero. Every generator is derived afresh from the pinned source by deleting terms meeting `Z`, dividing the maximal common power of every coordinate in `U`, primitive/sign-normalizing integer coefficients, deduplicating, and sorting. The state key binds the schema, source hash, both masks, and the canonical generator digest.

The reduction is independent of localization order because division by common coordinate powers commutes. Equal keys therefore have the same localized/specialized syntactic ideal, the same decided coordinates, and the same admissible descendants. Deduplication changes traversal multiplicity, not coverage. Each edge assigns one previously unassigned coordinate, so depth is at most 64 and the entire state space is bounded by `3^64`. A toy three-variable model exhaustively checks all 27 states, all localization orders, scalar normalization, and key uniqueness.

## Frozen exact branching and acceptance

Candidates are unassigned coordinates dividing every monomial of at least one canonical generator. The order is: largest divisible-generator count, then smallest zero-child term count, smallest zero-child generator count, and coordinate name. Children are `D(x)` (mark `x` localized) and `V(x)` (mark `x` zero), preserving `Spec(I)=Spec(I[x^-1]) union Spec(I+(x))`.

Acceptance requires an empty frontier, replay-valid keys and generator digests, no factor-exhausted nonunit leaf, and reverse-DAG truth for all 18 roots. Only then may the atomic result say `PASS_EXACT_ALL_18_ROOTS_STRUCTURAL_UNIT`. A partial frontier, node/resource abort, or a factor-exhausted leaf cannot imply closure.

## Resumption and resources

Each commit writes an immutable compressed record shard, a complete compressed frontier, and finally an atomic `CURRENT` pointer binding their sizes and SHA-256 hashes. Orphans not named by `CURRENT` are ignored. Resume replays every named artifact and re-derives state keys before expansion.

A future lane is limited to 25,000 new states, 2,000,000 global states, checkpoints every 250 expansions, native 480 seconds, hard wrapper 510 seconds, and 8 GiB live process-group RSS sampled by direct libproc every 250 ms. The wrapper uses an exclusive marker, nonce/expiry clearance, atomic logs/telemetry, and TERM-then-KILL. No such clearance or launch artifact exists now.

The nine-stratum lineage remains pinned through the capped parent package. This held design makes no rep5 closure claim.
