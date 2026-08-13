# The selected-fibre graph leaves one face; centered descent removes it

## Result

Let

\[
 b_{01}=f+m_1+m_2
\]

be the fixed-endpoint K4 fibre containing the marked occurrence `f` and its
two residual matching switches.  The coordinate `u_f` used by the pointed
conormal is a graph coordinate for the **single** occurrence `f`.  It is not
a coordinate for `b_01`:

\[
 u_f=f,\qquad z_{01}=b_{01}quad\Longrightarrow\quad
 z_{01}-u_f=m_1+m_2.                                 \tag{1}
\]

Therefore reusing `u_f` as the selected-fibre coordinate imposes
`m1+m2=0` and changes the classical source.  A fresh degree-zero coordinate
`z_01` with monic graph equation `z_01-b_01=0` is presentation-safe, but it
does not make `b_01` a source equation.

Checker:
[`verify_h3_e14_selected_fibre_graph_keq_koszul_gate.py`](../computations/verify_h3_e14_selected_fibre_graph_keq_koszul_gate.py).

## The exact `2 x 2` graph/Koszul square

Let

\[
 F=(H_0-u)e_{\rm Eq},qquad
 d\epsilon_g=z_{01}-b_{01},qquad d\theta=F.
\]

The graph extension has the canonical mixed cell

\[
 \kappa_g=\epsilon_g\wedge\theta,
 \qquad
 d\kappa_g=(z_{01}-b_{01})\theta-\epsilon_gF,        \tag{2}
\]

and `d^2 kappa_g=0`.  Thus the proposed derived square genuinely exists.
But (2) contains `z_01*theta` together with the desired
`-b_01*theta`; the graph has only moved the selected-fibre obstruction to a
private coordinate.

This is primitive.  In coordinates

```text
(b_01, sum of the other 29 fibres, z_01)
```

the complete response and graph equations are

```text
R             = ( 1,1,0)
z_01-b_01     = (-1,0,1),
```

while `b_01=(1,0,0)`.  The old rank is two, adjoining `b_01` raises it to
three, and `(1,-1,1)` kills both old rows and reads one on `b_01`.

Adding a basepoint cell `d tau=z_01` would solve the algebra:

\[
 \epsilon_{01}=\tau-\epsilon_g,qquad
 d\epsilon_{01}=b_{01}.                              \tag{3}
\]

But its classical truncation is `z_01=b_01=0`.  This is the same kind of
fibre-changing basepoint attachment already isolated for `P_f`, not a
presentation-safe construction.

## The fibre-preserving positive route

There is a unique centered alternative.  Among the thirty ordered endpoint
fibres put

\[
 R=\sum_{p\ne s}b_{ps},qquad
 c_{01}=30b_{01}-R.                                  \tag{4}
\]

If a physical generator `epsilon_c` satisfies `d epsilon_c=c_01`, the
existing complete response generator gives, over characteristic zero,

\[
 \epsilon_{01}={\epsilon_R+\epsilon_c\over30},
 \qquad d\epsilon_{01}=b_{01}.                       \tag{5}
\]

Then the desired selected central cell is automatic:

\[
 \kappa_{01}=\epsilon_{01}\wedge\theta,
 \qquad
 d\kappa_{01}=b_{01}\theta-epsilon_{01}F.           \tag{6}
\]

The marked occurrence projector lands on exactly this centered fibre.  On
the ninety occurrence coordinates, let

\[
 c_f=90e_f-\mathbf1_{90},qquad M=A+I.
\]

Since `M e_f=b_01` and `M 1=3*1`,

\[
                     \boxed{M(c_f)=3c_{01}.}          \tag{7}
\]

Thus one physical source-labelled lift of `c_f`, natural under the matching
numerator, supplies `epsilon_c=M(epsilon_cf)/3`; (5)--(6) then construct the
selected mixed cell without a new basepoint.  This is the sharpest positive
compression: the open selected response section and the open centered
occurrence descent are the same construction after (7).

## First physical descent face

The coefficient identity (7) does not by itself provide a source chain.  Its
first literal principal-parts face is

\[
\begin{aligned}
 db_{01}=p_0s_1(&dq_{23}q_{45}+q_{23}dq_{45}
               +dq_{24}q_{35}+q_{24}dq_{35}\\
               &+dq_{25}q_{34}+q_{25}dq_{34}),       \tag{8}
\end{aligned}
\]

in response head/word `11:110000`.  The complete old source contains only
`dR=sum db_ps`; selecting (8) raises the first-PP rank from one to two.
Therefore (8), together with the private `dz_01` companion in (2), is the
first physical word-labelled descent square.

The matching face has target zero.  Endpoint transport still carries the
known eighteen-word target normal, so the moving-target D4 cone remains a
proper face rather than a consequence of (6).  The full comparison must
also transport from the response cube `110000 -> G11[111111]` to E14 unary
word `000101`, and place the cap faces in
`01211222 / t*q_(v,N) / P3+K2`.

The selected square does not construct the shifted `pq/xv` Kähler class;
`gamma=-dOmega` remains the independent ridge face.  Equations (4)--(7) are
valid over `Q[beta]` and have no beta torsion, but the `beta=0`/Bockstein
branch follows only if the physical centered lift, central `theta`, and all
proper faces are themselves defined integrally in `beta`.

## Shortest construction theorem

Construct one physical centered occurrence cell `c_f`, natural under the
matching and endpoint orbit, plus the already open target-zero central
`theta`.  Then (7), (5), and the canonical Koszul product (6) construct the
central equality.  The remaining work is physical descent of the six-term
word face, endpoint target correction, and cap/ridge/q augmentation—not a
second abstract selected-fibre generator.

This is exact for canonical `h=3` over `Q[beta]`.  It does not construct the
physical centered cell or promote the primitive local dual to a terminal.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
printed by the checker:

```text
fb27970da3edf4ad7f92f9d4a3743a56935cd9b40daa47c7ec2ee07dff50f172
```
