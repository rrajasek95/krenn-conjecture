# The moving-target fourth-Hasse cone removes the fixed-fibre unit defect

## Result

The proposed orbit-relative construction genuinely evades the old
source-valid-tower no-go.  Let the four roots `0 -> 1` act at residual sites
`2,3,4,5`, and move the GHZ target along with the response equation.  The
target coefficients along the five Hasse orders are

```text
0, 0, 0, 0, 1.
```

Hence the fixed-fibre identity

\[
 D_4G_{110000}=G_{111111}=F_{111111}+1
\]

is replaced over the target orbit by

\[
 \boxed{D_4(G_{110000}-\Delta(t))
        =G_{111111}-1=F_{111111}.}                 \tag{1}
\]

The troublesome unit is exactly the fourth coefficient of the moving
affine target normal.  It is not discarded; it is retained as a mapping-cone
face.  Thus the earlier no-go for an endomorphism preserving the *fixed*
ideal does not apply to this relative family.

Checker:
[`verify_h3_e14_orbit_relative_d4_target_cone_gate.py`](../computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py).

## The complete four-root packet is canonical

The sixteen word vertices have order profile

```text
1, 4, 6, 4, 1
```

from `110000` to `111111`.  Their signed Boolean/Koszul differentials have
ranks

```text
1, 3, 3, 1
```

and consecutive products are zero.  The complex is exact in every proper
degree; in particular the top target coefficient has a primitive preimage.
Therefore the fourteen intermediate Hasse faces are one canonical
totalization, not fourteen new construction theorems.

Every word has the same ninety endpoint/matching occurrence tags, and each
root preserves the tag with coefficient one.  For the marked tag

```text
p@0:1, s@1:1, residual matching 24|35,
```

the bottom and top monomials are

```text
(p1_0_1*s1_1_1)q24_00*q35_00,
(p1_0_1*s1_1_1)q24_11*q35_11 = g.
```

Thus the centered profile `(89,-1)` is constant over the cube and formally

\[
                         D_4(c_f)=c_g.               \tag{2}
\]

This is the promised positive word transport at the orbit-relative level.

## What orbit covariance does not construct

Equation (2) starts from a physical centered occurrence section.  That base
cell is still open: the committed same-grade calculation proves that the
old complete response/stabilizer image contains only the total occurrence
sum, not `c_f`.  Equivalently the pointed comparison still needs the
separate conormal

\[
                         dP_f=u_f-u.                  \tag{3}

The orbit cube transports a supplied `(c_f,P_f)` section; it does not create
the bottom section or make (3) a boundary in the original source.

There is a second typing qualification.  At normalized cap parameter the
old graph cycle is

```text
           Yw  target  Q  ores
T+rho       0     +1   0   +1.
```

It exactly supplies the target/cap normalization left by isolating `g` from
`c_g`, so no new coarse scalar direction is needed.  But its committed
physical word/fine/repeated grade is

```text
01211222 / t*q_(v,N) / P3+K2,
```

whereas the orbit top lies in `G11[111111]` and then the E14 unary word
`000101`.  Making `T+rho` a horizontal source-labelled cap local system over
the four-root orbit is still a comparison clause; equality of its projected
target/residue numbers is not that clause.

## The first literal proper face after the two grants

Grant the pointed base section (3) and the horizontal cap graph.  The
Boolean totalization then lands on the normalized `+g` top face.  On the
silent branch `v04=0`, the complete unary row is

\[
 v_{24}^{11}U_{000101}=-g+T_{12}.                    \tag{4}

Adding (4) cancels the private occurrence and leaves

\[
                         (+g)+(-g+T_{12})=T_{12}.     \tag{5}

This is the exact first `d^2` proper face.  It is the full packet of twelve
word-resolved unary-times-`q` tails—ten cubic and two quartic monomials—not
only `(H0-u)e_Eq` or another projected Eq shadow.  The complete 269-column
first-hit image has rank 269, reduces `T_12` back to `R_E14`, and a primitive
integral dual pairs `-30`.  Hence the current physical inventory does not
fill (5).

## Shortest positive theorem

It is enough to construct:

1. one pointed source-labelled centered occurrence section at the `110000`
   base vertex;
2. one horizontal copy of the old cap graph over the moving target orbit;
3. one companion homotopy for the literal `T_12` face.

The canonical Boolean PP/Koszul cube then handles all root faces and the
moving affine target normal automatically.  This is a strict improvement:
the fixed-target `+1` defect and fourteen separate-face search disappear.
The remaining objects are physically graded comparison data, not another
abstract fourth-Hasse operator.

## Scope

This is exact for canonical `h=3`, chart `(1,1)`, the four residual root
sites, and the silent `v04=0` E14 branch.  It proves the orbit-relative
target repair, not the missing pointed/cap descent or the `T_12` companion.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
9a056dff4e63821841f07e752a3c1e01ebb857f902a9331299959e0fe6aea76b
```
