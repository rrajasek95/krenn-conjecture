# The cyclic comparison package is not an absolute matching cycle

## Exact obstruction

Order the five clean-(C_5) comparison vertices by deleted sites
((1,3,5,2,4)).  Their internal degrees are

\[
 (g_1,g_3,g_5,g_2,g_4)=(bd,ad,ac,ce,be).
\]

The first common homogeneous degree is (M=abcde), and the proposed
cyclic comparison boundary is

\[
 A=ace,C_1+bce,C_3+bde,C_5+abd,C_2+acd,C_4.       \tag{1}
\]

In the literal matching-base presentation the lower differential is
(d_0(C_v)=g_v).  Therefore

\[
                 \boxed{d_0A=5abcde.}                  \tag{2}
\]

Over characteristic zero, (1) is not an absolute cycle.  Consequently it
cannot be the boundary of any honest incidence, Pluecker, matching-square,
Hasse, or Bianchi cell in the existing source complex: every such boundary
lies in \(\ker d_0\) by \(d^2=0\).  The checker replays this on all five
cubic matching-base syzygies and on the existing degree-five Tate top.
The latter has boundary in the **edge** module and its next differential is
zero; it cannot be relabelled as (1).

This is the geometric reason that the tempting matching square does not
construct (G_{v,N}).  A four-endpoint switch can change the matching
presentation, but if it is source-valid its crossed faces form an ordinary
syzygy and have zero lower augmentation.  They cannot leave (2).

## What a relative construction must add

A relative/mapping-cone construction is possible only after adjoining a
new lower degree-(M) augmentation (U_M) with

\[
                        d_0U_M=M.                      \tag{3}
\]

Then (A-5U_M) is a cycle.  Equivalently, before cyclic packaging one may
adjoin a single primitive comparison vertex and propagate it with the four
existing incidence edges.  Equation (3) is not supplied by a matching
square; it is precisely new relative source data.  Physically it must retain
the labelled repeated (P_3\sqcup K_2) matching, endpoint word, chart
sector, and the zero readouts

\[
       (W,\operatorname{tgt},\operatorname{ores},
          \operatorname{ainc})=(0,0,0,0).              \tag{4}
\]

The current pure-anchor and repeated-site identities do not qualify: their
anchor incidence is accompanied by a physical target, while (4) requires
both to vanish.  Thus (2) is an exact first obstruction, not an all-relative-
resolution no-go.

## The surviving dual is not yet the Macaulay annihilator

After Laurent normalization, the five adjacent comparison squares are the
oriented incidence columns of (C_5).  The primitive abstract cokernel
functional is

\[
                         \epsilon=(1,1,1,1,1).         \tag{5}
\]

It kills every incidence/matching-square boundary.  This does **not** let
one bypass (G_{v,N}) by declaring (5) to be the terminal annihilator.
For the exact physical target-stabilizer tangents \(\eta_z\), all current
matching-companion (Q_{v,N}) and rootless-ridge readouts vanish, whereas

\[
 d\Omega_v(\eta_z)=
 \begin{cases}
 -1,&v\ne z,\\
 -1-u_z/t,&v=z.
 \end{cases}
\]

Hence the pullback of (5) is

\[
                         -5-u_z/t\ne0.                 \tag{6}
\]

So (5) is only a dual on the abstract comparison quotient, not on the
physical terminal quotient.  It fails zero indeterminacy.  A physical
extension must supply rootless value (5+u_z/t), exactly the comparison
law already isolated for (G_{v,N}).  The Fredholm alternative applies
only after that source-labelled comparison (and the physical cap/readout
landing) defines the map in the augmented quotient.

## Scope

This proves a source-complex no-go for constructing the cyclic package from
ordinary incidence/Pluecker/matching-square cells and a sharp no-go for
promoting its abstract dual without the comparison.  It does not exclude a
new relative generator with (3)--(4), nor construct the subsequent physical
cap correction.

Run:

```text
python3 computations/verify_h3_rootless_abcde_relative_matching_cell_obstruction.py
python3 -O computations/verify_h3_rootless_abcde_relative_matching_cell_obstruction.py
python3 -I -S computations/verify_h3_rootless_abcde_relative_matching_cell_obstruction.py
```

Frozen ledger SHA-256:

```text
d2f5e5c0b43319c03b48ae757edf97c17f31a50e1d69c976832763169dcdf789
```
