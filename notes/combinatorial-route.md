# Support/cancellation route

## 1. Exact aggregation (parallel sources and asymmetric colors retained)

Fix an ordering of \(B\).  For \(u<v\) and palette colors \(i,j\), put

\[
 X_{uv}(i,j)=\sum_{\substack{a\in A:\N(a)=\{u,v\}\\
                 k(a,u)=i,\ k(a,v)=j}}w(a).
\]

Thus \(X_{uv}\in V_u\otimes V_v\cong\mathbb C^{q\times q}\) is an
arbitrary matrix; no symmetry between its two indices is asserted.  Then,
for every coloring \(c\),

\[
 w_G(c)=\sum_{M\in\operatorname{PM}(B)}
              \prod_{uv\in M}X_{uv}(c(u),c(v)).                 \tag{1}
\]

Indeed, after fixing the underlying perfect matching \(M\), expanding the
product on the right chooses independently one parallel source above every
pair of \(M\), with exactly its source weight.  This is a bijection with the
terms in the original definition.  Conversely, any finite collection of
matrices \(X_{uv}\) is realized by using one decorated source for every
nonzero matrix entry.  Consequently, parallel-source cancellation is fully
and exactly captured by the matrices, including asymmetric endpoint colors.

Write \(\mathcal H_B(X)\) for the tensor in (1).  The conjectural upper bound
for \(q=3\) asks whether

\[
 \mathcal H_B(X)=D_{3,n}:=\sum_{i=0}^2 e_i^{\otimes n}.          \tag{2}
\]

Restriction to any three colors shows that excluding (2) for \(q=3\)
excludes every \(q>3\) as well.

## 2. A six-vertex cancellation-mate lemma

The following is a support consequence that survives arbitrary complex
weights and arbitrary asymmetric entries elsewhere.

**Lemma (a fourth decorated matching is forced).**  Suppose \(n=6\), and
choose three colors \(0,1,2\).  For each \(i\), choose a perfect matching
\(M_i\) for which every selected diagonal entry \(X_{uv}(i,i)\), \(uv\in
M_i\), is nonzero.  Then the nine selected decorated occurrences contain a
perfect matching \(H\) whose inherited coloring \(c_H\) is nonconstant.  If
\(\mathcal H_B(X)=D_{3,6}\), there is a second perfect matching \(H'\ne H\)
compatible with \(c_H\), having nonzero monomial weight.  In particular,
\(H'\) uses at least one nonzero decorated matrix entry outside the nine
selected occurrences.

**Proof.**  Consider first two of the matchings, with their occurrences
remembering their two distinct colors.  Their union is a disjoint union of
even alternating cycles; a common underlying pair counts as a doubled
2-cycle.  If some pair \(M_i,M_j\) has at least two such components, take
the \(M_i\)-edges on a nonempty proper collection of components and the
\(M_j\)-edges on the rest.  This is a perfect matching \(H\), all of whose
entries are nonzero, and its coloring uses both \(i\) and \(j\).

It remains to consider the case in which the union of every pair is one
alternating Hamilton cycle.  The three underlying matchings are then
pairwise edge-disjoint.  Label the Hamilton cycle \(M_0\cup M_1\) cyclically
by \(0,1,\ldots,5\).  Every edge of \(M_2\) is a chord.  The even and odd
cycle vertices both have odd cardinality, so \(M_2\) cannot pair only
vertices of the same cycle parity.  It therefore has an edge joining
opposite parities.  A non-cycle edge of \(C_6\) joining opposite parities is
an opposite chord, say \(03\).  Removing \(0,3\) leaves the two cycle edges
\(12\) and \(45\); hence
\[
 H=\{03,12,45\}
\]
is a fourth perfect matching.  It uses an \(M_2\)-occurrence and cycle
occurrences, so its inherited coloring is nonconstant.

In either case, the monomial contributed by \(H\) to \(w_G(c_H)\) is
nonzero.  But \(w_G(c_H)=0\).  A sum containing one nonzero summand can
vanish only if it contains at least one further nonzero summand; this gives
\(H'\ne H\).  Finally, among the nine selected occurrences each vertex has
exactly one incident occurrence of each requested color.  Thus \(c_H\)
uniquely determines \(H\) inside those nine occurrences, and \(H'\) must
use occurrences outside them.  In fact, a perfect matching \(H'\ne H\) on
six vertices can share at most one edge with \(H\) (sharing two forces the
last edge), so at least two of its three decorated entries lie outside the
nine. \(\square\)

Because each constant coefficient is \(1\), at least one nonzero matching
monomial \(M_i\) can always be selected for each color.  Hence every putative
six-vertex, three-color solution has the forced support proliferation in the
lemma.  In particular, its aggregate support has at least eleven nonzero
decorated entries (the nine selected diagonal occurrences plus two outside
occurrence).  What is not yet proved is that iterating these cancellation
mates must terminate in a uniquely supported mixed coefficient.

## 3. An exact border degeneration at \(n=6,q=3\)

The nearly singular numerical solutions are explained by the following
exact family.  Let \(B=\{0,1,2,3,4,5\}\), let \(t\ne0\), and use only the
following nine diagonal decorated entries (an entry \(uv:i,z\) means
\(X_{uv}(i,i)=z\)):

\[
\begin{array}{c|ccc}
 i=0&04:1&12:t&35:t^{-1}\\
 i=1&05:t^{-1}&14:t^{-1}&23:t^2\\
 i=2&03:t&15:1&24:t^{-1}.
\end{array}                                                     \tag{3}
\]

All omitted entries are zero.  The three rows of (3) are perfect matchings

\[
 M_0=\{04,12,35\},\quad M_1=\{05,14,23\},\quad
 M_2=\{03,15,24\},
\]

each having weight exactly \(1\).  Their union is the triangular prism and
has exactly one further perfect matching,

\[
 H=\{04,15,23\}.
\]

(This can also be checked directly: vertex \(0\) has only the choices
\(03,04,05\), after each of which the remaining choices are forced except
that \(04\) permits precisely \(M_0\) and \(H\).)  The inherited coloring of
\(H\) is

\[
 c=(0,2,1,1,0,2),
\]

and its weight is \(1\cdot1\cdot t^2=t^2\).  Therefore the identity is
exactly

\[
 \boxed{\mathcal H_B(X(t))=D_{3,6}+t^2
 e_0\otimes e_2\otimes e_1\otimes e_1\otimes e_0\otimes e_2.} \tag{4}
\]

In particular, \(D_{3,6}\) lies in the coefficientwise (and projective)
closure of the matrix-valued-hafnian image, although no member of (3) with
finite \(t\ne0\) is monochromatic.  Thus **no polynomial identity in the
output tensor alone can prove the desired non-realizability**: every such
identity vanishing on all \(\mathcal H_B(X)\) also vanishes on their closure
and hence on \(D_{3,6}\).  A successful obstruction has to retain parameter
data (or distinguish the image from its closure).

This exactly matches the saved numerical candidate: its dominant entries
are the nine entries in (3), and its maximum residual is the product on
\(H\).  For example, in
`candidate_n6_q3_seed2.npz` that product is approximately

\[
 (-3.898179855)(-0.242389001)(-5.7789815\cdot10^{-6}),
\]

whose magnitude is the reported residual (up to the displayed rounding).

There is also a quantitative finite-versus-border certificate in this sparse
ansatz.  Give the nine entries arbitrary values, let \(p_i\) be the product
on \(M_i\), let \(r\) be the product on \(H\), and suppose every entry has
modulus at most \(R\ge1\).  Since the nine occurrences in \(p_0p_1p_2\)
split into the three occurrences of \(r\) and the other six occurrences,

\[
 |p_0p_1p_2|\le |r|R^6.                                        \tag{5}
\]

Hence if \(|p_i-1|\le\varepsilon<1\) and \(|r|\le\varepsilon\), then

\[
 R\ge \left(\frac{(1-\varepsilon)^3}{\varepsilon}\right)^{1/6}.\tag{6}
\]

Thus even in the exact support selected by the optimizer, convergence to
the target necessarily sends the parameter norm to infinity.  At a finite
point, all \(p_i=1\) makes every selected entry nonzero, so the sole mixed
coefficient \(r\) cannot vanish.

### Full-matrix rigidity on the prism support

The finite obstruction is not an artifact of taking diagonal rank-one
entries.

**Proposition (arbitrary prism matrices are impossible).**  Suppose the only
possibly nonzero aggregate matrices are on the nine edges in (3).  Even when
each of those matrices is an arbitrary \(3\times3\) complex matrix,
\(\mathcal H_B(X)\ne D_{3,6}\).

**Proof.**  Group the six local color spaces into
\[
 W_X=V_0\otimes V_4,\qquad W_Y=V_1\otimes V_5,\qquad
 W_Z=V_2\otimes V_3,
\]
and put \(d_i^X=e_i\otimes e_i\), with analogous notation in \(Y,Z\).
The target, under this grouping, is
\[
 D=\sum_{i=0}^2d_i^X\otimes d_i^Y\otimes d_i^Z.                \tag{7a}
\]
Let
\[
 x=X_{04}\in W_X,\qquad y=X_{15}\in W_Y,\qquad z=X_{23}\in W_Z
\]
be the three edges of the fourth prism matching.  The other two edges of
each color-class matching combine into tensors
\[
 B\in W_Y\otimes W_Z,\qquad C\in W_X\otimes W_Y,\qquad
 E\in W_X\otimes W_Z.
\]
Thus the four prism matchings give an identity of the form
\[
 D=x\otimes B+C\otimes z+E\otimes y+x\otimes y\otimes z.      \tag{7b}
\]
Scalars have simply been retained inside \(x,y,z,B,C,E\).

We first need a small quotient lemma.  If a three-term diagonal tensor
\(\sum_i d_i^X\otimes d_i^Y\otimes d_i^Z\) belongs to
\[
 x\otimes W_Y\otimes W_Z+
 W_X\otimes y\otimes W_Z+
 W_X\otimes W_Y\otimes z,                                    \tag{7c}
\]
then \(x,y,z\) are proportional to three *distinct* diagonal vectors
\(d_a^X,d_b^Y,d_c^Z\).

To prove this, quotient (7c) by the three displayed lines.  If bars denote
quotient images, then
\[
 \sum_i\bar d_i^X\otimes\bar d_i^Y\otimes\bar d_i^Z=0.         \tag{7d}
\]
The three \(\bar d_i^X\) span a space of dimension at least two.  Flattening
(7d) in the \(X\)-factor therefore says that the three products
\(\bar d_i^Y\otimes\bar d_i^Z\) span a space of dimension at most one.
If two of these products were nonzero and proportional, both corresponding
pairs \(\bar d_i^Y,\bar d_j^Y\) and
\(\bar d_i^Z,\bar d_j^Z\) would be proportional.  This forces both \(y\)
and \(z\) into
\(\operatorname{span}\{d_i,d_j\}\).  The third quotient vectors are then
nonzero and independent of those pairs, making the third product
nonzero and nonproportional, a contradiction.  Hence at most one product
is nonzero.  A one-dimensional quotient can kill \(d_i\) only when its
defining vector is proportional to that \(d_i\), and each of \(y,z\) can
kill at most one of the three independent diagonal vectors.  Consequently
they kill two distinct indices, and (7d) forces \(x\) to kill the remaining
index.  This proves the quotient lemma (and also shows none of \(x,y,z\)
can be zero).

Apply the lemma to (7b), and relabel colors so that
\[
 x=\alpha d_a^X,\qquad y=\beta d_b^Y,\qquad z=\gamma d_c^Z,
 \qquad \{a,b,c\}=\{0,1,2\},                                  \tag{7e}
\]
with all three scalars nonzero.  Quotient (7b) only in \(Y\) by \(y\) and
in \(Z\) by \(z\).  The \(C,E\), and fourth-matching terms die; on the
target side only index \(a\) survives.  Hence
\[
 B=\lambda\,d_a^Y\otimes d_a^Z+y\otimes P+Q\otimes z           \tag{7f}
\]
for some \(\lambda\ne0\), \(P\in W_Z\), and \(Q\in W_Y\).

Now use the extra structure that \(B\) is the product of the two individual
edge matrices \(X_{12}\) and \(X_{35}\).  Regroup its four factors across
\[
 (V_1\otimes V_2)\mid(V_3\otimes V_5).
\]
In this flattening, \(B=X_{12}\otimes X_{35}\) has matrix rank at most one.
In (7f), the \(\lambda\)-term gives a nonzero pivot at row
\((a,a)\), column \((a,a)\).  Since \(a,b,c\) are distinct, the
\(y\otimes P\) term is supported only on rows whose first coordinate is
\(b\) and columns whose second coordinate is \(b\), while the
\(Q\otimes z\) term is supported only on rows whose second coordinate is
\(c\) and columns whose first coordinate is \(c\).  Therefore the pivot's
entire row and column are zero away from the pivot.  A rank-one matrix with
a nonzero pivot satisfies
\[
 M_{r,s}=M_{r,s_0}M_{r_0,s}/M_{r_0,s_0},
\]
so every other entry is zero.  Thus
\[
 B=\lambda\,d_a^Y\otimes d_a^Z,
\]
and the two nonzero factors \(X_{12},X_{35}\) are each proportional to the
same-color basis edge \(e_a\otimes e_a\).

The two cyclically analogous quotient-and-pivot arguments show that the
cross edges belonging to the \(z\)-matching all have color \(c\), and those
belonging to the \(y\)-matching all have color \(b\).  Consequently the
first three terms in (7b) are supported only at the three constant grouped
colorings \((a,a,a),(c,c,c),(b,b,b)\).  The last term is the nonzero mixed
tensor
\[
 \alpha\beta\gamma\,d_a^X\otimes d_b^Y\otimes d_c^Z,
\]
which none of the first three can cancel.  This contradicts (7b).
\(\square\)

This proposition upgrades the sparse-chart obstruction from scalar or
rank-one edges to completely general asymmetric endpoint matrices.  Any
finite exact solution near the prism degeneration must introduce additional
underlying vertex pairs, not merely higher-rank entries on the prism.

## 4. Target-stabilizing torus and a support-minimality lemma

For nonzero scalars \(\lambda_{v,i}\), define

\[
 X'_{uv}(i,j)=\lambda_{u,i}\lambda_{v,j}X_{uv}(i,j).             \tag{7}
\]

Every monomial contributing to the coefficient of \(c\) is multiplied by
the same factor \(\prod_v\lambda_{v,c(v)}\).  It follows that (7) preserves
(2) whenever

\[
 \prod_{v\in B}\lambda_{v,i}=1\qquad\text{for every color }i.   \tag{8}
\]

This explains the many differently scaled versions of (4): a mixed error
is a nontrivial torus weight and can be driven to zero while the three
constant coefficients remain fixed.

The torus gives a rigorous necessary condition on a support-minimal exact
solution.  Let \(S\) be the support of all nonzero entries \(X_{uv}(i,j)\).
Associate to \(s=(uv;i,j)\in S\) the incidence vector

\[
 a_s=e_{u,i}+e_{v,j}\in\mathbb R^{B\times[3]}.
\]

**Lemma (balanced support).**  If an exact realization of (2) exists, choose
one with the minimum number of nonzero aggregate entries.  Then there are
strictly positive reals \(\alpha_s\), \(s\in S\), such that, for each fixed
color \(i\),

\[
 \sum_{s\in S}\alpha_s a_s(v,i)
\quad\text{is independent of }v.                               \tag{9}
\]

**Proof.**  Let

\[
 H=\{h\in\mathbb R^{B\times[3]}:\sum_vh(v,i)=0\text{ for every }i\}.
\]

If some \(h\in H\) had \(\langle h,a_s\rangle\ge0\) for every \(s\in S\),
with a strict inequality for at least one \(s\), applying (7) with
\(\lambda_{v,i}=t^{h(v,i)}\) and taking \(t\downarrow0\) would give a finite
limit which still realizes (2), by (8) and continuity, but has strictly
smaller support.  Thus no such \(h\) exists.  The strict theorem of
alternatives (equivalently, separation of the finitely generated cone after
orthogonal projection to \(H\)) gives positive \(\alpha_s\) with

\[
 \sum_s\alpha_s\operatorname{proj}_H(a_s)=0.
\]

Therefore \(\sum_s\alpha_sa_s\in H^\perp\).  The vectors in (H^\perp)
are exactly those whose coordinate is constant over \(v\), separately for
each color, which is (9). \(\square\)

The lemma retains asymmetric entries: an \(i,j\) entry contributes incidence
to color \(i\) at one endpoint and color \(j\) at the other.  It is a genuine
constraint beyond “every color has a perfect matching,” but by itself it
does not yet rule out a dense balanced support.

## 5. Exact contraction formula and why pair-deletion is not closed

Let \(u,v\in B\), \(U=B\setminus\{u,v\}\), and contract the \(u,v\) tensor
slots against any bilinear functional \(K\in(V_u\otimes V_v)^*\).  Put

\[
 s=\langle K,X_{uv}\rangle.
\]

For \(a<b\) in \(U\), let \(R_{ab}\in V_a\otimes V_b\) be the sum of the
two contractions corresponding to \(u\!-\!a,v\!-\!b\) and
\(u\!-\!b,v\!-\!a\):

\[
 R_{ab}=K\mathbin{\lrcorner}(X_{ua}\otimes X_{vb})
       +K\mathbin{\lrcorner}(X_{ub}\otimes X_{va}),             \tag{10}
\]

with tensor factors reordered to \(V_a\otimes V_b\).  Sorting perfect
matchings by the partners of \(u,v\) proves

\[
 K\mathbin{\lrcorner}\mathcal H_B(X)
 =s\,\mathcal H_U(X)
  +\sum_{a<b} R_{ab}\otimes
       \mathcal H_{U\setminus\{a,b\}}(X),                       \tag{11}
\]

where every term is placed in its natural vertex slots.

For \(K=\sum_i e_i^*\otimes e_i^*\), the left side of (11) contracts
\(D_{q,n}\) to \(D_{q,n-2}\).  However, the right side is only *linear* in
the effective edges \(R_{ab}\).  It is generally not
\(\mathcal H_U(C)\) for \(C_{ab}=s^\gamma X_{ab}+R_{ab}\), because expanding
that hafnian also produces matchings containing two or more \(R\)-edges;
those terms correspond to reusing the deleted vertices and are absent from
(11).  Thus the tempting deletion/contraction induction is not valid
without an additional lemma forcing all multi-\(R\) contributions to vanish
or cancel.

## 6. Diagonal specialization (complex cancellation still allowed)

If every aggregate matrix is diagonal, write \(x^i_{uv}=X_{uv}(i,i)\) and
\(h_i(S)=\operatorname{haf}(x^i[S])\), with \(h_i(\varnothing)=1\).  For a
coloring with classes \(S_i=c^{-1}(i)\), compatible matchings cannot cross
between classes, so (1) factors exactly as

\[
 w_G(c)=\prod_i h_i(S_i).                                       \tag{12}
\]

This formula does not assume positivity: every \(h_i(S_i)\) is the full
complex weighted matching sum.  In particular, monochromaticity implies

\[
 h_i(B)=1,
 \qquad
 \prod_i h_i(S_i)=0
 \quad\text{for every nonconstant even partition }(S_i).       \tag{13}
\]

The prism family shows that (13) can approach the forbidden point at
infinity even when every color subgraph is a single perfect matching.

### An exact cofactor counterexample

A tempting next claim is that, if \(h_i(B)\ne0\), the “active” edge set
\[
 R_i=\{e:x^i_e\ne0,\ h_i(B\setminus e)\ne0\}
\]
must contain a perfect matching.  This is false even on six vertices.
Partition the vertices into two triples \(L,R\).  Put weight \(1\) on all
six edges internal to the two triangles and put the same weight \(z\) on
all nine cross edges, where
\[
 z^2=-\frac12.
\]
There are nine perfect matchings with one cross edge and six with three
cross edges, so
\[
 h(B)=9z+6z^3=6z\ne0.                                         \tag{14}
\]
For a cross edge \(e\), its four-vertex cofactor consists of the two
internal edges or one of two cross pairings, and hence
\[
 h(B\setminus e)=1+2z^2=0.
\]
For an internal edge \(e\), the remaining lone vertex on that side can be
sent to any of the three vertices on the other side, after which the final
two vertices use their internal edge; hence
\[
 h(B\setminus e)=3z\ne0.
\]
Thus \(R\) is exactly the disjoint union of the two triangles.  It is an
edge cover, and every one of its edges extends to a support-perfect
matching, but \(R\) itself has no perfect matching.  Multiplying every edge
weight by any cube root of \((6z)^{-1}\) normalizes (14) to \(h(B)=1\)
without changing the zero pattern.  Therefore the edge-cover, extension,
and exact cofactor properties alone do not finish the diagonal case.

### The diagonal six-vertex case is nevertheless impossible

For (B=[6]), put

\[
 P_i=\{e:x^i_e\ne0\},\qquad
 q_i(e)=h_i(B\setminus e),\qquad
 R_i=\{e:x^i_eq_i(e)\ne0\}.
\]

Three support consequences of (13) are enough to finish this specialization.

1. (R_i) is an edge cover.  Indeed, expansion at any vertex (v) gives
   \[
   1=h_i(B)=\sum_{e\ni v}x^i_eq_i(e),
   \]
   so some edge of (R_i) meets (v).
2. The (R_i) are pairwise exclusive: (R_i\cap P_j=\varnothing) for
   (i\ne j).  Color the endpoints of (e) by (j) and the remaining
   four vertices by (i).  Equation (13) says
   (x^j_e q_i(e)=0); for (e\in R_i), (q_i(e)\ne0).
3. Every (e\in R_i) extends to a perfect matching of (P_i), since the
   nonzero sum (q_i(e)) contains at least one nonzero matching monomial.
   Conversely, the three (P_i) have no rainbow perfect matching.  Such a
   matching would define a (2+2+2) coloring whose coefficient is the
   single nonzero product of its three edge weights.

It remains a finite support lemma.

**Six-vertex support lemma.**  There do not exist graphs
(R_i\subseteq P_i\subseteq K_6), (i=0,1,2), such that each (R_i) is
an edge cover, (R_i\cap P_j=\varnothing) for (i\ne j), every edge of
(R_i) extends to a perfect matching of (P_i), and the (P_i) have no
rainbow perfect matching.

Here is a short exact exhaustive proof, retained as a machine-checkable
finite lemma rather than mistaken for the general theorem.  Shrink each
(R_i) to an inclusion-minimal edge cover.  There are (171) such covers
in labeled (K_6).  Enumerating disjoint triples with no rainbow matching
and quotienting by (S_6\times S_3) leaves exactly ten cases.  For each
case introduce the (45) Boolean variables ([e\in P_i]).  Unit clauses
encode (R_i\subseteq P_i) and cross-color exclusion.  The 90 negative
three-clauses (15 perfect matchings times 6 color bijections) forbid a
rainbow matching.  Finally, for each (e\in R_i), three selector variables
encode that one of the three pairings of (B\setminus e) lies in (P_i).
All ten formulas are unsatisfiable.  The complete enumerator and SAT audit
is `computations/verify_diagonal_n6_obstruction.py`; it uses no numerical
arithmetic and asserts both the orbit counts and every UNSAT result.

Consequently (13), and hence the original tensor equation, has no
(q=3,n=6) solution in which all aggregate edge matrices are diagonal.

## 7. Strongest conclusion and remaining gap

The concrete outcome is an exact explanation of the observed singular
search: \(D_{3,6}\) is a border matrix-hafnian tensor via (3)--(4), and the
finite obstruction on that support is the unique nonconstant prism matching.
This rules out any proof based only on Zariski-closed/output-tensor identities
and shows precisely why numerical residuals alone are misleading.

For a genuine exact solution, the coefficient of the prism's mixed coloring
could be canceled by additional matchings using asymmetric entries.  The
unresolved theorem-strength step is to prove that closing all such
cancellation chains is impossible at a finite balanced support satisfying
(9).  Formula (11) similarly shows that naive pair deletion does not bypass
that step.
