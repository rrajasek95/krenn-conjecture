# Full-site tag contraction has one pointed chart proper face

## Coefficient theorem: confirmed

The rank calculation in `df8c061` is correct.  With two response endpoints
`P,S` and residual sites `0,...,5`, the dictionary

```text
d = PS,       p_i = Pi,       s_i = Si,       q_ij = ij
```

identifies the 105 response occurrences with all perfect matchings of
`K8`.  Hence the response polynomial is covariant under `S8`.  The checker
reconstructs all 105 matchings independently and verifies the action
literally.

For the representative four-set `{P,S,0,1}`, write

\[
 A=Dq_{01},\qquad B=p_0s_1,\qquad C=p_1s_0.           \tag{1}
\]

The physical-site transposition `sigma=(P 0)` acts by

\[
                         A\leftrightarrow C,
 \qquad                  B\mapsto B.                 \tag{2}
\]

Together with a second transposition exchanging `A,B`, the raw action
relations span the full centered plane.  In particular

\[
             2A-B-C=-(B-A)-(C-A).                    \tag{3}
\]

This independently confirms why full `S8` raises the tag-action rank from
139 to 140.

Checker:
[verify_h3_h2_full_site_chart_swap_pointed_scalar_guard.py](../computations/verify_h3_h2_full_site_chart_swap_pointed_scalar_guard.py).

## Why this is not yet a physical boundary

The transposition in (2) is a source-algebra isomorphism **between response
chart objects**.  There are two inequivalent ways to turn its groupoid edge
into a putative fixed-source boundary.

1. Retain the chart label and compare the moved endpoint by the inverse
   chart identification.  Since `sigma^2=1`, every tag returns to itself and
   the boundary is zero.
2. Forget the object label and fold both charts into one coordinate space.
   Then the boundary is `e_(sigma tag)-e_tag`, as used in (3), but this adds
   the equations `A=B=C` to the fixed source.

The rank loss is explicit.  With only the local response equation
`A+B+C=0`, the quotient has dimension two.  Adding the two raw action
relations makes the coefficient matrix rank three and the quotient
dimension zero.  The smallest presentation-preserving graph cone instead
uses

\[
 db_1=(B-A)-u_1,\qquad db_2=(C-A)-u_2.                \tag{4}
\]

On coordinates `(A,B,C,u1,u2)`, the response row and (4) have rank three,
so the quotient remains two-dimensional.  The graph coordinates record the
proper faces that raw chart folding deletes.

This is the same retained-label versus raw-fold distinction already seen in
the pointed Maschke occurrence audit.  A finite-group coefficient action is
not automatically a homotopy inside a fixed source fibre.

## Word, fine grade, and target

The checker exhausts all `3^8=6561` ternary words under `(P 0)`:

```text
word fixed       2187
word changed     4374.
```

For example,

```text
00000011  ->  10000001
```

in site order `0,1,2,3,4,5,P,S`.  Hence two thirds of the chart edges are
literal cross-word comparisons.  On the remaining third, the word is fixed
but the direction-pair grade still changes

```text
Hasse[2](D,q01)  ->  Hasse[2](p1,s0).
```

Thus equality of Hasse order and of the squarefree four-set does not give
equality of the fine/direction grade.  For this representative swap the
complementary `2345` matching tail is fixed.

The GHZ target is invariant under every physical-site permutation; this is
verified on every ternary word.  Therefore the chart swap has target defect
zero.  Its obstruction occurs before target correction, in the pointed
source comparison.

## The first proper face is exactly `L01`

The additive C4 Euler audit `0d14815` identifies the graph coordinate needed
on the surviving direction line.  The integrated scalar is

\[
 L_{01}=(2Dq_{01}-p_0s_1-p_1s_0)
        (q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}).     \tag{5}
\]

It has nine occurrence monomials, coefficient profile `3 x 2` and
`6 x (-1)`, and occurrence augmentation zero.  Its second-Hasse symbol is
exactly `2e_DQ-e_PS01-e_PS10`.  A literal response-row specialization has

\[
                              R=0,\qquad L_{01}=3,    \tag{6}
\]

so (5) cannot be omitted as an Euler consequence.  On the single surviving
line, the presentation-safe chart cylinder has the schematic boundary

\[
                         d\epsilon_{01}=L_{01}-u_{01}.
                                                               \tag{7}
\]

Equation (7), with word/fine/direction labels retained, is the exact first
missing physical datum behind the full-`S8` contraction.

## Augmented promotion

Before (7) is placed, the cap-specific anchor, physical-`q`, ridge, and
eta/sigma rows are not typed by coefficient covariance.  After literal
same-grade placement, `4373ae6` extends the local dual through the known
`q/ainc/target/W/ores/ridge` packet and gives exactly

```text
protected-zero physical filler
or
accepted augmented terminal.
```

There is no third branch.

## Correct scope of `df8c061`

`df8c061` removes the C4 tag as an independent **coefficient invariant**.
Physically, it gives a conditional reduction:

> a pointed, termwise endpoint-chart PP cylinder carrying (5) makes the
> full-site action contraction valid; failure of its protected filler then
> terminalizes.

It does not supply that cylinder merely from `S8` covariance.  The
downstream `P2` word-`0102` private carrier remains a separate proper face.

The checker runs normally, optimized, and isolated/no-site.  Its frozen
ledger digest is recorded in the checker.
