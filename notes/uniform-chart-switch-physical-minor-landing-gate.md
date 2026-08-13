# Physical switch contrasts detect every nonzero three-term packet

## The switch carrier is a polynomial, not a relation

For one `h=3` complete lower packet, write

\[
                       H=F+C_1+C_2,                  \tag{1}
\]

where `F` is the fixed-chart term and `C1,C2` are its two four-cycle
companions.  The relative switch DGA has the canonical physical carrier
values

\[
                       t_1=C_1-F,\qquad t_2=C_2-F.   \tag{2}
\]

Each expression in (2) is a literal matching-exchange binomial, quadratic
in the underlying edge/endpoint coefficient cells.  It is not a physical
Plücker or Segre equation.

Checker:
[`verify_uniform_chart_switch_physical_minor_landing_gate.py`](../computations/verify_uniform_chart_switch_physical_minor_landing_gate.py).

The three actual packet types make the distinction transparent:

```text
C4:       F=q01 q23,   C1=q02 q13,   C2=q03 q12
C2+:      F=D q23,     C1=p2 s3,     C2=p3 s2
P2:       F=s1 q23,    C1=s2 q13,    C2=s3 q12
```

In the `C4` row, declaring `C1-F=0` would impose decomposability on an
arbitrary physical `q` matrix.  In `C2+`, it would identify a direct term
`Dq` with an endpoint term `ps`.  In `P2`, it would identify endpoint terms
from different sites.  None is an outer-product relation in the actual
source presentation.

This differs from the pinned toric identity

\[
 u_{Ay}u_{Bx}-u_{Ax}u_{By}=0,                         \tag{3}
\]

whose two products have exactly the same physical factor multiset.  Formula
(3) is quadratic in occurrence coordinates.  Formula (2) is linear in
occurrence coordinates, and its two edge monomials have different factor
multisets.  The physical toric resolution therefore does not kill (2).

## Exact bright/dark coordinates on a complete lower zero row

The change of coordinates

\[
 \begin{pmatrix}H\\t_1\\t_2\end{pmatrix}
 =
 \begin{pmatrix}
 1&1&1\\-1&1&0\\-1&0&1
 \end{pmatrix}
 \begin{pmatrix}F\\C_1\\C_2\end{pmatrix}            \tag{4}
\]

has determinant `3`.  Over the characteristic-zero theorem field,

\[
\begin{aligned}
 F&=(H-t_1-t_2)/3,\\
 C_1&=(H+2t_1-t_2)/3,\\
 C_2&=(H-t_1+2t_2)/3.
\end{aligned}                                        \tag{5}
\]

Thus `t1,t2` are exact coordinates on the complete lower zero fibre `H=0`.
In particular,

\[
              H=t_1=t_2=0\quad\Longrightarrow\quad
              F=C_1=C_2=0.                           \tag{6}
\]

Every nonzero complete lower packet is therefore switch-bright, **provided
`H=0` is a source-valid row in the actual physical grade**.  This is a
positive physical coefficient landing: the relative graph carrier cannot
remain invisible on a nonzero packet once that row has been constructed.

The complete row does not nullhomotope it.  Each of the three displayed
packet types admits the literal physical assignment

```text
(F,C1,C2)=(1,-1,0),
```

so that

```text
H=0,  t1=-2,  t2=-1.
```

These are assignments to the underlying `q,D,p,s` cells, not free
occurrence values.  They are complete local coefficient guards; they are
not asserted to extend through every unary, anchor, physical-`q`, ridge,
and terminal row of a full GHZ source point.

The annihilator of the complete row has the natural even/odd basis

\[
                  (2,-1,-1),\qquad(0,1,-1).          \tag{7}
\]

The odd line is the Cartan orientation.  The even line is the fixed-chart
`C+`/relative-`C4` carrier.  Equation (7) is the first literal coefficient
guard, not yet an accepted augmented terminal.

## Uniform order descent in the dark branch

At general `h`, every fixed parent has `2h-4` companions.  If all switch
contrasts are dark, every child equals its parent.  Hence the complete
packet sum satisfies

\[
                         P=(2h-3)F,                  \tag{8}
\]

where `F` is the lower fixed-chart matching sum.  Therefore a **source-valid
same-grade equation** `P=0` implies `F=0` in characteristic zero.  If the
common fixed edge vanishes, the whole switch-dark packet is already zero;
otherwise (8) is the response equation one order lower.  Common-edge proper
faces commute with this reduction, as proved by the switch DGA.

This hypothesis cannot be dropped.  `P` first appears here as a Hasse/
principal-parts coefficient of the chart construction.  Arbitrary
derivatives of a point equation are not point equations.  The original GHZ
value row does not make `P` vanish unless the physical restriction/
algebraization map supplies the complete lower row with its word, endpoint
head, fine, and repeated grade.

For a mixed response word the GHZ target coordinate of that complete row is
zero.  For a pure target word it is normalized rather than zero, so the
same reduction is affine until the target value is separately cancelled.
Unary rows do not repair this automatically: their product-rule faces must
be transported by the same physical source map.

The resulting physical coefficient alternative is exhaustive:

```text
some t_c is bright
    -> literal occurrence-asymmetric C+/P2 or relative-C4 carrier;

every t_c is dark + source-valid P=0
    -> strict response-order reduction, or zero packet;

every t_c is dark but P is only a formal coefficient
    -> the complete lower restriction/algebraization row remains open.
```

What remains is source placement: extend a bright binomial through the
complete augmented `C+/P2` or same-grade relative-`C4` map.  The complete
mixed GHZ row and ordinary Segre identities do not provide that
nullhomotopy, and the local dual in (7) is not terminal before this augmented
extension.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
`ce836892431a8a06b2f2056c5dcfd0652df424fb238263017ceb28c000e47304`.
