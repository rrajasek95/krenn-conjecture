# Laurent-fiber obstructions with one exceptional edge

This note eliminates the residual active-edge support charts arising in the
six-vertex audit with

\[
 F=\{01\}.
\]

Write the exceptional matrix as (A=A_{01}).  For every other edge
(uv), write the rank-one matrix as
(R_{uv}=x^{uv}\otimes y^{uv}), with the first factor at (u).  If a
coordinate belongs to a displayed support, its value is nonzero.

## 1. A six-variable obstruction

**Lemma 1.**  Over a field of characteristic different from two, nonzero
elements (a,b,c,d,e,f) cannot satisfy

\[
 ab+cd=0,\qquad eb+cf=0,\qquad af+ed=0.                 \tag{1}
\]

**Proof.**  The first two equations give

\[
 a=-\frac{cd}{b},\qquad e=-\frac{cf}{b}.
\]

Consequently

\[
 af+ed=-\frac{cdf}{b}-\frac{cfd}{b}
       =-\frac{2cdf}{b}\ne0,
\]

contrary to the third equation. □

## 2. The two sparse residual charts

For an edge (uv), the table records
((\operatorname{supp}x^{uv},\operatorname{supp}y^{uv})).  These are the
two support representatives returned by the fixed-minor audit.

| edge | same omitted color | different omitted colors |
|---|---|---|
| 02 | 012 / 012 | 0 / 2 |
| 03 | 0 / 1 | 012 / 012 |
| 04 | 0 / 0 | 012 / 1 |
| 05 | 012 / 2 | 0 / 0 |
| 12 | 012 / 012 | 2 / 2 |
| 13 | 1 / 1 | 012 / 012 |
| 14 | 1 / 0 | 012 / 1 |
| 15 | 012 / 2 | 2 / 0 |
| 23 | 012 / 1 | 2 / 012 |
| 24 | 012 / 0 | 0 / 0 |
| 25 | 2 / 2 | 1 / 1 |
| 34 | 2 / 2 | 1 / 1 |
| 35 | 0 / 0 | 012 / 0 |
| 45 | 1 / 1 | 2 / 2 |

The exceptional supports are respectively

\[
 \operatorname{supp}A
 =\{00,01,02,11,21\},                                  \tag{2}
\]

and

\[
 \operatorname{supp}A
 =\{00,01,02,12,22\}.                                  \tag{3}
\]

Here a six-digit word is a vertex coloring, and a vertical-bar expression
is a perfect matching.  Direct enumeration from (2) and the left support
column gives exactly the following nonzero matching terms.

| coloring | first matching | second matching |
|---|---|---|
| 001000 | 01\|24\|35 | 04\|12\|35 |
| 001102 | 03\|15\|24 | 04\|15\|23 |
| 001111 | 01\|23\|45 | 03\|12\|45 |

All three colorings are mixed, so each row supplies a two-term coefficient
equation.  Canceling the common nonzero matching factor in each row gives
(1), with

\[
\begin{aligned}
a&=A(0,0),& b&=R_{24}(1,0),& c&=R_{04}(0,0),\\
d&=R_{12}(0,1),&e&=R_{03}(0,1),&f&=R_{23}(1,1).
\end{aligned}                                           \tag{4}
\]

Lemma 1 therefore excludes the same-omitted-color chart.

For (3) and the right support column, the corresponding exact fibers are

| coloring | first matching | second matching |
|---|---|---|
| 000100 | 01\|24\|35 | 05\|13\|24 |
| 002110 | 02\|14\|35 | 05\|14\|23 |
| 002122 | 01\|23\|45 | 02\|13\|45 |

After canceling the common factors, these again give (1), now with

\[
\begin{aligned}
a&=A(0,0),&b&=R_{35}(1,0),&c&=R_{05}(0,0),\\
d&=R_{13}(0,1),&e&=R_{02}(0,2),&f&=R_{23}(2,1).
\end{aligned}                                           \tag{5}
\]

Thus Lemma 1 excludes the different-omitted-colors chart as well.

Equivalently, in either chart the ratios of the first and second matching
terms in the three rows have an odd signed exponent relation.  Each ratio
must equal (-1), while their signed product cancels to (1); hence
(1=-1).  This is the shortest Laurent interpretation of the same proof.

## 3. The full-​(A) chart exposed by the new cuts

After adding the preceding odd-fiber cuts, the support CEGAR exposes one
further chart with all nine entries of (A) nonzero.  Its rank-one endpoint
supports are

| edge | supports | edge | supports |
|---|---|---|---|
| 02 | 012 / 2 | 03 | 012 / 012 |
| 04 | 1 / 1 | 05 | 012 / 0 |
| 12 | 012 / 2 | 13 | 012 / 012 |
| 14 | 012 / 1 | 15 | 0 / 0 |
| 23 | 2 / 2 | 24 | 0 / 0 |
| 25 | 1 / 1 | 34 | 012 / 1 |
| 35 | 012 / 0 | 45 | 2 / 2 |

For a supported matching (M) at coloring (c), let (p(c,M)) be its
nonzero Laurent monomial in the exceptional entries and rank-one endpoint
factors.  The following two mixed fibers have exactly three terms:

| coloring | term 0 | term 1 | term 2 |
|---|---|---|---|
| (E=000100) | 01\|24\|35 | 03\|15\|24 | 05\|13\|24 |
| (G=002010) | 02\|14\|35 | 02\|15\|34 | 05\|12\|34 |

Denote their terms by (E_0,E_1,E_2) and (G_0,G_1,G_2).  Seven other
mixed fibers are binomials.  Orient each ratio by the matching order shown:

| coloring (c) | numerator matching | denominator matching |
|---|---|---|
| 001111 | 01\|25\|34 | 03\|14\|25 |
| 012010 | 02\|14\|35 | 05\|12\|34 |
| 012110 | 02\|14\|35 | 05\|12\|34 |
| 001011 | 01\|25\|34 | 03\|14\|25 |
| 002022 | 02\|13\|45 | 03\|12\|45 |
| 110000 | 01\|24\|35 | 05\|13\|24 |
| 110100 | 01\|24\|35 | 05\|13\|24 |

Writing the corresponding ratio as ρ_c, every binomial equation says
ρ_c=-1.  Direct cancellation of endpoint-factor exponents gives

\[
 \frac{E_1/E_0}{G_1/G_0}
 =\rho_{001111}^{-1}\rho_{012010}\rho_{012110}^{-1}
 =-1,                                                   \tag{6}
\]

and

\[
 \frac{E_2/E_0}{G_2/G_0}
 =\rho_{001011}^{-1}\rho_{002022}
  \rho_{110000}\rho_{110100}^{-1}
 =1.                                                    \tag{7}
\]

Set (r=G_1/G_0) and (s=G_2/G_0), both nonzero.  Dividing the two
trinomial coefficient equations by (E_0) and (G_0), then applying
(6)--(7), yields

\[
 1-r+s=0,\qquad 1+r+s=0.                                \tag{8}
\]

Their difference is (2r=0), impossible over the complex numbers.  Hence
the full-​(A) chart is also unrealizable.

## 4. Exact audit

Run

```text
.venv/bin/python computations/verify_one_exceptional_edge_obstruction.py
```

The checker independently enumerates all fifteen perfect matchings for
every displayed coloring.  It verifies that the fibers have exactly the
claimed sizes and checks (6)--(7), as well as both sparse odd cycles, by
integer equality of full formal exponent vectors.  Floating-point
calculation is not used.
