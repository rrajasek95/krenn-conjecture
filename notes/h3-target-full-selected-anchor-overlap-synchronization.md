# Target-full sites synchronize with the selected bright arms

## Result

For an eight-site `h=3` source, write the cap endpoints as `P,S` and the
six residual sites as `U`.  Choose the pure-zero target matching through
`PS`, and one selected matching in each bright target.  Let `n_1,n_2` be
the two selected bright neighbours of `S`.

The corrected incidence theorem gives at least two target-full residual
sites: `q^[3]=X_0` makes colour zero full everywhere, while the two bright
incidence sets each have size at least four.  Let `F` be the target-full
set.  Exactly one of the following elementary alternatives occurs.

1. Some `u in F` lies outside `{n_1,n_2}`.  In the overlap cap `(S,u)`,
   the selected `PS:00`, `S n_1:11`, and `S n_2:22` arms all survive.
   Hence the selected `S`-star already has rank three; the `u`-star has rank
   three because `u` is target-full.
2. No such `u` exists.  Since `|F|>=2`, necessarily
   `F={n_1,n_2}` and `n_1!=n_2`.  Choose `u=n_1`.  The overlap retains the
   selected colour-zero and colour-two arms, while the deleted selected arm
   `S u:11` is exactly the missing quotient direction.  Its bright matching
   has two internal pure-`11` edges, both disjoint from `S u`; either is a
   nonzero selected cofactor tail.

After relabelling the six internal sites, the second alternative is exactly

```text
07:11 wedge 24:11,
```

the primitive face of the order-six comparison.  Thus the site/colour
normalization in the one-sided landing is not an independent conjectural
choice.

## What this removes

Conditional on a source-faithful physical totalization of the order-six
class, there is no third selected-anchor rank branch:

- either the target-full overlap is already rank `(3,3)`; or
- the primitive bright arm is the selected missing quotient axis and has a
  selected nonzero pure cofactor.

The remaining issue is now genuinely the physical relative totalization
and its activity, not finding a compatible full site, colour, and tail.

## Scope

The theorem does not construct the relative order-six cell.  In the
already-rank-three branch it also does not infer that an unoccupied
endpoint direction is active merely because it is a Hasse derivative.
It proves only the matching/rank/label synchronization needed once the
physical carrier exists.

Verification:

```text
python3 computations/verify_h3_target_full_selected_anchor_overlap_synchronization.py
python3 -O computations/verify_h3_target_full_selected_anchor_overlap_synchronization.py
python3 -I -S computations/verify_h3_target_full_selected_anchor_overlap_synchronization.py
```

Frozen ledger SHA-256:

```text
9f659658be255adff96c424c557fbe32742af49b65e727b61c1de18fcc24d908
```
