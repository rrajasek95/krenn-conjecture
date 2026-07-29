# The eighth split: common-pole closure of \((3^3,2^5)\)

## 1. Result

Consider the profile

\[
                       (h,k;\lambda)=(8,1;(3^3,2^5)).       \tag{1}
\]

Thus \(p=9\), there are three triple values \(a,b,c\), and there are five
double values.  All repeated exceptional values are nonzero, distinct, and
nonopposite.

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

The proof compares the three legal constant-residual selections according
to which triple is selected only twice.  The inherited common value
satisfies

\[
                              \mu\ne0.                       \tag{2}
\]

This is part of the standing cyclic three-zero residual, not a genericity
assumption: the cyclic ports give the two nonzero centre beta values
\(\mu\ne0\) and the three zero-site beta values \(-\mu\), as recorded in
equation (6) of
[live-three-zero-common-power-star-injectivity.md](live-three-zero-common-power-star-injectivity.md)
and at the start of
[live-three-zero-common-beta-all-orders.md](live-three-zero-common-beta-all-orders.md).
Consequently \(\mu=0\) is not a residual subcase requiring a separate
argument.

## 2. Three constant-residual selections

Assume that all isolated-star pivots vanish.  For each
\(x\in\{a,b,c\}\), select the other two triples fully and select two labels
from \(x\).  In multiplicity notation,

\[
                         R_x=x^2y^3z^3,
                         \qquad\{x,y,z\}=\{a,b,c\}.          \tag{3}
\]

The unselected mate at \(x\) is a singleton in the complement.  The five
double classes are untouched, so the complement has

\[
                             1+5\cdot2=11=p+2              \tag{4}
\]

labels.  Since (3) represents three value classes, the Hermite numerator
has degree at most \(p+3-1=11\).  Division by all complementary row roots
therefore leaves a nonzero constant residual.

The rational dependence has denominator degree

\[
                         2+3+4+4=13,                        \tag{5}
\]

and numerator degree eleven.  It is \(O(z^{-2})\) at infinity.  Every
selected value pole has zero simple residue, so the residue theorem forces
the residue at the remaining double pole \(-\mu\) to vanish.  As in the
preceding \((4,3^5)\) closure, this is a scalar logarithmic-derivative
equation because the residual is constant.

## 3. Swapping the full and partial roles

Relative to an unselected class, selecting \(r\) labels of value \(x\)
changes the logarithmic derivative of the regular cofactor at \(-\mu\) by

\[
                 \Delta_r(x)={r\over x+\mu}-{r+1\over x-\mu}. \tag{6}
\]

The five double classes contribute the same constant in all three
selections.  So does the sum of the full-triple contributions, except that
the partial value \(x\) uses \(\Delta_2(x)\) in place of
\(\Delta_3(x)\).  The three common-pole equations therefore force the same
value of

\[
\begin{split}
 \Gamma(x)&=\Delta_3(x)-\Delta_2(x)\\
           &={1\over x+\mu}-{1\over x-\mu}
             =-{2\mu\over x^2-\mu^2}                       \tag{7}
\end{split}
\]

at \(x=a,b,c\).

All denominators in (7) are structurally nonzero.  For two distinct triple
values \(x,y\), equality \(\Gamma(x)=\Gamma(y)\), together with (2), gives

\[
 {1\over x^2-\mu^2}={1\over y^2-\mu^2}
 \quad\Longrightarrow\quad
                       (x-y)(x+y)=0.                       \tag{8}
\]

The first factor is excluded by distinctness of value classes and the
second by the structural no-opposite condition.  Thus even two of the
three equations are incompatible.  This contradiction proves Theorem 1.1.

## 4. Exact audit

[verify_live_three_zero_eighth_split_33322222_common_pole_closure.py](../computations/verify_live_three_zero_eighth_split_33322222_common_pole_closure.py)
checks all three selections, complement and degree counts, derives (7)
symbolically, and clears the difference of two role values to the exact
factor

\[
 {2\mu(x-y)(x+y)\over
  (x^2-\mu^2)(y^2-\mu^2)}.
\]
