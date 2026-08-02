# A localized sparsity no-go on the eight-site dual-edge chart

## Exact outcome

For the first \(n=8\) vertex-to-triangle boundary graph, restrict the full
252-variable coordinate ring to the 60 coordinate variables that occur in
the exact degree-one dual certificate of commit `e1a3e9e`.  Keep all twelve
properly coloured boundary-support variables nonzero and set every variable
outside those 60 to zero.

Over every field of characteristic different from two, the mixed hafnian
coefficients have **no common zero on this chart with at most 13 nonzero
off-support coordinates**.  Equivalently, any common mixed zero in this
60-edge ansatz must use at least 14 of its 48 off-support coordinates.

This is a sharp bounded-ansatz no-go, not a proof for the unrestricted
localized ideal.  The cases with 14 or more off-support coordinates remain
open.

## Normalization

The twelve boundary variables form a perfect matching of the 24 coloured
ports \((v,a)\).  Under the port-torus action

\[
  x_{uv}^{ab}\longmapsto t_{u,a}t_{v,b}x_{uv}^{ab},
\]

each of those twelve variables uses two ports that no other boundary
variable uses.  They can therefore be normalized independently to one.
Every coefficient \(H_c\) is merely multiplied by the nonzero scalar
\(\prod_v t_{v,c_v}\), so this normalization preserves its vanishing.

The degree-one dual uses 60 coordinate variables in total: the twelve
normalized support variables and 48 possible extra variables.  The checker
freezes the complete 60-variable list and verifies that it contains both
the boundary support and the dual's displayed zero-support port matching.

The still smaller ansatz consisting only of the support plus the nine new
variables from that zero-support matching fails immediately:

\[
  H_{12012000}=1.
\]

Thus the zero-support matching is a useful direction selector, but is not
itself a common zero.

## The exact support search

On the normalized 60-edge chart, only 931 of the \(3^8=6{,}561\) colour
words have a nonzero coefficient: three pure words and 928 mixed words.
The mixed term-count census is

\[
\begin{array}{c|ccccc}
\text{number of terms}&1&2&3&4&5\\ \hline
\text{number of mixed words}&216&474&44&178&16.
\end{array}
\]

There are 900 distinct mixed polynomial supports.  For a proposed set
\(S\) of nonzero extra coordinates, call a monomial active when every
variable in it lies in \(S\).  A polynomial that has exactly one active
monomial cannot vanish, since that monomial is nonzero.  This gives a
necessary Boolean support condition without making any assumption about
the nonzero values.

Two mixed coefficients contain the normalized constant term one.  Each has
four possible correction monomials, giving 16 initial branches.  Whenever
a partial support activates exactly one term of another coefficient, every
admissible extension must activate one of its remaining terms.  The
checker branches on precisely these forced repairs.  The exhaustive search
through cardinality 13 visits only 98 supports and finds exactly four
minimal admissible supports, all of size twelve:

```text
0210 0211 0310 2400 2401 2410 2510 3401 3410 3411 3500 3510
0520 0522 0720 2502 2700 2702 5600 5602 5620 6702 6720 6722
1220 1222 1420 2300 2302 2320 2520 3402 3420 3422 4500 4520
1510 1511 1610 2501 2600 2601 5700 5701 5710 6701 6710 6711
```

As before, `uvab` denotes \(x_{uv}^{ab}\).  Every admissible support of
size at most 13 must contain one of these four patterns.  Exactly 48 of
their one-coordinate extensions remain Boolean-admissible.

## The three-binomial obstruction

Boolean admissibility is not enough.  On each of the four minimal patterns
and each of the 48 admissible extensions, the checker finds three surviving
mixed binomials

\[
  X^{a_i}+X^{b_i}=0\qquad(i=1,2,3)
\]

and signs \(\epsilon_i\in\{\pm1\}\) such that

\[
  \sum_i\epsilon_i(a_i-b_i)=0,
  \qquad
  \sum_i\epsilon_i\equiv1\pmod 2.
\]

All coordinates in the proposed support are nonzero, so the binomials give
\(X^{a_i-b_i}=-1\).  Raising them to the signed powers and multiplying
gives \(1=-1\), impossible outside characteristic two.  The frozen checker
records all 52 explicit triples.

For example, on the third minimal support set

\[
  A=x_{23}^{00},\quad B=x_{45}^{20},\quad
  C=x_{34}^{02},\quad D=x_{12}^{20}.
\]

Three mixed coefficients restrict to

\[
  AB+C=0,\qquad 1+DB=0,\qquad DC+A=0.
\]

Because \(A,B,C,D\ne0\), multiplying

\[
  \frac{AB}{C}=-1,\qquad
  \frac1{DB}=-1,\qquad
  \frac{DC}{A}=-1
\]

produces the contradiction \(1=-1\).  The other 51 cases are checked by
the same exact exponent-vector identity; no Gröbner basis, numerical solve,
or external SAT solver is used.

## Pure coefficients

The normalized restrictions of the three pure coefficients are also
audited exactly:

\[
\begin{aligned}
H_{00000000}={}&1+x_{23}^{00}x_{45}^{00}
 +x_{24}^{00}x_{35}^{00}
 +x_{26}^{00}x_{57}^{00}
 +x_{27}^{00}x_{56}^{00},\\
H_{11111111}={}&(1+x_{02}^{11}x_{34}^{11})
                 (1+x_{15}^{11}x_{67}^{11}),\\
H_{22222222}={}&(1+x_{05}^{22}x_{67}^{22})
                 (1+x_{12}^{22}x_{34}^{22}).
\end{aligned}
\]

Each retains its normalized constant term, but these expressions can still
vanish at special off-support values.  Since the mixed system already has
no point in the bounded ansatz, there is no candidate here on which to
impose a further pure-coefficient normalization.  Any future search at
sparsity 14 or higher must test these three displayed expressions directly.

## Scope and next step

The exact conclusion is

\[
 V(I_{\mathrm{mix}})\cap
 \{\text{dual 60-edge chart, at most 13 extras}\}=\varnothing.
\]

It does not imply \(P_G\in\sqrt{I_{\mathrm{mix}}}\), because a localized
common zero may use a coordinate outside the dual's 60-edge set or at least
14 of the 48 extras.  The next bounded computation is therefore sharply
identified: start at 14 nonzero extras, retaining the same Boolean-support
and odd-binomial filters before invoking heavier algebra.

## Reproduction

```sh
python3 computations/verify_n8_localized_dual_edge_sparse_no_go.py
python3 -O computations/verify_n8_localized_dual_edge_sparse_no_go.py
python3 -I computations/verify_n8_localized_dual_edge_sparse_no_go.py
python3 -S computations/verify_n8_localized_dual_edge_sparse_no_go.py
```

The ledger freezes the coefficient census, four minimal patterns, 48
extensions, and all 52 contradiction triples by SHA-256.
