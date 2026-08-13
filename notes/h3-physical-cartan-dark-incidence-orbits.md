# The dark Cartan incidence frontier has 36 candidate-arm types

## Orbit reduction

The physical landing census leaves 151,200 selected packets in which the
chosen target-full overlap already has rank `(3,3)`, but its candidate arm
is absent from both selected bright matchings.  Their exact split is

```text
shared selected bright neighbour                       76,950
target-full set avoids two distinct bright neighbours  74,250.
```

In the shared branch, the common neighbour belongs to the target-full set
in 41,850 packets and lies outside it in 35,100.  This distinction does not
change the overlap choice: deleting the common neighbour would remove both
selected bright arms, so the viable overlap still uses a different
target-full site.

Quotienting complete packets by all `6!` physical permutations of the
internal sites gives 261 ordered-colour orbits, or 181 after the global
bright-colour swap.  Most of this count records irrelevant choices of the
whole target-full subset.  If one retains only

```text
(selected colour-1 matching,
 selected colour-2 matching,
 one candidate target-full site outside their S-neighbours),
```

the 33,750 possible triples have exactly **36** physical orbit types modulo
the bright swap.

Checker:
[`verify_h3_physical_cartan_dark_incidence_orbits.py`](../computations/verify_h3_physical_cartan_dark_incidence_orbits.py).

## What the corrected signed face supersedes

Only 4,770 candidate triples have a selected internal physical edge common
to both bright matchings and disjoint from the candidate site; 28,980 do
not.  This split remains a useful incidence falsification check, but it is no
longer the activity frontier.  Correcting the signed primitive face exposes
two nonzero pure-matching tori.  Physical relabelling then closes 150,930 of
the 151,200 packets in this file.  The only survivors are 270 double-coloop
packets, with identical two-edge tails or one residual `C4`; see
`h3-order6-primitive-selected-matching-activity.md`.

Consequently the 36 types should not be proved by 36 activity computations.
They were the finite falsification skeletons for the structural theorem, and
the corrected signed calculation has now verified that theorem away from the
single double-coloop orbit:

> For a candidate target-full site whose selected arm is absent, the complete
> additional occupied support either enters a nonzero primitive Cartan
> interference coefficient, or the reachable complete columns form a tight
> source-typed set and yield an anchor-safe dependence/physical separator.

The orbit census remains useful as a falsification suite.  The intended final
local proof should now explain the two-coloop interference lock directly,
not revisit the 36 old incidence types.

## Scope

Only physical matching incidence and symmetry are used.  No Hasse direction
is called active, and no Hall family is inferred from bare matching tails.
The reduction removes irrelevant target-full-set bookkeeping but leaves the
source-typed activity/dependence statement open.

Verification:

```text
python3 computations/verify_h3_physical_cartan_dark_incidence_orbits.py
python3 -O computations/verify_h3_physical_cartan_dark_incidence_orbits.py
python3 -I -S computations/verify_h3_physical_cartan_dark_incidence_orbits.py
```

Frozen ledger SHA-256:

```text
019a750af79c662e7e25498fdc7e76480960c54afb6ab9afa65fa8985c9a8fce
```
