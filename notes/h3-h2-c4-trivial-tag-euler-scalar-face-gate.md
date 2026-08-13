# The C4 tag invariant is an annihilator with a centered scalar face

## Exact product-rule calculation

For the representative direction-pair fibre over sites `0,1`, put

\[
 H_{2345}=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.
\]

For the complete 105-occurrence response polynomial `R`, literal second
Hasse differentiation gives

\[
 \partial_D\partial_{q_{01}}R
 =\partial_{p_0}\partial_{s_1}R
 =\partial_{p_1}\partial_{s_0}R
 =H_{2345}.                                           \tag{1}
\]

Consequently the unique direction-tag coinvariant from `d5a5581` satisfies

\[
 (2\partial_D\partial_{q_{01}}
  -\partial_{p_0}\partial_{s_1}
  -\partial_{p_1}\partial_{s_0})R=0.                 \tag{2}
\]

Equation (2) is an exact apolar or Hessian-symbol relation.  It is not yet a
source-algebra boundary.

Checker:
[verify_h3_h2_c4_trivial_tag_euler_scalar_face_gate.py](../computations/verify_h3_h2_c4_trivial_tag_euler_scalar_face_gate.py).

## Integrating the symbol exposes the first proper face

Apply the corresponding logarithmic coordinate projectors.  Their
zero-order lift is

\[
 L_{01}=
 (2Dq_{01}-p_0s_1-p_1s_0),H_{2345}.                 \tag{3}
\]

This has nine distinct occurrence monomials: three have coefficient `2`
and six have coefficient `-1`.  Monomials are a basis of the polynomial
ring, so (3) is nonzero.  It is not proportional to the local response
aggregate, whose nine coefficients are all one.

The target augmentation of (3) is nevertheless zero:

\[
                         3(2-1-1)=0.                 \tag{4}
\]

Thus the first defect is not a new target normal.  It is the target-zero,
occurrence-private scalar face (3).

There is a literal response-row countermodel.  Set

```text
D=q01=q23=q45=p0=1,   s1=-1,
all other displayed variables=0.
```

Only `D q01 q23 q45` and `p0 s1 q23 q45` survive.  Hence

\[
                         R=1-1=0,
 \qquad                 L_{01}=2-(-1)=3.             \tag{5}
\]

This is a countermodel for deduction from the complete response row and its
homogeneity, not a claim that the assignment solves every GHZ equation.

## Why Euler homogeneity does not close it

Give `(D,P,S,Q)` type weights `(a,b,c,d)`.  Direct response monomials have
weight `a+3d`; endpoint monomials have weight `b+c+2d`.  A type Euler field
is homogeneous on the response exactly when

\[
                         a+d=b+c.                    \tag{6}
\]

But the induced weights on the three directions in (1) are

\[
               (a+d,\ b+c,\ b+c),                   \tag{7}
\]

which are constant under (6).  Their pairing with `(2,-1,-1)` is zero.
Site Euler fields are even more rigid: every response occurrence covers all
six sites once, so they also act by one common character.  Iterating such
physical homogeneous Euler fields cannot select (3).

The raw coordinate Euler projectors do select (3), but (5) proves they do
not preserve the response ideal.  Calling (2) an Euler boundary would omit
exactly this scalar proper face.

## Relation to the pointed occurrence theorem

Let `v_01` be the coefficient vector of (3) in the complete
105-occurrence response coordinate space.  Equation (4) says

\[
              \mathbf1^Tv_{01}=0,
 \qquad       (105I-J)v_{01}=105v_{01}.               \tag{8}
\]

So the C4 tag survivor is not a new scalar species: it is the selected
second-Hasse face of a centered occurrence comparison.  A primitive local
dual is `v_01/18`, since the squared coefficient norm is
`3*(2^2+1+1)=18`.

This is a statement about the **schema**, not an already constructed
physical column.  The known mixed-word pointed comparison used a specific
occurrence block; (3) still has to be placed in its literal response word,
fine grade, and `Hasse[2]` direction-pair object.

There are also two different invariant factors that must not be conflated:

```text
direction factor   2 e_DQ - e_PS01 - e_PS10,
tail factor        q23*q45 + q24*q35 + q25*q34.
```

Their tensor product is (3).  The previously isolated generic symmetric
lower-C4 placement concerns the tail factor in a fixed direction grade;
(2) couples the three direction grades and introduces the scalar face.

## Exact terminal promotion

Once (3) is placed in an exhaustive physical map with its literal
word/fine/direction and repeated grade, `4373ae6` extends its local dual
through all known `q/ainc/target/W/ores/ridge` rows.  Exact duality then has
only two branches:

1. a protected-zero physical filler for the centered occurrence face; or
2. an accepted augmented terminal detecting it.

There is no third branch.  This promotion is conditional on same-grade
placement; the coefficient dual `v_01/18` is not by itself a physical
terminal.

## Frontier change

Homogeneity does not eliminate the sole C4 tag coinvariant.  It identifies
its first missing datum much more tightly: a pointed occurrence/AugP2
comparison for the nine-term target-zero scalar (3).  Thus the surviving
C4 direction line should be built as a face of the pointed occurrence
schema, not as an unrelated third lower theory.  It remains distinct from
the downstream `P2` word-`0102` private landing.

The checker was run normally, optimized, and isolated/no-site.  Its frozen
ledger digest is recorded in the checker.
