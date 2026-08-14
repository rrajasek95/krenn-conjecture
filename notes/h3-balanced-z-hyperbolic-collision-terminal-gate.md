# The collision first faces preserve the balanced terminal; the two returns fill it

## Exact verdict

The corrected pure-safe `z` dual from `037ac9f` extends through all four
first faces of the hyperbolic root-return construction and through every
currently known cap/Cartan image.  The normalized value on each collision
coordinate is zero.  The four first faces therefore do **not** provide the
desired filler.

The two second-step returns are decisive.  In chart coordinates

\[
 A=Dq_{01}H,\qquad B=p_0s_1H,\qquad C=p_1s_0H,
\]

they are

\[
 r_1=A-B,\qquad r_2=A-C,
 \qquad z=r_1+r_2=2A-B-C.                         \tag{1}
\]

The normalized direction covector is

\[
                 \psi=(2,-1,-1)/6.
\]

Consequently

\[
 \psi(F_{01})=\psi(F_{10})=\psi(F_{02})=\psi(F_{20})=0,
 \quad \psi(r_1)=\psi(r_2)=\tfrac12,
 \quad \psi(z)=1.                                  \tag{2}
\]

Thus one return breaks this particular covector but does not fill `z`; both
returns are necessary and sufficient to fill it.  This is exactly the pair
of mixed physical chart arrows isolated in `037ac9f`.

Exact checker:
[`verify_h3_balanced_z_hyperbolic_collision_terminal_gate.py`](../computations/verify_h3_balanced_z_hyperbolic_collision_terminal_gate.py).

## Rank calculation

In the seven-coordinate operation quotient

```text
(A,B,C,F01,F10,F02,F20),
```

the complete response has rank one.  The four collision faces are private
pivots.  The exact ranks are

| admitted columns | rank | rank after adjoining `z` |
|---|---:|---:|
| complete response + four first faces | 5 | 6 |
| the preceding + only `A-B` | 6 | 7 |
| the preceding + only `A-C` | 6 | 7 |
| the preceding + both returns | 7 | 7 |

The same conclusion holds in the complete four-word direction quotient,
not just in the three-coordinate shadow.  The tag-preserving root edges and
four complete-response rows have rank `10`.  After adjoining four private
collision coordinates the rank is `14`, and `z` raises it to `15`.  One
return gives ranks `15 -> 16` after `z`; both returns give `16 -> 16`.

This distinction matters.  Independence of a collision monomial from the
old squarefree chart space raises the ambient/source rank in a new
coordinate, but it cannot lower the old `z` cokernel rank.  A filler appears
only when a source relation cancels the private collision coordinates and
leaves the pure chart returns (1).

## Corrected cap/Cartan extension

The normalized pure-safe augmented covector has signature

```text
B       = ( 1/4,  1/4, -1/4, -1/4)
Eq      = (   0,    0,  1/4,  1/4)
target  = (-1/4, -1/4,    0,    0)
W       = (-1/4, -1/4,    0,    0)
ores    = ( 1/4,  1/4,    0,    0)
M, ainc, q, P_f, ridge, eta, sigma = 0.
```

It annihilates the complete known `r0_j,T_j,rho_j,K` packet and both pure
target columns.  Their rank is `15`, while adjoining `z` gives `16`.

As the strongest harmless collision stress test, graph the four private
collision coordinates over the four complete `r0_j` images, retaining all
`T/rho/K` and pure-target columns.  The rank becomes `19`, and adjoining
`z` gives `20`.  Extending the covector by zero on the four private
coordinates kills every graph column.  The same statement holds if a graph
tail is any linear combination of the known augmented columns.

This test deliberately uses complete `r0` images.  A bare cap corner `B_j`
is not a source column; replacing `r0_j` by `B_j` would discard its Eq,
target and anchor faces and would manufacture a false nonzero pairing.

## Why this is not yet a physical filler

The coefficient identity (1) is exact, and the local response now has a
literal `K4` Pfaffian origin.  What is still absent is the source-labelled
totalization that makes both second-step returns actual columns of the full
decorated source complex.

The committed collision packet lies in response word

```text
11:110000,
```

whereas the canonical cap packet lies in word

```text
01211222.
```

They differ at six augmented sites.  No existing `D4` response cube supplies
that word/fine map.  Even after formally granting it, the packaging quotient
has ranks

```text
2  ->  3  ->  4
lower+Eq    mixed incidence    labelled shifted ridge,
```

so the collision lower face does not itself provide the mixed reduced-Eq
cap descent or the shifted Kähler face.

Therefore the exact fork is:

1. On the currently constructed literal packet, the corrected terminal
   survives the four collision first faces and all old augmented tails.
2. If one constructs a single physical two-root collision mapping
   bicomplex containing both returns, all four first faces, the word/fine
   transport, reduced-Eq cap incidence and labelled shifted ridge, then the
   two return columns fill `z` exactly by (1).

There is no license to adjoin the pure returns before that totalization:
doing so assumes the missing physical source chain map.

## Scope

This is exact for the canonical `h=3` operation packet, the complete
four-word direction quotient, and the committed cap/Cartan and collision
packaging interfaces.  It is neither a constructed full decorated GHZ
source cell nor an all-`h` terminal theorem.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
8775723e36bd54f9a729ca313cc97efc42f69d77e5afe03fd4ea6949bf3126dd
```
