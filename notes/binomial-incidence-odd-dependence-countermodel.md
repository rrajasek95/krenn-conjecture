# Parallel colored cells refute bare binomial odd dependence

## Outcome

The proposed uniform incidence theorem is false if its constant hypothesis
only selects one normalized matching monomial in each color.  Already on six
vertices there is a 48-cell aggregate support with the following properties:

1. one chosen constant-color matching in each color has product `+1`;
2. every nonempty mixed fiber has exactly two perfect matchings;
3. a single `+/-1` signing cancels every mixed binomial; and therefore
4. the mixed alternating-cycle exponent vectors have no odd integer
   dependence.

The exact missing hypothesis is visible in the same example.  Each constant
fiber also has two terms, of weights `+1` and `-1`, so all three constant
**coefficients** vanish.  The complete matching tensor is zero.  Thus this
is not a Krenn counterexample, but it minimally refutes the term-level
incidence statement even when the three selected constant terms themselves
are normalized.

Any viable corrected theorem must assume the three constant fiber sums are
nonzero (or normalized to one), not merely that three normalized constant
matching monomials exist.

The dependency-free audit is
`computations/verify_parallel_binomial_incidence_countermodel.py`.

## 1. The 48 aggregate cells

Vertices are `0,...,5`.  A cell `uv;ab` means the aggregate coordinate
`A_uv(a,b)`.  Every listed cell is nonzero and no aggregate coordinate is
duplicated.  Several differently colored cells may share one underlying
pair, as required by the parallel-occurrence version of the question.

The support is

\[
\begin{array}{c|l}
uv&\text{endpoint-color pairs }ab\\ \hline
03&22\\
04&00\\
05&11\\
12&00,01,02,10,11,12,20,21,22\\
13&00,01,20,21\\
14&11,12\\
15&00,02,10,12,20,22\\
23&00,01,10,11,20,21\\
24&01,02,11,12,21,22\\
34&01,02,11,12\\
35&00,02,10,12\\
45&10,12,20,22.
\end{array}                                                \tag{1}
\]

There are 48 cells on twelve underlying pairs.  Give weight `-1` to

\[
\begin{split}
 15;00,10,20;\qquad
 34;01,02,11,12;\qquad
 35;02,12;\qquad
 45;12,22,                                                \tag{2}
\end{split}
\]

and weight `+1` to every other cell in (1).

## 2. Exact fiber enumeration

Direct enumeration of all fifteen underlying perfect matchings at each of
the `3^6=729` colorings gives

\[
 \#\{c:|\mathcal F_c|=0\}=621,\qquad
 \#\{c:|\mathcal F_c|=2\}=108.                            \tag{3}
\]

No other fiber size occurs.  Three of the binomial fibers are constant and
the remaining 105 are mixed.  In every mixed fiber one matching monomial
has weight `+1` and the other has weight `-1`, so every mixed coefficient is
zero.

Use the same selected matchings as in the triangular-prism chart:

\[
\begin{aligned}
 P_0&=04_{00}|12_{00}|35_{00},\\
 P_1&=05_{11}|14_{11}|23_{11},\\
 P_2&=03_{22}|15_{22}|24_{22}.                             \tag{4}
\end{aligned}
\]

All three products in (4) are `+1`.  The complete constant fibers are

\[
\begin{array}{c|c|c}
a&\text{two supported matchings}&\text{weights}\\ \hline
0&04|12|35,\quad04|15|23&+1,-1\\
1&05|12|34,\quad05|14|23&-1,+1\\
2&03|12|45,\quad03|15|24&-1,+1.
\end{array}                                                \tag{5}
\]

Thus `F_(a^6)=0` for all three colors.  Equations (3)--(5) prove that the
whole matching tensor is zero: empty fibers contribute nothing and every
nonempty fiber is an opposite-weight binomial.

## 3. Why no odd exponent dependence can exist

For each nonempty mixed fiber choose an order `(M_c,N_c)` and put

\[
                         d_c=\chi_{M_c}-\chi_{N_c}.         \tag{6}
\]

The signing (2) gives

\[
                              w^{d_c}=-1                   \tag{7}
\]

for all 105 mixed fibers.  If integers `z_c` obeyed

\[
                              \sum_c z_cd_c=0,             \tag{8}
\]

then evaluating (8) at (2) would give

\[
                    1=w^{\sum z_cd_c}=(-1)^{\sum z_c}.     \tag{9}
\]

Consequently `sum z_c` is even.  This proves directly, without a Smith
calculation, that the mixed exponent rows have no odd integer dependence.

The example therefore refutes the claimed incidence implication at its
smallest allowed even order and with honest aggregate coordinates.  It does
not refute the strengthened statement in which the three *fiber sums* in
(5) must be nonzero.  That strengthening is essentially the remaining
binomial-support case of the Krenn problem rather than a support-only
incidence lemma.
