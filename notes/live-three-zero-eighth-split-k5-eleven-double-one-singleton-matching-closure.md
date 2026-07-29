# The eighth split at \(k=5\): eleven-double matching closure

## 1. Result

At \((h,k,M)=(8,5,23)\), the collision profile

\[
                              2^{11}1                       \tag{1}
\]

is impossible on the no-extra-singular stratum.

Choose five double values as formal double layers.  All-order formal-five
duality gives a relation pencil in the cubics.  Its singleton row cuts the
cubic space to a three-space, and every one of the six outside-double rows
restricts to the same line in the dual of that three-space.  Fix two outside
doubles.  A fourth Boolean difference over four disjoint selection swaps
then puts a homogeneous quadratic relation on the four edge labels of every
near-perfect matching of the remaining nine doubles.  Quadratic fibres
make the zero-labelled edges matchings, while an exact \(K_7\) incidence
rank calculation removes every noncommon zero.  The resulting projective
edge-label system on \(K_9\), even with its one possible missing edge, is
inconsistent.

Only the standing structural assumptions are used: repeated exceptional
values are nonzero, distinct exceptional values are distinct and
pairwise nonopposite, and no exceptional value meets \(\pm\mu\).  The sole
singleton may be zero.

## 2. The cubic relation pencil

Let \({\cal D}\) be the eleven double values and let \(r\) be the singleton
value.  Choose a five-set \(T\subset {\cal D}\), put

\[
 Q_T(z)=\prod_{t\in T}(z+t),\qquad
 C_T(z)=\prod_{u\in {\cal D}\setminus T}(z-u).             \tag{2}
\]

Every formal-five pair drop is legal: the two lowered double layers leave
two nonzero singleton mates.  The complementary polynomial is

\[
                         A_T(z)=C_T(z)^2(z-r),              \tag{3}
\]

of degree thirteen with seven distinct roots.  The all-order formal-five
duality theorem therefore gives an exact two-dimensional relation space

\[
                         {\cal S}_T\subset\mathbb C[z]_{\le3}. \tag{4}
\]

For every \(S\in{\cal S}_T\), the associated rational derivative is

\[
 G_S'(z)=
 { (z+\mu)^5Q_T(z)^2S(z)\over C_T(z)^3(z-r)^2}.             \tag{5}
\]

At the order-two pole \(r\), its zero residue is

\[
                         S'(r)+\mathcal A_T S(r)=0,         \tag{6}
\]

where \(\mathcal A_T\) denotes the logarithmic derivative at \(r\) of the regular
factor in (5).  At an outside double \(u\in O_T={\cal D}\setminus T\),
write

\[
 B_{T,u}(z)={ (z+\mu)^5Q_T(z)^2\over
   \displaystyle\prod_{w\in O_T\setminus\{u\}}(z-w)^3(z-r)^2},
 \quad
 Y_T(u)={B_{T,u}'(u)\over B_{T,u}(u)},\quad
 J_T(u)=\left({B_{T,u}'\over B_{T,u}}\right)'\!(u).        \tag{7}
\]

The order-three residue row is

\[
 S''(u)+2Y_T(u)S'(u)+\bigl(Y_T(u)^2+J_T(u)\bigr)S(u)=0.    \tag{8}
\]

The singleton row (6) and the row (8) at a distinct node are independent.
Since both annihilate the plane (4), every outside-double row restricts to
the same nonzero line on the three-dimensional kernel of (6).

## 3. One exact quotient-row minor

Use \(w=z-r\), and write \(x=u-r\).  On the kernel of (6), use the basis

\[
                         1-\mathcal A_Tw,\qquad w^2,\qquad w^3. \tag{9}
\]

Put \(p=Y_T(u)\) and \(U=p^2+J_T(u)\).  The restriction of (8) in this
basis is

\[
\begin{aligned}
 h_u&=U-\mathcal A_T(2p+xU),\\
 \ell_{2,u}&=2+4xp+x^2U,\\
 \ell_{3,u}&=6x+6x^2p+x^3U.                              \tag{10}
\end{aligned}
\]

Fix two outside doubles \(u,v\), put \(y=v-r\), and use \(q=Y_T(v)\),
\(V=q^2+J_T(v)\) in the analogous formulas.  Proportionality of the two
restricted rows gives, in particular,

\[
 M_T(u,v):=\ell_{2,u}\ell_{3,v}-\ell_{3,u}\ell_{2,v}=0.   \tag{11}
\]

The logarithmic jet at a fixed outside double is affine in the selected
five-set:

\[
 Y_T(u)=\kappa_u+\sum_{t\in T}\Phi_u(t),\qquad
 \Phi_u(t)={2\over u+t}+{3\over u-t}
           ={5u+t\over u^2-t^2}.                          \tag{12}
\]

The derivative jet \(J_T(u)\) is affine as well.  Its precise increments
will cancel below.

Remove \(u,v\) from \({\cal D}\).  Given any four-edge matching

\[
                 \{a_1b_1,a_2b_2,a_3b_3,a_4b_4\}          \tag{13}
\]

on eight of the remaining nine values, keep the ninth value selected and,
independently in every pair, select one endpoint and leave the other
outside.  These are sixteen legal five/six partitions, so (11) vanishes at
all vertices of the Boolean four-cube.  Orient the swaps and put

\[
 \alpha_i=\Phi_u(a_i)-\Phi_u(b_i),\qquad
 \beta_i =\Phi_v(a_i)-\Phi_v(b_i).                         \tag{14}
\]

The fourth mixed difference of (11) is exact:

\[
 \Delta_1\Delta_2\Delta_3\Delta_4 M
 =-4x^2y^2(x-y)
   \sum_{1\le i<j\le4}\alpha_i\alpha_j
                 \prod_{k\notin\{i,j\}}\beta_k.          \tag{15}
\]

Indeed, the degree-four part of (11) is
\(x^2y^2(y-x)p^2q^2\); every term involving either affine derivative jet
has Boolean degree at most three.  Since \(x,y,x-y\ne0\), every four-edge
matching \({\cal M}\) on the remaining \(K_9\) satisfies

\[
 H({\cal M}):=
 \sum_{\{e,f\}\subset\mathcal M}\alpha_e\alpha_f
       \prod_{g\in\mathcal M\setminus\{e,f\}}\beta_g=0. \tag{16}
\]

Reversing one oriented edge changes both of its increments by a sign and
does not affect the zero assertion.

## 4. Removing zero increments

For distinct \(a,b\), direct subtraction in (12) gives

\[
 \Phi_u(a)-\Phi_u(b)=
 { (a-b)\bigl(ab+5u(a+b)+u^2\bigr)\over
   (u^2-a^2)(u^2-b^2)}.                                  \tag{17}
\]

Every fibre of \(\Phi_u\) has size at most two, because
\(\Phi_u(t)=\lambda\), after clearing its nonzero structural denominator,
is a nonzero polynomial of degree at most two.  Hence the \(\alpha\)-zero
edges form a matching; the same holds for the \(\beta\)-zero edges.

Suppose \(e\) is an \(\alpha\)-zero edge but \(\beta_e\ne0\).  Delete its
two endpoints.  On the remaining \(K_7\), let \(Z\) be the matching of
the other \(\alpha\)-zero edges, so \(|Z|\le3\).  For every three-edge
matching \(N\) avoiding \(Z\), equation (16) for \(N\cup\{e\}\) reduces
to

\[
 \sum_{f\in N}{\beta_f\over\alpha_f}=0.                  \tag{18}
\]

The incidence matrix whose rows are the three-matchings of
\(K_7\setminus Z\) and whose columns are its edges has full column rank.
For \(|Z|=0,1,2,3\), its exact ranks and column counts are

\[
\begin{array}{c|rrrr}
 |Z|&0&1&2&3\\ \hline
 \operatorname{rank}&21&20&19&18.
\end{array}                                               \tag{19}
\]

Thus (18) forces \(\beta_f=0\) on every edge outside \(Z\), contradicting
the fact that the \(\beta\)-zero graph is a matching.  Interchanging
\(\alpha,\beta\) proves that every zero of either increment is a common
zero.

There is at most one common-zero edge.  Indeed, (17) at both \(u\) and
\(v\) gives

\[
                         a+b=-{u+v\over5},\qquad ab=uv,    \tag{20}
\]

which determines the unordered pair \(\{a,b\}\).  Consequently all edges
of the remaining \(K_9\), except possibly one edge \(e_0\), have a
well-defined nonzero projective label

\[
                              R_e={\alpha_e\over\beta_e}.  \tag{21}
\]

For every four-matching avoiding \(e_0\), (16) becomes

\[
                              e_2(R_e:e\in\mathcal M)=0. \tag{22}
\]

## 5. The one-forbidden-edge matching lemma

**Lemma 5.1.**  There is no nonzero edge-labeling of
\(K_9\setminus\{e_0\}\), where \(e_0\) is absent or is one edge, for which
(22) holds on every four-matching avoiding \(e_0\).

**Proof.**  Choose a four-matching avoiding \(e_0\).  One of its
three-edge submatchings has labels \((a,b,c)\) for which

\[
 e_1(a,b,c),e_2(a,b,c)\quad\hbox{are not both zero}.       \tag{23}
\]

Otherwise the four triple sums \(e_1=0\) would make all four nonzero edge
labels equal and then give \(3a=0\).  Among the three edges in (23), choose
two, called \(A,B\), such that

\[
                              a^2+ab+b^2\ne0.              \tag{24}
\]

If all three pair expressions vanished, their nonzero ratios would be the
two primitive cube roots and \((a,b,c)\) would itself have
\(e_1=e_2=0\).

Let \(S\) be the five vertices not incident to \(A\cup B\).  For any
allowed edge of the induced \(K_5\) on \(S\), the matching triple with
\(A,B\) is nonexceptional by (24).  Extending it by each allowed edge of
its complementary triangle in (22) shows that triangle is monochromatic.
These triangle equalities form a connected relation graph on
\(E(K_5)\setminus\{e_0\}\), so all allowed edges inside \(S\) have one
nonzero label \(t\).

The triples with labels \((a,t,t)\) and \((b,t,t)\) are nonexceptional:
if their first elementary sum vanished, their second would be
\(-3t^2\ne0\).  Using two disjoint internal edges of \(S\) therefore shows
that every allowed \(A\)-to-\(S\) edge has label \(a\), and every allowed
\(B\)-to-\(S\) edge has label \(b\).  Finally, triples of the form
\((a,b,t)\) are nonexceptional by (24).  Choosing such triples so that
their complementary triangles contain both a cross edge and an internal
edge gives

\[
                              a=b=t.                      \tag{25}
\]

All choices can avoid the one forbidden edge: relative to \(A,B,S\), it
has only the four positions \(A\)--\(B\), \(A\)--\(S\), \(B\)--\(S\), or
inside \(S\); \(K_4\) minus one edge always has a perfect matching, and
the five vertices of \(S\) leave a spare choice at every cross step.
The exact finite audit checks every individual placement.

Now take \(A,B\) and any allowed two-matching inside \(S\).  Its four
labels are all \(t\), so (22) says

\[
                              0=e_2(t,t,t,t)=6t^2,          \tag{26}
\]

contrary to \(t\ne0\).  This proves the lemma. \(\square\)

Lemma 5.1 contradicts (22), proving that profile (1) is impossible.

## 6. Exact audit

[verify_live_three_zero_eighth_split_k5_eleven_double_one_singleton_matching_closure.py](../computations/verify_live_three_zero_eighth_split_k5_eleven_double_one_singleton_matching_closure.py)
checks the formal-five degrees, both residue-row formulas, the quotient-row
coordinates, the full fourth Boolean difference including cancellation of
all base and derivative-jet terms, the quadratic fibre and common-zero
identities, all four \(K_7\) incidence ranks, and the forbidden-edge
propagation for every admissible placement.
