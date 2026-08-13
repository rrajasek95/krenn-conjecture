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

1. If some `u in F` is outside `{n_1,n_2}`, then the selected colour-zero,
   colour-one, and colour-two arms at `S` all survive in the overlap `(S,u)`.
   Both endpoint stars already have rank three.  One of the selected
   colour-one matching tails avoids `u`, giving the canonical face type.
   However `S-u` belongs to neither selected bright matching.  Thus the
   selected data do not certify a nonzero quadratic Cartan coefficient.
   This is the remaining activity gate.
2. Otherwise `F={n_1,n_2}`.  Choosing `u=n_1` leaves the `S`-star with
   `span(e0,e2)`, and the selected arm `S-u:11` is precisely the missing
   quotient direction.  Its selected bright matching supplies two disjoint
   pure-`11` cofactors in the same selected matching.  The pinned physical
   carrier changes `(2,3)` to `(3,3)`.

The checker exhausts all `461,700` selected matching/full-site packets:

```text
already rank (3,3), Cartan coefficient unresolved    454,950
selected arm repairs (2,3) to (3,3)                    6,750
```

Both currently occupied and new arm directions occur.  The latter are the
scope guard: source provenance of a direction is weaker than nonvanishing of
its coefficient at the selected point.

## Frontier shift

The trapped selected-arm branch of one-sided landing is finished.  The only
remaining branch already has rank `(3,3)` at both endpoints; it asks whether
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
63624aa41504526b8ef7676cab86bd75f3e7b550771a6acce99fe33d8bb36dd8
```
