# Exact obstruction for all four-edge six-vertex rank graphs

Assume `H_6(A)=Delta_(6,3)`, let `R` be the graph of nonzero rank-one
aggregate matrices, and let `F` consist of the zero and rank-at-least-two
matrices.  The forced-anchor theorem gives `Delta(F)<=2`.  If `|F|=4`, the
five graph types are

\[
 P_5\sqcup P_1,\quad P_4\sqcup P_2,\quad P_3\sqcup P_3,
 \quad C_3\sqcup P_2\sqcup P_1,\quad C_4\sqcup2P_1.        \tag{1}
\]

The checker `computations/verify_f4_support_obstruction.py` excludes all
five.  It uses the global arbitrary-factor support formula and the exact
cancellation transfers proved in
`proofs/five-edge-rank-graph-obstruction.md`; this note isolates the one new
algebraic step.

## 1. Support closure and coefficient rectangles

Continue to encode every rank-one factor by its arbitrary nonempty
coordinate support, require the three opposite-head singleton anchors at
every vertex, allow an `F`-matrix either to vanish or to contain a support
two-matching, and impose the exact constant-support/mixed-no-singleton
coefficient rules.  Add the two sound translated-fiber cuts:

1. a nonempty constant coefficient and a mixed coefficient cannot be
   common Laurent-monomial multiples of one another; and
2. a mixed zero coefficient cannot be a common Laurent-monomial copy of all
   but one supported term of another mixed zero coefficient.

These cuts retain arbitrary complex values and every cancellation not
logically covered by those two statements.

Call the support of a matrix *two-closed* if, whenever it contains two cells
`(i,j),(k,l)` in distinct rows and columns, it also contains the cross cells
`(i,l),(k,j)`.

**Lemma 1.1 (finite closure/rectangle audit).**  In each support system
remaining after the translated-fiber cuts, the checker identifies an
exceptional edge `e` with the following properties:

1. `A_e` is forced active, or every exceptional edge has the properties
   below and the all-zero exceptional assignment is impossible;
2. conditional on `A_e` being active, its support is two-closed; and
3. conditional on all four cells of any `2 by 2` submatrix of `A_e` being
   supported, there is an assignment of the other four vertex colors and a
   pair of perfect matchings `M,N` such that all four resulting colorings
   are mixed and exactly `M,N` are supported.  The edge `e` belongs to
   exactly one of `M,N`.

**Exact audit.**  For two-closure, assume the active variable, two diagonal
support cells, and the negation of either cross cell; every such SAT call is
UNSAT.  For the rectangle assertion, enumerate all pairs among the fifteen
perfect matchings for which `e` belongs to exactly one, and all `3^4`
assignments of the other colors.  Clauses asserting that no candidate is an
exact two-matching rectangle are inconsistent once the active variable and
four corner entries are assumed.  No numerical values enter either check.
`QED`

**Lemma 1.2 (a good active edge is impossible).**  An edge satisfying
properties 2--3 of Lemma 1.1 cannot have rank at least two.

**Proof.**  Rank at least two gives a nonzero `2 by 2` minor.  In particular
its support contains one of the two diagonal cell pairs.  Two-closure makes
all four cells supported.  Choose the coefficient rectangle in property 3
and suppose `e in M`.  At a corner `(a,b)` the exact coefficient equation is

\[
             A_e(a,b)K+P(a)Q(b)L=0,                        \tag{2}
\]

where `K,L` are independent of `a,b`: the other edges of `M` avoid both
endpoints of `e`, while `N` pairs those endpoints separately.  Every factor
is nonzero because precisely `M,N` are supported.

The product of two instances of (2) is only `0=0`, so rearrange (2) into an
equality of two nonzero products before multiplying:

\[
             A_e(a,b)K=-P(a)Q(b)L.                         \tag{2'}
\]

Multiply the instances of (2') at the corners `(i,j),(k,l)`, and again at
the corners `(i,l),(k,j)`.  Both products have the same right-hand side
`P(i)P(k)Q(j)Q(l)L^2`, so

\[
 A_e(i,j)A_e(k,l)K^2=A_e(i,l)A_e(k,j)K^2.
\]

Since `K!=0`, division by `K^2` gives

\[
 A_e(i,j)A_e(k,l)=A_e(i,l)A_e(k,j).                        \tag{3}
\]

This says the chosen minor is zero, a contradiction.  If `e in N`, exchange
the two matchings. \(\square\)

## 2. The five exact cases

The checker obtains the following exhaustive outcomes.

\[
\begin{array}{c|c|c}
F&\text{translated-fiber cuts}&\text{final certificate}\\ \hline
P_5\sqcup P_1&0&01\text{ forced active and good}\\
P_4\sqcup P_2&43&01\text{ forced active and good}\\
P_3\sqcup P_3&0&01\text{ forced active and good}\\
C_3\sqcup P_2\sqcup P_1&0&\text{support formula UNSAT}\\
C_4\sqcup2P_1&10&\text{all four edges good; not all zero}.
\end{array}                                                \tag{4}
\]

In the first three rows Lemma 1.2 contradicts the forced active edge.  In
the last row at least one exceptional matrix is active, and whichever one
is active contradicts Lemma 1.2.  The direct UNSAT row needs no coefficient
algebra.  Therefore:

**Theorem 2.1.**  The graph `F` cannot have four edges in a six-vertex,
three-color realization.

Run the complete exact audit with

```sh
uv run python computations/verify_f4_support_obstruction.py
```

The script constructs all five graph types, keeps arbitrary endpoint-factor
supports, asserts every transfer and closure witness it uses, and reports
the five rows of (4).  The transfer counts in (4) record the current
deterministic solver trajectory only; the proof uses the semantic endpoint
of each row, not those counts.
