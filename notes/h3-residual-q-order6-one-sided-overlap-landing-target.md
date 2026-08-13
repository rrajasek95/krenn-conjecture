# The primitive order-six face is exactly a one-sided overlap arm

## Outcome

The order-six source-shadow construction and the post-KS rank theorem are
not independent end-game steps.  The primitive face common to all 188 terms
is

```text
07:11 wedge 24:11.
```

Here `07:11` is a colour-1 arm from endpoint `S=7` to internal site `0`, and
`24:11` is a disjoint internal cofactor edge.  If site `0` is chosen among
the target-full sites forced by full-nine incidence, it is already rank
three in the overlapping cap.  Normalize the deficient quotient at `S` to
miss `e1`; the `07:11` arm is then nonzero in that quotient, so the overlap
profile changes exactly

```text
(2,3) -> (3,3).
```

Thus one physical totalization can plausibly perform both outstanding local
jobs: close the residual endpoint holonomy and land the active carrier at a
four-good overlapping cap.

Checker:
`computations/verify_h3_residual_q_order6_one_sided_overlap_landing_target.py`.

## Exact ingredients

For an eight-site `h=3` source, deleting the two cap endpoints leaves six
residual sites.  The unary equation `q^[3]=X_0` makes colour zero full on all
six; full-nine incidence gives a four-cover in each bright colour.  Their
intersection supplies at least two internal target-full sites.  A
target-full site remains rank three when promoted to an endpoint of either
overlapping cap.  The other endpoint has a one-dimensional deficient
quotient.  After a target-basis change, write its rank-two span as
`span(e0,e2)`.

The order-six target coefficient on `07:11 wedge 24:11` is one.  Conditional
on a source-faithful totalization preserving it as a literal nonzero
determinant/cofactor carrier, its outer head is `e1`, while the internal head
at site `0` is already contained in a rank-three star.  Elementary rank
algebra then gives `(3,3)`.

This is strictly weaker than repairing both deficient quotients of the
original `(2,2,3,3)` cap.  The proof may descend on the overlapping cap.

## Selected-anchor normalization is now closed

The selected-anchor synchronization theorem proves that the site/colour/tail
choice is not an additional branch.  Relative to endpoint `S`, either a
target-full site lies outside its two selected bright neighbours, in which
case the overlap already has selected rank `(3,3)`, or the two full sites are
exactly those neighbours.  Choosing the colour-one neighbour then makes the
selected `S-u:11` arm the missing quotient direction, and its selected
bright matching supplies two disjoint nonzero pure-`11` cofactor edges.
Relabelling gives precisely `07:11 wedge 24:11`.

What remains is source typing in the stronger sense: the relative
totalization must produce a physical active carrier, not merely a Hasse
derivative direction.  In the already-rank-three branch, an unoccupied
`S-u` direction is not declared active.  Failure of physical activity must
still yield the existing same-row support dependence or the exhaustive
separator/generator alternative.

## Consequence for the shortest proof

The preferred local theorem can now be stated as one package:

> Physically totalize the explicit order-six residual chain.  Either its
> primitive endpoint/cofactor face is visible through a target-full overlap,
> producing a rank-`(3,3)` active cap, or its complete family of primitive
> faces is source-dependent/dark and yields support contraction or the
> terminal separator/generator branch.

This merges the former residual-cell theorem with the selected-anchor part
of active-rank landing.  Hall routing and the global decreasing potential
remain downstream.

## Scope

No physical totalization or activity of an unoccupied derivative arm is
proved here.  The exact face topology, one-sided rank calculation, and
selected-anchor synchronization identify why the same missing physical
comparison is the highest-leverage target for Theorems A and B/C.

Verification:

```text
python3 computations/verify_h3_residual_q_order6_one_sided_overlap_landing_target.py
python3 -O computations/verify_h3_residual_q_order6_one_sided_overlap_landing_target.py
python3 -I -S computations/verify_h3_residual_q_order6_one_sided_overlap_landing_target.py
```

Frozen ledger SHA-256:

```text
ee0d5de58b1e74555af7617e5d72f894fff4dab304dc3ee04d3bac5b3cde2900
```
