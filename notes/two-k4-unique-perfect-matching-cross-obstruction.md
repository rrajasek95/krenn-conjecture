# Two `K_4` shores cannot be joined by a unique cross perfect matching

## 1. Result

Let

\[
 L=\{L_0,L_1,L_2,L_3\},\qquad
 R=\{R_0,R_1,R_2,R_3\},
\]

and put the standard unit ternary-equality `K_4` on each shore.  Thus the
three one-factors are

\[
 01\mid23,\qquad 02\mid13,\qquad 03\mid12,                 \tag{1}
\]

with respective colours `0,1,2`.  Add arbitrary complex `3 by 3` matrices
on a bipartite cross graph $G\subseteq L\times R$.  Zero aggregate matrices
are deleted when defining `G`.

**Theorem 1.**  If `G` has a unique four-edge perfect matching, the resulting
eight-site matching tensor is not `Delta_(8,3)`.

The matrices may have arbitrary rank and coordinate support.  The result is
support-theoretic: it uses only that a lone nonzero matching monomial cannot
cancel over a field.  In particular, it is independent of numerical
conditioning, signs, positivity, or genericity.

Together with
[`two-k4-low-matching-cross-obstruction.md`](two-k4-low-matching-cross-obstruction.md),
this excludes every two-`K_4` cross graph with matching number at most three,
and also the matching-number-four stratum whose cross perfect matching is
unique.

## 2. Every unique-matching graph is triangular

Normalize the unique cross perfect matching to

\[
                         P=\{L_iR_i:0\leq i<4\}.          \tag{2}
\]

Contract the four edges of `P`, and orient a nonmatching edge `L_iR_j` as
the arc $i\to j$.  A directed cycle would alternate with edges of `P` and
produce a second perfect matching.  Hence this digraph is acyclic.  A
topological ordering embeds `G` in

\[
              E_\triangle=\{L_iR_j:i\leq j\}.            \tag{3}
\]

Conversely, (3) has only its diagonal perfect matching: a permutation
$\pi$ satisfying $i\leq\pi(i)$ for every `i` must be the identity.

After the topological relabelling, a global permutation of the three
physical colours normalizes the left factorization to (1).  The right
factorization is then

\[
                         \kappa_R=\sigma\circ\kappa       \tag{4}
\]

for one of the six permutations $\sigma\in S_3$.  Therefore it suffices to
allow arbitrary matrices, including zero matrices, on all ten edges (3),
require the four diagonal matrices to be nonzero, and exclude each of the
six choices of `sigma`.

This reduction loses nothing.  Every missing edge of the original graph is
represented by a zero matrix in (3).

## 3. The exact support formula

Write

\[
             x_{ij}^{ab}=[A_{L_iR_j}]_{ab},\qquad i\leq j, \tag{5}
\]

and let `z_(ij)^(ab)` mean that this cell is nonzero.  There are ninety such
Boolean cell variables.

For a physical word

\[
                  w=a_0a_1a_2a_3\mid b_0b_1b_2b_3,       \tag{6}
\]

let $\mathcal M_\sigma(w)$ be the cross-sector matching monomials compatible with
`w`.  They are exactly the following.

1. There is one four-cross monomial,

   \[
                \prod_{i=0}^3x_{ii}^{a_i b_i}.           \tag{7}
   \]

   Its uniqueness is the unique-perfect-matching property of (3).

2. A two-cross monomial chooses a pair `I` on the left, a pair `J` on the
   right, and a bijection $\phi:I\to J$ with $i\leq\phi(i)$.  The two
   complementary shore edges must have their prescribed factor colours,
   and the monomial is

   \[
                       \prod_{i\in I}x_{i,\phi(i)}^{a_i b_{\phi(i)}}.
                                                                    \tag{8}
   \]

Introduce a witness `y_m` with the exact Boolean definition

\[
                         y_m\quad\Longleftrightarrow\quad
                         \bigwedge_{z\in m}z .             \tag{9}
\]

The target equations imply two elementary necessary conditions.

* If `w=r^4|s^4` with `r != s`, the zero-cross sector contributes `1`
  while the target coefficient is zero.  Hence at least one cross monomial
  is nonzero:

  \[
                              \bigvee_{m\in\mathcal M_\sigma(w)}y_m. \tag{10}
  \]

* For every other word, the cross sector must vanish.  It therefore cannot
  contain exactly one nonzero monomial:

  \[
       y_m\quad\Longrightarrow\quad
       \bigvee_{n\in\mathcal M_\sigma(w),\ n\ne m}y_n
       \qquad(m\in\mathcal M_\sigma(w)).                   \tag{11}
  \]

For a global constant word, the zero-cross coefficient already equals the
target coefficient, so (11) is still the correct cross-sector condition.
For a mixed word the zero-cross coefficient is zero.  Thus (10)--(11)
cover all `3^8=6,561` words.

Finally, each edge of the unique matching (2) is a genuine edge of `G`, so
each diagonal block has a nonzero cell:

\[
                         \bigvee_{a,b}z_{ii}^{ab}
                         \qquad(0\leq i<4).               \tag{12}
\]

Equations (9)--(12) form a CNF formula $F_\sigma$.  The support of any exact
complex realization would satisfy $F_\sigma$.  No converse is assumed: the
formula deliberately forgets all coefficient magnitudes and most
cancellation equations, so proving it unsatisfiable is a valid obstruction.

## 4. Exact exhaustion of the triangular envelope

For every $\sigma\in S_3$, $F_\sigma$ is unsatisfiable.  Each formula has
8,676 variables, 8,586 cross-monomial witnesses, and 47,453 or 47,454
clauses.  The six cases are:

| `sigma(012)` | clauses | SHA-256 prefix |
|---|---:|---|
| `012` | 47,454 | `d21f736e401d` |
| `021` | 47,453 | `2c3556b254b6` |
| `102` | 47,453 | `6c5e63308763` |
| `120` | 47,453 | `5a85e3b3deef` |
| `201` | 47,453 | `62e56e47016f` |
| `210` | 47,454 | `446cdf25a921` |

The checker constructs the matching fibres directly from all 105 perfect
matchings of eight labelled sites.  It verifies that every word has one and
only one four-cross term, solves each formula independently with CaDiCaL and
Glucose, obtains a DRUP trace from Glucose, and independently checks every
additive proof clause by reverse unit propagation.  Only four to thirteen
RUP additions, after deletion records are discarded, are needed in the six
cases.  Deletion records may safely be ignored because retaining clauses can
only strengthen unit propagation.

This is an exact Boolean proof, not a floating-point or bounded-coefficient
search.

For the identity relative colouring there is also a small explicit core.
Besides (12), it uses the three required fibres

```text
0000|1111  0000|2222  1111|2222
```

and the following eighteen zero-fibre no-singleton conditions:

```text
0001|2101  0001|2221  0000|0100  0000|2100  0000|2221
0100|1100  0101|2101  0101|2121  0101|2202  0111|1112
0111|1121  0111|2112  0111|2122  1000|2100  1000|2111
1101|2202  0000|2122  0111|0021
```

These 21 fibres contain only 47 matching witnesses and give an unsatisfiable
226-clause formula.  The checker audits this core separately before running
the full six formulas.

The exact audit is
[`verify_two_k4_unique_perfect_matching_obstruction.py`](../computations/verify_two_k4_unique_perfect_matching_obstruction.py).

## 5. A hand proof when the cross graph is exactly `P`

The four-edge subcase admits a useful conceptual proof that explains why the
four-cross bad words are so restrictive.

Call a four-site word `a=(a_0,a_1,a_2,a_3)` **live** if some shore edge
`uv` satisfies

\[
                         a_u=a_v=\kappa(uv),              \tag{13}
\]

and **dead** otherwise.  There are 30 dead words.  On the matching edge
`L_iR_{P(i)}`, let `S_i` be its set of nonzero row colours.  If a dead word
`a` belonged to $S_0\times S_1\times S_2\times S_3$, choose independently a
nonzero cell in each selected row.  The resulting eight-site word would
have exactly one supported matching monomial: the four-cross product on
`P`.  It has no two-cross term because `a` has no compatible internal left
edge, and its target coefficient is zero.  This is impossible.  Hence

\[
                         S_0\times S_1\times S_2\times S_3
                         \subseteq \{\hbox{live words}\}. \tag{14}
\]

The same argument applied to columns gives a live Cartesian column box.

There are exactly 34 inclusion-maximal nonempty live boxes.  Under the
natural `S_4` action on vertices and induced action on the three factor
colours, their four orbits have the following representatives.  Here, for
example, `012` denotes the full colour set.

| representative `(S_0,S_1,S_2,S_3)` | orbit size | correctable colours |
|---|---:|---:|
| `(0,012,2,1)` | 4 | 3 |
| `(0,01,0,01)` | 12 | 2 |
| `(0,01,012,1)` | 12 | 2 |
| `(0,0,012,012)` | 6 | 1 |

To see the last column, put

\[
                         I_r=\{i:r\in S_i\}.              \tag{15}
\]

With only the matching `P` available, a left-constant colour `r` can occur
in a four-cross correction only if `I_r` is all four vertices.  It can
occur in a two-cross correction only if `I_r` contains an edge of the
colour-`r` one-factor.  Every `r` needs a correction, since one may inspect
any off-diagonal block word `r^4|s^4`.  The table therefore leaves only the
four star boxes

\[
 S_\alpha=\{0,1,2\},\qquad
 S_i=\{\kappa(\alpha i)\}\quad(i\ne\alpha).              \tag{16}
\]

Nonemptiness and the three correction requirements show that the actual box
equals, rather than merely lies inside, (16).  The column box is similarly
a star with centre `beta`.

For each colour `r`, let `i_r` be the colour-`r` neighbour of `alpha`; for
each `s`, let `j_s` be the colour-`s` neighbour of `beta`.  A four-cross
block-constant term is impossible in a star box.  The only possible
two-cross correction at `r^4|s^4` uses the two matching edges indexed by
`{alpha,i_r}`, and its two right endpoints must be `{beta,j_s}`.  Thus

\[
                  r^4|s^4\text{ can be corrected only if }
                  P\{\alpha,i_r\}=\{\beta,j_s\}.          \tag{17}
\]

If `P(alpha)=beta`, the image pair in (17) selects only one `s` for each
fixed `r`, whereas both values `s != r` are required.  If
`P(alpha) != beta`, then for all but one `r` the image pair omits `beta`, so
it selects no `s` at all.  Either way an off-diagonal block word cannot be
corrected.  This proves the four-edge subcase by hand.

The checker enumerates the `7^4` Cartesian boxes, verifies the four-orbit
classification and all 24 possible bijections `P`, and independently
exhausts the 4,096 normalized cross graphs.  Exactly 543 have the diagonal
as unique perfect matching, agreeing with the 543 labelled acyclic digraphs
on four vertices and auditing the triangularization step.

## 6. Remaining two-`K_4` graph stratum

This theorem does not exclude a cross graph with two or more four-edge
perfect matchings.  After combining it with the low-matching theorem, that
is the precise graph-theoretic remainder of the arbitrary two-`K_4` cross
matrix ansatz.  The separate
[`two-k4-dead-slice-determinantal-boundary.md`](two-k4-dead-slice-determinantal-boundary.md)
also shows that a full-cross solution cannot have all sixteen cross blocks
invertible; that rank boundary is complementary to the unique-matching
obstruction proved here.
