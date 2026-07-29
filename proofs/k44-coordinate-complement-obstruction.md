# A coordinate-complement obstruction on `K_{4,4}`

This note exactly excludes the first tight-cut-free degree-four brace,
`K_{4,4}`.  It first records a small coordinate-complement audit and then
uses the forced incident-edge theorem to cover all arbitrary complex edge
matrices on this support.

Let the bipartition classes of `K_{4,4}` be

\[
             X=\{x_0,x_1,x_2,x_3\},\qquad
             Y=\{y_0,y_1,y_2,y_3\},
\]

and fix the perfect matching

\[
                         F=\{x_i y_i:0\le i<4\}.             \tag{1}
\]

## 1. The excluded chart

Assume that every edge outside `F` carries a nonzero coordinate rank-one
matrix

\[
             A_{x_i y_j}=\lambda_{ij}
                 e_{a_{ij}}^{(x_i)}\otimes e_{b_{ij}}^{(y_j)}
                 \quad(i\ne j),                             \tag{2}
\]

and that the three labels incident at every vertex are distinct on their
respective endpoint:

\[
 \{a_{ij}:j\ne i\}=\{0,1,2\},\qquad
 \{b_{ij}:i\ne j\}=\{0,1,2\}.                              \tag{3}
\]

Equivalently, the `a`-labels and `b`-labels are two, not necessarily equal,
proper three-edge-colourings of the cubic graph `K_{4,4}-F`.  Put completely
arbitrary `3 by 3` complex matrices on the four edges of `F`.

**Theorem 1 (coordinate-complement obstruction).**  Matrices satisfying
(2)--(3) cannot have matching tensor `Delta_(8,3)`.

The proof needs only supports.  In any exact realization:

1. each constant colouring has at least one nonzero matching monomial; and
2. each mixed colouring has either zero or at least two nonzero matching
   monomials, since a unique nonzero monomial cannot cancel.

There are nine derangements of four symbols, hence nine perfect matchings of
`K_{4,4}-F`.  Its proper three-edge-colourings are precisely its four
partitions into three derangements.  For each ordered pair of endpoint
colourings and each choice of zero/nonzero cells on the four arbitrary
`F`-matrices, one can enumerate the 24 perfect matchings and impose the two
conditions above.  The resulting Boolean formula is unsatisfiable in every
case.

The exact audit is

```text
computations/verify_k44_coordinate_complement_obstruction.py
```

Simultaneous conjugation of the four indices has two orbits on the four
one-factorizations: the factorization by the three double transpositions,
and the other three factorizations.  A common permutation of output colours
normalizes the left colour order.  The audit therefore checks

\[
                         2\cdot4\cdot 3!=48                 \tag{4}
\]

symmetry classes.  Each formula has 7,164 variables and between 41,535 and
41,544 clauses, and every formula is `UNSAT`.  The clauses encode an exact
equivalence between a matching-support witness and the conjunction of the
cells it uses; thus this is an exhaustive finite proof of the two necessary
support conditions.  Since those conditions are weaker than the coefficient
equations, Theorem 1 follows.

## 2. The full forced-anchor obstruction

The forced incident-edge theorem says that at every vertex of an exact
three-colour realization there are three distinct incident rank-one matrices
whose factor at the opposite endpoint is respectively `e_0,e_1,e_2`.
Consequently, on a four-regular support, the rank-at-least-two edges form a
matching.  The coordinate-complement chart above would follow if one perfect
matching contained every remaining one-sided exception.  This containment
is not automatic: the exceptional edge seen from its `X` endpoint and the
exceptional edge seen from its `Y` endpoint can differ.

The one-sided freedom can nevertheless be retained in a finite exact audit.

**Theorem 2 (`K_{4,4}` obstruction).**  Put arbitrary nonzero aggregate
`3 by 3` complex matrices on all sixteen edges of `K_{4,4}`.  Their matching
tensor is not `Delta_(8,3)`.

**Proof.**  Record only the zero/nonzero support of every matrix.  For an
edge `e`, introduce a Boolean `rho_e` saying that its matrix has rank one.
When `rho_e` is true, introduce nonempty endpoint supports `L_e,R_e` and
impose the exact rectangle identity

\[
          A_e(a,b)\ne0\quad\Longleftrightarrow\quad
          a\in L_e\ \hbox{ and }\ b\in R_e.                \tag{5}
\]

When `rho_e` is false, its nine cell supports are arbitrary.  Impose the
following necessary conditions.

1. At most one edge with `rho_e=false` is incident with any vertex.
2. For every `x in X` and colour `r`, some incident rank-one edge has
   opposite support `R_e={r}`.  For every `y in Y`, symmetrically some
   incident rank-one edge has `L_e={r}`.
3. Every underlying edge matrix is nonzero.
4. Each of the three constant colourings supports a perfect matching.
5. No mixed colouring supports exactly one perfect matching.

Conditions 1--2 are precisely the forced incident-edge theorem specialized
to degree four.  Conditions 4--5 follow from the coefficients `1` and `0`
of the target.  In particular, all five conditions hold for the support of
any hypothetical exact realization.

There are only `3^8=6,561` vertex colourings and 24 perfect matchings.  The
checker

```text
computations/verify_k44_forced_anchor_support_obstruction.py
```

encodes (5) and Conditions 1--4 in CNF.  It then uses an exact CEGAR loop:
after each SAT model it enumerates all 6,558 mixed colourings; for every
mixed singleton found, it adds the exact equivalences between the 24
matching witnesses and their four cell conjunctions, together with the
condition that every supported witness have a distinct mate.  Thus every
added clause is a necessary instance of Condition 5.  If a model with no
singleton existed, the direct enumeration would return it.

The loop terminates `UNSAT` after 38 rounds.  It needs only 1,633 of the
6,561 colouring fibers, giving 39,544 Boolean variables and 236,115 clauses.
Hence Conditions 1--5 are mutually inconsistent.  A hypothetical exact
realization would supply a satisfying assignment, contradiction. `QED`

## 3. A sharp graph-theoretic obstruction to the proposed reduction

The underlying graph `K_{4,4}` is connected, four-regular, matching covered,
and has no nontrivial tight cut.  For the last assertion, a nontrivial odd
shore may be replaced by its complement and hence has size three.  If all
three vertices lie in one bipartition class, every perfect matching crosses
the cut three times.  If the shore meets the two classes in sizes one and
two, completeness supplies both a matching with one internal shore edge and
a matching with none, hence crossing counts one and three.  The cut is not
tight in either case.

It has no cubic vertex, and it contains no octahedral subgraph because it is
bipartite whereas `K_6` minus a perfect matching contains triangles.  In
fact every edge of `K_{4,4}` is graph-theoretically removable: after deleting
one edge, any other edge extends to a permutation avoiding the deleted pair.

This last fact does not permit an algebraic deletion.  Setting an aggregate
edge `A_e` to zero changes the matching tensor by

\[
            A_e\otimes H_{B\setminus e}(A),                \tag{6}
\]

which is nonzero at an entry-minimal exact point.  Graph removability says
only that the remaining edges still extend to perfect matchings; it gives no
identity cancelling (6).  Theorem 2 is exactly such an algebraic obstruction
for the smallest four-regular brace, but the graph facts show that it cannot
be obtained from the proposed cubic/tight-cut/octahedral trichotomy.  Any
uniform minimal-support proof must add further brace obstructions or a
reduction valid on tight-cut-free bipartite cores of unbounded order.
