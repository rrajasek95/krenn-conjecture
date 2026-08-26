# Combined eight+nine-block exact-16 target-union referee

Verdict: **PASS_STATIC_COMBINED_TARGET_UNION_REFEREE**.

The referee independently rebuilt the eight-block exact-16 layer from the
compact corrected interface and recomputed the nine-block layer from the
authoritative source algorithms without reading its 5 MB materialized result.
The layers contain 16 and 85 unlabelled degree-four exact-16 graph classes;
nine classes overlap, hence the exact graph-class union is 92.

Exhaustive degree-four-center and singleton-neighbor rootings, all `3!`
permutations of the remaining center neighbors, and all `3!` permutations of
the outside vertices yield 5,508 eight-layer masks and 33,876 nine-layer
masks. Their intersection has 3,492 masks, so the deduplicated union has
35,892. The sorted support ledger has SHA-256
`6bffb2962242725f8bd0603dfaeb91f64c2ee0e4430632b445b42e44d4a424d5`.

The pinned current SAT source maps the 25 block variables to 226--250. One
selector per target and 25 complete-cube implications per selector, followed
by one global selector OR, cover every target and prevent the unrestricted
generic skeleton from satisfying the refinement. The exact patch delta is
35,892 variables and `35,892*25+1 = 897,301` clauses; the resulting header is
464,139 variables and 3,980,473 clauses.

The already materialized narrow CNF (`dc5cd1ca...`, header
433,755/3,220,873) uses the same sound selector semantics, and its 5,508
supports are an exact subset of this union. It is not an additive base for the
combined patch: its selector IDs occupy 428,248--433,755 and its global OR
continues to require a narrow target. A combined materializer must therefore
replace the narrow patch and start from the original 428,247-variable CNF.

Hostiles reject omission of either layer, treating the nine shared classes as
distinct, omitting any rooting/permutation family, malformed supports,
incomplete/flipped selector cubes, and omission of the global OR. This is
static design/referee evidence only: no large CNF was read or written, no
solver was launched, and no SAT, UNSAT, or theorem claim is made.
