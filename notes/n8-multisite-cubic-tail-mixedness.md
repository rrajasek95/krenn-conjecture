# The remaining cubic cap tail is necessarily mixed

## Setup

Retain the complete binary response packet from
`n8-multisite-full-anchor-cap-quotient.md`:

\[
 q^{[3]}=X_0,\qquad
 p_i s_jq^{[2]}=\delta_{ij}X_{i+1}\quad(i,j=0,1),
\]

and put

\[
 R=p_0(s_0+s_1)+p_1(s_1-s_0).
\]

This note treats exactly the sharp branch left open there,

\[
 qR^{[2]}=0,\qquad R^{[3]}\ne0.                 \tag{1}
\]

The checker is
`computations/verify_n8_multisite_cubic_tail_mixedness.py`.

## The sixteen sectors

Write `a=p0`, `b=p1`, `c=s0`, and `d=s1`.  The cubic divided power is

\[
 R^{[3]}={1\over6}\bigl(a(c+d)+b(d-c)\bigr)^3.
\]

Index its literal row/column sectors by the number of `b` labels and `d`
labels, respectively.  Their coefficient table is

\[
\begin{pmatrix}
  1/6& 1/2& 1/2&1/6\\
 -1/2&-1/2& 1/2&1/2\\
  1/2&-1/2&-1/2&1/2\\
 -1/6& 1/2&-1/2&1/6
\end{pmatrix}.                                           \tag{2}
\]

Thus all sixteen repeated-label sectors are present.  The invertible label
change

\[
 u=c+d,\qquad v=d-c,
\]

has determinant `2` and compresses (2) to the four binary cubic sectors

\[
 R^{[3]}={a^3u^3\over6}+{a^2bu^2v\over2}
          +{ab^2uv^2\over2}+{b^3v^3\over6}.              \tag{3}
\]

This is a label-sector normal form, not a statement about tensor rank on
the six physical output sites.

## Mixedness theorem

For every scalar `t`, the full anchors and (1) give the source-faithful
identity

\[
 (q+tR)^{[3]}=X_0+t(X_1+X_2)+t^3R^{[3]}.                 \tag{4}
\]

Suppose for contradiction that the cubic tail were diagonal-only in the
fixed output basis:

\[
 R^{[3]}=y_0X_0+y_1X_1+y_2X_2.                          \tag{5}
\]

The three diagonal coefficients in (4) would then be

\[
 1+t^3y_0,\qquad t+t^3y_1,\qquad t+t^3y_2.              \tag{6}
\]

None is the zero polynomial in `t`.  Over the complex numbers one can
therefore choose a nonzero `t` outside their finite union of zero sets.  At
that value, (4) is a six-site ordinary source whose output consists of
three nonzero diagonal tensors.  An invertible diagonal change of basis at
one output site normalizes their three coefficients to one.  This produces
`Delta_(6,3)`, contradicting the pinned arbitrary-complex six-site theorem
in `proofs/six-site-arbitrary-complex-obstruction.md`.

Consequently

\[
 \boxed{R^{[3]}\notin\langle X_0,X_1,X_2\rangle}.        \tag{7}
\]

In particular the surviving cubic cap tail has at least one nonzero mixed
output coefficient.  This is stronger than the earlier conclusion
`R^[3] != 0`: the last obstruction cannot hide in a third diagonal anchor.

## Exact scope

The argument classifies the raw sixteen label sectors and forces a mixed
physical output component.  It does **not** determine the tensor rank of
`R^[3]`, exclude its lying in a nontrivial local-GL orbit of a simpler
tensor, or prove that the full one-bad packet is empty.  In particular,
"mixed in the fixed anchor frame" is not promoted here to "not
GL-locally removable."  Any such promotion requires an invariant of the
six-site tensor or a source-level relation among the sixteen sectors.

## Reproduction

```bash
.venv/bin/python computations/verify_n8_multisite_cubic_tail_mixedness.py
.venv/bin/python -O computations/verify_n8_multisite_cubic_tail_mixedness.py
python3.14 computations/verify_n8_multisite_cubic_tail_mixedness.py
```
