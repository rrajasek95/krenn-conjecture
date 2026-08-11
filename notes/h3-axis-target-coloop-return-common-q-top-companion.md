# Every exact 852-return carrier packet needs a new common-q companion

## Result

The second endpoint hybrid leaves `852` possible return terms.  At exact
carrier support retain the three selected pure matchings

```text
K (pure 0),  L (pure 1),  M (pure 2),
```

the first cancellation term `B` with endpoint cells `P0:11,S1:21`, and
the second return `C` with endpoint cells `P2:12,S3:22`.  Keep every
literal decorated common-`q` cell in those five monomials.

Checker:
`computations/verify_h3_axis_target_coloop_return_common_q_top_companion.py`.

For every one of the `852` returns, this finite selected support contains
at least one **private** nonzero matching monomial in a nonzero-colour
coefficient of `q^[3]`.  Since the unary target is `q^[3]=X0`, that
coefficient is zero.  After localizing the selected carrier cells, the
private row is an ordinary source unit.

Equivalently, no exact-support `M,L,K,B,C` carrier packet is a full source.
Every physical completion must add a decorated `q` matching on a different
physical perfect matching in the same literal top word.  This is the first
mandatory omitted source row; it is not an abstract aggregate column.

## Exact private-row audit

Expanding all fifteen six-site perfect matchings and every decorated cell
already selected by `M,L,K,B,C` gives between `4` and `26` private top rows
per return.  A deterministic witness can always be chosen to contain a
cell exclusive to one of the two cancellation tails.  The split is

```text
witness touches exclusive B and C cells: 678,
witness touches one exclusive return tail: 174.
```

Thus the unit is genuinely attached to the return data, not merely to the
old three pure anchors.

There is a stronger minimax choice.  On `848/852` records one can choose a
private row for which **every one** of the fourteen alternate physical
matchings has an off-diagonal `q` edge.  Across those chosen rows the
alternate matchings split as

```text
external off-diagonal edge:          9,549,
anchor-contained off-diagonal edge:  2,323.
```

The first class enters the pinned nonanchor route.  The second enters the
complete decorated-anchor exchange/five-lock interface.  This connects the
forced common-`q` companion directly to the off-diagonal alternatives of
the double-companion theorem (`1ea9807`), rather than merely asserting that
some new support cell exists.

Exactly four records have no such private-row choice: two `q_only` and two
`same_skeleton`, all with `rho3=1`.  Up to the residual-site symmetry they
have

```text
M q-tail = K q-tail = 24|35,   B q-tail = 25|34,
L q-tail = C q-tail = 05|14.
```

Their private words are the symmetry orbit represented by

```text
002222, 001111, 002020, 000202,
```

and each private selected monomial has exactly two all-diagonal alternate
perfect matchings.  This four-record, two-mate switching packet is the
sharp diagonal-`q`/affine residual already retained by `1ea9807`; it is the
only unavoidable diagonal orbit in the complete minimax audit.

The complete distribution of private rows per return is

```text
4:8, 5:14, 6:36, 7:8, 8:148, 9:78, 10:64,
11:90, 12:76, 14:143, 15:12, 17:70, 20:66, 26:39.
```

## The shortest `PS:00` top hybrid

There is a particularly transparent row whenever the two distinguished
return-tail edges are disjoint and their complementary physical edge
already carries a selected diagonal cell.  In canonical labels it is

```text
PS:00 * q01:12(C) * q23:(1,rho3)(B) * q45:aa(selected).
```

It occurs on `604/852` returns:

```text
rho3=0: 158,
rho3=1: 288,
rho3=2: 158.
```

In each available diagonal colour `a`, this is the unique selected
monomial in its full-top word, so the zero coefficient forces a distinct
literal matching mate.

For `rho3=0,1`, every possible alternate matching contains an off-diagonal
`q` edge.  These mates enter either the pinned nonanchor off-diagonal route
or the anchor-contained decorated-edge exchange.  For `rho3=2`, a genuine
diagonal alternative remains.  The canonical claim that there is always
only one such matching is false without a colour guard: when `a=1` or
`a=2`, four sites have the same colour and three diagonal perfect matchings
can occur.  This checker retains those diagonal alternatives rather than
promoting them to a unit.

The short row is unavailable on the remaining `248` records for exact
combinatorial reasons:

```text
complementary physical edge has no selected diagonal cell: 84,
the distinguished B and C tail edges overlap:             164.
```

Those `248` records are not guards: the exhaustive top expansion still
finds a private return-tail row in every case, so they too require a new
matching companion.  What is not yet proved is a uniform route for the
new companion after arbitrary additional `q` support is admitted.

## Scope

This is an exact localized coefficient-unit theorem for the smallest
literal carrier packet and an exact first-companion theorem for every one
of the `852` return records.  It does **not** prove the arbitrary-support
full five-tensor packet empty, and it does not by itself manufacture the
affine target-coordinate point of `ca0849f`.  The remaining load-bearing
step is to route the forced new common-`q` mate through the existing
offdiagonal/decorated-anchor/five-lock alternatives or show that its
diagonal switching class supplies the missing affine line hit.

Run

```text
python3 computations/verify_h3_axis_target_coloop_return_common_q_top_companion.py
python3 -O computations/verify_h3_axis_target_coloop_return_common_q_top_companion.py
python3 -I -S computations/verify_h3_axis_target_coloop_return_common_q_top_companion.py
```

Frozen ledger SHA-256:

```text
7a746bb0b550f85b8bb1903284b0ae3f958e5a4014b950745d63f78a668625c7
```
