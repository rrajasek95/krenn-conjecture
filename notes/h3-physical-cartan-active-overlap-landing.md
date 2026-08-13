# Physical Cartan landing reduces to one coefficient-activity gate

## Composition theorem

The formerly conditional order-six landing now has its missing hypothesis.
Physical source-orbit Cartan descent makes the primitive face

```text
S-u:11 wedge ab:11
```

an actual coefficient-space relative direction.  Here `ab:11` is a
selected internal bright edge disjoint from `u`.  Physical site
relabeling fixes the cap endpoints and sends every such pair to

```text
07:11 wedge 24:11.
```

This is not a claim that an unoccupied scalar cell was already in the
support.  Cartan descent supplies a genuine physical **direction** in that
cell.  Its coefficient still has to evaluate nonzero, or its vanishing must
yield the dependence/separator branch.

## The two exhaustive branches

Let `n_1,n_2` be the selected bright neighbours of endpoint `S`, and let
`F` be the target-full internal sites.

1. If `n_1!=n_2` and either selected bright neighbour belongs to `F`, choose
   that neighbour.  Deleting its selected arm leaves the colour-zero arm and
   the other bright arm, while the chosen bright matching supplies two
   internal cofactors.  The physical Cartan carrier repairs `(2,3)` to
   `(3,3)`.  A global swap of the two bright colours covers either neighbour.
2. Otherwise choose `u in F` outside `{n_1,n_2}`.  Then the selected colour-zero,
   colour-one, and colour-two arms at `S` all survive in the overlap `(S,u)`.
   Both endpoint stars already have rank three.  One of the selected
   colour-one matching tails avoids `u`, giving the canonical face type.
   However `S-u` belongs to neither selected bright matching.  Thus the
   selected data do not certify a nonzero quadratic Cartan coefficient.
   This is the remaining activity gate.  It has two exact incidence types:
   the bright neighbours coincide, or the target-full set avoids both
   distinct bright neighbours.

The checker exhausts all `461,700` selected matching/full-site packets:

```text
selected target-full arm repairs (2,3) to (3,3)       310,500
shared bright neighbour, activity unresolved           76,950
target-full set avoids both, activity unresolved        74,250
```

Both currently occupied and new arm directions occur.  The latter are the
scope guard: source provenance of a direction is weaker than nonvanishing of
its coefficient at the selected point.

## Frontier shift

Every packet with distinct bright neighbours meeting the target-full set is
finished—`310,500` of the `461,700` exact incidence packets.  The remaining
two types already have rank `(3,3)` at both endpoints and ask only whether
one Cartan coefficient is nonzero.  If it is, the active clean overlap is
done.  If every target-full choice is dark, the complete source orbit must
produce an occupied-column dependence or the physical separator/generator.
This is much smaller than the former general transverse-rank theorem, but it
is not yet proved.

After this activity gate, the remaining conjecture-level issue is
earlier/lateral: prove uniform entry of an arbitrary no-clean-zero packet
into this synchronized `h=3` packet, or complete the inactive dual comparison
and routing.  Active clean-pair descent and the six-site terminal
contradiction are already proved.

Verification:

```text
python3 computations/verify_h3_physical_cartan_active_overlap_landing.py
python3 -O computations/verify_h3_physical_cartan_active_overlap_landing.py
python3 -I -S computations/verify_h3_physical_cartan_active_overlap_landing.py
```

Frozen ledger SHA-256:

```text
a57bee7b222b44d614eadf3f9564b6c06ef0e8bea5bbd5fa04637130f849d8c8
```
