# A cubic obstruction to a support-only loop reduction

This note records a finite counterexample to the following tempting
support-level claim:

> If a connected matching-covered cubic graph has a fixed perfect matching
> `M_0` and has no proper `M_0`-alternating cycle, then it has at most one
> perfect matching other than `M_0`.

The claim is false already on eight vertices.  Consequently, vanishing of
all *properly supported* loop activities does not by itself force the full
loop sector to consist of a single term.  Any useful version of that
argument must retain the compatibility imposed by sharing aggregate edge
matrices (or use cancellation data, rather than support alone).

## 1. The graph

Let

\[
 M_0=\{01,23,45,67\}
\]

and add the eight edges

\[
 04,05,12,13,27,37,46,56.                              \tag{1}
\]

Thus

\[
\begin{split}
E(G)=\{&01,04,05,12,13,23,27,37,\\
       &45,46,56,67\}.
\end{split}                                               \tag{2}
\]

The graph is connected and cubic.  Its perfect matchings are exactly

\[
\begin{array}{c|c}
0 & 01,23,45,67\\
1 & 04,12,37,56\\
2 & 04,13,27,56\\
3 & 05,12,37,46\\
4 & 05,13,27,46.
\end{array}                                                \tag{3}
\]

In particular every edge occurs in a perfect matching, so `G` is
matching-covered.

There is a short direct enumeration.  A matching containing `01` is forced
successively to contain `23,45,67`, giving `M_0`.  Otherwise vertex `0`
is paired with `4` or `5`, and vertex `1` is paired with `2` or `3`.
Those two binary choices force the partners of all four remaining vertices,
and give precisely the last four rows of (3).

## 2. All relative loops are spanning

For each `i=1,2,3,4`, the symmetric difference

\[
                         M_i\mathbin\triangle M_0          \tag{4}
\]

contains all eight vertices.  Since the symmetric difference of two
perfect matchings is a disjoint union of alternating cycles, it is enough
to display the four differences as cycles:

\[
\begin{array}{c|c}
1&0,1,2,3,7,6,5,4,0\\
2&0,1,3,2,7,6,5,4,0\\
3&0,1,2,3,7,6,4,5,0\\
4&0,1,3,2,7,6,4,5,0.
\end{array}                                                \tag{5}
\]

Each is therefore a Hamilton alternating cycle.

Conversely, flipping any `M_0`-alternating cycle produces a perfect
matching.  The complete list (3) therefore proves that `G` has no proper
`M_0`-alternating cycle at all, although it has four distinct spanning
ones.  This disproves the support-level claim above under all of the usual
minimal-core graph hypotheses (connected, cubic, and matching-covered).

## 3. The top-loop rectangle

Give the eight non-`M_0` edges in (1) scalar labels

\[
 a=04,\ b=05,\ c=12,\ d=13,\ e=27,\ f=37,\ g=46,\ h=56.
\]

After dividing by the nonzero weight of `M_0`, the four spanning-loop
monomials are, up to the corresponding inverse `M_0` weights,

\[
                  acfh,\qquad adeh,\qquad bcfg,\qquad bdeg. \tag{6}
\]

They satisfy the rectangle relation

\[
                  (acfh)(bdeg)=(adeh)(bcfg).               \tag{7}
\]

In fact their sum factors:

\[
 acfh+adeh+bcfg+bdeg=(ah+bg)(cf+de).                       \tag{8}
\]

This is not an accident.  Deleting `M_0` leaves the disjoint union of the
two four-cycles on

\[
             \{0,4,5,6\}\qquad\hbox{and}\qquad\{1,2,3,7\}.
\]

Hence, even with arbitrary aggregate edge tensors rather than scalar edge
labels, the tensor sum of the four alternative matchings factors across
this vertex bipartition.  It has flattening rank at most one there.  In
particular it cannot equal
`e_1^(tensor 8)+e_2^(tensor 8)`, whose rank across every nontrivial
flattening is two.

Thus the four terms are not arbitrary, but neither are they literally a
single loop term.  Equations (7)--(8) display the residual edge-sharing
compatibility that a tensor or colored loop argument has to exploit.  This
example refutes the *counting* claim while remaining consistent with the
stronger conjectural rank-one conclusion for a top excitation sector.

## 4. A valid factorization lemma at cross-degree two

The factorization seen above is forced if the active graph away from the
vacuum matching has maximum degree two.  It is useful to state this at the
level of decorated edge occurrences, so parallel sources and asymmetric
endpoint colors remain distinct.

**Lemma 4.1 (degree-two top-sector factorization).**  Let `M_0` be a fixed
perfect matching on an even vertex set `B`, with `|B|>=6`, and let `H` be a
multigraph on `B`, edge-disjoint from `M_0` as a set of occurrences.  Assume

1. `H` has a perfect matching;
2. every edge of `H` belongs to a perfect matching of `H`;
3. `Delta(H)<=2`; and
4. `M_0 union H` has no perfect matching which uses a nonempty proper
   subset of `M_0`.

Then `H` is disconnected.  Consequently, for arbitrary two-endpoint
tensors on the edges of `H`, its perfect-matching tensor factors across a
nontrivial vertex cut and has flattening rank at most one across that cut.

**Proof.**  A graph of maximum degree two in which every edge belongs to a
perfect matching is a disjoint union of even cycles and single matching
edges (parallel edges merely give a two-cycle).  If `H` were connected on
at least six vertices, it would therefore be an even cycle.  Let `M_1,M_2`
be its two alternating perfect matchings.

We recall directly why the properly three-edge-colored cubic multigraph
`M_0 union M_1 union M_2` has a fourth perfect matching using some, but not
all, edges of `M_0`.  View `H=M_1 union M_2` as a Hamilton cycle.  If an
`M_0`-chord joins opposite cycle parities, use it and match the two even
open paths left on the cycle.  If every `M_0`-chord joins equal parities,
the chords separately pair the even and odd positions.  An even chord and
an odd chord must interlace: otherwise the number of opposite-type
endpoints inside each chord first forces paired indices to agree modulo
two, then modulo four, and inductively modulo every power of two, which is
impossible in a finite nonempty matching.  Use an interlacing pair and
match the four even open paths along the cycle.  The resulting matching is
new.  The only case in which the construction can use all of `M_0` is the
four-vertex exception; since `|B|>=6`, it uses a nonempty proper subset.

This contradicts assumption 4, so `H` is disconnected.  If its components
have vertex sets `B_1,...,B_k`, where `k>=2`, unique componentwise
decomposition of perfect matchings gives

\[
                         H_B(A)=\bigotimes_{j=1}^k H_{B_j}(A). \tag{9}
\]

This is a simple tensor across `B_1 | (B\setminus B_1)`, proving the
flattening assertion. `QED`

Thus a support-level loop argument is sound in the degree-two cross graph:
it cannot produce a two-dimensional top excitation such as
`e_1^(tensor B)+e_2^(tensor B)`.  The unresolved case begins when the
active cross graph has degree at least three, or when proper connected
activities vanish only by cancellation rather than by absence of their
support.

## 5. Detection by the cubic-selector condition

For the three-color hafnian problem the eight-vertex example is not itself
a candidate minimal realization.  For example, at vertex `0` the closed
neighborhood is `\{0,1,4,5\}` and its edge boundary is only

\[
                         \{12,13,46,56\}.                 \tag{10}
\]

The six-edge closed-neighborhood theorem in
`notes/cubic-selector-reduction.md` therefore excludes this support from an
order-minimal exact realization.  The two facts fit together cleanly:
support-only loop reasoning fails, while the color-sensitive mixed-curvature
condition detects the failure.
