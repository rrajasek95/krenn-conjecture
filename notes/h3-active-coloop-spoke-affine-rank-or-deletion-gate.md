# Minimum support forces rank two on the arbitrary-coloop spoke fibre

## Exact affine-line theorem

Fix the pure-colour coloop edge `01` and write its four-site residual
cofactor as

\[
 C=x_1y_1+x_2y_2+x_3y_3,                             \tag{1}
\]

where

```text
x=(q23,q24,q25),       y=(q45,q35,q34).
```

Every selected `x_i` is incident with site `2`.  A perfect matching uses
exactly one edge at that site, hence no target or response occurrence can
contain two selected spokes.  Literal enumeration gives

```text
15 target occurrences:           6 use no x_i,  9 use one x_i;
90 response occurrences/head:   54 use no x_i, 36 use one x_i.
```

Therefore, after every other decorated scalar coordinate is fixed, the
complete physical source map has the exact form

\[
                         F(x)=b+Mx.                   \tag{2}
\]

There are no hidden second- or third-Hasse corrections in these three
variables.  Any protected matching-derived anchor/readout can be included as
another row of `M`; the same one-spoke argument applies.

Checker:
[verify_h3_active_coloop_spoke_affine_rank_or_deletion_gate.py](../computations/verify_h3_active_coloop_spoke_affine_rank_or_deletion_gate.py).

## Rank or exact deletion

On the full three-tail branch suppose all `x_i y_i` are nonzero.  Then all
`x_i` and all `y_i` are nonzero.  The normalized target equation

\[
                         \alpha C=\alpha y^Tx=1      \tag{3}
\]

supplies the nonzero target row `y` in `M`.  Let `Mbar` be the remaining row
map modulo this target line.

There are exactly two alternatives.

### Rank two

If

\[
                       \operatorname{rank}Mbar=2,     \tag{4}

then `rank M=3`.  The target row and two source rows span the three
coordinate selectors.  This is a positive local Fitting/coordinate result:
there is no remaining affine-accessibility obstruction in the spoke fibre.

### Rank deficient

If `rank Mbar<2`, rank-nullity gives a nonzero `xi in ker M`.  By (2),

\[
                         F(x+t\xi)=F(x)               \tag{5}

for every scalar `t`, not merely to first order.  Choose any `i` with
`xi_i != 0` and set

\[
                         t=-x_i/\xi_i.                \tag{6}

Then the `i`th occupied spoke becomes zero.  No coordinate outside the
three already occupied spokes changes, so no new scalar support is
activated.  Other spokes may also vanish; in all cases occupied support
strictly drops.

If protected anchor rows are included in `M`, (5) preserves them.  A
nonzero kernel coordinate cannot be one constrained by an independent
fixed-coordinate anchor row.  The coloop cell `alpha` and mate factors `y`
are held fixed throughout, and (3) stays normalized because `y^Txi=0`.

The checker exhausts `8*27^2=5832` exact rank systems with nonzero target
entries in `{+1,-1}` and two test rows in `{-1,0,1}^3`, reconstructing a
kernel in every deficient case.  This is a check of the implementation; the
proof is the rank-nullity argument above.

## Minimum-support consequence

At a source chosen with minimum occupied scalar support, the deficient
branch contradicts minimality by (5)-(6).  Hence

\[
 \boxed{\operatorname{rank}Mbar=2}
\]

on the full three-tail arbitrary-coloop branch.  More generally, with `k`
occupied spokes, either the quotient rank is `k-1` or the same argument
deletes one.  For `k=1` the cofactor is already monomial; for `k=2` minimum
support forces quotient rank one.

This closes the nonlinear/integration part of arbitrary-coloop entry.  The
rank-two module isolated in `4b8f87a` cannot remain invisible at a
minimum-support source.

## Why rank two is not yet the `93cf9ae` processor

The issue is physical grading and privacy, not linear algebra.  The checker
freezes a three-row restriction

\[
 \begin{pmatrix}
  1&1&1\\
  1/2&1/2&0\\
  0&1/2&1/2
 \end{pmatrix}.                                      \tag{7}
\]

It has rank three and quotient rank two.  Gaussian elimination gives the
three coordinate rows exactly:

\[
\begin{aligned}
e_1&=T-2R_{\rm right},\\
e_2&=-T+2R_{\rm left}+2R_{\rm right},\\
e_3&=T-2R_{\rm left}.
\end{aligned}                                        \tag{8}

But none of the three literal rows in (7) is private: each uses at least two
tails.  Label the first as a pure target row and the other two by different
response heads or output words.  Then the combinations (8) have no single
word, response head, fine grade, or repeated grade.

This is an exact affine row-quotient guard, not a full GHZ source.  It proves
the logical nonimplication

```text
rank two modulo target
    does not imply
a literal target-zero response coefficient with one supported occurrence.
```

The special processor of `93cf9ae` needs specifically

```text
R11[110000], R11[110011], R11[111100]
```

to be private before their alternate mates are forced.  Row reduction across
a pure target normal, different response heads, or different words cannot
replace those three coefficient equations.  It also does not set the other
two cofactor tails to zero, so it does not create the special support packet
by itself.

## Shortest remaining theorem

Upgrade the forced ungraded rank-two selector to a homogeneous physical
private-tail statement:

> Within the literal word/fine/head packet of the chosen tail, either the
> three named target-zero response rows are triangular/private, or failure
> yields a typed outside-shore, four-good, or augmented terminal dual.

No further affine integration theorem is needed.  Once this promotion is
proved, the completed special processor and Hall termination of `93cf9ae`
apply.

The result is exact at canonical h=3.  It assumes the restriction matrix
contains every protected row that must remain fixed.  The checker runs
normally, optimized, and isolated/no-site, with its frozen digest recorded
in the script.
