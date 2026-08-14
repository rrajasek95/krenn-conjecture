# Support 17: noncoordinate inserted edges retain singleton debt

## Result

Every genuinely noncoordinate one-edge insertion into the 148-orbit
support-16 cap-dark frontier retains an inherited singleton mixed row.  No
cap formula for the inserted block is needed.

The exhaustive totals are

```text
support-16 pure-supported completion charts       81,685
missing edges per chart                               12
inserted noncoordinate supports                        4
total augmentations                            3,920,880

inherited singleton by cardinality             3,408,610
inherited singleton by literal word check         512,270
unresolved necessary counterguards                       0.
```

The four inserted supports are `01`, `02`, `12`, and `012`, with every
declared component live.  Together with the coordinate one-edge recurrence,
this closes arbitrary support type for the added block over all 148
cap-dark support-16 completion families.

The checker is

```text
python3 computations/verify_n8_support17_all_guard_noncoordinate_edge_debt.py
python3 -O computations/verify_n8_support17_all_guard_noncoordinate_edge_debt.py
python3 -I -S computations/verify_n8_support17_all_guard_noncoordinate_edge_debt.py
```

## Exact mechanism

Let `S` be the inherited singleton mixed-word set of one support-16
completion.  For a new edge `e`, precompute every new perfect matching of
`G+e`; each contains `e`.  If the inserted block has support `T`, that
matching contributes one decorated word for each colour in `T`, multiplied
also by the support size of the old target block when the matching contains
both noncoordinates.

If the total number of new decorated occurrences is smaller than `|S|`, not
all old debts can be mated.  This monotone cardinality bound proves over 3.4
million cases.  In the remaining 512,270, the checker expands only the new
matching occurrences and compares their literal eight-site words with `S`.
Every case misses at least one inherited word.

A missed inherited singleton has its original nonzero coefficient unchanged:
the new edge occurs in no matching of that word.  Therefore it remains an
exact mixed-row/unit contradiction regardless of the actual nonzero values
of the inserted block components.  No cancellation or generic-coefficient
assumption is used.

## Why no cap analysis is hidden

The inserted block is not assigned a coordinate colour, so the complementary
binary-cap test from the coordinate recurrence would not be source-valid.
This audit deliberately makes no cap claim.  It closes every case at the
matching-row level before a cap covector is needed.

This is stronger than treating the noncoordinate edge as several coordinate
specializations: all its live components are expanded simultaneously, so
new word collisions between components are included.

## Remaining support-17 scope

What remains is not the 148 cap-dark frontier.  It is

1. persistence or repair of descendants of the 133 support-16 routes already
   landed by original two-cap, complete-private, or collision-normalization
   arguments; and
2. the support-17 graph class whose high-degree vertices form an independent
   set, where no high-high edge deletion reaches the present support-16
   register.

For the 110 complete-private routes, a first structural count already shows
that 905 of 1,320 representative missing-edge augmentations retain a literal
private cap.  The 415 failures are the finite deformation strata to classify;
208 of them acquire at least one crossed binary face structurally, while 207
have no private or binary face before colours and source rows are imposed.
