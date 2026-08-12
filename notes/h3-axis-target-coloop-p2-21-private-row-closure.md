# The missing `P2:21` face exits through its first private row

## Result

The last affine block in
[`h3-axis-target-coloop-l-pair-affine-response-obstruction.md`](h3-axis-target-coloop-l-pair-affine-response-obstruction.md)
cannot be closed by freely adjoining the missing endpoint component

```text
P2:21.
```

If that component is nonzero, its first target-augmented/private
coefficient is the literal word

```text
11111121.
```

At the exact four carrier packets, the selected pure-one matching `L` is
the unique direct-free monomial in this row.  Thus absence of a cancellation
mate is already a localized source unit.  Every possible mate routes after
one source-valid pure-target reselection.  Consequently the unresolved
affine block may be restricted to the literal branch `P2:21=0`.

Checker:
`computations/verify_h3_axis_target_coloop_p2_21_private_row_closure.py`.

## The complete private coefficient

The full eight-site coefficient has `105` physical matchings.  Its `15`
terms containing `PS:21` vanish in the normalized direct-free one-bad
branch, leaving `90` terms.  The selected term is

```text
P2:21 * S3:11 * (the three-factor pure-one L cofactor).
```

After localizing the selected carrier factors and `P2:21`, this monomial is
a unit unless one of the other `89` direct-free matchings is nonzero.
Across the four residual-site mirrors, the `356` alternate slots split as

```text
P-w:21 off the anchor union:       240
P0:21 internal mates:               60
P2:21 same-port internal mates:     56
```

The first class is already a nonanchor off-diagonal endpoint carrier, so
the pinned target-augmented active-minor and deleted-star-rank theorem
applies.

For an internal mate, `w` is `0` or `2`.  The corresponding pure-one cells

```text
P0:11, P2:11
```

are selected.  Replace the mate's single `P-w:21` factor by `P-w:11`.
Every other factor is unchanged and already nonzero, so the same physical
matching is a nonzero pure-one target monomial `L'`.  It is not the old
`L`.  The old two `02` cells lie on the two `L`-only edges; every such `L'`
omits at least one of them (`28` mates omit one and `88` omit both).
Reselecting `L'` therefore makes an already nonzero `02` cell lie outside
`K union L' union M`, which is again the pinned nonanchor route.

This is a literal coefficient argument.  It does not assume an abstract
endpoint column or replace a zero source factor.

## The `R21/R22` typing

The same component does supply both missing response faces on the old
rainbow cofactor:

```text
00112221:  P2:21 * S3:11 * C23,
00112222:  P2:21 * S3:21 * C23.
```

Here

```text
C23 = x01^00*x45^22 + x04^02*x15^02 + x05^02*x14^02.
```

In particular, the second word does **not** use `P2:22,S3:22`: residual
sites `2,3` have colour `1`, so its literal port types are `P2:21,S3:21`.
At exact carrier support, the selected `L` monomial is the only supported
term in each of these two rows.

Thus adding `P2:21` indeed fills `R21` and `R22`, but its pure-one private
row exits to a unit/reselection/nonanchor carrier before an
E2/common-covector/five-lock argument is needed.

## Exact remaining scope

This closes only the branch

```text
P2:21 != 0.
```

It neither forces `P2:21` to be nonzero nor closes the rank-one affine
return when `P2:21=0`.  The original twelve internal affine slots are now
sharpened to that literal zero-face branch; no free opposite endpoint
component remains available there.

Run

```text
python3 computations/verify_h3_axis_target_coloop_p2_21_private_row_closure.py
python3 -O computations/verify_h3_axis_target_coloop_p2_21_private_row_closure.py
python3 -I -S computations/verify_h3_axis_target_coloop_p2_21_private_row_closure.py
```

Frozen ledger SHA-256:

```text
9223046b5bf36dcb3635350fbfbc6fec5e0af85f66f812fd8050eb789ee608d9
```
