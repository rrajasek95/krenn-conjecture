# Spectator completion preserves exactly one private-minus-`Eq` class

## Result

The exhaustive four-site terminal of `020277c` does not proliferate when
spectator perfect matchings, matching differences, restriction/reinsertion,
or overlap descent are added.  In the private/reduced-`Eq` projection there
is exactly one class at every order.

Let `k` be the number of labelled residual perfect matchings.  For each
matching retain `B` and `Eq` copies of the four balanced operation corners,
and put

```text
delta = (1,1,-1,-1).
```

Grant a projection-complete map containing:

- every matching-augmentation-zero difference in each corner, separately
  in `B` and `Eq`;
- the four aggregate physical response/cap columns, which tie `B=Eq`; and
- the four aggregate signless `K2,2` companions in the private block.

This map has rank

```text
8k-1 in dimension 8k.
```

Its unique left kernel is

\[
 \Psi_k=\sum_{m=1}^k\delta\cdot(B_m-\operatorname {Eq}_m).       \tag{1}
\]

Consequently every spectator-Hasse, shuffle, reinsertion, and
window-overlap column whose total mismatch in (1) is zero already lies in
the projected image.  These uniform structures can neither fill the class
nor create further private/`Eq` obstruction directions.  A single
occurrence-local column with nonzero value under (1) fills the projected
quotient.

Exact checker:
[`verify_uniform_uc4_private_eq_spectator_projection_gate.py`](../computations/verify_uniform_uc4_private_eq_spectator_projection_gate.py).

## Proof

The matching-difference columns have disjoint block/corner support and rank

\[
                         8(k-1).                       \tag{2}
\]

After quotienting by them, every matching fibre is represented only by its
augmentation.  The remaining quotient has four `B` and four `Eq`
coordinates.  Its columns are the four diagonals `(e_j,e_j)` and the four
signless shore-crossing `K2,2` incidences.  This is exactly the
eight-coordinate calculation of `f753b5d`: it has rank seven and unique
primitive left kernel

\[
                         \delta\cdot(B-Eq).             \tag{3}
\]

Combining (2) and (3) gives

\[
                  \operatorname {rank}=8(k-1)+7=8k-1, \tag{4}
\]

and pulls (3) back to (1).  Since (1) spans the entire left kernel, the
image is exactly its kernel.  This last equality is the useful strength of
the theorem: no separate census is needed for a new spectator or overlap
column once its total private/`Eq` mismatch is known to vanish.

## Exact controls

Let `delta_B` and `delta_Eq` denote the balanced aggregate over all `k`
matchings.  Then

```text
Psi_k(delta_B)          =  4k,
Psi_k(delta_Eq)         = -4k,
Psi_k(delta_B+delta_Eq) =  0.
```

Thus either a private-only or Eq-only balanced aggregate raises the rank to
`8k`, while a fully decorated tied packet does not.  More sharply, a
private-only `delta` supported on one matching already has value `4` and
fills.  The difference of two such occurrence packets has value zero and
is already in the old image; this is the exact overlap/descent control.

The checker verifies the literal ranks for `k=1,3,15`, corresponding to the
first three spectator sizes, and proves (4) symbolically for arbitrary
`k`.  The number of residual matchings at order `h` is `(2h-3)!!`, so the
statement is uniform in `h`.

## Consequence for the proof frontier

The uniform obstruction is not a growing moment or spectator family.  Its
entire private/`Eq` content is the one scalar

\[
            \sum_m\delta\cdot(B_m-Eq_m).              \tag{5}
\]

Therefore the remaining positive construction has an exact minimal test:
one source-labelled cross-profile `DQ/PS` comparison must have nonzero
value in (5).  If every full-source cross-word column has value zero, (1)
is already the unique projected terminal at all orders.

This does not make an arbitrary bright column physical or finish its other
faces.  Such a column must still carry its word/fine/repeated placement,
target, physical `q`, anchor, ordinary residue, `W`, and shifted ridge in
one source-valid totalization.  Nor does the theorem prove that the current
column list exhausts the global source.  It removes spectator completion
itself from that list of unknowns: only cross-profile gluing can decide the
class.

## Verification

Run normally, optimized, and isolated/no-site.  The checker freezes the
dependency hashes, finite ranks, structural proof data, controls, and
ledger digest
`1912730a076903a3b51c41ec277d5267adf2938752ac17414961cb748188f3d8`.
