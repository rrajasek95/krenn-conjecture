# Opposite companions close every honest even Hall path

## Statement

The six-site packet of `242a91c` is not exceptional.  It is the radius-two
window around the distinguished even vertex of an arbitrary fixed-hole
alternating path.

Write the selected colour-one/colour-two component as

```text
v0 -Q2- v1 -Q1- v2 -Q2- ... -Q1- v_{2r}
```

and let the dual-blind centre be the interior even vertex `c=v_{2t}`.  Put

```text
e1 = v_{2t-1} c,       e2 = c v_{2t+1},
f2 = v_{2t-2} v_{2t-1},
f1 = v_{2t+1} v_{2t+2}.
```

Thus `e1,f1` are colour-one anchor edges and `f2,e2` are colour-two
anchor edges.  A paired opposite companion has the same four local labels
as in the six-site packet:

```text
on Q1:  e1 has head 2 at c, and f1 has head 2 at v_{2t+1};
on Q2:  e2 has head 1 at c, and f2 has head 1 at v_{2t-1}.
```

All remote labels in this normalized word are zero.  Then exact complete
rows give one of:

1. pure-anchor reselection, an off-anchor avoiding matching, or a localized
   unit through the existing complete-exchange theorem;
2. a terminal pure missing-colour direct cell through the existing
   two-shared label migration; or
3. two source-active central arms `e1,e2`, good at all four deleted stars,
   with nonzero distinct-head transition minor.

Checker:
`computations/verify_uniform_hall_even_path_opposite_companion_wedge.py`.

## Four local ranks

Let `P-c` be the pure-zero arm at the centre.  After deleting `e1`, the
three rows at `c` are supplied by

```text
Q0 on P-c,       Q2 on e2,       the row-one decoration on e2.
```

Their domain columns are `(P,0),(v_{2t+1},2),(v_{2t+1},0)`, hence the
rank is three.  After deleting `e2`, interchange colours one and two.

At the outer endpoint of `e1`, use the pure-zero arm, the pure-two arm
`f2`, and the row-one decoration on `f2`.  These again give rank three
unless the zero arm and `f2` are the same physical edge.  This parallel
collision is the only local incidence which the minimal six-site packet
does not display.  In that case the edge is shared by the selected
pure-zero and pure-two anchors, and carries the non-pure cell `10`.  Apply
the two-shared theorem with

```text
(k,l,m)=(2,0,1).
```

It gives an earlier reselection/off-anchor/unit landing or the direct cell
`11`.  In the last branch, `q00,q11,q22` occupy the three distinct tail
columns `0,1,2`, restoring rank three.  The other outer endpoint is
identical with `(k,l,m)=(1,0,2)` and terminal cell `22`.

This use of the terminal cell is activity-safe: it is used only as a
deleted-star column.  No claim is made that the cell alone has a nonzero
cofactor.

## The central transition

At `c`, let

```text
B = q_e1^(2,0),      D = q_e2^(1,0)
```

be the two nonzero opposite companions.  The only entries in the same two
physical/tail columns which can cancel their head wedge are

```text
X = q_e1^(1,0),      Y = q_e2^(2,0).
```

Therefore

\[
                       \kappa=XY-BD.                 \tag{1}
\]

If `X` or `Y` is nonzero, its endpoint label is the selected anchor label;
the pinned complete decorated-anchor exchange gives the prior landing.  In
the sharp residual `X=Y=0`, so

\[
                       \kappa=-BD\ne0.               \tag{2}
\]

The selected colour-one and colour-two response monomials contain `e1`
and `e2`; deleting those cells leaves nonzero literal cofactor products.
Thus (2), together with the four rank-three deleted stars, is a
source-active distinct-head four-good overlap.

## Why path length adds no topology

An interior even vertex has exactly the four-edge window above.  All
remaining path edges enter only the two selected activity cofactors.  The
fixed `Q1/Q2` union is one path plus vertex-disjoint even alternating
cycles.  Cycles away from the window switch independently and are absorbed
in the same literal cofactor class.

A different matching class which changes the window is not silently
identified with that class.  If its changed cell is a `k`-labelled
endpoint/direct cell, it enters the complete-exchange or two-shared
migration branch above.  Otherwise it is precisely an unmatched or
unequally weighted tail in the sense of the signless-incidence theorem
`f3716b2`; the present path theorem makes no common-tail inference from
physical incidence alone.

Hence diagonal padding and arbitrarily long path tails do not change the
local rank or (2).  The only collapsed incidence is a doubled common
`Q1/Q2` edge.  That is an alternating two-cycle, not an honest path, and is
outside the fixed-hole path branch of `3ed7f4a`.

The theorem is deliberately coefficient-honest: it starts after choosing
one nonzero literal opposite-companion term from the complete aggregate.
It does **not** assert that arbitrary unequal multi-class aggregates share
a common tail; that separate provenance issue remains the exact scope guard
of the signless-incidence theorem.

## Exact remaining cases after combination

Combining this theorem with `07a1f02` and `f3716b2` gives the following
sharp list for the fixed-hole opposite-companion branch.

* Honest path endpoints and the radius-two window close here.
* A parallel `Q0` outer-arm collision closes by two-shared label migration.
* A central `k`-labelled entry closes by complete exchange; without it the
  distinct-head minor is nonzero.
* If every residual row has one literal common tail and exactly two lock
  columns, `f3716b2` closes the whole component: bipartite components
  (including even cycles) give the exact alternating deletion kernel, and
  nonbipartite components give an odd-cycle localized unit.

The only remaining coefficient case is therefore an unmatched full-row
column or unequal/multiple literal tail classes which cannot be routed to
one of the endpoint/direct cells above.  This is the same sole provenance
gate already frozen by `f3716b2`, not a new longer-path topology.  A doubled
common `Q1/Q2` edge is an alternating two-cycle rather than a path and also
belongs to that non-path provenance boundary.

## Verification

Run

```text
python3 computations/verify_uniform_hall_even_path_opposite_companion_wedge.py
python3 -O computations/verify_uniform_hall_even_path_opposite_companion_wedge.py
python3 -I -S computations/verify_uniform_hall_even_path_opposite_companion_wedge.py
```

Frozen ledger SHA-256:

```text
facd9b94ba9dfa6734f7060f0069ef3e464d4b1c8f5b72b36db83af0c97d0248
```
