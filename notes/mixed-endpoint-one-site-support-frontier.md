# The mixed-endpoint one-site support frontier starts at 32 cells

## 1. Exact outcome and scope

Let \(U\) be a six-set, let each \(V_u\) have coordinate axes
\(e_0^{(u)},e_1^{(u)},e_2^{(u)}\), and write

\[
 q=\sum_{\{u,v\}\in\binom U2}\sum_{a,b=0}^2
     x_{uv}^{ab}e_a^{(u)}e_b^{(v)}.
\]

Thus \(q\) may contain all 135 endpoint-ordered coordinate cells, with
arbitrary complex weights.  Suppose the six response factors are one-site
coordinate rows and

\[
 q^{[3]}=0,\qquad p_i s_jq^{[2]}=\delta_{ij}X_i.       \tag{1}
\]

**Theorem 1.1.** Every solution of (1) in this restricted class has at
least 32 nonzero aggregate cells \(x_{uv}^{ab}\).

This is a lower bound, not an existence result at 32 cells.  It concerns
one-site coordinate response rows and coordinate cells of \(q\); it does
not cover multi-site rows or non-coordinate edge blocks.  In particular,
the calculation below is not a global obstruction to (1).

## 2. The two row geometries entering the mixed-cell search

Up to site relabelling, target-colour relabelling, and simultaneous reversal
of all response arrows, there are seventeen directed one-site row orbits.
Before imposing any property of \(q\), the diagonal and off-diagonal
equations can ask the same four-site tensor block both to contain a target
coefficient and to vanish.  A literal audit of these block requirements
finds a direct conflict in fifteen orbits.  The two compatible representatives
are

\[
 \begin{aligned}
  \text{path--edge:}&\quad ((0,1),(1,2),(3,4)),\\
  \text{matching:}&\quad ((0,1),(2,3),(4,5)).
 \end{aligned}                                                   \tag{2}
\]

Only these two representatives are passed to the mixed-endpoint support
calculation.  The statement is deliberately limited to the one-site row
classification; (2) is not a classification of arbitrary response rows.

## 3. A necessary Boolean support relaxation

Give each of the 135 cells one support bit.  For every coordinate
coefficient of every four-site block sampled by the nine response products,
enumerate its three two-matchings.  For every coordinate coefficient of
\(q^{[3]}\), enumerate its fifteen perfect matchings.  Introduce an auxiliary
bit equivalent to the conjunction of the cell bits in each matching term.

The following implications are necessary over \(\mathbb C\).

1. A required nonzero target coefficient has at least one supported term.
2. A required zero coefficient cannot have exactly one supported term.

The second rule grants arbitrary cancellation whenever two or more terms
are supported.  Consequently the Boolean system is a relaxation of the
weight equations: its unsatisfiability is an obstruction, while its
satisfiability is not a construction.

Exact weighted MaxSAT gives minimum support 30 for both geometries.  There
are eight minimum supports in the path--edge geometry and five in the
matching geometry.  The next Boolean support cost is 31 for path--edge and
32 for matching.  There are exactly eighteen path--edge supports of cost
31, after which the next cost is 32.

## 4. Exact Laurent-sign obstruction on every support below 32

Fix one of the enumerated supports.  Whenever a required-zero quadratic
coefficient has exactly two supported monomials, its nonzero weight equation
has the Laurent form

\[
                    x^{d_k}=-1.                                  \tag{3}
\]

For every support at costs 30 and 31, the checker finds an exact integral
relation

\[
              \sum_k r_kd_k=0,\qquad \sum_k r_k\equiv1\pmod2.     \tag{4}
\]

Multiplying (3) to the powers \(r_k\), including negative powers in the
Laurent torus, yields

\[
       1=x^{\sum r_kd_k}=(-1)^{\sum r_k}=-1,
\]

which is impossible in characteristic zero.  The relations are reconstructed
from exact rational nullspaces, cleared to primitive integer vectors, and
their exponent cancellation and odd parity are checked directly.  Thus this
is not merely a parity calculation over \(\mathbb F_2\).

The exact layer data are:

| geometry and cost | supports | nonzero entries in displayed relations | relation sums |
|---|---:|---|---|
| path--edge, 30 | 8 | \(9,9,9,7,3,9,7,7\) | \(-1,1,1,-1,1,-1,1,1\) |
| path--edge, 31 | 18 | \(7,3,9,7,7,7,9,7,7,9,9,9,7,3,7,3,3,7\) | \(1,1,1,1,1,-1,1,3,1,1,1,1,1,1,1,1,1,-1\) |
| matching, 30 | 5 | \(3,7,3,7,9\) | \(1,1,1,3,5\) |

The matching relaxation has no support of cost 31.  This exhausts every
relaxed support below 32 and proves Theorem 1.1.

## 5. Reproducibility and the open next layer

Run

```sh
uv run python computations/verify_mixed_endpoint_one_site_support_frontier.py
```

The checker rebuilds the direct row-block filter, the Boolean clauses, the
weighted minimum layers, every support at costs 30 and 31, and each exact
odd Laurent relation.  Its deterministic support/relation ledgers are

```text
path-edge cost 30:
8f88e995a65d0d4e82543d42bb73bb96eb32cae05012ad54a9bf39b7ff8d7c52
path-edge cost 31:
e677d98a4075ff648c096de7e62a16cf8dcf0de393f09d766753d8c3a8e6a6df
matching cost 30:
c240e8e7c8c7b41ff600a3acc073fb9534a51e7992b31a252cb984b9c973e325
```

Cost 32 is the first unresolved layer.  A support surviving the displayed
binomial obstruction would still have to satisfy all quadratic cancellation
equations, the cubic equations \(q^{[3]}=0\), and the three target
normalizations with nonzero weights.  Those weight equations, rather than
another support-only SAT result, are the concrete next test.
