# An order-three tight/free counterexample via interpolation

The implication

> integer-tight support + free support + ordinary subrank at least three
> implies monomial subrank at least three

is false already for a `3 x 3 x 5` tensor.  This example has all support
coefficients equal to one and admits a short exact restriction to the
rank-three diagonal tensor.

## The tensor

Let the first two local bases be indexed by `0,1,2`, and let the third be
indexed by `0,1,2,3,4`.  Set

\[
 T=\sum_{0\leq i,j\leq 2} e_i\otimes e_j\otimes e_{4-i-j}.
\tag{1}
\]

Its support is integer-tight: use

\[
 \alpha_1(i)=i,\qquad \alpha_2(j)=j,\qquad
 \alpha_3(k)=k-4.
\tag{2}
\]

All three maps are injective on their local alphabets and their sum is zero
on every support tuple.  The support is also free, since any two coordinates
of a tuple in (1) determine the third.

## Exact subrank-three restriction

Use the three interpolation nodes

\[
 R=\{-1,0,1\}.
\]

For `r in R`, let `L_r(x)` be the quadratic Lagrange polynomial satisfying
`L_r(s)=delta_{r,s}` for `s in R`.  Explicitly, in coefficient order
`1,x,x^2`,

\[
 \begin{array}{c|ccc}
 r=-1&0&-1/2&1/2\\
 r=0 &1&0&-1\\
 r=1 &0&1/2&1/2.
 \end{array}
\tag{3}
\]

Take the first and second restriction matrices to have these three rows.
Take the row of the third restriction matrix indexed by `r` to be

\[
 C_{r,k}=r^{4-k}\qquad(0\leq k\leq4),
\tag{4}
\]

where `0^0=1`.  Thus its three rows are

\[
 (1,-1,1,-1,1),\qquad(0,0,0,0,1),\qquad(1,1,1,1,1).
\tag{5}
\]

If output coordinates `a,b,c` correspond to nodes `r_a,r_b,r_c`, the
resulting coefficient is

\[
 \begin{aligned}
 \sum_{i,j=0}^2 [x^i]L_{r_a}(x)[x^j]L_{r_b}(x)
 C_{r_c,4-i-j}
 &=\sum_{i,j=0}^2 [x^i]L_{r_a}(x)[x^j]L_{r_b}(x)
 r_c^{i+j}\\
 &=L_{r_a}(r_c)L_{r_b}(r_c)\\
 &=\delta_{a,c}\delta_{b,c}.
 \end{aligned}
\tag{6}
\]

Hence the image is exactly `Delta_3`.  The first two local dimensions are
three, so

\[
 Q(T)=3.
\tag{7}
\]

## Monomial subrank is only two

A size-three monomial restriction must retain all three first coordinates,
all three second coordinates, and three distinct third coordinates.  The
numbers of support entries over third symbols `k=0,1,2,3,4` are

\[
 1,2,3,2,1,
\tag{8}
\]

respectively.  Any three third symbols therefore retain at least four
support entries, whereas a monomial image equal to `Delta_3` may retain only
the three diagonal entries.  Thus `Q_mon(T)<3`.

Keeping first/second symbols `{0,2}` and third symbols `{0,4}` leaves exactly
the tuples `(0,0,4)` and `(2,2,0)`, so `Q_mon(T)=2`.

Consequently, any successful subrank-to-support argument for the Krenn
problem must use genuinely perfect-matching-specific structure: even order,
the fact that one local edge occurrence fixes a symbol at a second endpoint,
and alternating-cycle completion.  Integer tightness and freeness alone do
not suffice.

## Why direct symbol cloning cannot lift the example

A tempting lift replaces a local symbol `e_i` by the paired endpoint symbol
`e_i tensor e_i`.  After arbitrary maps on the two cloned sites, one source
column has the form

\[
                         u_i\otimes v_i,
\tag{9}
\]

so it is a decomposable `3 x 3` matrix.  On the other hand, the two-site
Schmidt support of `Delta_3` is

\[
 D=\operatorname{span}\{e_0\otimes e_0,e_1\otimes e_1,
                         e_2\otimes e_2\}.
\tag{10}
\]

The only nonzero decomposable tensors in `D` are its three coordinate
axes: a diagonal matrix has rank one only when exactly one diagonal entry
is nonzero.  More invariantly, if `(p_a)` and `(q_a)` are bases, then the
only decomposable points of
`span{p_a tensor q_a}` are the three displayed points.

Thus any clone whose individual column is forced to remain in the target's
two-site Schmidt support becomes monomial.  The Lagrange columns in (3)
have two or three nonzero entries, so their diagonal lifts have matrix rank
greater than one and cannot factor as (9).  A perfect-matching gadget could
only evade this obstruction by adding further matchings whose off-diagonal
parts cancel collectively.  The exact analysis of the smallest such
degree-four gadget is in `notes/octahedral-incidence-obstruction.md`; its
extra matchings still force a rank-four flattening.
