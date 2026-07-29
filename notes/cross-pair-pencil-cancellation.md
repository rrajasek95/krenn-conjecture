# Cross-pair pencils: an exact six-site descent criterion and a binary cancellation

## 1. Outcome

Degree-two boundary families from genuinely different deleted pairs can
cancel defects which no cap at either pair can remove by itself.  In the
exact rational binary `Delta_(8,2)` source used in the cap obstructions,
take the all-colors product caps at pairs `12` and `13`.  After identifying
their six surviving sets and swapping two boundary slots, their
denominator-cleared pair families `A,B` satisfy

\[
\begin{aligned}
 H_6(A+tB)={}&(t+1)(t^2+4)e_0^{\otimes6}\\
 &+{(t-2)(8t^2-7t-16)\over8}e_1^{\otimes6}\\
 &-{(t-2)(t+2)(2t+1)\over2}e_{101111}.                  \tag{1}
\end{aligned}
\]

Both endpoint families are dirty:

\[
             H_6(A)=4\Delta_{6,2}+2e_{101111},\qquad
             H_6(B)=\Delta_{6,2}-e_{101111}.             \tag{2}
\]

Nevertheless `t=-2` and `t=-1/2` kill the mixed coefficient while retaining
both pure coefficients.  For example,

\[
                         H_6(A-2B)
               =-8e_0^{\otimes6}-15e_1^{\otimes6}.       \tag{3}
\]

One diagonal normalization at one boundary vertex gives `Delta_(6,2)`.
Thus the polarized obstruction at one fixed pair does not globalize across
different pairs: their contaminants can cancel inside one genuine hafnian,
not merely in a formal sum of tensors.

For three colors, the same calculation gives a precise descent test.  The
726 mixed coefficient polynomials of a two-cap pencil have degree at most
three.  Their univariate gcd detects whether they have a common zero, and a
one-line square-free-factor test detects whether some such zero retains all
three pure amplitudes.  If it does, the two boundary families produce an
ordinary six-site ternary realization, contradicting the proved six-site
theorem.  Hence every hypothetical larger ternary source must fail this
test for every alignment of every two cap families.

The exact audit of (1)--(3) is
`computations/verify_cross_pair_pencil_cancellation.py`.

## 2. The two-family pencil criterion

Let `A=(A_uv)` and `B=(B_uv)` be arbitrary aggregate edge matrices on six
named sites, with local dimension `q`.  Put

\[
                         T(t)=H_6(A+tB).                  \tag{4}
\]

For a coloring `c`, write `f_c(t)=T(t)_c`.  Every perfect matching has
three edges, so every `f_c` has degree at most three.  Let

\[
 h(t)=\prod_{i=0}^{q-1}f_{i^6}(t).                       \tag{5}
\]

If at least one mixed polynomial is nonzero, let

\[
       g(t)=\gcd\{f_c(t):c\text{ mixed and }f_c\ne0\},   \tag{6}
\]

defined up to a nonzero scalar, and let

\[
                  g_{\rm sf}={g\over\gcd(g,g')}          \tag{7}
\]

be its square-free part.

**Theorem 2.1 (cross-pair pencil descent criterion).**

1. If every mixed `f_c` is identically zero, then some `t_0 in C` makes
   `T(t_0)` diagonal with all `q` diagonal coefficients nonzero if and only
   if `h` is not the zero polynomial.
2. If at least one mixed `f_c` is nonzero, such a `t_0` exists if and only if

   \[
                  \deg g\ge1\qquad\text{and}\qquad
                  g_{\rm sf}\nmid h.                     \tag{8}
   \]

For `q=3`, either conclusion gives an ordinary six-site realization of
`Delta_(6,3)` after an invertible diagonal change at one site.

**Proof.**  In the first case, if `h` is nonzero, avoid its finite zero set.
Conversely, any successful `t_0` has `h(t_0) ne 0`, so `h` cannot be the
zero polynomial.  In the second case, all mixed coefficients vanish at
`t_0` exactly when `t_0` is a common root of the nonzero mixed polynomials,
equivalently a root of their gcd `g`.  Such a common root retains every
pure coefficient exactly when `h(t_0) ne 0`.  The roots of `g_sf` are the
distinct roots of `g`; all of them are roots of `h` exactly when
`g_sf` divides `h`.  This proves (8).

At a successful `t_0`, write

\[
                  T(t_0)=\sum_{i=0}^{q-1}d_i e_i^{\otimes6},
                         \qquad d_i\ne0.                 \tag{9}
\]

Apply `diag(d_0^(-1),...,d_(q-1)^(-1))` at one site to every incident
edge matrix.  Every perfect matching uses exactly one such endpoint, so
(9) becomes the normalized diagonal target. `QED`

Multiplying either family by a nonzero scalar only rescales or
reparametrizes the pencil, so it does not change whether a successful point
exists.  The criterion also applies when `A,B` came from different original
six-sets: choose endpoint-order-preserving local identifications with one
abstract six-set first.

For `q=3`, the established arbitrary-matrix six-site obstruction gives the
following necessary cross-pair rigidity for a hypothetical larger source.

**Corollary 2.2.**  Take any two product caps (possibly at different
deleted pairs) with nonzero scalar components, form their normalized or
denominator-cleared degree-two boundary families, and identify their six
surviving spaces with six copies of `C^3`.  Then their pencil has neither
successful branch of Theorem 2.1.  Explicitly, if all its mixed
coefficients vanish identically, at least one constant-color coefficient
vanishes identically.  Otherwise, either its mixed gcd is constant, or
every common zero of its mixed coefficients kills at least one of the three
constant-color coefficients.

This statement couples genuinely different deleted pairs.  It is stronger
than saying that each cap separately is dirty: equation (1) shows that two
dirty endpoints of a pencil can have clean interior points.

## 3. The exact binary source

On vertices `1,...,8`, use the nonzero tensors

\[
\begin{array}{c|c}
12&(e_0+e_1)e_0\\
34,24&e_0e_0\\
13&-e_1e_0\\
16,23&e_1e_1\\
45&\frac34e_1e_1\\
15,46&\frac12e_1e_1\\
57,68&e_0e_0\\
78&e_1e_1.
\end{array}                                               \tag{10}
\]

Its matching tensor is exactly `Delta_(8,2)`.  Cap either deleted pair by

\[
                  \epsilon\otimes\epsilon,
             \qquad \epsilon=e_0^*+e_1^*.               \tag{11}
\]

For a pair `p,q`, let `F_2^(pq)` denote the degree-two component of the
complete capped boundary signature.  It is the denominator-cleared family

\[
 F_{2,uv}^{(pq)}=s_{pq}A_{uv}
  +\sum_{i,j=0}^1\left(
       A_{pu}(i,{\cdot})A_{qv}(j,{\cdot})
      +A_{pv}(i,{\cdot})A_{qu}(j,{\cdot})\right),        \tag{12}
\]

where `s_pq` is the sum of all four entries of `A_pq`.

For `pq=12`, order the surviving vertices as

\[
                         (3,4,5,6,7,8).                  \tag{13}
\]

For `pq=13`, first order them as `(2,4,5,6,7,8)` and then interchange the
third and fourth positions.  Identify both ordered lists with abstract
sites `(0,1,2,3,4,5)`, and call the resulting families

\[
                         A=F_2^{(12)},\qquad B=F_2^{(13)}.\tag{14}

The cap scalars are `s_12=2` and `s_13=-1`.  Direct expansion gives the two
endpoint values in (2).  More strongly, enumeration of all fifteen
matchings and all 64 binary colorings gives exactly the three nonzero rows
in (1); every other coloring fiber is empty.

The mixed gcd in Theorem 2.1 is therefore

\[
                  g(t)=(t-2)(t+2)(2t+1),                 \tag{15}
\]

up to a scalar.  Its root `2` kills the color-one coefficient, but its
other two roots do not:

\[
\begin{array}{c|cc}
t&f_{0^6}(t)&f_{1^6}(t)\\ \hline
-2&-8&-15\\
-1/2&17/8&105/32.
\end{array}                                               \tag{16}
\]

Thus `g_sf` does not divide the product of the two pure polynomials, and
Theorem 2.1 recovers both exact clean points.

## 4. Consequence for the uniform route

The fixed-pair polarized obstruction is real, but it is not stable under
coupling different deletions: (3) is a literal cancellation inside the
cubic hafnian map.  A uniform proof therefore cannot rule out cross-pair
reconstruction by tracking a defect line independently at every pair.

Corollary 2.2 gives a finite algebraic target for a positive continuation.
It is enough to find two cap degree-two families whose 726 mixed cubic
polynomials have a nonconstant gcd with at least one root outside the three
pure zero sets.  Conversely, a hypothetical larger ternary source must
force the stated root-cover obstruction simultaneously for every pair of
caps and every boundary alignment.  That simultaneous constraint is the
new cross-pair datum absent from the one-pair cumulant analysis.
