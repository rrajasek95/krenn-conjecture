# The loop repairs share a formal second-Hasse diagonal, not yet a physical cell

## Result

The relative-degeneracy idea identifies a real common structure behind the
Gate-I shared loops and the omitted `tau_plus` pair.  Every failed site
collapse identifies two source sites at target site `4`.  In the divided-
power Hasse algebra, the missing local term is exactly

\[
 \partial_4^{[2]}(fg)
       =\partial_4^{[1]}f\,\partial_4^{[1]}g                 \tag{1}
\]

for multi-affine factors `f,g`.  Its coefficient is one.  With ordinary
derivatives the second derivative would produce a factor two, so the Hasse
normalization is essential.

This is the right *formal local model*, but it is not already the required
physical source column.  It is a repeated-direction face `2e4` in the
prolonged Hasse–Schmidt resolution.  The old literal matching/cofactor Hasse
inventory consists only of submatchings and is site-squarefree: all 1680
literal faces have physical site degree at most one.  Hence it contains no
`2e4` column.

Checker:
[`verify_h3_loop_degeneracy_hasse_cross_term_scope_gate.py`](../computations/verify_h3_loop_degeneracy_hasse_cross_term_scope_gate.py).

## The common diagonal is exact

For Gate I, every successful support collapse has

```text
source 0,2 -> target 4,
```

and all three shared labels contain the edge `02`.  Thus their forbidden
`44` loop has target Hasse grade `2e4`.

For `tau_plus`, all sixteen maximal thirteen-label collapses also have their
unique double fibre over target `4`.  Across them, the omitted loop edge is
one of

```text
03, 05, 23, 25.
```

Each occurs in eight omitted-label records.  Therefore five distinct source
loop edges

```text
02, 03, 05, 23, 25
```

all map to the same target diagonal `2e4`.

This explains both the promise and the limitation.  One uniform target
divided-power geometry underlies both gates, but the target coordinate
forgets the source loop label.  A physical comparison must keep that label,
as well as the collision repeated-edge grade (`02` for the Gate-I shared
packet versus `01/04` or `12/24` for the `tau_plus` packet).

## Why the isolated cross term does not yet give `d_fixed`, `d_pair`, or `d_even`

The universal Hasse coproduct theorem does include repeated directions in
the formal prolonged source resolution.  Its stated open step is precisely
the map from that multigraded source resolution to the physical augmented
correction complex.  Formula (1) is an operator coefficient; it is not by
itself a relative syzygy with specified boundary and readouts.

The matching data make this obstruction literal:

- in Gate I, single-C4 replacements reach the allowed fixed and paired target
  choices, but no protected source binomial for those replacements has been
  constructed;
- for `tau_plus`, every single-C4 replacement of an omitted label lands only
  in `B0,B2,B3,B5`; none lands in the required fixed columns `B1,B4`.

Thus even after inserting the diagonal Hasse cross term, `tau_plus` still
needs a same-grade matching/denominator transport to
`(B1+B4)/2`.  Gate I still needs the labelled ordinary-residue section and
protected boundary.  A source-labelled relative diagonal cell would need to
carry all of the following at once:

```text
target diagonal:       2e4,
source loop label:     retained,
word/fine/repeated:    exact physical grades,
matching image:        required B-label combination,
ordinary residue:      required labelled section,
W/target/ainc:         zero after cone correction.
```

That is a genuine mapping-cone/relative Hasse cell.  Adjoining a free
degeneracy symbol with this boundary would merely restate the missing
syzygy; source validity requires deriving it from the complete polynomial
rows or proving its boundary lies in the physical source ideal.

## `beta=0` is not the same degeneracy

The third cofactor `J_M=1` belongs to the same broad Hasse/bar philosophy,
but it is not the second diagonal (1).  It is a nondegenerate order-three
cofactor, equivalently the top of the full-row order-four cube.

This distinction is forced by normalization.  A simplicial string with a
repeated vertex is degenerate and vanishes in normalized chains; its
normalized boundary vanishes too.  Declaring `J_M` to be such a degeneracy
therefore kills the unit rather than producing it.  Treating it correctly as
the unique nondegenerate four-simplex retains all five proper faces.

The committed physical audit then gives the existing obstruction:

```text
source-descent unit:     1,
endpoint ridge rank:     6,
primitive Omega rank:    5,
correct midpoint words:  0.
```

So a sufficiently broad higher relative Hasse/bar theorem might contain both
the loop cell and the `beta=0` cell at different orders.  The ordinary
normalized degeneracy operator does not construct the selected `D0` target
nullhomotopy.

## Frontier

The new structural target is now precise:

> Construct a source-loop-labelled relative diagonal Hasse comparison over
> `2e4`, natural across the five source loop labels, and prove its matching,
> word, fine-grade, residue, and protected readouts.

If such a comparison is componentwise in the source label, it could unify
the Gate-I and `tau_plus` loop repairs.  It would not automatically close
`beta=0`; that requires the corresponding higher-order, root-decorated
member of the same relative family.

## Verification

Run:

```text
python3 computations/verify_h3_loop_degeneracy_hasse_cross_term_scope_gate.py
python3 -O computations/verify_h3_loop_degeneracy_hasse_cross_term_scope_gate.py
python3 -I -S computations/verify_h3_loop_degeneracy_hasse_cross_term_scope_gate.py
```

The frozen ledger digest is
`bfa637ff164e5483f8f7649755b1c3d45a383132308e07822df2073260d01704`.
