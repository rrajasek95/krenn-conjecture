# The mixed GHZ row does not yet contain the lower Hasse packet

## Decisive physical grade check

The lower packet is not currently a literal target-zero coefficient in its
mixed word.  It is a second-Hasse coefficient with its varied direction
pair retained:

```text
QQ target one-edge          Hasse[2](Q01,Q23)
QQ response / C2+           Hasse[2](Q01,Q23)
DQ C4                       Hasse[2](D,Q01)
PS C4                       Hasse[2](P0,S1)
PQ P2                       Hasse[2](P0,Q12)
SQ P2                       Hasse[2](S0,Q12).
```

The mixed GHZ coefficient is in `Hasse[0]`, with no direction-pair label.
These are different direct-sum source grades even when output word, endpoint
head, fine labels, and bare residual polynomial agree.  More precisely, the
first mismatch is the direction-pair component of the **repeated source
grade**: the desired lower row has forgotten the varied pair, while the
physical second-Hasse face has retained it.

Checker:
[`verify_uniform_chart_switch_word_target_affine_gate.py`](../computations/verify_uniform_chart_switch_word_target_affine_gate.py).

The checker gives literal physical polynomial counterguards.  For example,
in the mixed word `001122`, set

```text
D=q01=0, q23=q45=1, all other displayed cells=0.
```

The complete response polynomial is zero, but

\[
 \partial_D\partial_{q_{01}}R
 =q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}=1.          \tag{0}
\]

Analogous assignments give value one for every row in the table above while
the underlying degree-zero target/response value is zero.  Thus

```text
mixed target value zero  does not imply  lower Hasse H=0.
```

The first mismatch is the repeated Hasse/direction-pair source grade, before
target, anchor, physical `q`, ridge, or terminal readouts.  A source-valid
restriction/algebraization cell with its product-rule faces is necessary.
Arbitrary differentiation of the point equation is invalid.

The remainder of this note describes the exact affine split **after** such
an algebraization is constructed.

## Every lower topology has mixed and pure realizations

The three terms in each lower packet carry the same output word.  Literal
decorated representatives are:

```text
C4, pure 0000:
  q01[00]q23[00], q02[00]q13[00], q03[00]q12[00]

C4, mixed 0011:
  q01[00]q23[11], q02[01]q13[01], q03[01]q12[01]

C2+, pure 00 / mixed 01:
  D q23, p2 s3, p3 s2

P2, pure 000 / mixed 001:
  s1 q23, s2 q13, s3 q12.
```

The checker verifies sitewise that all three terms in each line have the
displayed word.  Therefore none of the three packet topologies is
intrinsically mixed.  A fixed physical source can support only its pure
representative.

Site permutations and global colour permutations preserve the number of
colours in a word.  They cannot turn a pure packet into a mixed packet.  A
local colour/root change can, but it changes the physical word and carries
the target and product-rule defect.  That is the `C+` comparison being
sought, not an available covariance operation.

## The affine bright/dark split

Let

\[
 H=F+C_1+C_2=\tau_w,qquad
 t_1=C_1-F,qquad t_2=C_2-F,                          \tag{1}
\]

where `tau_w=0` for a mixed word and `tau_w=1` for a normalized pure word.
The determinant-three inverse from `03f0a78` gives

\[
\begin{aligned}
F&=(\tau_w-t_1-t_2)/3,\\
C_1&=(\tau_w+2t_1-t_2)/3,\\
C_2&=(\tau_w-t_1+2t_2)/3.                            \tag{2}
\end{aligned}

Consequently

\[
t_1=t_2=0\quad\Longleftrightarrow\quad
(F,C_1,C_2)=(\tau_w/3,\tau_w/3,\tau_w/3).            \tag{3}
\]

For a mixed word, (3) is the zero packet.  Hence once a physical bridge makes
the lower `H` an actual same-grade mixed GHZ coefficient, every nonzero
packet is unconditionally switch-bright.  Equation (0) proves that this
bridge is a real hypothesis, not bookkeeping.

For a pure word, (3) is the nonzero flat packet

\[
                         (1/3,1/3,1/3).               \tag{4}
\]

All three topologies admit literal underlying-cell assignments realizing
(4).  Thus choosing a mixed representative is not a valid exhaustion.

## What all-word darkness does and does not close

Suppose every physical switch contrast is dark for every admitted word and
endpoint head.

- Every mixed lower coefficient vanishes.
- Every centered occurrence carrier on a pure coefficient vanishes.
- The pure target-normal invariant line (4) remains.

The coarse target of the six-direction packet cancels because

\[
                  2+2-1-1-1-1=0.
\]

This coarse cancellation does not construct a fine-labelled source
boundary.

For the `C2+/P2` lane, the selected centered `t_zprivate` debt is gone in
the all-dark branch.  Its target/unary product-rule compatibility still has
to be transported by the same physical restriction/reinsertion map; it is
not implied by coefficient darkness.

For `C4`, (4) is exactly the invariant augmentation-one line isolated by
the generic symmetric placement theorem.  The remaining datum is

```text
U_C4[D,Q01;2345]
```

or, with a nonunit common core, the one invariant colon/`Tor_1` class.  Once
that same-grade column is placed, the committed cap extension gives the
exhaustive protected filler-or-augmented-terminal fork.

Thus all-word/head darkness is useful but not final:

```text
mixed words                     -> zero packet;
pure centered switch directions -> zero;
pure invariant affine line       -> U_C4 / one colon-Tor gate.
```

The shortest next theorem is a source-valid word/head restriction map whose
mixed components use target zero and whose pure component supplies the
target-normal augmentation-one `C4` column, together with the unary
product-rule faces.  This note does not infer point equations from arbitrary
Hasse coefficients.

Pinned checker ledger:

```text
b3b9522faf0444ebb5f8d573c1db11cef4e069a3d4e2a85a47368e12fa870c2d
```
