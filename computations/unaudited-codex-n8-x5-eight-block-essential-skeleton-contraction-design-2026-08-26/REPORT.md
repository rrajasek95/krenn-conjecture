# Eight-block essential-skeleton census and contracted held chart

Status: **PASS exact census / conditional degree-four bridge / zero solver runs**.

This package is pinned to the corrected eight-block interface manifest
`43348045...`, not its superseded predecessor.  It independently rebuilds the
matching-essential skeleton of every one of the 616 unresolved records.  An
edge is essential here exactly when it occurs in at least one supported
perfect matching.

## Exact census

Every record has a degree-four skeleton vertex.  The essential-edge
histogram is

```text
12: 88
13: 104
14: 124
15: 184
16: 116
```

Thus exactly **500/616** records are in the at-most-15 interface and the
remaining **116/616** are exact-16.  The latter have raw support size 16, all
four variable-family blocks nonzero, 16 genuine unlabeled graph-isomorphism
classes (class-size census `4:5, 8:10, 16:1`), and 58 two-member orbits under
the literal order-two source/guard permutation.  The earlier count 32 is also
reproduced, but it is only the diagnostic tuple `(raw edge count, essential
edge count, perfect-matching count, degree sequence)` and is not an
isomorphism count.  Across all 616 records there are 51 unlabeled skeleton
classes.

The graph canonicalizer is exhaustive: vertices are first placed in their
invariant degree cells and every within-cell permutation is tested.  The
guard quotient separately applies only `1<->2, 6<->7`, including the variable
family labels.  The two equivalence notions are never conflated.

## Degree-four proof interfaces

The fresh current-source at-most-15 CNF is pinned only through its preflight
manifest `c7863b37...`: 428,223 variables, 3,083,125 clauses, 231,408,707
bytes, SHA `f18ad14a...`.  The preflight rejects the stale legacy instance.
At this package's seal, the independent DRAT replay has not supplied a pinned
terminal seal, so **zero of the 500 records are promoted here**.  A terminal
`s VERIFIED` replay plus its independent manifest would promote exactly those
500 records.

The exact finite implication still needed for the remainder is:

> No exact eight-vertex, three-colour full-X5 witness has a
> matching-essential skeleton with a degree-four vertex and exactly 16
> edges.

A freshly source-reproduced selector/CNF proof of that statement, with
checked DRAT and the current source-to-CNF bridge, eliminates all 116 records
at once.  The historical exact-16 generator/verifier are hashed only as
interface identifiers; their old proof bundle is not imported or replayed.
The historical exact-17 hypothesis adds no coverage to this ledger because
no current record has more than 16 essential edges.

## Smallest exact algebraic fallback

For the smallest new orbit-1 diagonal failure, the corrected eight matching
tensors (including the four-pair equality base with 81 words: 3 pure and 78
mixed) are materialized literally.  On the chart

```text
A07*x=e0, x0!=0,
A35[0,0] A46[0,0] A47[0,0] != 0,
A01[0,0] A15[0,0] A17[0,0] A23[0,0] A26[0,0] != 0,
```

the four-dimensional edge-scaling torus has selected weight minor
`diag(-1,1,1,1)`.  It therefore normalizes `x0` and the three displayed
entries exactly.  Substitution of `A07[:,0]` contracts the raw 171-variable,
6576-generator diagonal system to **82 variables / 6566 generators / 23,011
expanded terms**.  No further constant-coefficient monic pivot exists.  Both
Q and p32003 sources are sealed, but they are one chart only and no Singular
process was run.

Validation passes under standard Python, `-O`, and `-I -S`; 14 hostile
mutations are rejected.  This package makes no deletion-monotonicity,
eight-block closure, or conjecture-level claim.
