# Segre brightness does not start the private-site identity without an incidence map

## Result

The full target-augmented private-site identity does not by itself turn a
nonzero response-Segre conormal into an active fan.  Its hypothesis is a
named nonzero offdiagonal decorated cell

\[
 e=A_{vu}^{ba},\qquad a\ne b,                         \tag{1}
\]

whereas the response-Segre factor is

\[
 (p_1s_0-p_0s_1)(x_i-x_j)\ne0                       \tag{2}
\]

with diagonal `00` residual matching products `xi`.  No committed source
map identifies either factor of (2) with the cell and cofactor consumed by
(1).

Checker:

```text
computations/verify_h3_segre_bright_private_site_incidence_tate_alternative.py
```

Frozen ledger digest:

```text
04f70446b8a3b0447114627568d34cf134acc7001f79c9128a789cabc3103fba
```

## Sharp complete-local-row guard

Take the fixed-endpoint `2 x 3` block with

\[
 A=1,\qquad B=0,\qquad (x_0,x_1,x_2)=(1,0,-1).
\]

Then

\[
 Y=\begin{pmatrix}1&0&-1\\0&0&0\end{pmatrix},
\]

so each complete orientation response sum is zero.  The three all-ones
Segre derivatives are

\[
                         (1,2,1),                    \tag{3}
\]

hence the block is bright.

At the same time, retain only diagonal `00` residual cells and set all six
ternary offdiagonal decorated reference types to zero.  Every exact
private-site consequence becomes

\[
                  \sum_s\Delta_{us}C_s=-e=0.         \tag{4}
\]

Thus the complete selected response rows and all local private-site rows
are compatible with (3) and no offdiagonal reference cell.  The private-site
identity is an implication *from* (1), not an inverse construction of (1).

This is a complete local response/private-site quotient, not a full GHZ
source point.  Unary, pure-target, anchor, and normalization rows may still
force additional structure globally; no counterexample to that stronger
claim is asserted.

## The precise incidence that is missing

Modulo current local rows, three objects remain independent:

```text
the endpoint-times-matching toric conormal,
an offdiagonal decorated cell e,
its signed physical cofactor/common-q C_e.
```

Their successive quotient ranks are `1,2,3`.  The first missing physical
square must send

\[
\begin{array}{ccc}
p_1s_0-p_0s_1&\longmapsto&e=A_{vu}^{ba},\ a\ne b,\\
x_i-x_j&\longmapsto&C_e
\end{array}                                           \tag{5}
\]

inside one complete zero mixed-response row, with identical word, fine, and
repeated grade.  Once (5) exists, `e!=0` invokes the exact source identity

\[
                         \sum_s\Delta_{us}C_s=-e,
\]

and gives a source-provenant private-site fan.  The complete pure supports
then yield the committed exhaustive landing: four-good or a literal
pure-colour coloop.

## One multiplicative Tate lift packages every arm

There is a shorter constructive target than building (5) separately.  Let
`L` be the centered occurrence scalar and suppose the physical comparison
contains a pointed, termwise multiplicative Tate generator

\[
                             d\epsilon=L.             \tag{6}
\]

For the closed toric conormal `k`, Leibniz gives exactly

\[
                         d(-\epsilon k)=-Lk.          \tag{7}
\]

The right side is the obstruction to the physical occurrence shear.  Thus
the entire bright rank-thirty toric orbit is a compulsory proper face of
one multiplicative comparison, not a second conjecture-level generator.

The same equivariant lift packages the two dark arms:

- if `A=B`, the toric face vanishes and the remaining matching-standard
  action face is contracted by the normalized residual-flip bar
  `-1/2[tau|y]`, conditional on termwise PP naturality;
- if `x0=x1=x2`, the toric face vanishes and the remaining endpoint-odd
  action face is the already source-provenant target-safe Cartan prism,
  conditional on placing the same `epsilon` in the AugP2/E14 grade;
- if both are dark, only the underlying centered Tate placement and its
  augmented readouts remain.

## Shortest exhaustive local alternative

1. Construct the pointed multiplicative physical `epsilon`.  Then (7)
   fills the bright toric face, and matching bars/odd Cartan fill the dark
   action faces.
2. If `epsilon` is absent and a Segre product is bright, construct (5) and
   enter the fan landing, or extend the first fully augmented nonlift to an
   accepted terminal.
3. In the endpoint-dark arm, construct the termwise matching-standard bar
   placement or its augmented terminal.
4. In the matching-dark arm, combine the physical odd Cartan prism with the
   centered AugP2/E14 placement or its augmented terminal.

There is no fifth coefficient case.  The remaining question is source
placement/augmentation, not another Segre identity.

Scope is canonical `h=3` over a characteristic-zero field.  The local guard
does not decide whether the remaining global unary/pure GHZ rows force the
missing multiplicative comparison or the incidence square.
