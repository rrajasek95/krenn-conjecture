# The nearest cross-word attachment is formal; its first literal face is selected `db01`

## Exact factorization

The shortest candidate uses only already isolated structures.  Let

\[
 c_f=90e_f-\mathbf1_{90},\qquad
 c_{01}=30b_{01}-R.
\]

Matching incidence gives the exact coefficient identity

\[
                         (A+I)c_f=3c_{01}.             \tag{1}
\]

If one grants a **multiplicative, matching/D4-natural physical** generator
`epsilon_cf` with `d epsilon_cf=c_f`, then

\[
 \epsilon_{c01}={(A+I)\epsilon_{cf}\over3},\qquad
 \epsilon_{01}={\epsilon_R+\epsilon_{c01}\over30},
 \qquad d\epsilon_{01}=b_{01}.                       \tag{2}
\]

For the central cell `d theta=(H0-u)e_Eq`, the Koszul product is canonical:

\[
 \kappa_{01}=\epsilon_{01}\wedge\theta,qquad
 d\kappa_{01}=b_{01}\theta-epsilon_{01}(H_0-u)e_{Eq}. \tag{3}
\]

D4 carries the marked pure-`00` occurrence to `R_E14` on the silent
`v04=0` fibre, while `T+rho` is the closed target/residue normalizer.  Theta
supplies the conjugate endpoint half automatically by the pinned flat grade
groupoid.

Thus there is no second abstract selected-fibre generator and no second
central-Koszul generator after one physical multiplicative `c_f`
attachment.  The issue is literal source placement of that one attachment.

Checker:

```text
computations/verify_h3_cross_word_cap_central_attachment_first_face_gate.py
```

Frozen ledger SHA-256:

```text
a0bb53ea0c5c3f683c2e815c2d8e83a2afa63857d0e945b1fc80b32d13bf50d8
```

## First literal face: the selected six-term derivative

The fixed-endpoint fibre is

\[
 b_{01}=p_0s_1(q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}),
\]

so its first principal-parts face is

\[
 db_{01}=p_0s_1\sum_{{ab|cd}}
          (dq_{ab}q_{cd}+q_{ab}dq_{cd}).              \tag{4}
\]

The old complete response PP row contains only `dR=sum db_ps`.  In
coordinates `(b01, other 29 fibres, z01)`, the response and graph rows are

```text
(1,1,0), (-1,0,1).
```

They have rank two.  Adjoining the selected fibre `(1,0,0)` raises rank to
three; the primitive covector `(1,-1,1)` kills both old rows and reads one
on it.  Therefore a graph coordinate does not construct (4).  The missing
cross-word attachment must carry this face itself.

## First cross-summand dual after granting the selected face

Give the construction every coefficientwise advantage and grant the
selected `db01/P_f` packet.  In shadow coordinates

```text
(P_f, cap, R_E14, central E, ridge),
```

the available independent faces are

```text
P_f=(1,0,0,0,0), cap=(0,1,0,0,0), D4=(0,0,1,0,0).
```

The required mixed comparison is

```text
Phi_orb(E)=R_E14=(0,0,1,1,0).
```

The primitive dual `(0,0,0,1,0)` kills every separate edge, including the
horizontal cap graph, and reads one on the mixed comparison.  Equivalently,
the pointed/D4/objectwise-`K_Eq` square has edge rank three and

\[
 H_1\cong\mathbb Z,qquad z=(1,-1,1,-1).              \tag{5}
\]

The formal wedge (3) is precisely the missing two-cell, but it is not a
physical source cell until `epsilon_cf` has been placed across the response,
cap, and E14 word/fine/repeated summands.

## First physical proper face of that mixed cell

After granting the coefficient of the mixed square, the first uncancelled
codimension-one face is the marked D3/root-lower transport

```text
face 3 -> B4,
face 5 -> B1,
```

which must send the even pair to

\[
                         -(B_1+B_4)=-2d_{even}.        \tag{6}
\]

There is no coefficient ambiguity once those literal maps exist.  The
label matrix followed by the cap-residue matrix is

\[
 \begin{pmatrix}0&-1\\-1&0\end{pmatrix},
\]

of determinant `-1`.  Hence rooted `d_even` is forced; current inventory
does not supply the source-labelled D3-to-`B1/B4` map or its `P3+K2`
placement.

## Sharp frontier

These are three views of one nested attachment, not three proof branches:

1. bottom face: selected `db01`/centered occurrence section;
2. mixed face: `Phi_orb((H0-u)e_Eq)=R_E14`;
3. first rooted proper face: D3 to `B4/B1`, hence `-2d_even`.

One source-valid multiplicative cross-word cap/central attachment at grade
`g`, carrying its cap graph, residue, anchor/physical `q`, `W`, and shifted
ridge, supplies all three.  Theta handles the conjugate grade and is not an
additional obligation.

Scope is canonical `h=3`.  The primitive local covectors are not promoted
to Macaulay terminals without extension through the full augmented source.
