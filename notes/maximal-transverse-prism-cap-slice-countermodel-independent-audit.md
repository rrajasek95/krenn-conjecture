# Independent audit of the maximal transverse prism cap slice

## Verdict

**PASS, with the stated transverse-slice scope.**  A clean-room matching
recurrence, an independent 81-coordinate cap calculation, and a separate
coloured square-free algebra reproduce every dimension, coefficient, rank,
and saturation claim in
[`maximal-transverse-prism-cap-slice-countermodel.md`](maximal-transverse-prism-cap-slice-countermodel.md).

For the displayed ten-site source, the full top cap map has rank nine.  Its
unique maximal diagonal-image subspace has dimension (75), and the unique
maximal subspace satisfying the literal global-GHZ cap formula has dimension
(73).  On either subspace the lower cofactor image is exactly the
four-parameter prism, and on the latter subspace the combined top/cofactor
map has rank four with a (69)-dimensional kernel.  The discrepancy ideal is

\[
 I_{\mathcal D}=(z_0z_1z_2),\qquad
 h=sz_0z_1z_2\in I_{\mathcal D},
\]

so its active saturation is the unit ideal.

This is not a global Krenn counterexample.  Eight of its nine top words are
globally mixed, and the global colour-one and colour-two target words are
absent.  It also does not obstruct an argument that uses effective cap
directions transverse to the (73)-plane: all six lower off-diagonal
directions omitted by the diagonal slice are nonzero and are detected by the
cap-adjugate determinant.

## Frozen inputs and independent executable

The primary files audited here had SHA-256 digests

```text
c6936267f51683f659fdc9188ba8e1b69d228c79e9a79f8bd089f3a9d39898aa  notes/maximal-transverse-prism-cap-slice-countermodel.md
dfd146c42471e2cbb2bb1b70e336e5f5d1fd25b247dbf8fe0a472e36e2a7a965  computations/verify_maximal_transverse_prism_cap_slice.py
```

The independent checker is
[`audit_maximal_transverse_prism_cap_slice_independent.py`](../computations/audit_maximal_transverse_prism_cap_slice_independent.py).
It does not import the primary verifier.  Its SHA-256 digest is

```text
9493f1ae930f56a40cdfe54da2c66529cf1f85f6437bf7cff9ed10f83957b507
```

and its frozen semantic-ledger digest is

```text
438b55c95bd56a72640f1a78652f64149c331b7a1665fe2f27c974be5f71bb35
```

## 1. Ambient source and complete top map

Keep the cap order ((p,q,r,s)), with boundary order
((x_0,x_1,x_2,y_0,y_1,y_2)).  The independent recurrence stores every
aggregate cell in physical endpoint order; in particular, reading the
nonsymmetric (pq) block backwards transposes its colour indices.  It finds
exactly two supported internal matching skeletons:

\[
 pq\mid rs,qquad pr\mid qs.
\]

Consequently

\[
 H_W=\sum_{i,j}a_{ij}e_{(i,j,0,0)}+e_{(1,2,1,2)}.       \tag{A1}
\]

Every supported ten-site matching instead uses (rs), one (px_i) edge,
one (qy_j) edge, and the two opposite triangle edges.  Thus the full tensor
has the nine distinct unit coefficients

\[
 H_{10}=\sum_{i,j=0}^2
 e_i^{(p)}e_j^{(q)}e_0^{(r)}e_0^{(s)}E_{ij}.            \tag{A2}
\]

Contracting an arbitrary cap (K) gives

\[
 \tau(K)=\sum_{i,j}K(i,j,0,0)E_{ij}.                   \tag{A3}
\]

The nine coordinate functionals in (A3) are independent, so the complete
top cap map has rank nine.  This also supplies the direct scope check.  Only
the (i=j=0) term of (A2) is globally pure; the other eight are extraneous
mixed words, while (e_1^{\otimes10}) and (e_2^{\otimes10}) are missing.
Hence (H_{10}\ne\Delta_{10,3}).

## 2. The two unique maximal slices

Let (c_{ij}=K(i,j,0,0)).  Since the nine (E_{ij}) are linearly
independent, the inverse image of the diagonal boundary span is exactly

\[
 L_{\rm img}=\{K:c_{ij}=0\text{ for }i\ne j\}.          \tag{A4}
\]

The six displayed coordinate equations are independent.  Therefore

\[
 \operatorname{codim}L_{\rm img}=6,qquad
 \dim L_{\rm img}=81-6=75,                             \tag{A5}
\]

and (A4), being the full inverse image, is the unique maximal linear
subspace whose top image is diagonal.

For the literal global-GHZ formula, the coefficient of (E_{ii}) must be
(kappa_i=K(i,i,i,i)).  At colour zero this is the same coordinate as
(c_{00}).  At colours one and two it adds the independent equations

\[
 c_{11}-K(1,1,1,1)=0,qquad
 c_{22}-K(2,2,2,2)=0.                                  \tag{A6}
\]

The clean-room (9\times81) matrix of (	au-\gamma) has rank eight.
Therefore

\[
 L_{\rm GHZ}=\ker(\tau-\gamma),\qquad
 \operatorname{codim}L_{\rm GHZ}=8,qquad
 \dim L_{\rm GHZ}=73.                                 \tag{A7}
\]

Again the kernel itself contains every linear subspace on which the formula
holds, proving the stated uniqueness and maximality without a genericity
assumption.

## 3. Complete lower cofactor image

The recurrence independently evaluates all fifteen tensors
(H_{W\cup\{u,v\}}).  It finds only the following two forms.

* A same-shore triangle block is its canonical rank-one cell multiplied by
  the scalar (s(K)=K\mathbin{\lrcorner}H_W).
* A cross-shore block (x_i y_j) is
  (c_{ij}e_i e_j).

On (L_{\rm img}), put (z_i=c_{ii}).  Equation (A1) then gives

\[
 s=z_0+5z_1+13z_2+K(1,2,1,2).                         \tag{A8}
\]

Thus all six off-diagonal cross blocks vanish and the remaining nine blocks
are exactly the triangular prism (D(s,z_0,z_1,z_2)).  The four effective
forms are independent on both maximal slices.  An explicit right inverse on
(L_{\rm GHZ}) is obtained by taking

\[
 K(1,2,1,2)=s-z_0-5z_1-13z_2,quad
 K(i,i,0,0)=K(i,i,i,i)=z_i,                            \tag{A9}
\]

with the colour-zero coordinate counted only once.  The independent matrix
calculation consequently gives effective rank four on each slice.  Its
kernel dimensions are (75-4=71) on (L_{\rm img}) and (73-4=69) on
(L_{\rm GHZ}).  The large ambient slice is therefore mostly an ineffective
common kernel, not a large family of distinct lower cofactors.

## 4. Hafnian normalization, discrepancy, and saturation

The independent checker represents a coloured boundary monomial by six
slots, with multiplication set to zero whenever two factors occupy the same
site.  Let (d) be the degree-two edge sum of the prism.  In this
square-free algebra, every perfect matching occurs in all (3!) orders in
(d^3).  Hence the normalization is exactly

\[
 d^3=6H_6(D),                                          \tag{A10}
\]

not merely up to an unspecified scalar.  Direct multiplication yields

\[
 H_6(D)=s^2\sum_{i=0}^2z_iX_i
       +z_0z_1z_2E_{012012}.                           \tag{A11}
\]

Since the capped top tensor on (L_{\rm img}) is
(sum_i z_iX_i), the denominator-cleared source discrepancy is

\[
 \mathcal D=6\left(s^2\sum_i z_iX_i-H_6(D)\right)
             =-6z_0z_1z_2E_{012012}.                  \tag{A12}
\]

Over (mathbb C), (6) is a unit, so the complete coordinate ideal is
(I_{\mathcal D}=(z_0z_1z_2)).  With (h=sz_0z_1z_2), already
(h\in I_{\mathcal D}), and (I_{\mathcal D}:h=(1)).  The checker also
computes the unit Groebner basis of the Rabinowitsch localization ideal

\[
 (z_0z_1z_2,\ 1-u,s z_0z_1z_2)=(1).                  \tag{A13}
\]

The active open set is nonempty: (s=z_0=z_1=z_2=1) makes both (h) and
the mixed generator nonzero.  Thus this is a genuine root cover, not an
empty-open-set artifact.

## 5. The adjugate-visible omitted rows

After deleting (r,s), the eight-site core consists of the two canonical
(K_4) shores and the top-inactive dense (pq) block.  In the coloured
square-free algebra its matrix-unit pair families have the direct form

\[
 B_{ij}=a_{ij}x+R_{ij},                                \tag{A14}
\]

where (x) is the sum of the six shore-triangle edges and (R_{ij}) is the
single cross edge (x_i y_j) with endpoint colours ((i,j)).  Expanding
the alternating determinant directly, rather than calling the universal
identity, gives

\[
 \det(B_{ij})=2\sum_{i,j}\operatorname{Cof}_{ij}(a)E_{ij}. \tag{A15}
\]

For the stated nonsymmetric matrix,

\[
 (\operatorname{Cof}_{ij}(a))=
 \begin{pmatrix}
 -12&4&4\\
 7&-11&5\\
 -1&5&-3
 \end{pmatrix}.                                       \tag{A16}
\]

All nine entries are nonzero.  Subtracting the formal GHZ right-hand side
(2\sum_i\operatorname{Cof}_{ii}(a)X_i) leaves exactly

\[
 2\sum_{i\ne j}\operatorname{Cof}_{ij}(a)E_{ij},      \tag{A17}
\]

with six nonzero coefficients.  Those six words are in one-to-one
correspondence with the quotient coordinates (c_{ij}), (i\ne j), killed
in (A4).  Thus every lower-effective direction missing from the
codimension-six slice is visible to the alternating common-edge identity.

The two further quotient rows between (L_{\rm img}) and (L_{\rm GHZ})
are the diagonal relocations in (A6).  They refer to the extra sites (r,s)
and are absent from the eight-site determinant.  This precisely separates
the eight transverse equations: six alter the lower cofactor family and are
adjugate-visible, while two enforce the positions of the global pure target
coordinates.

## 6. Exact scope

The construction refutes only an inference based on common-edge
realizability plus the exact GHZ cap formula on a large **proper** cap
subspace.  It cannot refute a theorem using the cap formula for every cap,
because (A2) explicitly violates that formula outside (L_{\rm GHZ}).
Nor can it refute a theorem that couples many effective lower transverse
directions: turning on any of the six coordinates (c_{ij}), (i\ne j),
creates the corresponding independent cross block (x_i y_j), and (A17)
shows that the shared-edge determinant sees all six.

The sharp remaining gate is therefore the same one stated in the primary
note: a genuine global repair must cancel the six off-diagonal top rows while
changing the common lower determinant by exactly (A17), and must also enact
the two diagonal relocations (A6).  The maximal prism slice contains none of
that transverse information.

## Reproduction

From the project root, run

```text
uv run python computations/verify_maximal_transverse_prism_cap_slice.py
uv run python computations/audit_maximal_transverse_prism_cap_slice_independent.py
```

The independent run ends with

```text
full top rank / terms: 9 9
maximal slice dimensions: 75 73
effective rank / GHZ-slice common kernel: 4 69
cofactor and adjugate transverse rows: 6 6
independent semantic ledger SHA-256: 438b55c95bd56a72640f1a78652f64149c331b7a1665fe2f27c974be5f71bb35
PASS: maximal transverse prism cap-slice independent audit
```
