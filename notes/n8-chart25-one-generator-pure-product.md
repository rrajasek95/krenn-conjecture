# Chart 25 has a one-generator pure-product identity

## Exact result

Take the 36-coordinate carrier of the exact chart-25 boundary dual, normalize
its twelve pure support variables to one, and set every coordinate outside
the carrier to zero.  The remaining ring has 24 variables.  In that ring,
the entire pure product is a multiple of one mixed coefficient:

\[
 \boxed{
 H_0H_1H_2
   =(1+x_3x_{12})(1+x_{16}x_{19})
      H_{11112222}.}
\tag{1}
\]

Here \(x_1,\ldots,x_{24}\) are the lexicographically ordered off-support
coordinates of the 36-coordinate carrier.  Direct expansion gives the more
transparent factor ledger

\[
\begin{aligned}
H_0&=1,\\
H_1&=(1+x_4x_7)(1+x_{16}x_{19}),\\
H_2&=(1+x_3x_{12})(1+x_{15}x_{24}),\\
H_{11112222}&=(1+x_4x_7)(1+x_{15}x_{24}).
\end{aligned}
\tag{2}
\]

Thus (1) is a literal factorization, not merely the output of a Gröbner
membership test.  It proves

\[
                  H_0H_1H_2\in I_{\rm mix}
\]

on the complete normalized 36-coordinate chart, at arbitrary sparsity.

## Polynomial rehomogenization

The four normalized multiplier terms in (1) require respectively
8, 6, 6, and 4 reference-support variables to recover the balanced port
multidegree.  Every required support exponent is zero or one.  Consequently
the checker rehomogenizes (1) to an ordinary polynomial identity

\[
                       QH_{11112222}=H_0H_1H_2
\tag{3}
\]

in the restricted unnormalized coordinate ring.  No Laurent denominator,
support power, rational coefficient, or additional mixed generator occurs.
The multiplier \(Q\) has four degree-eight monomials, all with coefficient
one.

This is much smaller than the chart-26 identity, which uses 73 mixed
generators, 282 multiplier terms, and Laurent support exponents down to
\(-2\).  The difference reflects the two extremal two-factor types: chart
25 has a Hamilton-cycle complement of hole type \((4,4)\), whereas chart 26
has cycle partition \((5,3)\) and hole type \((4,2,2)\).

## Full-source lifting frontier

Restoring all 252 variables does not create an off-chart degree-one tail.
The restricted identity already agrees with the full pure product through
that layer.  The first nonzero tail is at off-chart degree two and has 592
rows:

\[
                    464\text{ coefficients }-1,
                    \qquad128\text{ coefficients }+1.
\]

The absence of target degree one is structural: relative to the reference
perfect matching, a different pure matching first departs along an
alternating cycle and therefore changes at least two edges.  Chart 25 should
accordingly be lifted starting at degree two, not by repeating the
degree-one chart-26 calculation.

The current result is still a restricted-chart theorem.  A counterexample
localized at chart 25 may use coordinates outside the 36-coordinate carrier;
the 592-row tail must be removed by additional full-source mixed syzygies
before chart-25 saturation is complete.

## Exact census

Among the 6,558 mixed words there are 254 distinct nonzero restricted
polynomials.  Certificate (1) uses one.  The mixed coefficient has four
terms; the three pure coefficients have \((1,4,4)\) terms, and their product
has 16.  The checker reconstructs all these polynomials from the 105 perfect
matchings rather than storing the displayed factorization as input.

## Reproduction

```sh
python3 computations/verify_n8_chart25_pure_product_membership.py
python3 -O computations/verify_n8_chart25_pure_product_membership.py
python3 -I computations/verify_n8_chart25_pure_product_membership.py
python3 -S computations/verify_n8_chart25_pure_product_membership.py
```

The audit independently reconstructs the 36-coordinate carrier from the
exact boundary dual, verifies the normalized and polynomially rehomogenized
identities term by term, counts all restricted mixed polynomials, and streams
the complete full-source degree distribution to freeze the first lifting
tail.
