# The aggregate matching face does not fill endpoint-triangle isotropy

## Coefficient-level action

Use the three residual K4 matchings

```text
M0=23|45,   M1=24|35,   M2=25|34.
```

The matching adjacency is the complete graph on these three vertices, so

\[
                         A+I=J_3.                    \tag{1}
\]

Both residual flips produced by the endpoint triangles act as

```text
tau23: M0->M0, M1<->M2,
tau45: M0->M0, M1<->M2.
```

Thus they stabilize the marked occurrence and the selected matching fibre

\[
                         b_{01}=M_0+M_1+M_2.         \tag{2}
\]

They commute with `A`, but they are not `A` or a polynomial in `A`.  On the
two-dimensional standard matching module, `A` is the scalar `-1`, whereas a
flip has `+1` and `-1` eigenlines.  Precisely,

\[
 (A+I)(\tau-I)=(\tau-I)(A+I)=0.                     \tag{3}
\]

The invariant matching face spans `(1,1,1)`, while the first isotropy
direction is `(0,-1,1)`; adjoining it raises rank from one to two.  Hence
the relation is semidirect, not an identification of source boundaries.

Checker:
[`verify_h3_matching_face_residual_flip_semidirect_gate.py`](../computations/verify_h3_matching_face_residual_flip_semidirect_gate.py).

## Centered classes remain invariant

On all ninety occurrences,

\[
 c_f=90e_f-\mathbf1_{90},
 \qquad c_{01}=30b_{01}-\mathbf1_{90}.               \tag{4}
\]

Both `tau23` and `tau45` fix `e_f`, `b01`, `c_f`, and `c01`.  The exact
matching identity

\[
                     (A+I)c_f=3c_{01}                \tag{5}
\]

is flip-equivariant.  In particular, applying a residual-flip bar to the
aggregate centered top has boundary zero.  Equation (5) constructs the
selected fibre from a physical centered lift, but does not construct the
triangle homotopy.

## The distinction first appears termwise in principal parts

Order the six terms of the selected matching face as

```text
0 dq23*q45      1 q23*dq45
2 dq24*q35      3 q24*dq35
4 dq25*q34      5 q25*dq34.
```

The two triangle flips act by

```text
tau23 = (2 5)(3 4),
tau45 = (2 4)(3 5),
```

and fix terms `0,1`.  Therefore both fix the aggregate

\[
\begin{aligned}
 db_{01}=p_0s_1(&dq_{23}q_{45}+q_{23}dq_{45}
               +dq_{24}q_{35}+q_{24}dq_{35}\\
               &+dq_{25}q_{34}+q_{25}dq_{34}).       \tag{6}
\end{aligned}
\]

The bar boundary of the supplied aggregate face (6) is consequently zero.
On the individual PP terms, however, the two flip-boundary images span the
entire three-dimensional augmentation-zero module of the four cross terms.
Together with the invariant vector (6), the rank is four.  Examples of the
missing standard directions are

```text
q25*dq34 - dq24*q35,
dq25*q34 - dq24*q35.
```

Thus a source object retaining the six labelled terms has a canonical
semidirect residual-flip action, but the one aggregate `db01` column does
not supply its isotropy bars.

## Normalized `C2` bars contract the standard module conditionally

There is no new rational homology once the termwise source object exists.
On the four cross terms, `tau23,tau45` generate the regular `V4` action.
An explicit basis for its augmentation-zero module is

```text
y1=( 1,-1,-1, 1),   eigenvalues (tau23,tau45)=(+1,-1),
y2=( 1,-1, 1,-1),   eigenvalues                 =(-1,+1),
y3=( 1, 1,-1,-1),   eigenvalues                 =(-1,-1).
```

For a flip `tau` acting as `-1` on `y`, the group-bar boundary is

\[
 d[\tau\mid y]=(\tau-1)y=-2y.
\]

Therefore, over `Q[beta]`,

\[
                         h(y)=-\tfrac12[\tau\mid y],
 \qquad dh(y)=y.                                    \tag{7}
\]

Choose `tau45` for `y1` and `tau23` for `y2,y3`.  This contracts all three
standard directions exactly.  The normalized bars have zero GHZ target,
central Eq incidence, marked-anchor/centered-top, aggregate six-term `q`,
and coefficient augmentation.

Equation (7) is a source-valid construction only under one precise
hypothesis: the pointed centered response section is **termwise PP-natural**
under the literal residual site flips.  Then the orbit-labelled cells
`[tau|y]` are physical bars and their transported fine labels are part of
the same semidirect object.  The aggregate matching column does not imply
this hypothesis, because it has forgotten the three character lines.

## Physical typing

At the checked response level:

- the coefficient and PP word is `11:110000`;
- the marked decorations are `q23:00*q45:00` and the other two K4
  matchings;
- both triangle flips have GHZ target readout zero;
- their central Eq incidence is zero;
- they fix the marked anchor, `c_f`, and the aggregate physical six-term
  `q` face.

Their nonzero component is the mixed/path-labelled PP standard module, for
example the target-word difference

\[
                         X_{000100}-X_{001000}.       \tag{8}
\]

No checked identity transports the required termwise bar from response word
`110000` to the cap word/fine/repeated grade

```text
01211222 / t*q_(v,N) / P3+K2
```

or to `G11[111111]` and unary E14 word `000101`.  Equality of target,
anchor, Eq, and aggregate-q readouts does not supply that source placement.

## Consequence for the totalization

Adding the already required aggregate matching PP face does **not** close
endpoint-triangle isotropy automatically.  Relative to that aggregate
column, the isotropy bar is an independent source face.  But once a
termwise flip-equivariant pointed section is granted, (7) makes the bars
canonical normalized faces; no further independent isotropy theorem is
needed.  One higher semidirect endpoint/matching PP totalization can package

1. the aggregate matching face;
2. the termwise residual-flip bars;
3. the endpoint triangle 2-simplices; and
4. the independent `B-2` and `B+2` product-rule faces.

Constructing that source-natural termwise object, with cap/E14 grade
transport, is the exact positive theorem.  This audit does not construct it
or promote its local standard-module covectors to physical terminals.

## Verification

```text
python3 computations/verify_h3_matching_face_residual_flip_semidirect_gate.py
python3 -O computations/verify_h3_matching_face_residual_flip_semidirect_gate.py
python3 -I -S computations/verify_h3_matching_face_residual_flip_semidirect_gate.py
```

Frozen ledger SHA-256:

```text
81e1af78ed28743afb896e72ff7d96943318a0d978b9358709751823731e5288
```
