# The mixed-singleton lemma fails first on eight vertices

Consider the monomial rank-one model in which every supported pair has one
ordered endpoint-color label and one nonzero scalar weight.  A perfect
matching then induces a unique vertex coloring.  It is tempting to hope that
three constant-color perfect matchings always force a mixed coloring whose
fiber consists of one perfect matching.  This is true on six vertices, but
false on eight.

## 1. A `K_8` counterexample

Number the vertices `0,...,7`.  Label every edge by `(r,r)`, with

\[
\begin{aligned}
 E_1={}&\{02,13,46,57\},\\
 E_2={}&\{04,06,15,17,24,26,35,37\},\\
 E_0={}&\binom{[8]}2\setminus(E_1\cup E_2).
\end{aligned}                                             \tag{1}
\]

The set `E_1` is a perfect matching, `E_2` contains four perfect
matchings, and `E_0` contains twenty-four, so all three constant colorings
occur.  Exact enumeration of the 105 perfect matchings gives

\[
 \#\{\text{fibers of size }1,2,4,24\}=1,38,1,1.           \tag{2}
\]

The exceptional fibers of sizes `1,4,24` are precisely the three constant
colorings, in colors `1,2,0`, respectively.  Every one of the 38 mixed
fibers has size exactly two.  Thus (1) disproves the proposed uniform
mixed-singleton statement.

An exact SAT search also allows an edge to be absent as a tenth edge state.
For `n=6`, the three designated edge-disjoint constant matchings have two
colored isomorphism types; both resulting formulas are unsatisfiable.  For
`n=8`, fixing one matching leaves thirteen colored triple types, and the
first satisfying type occurs on the third orbit.  Hence eight is the
smallest even order at least six at which the statement fails.  The SAT
search is `computations/search_monomial_no_singleton_sat.py`, and the
dependency-free direct audit of (1) is
`computations/verify_monomial_n8_counterexample.py`.

## 2. The counterexample cannot satisfy the weighted identity

Although no mixed fiber is a singleton, its scalar cancellation equations
are inconsistent even over arbitrary nonzero complex weights.  Write `x_uv`
for the weight of edge `uv`.  Three of the mixed fibers are

\[
\begin{array}{c|c|c}
c&M^+&M^-\\ \hline
00222200&\{01,24,35,67\}&\{07,16,24,35\}\\
00220220&\{01,26,35,47\}&\{07,14,26,35\}\\
10120200&\{02,14,35,67\}&\{02,16,35,47\}.
\end{array}                                               \tag{3}
\]

Let `R_j=x^{M_j^+}/x^{M_j^-}` for the three rows.  Direct cancellation in
each two-element fiber requires `R_j=-1`.  But the edge exponents in (3)
give the identity

\[
 \frac{R_2R_3}{R_1}
 =\frac{x_{01}x_{47}}{x_{07}x_{14}}
  \frac{x_{14}x_{67}}{x_{16}x_{47}}
  \frac{x_{07}x_{16}}{x_{01}x_{67}}=1.                  \tag{4}
\]

The proposed values instead make the left side
`(-1)(-1)/(-1)=-1`, a contradiction.  Equivalently, if `d_j` is the
integer exponent difference of the two matching monomials, then

\[
                         -d_1+d_2+d_3=0                  \tag{5}
\]

is an odd-sum lattice relation.  Thus this example kills the singleton
proof strategy but is not itself a weighted monomial realization of the
three-color GHZ tensor.

## 3. Remaining monomial question

The useful strengthened target is now a cycle-lattice statement: show that
whenever all mixed fibers have size at least two, their matching exponent
differences (or the corresponding multi-term equations) contain an
inconsistent cancellation circuit.  The three four-cycle switches in (3)
are the smallest such circuit.  Establishing this uniformly would replace
the false singleton lemma by an exact weight-aware obstruction.
