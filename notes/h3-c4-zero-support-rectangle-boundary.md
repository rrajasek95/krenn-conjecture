# Flat C4 zero supports are vertex rectangles; one q-edge K2,2 remains

## Result

Consider the four literal edge functions in the target-coloop diagonal
return, on vertex order `0,1,4,5`:

\[
A(x)=f_{01}(x_0,x_1)f_{45}(x_4,x_5),\qquad
B(x)=f_{05}(x_0,x_5)f_{14}(x_1,x_4).                 \tag{1}
\]

Suppose the nonzero word supports of `A` and `B` agree.  Then there are
nonempty colour subsets `S0,S1,S4,S5` such that

\[
\begin{aligned}
\operatorname{supp}f_{01}&=S_0\times S_1,&
\operatorname{supp}f_{45}&=S_4\times S_5,\\
\operatorname{supp}f_{05}&=S_0\times S_5,&
\operatorname{supp}f_{14}&=S_1\times S_4.             \tag{2}
\end{aligned}
\]

Hence the common nonzero word support is the single Cartesian product

\[
                         S_0\times S_1\times S_4\times S_5. \tag{3}
\]

It is connected in the Hamming graph.  Zeros cannot split a flat C4 into
several unrelated word components: either the two supports mismatch at a
word, giving the first curvature word, or every zero is a coordinate
deletion as in (2).

This support statement must not be confused with a weakening of complete
tensor equality.  If `A=lambda B` holds coefficientwise on **all** words,
then equality of nonzero supports is automatic; the rectangle theorem and
the coefficient argument below show that the full tensor is still a Segre
intersection with vertex gauges.  Zeros cause no additional obstruction in
that stronger problem.  The separate value of the support theorem is at an
additional-term boundary, where one first knows only which terms can be
nonzero and must decide whether a mismatched word supplies curvature.

Checker: `computations/verify_h3_c4_zero_support_rectangle_boundary.py`.

## Proof of the rectangle theorem

Write `R01,R45,R05,R14` for the four edge supports.  Their matching-product
support equality is

\[
 R_{01}\times R_{45}=R_{05}\times R_{14}              \tag{4}
\]

after permuting coordinates.

Choose one edge from `R45`.  If `(a,b)` and `(a',b')` lie in `R01`, the two
corresponding words lie in the right side of (4).  Cross their `0` and `1`
coordinates there and apply (4) backwards.  This gives `(a,b')` and
`(a',b)` in `R01`.  Thus `R01` is the product of its two projections.
The same argument applies to the other three edges.  Their projections
must agree at every shared vertex, proving (2).

This works for any finite colour set.  The checker exhausts the ternary
case directly: among all

```text
(2^9-1)^2 = 261121
```

nonempty pairs `(R01,R45)`, exactly

```text
7^4 = 2401
```

also factor across the `05|14` matching.  They are exactly the four choices
of nonempty vertex subsets.  All `2401` common supports are Hamming
connected.

## Coefficients on a nonzero rectangle

If the stronger flat identity

\[
                              A=\lambda B\ne0          \tag{5}
\]

holds on (3), fix one active value at the two opposite vertices.  Equation
(5), while varying the other two values, writes each edge matrix as an
outer product.  Consequently there are nonzero vertex functions `u_v` and
edge scalars `c_e` with

\[
              f_{uv}(x_u,x_v)=c_{uv}u_u(x_u)u_v(x_v), \tag{6}
\]

and the only coefficient condition is

\[
                  c_{01}c_{45}=\lambda c_{05}c_{14}.  \tag{7}
\]

Thus the nonzero part is a vertex gauge.  The checker constructs an exact
nonzero rational example on every one of the `2401` rectangle supports.
Extended by zero outside the vertex rectangle, (6) is the complete tensor
factorization.  In particular, full coefficientwise equality has no
disconnected-zero exception.

## Canonical target-coloop specialization

The diagonal-return base word is `(0,0,2,2)`, so each `S_v` contains its
displayed base colour.  There are `4^4=256` such rectangle patterns.

In the canonical packet the physical edge `45` is outside the selected
anchor union and already carries `45:22`.  If either `S4` or `S5` contains
another colour, rectangularity supplies an off-diagonal decorated cell on
`45`.  The pinned nonanchor theorem routes it.  This closes `240` of the
`256` patterns.

In the remaining `16`,

```text
S4 = S5 = {2}.
```

They split as

```text
fully singleton diagonal C4:             1
one decorated vertex star on the C4:     6
two adjacent decorated vertex stars:     9.
```

Their physical edge graph is exactly

```text
01 - 14 - 45 - 05 - 01,
```

a `C4=K2,2`.  This is the sharp zero-support landing: all larger flat
supports either expose the off-anchor edge or remain on this one physical
four-cycle.

## Why this does not yet invoke the strict Hall theorem

The strict Hall normal forms classify **endpoint response-hole families**.
The four edges above are residual `q` edges.  Bare support equality does not
turn this q-edge `K2,2` into cross-intersecting endpoint holes or an exact
joint-kernel source direction.

The smallest coefficient guard is already the original diagonal return:

```text
x01^00 =  1,   x45^22 = -1,
x05^02 =  1,   x14^02 =  1.
```

Then `A=-B` on its singleton common word support.  There is no off-diagonal
cell on the off-anchor edge and no endpoint-hole family has been supplied.
This is a genuine coefficient-level counterguard to promoting the support
rectangle theorem directly to strict Hall or deletion.  It is not a full
five-tensor source.

The exact next input is therefore source-labelled: either lift this
residual q-edge `K2,2` to cross-intersecting response holes using the
complete companion rows, or use a cofactor/Euler identity to construct a
complete-column kernel.  Further zero-support classification cannot supply
that lift.

## Verification

Run

```text
python3 computations/verify_h3_c4_zero_support_rectangle_boundary.py
python3 -O computations/verify_h3_c4_zero_support_rectangle_boundary.py
python3 -I -S computations/verify_h3_c4_zero_support_rectangle_boundary.py
```

Frozen ledger SHA-256:

```text
e716cd11480815da0fa4c8565c442ec1087feece4ffe1480c2d63f3aa9571381
```
