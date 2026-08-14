# Support 17: landed-parent persistence register

## Reduction and current frontier

Every eight-vertex, 17-edge support graph of minimum degree at least three has
an edge joining two vertices of degree at least four.  Deleting that edge
preserves minimum degree and gives a support-16 graph.

Indeed the total excess above cubic is `34-24=10`.  If the high-degree set
`H` were independent, its vertices would have total degree `3|H|+10`, all
landing in the cubic complement of capacity `3(8-|H|)`.  Hence `|H|<=2`.
But two vertices can carry at most eight excess units, contradiction.

Thus the support-17 problem reduces to persistence/repair over support-16
parents.  The 148 cap-dark parents are already closed for coordinate and
noncoordinate inserted blocks by the singleton-debt recurrence.  This note
freezes the remaining structural register over the 133 already-landed
parents.

The checker is

```text
python3 computations/verify_n8_support17_landed_parent_persistence_register.py
python3 -O computations/verify_n8_support17_landed_parent_persistence_register.py
python3 -I -S computations/verify_n8_support17_landed_parent_persistence_register.py
```

## Complete-private parents

There are 110 complete-private parent orbits and twelve missing edges per
representative, for 1,320 augmentations.

```text
literal private cap persists               905
private cap fails                          415
  failure has crossed binary face(s)       208
  failure has no private or binary face    207.
```

The 415 failures quotient to 355 directed support-17 graph types.  Their
parent multiplicity distribution is

```text
multiplicity 1: 307 types
multiplicity 2:  39
multiplicity 3:   7
multiplicity 4:   1
multiplicity 5:   1.
```

The 905 persistent cases are already active-clean by the denominator-free
left/right kernel construction: the added edge creates no companion term in
at least one complete private response.

## Original two-cap parents

There are 22 parent orbits and 264 augmentations.

```text
new complete-private cap                     24
no private cap, at least two binary faces   139
no private cap, zero or one binary face     101.
```

The first 24 are unconditional landings.  The 139 with at least two binary
faces are the exact rank-deformation candidates, but structural face count
alone does not prove that their direct and shore colours meet the
complementary rank criterion.  The 101 hard augmentations quotient to 91
directed graph types.

## Collision-normalization parent

The sole collision parent has twelve augmentations:

```text
two binary faces : 3
one binary face  : 8
zero binary face : 1.
```

The old argument was a missing pure-colour row, not a cap, so all twelve need
a new normalized-row or cap audit.  They quotient to seven directed graph
types.  Only one augmentation is structurally devoid of a binary candidate.

## Sharp remaining statement

The unresolved work is now finite and source-labelled:

1. prove colour/rank persistence on the binary candidate strata, allowing
   the old cap covector to deform while preserving all diagonal readouts;
2. on the 309 hardest representative augmentations
   (`207 private + 101 two-cap + 1 collision`), enumerate normalized anchor
   charts and test complete mixed singleton/unit rows; and
3. extend only any genuine survivors to a noncoordinate deleted edge.

The structural checker makes no claim that a crossed binary face lands
without the complementary-colour condition.  It also does not identify
independently typed cap covectors across faces.  Those are precisely the
remaining algebraic—not graph-census—issues.
