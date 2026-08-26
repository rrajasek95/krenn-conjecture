# Exact-16 target-union static referee

Verdict: **PASS_STATIC_EXACT16_TARGET_UNION_REFEREE**.

From the compact, pinned eight-block census (`MANIFEST.sha256` SHA-256
`bef35566...`), the referee independently rebuilt the 616-record histogram
`12:88, 13:104, 14:124, 15:184, 16:116` and all 16 unlabelled exact-16 graph
classes. Exhaustive choice of every degree-four center, every singleton
neighbor, all `3!` other-neighbor permutations, and all `3!` outside-vertex
permutations gives 8,928 rooted embeddings and exactly 5,508 distinct
normalized supports. Their sorted line ledger is byte-identical to the
cross-producer convention: SHA-256
`3caf456fcd37b963f22d7e70b914817a5fd71032dbea873729d6dc0d3dd50aae`.

The pinned SAT source allocates 225 entry variables followed by the 25 block
variables 226--250. The target-union refinement adds one selector per support.
Each selector has exactly 25 implications fixing the complete block cube, and
one global OR requires at least one selector. Therefore every target support is
covered and an unrestricted generic skeleton is excluded. The exact delta is
5,508 variables and `5,508*25+1 = 137,701` clauses, so the patched header is
433,755 variables and 3,220,873 clauses. The previously proposed 26 clauses
per selector / 143,209-clause delta is explicitly rejected.

Omitting any center rooting, singleton rooting, neighbor permutation, or
outside permutation changes the witness census; malformed/extra supports,
bad block-variable ranges, incomplete/flipped implications, and omission of
the global OR are also refused. This package is design/referee only: it did
not open or write the 231 MB base CNF, launch a solver, or establish SAT,
UNSAT, or any theorem promotion.
