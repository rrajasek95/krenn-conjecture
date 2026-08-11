# The four diagonal incidence kernels do not lift multiplicatively

## Result

The common-`q` minimax theorem leaves four symmetry-related target-coloop
records for which every private selected top monomial has two diagonal
alternate perfect matchings.  Their first unary-plus-four-response
incidence lock is highly singular, but none of its diagonal realizations is
a physical common-`q` completion.

Checker:
`computations/verify_h3_axis_target_coloop_four_diagonal_switch_five_lock.py`.

For one representative the selected tails are

```text
M q-tail = K q-tail = 24|35,
B q-tail = 25|34,
L q-tail = C q-tail = 05|14,
rho3 = 1.
```

The other records are its residual-site mirror and the `q_only` versus
`same_skeleton` source labels.

## Exact five-row deletion lock

For a diagonal top matching `Q` in residual word `w`, delete each of its
three edges and insert the endpoint cells actually selected by
`M,L,B,C,N`.  Record the resulting column in feature order

```text
(top, R11, R12, R21, R22).
```

Each of the four private words has one selected matching and two diagonal
alternates.  Subtracting the selected column from an alternate column gives
eight top-preserving switch directions per record.  Their exact histogram
is

```text
(0,0,0,0,0): 6,
(0,0,1,0,0): 1,
(0,1,1,0,0): 1.
```

Thus the five-row switch map has rank `2` and kernel dimension `6`.  Six
directions are literal zero columns, not numerical cancellations.  The two
visible directions meet only `R11,R12`; neither `R21` nor `R22` appears.
Consequently the incidence lock alone supplies neither an opposite crossed
wedge nor a target constant/source unit.

This is an important scope guard: an incidence kernel is not yet an actual
finite deformation of the common `q`.

## Multiplicative diagonal completion is impossible

The full common-`q` multiplication kills that formal kernel.  In every
private top equation the selected nonzero monomial forces at least one of
its two diagonal alternate monomials to be nonzero.  Choose one active
alternate in each of the four rows.  There are exactly

```text
2^4 = 16
```

choices per record and `64` over all four records.

Every choice contains a nonzero diagonal perfect matching with one `00`,
one `11`, and one `22` edge.  Its residual word has colour multiplicities
`(2,2,2)`.  Therefore it has exactly one all-diagonal perfect matching.

The checker tests this against the **complete diagonal envelope**: all
`00/11/22` cells on all fifteen residual edges are allowed, together with
the already selected off-diagonal `12` cell.  The rainbow coefficient still
has exactly one supported monomial.  A matching in a `(2,2,2)` word cannot
use exactly one cross-colour edge, so the single existing `12` cell cannot
provide a mate.  The witness-word histogram is

```text
001122: 16,
001212: 32,
001221: 16.
```

All `64` diagonal choices are therefore localized source units.  A genuine
completion of any of the four records must introduce at least one
**additional off-diagonal** `q` cell.

## Exact routing of the forced off-diagonal mate

For each of the `64` diagonal choices, use the lexicographically first
private rainbow word and classify all fourteen alternate physical
matchings relative to the three selected pure anchors.  The complete split
is

```text
external off-diagonal matching:   840,
two-shared decorated anchor:       40,
one-shared affine return:           16.
```

The first class enters the pinned nonanchor active route.  In the second,
some off-diagonal edge lies in two selected pure anchors, so the complete
two-shared unary label-migration theorem applies: it gives pure-anchor
reselection, an off-anchor avoiding matching, a source unit, or the third
direct label.

The sixteen residual slots are all one literal row, up to the residual-site
mirror and source-kind duplicate.  In the displayed representative it is

```text
output word: 00112200,
matching:    PS:00 | 05:02 | 14:02 | 23:11.
```

The two off-diagonal edges `05,14` are exactly the two `q`-tail edges of
the pure-one anchor `L`; each belongs to `L` alone.  The third residual
edge `23` is diagonal `11`.

Applying the complete decorated-edge exchange to either `L` edge is
source-valid.  A dark pure-one cofactor reselects `L` away from that edge;
a non-dark cofactor forces an avoiding matching, and any off-anchor exit
enters the certified active route.  What is not automatic is synchronization
of the two anchor-contained avoiding aggregates.  The two decorated edges
are disjoint, so the same-star hypothesis of the five-lock switch theorem
does not hold; the current row also supplies no opposite crossed `R21`
face.  Thus `00112200` above is the smallest exact affine-return row left
after applying the pinned theorems, not a hidden five-lock closure.

## Consequence and scope

This removes the last unavoidable diagonal-mate orbit from the 852-return
minimax.  Combining the two exact audits gives:

* `848` records directly force an off-diagonal matching mate;
* the remaining `4` cannot be completed using arbitrary diagonal cells and
  the one already selected cross-colour cell, so they also force another
  off-diagonal cell.

The result does not by itself close the arbitrary-support packet.  The new
off-diagonal cell enters the already pinned nonanchor or
decorated-anchor/five-lock route; the anchor-contained return of that route
is the remaining affine-accessibility interface.  The crossed-`M`
specialization is independently closed by the private-site theorem, but it
is not silently assumed here.

Run

```text
python3 computations/verify_h3_axis_target_coloop_four_diagonal_switch_five_lock.py
python3 -O computations/verify_h3_axis_target_coloop_four_diagonal_switch_five_lock.py
python3 -I -S computations/verify_h3_axis_target_coloop_four_diagonal_switch_five_lock.py
```

Frozen ledger SHA-256:

```text
1b2bc65653177b77e81b59604a9b292b1e831d93627f78ea409f6dea4928abf1
```
