# Occurrence bridges under full fibre equations and at square degree

## Outcome

There are two distinct obstructions, and they should not be conflated.

First, degree doubling removes the *literal* bridge but not its odd-cut
defect.  If two locally-rainbow cubic states cross the same odd shore once,
their product has two crossing occurrences.  A decomposition at square
degree would require six perfect matchings, hence at least six crossing
occurrences.  Thus neither a pure bridge square nor a product of two
different bridge states lies in the six-perfect-matching monomial cone.

Second, the complete homogeneous mixed-fibre system does not force an
occurrence bridge to become a support-level separator or to produce an odd
Laurent circuit.  A 67-cell rational sign model on six sites has exactly two
opposite terms in every one of its `729` colouring fibres.  It contains the
bridge state from `higher-epsilon-web-saturation.md`, but two of its mixed
rewrites merely move the unique bridge to a different crossing edge.  Its
full pair support is the dense graph

\[
                       K_6\setminus\{13,45\}.
\]

The missing input is normalization: all three *complete* pure coefficients
of this model are zero, although the three selected pure monomials are each
one.  Conversely, a smaller 15-cell model satisfies the three inhomogeneous
constant equations and the bridge relation exactly, but fails six other
mixed equations.  These two models locate the boundary; neither is a Krenn
counterexample.

## 1. Odd-cut capacity survives degree doubling

For an occurrence multigraph `D` and a shore `S`, count cut occurrences with
multiplicity and denote the result by `b_S(D)`.

**Lemma 1 (cut-capacity obstruction).**  Let `S` have odd cardinality, and
let `G_1,...,G_m` be spanning occurrence graphs, each of degree three at
every site and satisfying

\[
                          b_S(G_i)=1.
\]

Then the product occurrence multigraph

\[
                          D=G_1\cdots G_m
\]

cannot be partitioned into `3m` perfect matchings.

**Proof.**  The graph `D` has degree `3m` at every site, so a perfect-matching
partition would have exactly `3m` classes.  Every perfect matching crosses
an odd shore an odd number of times, in particular at least once.  Such a
partition would therefore give

\[
                         b_S(D)\geq 3m.
\]

On the other hand, cut occurrences add under products, so

\[
                         b_S(D)=\sum_i b_S(G_i)=m.
\]

This is impossible for every positive `m`. `QED`

The useful square case is `m=2`.  If the two bridge occurrences coincide,
the product contains two parallel copies and neither copy is a graph bridge.
If they differ, either crossing occurrence can be deleted while the other
still connects the shores.  In both cases the doubled graph can be literally
bridgeless while its cut multiplicity is only two.  Thus “the bridge
disappears in the square” is not a matching-cover argument.

The same proof gives a slightly more general test: any degree-`3m` occurrence
multigraph with `b_S(D)<3m` is absent from every `3m`-perfect-matching source
web, regardless of endpoint colours or local bracket choices.

## 2. A normalized four-term bridge relation

Use the selected matchings

\[
\begin{aligned}
 P_0&=04|12|35,\\
 P_1&=05|14|23,\\
 P_2&=03|15|24,
\end{aligned}
\]

and give their constant-colour occurrences weight one.  Their union is the
selected locally-rainbow state `U`.  It contains

\[
 R=04_{00}|15_{22}|23_{11},\qquad
 c=(0,2,1,1,0,2).
\]

Add the following six cells and no others:

\[
\begin{array}{c|cc}
 &\text{first new cell}&\text{second new cell}\\ \hline
 N_0&12_{21}=-1/3&35_{12}=1\\
 N_1&05_{02}=-1/3&14_{20}=1\\
 N_2&03_{01}=-1/3&24_{10}=1.
\end{array}
\]

Together with the shared selected cells `04_00`, `23_11`, and `15_22`, the
rows form the three `c`-compatible matchings

\[
\begin{aligned}
 N_0&=04_{00}|12_{21}|35_{12},\\
 N_1&=05_{02}|14_{20}|23_{11},\\
 N_2&=03_{01}|15_{22}|24_{10}.
\end{aligned}
\]

The complete `c`-fibre is exactly

\[
                     z(R)+z(N_0)+z(N_1)+z(N_2)
                     =1-\frac13-\frac13-\frac13=0.       \tag{1}
\]

Each constant fibre is a singleton `P_i` of coefficient one.  Put

\[
 Q=U\setminus R,\qquad G_i=Q\sqcup N_i,
\]

and write `u=w_U`, `g_i=w_{G_i}`.  Multiplying (1) by `w_Q` gives

\[
                        \rho:=u+g_0+g_1+g_2=0,             \tag{2}
\]

with exact values

\[
                      (u,g_0,g_1,g_2)
                      =\left(1,-\frac13,-\frac13,-\frac13\right). \tag{3}
\]

For the odd shore

\[
                             S=\{0,3,5\},                  \tag{4}
\]

the states `G_0,G_1,G_2` have unique bridges `04_00`, `23_11`, and `15_22`,
respectively.  Every state has exactly four occurrence-perfect-matchings,
and all four use its bridge.  The underlying pair support is nevertheless
the 3-connected triangular prism.

This 15-cell assignment is a genuine common zero of

\[
 F_c,\quad F_{0^6}-1,\quad F_{1^6}-1,\quad F_{2^6}-1.     \tag{5}
\]

It is important not to extend that statement: among all `729` fibres, the
term-count distribution is

\[
                   \#0\text{-term}=719,\quad
                   \#1\text{-term}=9,\quad
                   \#4\text{-term}=1,                     \tag{6}
\]

and exactly six of the other mixed coefficients are nonzero.

## 3. Exact square-level obstruction for the local relation

The selected state has `b_S(U)=3`, whereas `b_S(G_i)=1`.  Therefore

\[
 b_S(U^2)=6,\qquad b_S(UG_i)=4,\qquad b_S(G_iG_j)=2.       \tag{7}
\]

Every product in (7) is degree six at each site.  The odd-cut capacity bound
shows that none of the last two types can be partitioned into six perfect
matchings.  Direct
deletion confirms that all nine multigraphs `G_iG_j` have no literal graph
bridge, so the failure is strictly an odd-cut-capacity failure.

There is also a small exact dual certificate.  Let `V_2` be the vector space
spanned by the ten commutative quadratic monomials in

\[
                         x=(u,g_0,g_1,g_2).
\]

The quadratic consequences of (2) are the four rows `rho*x_k`.  For

\[
                         \alpha=(0,1,-1,0)
\]

define

\[
                \Lambda_\alpha(x_i x_j)=\alpha_i\alpha_j. \tag{8}
\]

Since `sum_i alpha_i=0`,

\[
       \Lambda_\alpha(\rho x_k)=0\quad(0\leq k<4),\qquad
       \Lambda_\alpha(u^2)=0,
       \qquad\Lambda_\alpha(g_0^2)=1.                     \tag{9}
\]

Within this four-state monomial span, `u^2` is the only monomial which even
passes the necessary six-matching cut test.  Thus `g_0^2` is not in the span
of the good monomial `u^2` and the four quadratic rewrite rows.  This is a
square-level dual counterfunctional to the proposed *local* finite
reduction.

A second dual records the inhomogeneous equations.  Evaluation at the
15-cell assignment annihilates the ideal generated by (5), takes `u^2` to
one, and on `V_2` is the rank-one functional associated with

\[
                  \beta=\left(1,-\frac13,-\frac13,-\frac13\right).
\]

It annihilates every `rho*x_k` because `sum beta_i=0`.  Hence the bridge
relation together with the three normalized constant equations is exactly
consistent; no finite algebraic contradiction can use only those four
equations.  This does not rule out a reduction using the omitted mixed
fibres.

## 4. A full 729-binomial model in which the bridge moves

The preceding local model deliberately misses mixed equations.  The next
model satisfies the entire homogeneous fibre system.  Its 67 supported
cells are specified below; each two-digit string is an endpoint-colour pair.

\[
\begin{array}{c|l@{\qquad}c|l}
01&12&02&10,11,12\\
03&00,01,02,20,21,22&04&00,01,02,20,21,22\\
05&00,01,10,11,20,21&12&00,02,10,12,20,21,22\\
14&00,01,02,10,11,12&15&01,02,11,12,21,22\\
23&10,11,12&24&00,01,02,20,21,22\\
25&10,12&34&00,01,02,10,11,12,20,21,22\\
35&00,02,10,12,20,22&&
\end{array}                                                \tag{10}
\]

Initially give every supported cell weight `+1` except

\[
\begin{gathered}
15_{01},15_{11},15_{21},\quad
25_{10},25_{12},\\
35_{00},35_{02},35_{10},35_{12},35_{20},35_{22},
\end{gathered}                                             \tag{11}
\]

which have weight `-1`.  Finally apply the endpoint gauge which multiplies
every supported cell using port `(0,0)` by `-1`.

**Lemma 2 (full-binomial bridge model).**  For the weights (10)--(11):

1. every one of the `3^6=729` colouring fibres has exactly two supported
   perfect matchings;
2. their weights are `+1` and `-1`, so every coefficient is zero;
3. the selected constant monomials on `P_0,P_1,P_2` each have weight `+1`;
4. the bridge state

   \[
             G=(U\setminus R)\sqcup
               (04_{00}|12_{21}|35_{12})                 \tag{12}
   \]

   is connected, locally rainbow, and has unique bridge `04_00` across
   (4); all four occurrence-perfect-matchings of `G` use that bridge.

The proof is finite exact enumeration.  There are only fifteen underlying
perfect matchings in each fibre.  The checker constructs all fifteen,
intersects them with (10), and verifies the two term weights over the
integers.  No random or floating-point step is used.

Three of the four occurrence-perfect-matchings in (12) are mixed.  Their
unique fibre mates behave as follows:

\[
\begin{array}{c|c|c|c}
\text{colouring}&\text{unique other matching}&
 b_S(\text{old}),b_S(\text{mate})&\text{new state}\\ \hline
(0,0,0,1,0,2)&03_{01}|15_{02}|24_{00}&1,1&
   b_S=1,\ \text{bridge }15_{02}\\
(0,2,1,0,0,0)&05_{00}|12_{21}|34_{00}&1,1&
   b_S=1,\ \text{bridge }34_{00}\\
(0,2,1,1,0,2)&04_{00}|15_{22}|23_{11}&1,3&
   U,\ b_S=3,\ \text{no bridge}.
\end{array}                                                \tag{13}
\]

Thus the full mixed system supplies an escape only through the reversible
move back to `U`; two other exact equations transport the one-edge cut and
change which occurrence is its bridge.  There is no rule forcing every
mixed occurrence matching in a bridged state to have a mate with three or
more cut crossings.

There is also no hidden support contraction.  The pair support in (10) is
`K_6` minus `13` and `45`, has ten perfect matchings, remains connected after
deleting any two vertices, and has seven pair edges across (4).  It has no
nontrivial tight odd shore.  The one-edge cut belongs to the *particular
occurrence state* (12), not to the tensor support.  Contracting its shores
would discard the two bridge-moving mates in (13), so it is not an operation
preserved by the fibre equations.

Finally, (10)--(11) is itself a nonzero solution of all signed binomial
relations.  Any odd Laurent sign circuit would multiply those relations to
`1=-1`, which is impossible at this assignment.  Hence the complete
binomial support has no such circuit.  This directly rules out deriving an
odd Laurent contradiction from these fibres.

The price is unavoidable and explicit: each pure fibre also has its second,
opposite term.  Therefore

\[
                    F_{0^6}=F_{1^6}=F_{2^6}=0,             \tag{14}
\]

not one.  The model proves a limitation of the homogeneous mixed equations,
not failure of the normalized conjecture.

## 5. Relation to the arbitrary-matrix square filtration

In the notation of `ideal-membership-route.md`, let `K` be the ideal of
bichromatic cells.  In the normalized 15-cell model, `u` has `K`-degree zero
and every `g_i` has `K`-degree two.  Consequently

\[
        \deg_K(u^2)=0,\qquad \deg_K(ug_i)=2,\qquad
        \deg_K(g_i g_j)=4.                                \tag{15}
\]

The local dual (8) therefore lives entirely at or below off-diagonal degree
four.  Section 6 of `ideal-membership-route.md` proves globally that

\[
                              P^2\in I+K^6.
\]

So the constructed full mixed Macaulay lift has no target remainder through
degree five.  There is no conflict: the 15-cell point fails exactly six
additional mixed equations, and their global consequences are absent from
the four-row state calculation above.  In particular, the local dual cannot
extend to a target-separating dual of the full square Macaulay map through
that filtration range.

Conversely, the 67-cell point satisfies all mixed equations but has
`P=F_{0^6}F_{1^6}F_{2^6}=0`, so evaluation there cannot separate `P^2` from
the mixed ideal.  The two exact models therefore leave the full square
question precisely where the filtration computation puts it: any remaining
dual obstruction must use the globally coupled normalized system and first
survive in off-diagonal degree at least six.  Literal disappearance of an
occurrence bridge at degree two supplies no shortcut through that tail.

The dependency-free audit is
`computations/verify_bridge_rewrite_square_boundary.py`.
