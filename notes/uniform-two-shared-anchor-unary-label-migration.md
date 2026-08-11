# Two-shared anchor edges have a finite unary label migration

## Statement

Let `e=uv` lie in the selected pure-`k` and pure-`l` matchings, but not in
the selected pure-`m` matching.  Write

```text
g = u-x,     h = v-y
```

for the two edges of the pure-`m` anchor at the endpoints of `e`.  Suppose
`q_e^{ij}` is a nonzero non-pure cell relative to colour `k`:

```text
(i,j) != (k,k).
```

Then the complete unary/common-`q` rows force at least one of:

1. a pure selected-anchor matching reselected away from the current
   decorated edge;
2. a nonzero avoiding matching with a physical pair outside the selected
   anchor union;
3. an ordinary localized source unit; or
4. the nonzero direct cell `q_e^{mm}`.

The last cell carries the third-anchor label at both endpoints of the
formerly two-shared pivot.  If `(i,j)=(m,m)` it is already present at the
start; otherwise it is exactly the “different direct cell” which same-cell
companion tails could not manufacture in `1c08419`.

Checker:
`computations/verify_uniform_two_shared_anchor_unary_label_migration.py`.

## Four complete-row partitions

Every step uses the same source identity.  For a nonzero decorated cell
`q_f^{rs}` on a selected pure-`a` edge,

```text
0 = q_f^{rs} C_f^a + R_f,                (rs)!=(aa),       (1)
```

where `R_f` is the complete aggregate of matchings avoiding `f`.

If `C_f^a=0`, the pure-`a` target row reselects a pure-`a` matching
avoiding `f`.  If `C_f^a!=0`, (1) either forces `R_f!=0` or is a localized
unit.  From a nonzero `R_f`, choose any nonzero literal term.  If its
physical matching leaves the selected anchor union, the pinned nonanchor
rank-three/active route applies.  It remains only to follow terms wholly
inside that union.

At `u`, the union has exactly the two edges `e` and `g`; at `v`, exactly
`e` and `h`.  Consequently an anchor-contained term avoiding one edge is
forced onto the other.  The endpoint words then give the finite chain

```text
e:(i,j)  ->  g:(i,k)  ->  e:(i,m)  ->  h:(m,k)  ->  e:(m,m).   (2)
```

More explicitly:

* the first row through `e:(i,j)` avoids `e`, hence uses both third-anchor
  arms and contains `g:(i,k)` and `h:(j,k)`;
* the row through `g:(i,k)`, with pure-`m` cofactor, avoids `g` and returns
  through `e:(i,m)`;
* the row through `e:(i,m)`, with pure-`k` cofactor, avoids `e` and forces
  `h:(m,k)`; and
* the row through `h:(m,k)`, with pure-`m` cofactor, avoids `h` and returns
  through the new cell `e:(m,m)`.

All four rows are genuinely mixed: respectively their through labels are

```text
(i,j)!=(k,k),  (i,k)!=(m,m),
(i,m)!=(k,k),  (m,k)!=(m,m).
```

Thus no target constant is silently used in (1).

## Alternating-path interface

The third anchor's edges `g,h` are the endpoint segments of the alternating
`k/m` component through `e`.  The internal component may contain cycles or
an arbitrarily long path.  Those choices occur entirely inside the complete
cofactors `C_f^a` and avoiding aggregates `R_f`; the proof needs only the
forced degree-two endpoint incidence.  This is why the parity split of the
pinned Hall alternating-path theorem does not open a new support family
here.

The checker exhausts all ordered two-shared anchor triples at six and eight
sites and every anchor-contained matching term.  It also audits all `48`
ternary choices of `(k,l,m,i,j)`, expands the four literal word labels on a
canonical physical chart, and verifies that the terminal label is `(m,m)`
in every case.

## Scope

This is an integral-domain, source-labelled complete-cofactor theorem.  It
does not assume bounded support and it does not enumerate support faces.
Its conclusion is the requested direct-label/reselection/off-anchor/unit
dichotomy.  Any subsequent use of `q_e^{mm}` to upgrade a chosen overlap
must still cite the appropriate activity/rank theorem; no four-good rank is
claimed merely from the direct cell.

Run

```text
python3 computations/verify_uniform_two_shared_anchor_unary_label_migration.py
python3 -O computations/verify_uniform_two_shared_anchor_unary_label_migration.py
python3 -I -S computations/verify_uniform_two_shared_anchor_unary_label_migration.py
```

Frozen ledger SHA-256:

```text
bdb6758249e8e33552d236c178de8d5e4be048b0c7a6b7920dfec8763dd5517a
```
