# The uniform dense six-site point has no cyclic eigencontact

## Outcome

At the maximally dense six-site leading point

\[
                         C_{ij}=\alpha\qquad(i<j),
             \qquad 15\alpha^3=1,                         \tag{1}
\]

all fifteen pair cofactors are nonzero.  Nevertheless, no complete binary
contact direction can span a one-dimensional eigenspace under cyclic
translation of the six vertices.

More precisely, after the common scale is removed, such a directed first
jet has five offset values and a sixth-root character

\[
       b_{i,i+d}=\zeta^i x_d,\qquad d=1,\ldots,5,
                         \qquad\zeta^6=1.                  \tag{2}
\]

and the tangent equations give `x_1+...+x_5=0`.  The pair equations uniquely
determine every second block.  Exact matching enumeration then leaves nine
cyclic-orbit equations in the four variables `x_1,...,x_4`.  For the fixed
character `zeta=1`, their ideal is the unit ideal over `Q`.  The accompanying
checker constructs and verifies an explicit extended-Buchberger identity

\[
                              1=\sum_w q_w f_w.             \tag{3}
\]

The other three rational cyclotomic cases `Phi_2`, `Phi_3`, and `Phi_6` also
give exact unit ideals.  Thus the obstruction holds for every sixth-root
character over every characteristic-zero field.  It excludes, in
particular, any all-three-face cofactor-plane survivor at (1) whose
orbit-normalizing basis contains a complete-contact eigensection.

This is a rigorous dense symmetric-chart obstruction, not a classification
of all six planes in `Gr(2,4)^6`.  Cyclic symmetry which mixes or swaps the
two selected contact lines, and noncyclic contacts through (1), are not
covered.

## 1. Dimensionless binary lift

Put `C_ij=1` temporarily and multiply every cell of the final source by
`alpha`.  The dimensionless leading hafnian, pair cofactors, and
four-deletion cofactors are

\[
                   h_\varnothing=15,\qquad h_{ik}=3,
                   \qquad h_{ikj\ell}=1.                  \tag{4}
\]

Because a six-site matching uses three cells, (1) turns the desired
dimensionless binary output `15(X_0+X_1)` into the normalized output
`X_0+X_1`.

For `i<k`, write the dimensionless binary edge block as

\[
             \widehat A_{ik}=
               \begin{pmatrix}
                    1&b_{ki}\\
                    b_{ik}&d_{ik}
               \end{pmatrix}.                              \tag{5}
\]

The one-site and two-site zero equations are exactly

\[
       3\sum_{j\ne i}b_{ij}=0,                             \tag{6}
\]

and

\[
       3d_{ik}+
       \sum_{\substack{j,\ell\notin\{i,k\}\\j\ne\ell}}
                    b_{ij}b_{k\ell}=0.                     \tag{7}
\]

Hence (2) obeys (6) precisely when

\[
                       x_5=-x_1-x_2-x_3-x_4,                \tag{8}
\]

and (7) gives the unique polynomial lift

\[
       d_{ik}=-{1\over3}
       \sum_{\substack{j,\ell\notin\{i,k\}\\j\ne\ell}}
                    b_{ij}b_{k\ell}.                       \tag{9}
\]

No localization or division by a variable occurs: the only denominator is
the fixed nonzero cofactor `3`.

## 2. The fixed-character orbit equations form the unit ideal

First take `zeta=1` in (2).  This is the pointwise translation-fixed
subchart.

For a binary word `w in {0,1}^6`, let

\[
       f_w=[X^w]H_V(\widehat A)-15\,[w=111111].             \tag{10}
\]

Equations of weights zero, one, and two hold automatically by (4), (6), and
(9).  Cyclic rotation reduces every remaining equation to the following
nine representatives.

| representative `w` | degree of `f_w` | orbit size |
|---|---:|---:|
| `000111` | 3 | 6 |
| `001011` | 3 | 6 |
| `001101` | 3 | 6 |
| `001111` | 4 | 6 |
| `010101` | 3 | 2 |
| `010111` | 4 | 6 |
| `011011` | 4 | 3 |
| `011111` | 5 | 6 |
| `111111` | 6 | 1 |

The orbit sizes account for all `42` words of weight at least three.  Direct
exact reduction gives

\[
 \left\langle
 f_{000111},f_{001011},f_{001101},f_{001111},f_{010101},
 f_{010111},f_{011011},f_{011111},f_{111111}
 \right\rangle=\langle1\rangle
 \subset\mathbb Q[x_1,x_2,x_3,x_4].                       \tag{11}
\]

There are two independent exact audits of (11).

1. SymPy's reduced grevlex Groebner basis is the singleton `[1]`.
2. A deterministic extended Buchberger pass reaches the constant after `72`
   processed S-pairs while tracking every basis element in the nine original
   generators.  The nine multipliers in (3) have respectively

   \[
   (102,96,75,44,41,40,39,23,9)                            \tag{12}
   \]

   nonzero terms and degrees

   \[
                         (9,9,9,8,9,8,8,7,6).              \tag{13}
   \]

The checker reconstructs the right side of (3) as a rational polynomial
and asserts that it is literally one.  The large multipliers need not be
trusted as opaque stored output: they are regenerated from the matching
formula (5)--(10), then independently multiplied back into the original
equations.

### The other cyclic characters

A one-dimensional representation of the six-cycle has `zeta^6=1`.  Over
`Q`, the remaining roots are partitioned by

\[
 \Phi_2(z)=z+1,\qquad
 \Phi_3(z)=z^2+z+1,\qquad
 \Phi_6(z)=z^2-z+1.                                      \tag{14}
\]

For `Phi_2`, direct substitution `z=-1` makes the complete set of 42
weight-at-least-three equations generate one in
`Q[x_1,x_2,x_3,x_4]`.  For each quadratic factor, exact grevlex reduction
gives

\[
 \big\langle f_w(x,z):|w|\ge3\big\rangle+\langle\Phi_m(z)\rangle
       =\langle1\rangle
       \subset\mathbb Q[x_1,x_2,x_3,x_4,z],
       \qquad m=3,6.                                      \tag{15}
\]

These two quotient calculations simultaneously cover both conjugate roots.
Together with (11), they exclude every character satisfying `zeta^6=1`.

## 3. Two hand-readable fixed-character reflection slices

The full unit certificate is computational, but two natural two-parameter
slices collapse by elementary equations.

### Antisymmetric offsets

Take

\[
                    (x_1,x_2,x_3,x_4,x_5)=(a,b,0,-b,-a).
                                                                  \tag{16}
\]

Three of the nine equations are

\[
 {a(2a^2+3ab+3b^2)\over3}=0,\qquad
 {4a^3(a+6b)\over9}=0,                                    \tag{17}
\]

and

\[
 {8a^6-24a^4b^2-96a^3b^3-405\over27}=0.                  \tag{18}
\]

Equation (18) makes `a` nonzero.  The quartic in (17) then gives
`b=-a/6`, while its cubic factor becomes `(19/12)a^2`, a contradiction.

### Reflection-symmetric offsets

Take

\[
             (x_1,x_2,x_3,x_4,x_5)=(a,b,-2a-2b,b,a).       \tag{19}
\]

Two cubic orbit equations, up to nonzero rational scalars, are

\[
 \begin{aligned}
 F&=4a^3+13a^2b+7ab^2+6b^3,\\
 G&=3a^3+6a^2b+4ab^2+2b^3.
 \end{aligned}                                             \tag{20}
\]

Their exact resultant is

\[
                         \operatorname{Res}_a(F,G)=-750b^9. \tag{21}
\]

Thus a common zero has `b=0`, and then either cubic gives `a=0`.  The
terminal equation at the origin is `-15=0`, again impossible.

## 4. Consequence for the cofactor-plane route

At the uniform point, each cofactor kernel is the four-space

\[
                K_i=\{(u_j)_{j\ne i}:\sum_{j\ne i}u_j=0\}.  \tag{22}
\]

The all-three-face normal form chooses a plane `L_i subset K_i` and two
ordered sections which must each be complete binary contacts.  The present
calculation says that an orbit-normalizing choice of those sections cannot
contain a one-dimensional cyclic eigensection of the form (2).  This
conclusion arrives before imposing either the binary-GHZ orbit condition on the
restricted cofactor pairing or any of the 120 mixed cubic Bianchi
equations.

The subsequent note
[`uniform-dense-cyclic-plane-obstruction.md`](uniform-dense-cyclic-plane-obstruction.md)
uses the radical of the four cubic orbit equations and one mixed Bianchi
component to exclude those mixing and swapping branches as well.  Thus only
noncyclic planes remain at the uniform leading point, while the unrestricted
dense `Gr(2,4)^6` system is still open.

The exact audit is
[`computations/verify_uniform_dense_cyclic_contact_obstruction.py`](../computations/verify_uniform_dense_cyclic_contact_obstruction.py).
