# The conditional E14 private placement leaves exactly root-decorated `d_even`

## Result

The proposed placement is coefficient-exact.  Put

\[
 H_0-u\longmapsto1-v_{04}^{00},\qquad
 e_{\rm Eq}\longmapsto
 (p_{1,0}^1s_{1,1}^1)u_{35}^{11}v_{24}^{11}.
\]

Its image is the canonical private return

\[
 R_{E14}=(p_{1,0}^1s_{1,1}^1)
 u_{35}^{11}v_{24}^{11}(1-v_{04}^{00}).
\]

The exact sparse identity

\[
                         B_{E14}=U+R_{E14}
\]

then says that the old word-`000101` unary column `U` plus the placed return
is the full E14 target, including the visible
`u05_01*v13_01*v24_11` companion.  No target-normal remainder survives this
conditional placement.

The remaining ordinary residue is

\[
 \boxed{-E=-2D_{\rm root}\otimes d_{\rm even}},\qquad
 D_{\rm root}=(-1,1,-1,1),\quad
 d_{\rm even}={B_1+B_4\over2}.
\]

Thus it is exactly the root decoration of the already isolated `d_even`
direction, not `z_cap` and not a fourth residue source type.

Checker:
[`verify_h3_e14_keq_private_placement_residue_identification_gate.py`](../computations/verify_h3_e14_keq_private_placement_residue_identification_gate.py).

## The E14 identity

For the pinned target, unary column, and 22-support covector,

```text
lambda(U)       =  0,
lambda(R_E14)   = -1,
lambda(B_E14)   = -1,
B_E14           = U + R_E14.
```

The companion occurs with coefficient `-1` in both `U` and `B_E14` and does
not occur in `R_E14`.  The private placement therefore does not manufacture
the companion; it supplies the return which lets the already physical unary
column survive as the complete target boundary.

This remains conditional on source provenance.  The central Eq object and
the E14 occurrence object are different physical source summands until the
pointed `P2/iota` comparison constructs the displayed map.

## Exact residue identification

In the four root-word copies and six pure-label coordinates, put

```text
E = 2 D_root tensor d_even.
```

It has eight nonzero coefficients, all `+1` or `-1`.  The nearest physical
`K_Eq` dressing has

```text
(lower/private, Eq, word-resolved ores)=(+E,+E,-E).
```

The conditional `P2` placement supplies hidden lower `-E`, and the pure
section `d_even`, decorated by `2D_root`, supplies word-resolved residue
`+E`.  Hence

\[
 (-E,0,0)+(E,E,-E)+(0,0,E)=(0,E,0),
\]

the clean `K_Eq` face.  The root-residue debt is therefore closed exactly.

This statement must be read at full word resolution.  Summing the four root
words sends `-E` to zero because `sum(D_root)=0`; that coarse vanishing does
not construct its physical cancellation.

## Why `z_cap` is different

Keep three residue blocks separately:

```text
24 word-resolved root-label residues,
 6 unrooted B-label residues,
 1 scalar cap residue.
```

The rooted `d_even`, unrooted `d_even`, and `z_cap` directions have rank
three in this direct sum.  Only rooted `d_even` cancels `-E`.

`z_cap` is the scalar cap-grade class left by primitive-cap reduction.  It
has zero value on all 24 root-word residue coordinates.  Conversely the
scalar cap covector kills both versions of `d_even` and reads one on
`z_cap`.  Therefore the two obligations cannot be merged:

- rooted `d_even` cancels the E14/`K_Eq` word-resolved residue;
- `z_cap` still supplies the independent primitive-cap scalar landing.

The unrooted `d_even` copy also supplies the prescribed ordinary residue
`v=(B1+B4)/2` of the full generic carrier, but without root decoration it
does not cancel `-E`.

## Physical status

There is no new coefficient direction beyond `d_even`, but the conclusion is
not yet unconditional.  It requires a same-grade pure protected-zero
`d_even` source section stable under the connected root decoration.  The
committed Cartan-parity inventory does not construct that section; its
primitive fixed-plane dual survives.  The existing `P2` residue theorem also
uses pure `d_even` as a hypothesis.

Consequently the shortest remaining source statement is the joint pointed
placement which:

1. realizes the occurrence map to `R_E14` in every needed root/label copy;
2. transports the pure `d_even` section into the same word/fine/repeated
   grade and permits the `2D_root` decoration; and
3. separately lands the scalar `z_cap` class and terminal faces.

## Scope

This is exact for the canonical `h=3`, word-`000101` first-hit packet and
the eight nonzero root/label components of the generic `C+` dressing.  It
does not construct the source-labelled occurrence map, pure `d_even`, its
root decoration, `z_cap`, or the remaining terminal comparison.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
c4f7850fc66736cc5494131c67ee510483d4898f46330e2904c0a602a2f4d160
```
