# A rank-one ratio rectangle excluding an `F=empty` survivor

This note excludes the following exact all-rank-one support chart on six
vertices.  An expression such as `012 x 12` denotes the Cartesian product
of the displayed row and column supports; every listed factor coordinate is
nonzero.

\[
\begin{array}{c|ccccccccccccccc}
e&01&02&03&04&05&12&13&14&15&23&24&25&34&35&45\\ \hline
\operatorname{supp}A_e
&00&22&012\!\times\!12&012\!\times\!012&21&12
&2\!\times\!12&2\!\times\!012&11&1\!\times\!12
&1\!\times\!012&00&00&12\!\times\!02&012\!\times\!02.
\end{array}                                                  \tag{1}
\]

Every `A_e` has matrix rank one.  We show directly, without a genericity
assumption, that this support cannot satisfy

\[
 H_6(A)=\Delta_{6,3}.                                       \tag{2}
\]

## 1. Four exact two-matching fibers

For `a,b in {0,1}`, let

\[
 c^{ab}=(a,1,1,1,b,1),                                     \tag{3}
\]

in vertex order `0,1,2,3,4,5`.  At each of these four colorings exactly two
perfect matchings are supported:

\[
 P=\{03,15,24\},\qquad Q=\{04,15,23\}.                    \tag{4}
\]

For completeness, the other thirteen matchings have the following uniformly
forbidden edge at every one of the four colorings (3):

\[
\begin{array}{c|c@{\qquad}c|c}
01|23|45&01&01|24|35&01\\
01|25|34&01&02|13|45&02\\
02|14|35&02&02|15|34&02\\
03|12|45&12&03|14|25&14\\
04|12|35&12&04|13|25&13\\
05|12|34&05&05|13|24&05\\
05|14|23&05&&
\end{array}                                                  \tag{5}
\]

For example, `12` requires colors `(1,2)` but has colors `(1,1)`, while
`05` requires `(2,1)` but vertex `0` has color `0` or `1`.  The two
matchings in (4) use, respectively,

\[
\begin{array}{c|ccc}
P&A_{03}(a,1)&A_{15}(1,1)&A_{24}(1,b)\\
Q&A_{04}(a,b)&A_{15}(1,1)&A_{23}(1,1),
\end{array}                                                  \tag{6}
\]

and every displayed entry is nonzero by (1).  The independent checker cited
below enumerates all fifteen matchings at all four corners.

Put

\[
 X_{ab}=A_{03}(a,1)A_{15}(1,1)A_{24}(1,b),\qquad
 Y_{ab}=A_{04}(a,b)A_{15}(1,1)A_{23}(1,1),                 \tag{7}
\]

and `rho_ab=X_ab/Y_ab`.  The three colorings `c^(00),c^(01),c^(10)` are
mixed, so (2) and the exact fibers (4) give

\[
 X_{00}+Y_{00}=X_{01}+Y_{01}=X_{10}+Y_{10}=0,
 \qquad
 \rho_{00}=\rho_{01}=\rho_{10}=-1.                         \tag{8}
\]

The fourth coloring is `c^(11)=1^6`, whose coefficient is required to be
one.

## 2. Rank-one rectangle transfer

Factor the four relevant rank-one matrices at their endpoints.  All factors
in (7) are nonzero, and cancellation of the common `A_15(1,1)` gives

\[
 \rho_{ab}
 =K\,
   \frac{x_{03}(a)}{x_{04}(a)}
   \frac{y_{24}(b)}{y_{04}(b)}                              \tag{9}
\]

for a fixed nonzero scalar `K`; the fixed endpoint factors from `03,24,23`
have been absorbed into `K`.  Thus the ratio table has rank one and obeys
the multiplicative rectangle identity

\[
 \rho_{00}\rho_{11}=\rho_{01}\rho_{10}.                   \tag{10}
\]

Substitution of (8) into (10) forces `rho_11=-1`.  Therefore

\[
 [H_6(A)]_{1^6}=X_{11}+Y_{11}=0,                            \tag{11}
\]

contrary to `[Delta_(6,3)]_(1^6)=1`.  This proves:

**Proposition 2.1.**  No choice of nonzero complex rank-one factors on the
support chart (1) realizes `Delta_(6,3)`. `QED`

## 3. General certificate and exact audit

The proof used a reusable support criterion.  For any all-rank-one chart,
the ratio of the monomials of two fixed perfect matchings factors as a
product of one-variable functions, one per vertex.  Consequently its values
on a two-vertex coloring rectangle obey (10).  If the same two matchings are
the exact supported fiber at all four corners, three mixed corners force the
fourth corner to cancel.  A constant fourth corner is an immediate
contradiction.

This criterion is implemented as `rectangle_cancellation_witness` in
`computations/verify_color_sensitive_support_obstruction.py`.  The
standalone audit

```sh
.venv/bin/python computations/verify_rank_one_ratio_rectangle.py
```

checks the chart (1), all four exact matching fibers, and the formal
rank-one exponent identity underlying (10).
