# A good-pair fan reduces the rigid branch to six ports

## 1. Outcome

Let an exact ternary source on an even set \(B\), \(|B|=N\), satisfy

\[
                         H_B(A)=\Delta_{B,3}.
\]

The aggregate-star count can be sharpened by a factor of two.  At least

\[
                         \boxed{\frac{N(N-7)}2}          \tag{1}
\]

unordered physical pairs have injective aggregate stars at both endpoints.
Consequently one vertex is the common endpoint of at least \(N-7\) such
pairs.  The proof uses the full mode flattening at one physical vertex:
only three incident neighbour subspaces can be essential under deletion.
It does not use the weaker six-deficiency count coming from a pair cap.

This larger fan gives an exact conditional reduction at \(N\geq16\).  Call
a good pair **regular nonbipartite** when its internal source Hessian has
only the vertex-gauge kernel and its internal rank-three graph is connected
and nonbipartite.  For a common-endpoint fan, either

1. at least \(N-15\) good pairs are not regular nonbipartite; or
2. three good neighbours \(u,v,w\) have literal zero direct blocks
   \(A_{ru}=A_{rv}=A_{rw}=0\), while the three rows at \(r\) are supported
   altogether on at most six other physical sites.  Each of \(u,v,w\)
   also has all three global colour rows supported on at most two sites.

The alternatives in item 1 are concrete: an extra internal Hessian kernel,
a disconnected internal rank-three graph, or a connected bipartite
rank-three graph.  Thus a proof which controls these escape charts may work
directly with item 2.

There is a stronger hereditary version at \(N\geq24\).  Either at least
\(N-23\) pairs in the fan are not regular nonbipartite, or the three
zero-block neighbours \(u,v,w\) in item 2 can be chosen **pairwise good**.
In the latter case all three star triples \(p,s,t\) in (2) are aggregate
injective after the three named endpoints are removed.

Item 2 has a cancellation-safe mixed elimination.  For any two of the
zero-block neighbours, say \(u,v\), put
\(W=B\setminus\{r,u,v\}\), write \(q\) for the quadratic internal to
\(W\), and orient all named endpoint blocks literally.  If \(N=2m\), then
all 27 triple contractions are

\[
 p_c\left(b_{de}q^{[m-2]}+s_dt_eq^{[m-3]}\right)
      =\delta_{c=d=e}X_c^W.                              \tag{2}
\]

Here \(p_c,s_d,t_e\) are respectively the rows from \(r,u,v\) into
\(W\), and \(b_{de}=A_{u\mid v}(d,e)\).  Both endpoint orders, parallel
aggregates, zero blocks, and arbitrary complex cancellation are retained.
All nine rows \(p_c,s_d,t_e\) have site support at most two.  Every
\(p_c\) has a local component on its corresponding target axis.  For
\(s_d\) and \(t_e\), the guaranteed global coordinate anchor either remains
in \(W\) or lies on the extracted direct block \(b\); the latter alternatives
make respectively a whole row or column of \(b\) diagonal-coordinate.

Let \(C\subset W\) be the union of the site supports of
\(p_0,p_1,p_2\); then \(|C|\leq6\).  A near-top tensor on \(W\) is a
direct sum of sectors indexed by its one missing physical site.  Since all
\(p_c\) are supported on \(C\), sectors missing a site outside \(C\) are
annihilated automatically.  Keeping only the other sectors and capping
\(W\setminus C\) gives exact tensors \(\overline R_{de}\) on at most six
ports satisfying

\[
                       p_c\overline R_{de}
                         =\delta_{c=d=e}X_c^C.           \tag{3}
\]

Equation (3) is not by itself contradictory: a three-port coordinate
model satisfies all 27 equations.  The remaining gate is therefore
precise.  One must use that, simultaneously for the three pairs among
\(u,v,w\), the nine responses in (3) are capped projections of the
factorized cofactors displayed in (2), built from the same physical edge
blocks.  An argument using only aggregate rank, the abstract response
table, or pair-chart exchange cannot finish the reduction.

## 2. Full mode span and deletion-essential neighbours

Orient an aggregate physical block with its named endpoint first and put

\[
 L_{u\leftarrow v}
   =\operatorname {im}\left(A_{u\mid v}:V_v^*\longrightarrow V_u\right),
 \qquad
 T_u=\sum_{v\ne u}L_{u\leftarrow v}.                    \tag{4}
\]

**Lemma 2.1 (full incident mode span).**  For every physical site \(u\),

\[
                              T_u=V_u.                  \tag{5}
\]

**Proof.**  If a nonzero \(\alpha\in V_u^*\) annihilated \(T_u\), then
contracting the source matching tensor at \(u\) by \(\alpha\) would give
zero: every perfect matching uses exactly one block incident with \(u\),
and its \(u\)-factor is killed.  The same contraction of the target is

\[
        \sum_{c=0}^2\alpha(e_c^{(u)})
               \bigotimes_{x\ne u}e_c^{(x)}.            \tag{6}
\]

The three displayed pure tensors are linearly independent, so every
\(\alpha(e_c^{(u)})\) is zero.  The three target axes form a basis of
\(V_u\), contradicting \(\alpha\ne0\).  \(\square\)

We use the following elementary dimension lemma.

**Lemma 2.2 (at most \(d\) deletion-essential subspaces).**  Let a finite
family of subspaces \((L_i)_{i\in I}\) span a \(d\)-dimensional vector
space \(V\).  Then at most \(d\) indices \(i\) have

\[
                         \sum_{j\ne i}L_j\ne V.         \tag{7}
\]

**Proof.**  For every such essential index \(i\), choose a covector
\(\phi_i\) which annihilates \(\sum_{j\ne i}L_j\) but not \(L_i\), and
choose \(x_i\in L_i\) with \(\phi_i(x_i)\ne0\).  For distinct essential
indices \(i,j\), one has \(\phi_i(x_j)=0\).  Thus the matrix
\((\phi_i(x_j))\) is diagonal with nonzero diagonal, so the vectors
\(x_i\) are linearly independent.  There are at most \(d\) of them.
\(\square\)

For distinct \(r,u\), call the directed pair \((r,u)\) deficient when

\[
                 \sum_{v\notin\{r,u\}}L_{u\leftarrow v}\ne V_u. \tag{8}
\]

This is exactly failure of injectivity of the aggregate star at \(u\)
after the physical pair \(\{r,u\}\) is deleted.  Lemmas 2.1--2.2 say that,
for each fixed \(u\), at most three choices of \(r\) are deficient.  There
are therefore at most \(3N\) directed deficiencies in total.

Every unordered pair which is not injective at both ends has at least one
deficient orientation.  Assign it to either such orientation.  Distinct
unordered pairs give distinct directed pairs, and hence

\[
 \#\{\text{both-injective unordered pairs}\}
     \geq {N\choose2}-3N=\frac{N(N-7)}2.                \tag{9}
\]

Their graph has average degree at least \(N-7\), proving the fan assertion.
This argument is over the original aggregate endpoint subspaces.  It never
selects a nonzero parallel source or infers termwise vanishing.

We will also use the hereditary consequence proved, with an independent
audit, in
[the target-flattening essential-star theorem](target-flattening-essential-star-pair-bound.md).
The graph of bad unordered pairs is \(4\)-degenerate.  Here is the short
reason.  Equality in Lemma 2.2 at an endpoint makes its three essential
subspaces independent lines and every other incident block zero, so such
an endpoint has bad degree at most three.  An induced bad graph of minimum
degree at least five can therefore contain no endpoint with three essential
neighbours.  Orient each bad edge toward one deficient endpoint.  Every
remaining endpoint receives at most two edges, giving at most \(2|D|\)
edges on an induced vertex set \(D\), whereas minimum degree five would
give at least \(5|D|/2\).  This contradiction proves \(4\)-degeneracy.

Consequently every vertex subset \(D\) contains a clique of good pairs of
size at least

\[
                              \left\lceil\frac{|D|}{5}\right\rceil. \tag{9a}
\]

Indeed, greedily \(5\)-colour the induced bad graph and take its largest
colour class.

## 3. A regular fan creates literal zero direct blocks

Fix a vertex \(r\), and for each colour \(c\) define the intrinsic global
row support

\[
       S_c(r)=\{x\ne r:\text{row }c\text{ of }A_{r\mid x}\ne0\}. \tag{10}
\]

If \(\{r,u\}\) is regular nonbipartite, the source-Hessian sparse-row
theorem applied to that pair gives

\[
                            |S_c(r)\setminus\{u\}|\leq2
                      \qquad(c=0,1,2).                  \tag{11}
\]

This is a conclusion from the complete off-diagonal pair equations, not a
support assumption.

**Lemma 3.1 (four deletions fix a two-site support).**  If a set \(F\) of
at least four neighbours satisfies (11) for every \(u\in F\), then

\[
                              |S_c(r)|\leq2              \tag{12}
\]

for every colour \(c\).

**Proof.**  A set of size at least four still has size at least three after
one deletion, contrary to (11).  A set of size exactly three satisfies
(11) only when every member of \(F\) lies in that three-set, which is
impossible for \(|F|\geq4\).  \(\square\)

It follows that

\[
                    C=\bigcup_{c=0}^2S_c(r),\qquad |C|\leq6. \tag{13}
\]

For every \(u\in F\setminus C\), all three endpoint rows vanish, so

\[
                               A_{ru}=0.                 \tag{14}
\]

In particular, \(|F|\geq9\) gives at least three literal zero blocks.

For every \(u\in F\setminus C\), apply the same sparse-row conclusion at
the other endpoint of the regular pair \(\{r,u\}\).  Since \(A_{ur}=0\),
deleting \(r\) removes no nonzero row of the \(u\)-star, and hence

\[
 \left|\{x\ne u:\text{row }d\text{ of }A_{u\mid x}\ne0\}\right|
      \leq2\qquad(d=0,1,2).                              \tag{14a}
\]

Thus every selected zero-block neighbour has aggregate support degree at
most six as well.

Take the fan of at least \(N-7\) good pairs furnished by (9), and let
\(F\) be its regular nonbipartite part.  If \(|F|\leq8\), at least

\[
                         (N-7)-8=N-15                  \tag{15}
\]

fan pairs lie in one of the three escape charts named in Section 1.  If
\(|F|\geq9\), equations (13)--(14) give item 2 of the outcome.  This proves
the claimed dichotomy for every \(N\geq16\).

For the hereditary sharpening, suppose \(N\geq24\).  If \(|F|\leq16\),
the fan has at least

\[
                         (N-7)-16=N-23                 \tag{15a}
\]

nonregular pairs.  If \(|F|\geq17\), the zero-block set
\(Z=F\setminus C\) has size at least eleven.  Equation (9a), applied
inside \(Z\), supplies three vertices \(u,v,w\) whose three mutual pairs
are all good.  This proves the stronger dichotomy stated in Section 1.

Aggregate injectivity has not been lost in the zero-block branch.  For
\(u\in F\setminus C\), the star from \(r\) after deleting \(u\) is the
same triple \((p_0,p_1,p_2)\), and it remains injective.  Hence the three
linear forms are independent in \(\bigoplus_{x\in C}V_x\), even though
each has site support at most two.

The diagonal first-contraction equations add a useful local fact which is
not contained in aggregate rank.

**Lemma 3.2 (two-hole coordinate anchor).**  Let \(U\) be any odd site
set, let \(F\in({\cal R}_U)_{|U|-1}\), and suppose a linear form
\(p=\sum_xp_x\), supported on at most two sites, satisfies

\[
                              pF=X_c^U.                 \tag{16a}
\]

If \(p\) is supported only at \(a\), then

\[
 p_a=\lambda e_c^{(a)},\qquad
 F_{\widehat a}=\lambda^{-1}X_c^{U\setminus\{a\}}       \tag{16b}
\]

for some \(\lambda\ne0\).  If its support is \(\{a,b\}\), then

\[
        p_a\in\mathbb C e_c^{(a)}
        \quad\hbox{or}\quad
        p_b\in\mathbb C e_c^{(b)}.                      \tag{16c}
\]

If exactly the first alternative holds, the hole-\(b\) sector of \(F\)
is divisible by \(e_c^{(a)}\); the symmetric statement holds for the
second alternative.

**Proof.**  Only a sector whose hole is a support site can survive
multiplication by \(p\).  The one-site assertion is therefore equality of
two nonzero simple tensors across the split
\(V_a\mid\bigotimes_{x\ne a}V_x\), which gives (16b).

For support \(\{a,b\}\), quotient the \(a\)-factor by
\(\mathbb Cp_a\) and the \(b\)-factor by \(\mathbb Cp_b\).  The two
summands \(p_aF_{\widehat a}\) and \(p_bF_{\widehat b}\) both vanish in
the double quotient.  The image of the right side of (16a) is

\[
  (e_c^{(a)}\bmod p_a)\otimes(e_c^{(b)}\bmod p_b)
       \otimes X_c^{U\setminus\{a,b\}}.
\]

It can vanish only if one of its first two nonzero-simple-tensor factors
vanishes, proving (16c).  If, for example, \(p_a\) is proportional to
\(e_c^{(a)}\) while \(p_b\) is not, quotient only the \(a\)-factor by
\(\mathbb Ce_c^{(a)}\).  The first summand and the target vanish.  Since
\(p_b\ne0\), the remaining equation says that the hole-\(b\) sector has
zero image in that quotient, which is the claimed divisibility.
\(\square\)

Apply the lemma to the exact first contraction at \(r\),

\[
                 p_c\left(A|_{B\setminus\{r\}}\right)^{[m-1]}
                    =X_c^{B\setminus\{r\}}.             \tag{16d}
\]

Thus every colour row at the sparse fan centre has a physical support site
at which its local vector is exactly on the corresponding target axis.
The three anchors may coincide, and a second noncoordinate support site is
still allowed; neither possibility is silently discarded below.

The identical argument at every \(u\in F\setminus C\), using (14a), gives
a target-coordinate anchor in each of its three sparse rows.  In
particular, after choosing \(u,v\) in Section 4, all nine rows
\(p_c,s_d,t_e\) have site support at most two.  The \(r\)-anchors remain
in \(W\), because both extracted blocks at \(r\) are zero.  An anchor of
the \(u\)-row \(d\) may instead be at \(v\); in that case

\[
                    b_{de}=0\ (e\ne d),\qquad b_{dd}\ne0. \tag{16e}
\]

Symmetrically, if the anchor of the \(v\)-row \(e\) is at \(u\), then

\[
                    b_{de}=0\ (d\ne e),\qquad b_{ee}\ne0. \tag{16f}
\]

These direct-block alternatives are retained rather than silently
assuming that every anchor survives in a triple star.

## 4. Exact triple-slice elimination

Choose distinct \(u,v\in F\setminus C\).  Thus

\[
                              A_{ru}=A_{rv}=0.           \tag{16}
\]

Put \(W=B\setminus\{r,u,v\}\).  In the site-square-zero algebra, decompose
the source quadratic according to the three named endpoints:

\[
 h=q+\sum_ce_c^{(r)}p_c+\sum_de_d^{(u)}s_d
       +\sum_ee_e^{(v)}t_e
       +\sum_{d,e}b_{de}e_d^{(u)}e_e^{(v)}.             \tag{17}
\]

The two omitted direct blocks in (16) are literally absent from (17).
All other blocks occur exactly once in their endpoint-oriented role.

**Proposition 4.1 (zero-block triple slice).**  The 27 contractions of
\(h^{[m]}\) at \((r,u,v)\) are exactly equation (2).

**Proof.**  In a perfect matching, either \(u\) is paired directly with
\(v\), after which \(r\) uses one star edge into \(W\), or all three named
vertices use star edges to three distinct sites of \(W\).  A direct edge
from \(r\) to \(u\) or \(v\) has zero aggregate block by (16), and there
is no other case.  The two surviving contributions are respectively

\[
             b_{de}p_cq^{[m-2]},\qquad
             p_cs_dt_eq^{[m-3]}.                       \tag{18}
\]

Divided powers count every residual internal matching once.  Contracting
the target at three named sites is zero unless their colours agree, and in
the agreeing case it is \(X_c^W\).  This proves (2).  \(\square\)

Equivalently, define the nine near-top cofactor responses

\[
             R^{uv}_{de}=b_{de}q^{[m-2]}+s_dt_eq^{[m-3]}.
                                                               \tag{19}
\]

Then

\[
                         p_cR^{uv}_{de}
                              =\delta_{c=d=e}X_c^W.      \tag{20}
\]

The same construction applies to the pairs \((u,w)\) and \((v,w)\).
Those three response tables share the same physical \(r\)-star and their
cofactor factors are redecompositions of the same aggregate edge family.

In the hereditary \(N\geq24\) branch, choose \(u,v,w\) pairwise good.
Then the star map represented by each of the triples \(p,s,t\) into
\(\bigoplus_{x\in W}V_x\) is injective.  For example, goodness of
\(\{u,v\}\) makes the \(u\)-star injective after deleting \(v\); its
additional component at \(r\) is zero because \(A_{ur}=0\), so the
remaining map is exactly the \(s\)-map into \(W\).  The other two cases
are identical.  Thus the strengthened triple slice retains three
independent sparse row frames, with the direct-block anchor alternatives
(16e)--(16f) still retained, not merely one injective frame.

## 5. Hole sectors leave an exact six-port core

The degree-\((|W|-1)\) component has the direct physical-hole
decomposition

\[
 ({\cal R}_W)_{|W|-1}
     =\bigoplus_{x\in W}\bigotimes_{y\in W\setminus\{x\}}V_y. \tag{21}
\]

Write \(R=\sum_xR_{\widehat x}\) accordingly.  Multiplication by
\(p_c=\sum_{x\in C}p_{c,x}\) gives

\[
                       p_cR=\sum_{x\in C}p_{c,x}R_{\widehat x}. \tag{22}
\]

Indeed, a term \(p_{c,x}R_{\widehat y}\) vanishes unless \(x=y\): for
\(x\ne y\), the sector already occupies site \(x\).  In particular all
sectors whose hole lies outside \(C\) are invisible to every one of the
three rows.

Let \(D=W\setminus C\), choose
\(K\in(\bigotimes_{y\in D}V_y)^*\), and cap the \(D\)-factors of the
sectors retained in (22).  Denote the resulting degree-\((|C|-1)\) tensor
by \(\overline R^K\).  Applying this operation to (20) gives

\[
 p_c\overline R^{uv,K}_{de}
   =\delta_{c=d=e}K(X_c^D)X_c^C.                       \tag{23}
\]

Take at each site of \(D\) a covector which has value one on all three
target axes, and let \(K\) be their product.  Then all three scalars in
(23) equal one, proving (3).  Product capping is used only for this
normalization; (23) is valid for arbitrary, possibly entangled, \(K\).

No information about the factorization (19) was discarded before the cap:
\(\overline R^{uv,K}_{de}\) is the literal capped projection of its two
displayed common-edge terms.  What is discarded is the automatically
annihilated hole sector, which cannot occur in any equation (20).

## 6. Sharpness and the remaining common-cofactor gate

The abstract six-port response (3) is consistent.  On
\(C=\{0,1,2\}\), put

\[
             p_c=e_c^{(c)},\qquad
             \overline R_{de}=0\ (d\ne e),\qquad
             \overline R_{dd}=\bigotimes_{x\ne d}e_d^{(x)}. \tag{24}
\]

If \(c=d\), multiplication inserts the missing factor and gives \(X_c^C\).
If \(c\ne d\), the factor \(p_c\) is placed at a site already occupied by
\(\overline R_{dd}\), so the product is zero.  Thus all 27 equations (3)
hold exactly and the three \(p_c\)'s are aggregate-independent.

Model (24) is not claimed to arise from a physical source.  It retains the
entire projected response table but supplies no common \(q,s,t,b\) whose
cofactors satisfy (19), and supplies no compatibility among the three
choices \(uv,uw,vw\).  This is exactly why an abstract rank or response
argument stops here.

The next conjecture-level lemma can now be stated without ambiguity:
exclude the simultaneous three-neighbour realization of (23) by the
capped common-edge factorizations (19), or show that its existence forces
one of the Hessian/disconnected/bipartite escape charts in (15).  Either
conclusion would convert the good-pair incidence theorem into a genuine
uniform descent mechanism.

## 7. Exact audit

The standalone checker
[verify_good_pair_fan_six_port_triple_cofactor_reduction.py](../computations/verify_good_pair_fan_six_port_triple_cofactor_reduction.py)

* exhausts every subspace family in \(\mathbb F_2^3\) and verifies the
  deletion-essential bound of Lemma 2.2;
* checks the count (9), fan threshold, support lemma, zero-block count, and
  both dichotomies for a range of even orders, including the hereditary
  \(4\)-degenerate good-clique bound;
* enumerates perfect matchings at orders \(8,10,12\) and verifies the two
  disjoint matching classes in Proposition 4.1, including their exact
  double-factorial counts;
* checks named-endpoint orientation under every numerical ordering of the
  three deleted vertices;
* exhausts the two-site tangent-space test behind Lemma 3.2 over
  \(\mathbb F_2\);
* audits the physical-hole rule (22); and
* verifies all 27 equations in the sharp abstract response (24).

The finite checks audit the displayed algebra and ledgers.  Lemmas
2.1--3.2 and Proposition 4.1 are the uniform proofs.
