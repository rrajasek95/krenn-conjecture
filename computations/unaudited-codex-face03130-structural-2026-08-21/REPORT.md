# k5 face `0:31:30`: exact structural reverse interface

Status: **UNAUDITED exact source rebuild and two-row elimination; no ideal
solve and no emptiness claim.**

## Outcome

The frozen routing key has been rebuilt source-faithfully.  In edge order
`01,02,03,12,13,23`, state `0:31:30` means:

- selected offdiagonal terms on edges `0,1,2,3,4` and the selected diagonal
  term on edge `5`;
- both permanent terms live on the four-cycle edges `1,2,3,4`;
- the lossless site-torus gauge `b0=b1=b2=d1=1`.

The normalized chart has 12 active variables

```text
a0,a1,a2,a3,a4,a5,b3,b4,b5,d2,d3,d4
```

and all 16 nonpermanent literal source rows survive.

The shortest literal row is raw 20, `cofactor_5_0`, the ten-term cubic

```text
a0*d2*d3 + a0*d4 + b3*d2 + b3*d4 + b4*d3 + b4
  + d2 - d3 - d4 + 1.
```

It is linear in `a0,b3,b4,d2,d3,d4`.  Its cheapest solve coefficient is
`d2+d4` for `b3` (equally, `d3+1` gives a small `b4` split).  Thus a direct
reverse attack can split on `d2+d4`; the closed side retains the explicit
eight-term residual rather than silently dividing.

## Smallest literal omitted-cofactor packet

An exact census of fraction-free common-linear-variable eliminations from
the eight shortest rows against all literal cofactor rows found a smaller
global packet than the raw-20 solve.  Let

```text
f = raw7  = t_013     = A*a4 + B,
g = raw16 = Cof(3,0)  = C*a4 + D,

A = -a0*d2*d4 + b4*d2 + d4,
C = -a5*d2*d4 - a5*d4 + d4.
```

Literal expansion proves

```text
A*g - C*f = -b4*R25,
```

where `R25` is the stored irreducible 25-term degree-six polynomial.  The
original selected-base localizer makes `b4` live, so every point of this
chart satisfies `R25=0`.  No division by `A` was made.

This gives the smallest frozen reverse split:

1. `A != 0`: solve `a4=-B/A`, retain `R25=0`, and restore the other fourteen
   literal source rows and every original live factor;
2. `A = 0`: retain the literal residual `B=0` and the full remaining source
   packet.  This branch is not covered by the open solve.

The smallest packet forced to use the absolute shortest row is raw20 with
raw11 (`Cof(0,3)`), eliminating `b4`; its coefficient is `d3+1` and its
primitive resultant is an irreducible 32-term degree-five polynomial.  It is
therefore a useful alternate branch but not the smallest resultant overall.

## Controls and artifacts

`audit_face03130_reverse_interface.py` independently imports the frozen raw
endpoint-ordered generator, rebuilds the chart, verifies the routing masks,
profiles all rows, and replays the selected sparse identity literally.  A
single-coefficient mutation is required to break the identity.

Three execution modes give the same standard logical digest:

```text
standard  96052061416f3e47eb5d2b051ba92f3e6d2f34d7bdc2198778697ba7670418ba
-O        96052061416f3e47eb5d2b051ba92f3e6d2f34d7bdc2198778697ba7670418ba
-I -S     96052061416f3e47eb5d2b051ba92f3e6d2f34d7bdc2198778697ba7670418ba
mutation  9725d9d0488341b95a36041df28ae8bbf4bb60b4d9e5a25537465bc04a87d418
```

Stable file SHA-256 values:

```text
audit_face03130_reverse_interface.py
  8fc8331a646837d4280e46caf77b6a195475650d5a48f048932ae5aef49aa2ef
results_face03130_reverse_interface_standard.json
  d169384a8ffc6a63f3ac5a3f76af9a02e28badb7b2d309eaeb552c51ddf74af1
results_face03130_reverse_interface_mutation.json
  401274775542766b6fba14409d7741a8e53edb8e0538f2d4944852a84e5ceede
```

## Scope guard

This package proves only exact necessary source identities and exposes a
bounded pivot split.  It does not prove either branch empty.  A future
`A!=0` certificate must replay all source rows after denominator clearing;
an `A=0` certificate must not invert `A`.  Likewise, using the remaining
`c`-numerator localizer concerns only this face's interior and does not cover
the routed descendant `0:15:13`.

## A-open follow-up

The exact `A!=0` substitution, all fifteen reduced source rows, every
transported live factor, the eight-smallest-row core, and the bounded solver
ledger are frozen in
`../unaudited-codex-face03130-aopen-char0-2026-08-21/REPORT.md`.  No unit or
component sentinel landed within the declared caps, so the branch remains
open.  Exact profiling shows that the natural raw16/`a2` and raw20/`b3`
second pivots inflate the largest row/live packets to `262/735` and
`425/1103` terms; future work should use a component/slice or an alternate
sparse row combination instead.  A subsequent deterministic affine-slice
screen at depths one through three, using core8 and exact base-live F4SAT
saturation, also timed out at 120 seconds per depth before producing a
basis.  Thus no component signature or finite residual is yet available;
the next route must change the component representation or source
restriction rather than add more slices to this presentation.
