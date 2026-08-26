# Nine-block exact-17 degree-four target-union referee

Verdict: **PASS_STATIC_EXACT17_TARGET_UNION_REFEREE__FUTURE_BASE_HELD**.

The referee independently regenerated the nine-block unresolved census from
the pinned source algorithms and matched the sealed residual manifest
`b5494d96...`: exactly 534 exact-17 records, 267 literal guard pairs, and 50
unlabelled graph classes. It then exhaustively chose every degree-four center,
every singleton neighbor, all permutations of the other three center
neighbors, and all permutations of the three outside vertices.

The 50 classes give 24,048 rooted/permuted embeddings and exactly 18,180
distinct normalized 17-edge supports. The sorted ledger is 927,180 bytes and
has SHA-256
`f280c2b3223a9673c80d2aa7bfed7f97c0558fbc2dcb80f4ecac88f16c4b9dd8`.

For a future independently pinned current max-17 base with header `(V,C)`,
the replacement patch allocates selectors `V+1` through `V+18,180`. Each has
25 implications fixing the complete block assignment over variables 226--250,
and one global selector OR is added. The exact delta is therefore 18,180
variables and `18,180*25+1 = 454,501` clauses, producing header
`(V+18,180, C+454,501)`. No numeric final header is accepted until the future
base path, hash, and header are independently sealed.

Records 1114, 1978, 2014, and 2036 are explicitly outside this target union:
they have 16 essential edges and degree sequence `(3^4,5^4)`, hence no
degree-four vertex. They are not closed here. Hostiles reject omitted
rootings/permutations, any omitted record/class, malformed edge counts,
historical-role substitution, premature future-base binding, additive use on
a max-16 CNF, 26-per-selector arithmetic, or a missing global OR.

This package read or wrote no large CNF, launched no solver, and proves no
SAT, UNSAT, residual closure, or conjecture statement.
