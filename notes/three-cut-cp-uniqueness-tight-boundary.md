# Three-cut CP uniqueness reaches a tight-cut boundary

## 1. Outcome

Rank three across every balanced \(3|3\) flattening, even together with
Kruskal uniqueness of the global rank-three CP decomposition, does not
separate the one-cross and three-cross matching sectors. There is an exact
six-site rank-one aggregate source whose output has:

1. CP rank exactly three and an essentially unique three-term decomposition;
2. matrix rank exactly three across all twenty \(3|3\) cuts;
3. a matching-covered, bridgeless, two-connected support with no edge common
   to all perfect matchings; and
4. on one \(3|3\) cut, a one-cross sector equal to one CP summand and a
   three-cross sector equal to the other two CP summands.

The escape is precise: two sites have deficient local CP factor matrices.
The support also has a nontrivial tight three-cut. Thus the example does not
refute a theorem using the full local geometry of the target; it shows that
balanced flattening ranks and uniqueness alone do not contain that geometry.

There is a complementary uniform positive lemma. Every matching-covered
graph on any even number \(n\geq6\) of vertices with exactly three perfect
matchings has a nontrivial tight three-vertex shore. Contracting that shore
is an explicit \(n\mapsto n-2\) reduction. In the rank-one three-matching
chart, if the three matching
terms were the unique CP decomposition of a tensor with three independent
local factors at every site—as they are for \(\Delta_{6,3}\)—the matchings
would be pairwise edge-disjoint. The standard three-one-factors lemma would
then supply a fourth perfect matching. Hence the target cannot occur in this
chart.

What remains open is exactly the coefficient-aware case with more than three
matching terms. CP uniqueness applies to minimal three-term decompositions;
it does not prohibit a longer pure-tensor expansion with cancellations.

## 2. One-cross and three-cross sectors at six sites

Fix a three-set \(S\) and its three-set complement. Every perfect matching
crosses \(S\) an odd number of times, hence either once or three times. Write

\[
                         H_6(A)=T_1^S+T_3^S.             \tag{1}
\]

The target has the unique CP decomposition

\[
                 \Delta_{6,3}=\sum_{r=0}^2e_r^{\otimes6}. \tag{2}
\]

It is tempting to infer from the rank-three flattening of (2) that one of the
two sectors in (1) must vanish or miss the target CP directions. The example
below shows that neither conclusion follows from rank and CP uniqueness.

## 3. Exact six-site countermodel

Use the three perfect matchings

\[
\begin{aligned}
 M_0&=01\mid23\mid45,\\
 M_1&=01\mid24\mid35,\\
 M_2&=02\mid34\mid15.                                   \tag{3}
\end{aligned}
\]

Put the following rank-one matrices on their union and zero elsewhere:

\[
\begin{array}{c|c}
01,23,45&E_{00}\\
24,35&E_{11}\\
02,34,15&E_{22}.
\end{array}                                               \tag{4}
\]

The underlying eight-edge graph has exactly the three perfect matchings in
(3). Therefore its matching tensor is

\[
 T=e_0^{\otimes6}
   +(e_0\otimes e_0\otimes e_1\otimes e_1\otimes e_1\otimes e_1)
   +e_2^{\otimes6}.                                      \tag{5}
\]

At sites \(0,1\), the three local CP factors are
\((e_0,e_0,e_2)\), of Kruskal rank one. At each of sites \(2,3,4,5\), they
are \((e_0,e_1,e_2)\), of Kruskal rank three. Hence the sum of the six
Kruskal ranks is

\[
                         1+1+3+3+3+3=14.
\]

For a six-way rank-three tensor, Kruskal's uniqueness threshold is
\(2\cdot3+(6-1)=11\). Thus (5) is an essentially unique CP decomposition.
It also has CP rank exactly three.

Every three-set and its complement contains at least one of the four sites
\(2,3,4,5\). At such a site the three local factors form a basis, so the
three grouped product vectors on that shore are independent. The same holds
on the opposite shore. It follows that every one of the twenty balanced
flattenings of \(T\) has matrix rank exactly three.

Now take

\[
                              S=\{0,3,5\}.                \tag{6}
\]

The crossing counts of \((M_0,M_1,M_2)\) are \((3,1,3)\). Consequently

\[
\begin{aligned}
 T_1^S&=
 e_0\otimes e_0\otimes e_1\otimes e_1\otimes e_1\otimes e_1,\\
 T_3^S&=e_0^{\otimes6}+e_2^{\otimes6}.                  \tag{7}
\end{aligned}
\]

Both sectors are nonzero. More strongly, the three-cross sector is exactly
the sum of two members of the unique CP decomposition. Its left and right
Schmidt spaces are two-dimensional subspaces of the corresponding
rank-three CP spaces. CP uniqueness identifies this contamination; it does
not remove it.

All eight edges in (4) belong to a perfect matching. The support has no
bridge, no articulation vertex, and no edge common to all three matchings.
It nevertheless has a tight cut:

\[
                              \{0,1,2\}\mid\{3,4,5\}.     \tag{8}
\]

Each matching in (3) crosses (8) exactly once. This is the compressible
boundary left invisible by the numerical flattening ranks.

There is also a sharp activity warning. Add an arbitrary full-rank matrix
on edge \(05\). Its complementary four-site graph on
\(\{1,2,3,4\}\) has no perfect matching, so no global matching uses \(05\).
The output, its unique CP decomposition, and all twenty flattening ranks
remain unchanged. Thus no raw aggregate-edge rank conclusion follows
without first imposing tensor activity or entry minimality.

## 4. Three perfect matchings force a uniform tight cut

Call a support matching-covered when every edge belongs to a perfect
matching.

**Lemma 4.1.** Let \(G\) be a matching-covered graph on an even number
\(n\geq6\) of vertices with exactly three perfect matchings. Then some
three-set \(S\)
satisfies

\[
                         |M\cap\delta(S)|=1              \tag{9}
\]

for every perfect matching \(M\) of \(G\).

**Proof.** Denote the matchings by \(M_0,M_1,M_2\). Two of them share an
edge: otherwise their pairwise edge-disjoint union would contain a fourth
perfect matching by the standard three-one-factors lemma (the exceptional
three-one-factorization of \(K_4\) is excluded by \(n\geq6\)).

First suppose an edge \(uv\) occurs in exactly two matchings, say
\(M_0,M_1\), and write \(ux\in M_2\). Set \(S=\{u,v,x\}\). In each of
\(M_0,M_1\), the edge \(uv\) lies inside \(S\), while the mate of \(x\)
lies outside \(S\). In \(M_2\), the edge \(ux\) lies inside \(S\), while
the mate of \(v\) lies outside. Thus all three matchings cross
\(\delta(S)\) exactly once.

The only remaining case is that every shared edge occurs in all three
matchings. Choose such a common edge \(uv\) and any
\(x\notin\{u,v\}\). For \(S=\{u,v,x\}\), all three matchings use the
internal edge \(uv\), and each sends \(x\) outside \(S\). Again (9)
holds. \(\square\)

Because \(|S|=3\) and \(n\geq6\), both shores are nontrivial. The usual
tight-cut contraction replaces \(S\) by one vertex and produces a graph on
\(n-2\) vertices. This is the promised explicit compression, rather than
merely a numerical rank defect.

For comparison, the complete six-site support classification can also be
written down. Normalize a shared pair to

\[
 01\mid23\mid45,\qquad 01\mid24\mid35.                   \tag{10}
\]

There are only thirteen remaining perfect matchings. Up to the stabilizer
of the unordered pair (10), requiring that their union contain no fourth
perfect matching leaves the following three matching-covered unions:

\[
\begin{array}{c|c}
\text{third matching}&\text{edge set}\\ \hline
01\mid25\mid34&
\{01,23,24,25,34,35,45\}\\
02\mid13\mid45&
\{01,02,13,23,24,35,45\}\\
02\mid15\mid34&
\{01,02,15,23,24,34,35,45\}.
\end{array}                                               \tag{11}
\]

Any extra edge of a matching-covered graph belongs to a fourth matching, so
(11) is also the complete six-site support classification. In every row of
(11), the three-set \(S=\{0,1,2\}\) is crossed exactly once by all three
matchings, in agreement with Lemma 4.1.

The finite check in (11) is particularly small: normalize (10), list the
fifteen matchings of six vertices, and discard the two already chosen and
every candidate whose union supports a fourth. The verifier independently
performs the label-free version over all \(\binom{15}{3}\) triples. It finds
375 labelled matching-covered supports, three isomorphism classes, and a
tight three-set in every case.

## 5. CP consequence in the rank-one three-term chart

**Proposition 5.1.** Suppose a matching-covered source on an even number
\(n\geq6\) of sites has nonzero rank-one matrices on its support and exactly
three perfect matchings. If its matching tensor has CP rank three and its
displayed matching terms form the unique minimal CP decomposition, then the
support has a tight three-vertex shore and admits the \(n\mapsto n-2\)
tight-cut contraction. If, in addition, the three local CP factors are
independent at every site, the chart is impossible.

**Proof.** Lemma 4.1 gives the tight cut and contraction. For the second assertion, uniqueness
identifies the three matching products with the three CP summands, up to
rescaling and permutation. If two matchings shared an edge \(uv\), the
rank-one matrix on that edge would give them proportional local factors at
both \(u\) and \(v\), contradicting local independence. The three matchings
are therefore pairwise edge-disjoint. Their union has a fourth perfect
matching. Every edge matrix is nonzero and rank one, so that fourth matching
gives another nonzero matching term, contrary to the hypothesis that the
support has exactly three perfect matchings. \(\square\)

For \(\Delta_{n,3}\), local independence and CP uniqueness both hold. The
proposition therefore closes the rank-one, exactly-three-matching chart for
every even \(n\geq6\).
It does not extend automatically to a source with additional matching
terms: a unique minimal CP decomposition can coexist with a longer
nonminimal pure-tensor expansion, and complex cancellation is exactly the
uncontrolled issue.

## 6. Exact audit

[verify_three_cut_cp_uniqueness_tight_boundary.py](../computations/verify_three_cut_cp_uniqueness_tight_boundary.py)
checks over the integers that:

1. (4) has exactly the three supported perfect matchings (3) and output (5);
2. all twenty balanced flattenings have rank three;
3. the local Kruskal ranks are \((1,1,3,3,3,3)\);
4. the sector split (7), support activity, connectivity properties, and
   tight cut (8) hold;
5. the full-rank edge \(05\) is tensor-inactive; and
6. all 375 six-vertex labelled unions supporting exactly three perfect
   matchings have a tight three-set, in three isomorphism classes; and
7. the uniform constructive proof is exhaustively audited on all 69,090
   eight-vertex triples whose union supports exactly three perfect matchings.
