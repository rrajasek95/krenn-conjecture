# The centered projector gives a conditional E14 arrow formula, not the transport

## Outcome

The decorated-core coincidence admits an exact **conditional** coefficient
formula.  Suppose an occurrencewise chain map `W` from the root response
block to the E14 unary/G11 S-pair block has already been supplied.  Let
`S_i` be the ninety source occurrences and put

\[
                         d_i=W(S_i)-S_i.               \tag{1}
\]

\[
                         C=90I-J,                      \tag{2}
\]

then for the marked occurrence `f`

\[
 \boxed{
 d_f={1\over90}\left(Cd_f+\sum_{i=1}^{90}d_i\right).} \tag{3}
\]

The first summand is the centered occurrence projector; the second is the
common aggregate occurrence line.  Thus the five-face centered projector is
the correct rank architecture once `W` exists, but it supplies neither `W`
nor the aggregate physically.  Its source lift is open, its scalar zero-face is
`90*f(x)`, and its physical cap projection stops at the primitive class

\[
                         p=(-Q,-\operatorname {ores}),
 \qquad                  \epsilon(p)=-1.               \tag{4}
\]

The smallest positive object is one pointed promoted-occurrence covariance
totalization carrying (3), (4), and all product-rule faces.  This is one
new source family, not a new identity for each occurrence.

Checker:
[verify_h3_centered_projector_e14_word_arrow_gate.py](../computations/verify_h3_centered_projector_e14_word_arrow_gate.py).

## 1. The coefficient arrow is exact

In the ninety-dimensional difference module, the columns of `C` have rank
89 and image `ker(augmentation)`.  The selected vector `d_f` is not in that
image.  The primitive augmentation covector kills every centered column and
reads one on `d_f`.

Adding the aggregate vector `sum_i d_i` raises the rank to ninety and gives
(3).  The denominator 90 is harmless over the characteristic-zero field of
the conjecture, but it records an integral index: a primitive physical
aggregate, rather than an unnormalized sum, is needed for an integral
source complex.

The selected polynomial coefficient is already correct.  After the pinned
site relabelling and colour transposition,

```text
a23_21*a45_12  ->  u05_01*v34_10,
```

and the canonical E14 unary remainder contains this core with coefficient
one.  Restoring

```text
p1_0_1*s1_1_1*v24_11
```

gives the exact promoted E14 monomial.  What differs is its source tag:
`01211222` on the root/cap side versus the E14 unary block `000101`.

The normalized local-`GL3` interval does **not** supply `W`.  Its committed
seven-site instance has source word `01211222` and all-output-lowered
endpoint `00000000`.  The full mixed input makes its GHZ target zero, but
the E14 object is a unary/G11 S-pair based at `000101`, not the all-zero
complete response row.  Therefore the first missing datum is already a
change of source-operation type, before occurrence selection.  Applying a
centered coefficient matrix cannot create that chain map.

## 2. Why the five-face projector does not already supply the arrow

The committed endpoint projector proves

```text
coefficient centered operator      yes
source chain lift                   no
first scalar face                  90*f(x)
physical cap word                  01211222
physical cap grade                 repeated P3+K2
physical standard face rank        4
remaining cap quotient             Z*epsilon.
```

Every centered/five-face column remains in the root-word block.  It has
zero projection to the E14 `000101` first-hit coordinate.  Extend the pinned
E14 rational first-hit dual by zero on the root block.  It kills all 269 old
E14 columns and every centered-projector column, but pairs `-1` with the
promoted target monomial.  Its primitive integral normalization pairs
`-30`.  This is the sharp source-presentation dual proving that the cross-
word column is new.

There is an independent cap shadow.  The physical Cartan routes span the
saturated rank-four lattice `ker(epsilon)` on the five faces.  They cannot
supply (4); `epsilon=sum_v lambda_v` detects it primitively.  These two
duals are compatible views of the missing totalization: one sees its E14
principal boundary, the other its aggregate proper face.  Neither is yet a
physical Fredholm terminal, because the complete augmented comparison has
not been constructed.

## 3. Minimal two-word quotient

After quotienting the old block-diagonal source maps, retain the primitive
root-cap and E14 first-hit coordinates.  The desired word arrow is

\[
                         g=(-1,+1).                    \tag{5}

One cross-word cell is necessary and sufficient to identify these two
classes.  The common covector `(1,1)` kills (5), so a common aggregate class
still survives.  The primitive cap column `p=(-1,0)` and (5) have determinant
one; together they complete the two-coordinate lattice.

This does not mean two unrelated construction theorems are needed.  A
single pointed totalization family may contain the word-arrow generator and
the primitive cap generator.  It does mean that a single boundary column
`g` cannot also erase the common aggregate class.

## 4. Smallest physical extension

The required family `G_f` must have:

- principal boundary equal to the promoted E14 monomial in word `000101`
  minus its relabelled decorated `2K2` occurrence tagged by `01211222`;
- occurrence face `90*e_f-sum_M e_M` and scalar correction `-90*f(x)`;
- primitive cap face (4) in the same labelled repeated `P3+K2` grade;
- all endpoint Cartan, second-Hasse, mixed endpoint/matching, and cubic
  Hasse product-rule faces;
- rootless ridge and physical-`q` transport; and
- `Eq`, `W`, target, anchor, eta, and sigma zero or committed physical
  boundaries.

At the coefficient level, (3) describes the arrow after the occurrencewise
transport `W` and aggregate line are granted.  At the physical level, `W`,
the aggregate/primitive cap cell, and their augmented product-rule
totalization are absent.  The five-face projector therefore reduces the
word-arrow theorem to one finite source extension; it does not already prove
it.

## 5. The same base cell cancels the two shifted `Gamma1` debts

The new restriction--insertion theorem identifies the two marked proper
faces of the centered occurrence class exactly.  For either residual edge
`e` in the marked matching,

\[
 D_ec_{f,3}={15\over2}c_{f/e,2}+{13\over2}H_0.         \tag{6}
\]

The two marked edges give the two order-two centered classes.  The shifted
raw `Gamma1` operator has coefficient `-5/8` on each of those same
`c_lower` coordinates.  Since

\[
 {1\over12}{15\over2}={5\over8},                      \tag{7}
\]

adding `(1/12)G_f` cancels both centered debts simultaneously.  Its
constant contribution on each face is

\[
 {1\over12}{13\over2}H_0={13\over24}H_0.              \tag{8}
\]

So the proposed `01211222 -> E14` centered comparison is exactly the common
base cell at the order-two occurrence quotient:

- unscaled, its marked restrictions lift the primitive carrier debts;
- scaled by `1/12`, the same restrictions cancel the two shifted `Gamma1`
  centered debts; and
- the residual constants in (8) must be transported through the one common
  `H0` base line.

The shortest literal base-cell theorem is now sharper.  Construct physical
order-two centered cells with `p/s`-odd orientation in the two mixed cuts

```text
deleted 23: lower word 0112, reinsert q23:21,
deleted 45: lower word 0121, reinsert q45:12.
```

Their reinsertions must land in the original word `01211222` and labelled
repeated `P3+K2` grade, and they must be the two marked faces of the same
pointed E14 comparison `G_f`.  Once those faces have coefficient (6), the
unscaled cell handles the primitive carrier, `(1/12)G_f` handles both
centered parts of `Gamma1`, and common-`H0` transport handles the remaining
`13/24` on each face.

This is not yet equality of complete physical columns.  Equation (7) checks
the coarse centered quotient; word, fine/repeated grade, Eq, target,
ordinary residue, physical `q`, anchor, eta/sigma, and `W` still have to
commute in the augmented comparison.  But it removes a possible extra
source theorem: the primitive carrier and shifted first-moment packet ask
for the same two marked faces of one base cell, not four unrelated fillers.

## Verification

Run the checker normally, optimized, and isolated/no-site.  Frozen ledger
SHA-256:

```text
c656ea22974f5935ca0f840d266f33753769e7460f4f75403b1ef32bac516127
```
