# One hybrid anchor row closes all 110 target-coloop label residuals

## Result

The mandatory other-bright matching reduction left exactly

```text
48 residual-q-only records,
50 same-base word-change records,
12 residual-C4 word-change records.
```

All `110` have a common source-labelled feature stronger than their three
separate graph descriptions.  With the normalized ports

```text
M : P0,S1     (pure colour 2),
N : P2,S3     (selected mixed word rho+(1,2)),
K : PS        (pure colour 0 direct anchor),
L : P2,S3     (pure colour 1),
```

the selected mixed matching `N` and the other-bright anchor `L` share the
physical edge

```text
e = S3.
```

Checker:
[`verify_h3_axis_target_coloop_hybrid_anchor_escape.py`](../computations/verify_h3_axis_target_coloop_hybrid_anchor_escape.py).

## The literal hybrid row

The selected `N` cell on `e` is

\[
                         x_e^{2,\rho_3}\ne0,
\]

whereas the selected `L` cell is `x_e^{11}!=0`.  Take the mixed cell on
`e` and the three pure-1 cells on `L\setminus e`.  They form one nonzero
literal matching monomial in the full output word

```text
colour 1 off e, colour 2 at S, colour rho_3 at site 3.
```

This word is mixed for every `rho_3`, so its exact target coefficient is
zero.  Let `B'` be any supported cancellation matching.

If `B'` retains `e`, every other edge of `B'` is labelled `11`.  Replacing
its mixed `e` cell by the already nonzero `x_e^11` gives a literal pure-1
monomial on `B'`.

If `B'` omits `e`, its new `S` partner lies off `e` and therefore has word
colour 1.  Thus `B'` contains a nonzero off-diagonal `21` endpoint cell on
a new physical edge.

The aggregate version removes a cancellation caveat.  If there is no
supported avoiding-`e` term at all, the complete mixed coefficient is

\[
             0=x_e^{2,\rho_3}H_e^1.
\]

Over an integral domain, `H_e^1=0`.  Expanding the normalized pure-1 target
coefficient gives

\[
  1=x_e^{11}H_e^1+
       \sum_{B'\not\ni e}\mu_{B'}(1^8)
    =\sum_{B'\not\ni e}\mu_{B'}(1^8).
\]

Hence a nonzero pure-1 matching `L'` omitting `e` exists.  This conclusion
does not divide by a matching tail and does not assume a support torus.

## Complete routing

For an avoiding mixed mate, the new `S` edge has only three possibilities.

1. Outside `M union K union L`, its nonzero `21` cell enters the pinned
   nonanchor rank-`(3,3)` active-minor route.
2. Inside the selected anchor union, it must be `M`'s edge `S1`; the pinned
   decorated-anchor exchange theorem supplies an avoiding source matching,
   pure-anchor reselection, or a localized unit.
3. The edge `PS` cannot occur in a supported mate: at this hybrid word it
   would require a `12/21` direct cell, while the normalized direct block
   has only its `00` cell.

In the no-avoiding-term branch, replace `L` by the pure-1 matching `L'`
omitting `S3`.  The edge `S3` is also absent from `M` (whose arm is `S1`)
and `K` (whose arm is `SP`).  Therefore the already selected active `N`
arm `S3` is external to all three pure anchors `M,K,L'`; the existing
external-endpoint theorem restores deleted-star rank three and enters the
active route.

Thus none of the `48+50+12` records remains a separate coefficient gate.
The argument uses one full mixed row and one normalized diagonal target
row; it is stronger than the earlier same-base-only hybrid theorem.

## Exact downstream scope

The preceding sentence means that there is no longer a *target-coloop-
specific* label packet.  It does not assert that every decorated `S1:21`
mate is already four-good.

Apply the complete decorated-anchor exchange to `S1:21` relative to the
pure-2 matching `M`.  A dark pure-2 cofactor reselects `M` away from `S1`,
after which the already active `S1` pair is nonanchor and enters the pinned
good-pair route.  In the non-dark branch, a mate leaving the anchor union
does the same.  Triple- and two-shared anchor returns enter the pinned
unary migration and strict Hall closure chain.

The only remaining possibility is the one-shared, anchor-contained,
arbitrary-multisite `M`-port web.  It contains an active
`p_1(0)s_2(1)q^[2]` carrier, but it need not contain an alternate pure-2
port.  The strict `K_{2,2}` unit cannot supply that port: its localization
hypothesis already includes a second pure-2 matching avoiding the coloop
arm.  Thus this case lands exactly on the previously isolated affine
target-line-hitting/anchor-preserving Hall-concentration interface of
`uniform-multisite-endpoint-affine-hall-concentration-boundary.md`.

There is a useful symmetric check, but it does not improve that landing.
The exact finite audit is
`h3-axis-target-coloop-second-endpoint-hybrid.md` (`a7cd5d1`).
The `M`-port mate also contains `P0:11`, while the pure-2 anchor contains
`P0:22`.  The hybrid row using `P0:11` and the three other pure-2 `M`
cells either reselects pure 2 away from `P0`, exposes a nonanchor `12`
endpoint cell, or transfers that cell to the pure-1 arm `P2`.  The `S`
dual transfers `S1:21` to `S3:22`.  Hence the fully anchor-contained
outcome is the two-edge transfer between the `M` ports `P0,S1` and the `L`
ports `P2,S3`.  Proportional one-star transfer columns are deleted by the
anchor-safe minimum-support theorem; nonproportional columns return to the
already pinned common-covector bistar/Fitting carrier.  No alternate
pure-2 port, common literal tail, or strict-chart localization factor is
created by this symmetric row.

Consequently `0556512` removes the target-coloop branch as an independent
topological or coefficient frontier.  The surviving obligation is the
global multisite affine-accessibility lemma: force a target-line point, a
free active carrier, or an anchor-preserving relation in the star/triangle/
rectangle Hall normal forms.  More companion tails through the same
decorated cell do not prove that lemma.

## Finite audit and scope

The checker reconstructs the pinned `4,500` quadruple partition and selects
the `110` residuals.  It verifies that every one has common ports `P2,S3`.
For each record, each of the three possible values of `rho_3`, and all
`104` alternate `K8` matchings, it audits the exhaustive split

```text
retains e / direct-PS forbidden / decorated-M-anchor / nonanchor.
```

This enumeration certifies the h=3 shared-port landing.  The hybrid-row
factorization itself is source-labelled and works at every even order once
the same shared-edge normalization is available.

Run

```text
python3 computations/verify_h3_axis_target_coloop_hybrid_anchor_escape.py
python3 -O computations/verify_h3_axis_target_coloop_hybrid_anchor_escape.py
python3 -I -S computations/verify_h3_axis_target_coloop_hybrid_anchor_escape.py
```

Frozen ledger SHA-256:

```text
7f3ff8ed4139cd7d3156f2c96e34405beaf0354b899cfe112ff0d1a82aeb38fa
```
