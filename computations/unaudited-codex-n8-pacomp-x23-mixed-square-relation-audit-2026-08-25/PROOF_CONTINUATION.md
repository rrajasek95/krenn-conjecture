# The primitive mixed-square formula is forced, but its physical filler is new

Status: **FORMULA AND SIGNS PROVED AT h=3; EXISTENCE NOT DERIVABLE FROM THE PINNED SQUARE/CUBE INVENTORY**.

The parent is the sealed X23 minimal-extension package, manifest SHA-256
`a13d2a726e1440e2f6406913adcd2c6674e7d9d3a5677e2c1d56031e9d7a1e24`.
No numerical membership solve is used here.

## Theorem (conditional mixed-square boundary)

Fix a cut `c` in `{23,45}` and an operation-root label `rho` in `{AB,AC}`.
Assume the pinned four objectwise arrows form an oriented physical square:

```text
response-left  -- P_f,c^rho -->       response-right
     | K_Eq,L,c^rho                         | K_Eq,R,c^rho
     v                                      v
cap-left       -- D4_c^rho -->          cap-right.
```

If `kappa_c^rho` is the oriented square cell, then the pinned cubical
differential forces

\[
 d\kappa_c^\rho=P_{f,c}^\rho-K_{Eq,L,c}^\rho
                 +K_{Eq,R,c}^\rho-D_{4,c}^\rho.       \tag{1}
\]

Thus the signs in (1) are a theorem from the boundary convention, not an
independent choice.  The existence of the physical, source-labelled
`kappa_c^rho` is not a theorem from the currently pinned grammar.

## Term-by-term sign expansion

Order the vertices as `(response-left, response-right, cap-left,
cap-right)`.  The four oriented edge boundaries are

\[
\begin{aligned}
 dP_f       &=(-1,+1,0,0),\\
 dK_{Eq,L}  &=(-1,0,+1,0),\\
 dK_{Eq,R}  &=(0,-1,0,+1),\\
 dD_4       &=(0,0,-1,+1).
\end{aligned}
\]

For horizontal degree-one edge `e_x` and vertical degree-one edge `e_y`,
the product convention is

\[
d(e_x\times e_y)=d(e_x)\times e_y-e_x\times d(e_y).
\]

The first term gives `right-left`; the second gives `bottom-top`.
Reordering the faces into the pinned edge order therefore gives

```text
bottom - left + right - top
= P_f - K_Eq,L + K_Eq,R - D4.
```

Applying `d` once more cancels at each vertex:

\[
(-1,1,0,0)-(-1,0,1,0)+(0,-1,0,1)-(0,0,-1,1)=0. \tag{2}
\]

Equation (2) is the exact content supplied by the objectwise commutative
square: the four-edge expression is a cycle.  It does not assert that the
cycle has a two-cell preimage.

## Primitive obstruction

Let an integral one-chain have coefficients `(a,b,c,d)` in edge order
`(P_f,K_Eq,L,K_Eq,R,D4)`.  The first three vertex equations for it to be
closed give

```text
b=-a,  c=a,  d=-a;
```

the fourth then vanishes automatically.  Hence

\[
\ker d_1=\mathbb Z(1,-1,1,-1).                    \tag{3}
\]

The generator is primitive.  The edge boundary matrix has rank three.  In
the pinned selected physical grade there is no response-to-cap mixed
two-cell column, so `im(d_2)=0` there and

\[
H_1\cong\mathbb Z,\qquad [P_f-K_L+K_R-D_4]\ne0.   \tag{4}
\]

Adjoining one unit cell with boundary (1) kills (4).  Adjoining a multiple
would leave integral torsion, so the coefficient must be `+/-1`.

## AB and AC are separate labelled instances

The pinned receiving-section quotient has two independent operation-root
coordinates.  Consequently (1) must be checked literally as

\[
\begin{aligned}
d\kappa_c^{AB}&=P_{f,c}^{AB}-K_{L,c}^{AB}+K_{R,c}^{AB}-D_{4,c}^{AB},\\
d\kappa_c^{AC}&=P_{f,c}^{AC}-K_{L,c}^{AC}+K_{R,c}^{AC}-D_{4,c}^{AC}.
\end{aligned}                                                   \tag{5}
\]

The degree-zero root transport sends every displayed AB edge to its AC
edge with coefficient `+1`, so applying it to the first equation yields the
second equation *if the root-natural schema has been supplied*.  This does
not reduce the old source obligation to one unlabelled cell: the two
labelled cycles have rank two, while their root-forgetting sum has rank one.

For the cut involution, the site map sends `B1` to `B4`, while the root map
sends `D_root=(-1,1,-1,1)` to `-D_root`.  Therefore each complete labelled
edge packet changes sign and

\[
 \sigma z_{23}^{\rho}=-z_{45}^{\rho}.              \tag{6}
\]

The normalized covariance `sigma(kappa_23^rho)=-kappa_45^rho` is exactly
compatible with (1), since `d` commutes with `sigma`.  The plus sign on the
underlying decorated `q23 -> q45` monomial remains separate from the minus
sign in the root/pure packet.

## Why existing square and cube identities do not derive existence

The pinned inventories establish all of the following in the selected
off-diagonal response-to-cap mixed grade:

1. objectwise `P_f`, `K_Eq`, and `D4` arrows supply the four edges;
2. the four-edge cycle has `d^2=0`, target value zero, and Eq-augmentation
   value zero;
3. the callable physical registry has zero literal `kappa` columns;
4. its source-derived free closure, even after the canonical relative
   Koszul/Tate enlargement, still has zero operation-changing `kappa`
   columns;
5. the 1,020 deleted-factor squares, nine ambiguous-lcm cylinders, and
   existing ordinary cubes have zero projection to this mixed-incidence
   coordinate.

A cube relation cannot evade this obstruction.  Its boundary is a sum of
square faces.  To make (1) a consequence, at least one of those faces must
have the selected physical response-to-cap mixed-square projection.  The
pinned registry/census says precisely that no such face is present.  The
existing cube identities therefore prove further compatibilities among
zero-projection faces; they do not manufacture the missing two-cell.

There is a useful conditional positive statement.  If one first adjoins a
normalized physical `Phi_KS,r0` and identifies its interchange cell with the
standard cubical/mapping-cone product, then (1) follows automatically from
the Leibniz formula above.  What is new is not the sign formula but the
physical constructor and this source-labelled identification.

## Minimal countermodel

For each `(c,rho)` in `{23,45} x {AB,AC}`, take the integral chain complex
with four vertices, the four edges displayed above, and no selected mixed
two-cell.  Let `tau_AB,AC` act by `+identity` between the two root-labelled
blocks and let `sigma` act by `-identity` from the `q23` packet to the `q45`
packet.  Send every existing higher square/cube generator to zero under the
selected mixed-grade projection, exactly as in the pinned inventory.

All edge identities, all `d^2=0` identities, AB/AC transport, and cut
covariance hold in this model.  Nevertheless each block has the nonzero
class (3).  Before covariance there are four primitive classes; sigma pairs
the cuts but leaves two independent AB/AC classes.  Therefore (1) with an
actual `kappa` is not derivable from the pinned relations.

## First unmatched datum and minimal extension

The first unmatched datum is not a sign or an edge term.  It is the
source-labelled two-cell `kappa_23^AB` in the physical off-diagonal
response-to-cap mixed-square grade, beginning with bottom face
`+P_f,23^AB`, together with its root-natural AC instance and sigma mate.

The minimal new source relation is one normalized schema

\[
\boxed{d\kappa_c^\rho=P_{f,c}^\rho-K_{Eq,L,c}^\rho
 +K_{Eq,R,c}^\rho-D_{4,c}^\rho},
\quad c=23,45,\ \rho=AB,AC,                         \tag{7}
\]

with `tau` coefficient `+1`, sigma coefficient `-1`, and primitive unit
normalization.  Within the pinned physical grammar, this is genuinely new
source data.  It could be supplied as the mixed face of a newly constructed
root-natural `Phi_KS,r0`; it is not justified merely by naming a standard
mapping cylinder.

## Scope

This closes the sign and non-derivability audit only at canonical `h=3`.
It does not construct `kappa`, prove `Q23-PROTECTED-FACTOR`, prove
`PAComp(3)`, extend to uniform `h`, or promote any result to the certified
spine.  The countermodel concerns the pinned declared grammar; it does not
prove that an unregistered geometric constructor cannot exist.
