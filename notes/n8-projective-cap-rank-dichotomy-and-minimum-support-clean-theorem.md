# At eight sites: projective cap rank, a minimum-support clean theorem, and the sharp rank guard

## Outcome

Fix an endpoint-ordered aggregate source on eight sites, a pair `p,q`, and
write

\[
 R=B\setminus\{p,q\},\qquad Q=H_R(A),\qquad
 E=\operatorname{span}\{X_0,X_1,X_2\},
 \quad X_c=e_c^{\otimes R}.
\]

There are five exact conclusions.

1. **Full-source projective-rank dichotomy.**  If
   \(H_B(A)=\Delta_{8,3}\), then for every cap covector `C`

   \[
   \boxed{\quad
   \kappa_{pq}(C)
    =[D H_R(A)[B^C]]
    =\left[\sum_{c=0}^2 C_{cc}X_c\right]
      \in T_R/\langle Q\rangle .\quad}                 \tag{1}
   \]

   Hence a **target-active** zero-error cap exists at this pair precisely
   when

   \[
                0\ne Q=q_0X_0+q_1X_1+q_2X_2,
                \qquad q_0q_1q_2\ne0.                 \tag{2}
   \]

   This is the finite deletion target.  Doubly injective endpoint stars do
   not alter (1); they must be used to force (2).

2. **Degree-two clean theorem.**  Suppose all 28 pairs are doubly
   aggregate-injective.  Every active edge incident with a degree-two
   support vertex admits an active clean cap.  Consequently every source
   with at most eleven nonzero aggregate blocks has an active clean cap.
   Thus no exact eight-site ternary source can lie below the cubic
   twelve-edge stratum, by the proved arbitrary-complex six-site
   obstruction.

3. **Sharp first-order guard.**  One pure-normalized rational `C8` source
   attains that minimum support and the block rank forced on that support,
   has all 28 pairs doubly injective, yet its projective cap-error map has
   rank nine at every pair.  Thus

   \[
                    \kappa_{pq}(C)\ne0
                    \quad\text{for every }C\ne0         \tag{3}
   \]

   at all 28 pairs.  Its eight support edges nevertheless have active clean
   caps.  This separates the linear deletion route from the nonlinear clean
   route exactly.  The guard is one common physical source, not 28
   independently chosen pair charts, but it is not a GHZ source: its first
   displayed mixed residual is `01000000 = 1283/117`.  A second exact guard
   at the first unresolved support, the cubic cube graph with twelve blocks,
   again has projective error rank nine everywhere and has no active clean
   cap at any pair.

4. **The thirteen-edge layer closes.**  For the exact clean-error support
   (s r^{[2]}x+r^{[3]}), every minimum-degree-three graph with thirteen
   edges has a support-forced active clean edge except one graph type:

   \[
                       K_{4,4}\setminus 3K_2.           \tag{26}
   \]

   That terminal has an independent four-set and a dead cross edge with
   cubic endpoints.  The proved 141-mixed-row dead-cross theorem therefore
   excludes it from the full source equation.  Consequently an exact
   all-pairs-good eight-site counterexample has at least fourteen aggregate
   support edges.

5. **The first support-14 terminal.**  Of the five possible degree
   sequences, only four graph orbits survive the generalized clean test.
   Three have independent four-sets and exit through proved full mixed
   rows.  The sole remaining orbit is a `C4` with every core edge
   triangulated and the four triangle apices paired across opposite core
   edges.  It has no independent four-set; all its clean-error seals are
   `RRX`, never `RRR`.  This is the exact next graph, not yet an exact-source
   counterguard.

The checker is
[`verify_n8_support_rank_minimal_projective_cap_error_counterguard.py`](../computations/verify_n8_support_rank_minimal_projective_cap_error_counterguard.py).

## 1. The full-source identity removes the star variables

For an arbitrary cap `C`, put

\[
 s_C=\langle C,A_{pq}\rangle,
\]

and let `B^C` be the exact two-star effective quadratic

\[
 B^C_{ij}=\operatorname{contr}_{p,q}^C
 \bigl(A_{pi}A_{qj}+A_{pj}A_{qi}\bigr).                \tag{4}
\]

Sorting the physical matchings according as they use `pq` gives

\[
 \operatorname{contr}_{p,q}^C H_B(A)
   =s_CQ+D H_R(A)[B^C].                                \tag{5}
\]

If the **complete** source equation is imposed, the same contraction is

\[
 \operatorname{contr}_{p,q}^C\Delta_{8,3}
   =\sum_c C_{cc}X_c.                                  \tag{6}
\]

Subtracting `s_C Q` and passing modulo `Q` proves (1).  This uses all nine
endpoint-colour rows at the pair.  In particular it is not a semisimple
one-cap calculation and does not select a source occurrence.

The quotient ranks are now elementary.

* If `Q=0` or `Q` is outside `E`, the three diagonal columns remain
  independent modulo `Q`.  The rank of `kappa` is three and its kernel is
  exactly the six-dimensional off-diagonal cap space.
* If `0 != Q=sum q_c X_c` lies in `E`, the quotient rank is two and

  \[
       \ker\kappa
       =\{C:\ (C_{00},C_{11},C_{22})=\lambda(q_0,q_1,q_2)\}. \tag{7}
  \]

  The six off-diagonal entries remain arbitrary.  The new diagonal line is
  target-active exactly when all three `q_c` are nonzero.

This also corrects a quantifier trap in the phrase “zero projective cap
error.”  Every off-diagonal cap of an exact target source already has zero
projective error at every pair.  It gives no descent: (6) is zero, and in
(5) the direct and error scalars cancel to the zero contraction.  The
useful statement is **target-active** zero error, which is exactly (2).

If (2) holds, the deleted aggregate array itself has matching tensor
`sum q_c X_c`; an invertible diagonal change at one residual site turns it
into `Delta_(6,3)`.  The six-site theorem excludes this.  Thus a hypothetical
exact eight-site source must keep every deleted cofactor either outside `E`
or on a coordinate face of `E`.  A successful direct support/rank proof has
been reduced to forcing one good pair off those alternatives.

## 2. A degree-two vertex forces the nonlinear clean alternative

Let `G` be the graph of nonzero aggregate blocks and assume every physical
pair is doubly injective.  Every vertex of `G` has degree at least two.  If
`p` had zero or one active neighbour `q`, deleting the pair `p,q` would
leave the `p`-star zero, contradicting injectivity.  The handshake lemma
therefore gives

\[
                            |E(G)|\ge8.                 \tag{8}
\]

Assume equality.  Every vertex has degree two.  Moreover, every active
block has rank three: at an endpoint `p`, delete one of its two neighbours;
the other block is then the sole surviving summand of the injective star.
Thus the total aggregate block rank is at least, and at equality is,

\[
                              8\cdot3=24.               \tag{9}
\]

Fix an active edge `pq`.  Outside that edge, `p` has one neighbour `i` and
`q` has one neighbour `j`.  Formula (4) shows that for every cap `K` the
effective correction `r=B^K` is supported on at most the single physical
pair `ij`; it is zero if `i=j`.  In the site-square-zero algebra,

\[
                              r^2=0.                    \tag{10}
\]

At eight sites the homogeneous clean error is

\[
 {\cal E}_{p,q}(K)=\frac{s_Kr^2x}{2}+\frac{r^3}{6},    \tag{11}
\]

so (10) kills it identically.  Since `A_pq` has rank three, one may choose
`K` outside the four hyperplanes

\[
 \langle K,A_{pq}\rangle=0,\qquad K_{00}=0,\qquad
 K_{11}=0,\qquad K_{22}=0.                              \tag{12}
\]

Over `C` their complement is nonempty.  This `K` has
`s_K K_00 K_11 K_22 != 0` and is an active clean cap.  The argument is
local and gives the slightly broader criterion:

> An active pair for which at least one deleted endpoint star is supported
> at at most one residual site is actively clean.

The minimum-support theorem follows by applying this criterion to any
support edge.  More strongly, if `|E(G)| <= 11`, then the average degree is
strictly below three.  Since the minimum degree is at least two, some vertex
`p` has degree exactly two.  Either incident edge supplies the local
criterion: the `p`-side of every effective correction is supported at its
one residual neighbour, so the whole correction is a star and has square
zero.  Hence

\[
 \boxed{\text{all 28 pairs good and }|E(G)|\le11
        \quad\Longrightarrow\quad\text{an active clean cap}.} \tag{13}
\]

At twelve edges the only way to avoid this conclusion is for every vertex
to have degree three.  Thus a cubic graph is the exact first support layer
not closed by the square-zero star argument.  Notice that the theorem
reaches the nonlinear alternative even when every first-order projective
error is nonzero.

## 3. The exact eight-edge guard

Use the cyclic support

\[
                  0-4-1-5-2-6-3-7-0.                  \tag{14}
\]

In stored endpoint order, put the following integral matrices on its eight
edges and zero on the other twenty:

```text
04 [[ 5, 3, 9], [ 4,16,15], [16,13, 7]]
07 [[ 4,16, 1], [13,14, 1], [15, 9, 8]]
14 [[ 4,11, 1], [ 1, 1, 1], [13, 7,14]]
15 [[ 1,17, 8], [15,16, 8], [12, 8, 8]]
25 [[15,10, 1], [14, 4, 6], [10, 4,11]]
26 [[17,14,17], [ 7,10,10], [16,17,13]]
36 [[ 2,16, 8], [13,14, 6], [12,12, 3]]
37 [[15,17, 4], [ 6,17,13], [12,16, 1]]
```

All eight determinants are nonzero.  Before normalization the three pure
coefficients are

\[
                         (1755,44304,4424).              \tag{15}
\]

For each block incident with site zero, multiply row `c` by the reciprocal
of the `c`-th number in (14).  Site multilinearity makes all three pure
coefficients exactly one, while preserving every block rank and every star
rank.

The support is sharp twice over.

* Every pair deletion leaves each endpoint with an invertible retained
  block, so all 28 pairs are doubly injective.
* Removing any support edge leaves one endpoint of degree one.  Deleting
  its other neighbour then leaves a zero star.  Thus the displayed source
  is edge-deletion-minimal for the all-pairs-good property, and (8)--(9)
  prove global minimality of its support size and show that total block rank
  24 is forced within this minimum-support stratum.

For each pair, the checker builds all 729 residual words and the literal
nine-column error matrix

\[
 C\longmapsto D H_R(A)[B^C]
 =\operatorname{contr}_{p,q}^C H_8(A)-\langle C,A_{pq}\rangle Q. \tag{16}
\]

Reduction modulo the prime `1000003` gives

\[
\begin{array}{c|c|c|c}
\text{pair type}&Q&\operatorname{rank}D&
 \operatorname{rank}[D\mid Q]\\ \hline
\text{same shore (12 pairs)}&0&9&9\\
\text{opposite shore (16 pairs)}&\ne0&9&10.
\end{array}                                                \tag{17}
\]

The normalization denominators are units modulo this prime.  Hence every
displayed nonzero minor lifts to a nonzero rational minor, and (16) proves
that the projective map has rank nine at all 28 pairs.  This is (3).

On the other hand, the identity cap is active and clean on all eight
support edges: its direct scalar is positive, its three diagonal readouts
are one, and the correction has the one-edge support used in (10).  Thus
the guard sharply says that projective deletion and clean Schur descent
cannot be identified.

## 4. The first unresolved support: a cubic physical guard

Take the cube graph

\[
 K_{4,4}\setminus\{04,15,26,37\},                      \tag{18}
\]

with shores `0,1,2,3` and `4,5,6,7`.  The checker freezes the following
twelve positive integral blocks in endpoint order:

```text
05 [[ 5, 3, 9], [ 4,16,15], [16,13, 7]]
06 [[ 4,16, 1], [13,14, 1], [15, 9, 8]]
07 [[ 4,11, 1], [ 1, 1, 1], [13, 7,14]]
14 [[ 1,17, 8], [15,16, 8], [12, 8, 8]]
16 [[15,10, 1], [14, 4, 6], [10, 4,11]]
17 [[17,14,17], [ 7,10,10], [16,17,13]]
24 [[ 2,16, 8], [13,14, 6], [12,12, 3]]
25 [[15,17, 4], [ 6,17,13], [12,16, 1]]
27 [[16, 2,10], [13, 6, 6], [17, 8, 1]]
34 [[ 7, 8,13], [17,12,12], [15, 9, 1]]
35 [[13,17, 5], [17, 7,14], [ 2,16,12]]
36 [[ 7,17,14], [16,12,14], [12, 1,11]]
```

Its integer pure coefficients are `(28170,106080,15242)`; the same
site-zero row normalization makes them `(1,1,1)`.  All blocks are
invertible, all 28 pairs are good, and the projective error ranks are nine
at all 28 pairs.  The normalized mixed word `01000000` is

\[
                              \frac{23257}{14085}\ne0.    \tag{19}
\]

This is the smallest possible support on which the degree-two theorem does
not fire.  At the support edge `05`, the external neighbour sets are
`{6,7}` and `{2,3}`.  The identity-cap correction therefore has a genuine
`K_(2,2)` square, while the leftover edge `14` is active.  Its all-zero
clean-error coefficient is the positive rational

\[
 \frac{10779982914855767329129}
 {134765354272985461922023296000},                       \tag{20}
\]

so the identity cap is not clean.  In fact every nonzero cap is dirty at
every support edge.  Fix such an edge `pq`, enumerate the two external
neighbours of `p` as `i_1,i_2` and those of `q` as `j_1,j_2`, and write the
four invertible star blocks as `P_alpha,S_beta`.  The effective blocks are

\[
                  R_{i_\alpha j_\beta}
                     =P_\alpha^{\mathsf T}KS_\beta.      \tag{21}
\]

Independent invertible changes of basis at the four residual sites turn
all four blocks in (21) into the same matrix `K`.  In those bases, the
coefficient of `r^[2]` with colour `a` at both `i`-sites and colour `c` at
both `j`-sites is

\[
                              2K_{ac}^2.                  \tag{22}
\]

Thus `r^[2]=0` forces `K=0`.  The two leftover residual vertices form an
active cube edge, so multiplication by its invertible block does not kill
`r^[2]`; and `r^[3]=0` because `r` uses only the four external sites.
Consequently the clean equation at an active edge forces either `s_K=0` or
`K=0`.  Both are inactive.  At each of the sixteen nonedges the direct
block is zero, so `s_K=0` for every cap there as well.

The cube therefore has **no active clean cap anywhere**.  Together with
projective rank nine, it is the smallest support counterguard to both
branches of the support/rank proposal.  Its one missing ingredient is
exactly the mixed target system, already exposed by (19); it is not a Krenn
counterexample.

### The complete cubic support classification

For a cubic graph and support edge `pq`, call the edge **sealed** when

1. the two external neighbour sets
   `N(p)-{q}` and `N(q)-{p}` are disjoint; and
2. the two vertices outside those four neighbours and `p,q` are adjacent.

An unsealed support edge is automatically actively clean.  If the external
sets meet, `r` uses at most three residual sites and `r^[2]=0`.  If they are
disjoint but the leftover pair is a nonedge, `r^[2]` can use only the four
external sites, its unique possible degree-two multiplier is the zero
leftover block, and `r^[3]=0`.  In either case the clean error vanishes for
every cap, and a cap avoiding the four activity hyperplanes exists because
the direct support block is nonzero.

There are exactly six simple cubic graph types on eight vertices.  The
checker generates all `19355` labelled cubic graphs, separates them by the
following signature, and verifies that the permutation orbit of each
representative has the full signature count.

| components | bipartite | triangles | four-cycles | sealed edges | labelled orbit | verdict |
|---|---:|---:|---:|---:|---:|---|
| `4+4` | no | 8 | 6 | 0 | 35 | active clean edge |
| `8` | no | 0 | 4 | 4 | 2520 | active clean edge |
| `8` | no | 1 | 3 | 6 | 3360 | active clean edge |
| `8` | no | 2 | 2 | 6 | 10080 | active clean edge |
| `8` | no | 4 | 2 | 2 | 2520 | active clean edge |
| `8` | yes | 0 | 6 | 12 | 840 | cube; terminal guard |

Thus the cube is the **unique** cubic support whose every edge is sealed.
The support/rank analysis at twelve edges is complete:

\[
 \boxed{\text{every non-cube cubic support has an active clean cap;}
 \quad Q_3\text{ is the sole support terminal}.}        \tag{23}
\]

The positive full-rank cube packet above proves that this terminal is real
before the mixed target equations are imposed.

### The full mixed equations exclude the cube

Now impose `H_8(A)=Delta_(8,3)` rather than only the three pure rows.  Every
cube vertex has support degree three.  The established cubic equality case
of the target-flattening/forced-anchor theorem therefore turns its three
incident aggregate blocks into three nonzero coordinate cells with distinct
target colours.  Applying this at both endpoints gives the same-colour
coordinate-cell normal form used in the independent cube subcase of
[`no-independent-four-set-at-eight.md`](no-independent-four-set-at-eight.md).

The three constant fibres then force the three colour classes to be a
one-factorisation of `K_(4,4)` minus its missing perfect matching.  There
are exactly 24 labelled factorisations.  The checker reconstructs all of
them from the literal nine derangements.  For **every** factorisation:

* each of the three constant detector words has exactly one supported
  matching; and
* exactly six mixed detector words have exactly one supported matching.

For the first canonical factorisation those mixed words are

```text
01101001  02022020  10010110
11222211  20200202  22111122
```

The coefficient of any such word is the product of four nonzero coordinate
cells.  It cannot cancel, contradicting the corresponding mixed target row.
Thus the cube support itself is impossible for an exact source.

Combining the degree-two theorem, the six cubic support classes, and this
last mixed-row obstruction gives the promised restricted full-source
theorem:

\[
 \boxed{H_8(A)=\Delta_{8,3}\text{ and all 28 pairs good}
        \quad\Longrightarrow\quad |E(\operatorname{supp}A)|\ge13.} \tag{24}
\]

This is not a proof of the eight-site case: the target-flattening theorem
guarantees several good pairs, not that all 28 pairs are good.  It is a
literal support/rank deletion theorem on a broad, sharply guarded stratum.

## 5. The thirteen-edge layer

The cubic definition of sealed edge has a useful exact extension.  For an
active edge `pq`, let

\[
 P=N(p)\setminus\{q\},\qquad S=N(q)\setminus\{p\},
 \qquad
 {cal R}_{pq}=\{ij:i\in P,\ j\in S,\ i\ne j\}.        \tag{27}
\]

Every physical edge which can occur in the effective response `r=B^K`
lies in `R_pq`.  Enumerate the fifteen perfect matchings of the six residual
sites and ask whether one can be tagged

* `RRR`, with all three edges in `R_pq`; or
* `RRX`, with two edges in `R_pq` and the third in the original support.

If neither tagging exists, both terms of

\[
                 {\cal E}_{p,q}(K)=s_Kr^{[2]}x+r^{[3]} \tag{28}
\]

vanish coefficient-independently for every `K`.  Since `A_pq` is nonzero,
a cap can be chosen off its direct-scalar hyperplane and the three diagonal
activity hyperplanes.  Hence such an edge is actively clean.  On a cubic
graph this exact matching test is equivalent to the simpler definition of
sealed edge above; the checker verifies the equivalence on all 19,355
labelled cubic graphs.

At thirteen edges, a degree-two vertex is already closed by Section 2.
If the minimum degree is at least three, the degree sum is 26, so there are
only two degree sequences:

\[
                  (5,3^7),\qquad (4,4,3^6).            \tag{29}
\]

The checker enumerates both sequences with the exceptional-degree labels
pinned and applies the literal `RRR/RRX` test at every support edge.

| degree sequence | labelled graphs | no support-clean edge |
|---|---:|---:|
| `(5,3^7)` | 9,660 | 0 |
| `(4,4,3^6)` | 15,740 | 120 |

The 120 survivors form one orbit under `S_2 x S_6`.  A representative has
edges

```text
01 02 03 04  15 16 17  25 26 35 37 46 47.
```

With shores `{0,5,6,7}` and `{1,2,3,4}`, this is precisely

\[
               K_{4,4}\setminus\{27,36,45\}.           \tag{30}
\]

Thus it has two independent four-sets, and each missing cross edge joins
two cubic vertices.  This verifies every graph-side premise of the
dead-cross branch of the proved
[`no-independent-four-set-at-eight`](no-independent-four-set-at-eight.md)
theorem.  That branch is genuinely a full-mixed-row exclusion: after the
one-live-row/column reduction, its checker derives 141 nonconstant `2x2`
rectangle rows; in all eight constant-fibre cases their closure fills all
36 core cells and contradicts the required anchors.  No coefficient or
positivity specialization is used.

Consequently the terminal is not an exact source, while every other
thirteen-edge support already supplies an active clean cap.  Together with
the six-site obstruction this strengthens (24) to

\[
 \boxed{H_8(A)=\Delta_{8,3}\text{ and all 28 pairs good}
        \quad\Longrightarrow\quad |E(\operatorname{supp}A)|\ge14.} \tag{31}
\]

## 6. The support-14 terminal census

The five degree sequences corresponding to the partitions of four excess
degrees above `3^8` are

```text
(7,3^7)  (6,4,3^6)  (5,5,3^6)  (5,4,4,3^5)  (4,4,4,4,3^4).
```

The same exact `RRR/RRX` matching test gives:

| degree sequence | labelled graphs | no support-clean edge |
|---|---:|---:|
| `(7,3^7)` | 465 | 0 |
| `(6,4,3^6)` | 3,030 | 0 |
| `(5,5,3^6)` | 5,280 | 0 |
| `(5,4,4,3^5)` | 8,820 | 120 |
| `(4,4,4,4,3^4)` | 14,634 | 180 |

The 300 labelled terminals split into exactly four orbits under the
degree-preserving permutation groups:

| degrees | orbit | triangles | squares | independent `4`-sets | verdict |
|---|---:|---:|---:|---:|---|
| `(5,4,4,3^5)` | 120 | 4 | 8 | 1 | full-row cube exit |
| `(4^4,3^4)` | 72 | 4 | 5 | 0 | **first terminal** |
| `(4^4,3^4)` | 36 | 0 | 19 | 2 | full-row dead-cross exit |
| `(4^4,3^4)` | 72 | 4 | 6 | 1 | full-row cube exit |

For the first and fourth rows, zeroing the two internal complement edges by
the independent-shore invisibility identity leaves `K4,4` minus a perfect
matching.  The six unique mixed fibres of the cube exclusion apply.  The
third row is already bipartite `K4,4` minus two disjoint edges; either dead
edge has cubic endpoints, so the 141 mixed rectangle rows apply.  Thus these
are source-valid full-row exits, not conclusions drawn merely from their
support pictures.

The remaining 72-label orbit has representative

```text
01 02 04 05  13 14 16  23 25 27  36 37  47 56.
```

Its degree-four vertices `0,1,2,3` span the cycle
`0-1-3-2-0`.  Vertices `4,6,7,5` are respectively the apices on its four
edges, and `47,56` pair apices belonging to opposite core edges.  Hence the
name **opposite-apex triangulated `C4`**.  It has four triangle faces, five
four-cycles, and no independent four-set.

The checker refines its fourteen sealed edges into three geometric types:

| endpoint degrees | edges | `RRR` witnesses | `RRX` witnesses per edge |
|---|---:|---:|---:|
| `(4,4)` core | 4 | 0 | 6 |
| `(4,3)` triangle spoke | 8 | 0 | 2 |
| `(3,3)` opposite-apex | 2 | 0 | 2 |

Thus `r^[3]` vanishes support-theoretically at every edge, but an active
residual `x` edge can multiply `r^[2]` everywhere.  The graph has not been
shown to carry coefficients satisfying the complete source equations; it
is the first point where support plus the independent-shore theorem stops.
The sharp next attack is finite: use the forced three distinct anchors at
each cubic apex, impose the three constant fibres, and enumerate the mixed
fibres on the resulting four triangle charts.  A unique mixed monomial
would exclude the orbit; a survivor would be the first genuine coefficient
guard at support 14.

## 7. Why the mixed equations are the first missing hypothesis

The construction is one endpoint-ordered quadratic.  Consequently every
pair response, restriction, and direct-edge/two-star matching identity is
automatically compatible across all 28 charts.  It is not a collection of
independent local shadows.

It nevertheless fails the target equation.  All displayed matrix entries
are positive, and the normalized coefficient of the mixed detector word

\[
                             01000000                    \tag{25}
\]

is exactly `1283/117`, not zero.  This explains the rank jump between (1)
and (17): the complete mixed GHZ equations collapse the projective error
rank from a possible nine to at most three.  Pure normalization, minimum
support, the rank forced on that support, all-pair goodness, and common
physical provenance do not cause that collapse.

The value `1283/117` is not needed to close supports at most eleven: the
degree-two clean theorem closes that layer before its sign can matter.  It
is instead the exact witness that pure normalization and common physical
provenance have not imposed the mixed target equations.  The cube value
(19) is the corresponding first witness at the genuine cubic boundary.
After the exact cubic equality case is imposed, the full-rank numerical
word `01000000` is replaced by the six unique coordinate-cell words above;
this is the rank degeneration through which the mixed rows kill the cube.

Beyond the support-13 closure, the shortest remaining direct-deletion
attack is now precise:

1. use at least one genuinely mixed full-source row to constrain the
   six-site deleted tensor `Q`, not merely the endpoint stars;
2. prove that for some good pair `Q` lies in the open diagonal plane
   `E^times` of (2); or
3. bypass `Q` by proving a local one-edge (or another nilpotent-support)
   condition on `B^K`, as in the minimum-support clean theorem.

The first-order zero-error statement without target activity is already
automatic and carries no descent.

## 8. Reproduction

```sh
python3 computations/verify_n8_support_rank_minimal_projective_cap_error_counterguard.py
python3 -O computations/verify_n8_support_rank_minimal_projective_cap_error_counterguard.py
python3 -I -S computations/verify_n8_support_rank_minimal_projective_cap_error_counterguard.py
python3 computations/verify_no_independent_four_set_at_eight.py
python3 -O computations/verify_no_independent_four_set_at_eight.py
python3 -I -S computations/verify_no_independent_four_set_at_eight.py
```

The frozen exact ledger digest is
`03747d5ca991950d5f9b81db8ab49d7422b16ba11bb4f49aa1c70162d6a03447`.
