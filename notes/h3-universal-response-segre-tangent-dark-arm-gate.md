# The `2 x 3` response Segre has exactly two tangent-dark arms

## Exact theorem

For a fixed endpoint pair, write the three residual matching values as
`x0,x1,x2` and the two endpoint orientations as `A,B`.  The physical
occurrence block is

\[
 Y=\begin{pmatrix}
 Ax_0&Ax_1&Ax_2\\
 Bx_0&Bx_1&Bx_2
 \end{pmatrix}.                                      \tag{1}
\]

Let `v` be the all-ones `2 x 3` occurrence shear.  Over the
characteristic-zero theorem field,

\[
 \boxed{v\in T_Y\{\operatorname {rank}\le1\}
       \quad\Longleftrightarrow\quad
       A=B\ \hbox{ or }\ x_0=x_1=x_2.}              \tag{2}
\]

This includes zeros: if the endpoint factor is zero then `A=B=0`, and if
the matching factor is zero then `x0=x1=x2=0`.

Checker:

```text
computations/verify_h3_universal_response_segre_tangent_dark_arm_gate.py
```

Frozen ledger digest:

```text
0b32d8cde4f6b53886d6b989c142fc076531f297f1a089a5ec1b607cfabf554e
```

## Proof of the iff

For columns `i<j`, differentiate the rank-one minor along the all-ones
direction:

\[
\begin{aligned}
 d(Y_{0i}Y_{1j}-Y_{0j}Y_{1i})(v)
   &=Bx_j+Ax_i-Bx_i-Ax_j\\
   &=(A-B)(x_i-x_j).                                \tag{3}
\end{aligned}
\]

The three linearized minors are therefore

\[
 (A-B)(x_0-x_1),\quad
 (A-B)(x_0-x_2),\quad
 (A-B)(x_1-x_2).                                    \tag{4}
\]

They all vanish if either factor is dark.  Conversely, if `A-B` is nonzero,
it is invertible in the coefficient field, so all three `xi` agree.  This
also proves the statement at the zero matrix; no smoothness assumption on
the Segre cone is used.  The checker exhausts all `5^5=3125` points with
coordinates in `[-2,2]` as a zero-inclusive guard.

The reverse implication requires an integral domain.  It is intentionally
not claimed over rings with zero divisors.

## Representation-theoretic meaning

The conormal is exactly

\[
  \langle(1,-1)\rangle_{\rm endpoint}
   \otimes
  \langle x_0-x_1,x_0-x_2\rangle_{\rm matching}.     \tag{5}
\]

Thus the tangent-dark locus is the union of two linear representation
strata, not a third mysterious cancellation.

### Endpoint-dark arm: `A=B`

The endpoint-odd value vanishes.  The matching-standard part may remain
nonzero, but the toric product sees none of it.  The existing residual-flip
theorem gives the exact next physical statement:

- on the three matchings, `A_match+I=J3` sees only the invariant line;
- residual flips act on the two-dimensional standard module;
- over `Q[beta]`, each standard character is contracted by the normalized
  bar `-1/2[tau|y]`.

That contraction is physical only after a termwise PP-natural pointed
section is supplied.  The aggregate matching face has forgotten those
characters and does not transport them to the cap/E14 repeated grade.
Therefore endpoint-dark reduces to the existing matching-standard source
gate; it is not a terminal by itself.

### Matching-dark arm: `x0=x1=x2`

Every matching-standard difference vanishes.  The endpoint-odd value may
remain nonzero, but again the toric product is zero.  Here the existing
endpoint-odd Cartan result is stronger: its prism is source-provenant and
target-safe on the canonical physical source orbit.

What it does not do is place the universal response KS generator, cap,
ridge, `W`, or physical `q` into the E14 comparison grade.  Thus the
matching-dark arm reduces to the known endpoint-odd packet plus the same
open augmented placement; it is not an active private-site fan.

At the intersection `A=B` and `x0=x1=x2`, both nontrivial representations
are dark and the all-ones direction has no toric conormal face.

## The bright arm and the precise missing incidence

If some

\[
                         (A-B)(x_i-x_j)\ne0,          \tag{6}
\]

then both an endpoint-odd value and a matching-standard value are nonzero in
one same-word physical toric conormal.  This is genuine progress: the
constant occurrence shear is not a source tangent.

It is not yet the evaluated determinant/private-site fan input.  In the
current response block,

```text
A-B       = p1*s0-p0*s1, an endpoint orientation/KS line;
xi-xj     = difference of residual q_ab:00 matching products.
```

Neither factor is presently an individual nonzero decorated offdiagonal
pair cell `e=A_uv^(ab)`, `a!=b`, together with its signed physical cofactor.
The active-fan theorem consumes exactly such an incidence inside one
complete zero mixed-response row.

The first missing datum is therefore one literal square:

\[
\begin{array}{ccc}
\text{endpoint-odd factor}&\longmapsto&
   \text{offdiagonal physical cell }e\\
\text{matching-standard factor}&\longmapsto&
   \operatorname {Cof}_e\text{ / common-}q
\end{array}                                           \tag{7}
\]

with the two images in the same word, fine, repeated grade, and complete
mixed row.  Coefficient factorization, the endpoint-odd prism alone, the
aggregate matching face alone, and the current physical `q`/anchor shadows
do not supply (7).

Once (7) is source-provenant, (6) yields the physical private-site fan.  The
complete pure supports then invoke the committed exhaustive landing:

```text
nonzero fan -> four-good overlap or literal pure-colour coloop.
```

## Scope

This classifies the canonical `h=3` fixed-endpoint response block over a
field, including all zero degenerations.  It does not construct the
incidence square (7), promote the toric covector to a terminal, or assert a
full GHZ source counterexample.
