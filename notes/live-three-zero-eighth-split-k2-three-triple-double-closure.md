# The eighth split at \(k=2\): three-triple/two-double closure

## 1. Result

At the current \(h=8,\ k=2\) frontier, consider either multiplicity
profile

\[
                    3^3 2^3 1^5,qquad 3^3 2^2 1^7.       \tag{1}
\]

Both have three triple value classes and at least two double value classes.

**Theorem 1.1.**  Both profiles in (1) are impossible on the
no-extra-singular stratum.

The proof uses only legal three-class cores, so every Hermite residual is
a nonzero constant.  The three \((3,3,2)\) permutations on the triple
values first determine the common first- and second-log-jet totals.  A
mixed core using two triples and one double then gives a cubic in the
omitted triple value.  The three triple values determine that cubic up to
scale.  Two different double values would therefore give proportional
points on an invertibly transformed twisted cubic, which is impossible.

As a result, the six-profile frontier in
[the post-role census](live-three-zero-eighth-split-k2-post-role-census.md)
shrinks to four profiles.

## 2. Universal order-two residue equation

Put \(w=z+\mu\).  For a selected role of multiplicity \(r\) at an
exceptional value \(v\), use the normalized common-pole factor

\[
 \widehat\rho_{r,v}(w)=
 \left(1-{w\over v+\mu}\right)^{-r}
 \left(1+{w\over v-\mu}\right)^{-(r+1)}.                 \tag{2}
\]

Its first two logarithmic jets are

\[
 \phi_r(v)={r\over v+\mu}-{r+1\over v-\mu},\qquad
 \psi_r(v)={r\over(v+\mu)^2}+{r+1\over(v-\mu)^2}.       \tag{3}
\]

Rewriting each selected-class factor against the full exceptional
multiset gives one unit \(U(w)\), independent of the chosen core.  Set

\[
                  \alpha=(\log U)'(0),\qquad
                  \beta=(\log U)''(0).                  \tag{4}
\]

Every core below selects eight labels in three value classes and leaves a
singleton in its complement.  The simultaneous-Hermite residual is thus
a nonzero constant.  The common pole has order three, and its zero residue
is exactly

\[
 \left(\alpha+\sum_v\phi_{r_v}(v)\right)^2
       +\beta+\sum_v\psi_{r_v}(v)=0.                     \tag{5}
\]

The scalar constant residual cancels from (5).  Because the background in
(4) was formed from the full multiset, the same \(\alpha,\beta\) occur for
the triple-only and mixed cores.

## 3. Fixing the triple totals

Let \(x_1,x_2,x_3\) be the three triple values, and define

\[
 T_3=\alpha+\sum_{i=1}^3\phi_3(x_i),\qquad
 W_3=\beta+\sum_{i=1}^3\psi_3(x_i).                      \tag{6}
\]

For each \(x_i\), select two labels there and three labels at each of the
other two triples.  This is a legal \((3,3,2)\) core because the role-two
triple leaves one complementary label.  Put

\[
\begin{split}
 d(x)&=\phi_3(x)-\phi_2(x)=-{2\mu\over x^2-\mu^2},\\
 \Delta(x)&=\psi_3(x)-\psi_2(x)
             =d(x)^2-{d(x)\over\mu}.                     \tag{7}
\end{split}
\]

Equation (5) for the core distinguished at \(x_i\) becomes

\[
                 T_3^2+W_3+\left({1\over\mu}-2T_3\right)
                 d(x_i)=0.                               \tag{8}
\]

For distinct, nonopposite values,

\[
 d(x)-d(x')={2\mu(x-x')(x+x')\over
              (x^2-\mu^2)(x'^2-\mu^2)}\ne0.             \tag{9}
\]

The standing reduction has \(\mu\ne0\).  Subtracting two instances of
(8), and then substituting back, gives the exact totals

\[
                         T_3={1\over2\mu},\qquad
                         W_3=-{1\over4\mu^2}.             \tag{10}
\]

## 4. The mixed triple--double equation

Fix a double value \(y\) and omit one triple value \(x\).  Select all
three labels at each of the other two triples and both labels at \(y\).
This is a \((3,3,2)\) core of size eight.  All singleton classes in (1)
are untouched, so its complement is legal, including if one of those
singletons is the possible zero value.

Using (6) and (10), equation (5) is

\[
\begin{split}
 0=E(x,y):={}&
 \bigl(\phi_2(y)-\phi_3(x)\bigr)^2
 +{\phi_2(y)-\phi_3(x)\over\mu}\\
 &+\psi_2(y)-\psi_3(x).                                  \tag{11}
\end{split}
\]

Scale

\[
                              X={x\over\mu},\qquad
                              Y={y\over\mu}.              \tag{12}
\]

Every denominator below is nonzero.  Clearing (11) gives the exact
factorization

\[
 \mu^2 E(x,y)=
 { (X-Y)Q_Y(X)\over
   (X^2-1)^2(Y^2-1)^2},                                  \tag{13}
\]

where, in ascending powers of \(X\), the coefficient vector of \(Q_Y\)
is

\[
\mathbf c(Y)=
\begin{pmatrix}
 -(5Y-1)(7Y^2+4Y+1)\\
 -11Y^3-37Y^2-Y+1\\
 -Y^3+Y^2+37Y+11\\
 -(Y-5)(Y^2+4Y+7)
\end{pmatrix}.                                            \tag{14}
\]

The values \(x\) and \(y\) belong to different value classes, so
\(X-Y\ne0\).  It follows from (11)--(13) that all three scaled triple
values \(X_1,X_2,X_3\) are roots of \(Q_Y\).

## 5. Twisted-cubic injectivity

Expanding (14) in powers of \(Y\) gives

\[
 \mathbf c(Y)=M
 \begin{pmatrix}1\\Y\\Y^2\\Y^3\end{pmatrix},\qquad
 M=
 \begin{pmatrix}
 1&-1&-13&-35\\
 1&-1&-37&-11\\
 11&37&1&-1\\
 35&13&1&-1
 \end{pmatrix}.                                          \tag{15}
\]

Direct elimination gives

\[
                              \det M=1327104\ne0.          \tag{16}
\]

In particular, \(Q_Y\) is never the zero polynomial.  Since it has the
three distinct roots \(X_1,X_2,X_3\), it must have degree three and is a
nonzero scalar multiple of

\[
                              H(X)=\prod_{i=1}^3(X-X_i).  \tag{17}
\]

Now choose two distinct double values \(y,y'\), available in both
profiles (1).  Equations (14) and (17) make
\(\mathbf c(Y)\) and \(\mathbf c(Y')\) proportional.  Applying
\(M^{-1}\) in (15) makes

\[
             (1,Y,Y^2,Y^3)\quad\hbox{and}\quad
             (1,Y',Y'^2,Y'^3)                            \tag{18}
\]

proportional.  Their first coordinates force the proportionality scalar
to be one, and their second coordinates then force \(Y=Y'\).  Hence
\(y=y'\), contradicting the distinctness of the two double value classes.
This proves Theorem 1.1.

## 6. Updated exact frontier

Removing (1) from the six profiles in the preceding census leaves exactly

\[
\begin{array}{c|c|l}
c&e&\lambda\\ \hline
10&10&2^{10}\\
10&10&3\,2^8 1\\
11& 9&2^9 1^2\\
11& 9&3\,2^7 1^3.
\end{array}                                                \tag{19}
\]

Thus the next target remains \(2^{10}\).  The updated residual count at
\((h,k)=(8,2)\) is four.

## 7. Exact audit

[verify_live_three_zero_eighth_split_k2_three_triple_double_closure.py](../computations/verify_live_three_zero_eighth_split_k2_three_triple_double_closure.py)
checks every core and complement in both profiles, the constant-residual
degree, the universal order-two residue equation, (7)--(10), the complete
factorization (13), every coefficient in (14), the determinant (16), the
projective twisted-cubic injection, and the four-profile update (19).
