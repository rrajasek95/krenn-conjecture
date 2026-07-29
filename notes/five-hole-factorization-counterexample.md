# An exact mixed-basis five-hole factorization

## 1. Outcome

The hoped-for universal obstruction

\[
                  \Delta_{5,3}\ne[X\,Y\,D\,Q]_{1^5}    \tag{1}
\]

is false.  There is an exact rational factorization with all five local
triples `(x_i,y_i,d_i)` invertible.  Its zero-cross masks for the pair
`(X,Y)` are, after a colour relabeling,

\[
                           (1,1,1,6,6).                 \tag{2}
\]

Thus it lies exactly on the exceptional `011166` union-five incidence row.
This does **not** contradict the full-row square obstruction in
[`n8-011166-full-row-square-obstruction.md`](n8-011166-full-row-square-obstruction.md).
The construction realizes the common-annihilator five-hole response at one
incidence row.  It does not realize the surrounding six-site equation and
all two-hole scalar cofactors which that obstruction uses.
In fact, the exact audit in
[`five-hole-factorization-two-hole-nonlift.md`](five-hole-factorization-two-hole-nonlift.md)
shows that this particular point fails the very first omitted layer: each
of its five complementary four-site hafnians is nonzero when the two-hole
equations require zero.

The example also shows that the coordinate-monomial theorem in
[`five-hole-monomial-factor-obstruction.md`](five-hole-monomial-factor-obstruction.md)
is a genuine boundary statement.  Four of the five local bases below are
mixed; their mixing is exactly what repairs the directed-cut obstruction.

## 2. A normalized response

First use a species basis in which

\[
                  x_i=e_0,\qquad y_i=e_1,\qquad d_i=e_2
                                                               \tag{3}
\]

at every site.  Let the columns of the following five invertible matrices
be three local rank-one component vectors:

\[
\begin{aligned}
M_0&=I,\\
M_1&=\begin{pmatrix}0&1&4\\1&0&3\\0&0&-3\end{pmatrix},&
M_2&=\begin{pmatrix}0&4&1\\0&-3&0\\1&3&0\end{pmatrix},\\
M_3&=\begin{pmatrix}-4&0&0\\3&0&1\\3&1&0\end{pmatrix},&
M_4&=\begin{pmatrix}0&4/3&4/3\\1&0&1\\1&1&0\end{pmatrix}.
                                                               \tag{4}
\end{aligned}
\]

Their determinants are

\[
                         1,\ 3,\ 3,\ 4,\ 8/3.          \tag{5}
\]

There is a unique normalized quadratic `Q` for which

\[
 [e_0e_1e_2Q]_{1^5}
       =\sum_{r=0}^2\bigotimes_{i=0}^4 M_i e_r.         \tag{6}
\]

All ninety entries of its ten edge matrices are nonzero.  In lexicographic
edge order they are

\[
\begin{array}{c|c@{\qquad}c|c}
01&\begin{psmallmatrix}-8/9&-1&1\\-1&-1/2&3/4\\-1&-3/4&1\end{psmallmatrix}&
02&\begin{psmallmatrix}-8/9&1&-1\\-1&1&-3/4\\-1&3/4&-1/2\end{psmallmatrix}\\[6pt]
03&\begin{psmallmatrix}16/9&-1&-1\\1&-1/2&-3/4\\1&-3/4&-1/2\end{psmallmatrix}&
04&\begin{psmallmatrix}-8/9&-1&-1\\-1&-1/2&-3/4\\-1&-3/4&-1/2\end{psmallmatrix}\\[6pt]
12&\begin{psmallmatrix}16/9&-1&1\\1&-1/2&3/4\\-1&3/4&-1/2\end{psmallmatrix}&
13&\begin{psmallmatrix}-8/9&1&1\\-1&1&3/4\\1&-3/4&-1/2\end{psmallmatrix}\\[6pt]
14&\begin{psmallmatrix}16/9&1&1\\1&1&3/4\\-1&-3/4&-1/2\end{psmallmatrix}&
23&\begin{psmallmatrix}-8/9&1&1\\1&-1/2&-3/4\\-1&3/4&1\end{psmallmatrix}\\[6pt]
24&\begin{psmallmatrix}16/9&1&1\\-1&-1/2&-3/4\\1&3/4&1\end{psmallmatrix}&
34&\begin{psmallmatrix}-8/9&-1&-1\\1&1&3/4\\1&3/4&1\end{psmallmatrix}.
\end{array}                                             \tag{7}
\]

Equation (6) is checked coefficientwise for all `3^5=243` words.

## 3. Undoing the local bases

Put

\[
                         U_i=M_i^{-1}.                  \tag{8}
\]

Take the three columns of `U_i` to be the actual vectors `x_i,y_i,d_i`,
and transform every edge block by

\[
                         A_{ij}=U_iQ_{ij}U_j^T.          \tag{9}
\]

Applying `tensor_i U_i` to (6) gives the desired exact identity

\[
                         [X\,Y\,D\,A]_{1^5}
                                  =\Delta_{5,3}.        \tag{10}
\]

No approximation or choice of algebraic roots is involved.

The cross products `x_i cross y_i` have zero masks

\[
                              (3,3,4,4,4)               \tag{11}
\]

in the displayed colour order.  Sending old colour `2` to new colour `0`
turns (11) into (2).  The `D` family visibly has coordinate anchors of all
three colours: `d_0=e_2`, `d_2=e_0`, and `d_3=e_1`, as required by the
one-slice covering lemma.

## 4. Consequence for the union-five route

The common-annihilator equation alone cannot eliminate even the hardest
union-five incidence row.  A successful continuation must retain at least
one of the structures absent from (10):

* the arbitrary row at the sixth site, including its two one-cross
  responses;
* the fact that all `d_i` are rows of the same five edge maps from that
  sixth site; or
* the simultaneous scalar two-hole cofactors of the common internal
  quadratic.

The `011166` square proof uses the third item and therefore survives this
countermodel.  For the other twelve residual rows, a five-hole-only
factorization obstruction is no longer a viable target.

For this exact rational point, the third item is already decisive.  All
five required two-hole scalar cofactors fail, for every assignment of two
of the three factor families as `X,Y`; see
[`five-hole-factorization-two-hole-nonlift.md`](five-hole-factorization-two-hole-nonlift.md).

## 5. Exact audit

Run

```text
.venv/bin/python computations/verify_five_hole_factorization_counterexample.py
```

The checker verifies (5)--(7), constructs all five inverses and the ten
transformed blocks (9), enumerates every coefficient of (10) over the
rationals, and audits the mask relabeling (11) to `11166`.
